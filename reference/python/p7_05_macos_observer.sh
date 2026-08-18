#!/bin/sh
set -eu

LABEL="com.arvectum.os.p7-05-observer"
RUNTIME_ROOT=${ARVECTUM_P7_02_ROOT:-"$HOME/Library/Application Support/ArvectumOS/persistent-internal"}
LAUNCH_AGENT="$HOME/Library/LaunchAgents/$LABEL.plist"
DOMAIN="gui/$(id -u)"
TARGET="$DOMAIN/$LABEL"
INTERVAL=${ARVECTUM_P7_05_OBSERVER_INTERVAL_SECONDS:-60}

fail() { printf '%s\n' "P7.05 observer FAIL: $*" >&2; exit 1; }
info() { printf '%s\n' "P7.05 observer: $*"; }

assert_macos() {
  [ "$(uname -s)" = "Darwin" ] || fail "macOS is required for the selected-Mac observer adapter"
}

current_release() {
  [ -L "$RUNTIME_ROOT/current" ] || fail "P7.02 current release is not installed"
  basename "$(readlink "$RUNTIME_ROOT/current")"
}

current_python() {
  rel=$(current_release)
  printf '%s/venvs/%s/bin/python\n' "$RUNTIME_ROOT" "$rel"
}

current_observer() {
  printf '%s/current/source/reference/python/p7_05_operational_visibility.py\n' "$RUNTIME_ROOT"
}

is_loaded() {
  launchctl print "$TARGET" >/dev/null 2>&1
}

write_plist() {
  py=$(current_python)
  script=$(current_observer)
  [ -x "$py" ] || fail "release Python is missing: $py"
  [ -f "$script" ] || fail "P7.05 implementation is missing from installed current release"
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
}

install_observer() {
  assert_macos
  command -v launchctl >/dev/null 2>&1 || fail "launchctl is unavailable"
  command -v plutil >/dev/null 2>&1 || fail "plutil is unavailable"
  write_plist
  if is_loaded; then
    launchctl bootout "$TARGET" >/dev/null 2>&1 || true
  fi
  launchctl bootstrap "$DOMAIN" "$LAUNCH_AGENT"
  launchctl kickstart "$TARGET" >/dev/null 2>&1 || true
  sleep 1
  run_once >/dev/null
  info "install PASS interval=${INTERVAL}s"
}

uninstall_observer() {
  assert_macos
  if is_loaded; then
    launchctl bootout "$TARGET" >/dev/null 2>&1 || fail "observer did not unload"
  fi
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
  py=$(current_python)
  script=$(current_observer)
  if is_loaded; then
    info "launchd observer loaded target=$TARGET"
  else
    info "launchd observer not loaded"
  fi
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
P7.05 retention cleanup on each observer cycle.
EOF
    exit 64
    ;;
esac
