#!/usr/bin/env bash
# lanes.sh TAG check... : run checks one after another in /tmp/opt647 with their own CADET_WORK; one line each in times.txt
tag=$1; shift; W=/tmp/work-$tag; mkdir -p $W/test; ln -sfn /tmp/cadet-work/three $W/three; ln -sfn /tmp/cadet-work/acorn $W/acorn
OUT=/tmp/claude-0/-home-user-Cadet-game/c1b02abe-9503-5276-8da1-eaa085c6ed9c/scratchpad/m/logs; mkdir -p $OUT
cd /tmp/opt647; export CADET_CHROME=/opt/pw-browsers/chromium CADET_WORK=$W
for c in "$@"; do
  t=$(date +%s)
  case $c in
    cadet) (mkdir -p $W/shots && cd $W/shots && timeout 3600 python3 /tmp/opt647/cadet_test.py /tmp/opt647/old0646.html /tmp/opt647/starship-cadet.html) > $OUT/$c.log 2>&1 ;;
    day1) timeout 3600 python3 day_check.py starship-cadet.html 1 > $OUT/$c.log 2>&1 ;;
    *) timeout 5400 python3 ${c}_check.py starship-cadet.html > $OUT/$c.log 2>&1 ;;
  esac
  rc=$?; echo "$c lane=$tag rc=$rc $(( $(date +%s) - t )) s :: $(tail -1 $OUT/$c.log | cut -c1-120)" >> $OUT/times.txt
done
echo "LANE $tag DONE" >> $OUT/times.txt
