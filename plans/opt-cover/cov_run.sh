#!/bin/bash
# The map run (tools/check_map.json), in a run that doesn't count: every check once under tools/check_cover.py, one
# browser at a time, on a frozen copy so the branch can move meanwhile. About 2 h 15 on 4 cores (2026-10-21, 0.64.12).
#   bash plans/opt-cover/cov_run.sh OUT_DIR [check ...]      (no checks named: all of them; a cover already in OUT_DIR is kept)
# then: python3 tools/affected.py --merge tools/check_map.json COMMIT OUT_DIR/*.json   (COMMIT = the game the run used)
set -u
OUT=$(realpath -m "$1"); shift; mkdir -p "$OUT/log"
ROOT=$(cd "$(dirname "$0")/../.." && pwd); SNAP=$OUT/snap
[ -d "$SNAP" ] || { mkdir -p "$SNAP"; git -C "$ROOT" archive HEAD | tar x -C "$SNAP"; }
G=$SNAP/starship-cadet.html
export CADET_CHROME=${CADET_CHROME:-/opt/pw-browsers/chromium} CADET_WORK=${CADET_WORK:-/tmp/cadet-work}
ALL="lines arc talk leave social machine cadet clothes career food deck disc puzzle device path tiles join bubble mech bigevents devmode events intro day1 interactions fridays player perf day0 day5 day7 day12 day13 day15 day16 day17 day19 day21 day22 day23 day24 day25 day26"
cd "$SNAP"
for n in ${@:-$ALL}; do
  [ -s "$OUT/$n.json" ] && continue
  case $n in
    cadet) f=cadet_test.py; a="$G $G";;
    day[0-9]*) f=day_check.py; a="$G ${n#day}";;
    *) f=${n}_check.py; a="$G";;
  esac
  t=$SECONDS; timeout 5400 python3 -u tools/check_cover.py "$OUT/$n.json" $f $a > "$OUT/log/$n.txt" 2>&1
  echo "$n exit $? $((SECONDS-t)) s $(date -u +%H:%M)" | tee -a "$OUT/log/_summary.txt"
done
