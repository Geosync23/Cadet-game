#!/bin/bash
# q.sh HTML TAG check... : run checks sequentially from the worktree, one log each
H=$1; T=$2; shift 2; cd ${WT:-/tmp/cw/wt2}; export CADET_CHROME=/opt/pw-browsers/chromium
for c in "$@"; do
  case $c in
    smoke|newgame) cmd="python3 -u /tmp/cw/bm/${c}_check.py $H";;
    day*) cmd="python3 -u day_check.py $H ${c#day}";;
    cadet) cmd="python3 -u cadet_test.py ${OLD:-/tmp/cw/c0b.html} $H";;
    *) cmd="python3 -u ${c}_check.py $H";;
  esac
  s=$(date +%s); timeout ${TMO:-1800} $cmd > /tmp/cw/logs/$T-$c.log 2>&1; rc=$?
  echo "$T $c rc=$rc $(( $(date +%s)-s ))s :: $(tail -1 /tmp/cw/logs/$T-$c.log | cut -c1-200)" >> /tmp/cw/logs/summary.txt
done
