#!/bin/bash
# (RN1: the #5 proof rounds; the event builds m5_*.html are made as described in plans/handover-opt-render.md "Loose ends")
# opt #5 on the event branches (switched on): old (without the change) vs new, day_check output line for line, cadet_test, memory
S=/tmp/claude-0/-home-user-Cadet-game/019501c3-ea82-5c10-ac85-e5cbe4c6d05b/scratchpad; G=/home/user/Cadet-game; export CADET_CHROME=/opt/pw-browsers/chromium
cd $G
r() { local name=$1; shift; local t0=$(date +%s); timeout 3600 "$@" > $S/p5b_$name.log 2>&1; echo "$name: exit $? in $(( $(date +%s) - t0 )) s: $(tail -1 $S/p5b_$name.log)"; }
for d in 13 14 21; do r day${d}_new python3 day_check.py $S/m5_on.html $d; r day${d}_old python3 day_check.py $S/m5_off_old.html $d; done
r day7line_new python3 day_check.py $S/m5_line_new.html 7; r day7line_old python3 day_check.py $S/m5_line_old.html 7
(cd $S/ct && r cadet_ev python3 $G/cadet_test.py $S/m5_off_old.html $S/m5_on.html)
(cd $S/ct && r cadet_line python3 $G/cadet_test.py $S/m5_line_old.html $S/m5_line_new.html)
r detach_ev python3 $G/plans/opt-probes/detach_test.py $S/m5_off_old.html
r detach_line python3 $G/plans/opt-probes/detach_test.py $S/m5_line_old.html
for d in 13 14 21; do diff <(grep -v " s\b\|seconds\|took" $S/p5b_day${d}_new.log) <(grep -v " s\b\|seconds\|took" $S/p5b_day${d}_old.log) > /dev/null && echo "day $d: day_check output IDENTICAL old/new" || echo "day $d: day_check output DIFFERS"; done
diff <(grep -v " s\b\|seconds\|took" $S/p5b_day7line_new.log) <(grep -v " s\b\|seconds\|took" $S/p5b_day7line_old.log) > /dev/null && echo "line day 7: IDENTICAL" || echo "line day 7: DIFFERS"
echo ALL DONE B
