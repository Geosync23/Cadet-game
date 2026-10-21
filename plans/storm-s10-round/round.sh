#!/bin/bash
# EV6's S10 round: each check on one build, one at a time; logs in $2
B=$1; OUT=$2; shift 2; cd /home/user/Cadet-game
export CADET_WORK=/tmp/cadet-work/r CADET_CHROME=/opt/pw-browsers/chromium
run() { local n=$1; shift; local t=$(date +%s); timeout 3600 "$@" > $OUT/$n.txt 2>&1; echo "$n exit $? $(( $(date +%s) - t ))s $(grep -E 'CHECK OK|CHECK FAILED|^OK$|^FAILED$|PERF CHECK|ALL IDENTICAL' $OUT/$n.txt | tail -1)" >> $OUT/summary.txt; }
for c in "$@"; do case $c in
  events) run events python3 events_check.py $B ;;
  big) run big python3 bigevents_check.py $B ;;
  day*) run $c python3 day_check.py $B ${c#day} ;;
  food) run food python3 food_check.py $B 11 4 ;;
  intro-*) run $c python3 intro_check.py $B --${c#intro-} ;;
  *) run $c python3 ${c}_check.py $B ;;
esac; done
echo DONE >> $OUT/summary.txt
