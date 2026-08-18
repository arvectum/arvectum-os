#!/bin/sh
set -eu

ROOT=${ARVECTUM_P7_02_ROOT:-"$HOME/Library/Application Support/ArvectumOS/persistent-internal"}
LABEL="com.arvectum.os.p7-06-ui3-operator"
DOMAIN="gui/$(id -u)"
TARGET="$DOMAIN/$LABEL"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
SERVICE_COPY="$ROOT/service/$LABEL.plist"
LOG_DIR="$ROOT/logs"
HOST="127.0.0.1"
DEFAULT_PORT=${ARVECTUM_P7_06_UI3_PORT:-8765}
CREDENTIAL_ID=${ARVECTUM_P7_06_UI3_CREDENTIAL_ID:-}

fail() { printf '%s\n' "P7.06-UI3 FAIL: $*" >&2; exit 1; }
info() { printf '%s\n' "P7.06-UI3: $*"; }
assert_macos() { [ "$(uname -s)" = "Darwin" ] || fail "macOS is required"; }

current_release() {
  [ -L "$ROOT/current" ] || fail "current release symlink is missing"
  rel=$(basename "$(readlink "$ROOT/current")")
  [ "${#rel}" -eq 40 ] || fail "current release must be a full Git SHA"
  case "$rel" in *[!0-9a-f]*) fail "invalid release identity" ;; esac
  printf '%s\n' "$rel"
}

release_python() { printf '%s/venvs/%s/bin/python\n' "$ROOT" "$1"; }
release_script() { printf '%s/releases/%s/source/reference/python/p7_06_ui3_private_operator.py\n' "$ROOT" "$1"; }
release_shell() { printf '%s/releases/%s/source/reference/python/p7_06_ui3_macos_operator.sh\n' "$ROOT" "$1"; }
deploy_shell() { printf '%s/releases/%s/source/reference/python/p7_06_macos_deploy.sh\n' "$ROOT" "$1"; }

config_port() {
  rel=$1; py=$(release_python "$rel")
  "$py" - "$ROOT/config/p7-06-ui3.json" "$DEFAULT_PORT" <<'PY'
import json, sys
from pathlib import Path
path = Path(sys.argv[1])
if not path.exists():
    print(sys.argv[2]); raise SystemExit(0)
value = json.loads(path.read_text(encoding="utf-8"))
port = value.get("listener_port")
if not isinstance(port, int): raise SystemExit(1)
print(port)
PY
}

service_pid() {
  launchctl print "$TARGET" 2>/dev/null | awk '$1 == "pid" && $2 == "=" && $3 ~ /^[0-9]+$/ { print $3; exit }'
}

require_lsof() {
  command -v lsof >/dev/null 2>&1 || fail "lsof is required for bounded listener verification"
}

listener_matches() {
  port=$1; pid=$2
  own=$(lsof -nP -a -p "$pid" -iTCP:"$port" -sTCP:LISTEN 2>/dev/null || true)
  [ -n "$own" ] || return 1
  printf '%s\n' "$own" | awk -v port="$port" 'NR>1 { seen=1; if ($2 !~ /^[0-9]+$/ || $9 != "127.0.0.1:" port) bad=1 } END { exit (seen && !bad) ? 0 : 1 }' \
    || return 1
  all=$(lsof -nP -iTCP:"$port" -sTCP:LISTEN 2>/dev/null || true)
  printf '%s\n' "$all" | awk -v port="$port" -v pid="$pid" 'NR>1 { seen=1; if ($2 != pid || $9 != "127.0.0.1:" port) bad=1 } END { exit (seen && !bad) ? 0 : 1 }'
}

wait_listener_ready() {
  port=$1
  require_lsof
  i=0
  while [ "$i" -lt 80 ]; do
    pid=$(service_pid || true)
    if [ -n "$pid" ] && kill -0 "$pid" >/dev/null 2>&1 && listener_matches "$port" "$pid"; then
      return 0
    fi
    i=$((i + 1)); sleep 0.25
  done
  return 1
}

assert_port_free() {
  port=$1
  require_lsof
  existing=$(lsof -nP -iTCP:"$port" -sTCP:LISTEN 2>/dev/null || true)
  [ -z "$existing" ] || fail "configured UI3 private port $HOST:$port is already in use before launchd start"
}

wait_unloaded() {
  i=0
  while [ "$i" -lt 30 ]; do
    launchctl print "$TARGET" >/dev/null 2>&1 || return 0
    i=$((i + 1)); sleep 0.2
  done
  return 1
}

write_plist() {
  rel=$1; py=$(release_python "$rel"); script=$(release_script "$rel")
  [ -x "$py" ] || fail "exact-release Python missing"
  [ -f "$script" ] || fail "exact-release UI3 module missing"
  mkdir -p "$HOME/Library/LaunchAgents" "$ROOT/service" "$LOG_DIR"
  chmod 700 "$ROOT/service" "$LOG_DIR"
  : > "$LOG_DIR/p7-06-ui3.stdout.log"
  : > "$LOG_DIR/p7-06-ui3.stderr.log"
  chmod 600 "$LOG_DIR/p7-06-ui3.stdout.log" "$LOG_DIR/p7-06-ui3.stderr.log"
  cat > "$PLIST" <<EOF2
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>Label</key><string>$LABEL</string>
<key>ProgramArguments</key><array>
<string>$py</string><string>$script</string><string>serve</string>
<string>--runtime-root</string><string>$ROOT</string>
</array>
<key>RunAtLoad</key><true/>
<key>KeepAlive</key><true/>
<key>ProcessType</key><string>Background</string>
<key>StandardOutPath</key><string>$LOG_DIR/p7-06-ui3.stdout.log</string>
<key>StandardErrorPath</key><string>$LOG_DIR/p7-06-ui3.stderr.log</string>
</dict></plist>
EOF2
  chmod 600 "$PLIST"
  cp "$PLIST" "$SERVICE_COPY"
  chmod 600 "$SERVICE_COPY"
}

verify_plist_release_pin() {
  rel=$1; py=$(release_python "$rel"); script=$(release_script "$rel")
  python3 - "$PLIST" "$LABEL" "$py" "$script" "$ROOT" <<'PY'
import plistlib, sys
path, label, py, script, root = sys.argv[1:]
with open(path, "rb") as h: p = plistlib.load(h)
expected = [py, script, "serve", "--runtime-root", root]
if p.get("Label") != label or p.get("ProgramArguments") != expected:
    raise SystemExit(1)
for arg in p.get("ProgramArguments", []):
    if "/current/" in arg: raise SystemExit(1)
PY
}

verify_listener() {
  port=$1; pid=$2
  require_lsof
  own=$(lsof -nP -a -p "$pid" -iTCP:"$port" -sTCP:LISTEN 2>/dev/null || true)
  if [ -z "$own" ]; then
    all=$(lsof -nP -iTCP:"$port" -sTCP:LISTEN 2>/dev/null || true)
    [ -z "$all" ] || fail "configured UI3 private port $HOST:$port is owned by another listener"
    fail "UI3 launchd process has no private listener"
  fi
  printf '%s\n' "$own" | awk -v port="$port" 'NR>1 { seen=1; if ($2 !~ /^[0-9]+$/ || $9 != "127.0.0.1:" port) bad=1 } END { exit (seen && !bad) ? 0 : 1 }' \
    || fail "UI3 process listener exposure is not exactly 127.0.0.1:$port"
  all=$(lsof -nP -iTCP:"$port" -sTCP:LISTEN 2>/dev/null || true)
  printf '%s\n' "$all" | awk -v port="$port" -v pid="$pid" 'NR>1 { seen=1; if ($2 != pid || $9 != "127.0.0.1:" port) bad=1 } END { exit (seen && !bad) ? 0 : 1 }' \
    || fail "another process/listener shares the UI3 private port"
}

verify_private_material() {
  rel=$1; py=$(release_python "$rel")
  "$py" - "$ROOT" "$PLIST" "$SERVICE_COPY" "$LOG_DIR/p7-06-ui3.stdout.log" "$LOG_DIR/p7-06-ui3.stderr.log" <<'PY'
import os, plistlib, sys
from pathlib import Path
root, plist, service_copy, stdout_log, stderr_log = map(Path, sys.argv[1:])
config = root / "config" / "p7-06-ui3.json"
secret = root / "secrets" / "p7-06-ui3" / "access.secret"
checks = ((config, 16384), (secret, 4096), (plist, 65536), (service_copy, 65536), (stdout_log, 1048576), (stderr_log, 1048576))
for path, limit in checks:
    if path.is_symlink() or not path.is_file() or path.stat().st_size > limit:
        raise SystemExit(1)
    if os.name != "nt" and path.stat().st_mode & 0o077:
        raise SystemExit(1)
if plist.read_bytes() != service_copy.read_bytes():
    raise SystemExit(1)
with plist.open("rb") as handle:
    payload = plistlib.load(handle)
if payload.get("Label") != "com.arvectum.os.p7-06-ui3-operator":
    raise SystemExit(1)
secret_value = secret.read_text(encoding="utf-8").rstrip("\n")
if not secret_value or "\n" in secret_value or "\r" in secret_value:
    raise SystemExit(1)
secret_bytes = secret_value.encode("utf-8")
if secret_bytes in stdout_log.read_bytes() or secret_bytes in stderr_log.read_bytes():
    raise SystemExit(1)
PY
}

init_config() {
  rel=$1; port=$2; py=$(release_python "$rel"); script=$(release_script "$rel")
  if [ -n "$CREDENTIAL_ID" ]; then
    "$py" "$script" init --runtime-root "$ROOT" --host "$HOST" --port "$port" --credential-id "$CREDENTIAL_ID" >/dev/null
  else
    "$py" "$script" init --runtime-root "$ROOT" --host "$HOST" --port "$port" >/dev/null
  fi
}

stop_service() {
  if launchctl print "$TARGET" >/dev/null 2>&1; then
    launchctl bootout "$TARGET" >/dev/null 2>&1 || fail "could not unload UI3 launchd target"
    wait_unloaded || fail "UI3 launchd target did not unload"
  fi
}

cleanup_ui3_material() {
  rm -f "$PLIST" "$SERVICE_COPY" \
    "$ROOT/config/p7-06-ui3.json" \
    "$ROOT/secrets/p7-06-ui3/access.secret" \
    "$LOG_DIR/p7-06-ui3.stdout.log" "$LOG_DIR/p7-06-ui3.stderr.log"
  rmdir "$ROOT/secrets/p7-06-ui3" >/dev/null 2>&1 || true
}

install_service() {
  assert_macos
  rel=$(current_release)
  port=$(config_port "$rel")
  init_config "$rel" "$port"
  stop_service
  assert_port_free "$port"
  write_plist "$rel"
  verify_plist_release_pin "$rel" || fail "launchd plist is not exact-release pinned"
  launchctl bootstrap "$DOMAIN" "$PLIST"
  launchctl kickstart -k "$TARGET" >/dev/null 2>&1
  wait_listener_ready "$port" || fail "UI3 launchd process did not become private-listener ready"
  status_service >/dev/null
  info "install PASS release=$rel listener=$HOST:$port"
}

status_service() {
  assert_macos
  rel=$(current_release); py=$(release_python "$rel"); script=$(release_script "$rel")
  launchctl print "$TARGET" >/dev/null 2>&1 || fail "UI3 launchd target is not loaded"
  pid=$(service_pid || true)
  [ -n "$pid" ] && kill -0 "$pid" >/dev/null 2>&1 || fail "UI3 launchd process is not running"
  [ -f "$PLIST" ] || fail "UI3 launchd plist missing"
  verify_plist_release_pin "$rel" || fail "UI3 launchd target is not pinned to current exact release"
  "$py" "$script" verify --runtime-root "$ROOT" --exact-release >/dev/null
  verify_private_material "$rel" || fail "UI3 private material/log minimization verification failed"
  port=$(config_port "$rel")
  verify_listener "$port" "$pid"
  info "status PASS release=$rel listener=$HOST:$port pid=$pid"
}

restart_service() {
  assert_macos
  status_service >/dev/null
  port=$(config_port "$(current_release)")
  launchctl kickstart -k "$TARGET" >/dev/null 2>&1
  wait_listener_ready "$port" || fail "UI3 launchd process did not become private-listener ready after restart"
  status_service >/dev/null
  info "restart PASS; process-local browser session invalidated"
}

show_secret() {
  assert_macos
  rel=$(current_release); py=$(release_python "$rel"); script=$(release_script "$rel")
  "$py" "$script" verify --runtime-root "$ROOT" --exact-release >/dev/null
  secret="$ROOT/secrets/p7-06-ui3/access.secret"
  [ -f "$secret" ] || fail "UI3 ingress secret missing"
  cat "$secret"
}

rotate_secret() {
  assert_macos
  rel=$(current_release); py=$(release_python "$rel"); script=$(release_script "$rel")
  "$py" "$script" rotate-secret --runtime-root "$ROOT" >/dev/null
  if launchctl print "$TARGET" >/dev/null 2>&1; then
    port=$(config_port "$rel")
    launchctl kickstart -k "$TARGET" >/dev/null 2>&1
    wait_listener_ready "$port" || fail "UI3 launchd process did not become private-listener ready after secret rotation"
    status_service >/dev/null
  fi
  info "access secret rotated; prior process/browser session invalidated"
}

reconcile_after_deploy() {
  rel=$(current_release); script=$(release_script "$rel")
  if [ -f "$script" ]; then
    # This controller may be newer than the resulting release after rollback.
    # Keep lifecycle hardening in the invoking controller while pinning the
    # actual service Python/module/config verification to the exact current
    # release. Historical UI3 shell bugs must not be replayed as migration logic.
    install_service >/dev/null
    status_service >/dev/null
    info "deploy reconciliation PASS release=$rel UI3=installed-exact-release"
  else
    cleanup_ui3_material
    info "deploy reconciliation PASS release=$rel UI3=absent-in-release"
  fi
}

governed_update() {
  assert_macos
  [ -n "${1:-}" ] || fail "governed-update requires a decision reference"
  status_service >/dev/null
  rel=$(current_release); deploy=$(deploy_shell "$rel")
  [ -f "$deploy" ] || fail "exact-release P7.06 deploy adapter missing"
  stop_service
  rc=0
  sh "$deploy" update "$1" || rc=$?
  reconcile_after_deploy || fail "UI3 reconciliation failed after governed update"
  [ "$rc" -eq 0 ] || fail "governed P7.06 update failed; source UI3 state was reconciled"
  info "governed-update PASS"
}

governed_rollback() {
  assert_macos
  status_service >/dev/null
  rel=$(current_release); deploy=$(deploy_shell "$rel")
  [ -f "$deploy" ] || fail "exact-release P7.06 deploy adapter missing"
  stop_service
  rc=0
  sh "$deploy" rollback-last || rc=$?
  reconcile_after_deploy || fail "UI3 reconciliation failed after governed rollback"
  [ "$rc" -eq 0 ] || fail "governed P7.06 rollback failed; current UI3 state was reconciled"
  info "governed-rollback-last PASS"
}

uninstall_service() {
  assert_macos
  rel=$(current_release); py=$(release_python "$rel"); script=$(release_script "$rel")
  stop_service
  "$py" "$script" remove-private-material --runtime-root "$ROOT" >/dev/null
  cleanup_ui3_material
  info "uninstall PASS; UI3 config/ingress secret/logs removed; P7.04 grants/credentials unchanged"
}

usage() {
  cat <<EOF2
Usage: $0 install|status|stop|start|restart|show-access-secret|rotate-access-secret|uninstall
       $0 governed-update <decision-ref>
       $0 governed-rollback-last

P7.06-UI3 supervises an exact-release private owner workspace on 127.0.0.1 only.
It consumes existing P7.04 least-privilege grants and never creates authority,
approval, canonical mutation, public ingress, or a UI4 real-interaction provider.
Once UI3 is installed, use governed-update/governed-rollback-last so the private
process is stopped before P7.06 mutation and re-pinned/removed after its result.
EOF2
}

case "${1:-}" in
  install|start) install_service ;;
  status) status_service ;;
  stop) assert_macos; stop_service; info "stop PASS" ;;
  restart) restart_service ;;
  show-access-secret) show_secret ;;
  rotate-access-secret) rotate_secret ;;
  governed-update) governed_update "${2:-}" ;;
  governed-rollback-last) governed_rollback ;;
  uninstall) uninstall_service ;;
  *) usage; exit 2 ;;
esac
