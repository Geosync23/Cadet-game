# BM27 R5 share for round 0998b on candidate 2 (wt-c2), after the gate chain (gates_c2.sh) ends; then cadet vs 0.99.6
until grep -q GATESDONE /tmp/bm27/g2/summary.md; do sleep 10; done
cd /tmp/bm27/wt-c2; B=$PWD/starship-cadet.html; L=/tmp/bm27/r5b; mkdir -p $L; R="bash /home/user/Cadet-game/plans/build-master/run1.sh"
sha256sum $B > $L/sha.txt
mkdir -p plans/rv31-probes; git -C /home/user/Cadet-game show origin/claude/review-rv31:plans/rv31-probes/p5retry_break.py > plans/rv31-probes/p5retry_break.py
sed 's/^var FIXTAP_ON = true;/var FIXTAP_ON = false;/; s/^var P5_RETRY_ON = true;/var P5_RETRY_ON = false;/' $B > /tmp/bm27/off_both_c2.html
grep -c "^var FIXTAP_ON = false;\|^var P5_RETRY_ON = false;" /tmp/bm27/off_both_c2.html >> $L/sha.txt
( $R events $L /tmp/bm27/w6a python3 events_check.py $B; $R machine $L /tmp/bm27/w6a python3 machine_check.py $B; $R mech $L /tmp/bm27/w6a python3 mech_check.py $B; $R bigevents $L /tmp/bm27/w6a python3 bigevents_check.py $B
  $R disc $L /tmp/bm27/w6a python3 disc_check.py $B; $R day12 $L /tmp/bm27/w6a python3 day_check.py $B 12 ) &
( $R fridays $L /tmp/bm27/w6b python3 fridays_check.py $B; $R machine2 $L /tmp/bm27/w6b python3 machine_check.py $B
  $R clothes $L /tmp/bm27/w6b python3 clothes_check.py $B; $R promo_beats $L /tmp/bm27/w6b python3 promo_beats_check.py $B
  $R day17 $L /tmp/bm27/w6b python3 day_check.py $B 17; $R stories $L /tmp/bm27/w6b python3 stories_check.py $B 36 ) &
# handed off after the restart (lead 50): R4 tiles, join, weekend, day 27 18 19; R1 food 1 7, food 11 4, day 13, 3, p5retry_break
wait; echo LANESDONE >> $L/summary.md
bash /home/user/Cadet-game/plans/build-master/bm25/cad.sh /tmp/bm27/old-0996.html $B $L/cad; echo "| cadet vs 0.99.6 | $(grep -E "IDENTICAL|DIFFERENCES" $L/cad/cadet.log | tail -1) |" >> $L/summary.md; echo ALLDONE >> $L/summary.md
