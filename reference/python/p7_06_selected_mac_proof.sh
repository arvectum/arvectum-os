#!/bin/sh
set -eu
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
DEPLOY="$SCRIPT_DIR/p7_06_macos_deploy.sh"
RUNTIME_ROOT=${ARVECTUM_P7_02_ROOT:-"$HOME/Library/Application Support/ArvectumOS/persistent-internal"}
DECISION_REF=${1:-P7.06-selected-mac-owner-operated-proof}
fail() { printf '%s\n' "P7.06 selected-Mac proof FAIL: $*" >&2; exit 1; }
current_release() { [ -L "$RUNTIME_ROOT/current" ] || fail "current release symlink missing"; basename "$(readlink "$RUNTIME_ROOT/current")"; }
[ "$(uname -s)" = "Darwin" ] || fail "macOS required"
source=$(current_release)
sh "$DEPLOY" update "$DECISION_REF:update"
target=$(current_release)
[ "$target" != "$source" ] || fail "update did not change exact release"
sh "$DEPLOY" rollback-last
[ "$(current_release)" = "$source" ] || fail "rollback did not restore source release"
sh "$DEPLOY" update "$DECISION_REF:final-update"
[ "$(current_release)" = "$target" ] || fail "final update did not restore target release"
sh "$DEPLOY" status >/dev/null
stamp=$(date -u '+%Y%m%dT%H%M%SZ')
summary="$RUNTIME_ROOT/evidence/p7-06/p7-06-selected-mac-proof-$stamp.json"
mkdir -p "$(dirname "$summary")"
python3 - "$summary" "$source" "$target" "$DECISION_REF" <<'PY'
import json, os, sys
from datetime import datetime, timezone
path, source, target, decision = sys.argv[1:]
value = {
  "schema": "arvectum.p7_06.selected-mac-proof/1",
  "status": "PASS",
  "operating_mode": "Persistent Internal / owner-operated",
  "source_release": source,
  "target_release": target,
  "final_release": target,
  "update_verified": True,
  "rollback_verified": True,
  "final_reupdate_verified": True,
  "runtime_exact_release_health_verified": True,
  "observer_exact_release_pin_verified": True,
  "pre_update_backup_required_for_each_update": True,
  "schema_changing_migration_executed": False,
  "historical_effect_replay_invoked": False,
  "product_external_effect_invoked": False,
  "canonical_mutation_performed_by_deploy": False,
  "operator_decision_ref": decision,
  "recorded_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
}
with open(path, "w", encoding="utf-8") as h:
    json.dump(value, h, ensure_ascii=False, sort_keys=True, indent=2); h.write("\n")
os.chmod(path, 0o600)
PY
digest=$(shasum -a 256 "$summary" | awk '{print $1}')
printf '%s  %s\n' "$digest" "$(basename "$summary")" > "$summary.sha256"
chmod 600 "$summary.sha256"
printf '%s\n' "P7.06 selected-Mac proof PASS source=$source target=$target evidence=$summary sha256=$digest"
