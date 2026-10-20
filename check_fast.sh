#!/usr/bin/env bash
# check_fast.sh: the quick check before every push (about 5 minutes). GitHub runs the same on every push.
#   bash check_fast.sh            (CADET_CHROME = a Chromium; CADET_WORK = where three.js and acorn live)
# 1. the game file matches its pieces   2. the words are baked   3. the script parses, piece by piece and whole,
# no name or shared-table key made twice, no "Deck 7" on screen   4. two lanes side by side, each in its own CADET_WORK:
# deck_check then machine_check then leave_check  |  device_check.
# A step passes only if it exits 0 AND prints its OK line (a check that only prints FAILED must not pass).
set -u
cd "$(dirname "$0")"
export CADET_CHROME="${CADET_CHROME-/opt/pw-browsers/chromium}"   # set but empty: Playwright's own Chromium (GitHub)
BASE="${CADET_WORK:-/tmp/cadet-work}"
LOGS="${CHECK_LOGS:-$BASE/check-fast}"; rm -rf "$LOGS"; mkdir -p "$LOGS"
T0=$(date +%s); FAIL=0
say() { printf '%-28s %s\n' "$1" "$2"; }
step() {   # step NAME OKPATTERN LOG cmd...
  local name=$1 pat=$2 log=$3; shift 3; local t=$(date +%s)
  "$@" > "$log" 2>&1; local rc=$?
  if [ $rc -eq 0 ] && grep -q -- "$pat" "$log"; then say "$name" "OK ($(( $(date +%s) - t )) s)"
  else say "$name" "FAILED (exit $rc, $(( $(date +%s) - t )) s): $log"; grep -E 'FAIL|STOPPED|Error|error' "$log" | head -8 | sed 's/^/    /'; return 1; fi
}
step 'pieces = game file' 'build --check: OK' "$LOGS/build.txt" python3 build.py --check || FAIL=1
step 'words baked' '^up to date' "$LOGS/words.txt" python3 content_gen.py pieces/content/s22-words.gen.js --check || FAIL=1
step 'parse, names, text' 'names_check: OK' "$LOGS/names.txt" env CADET_WORK="$BASE" node names_check.js || FAIL=1
if [ $FAIL -ne 0 ]; then echo "QUICK CHECK FAILED (the fast steps; browser checks not run) in $(( $(date +%s) - T0 )) s"; exit 1; fi
lane() {   # lane TAG step...; each lane its own CADET_WORK (parallel runs otherwise load each other's copies)
  local tag=$1; shift; local w="$BASE/lane-$tag"; mkdir -p "$w/test"; ln -sfn "$BASE/three" "$w/three"
  local f=0
  for c in "$@"; do
    case $c in
      deck)    CADET_WORK=$w step 'deck_check' 'DECK CHECK OK' "$LOGS/deck.txt" python3 deck_check.py starship-cadet.html || f=1 ;;
      machine) CADET_WORK=$w step 'machine_check' 'MACHINE CHECK OK' "$LOGS/machine.txt" python3 machine_check.py starship-cadet.html || f=1 ;;
      leave)   CADET_WORK=$w step 'leave_check' 'LEAVE CHECK OK' "$LOGS/leave.txt" python3 leave_check.py starship-cadet.html || f=1 ;;
      device)  CADET_WORK=$w step 'device_check' 'device_check: OK' "$LOGS/device.txt" python3 device_check.py starship-cadet.html || f=1 ;;
    esac
  done
  return $f
}
lane a deck machine leave & A=$!
lane b device & B=$!
wait $A || FAIL=1
wait $B || FAIL=1
if [ $FAIL -ne 0 ]; then echo "QUICK CHECK FAILED in $(( $(date +%s) - T0 )) s (logs in $LOGS)"; exit 1; fi
echo "QUICK CHECK OK in $(( $(date +%s) - T0 )) s"
