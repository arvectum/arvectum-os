#!/bin/sh
set -eu

LABEL="com.arvectum.os.p7-05-observer"
RUNTIME_ROOT=${ARVECTUM_P7_02_ROOT:-"$HOME/Library/Application Support/ArvectumOS/persistent-internal"}
LAUNCH_AGENT="$HOME/Library/LaunchAgents/$LABEL.plist"
DOMAIN="gui/$(id -u)"
TARGET="$DOMAIN/$LABEL"
INTERVAL=${ARVECTUM_P7_05_OBSERVER_INTERVAL_SECONDS:-60}
SERVICE_WAIT_ATTEMPTS=${ARVECTUM_P7_05_SERVICE_WAIT_ATTEMPTS:-20}
SERVICE_WAIT_INTERVAL=${ARVECTUM_P7_05_SERVICE_WAIT_INTERVAL:-0.5}

fail() { printf '%s\n' "P7.05 observer FAIL: $*" >&2; exit 1; }
info() { printf '%s\n' "P7.05 observer: $*"; }

assert_macos() {
  [ "$(uname -s)" = "Darwin" ] || fail "macOS is required for the selected-Mac observer adapter"
}

current_release() {
  [ -L "$RUNTIME_ROOT/current" ] || fail "P7.02 current release is not installed"
  basename "$(readlink "$RUNTIME_ROOT/current")"
}

release_python() {
  rel=$1
  printf '%s/venvs/%s/bin/python\n' "$RUNTIME_ROOT" "$rel"
}

release_observer() {
  rel=$1
  printf '%s/releases/%s/source/reference/python/p7_05_operational_visibility.py\n' "$RUNTIME_ROOT" "$rel"
}

current_python() {
  rel=$(current_release)
  release_python "$rel"
}

current_observer() {
  rel=$(current_release)
  release_observer "$rel"
}

is_loaded() {
  launchctl print "$TARGET" >/dev/null 2>&1
}

wait_unloaded() {
  i=0
  while is_loaded; do
    if [ "$i" -ge "$SERVICE_WAIT_ATTEMPTS" ]; then
      return 1
    fi
    i=$((i + 1))
    sleep "$SERVICE_WAIT_INTERVAL"
  done
  return 0
}

unload_observer() {
  if ! is_loaded; then
    return 0
  fi
  if ! launchctl bootout "$TARGET" >/dev/null 2>&1; then
    if ! is_loaded; then
      return 0
    fi
    return 1
  fi
  wait_unloaded
}

verify_plist_release_pin() {
  rel=$(current_release)
  py=$(release_python "$rel")
  script=$(release_observer "$rel")
  [ -f "$LAUNCH_AGENT" ] || fail "observer LaunchAgent is missing"
  "$py" - "$LAUNCH_AGENT" "$py" "$script" "$rel" <<'PY'
import plistlib
import sys

path, expected_python, expected_script, release = sys.argv[1:]
with open(path, "rb") as handle:
    payload = plistlib.load(handle)
args = payload.get("ProgramArguments")
if not isinstance(args, list) or len(args) < 2:
    raise SystemExit("observer ProgramArguments are invalid")
if args[0] != expected_python or args[1] != expected_script:
    raise SystemExit(
        f"observer release pin mismatch for {release}: python={args[0]!r} script={args[1]!r}"
    )
if "/current/" in args[1]:
    raise SystemExit("observer script must be pinned to an exact release, not current/")
PY
}

write_plist() {
  rel=$(current_release)
  py=$(release_python "$rel")
  script=$(release_observer "$rel")
  [ -x "$py" ] || fail "release Python is missing: $py"
  [ -f "$script" ] || fail "P7.05 implementation is missing from installed exact release $rel"
  mkdir -p "$RUNTIME_ROOT/service" "$RUNTIME_ROOT/logs" "$HOME/Library/LaunchAgents"
  chmod 700 "$RUNTIME_ROOT/logs"
  generated="$RUNTIME_ROOT/service/$LABEL.plist"
  "$py" - "$generated" "$LABEL" "$py" "$script" "$RUNTIME_ROOT" "$INTERVAL" \
    "$RUNTIME_ROOT/logs/p7-05-observer.stdout.log" \
    "$RUNTIME_ROOT/logs/p7-05-observer.stderr.log" <<'PY'
import plistlib, sys
path, label, py, script, root, interval, out, err = sys.argv[1:]
seconds = int(interval)
if seconds < 30:
    raise SystemExit("observer interval must be at least 30 seconds")
payload = {
    "Label": label,
    "ProgramArguments": [
        py, script, "observe", "--runtime-root", root, "--max-age-seconds", "20"
    ],
    "RunAtLoad": True,
    "StartInterval": seconds,
    "ProcessType": "Background",
    "StandardOutPath": out,
    "StandardErrorPath": err,
    "EnvironmentVariables": {"PYTHONDONTWRITEBYTECODE": "1"},
}
with open(path, "wb") as handle:
    plistlib.dump(payload, handle, sort_keys=True)
PY
  chmod 600 "$generated"
  plutil -lint "$generated" >/dev/null
  cp "$generated" "$LAUNCH_AGENT"
  chmod 600 "$LAUNCH_AGENT"
  verify_plist_release_pin
}

install_observer() {
  assert_macos
  command -v launchctl >/dev/null 2>&1 || fail "launchctl is unavailable"
  command -v plutil >/dev/null 2>&1 || fail "plutil is unavailable"
  write_plist
  unload_observer || fail "existing observer did not unload within bounded wait"
  launchctl bootstrap "$DOMAIN" "$LAUNCH_AGENT"
  launchctl kickstart "$TARGET" >/dev/null 2>&1
  is_loaded || fail "observer is not loaded after install"
  verify_plist_release_pin
  run_once >/dev/null
  info "install PASS release=$(current_release) interval=${INTERVAL}s"
}

uninstall_observer() {
  assert_macos
  unload_observer || fail "observer remains loaded after bounded uninstall wait"
  rm -f "$LAUNCH_AGENT"
  info "uninstall PASS"
}

run_once() {
  py=$(current_python)
  script=$(current_observer)
  "$py" "$script" observe --runtime-root "$RUNTIME_ROOT" --max-age-seconds 20
}

status_observer() {
  assert_macos
  is_loaded || fail "launchd observer is not loaded"
  verify_plist_release_pin
  py=$(current_python)
  script=$(current_observer)
  info "launchd observer loaded target=$TARGET release=$(current_release)"
  "$py" "$script" status --runtime-root "$RUNTIME_ROOT" --max-age-seconds 20
}

case "${1:-}" in
  install) install_observer ;;
  uninstall) uninstall_observer ;;
  run-once) run_once ;;
  status) status_observer ;;
  *)
    cat >&2 <<EOF
usage: $0 {install|uninstall|run-once|status}

The observer is an owner-local reversible launchd adapter. It has no network
listener, creates only non-canonical operational telemetry/alerts, and runs the
P7.05 retention cleanup on each observer cycle. Installed execution is pinned
to one exact runtime release and status fails closed on release-pin mismatch.
EOF
    exit 64
    ;;
esac
