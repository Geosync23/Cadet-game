#!/bin/bash
# resumable: each step writes res/<name>.log and .done
S=/tmp/claude-0/-home-user/a4344e06-66ec-50a3-8125-a9cc15d32fe0/scratchpad
H=${H:-$S/w/head}; R=${R:-$S/run/res}; mkdir -p $R
export CADET_CHROME=/opt/pw-browsers/chromium CADET_WORK=/tmp/cadet-work
cd $H
sed 's/^const SHORT_FRIDAY = false;/const SHORT_FRIDAY = true;/' starship-cadet.html > on.html
grep -c '^const SHORT_FRIDAY = true;' on.html
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
