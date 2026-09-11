#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════
# Week 17 — Infrastructure Verification Script
#
# This script IS your pass bar.  All six checks must go green.
# Run:  chmod +x verify.sh && ./verify.sh
# ══════════════════════════════════════════════════════════════════════════

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PASS=0
FAIL=0

check() {
    local label="$1"
    shift
    echo -n "  [$label] "
    if "$@" > /dev/null 2>&1; then
        echo -e "${GREEN}PASS${NC}"
        ((PASS++))
    else
        echo -e "${RED}FAIL${NC}"
        ((FAIL++))
    fi
}

echo ""
echo -e "${YELLOW}═══ Week 17 — Infrastructure Pass Bar ═══${NC}"
echo ""

# ── Check 1: Unit tests pass locally ──────────────────────────────────────
echo "① Local pytest"
check "pytest" python3 -m pytest tests/ -q --tb=no

# ── Check 2: Docker image builds ─────────────────────────────────────────
echo "② Docker build"
check "docker compose build" docker compose build --quiet

# ── Check 3: All services come up healthy ─────────────────────────────────
echo "③ Docker compose up"

# Copy .env.example if .env doesn't exist
[ -f .env ] || cp .env.example .env

docker compose up -d --wait --wait-timeout 60 2>/dev/null
check "services healthy" docker compose ps --filter "status=running" --quiet

# ── Check 4: /healthz/ returns 200 ───────────────────────────────────────
echo "④ Health check endpoint"
sleep 3  # give gunicorn a moment
check "curl /healthz/" bash -c 'curl -sf http://localhost:8000/healthz/ | python3 -c "import sys,json; d=json.load(sys.stdin); sys.exit(0 if d[\"status\"]==\"healthy\" else 1)"'

# ── Check 5: Tests pass inside the container ──────────────────────────────
echo "⑤ In-container pytest"
check "docker exec pytest" docker compose exec -T web python -m pytest tests/ -q --tb=no

# ── Check 6: Clean shutdown ───────────────────────────────────────────────
echo "⑥ Clean shutdown"
check "docker compose down" docker compose down -v

# ── Summary ───────────────────────────────────────────────────────────────
echo ""
echo "════════════════════════════════════════"
echo -e "  ${GREEN}PASSED: $PASS${NC}  ${RED}FAILED: $FAIL${NC}  (total: $((PASS+FAIL)))"
if [ "$FAIL" -eq 0 ]; then
    echo -e "  ${GREEN}🚀 LAB 17 COMPLETE${NC}"
else
    echo -e "  ${RED}✗  Fix the failing checks above${NC}"
fi
echo "════════════════════════════════════════"
echo ""

exit "$FAIL"
