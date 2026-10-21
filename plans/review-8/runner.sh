#!/bin/bash
# PR8's resumable runner (PR5's, plans/review-5/runner.sh): each step writes res/<name>.log and .done; one check at a time
S=/tmp/claude-0/-home-user/ede8ebf0-4d7f-58dc-8854-06cbdac645fa/scratchpad
H=${H:-/home/user/r8}; B=${B:-$S/b}; R=${R:-$S/run/res}; mkdir -p $R $S/run/ct
export CADET_CHROME=/opt/pw-browsers/chromium CADET_WORK=/tmp/cadet-work
cd $H
for step in "$@"; do
  name=${step%%:*}; cmd=${step#*:}
  [ -f $R/$name.done ] && continue
  echo "== $name: $cmd" ; t0=$(date +%s)
  ( eval "$cmd" ) > $R/$name.log 2>&1; rc=$?
  echo "rc=$rc secs=$(( $(date +%s)-t0 ))" >> $R/$name.log
  [ $rc -ne 137 ] && touch $R/$name.done
  tail -3 $R/$name.log
done
echo RUNNER DONE
