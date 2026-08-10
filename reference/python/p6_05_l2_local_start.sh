#!/bin/sh
set -eu

# P6.05-L2 bounded owner-operated local reference-runtime start.
#
# This script intentionally:
# - synchronizes only the canonical Arvectum OS checkout;
# - creates an isolated stdlib-only venv outside the source checkout;
# - runs the existing in-process reference runtime test harness;
# - writes only secret-safe local execution evidence;
# - does not invoke ai-corporation, EIS, external mutation, public ingress,
#   containers, or a persistent service topology.

fail() {
  printf '%s\n' "P6.05-L2 FAIL: $*" >&2
  exit 1
}

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd "$SCRIPT_DIR/../.." && pwd)
PYTHON_BIN=${PYTHON_BIN:-python3}
LOCAL_ROOT=${ARVECTUM_LOCAL_ROOT:-$(dirname "$REPO_ROOT")}

command -v git >/dev/null 2>&1 || fail "git is not available"
command -v "$PYTHON_BIN" >/dev/null 2>&1 || fail "$PYTHON_BIN is not available"

git -C "$REPO_ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1 || fail "repository checkout is not a Git worktree"

ORIGIN_URL=$(git -C "$REPO_ROOT" remote get-url origin 2>/dev/null || true)
case "$ORIGIN_URL" in
  *arutyunoveth/arvectum-os*) ;;
  *) fail "origin is not the canonical arutyunoveth/arvectum-os repository" ;;
esac

BRANCH=$(git -C "$REPO_ROOT" symbolic-ref --quiet --short HEAD 2>/dev/null || true)
[ "$BRANCH" = "main" ] || fail "checkout must be on canonical main (found: ${BRANCH:-detached})"

if [ -n "$(git -C "$REPO_ROOT" status --porcelain)" ]; then
  fail "working tree is not clean; preserve local work before L2 synchronization"
fi

printf '%s\n' "P6.05-L2: fetching canonical main..."
git -C "$REPO_ROOT" fetch --prune origin main
git -C "$REPO_ROOT" merge --ff-only origin/main >/dev/null

HEAD_SHA=$(git -C "$REPO_ROOT" rev-parse HEAD)
ORIGIN_SHA=$(git -C "$REPO_ROOT" rev-parse origin/main)
[ "$HEAD_SHA" = "$ORIGIN_SHA" ] || fail "local main does not equal origin/main after fast-forward"

HEAD_SHORT=$(printf '%s' "$HEAD_SHA" | cut -c1-12)
VENV_DIR=${ARVECTUM_L2_VENV_DIR:-$LOCAL_ROOT/runtime-data/venvs/p6-05-l2-arvectum-os-$HEAD_SHORT}
EVIDENCE_ROOT=${ARVECTUM_L2_EVIDENCE_ROOT:-$LOCAL_ROOT/evidence/p6-05-l2}

case "$VENV_DIR/" in
  "$REPO_ROOT"/*) fail "L2 venv must remain outside the source-controlled checkout" ;;
esac
case "$EVIDENCE_ROOT/" in
  "$REPO_ROOT"/*) fail "L2 evidence must remain outside the source-controlled checkout" ;;
esac

TIMESTAMP=$(date -u '+%Y%m%dT%H%M%SZ')
RUN_DIR="$EVIDENCE_ROOT/$TIMESTAMP-$HEAD_SHORT"
LOG_FILE="$RUN_DIR/reference-runtime.log"
SUMMARY_FILE="$RUN_DIR/summary.txt"

mkdir -p "$RUN_DIR" "$(dirname "$VENV_DIR")"

if [ ! -x "$VENV_DIR/bin/python" ]; then
  printf '%s\n' "P6.05-L2: creating isolated stdlib-only venv at $VENV_DIR"
  "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

VENV_PYTHON="$VENV_DIR/bin/python"
PYTHON_VERSION=$($VENV_PYTHON -c 'import platform; print(platform.python_version())')
PLATFORM_DESC=$($VENV_PYTHON -c 'import platform; print(platform.platform())')

printf '%s\n' "P6.05-L2: canonical HEAD $HEAD_SHA"
printf '%s\n' "P6.05-L2: Python $PYTHON_VERSION"
printf '%s\n' "P6.05-L2: running bounded reference runtime suite..."

set +e
(
  cd "$REPO_ROOT/reference/python"
  "$VENV_PYTHON" -m unittest discover -s tests -v
) >"$LOG_FILE" 2>&1
TEST_RC=$?
set -e

RAN_LINE=$(grep -E '^Ran [0-9]+ tests? in ' "$LOG_FILE" | tail -n 1 || true)
RESULT_LINE=$(grep -E '^(OK|FAILED)' "$LOG_FILE" | tail -n 1 || true)

if [ "$TEST_RC" -eq 0 ] && [ "$RESULT_LINE" = "OK" ]; then
  STATUS=PASS
else
  STATUS=FAIL
fi

cat >"$SUMMARY_FILE" <<EOF
p6_05_l2_status=$STATUS
operational_environment=Internal / local owner-operated runtime
production_readiness_claim=None
canonical_repository=arutyunoveth/arvectum-os
branch=main
head_sha=$HEAD_SHA
origin_main_sha=$ORIGIN_SHA
python_version=$PYTHON_VERSION
platform=$PLATFORM_DESC
dependency_mode=stdlib-only; no third-party dependency installation
runtime_mode=in-process reference harness
runtime_command=python -m unittest discover -s tests -v
runtime_result=${RESULT_LINE:-not-observed}
runtime_test_count=${RAN_LINE:-not-observed}
external_actions=false
public_ingress=false
product_invoked=false
eis_invoked=false
log_file=$LOG_FILE
EOF

if [ "$STATUS" = "PASS" ]; then
  printf '%s\n' "P6.05-L2 PASS"
  printf '%s\n' "${RAN_LINE:-runtime suite passed}"
  printf '%s\n' "Evidence: $SUMMARY_FILE"
  exit 0
fi

printf '%s\n' "P6.05-L2 FAIL"
printf '%s\n' "Evidence: $SUMMARY_FILE"
printf '%s\n' "Last runtime output:"
tail -n 40 "$LOG_FILE" >&2 || true
exit "$TEST_RC"
