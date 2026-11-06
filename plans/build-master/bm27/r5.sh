# BM27's R5 share for round 0998: on a worktree of COMMIT (arg 1), two lanes, then cadet vs 0.99.6 alone.
C=$1; cd /home/user/Cadet-game && git worktree add -q -f /tmp/bm27/wt-r5 $C
cd /tmp/bm27/wt-r5; B=$PWD/starship-cadet.html; L=/tmp/bm27/r5; mkdir -p $L; R="bash /home/user/Cadet-game/plans/build-master/run1.sh"
sha256sum $B > $L/sha.txt
mkdir -p plans/rv31-probes; git -C /home/user/Cadet-game show origin/claude/review-rv31:plans/rv31-probes/p5retry_break.py > plans/rv31-probes/p5retry_break.py
sed 's/^var FIXTAP_ON = true;/var FIXTAP_ON = false;/; s/^var P5_RETRY_ON = true;/var P5_RETRY_ON = false;/' $B > /tmp/bm27/off_both.html
grep -c "^var FIXTAP_ON = false;\|^var P5_RETRY_ON = false;" /tmp/bm27/off_both.html >> $L/sha.txt
( $R machine $L /tmp/bm27/w6a python3 machine_check.py $B; $R mech $L /tmp/bm27/w6a python3 mech_check.py $B; $R bigevents $L /tmp/bm27/w6a python3 bigevents_check.py $B
  $R disc $L /tmp/bm27/w6a python3 disc_check.py $B; $R events $L /tmp/bm27/w6a python3 events_check.py $B
  for d in 12 17 13 3; do $R day$d $L /tmp/bm27/w6a python3 day_check.py $B $d; done; $R stories $L /tmp/bm27/w6a python3 stories_check.py $B 36 ) &
( $R fridays $L /tmp/bm27/w6b python3 fridays_check.py $B; $R machine2 $L /tmp/bm27/w6b python3 machine_check.py $B
  $R clothes $L /tmp/bm27/w6b python3 clothes_check.py $B; $R promo_beats $L /tmp/bm27/w6b python3 promo_beats_check.py $B
  $R food_1_7 $L /tmp/bm27/w6b python3 food_check.py $B 1 7; $R food_11_4 $L /tmp/bm27/w6b python3 food_check.py $B 11 4
  $R tiles $L /tmp/bm27/w6b python3 tiles_check.py $B; $R join $L /tmp/bm27/w6b python3 join_check.py $B; $R weekend $L /tmp/bm27/w6b python3 weekend_check.py $B
  for d in 27 18 19; do $R day$d $L /tmp/bm27/w6b python3 day_check.py $B $d; done
  $R p5retry_break $L /tmp/bm27/w6b python3 plans/rv31-probes/p5retry_break.py /tmp/bm27/off_both.html $B ) &
wait; echo LANESDONE >> $L/summary.md
bash /home/user/Cadet-game/plans/build-master/bm25/cad.sh /tmp/bm27/old-0996.html $B $L/cad; echo "| cadet vs 0.99.6 | $(grep -E 'IDENTICAL|DIFFERENCES' $L/cad/cadet.log | tail -1) |" >> $L/summary.md; echo ALLDONE >> $L/summary.md
