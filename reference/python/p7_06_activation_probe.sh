#!/bin/sh
set -u

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
DEPLOY="$SCRIPT_DIR/p7_06_macos_deploy.sh"
RUNTIME_ROOT=${ARVECTUM_P7_02_ROOT:-"$HOME/Library/Application Support/ArvectumOS/persistent-internal"}
DOMAIN="gui/$(id -u)"
SERVICE_TARGET="$DOMAIN/com.arvectum.os.persistent-internal"
LOCK_FILE="$RUNTIME_ROOT/run/runtime.lock"
HEALTH_FILE="$RUNTIME_ROOT/run/health.json"
DECISION_REF=${1:-}

[ -n "$DECISION_REF" ] || { printf '%s\n' "P7.06 activation probe FAIL: decision-ref is required" >&2; exit 2; }
[ "$(uname -s)" = "Darwin" ] || { printf '%s\n' "P7.06 activation probe FAIL: macOS is required" >&2; exit 2; }
command -v launchctl >/dev/null 2>&1 || { printf '%s\n' "P7.06 activation probe FAIL: launchctl unavailable" >&2; exit 2; }
command -v lsof >/dev/null 2>&1 || { printf '%s\n' "P7.06 activation probe FAIL: lsof unavailable" >&2; exit 2; }
command -v ps >/dev/null 2>&1 || { printf '%s\n' "P7.06 activation probe FAIL: ps unavailable" >&2; exit 2; }

STAMP=$(date -u '+%Y%m%dT%H%M%SZ')
PROBE_DIR="$RUNTIME_ROOT/evidence/p7-06/activation-probe-$STAMP-$$"
mkdir -p "$PROBE_DIR"
chmod 700 "$PROBE_DIR"
SENTINEL="$PROBE_DIR/monitor.running"
: > "$SENTINEL"
chmod 600 "$SENTINEL"
SAMPLES="$PROBE_DIR/samples.tsv"
OWNERS="$PROBE_DIR/lock-owner-transitions.log"
printf '%s\n' 'timestamp	launch_pid	launch_state	lock_pids	health_release	health_pid	health_generation	health_state' > "$SAMPLES"
chmod 600 "$SAMPLES"
: > "$OWNERS"
chmod 600 "$OWNERS"

health_field() {
  field=$1
  [ -f "$HEALTH_FILE" ] || return 0
  python3 - "$HEALTH_FILE" "$field" <<'PY' 2>/dev/null || true
import json
import sys
path, field = sys.argv[1:]
try:
    with open(path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
except Exception:
    raise SystemExit(0)
value = payload.get(field, "")
if value is None:
    value = ""
print(value)
PY
}

monitor() {
  previous_owners="__initial__"
  while [ -f "$SENTINEL" ]; do
    ts=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
    launch=$(launchctl print "$SERVICE_TARGET" 2>/dev/null || true)
    launch_pid=$(printf '%s\n' "$launch" | awk '/^[[:space:]]*pid = / {print $3; exit}')
    launch_state=$(printf '%s\n' "$launch" | awk '/^[[:space:]]*state = / {print $3; exit}')
    lock_pids=""
    if [ -e "$LOCK_FILE" ]; then
      lock_pids=$(lsof -t "$LOCK_FILE" 2>/dev/null | sort -u | tr '\n' ',' | sed 's/,$//' || true)
    fi
    health_release=$(health_field release_sha)
    health_pid=$(health_field pid)
    health_generation=$(health_field generation)
    health_state=$(health_field state)
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
      "$ts" "${launch_pid:-}" "${launch_state:-}" "${lock_pids:-}" \
      "${health_release:-}" "${health_pid:-}" "${health_generation:-}" "${health_state:-}" >> "$SAMPLES"

    if [ "$lock_pids" != "$previous_owners" ]; then
      printf '%s lock_pids=%s\n' "$ts" "${lock_pids:-none}" >> "$OWNERS"
      old_ifs=$IFS
      IFS=','
      for pid in $lock_pids; do
        [ -n "$pid" ] || continue
        ps -p "$pid" -o pid=,ppid=,command= >> "$OWNERS" 2>/dev/null || true
      done
      IFS=$old_ifs
      previous_owners=$lock_pids
    fi
    sleep 0.2
  done
}

monitor &
MONITOR_PID=$!

set +e
sh "$DEPLOY" update "$DECISION_REF" > "$PROBE_DIR/update.stdout" 2> "$PROBE_DIR/update.stderr"
UPDATE_RC=$?
set -e

rm -f "$SENTINEL"
wait "$MONITOR_PID" 2>/dev/null || true

cat "$PROBE_DIR/update.stdout"
cat "$PROBE_DIR/update.stderr" >&2

ROLLBACK_RC="not-required"
if [ "$UPDATE_RC" -eq 0 ]; then
  printf '%s\n' "P7.06 activation probe: update reached target; rolling back to preserve diagnostic source state"
  set +e
  sh "$DEPLOY" rollback-last > "$PROBE_DIR/rollback.stdout" 2> "$PROBE_DIR/rollback.stderr"
  ROLLBACK_RC=$?
  set -e
  cat "$PROBE_DIR/rollback.stdout"
  cat "$PROBE_DIR/rollback.stderr" >&2
fi

set +e
sh "$DEPLOY" status > "$PROBE_DIR/final-status.stdout" 2> "$PROBE_DIR/final-status.stderr"
STATUS_RC=$?
set -e
cat "$PROBE_DIR/final-status.stdout"
cat "$PROBE_DIR/final-status.stderr" >&2

python3 - "$PROBE_DIR/manifest.json" "$DECISION_REF" "$UPDATE_RC" "$ROLLBACK_RC" "$STATUS_RC" <<'PY'
import json
import os
import sys
from datetime import datetime, timezone
path, decision_ref, update_rc, rollback_rc, status_rc = sys.argv[1:]
payload = {
    "schema": "arvectum.p7_06.activation-probe/1",
    "classification": "owner-local non-canonical operational diagnostics",
    "decision_ref": decision_ref,
    "update_exit_code": int(update_rc),
    "rollback_exit_code": rollback_rc if rollback_rc == "not-required" else int(rollback_rc),
    "final_status_exit_code": int(status_rc),
    "canonical_mutation_performed_by_probe": False,
    "product_external_effect_invoked": False,
    "historical_effect_replay_invoked": False,
    "recorded_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
}
with open(path, "w", encoding="utf-8") as handle:
    json.dump(payload, handle, ensure_ascii=False, sort_keys=True, indent=2)
    handle.write("\n")
os.chmod(path, 0o600)
PY

(
  cd "$PROBE_DIR" || exit 1
  shasum -a 256 manifest.json samples.tsv lock-owner-transitions.log update.stdout update.stderr final-status.stdout final-status.stderr > SHA256SUMS
  chmod 600 SHA256SUMS
)

printf '%s\n' "P7.06 activation probe COMPLETE update_rc=$UPDATE_RC rollback_rc=$ROLLBACK_RC status_rc=$STATUS_RC evidence=$PROBE_DIR"
[ "$STATUS_RC" -eq 0 ] || exit "$STATUS_RC"
exit 0
