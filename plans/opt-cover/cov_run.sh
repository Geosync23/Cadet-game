#!/bin/bash
# usage: cov_run.sh name... ; runs each check under coverage on 0.64.8
export CADET_CHROME=/opt/pw-browsers/chromium CADET_WORK=/tmp/cadet-work
G=/tmp/claude-0/-home-user-Cadet-game/1433b1df-649c-573b-b9ed-81a889f61fcc/scratchpad/b0648.html; cd /tmp/claude-0/-home-user-Cadet-game/1433b1df-649c-573b-b9ed-81a889f61fcc/scratchpad/snap
for n in "$@"; do
  case $n in
    cadet) f=cadet_test.py; a="$G $G";;
    day1) f=day_check.py; a="$G 1";;
    *) f=${n}_check.py; a="$G";;
  esac
  t=$SECONDS; python3 -u ../snap/tools/check_cover.py /tmp/claude-0/-home-user-Cadet-game/1433b1df-649c-573b-b9ed-81a889f61fcc/scratchpad/cov/$n.json $f $a > /tmp/claude-0/-home-user-Cadet-game/1433b1df-649c-573b-b9ed-81a889f61fcc/scratchpad/covlog/$n.txt 2>&1; echo "$n exit $? $((SECONDS-t)) s" >> /tmp/claude-0/-home-user-Cadet-game/1433b1df-649c-573b-b9ed-81a889f61fcc/scratchpad/covlog/_summary.txt
done
