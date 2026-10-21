#!/bin/bash
# PR9 (from PR8): resumable runner (PR5's, plans/review-5/runner.sh): each step writes res/<name>.log and .done; one check at a time
S=/tmp/claude-0/-home-user-Cadet-game/c90be8f5-63df-55cd-b247-474233586f38/scratchpad
H=${H:-$S/wt_208581c}; B=${B:-$S/b}; R=${R:-$S/run/res}; mkdir -p $R $S/run/ct
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
