# R5 for 0.99.7: what the early gates didn't cover (they did check_fast, machine, events, bigevents, join, tiles, weekend, fridays)
cd /tmp/bm24/wt-t2; B=$PWD/starship-cadet.html; L=/tmp/bm24/r5-997; mkdir -p $L; R="bash /home/user/Cadet-game/plans/build-master/run1.sh"
sha256sum $B > $L/sha.txt
mkdir -p plans/rv31-probes; git -C /home/user/Cadet-game show origin/claude/review-rv31:plans/rv31-probes/p5retry_break.py > plans/rv31-probes/p5retry_break.py
sed 's/^var FIXTAP_ON = true;/var FIXTAP_ON = false;/; s/^var P5_RETRY_ON = true;/var P5_RETRY_ON = false;/' $B > /tmp/bm24/off_both_997.html
( $R machine2 $L /tmp/bm24/w5a python3 machine_check.py $B; $R mech $L /tmp/bm24/w5a python3 mech_check.py $B; $R disc $L /tmp/bm24/w5a python3 disc_check.py $B
  for d in 12 17 13 3; do $R day$d $L /tmp/bm24/w5a python3 day_check.py $B $d; done; $R stories $L /tmp/bm24/w5a python3 stories_check.py $B 36 ) &
( $R clothes $L /tmp/bm24/w5b python3 clothes_check.py $B; $R promo_beats $L /tmp/bm24/w5b python3 promo_beats_check.py $B
  $R food_1_7 $L /tmp/bm24/w5b python3 food_check.py $B 1 7; $R food_11_4 $L /tmp/bm24/w5b python3 food_check.py $B 11 4
  for d in 27 18 19; do $R day$d $L /tmp/bm24/w5b python3 day_check.py $B $d; done
  $R p5retry_break $L /tmp/bm24/w5b python3 plans/rv31-probes/p5retry_break.py /tmp/bm24/off_both_997.html $B ) &
wait; echo LANESDONE >> $L/summary.md
bash /tmp/bm24/cad.sh /tmp/bm24/old-0996.html $B $L/cad; echo "| cadet | $(grep -E 'IDENTICAL|differ' $L/cad/cadet.log | tail -1) |" >> $L/summary.md; echo ALLDONE >> $L/summary.md
