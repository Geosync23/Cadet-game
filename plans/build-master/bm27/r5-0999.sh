# BM27's R5 share for round 0999 (check_fast, events and cadet vs 0.99.8 done as gates). Re-runnable: skips checks already in summary.md.
cd /home/user/wt999; B=$PWD/starship-cadet.html; L=/tmp/bm27/r5-9; mkdir -p $L; touch $L/summary.md
sha256sum $B >> $L/sha.txt
mkdir -p /tmp/bm27/probes; git -C /home/user/Cadet-game show origin/claude/review-rv31:plans/rv31-probes/p5retry_break.py > /tmp/bm27/probes/p5retry_break.py
sed 's/^var FIXTAP_ON = true;/var FIXTAP_ON = false;/; s/^var P5_RETRY_ON = true;/var P5_RETRY_ON = false;/' $B > /tmp/bm27/off_both_9.html
r() { n=$1; w=$2; shift 2; grep -q "^| $n |" $L/summary.md && return; bash /home/user/Cadet-game/plans/build-master/run1.sh $n $L $w "$@"; }
( r machine /tmp/bm27/w6a python3 machine_check.py $B; r mech /tmp/bm27/w6a python3 mech_check.py $B; r bigevents /tmp/bm27/w6a python3 bigevents_check.py $B
  r disc /tmp/bm27/w6a python3 disc_check.py $B; for d in 12 17 13 3; do r day$d /tmp/bm27/w6a python3 day_check.py $B $d; done
  r stories /tmp/bm27/w6a python3 stories_check.py $B 36; r tiles /tmp/bm27/w6a python3 tiles_check.py $B ) &
( r fridays /tmp/bm27/w6b python3 fridays_check.py $B; r machine2 /tmp/bm27/w6b python3 machine_check.py $B
  r clothes /tmp/bm27/w6b python3 clothes_check.py $B; r promo_beats /tmp/bm27/w6b python3 promo_beats_check.py $B
  r food_1_7 /tmp/bm27/w6b python3 food_check.py $B 1 7; r food_11_4 /tmp/bm27/w6b python3 food_check.py $B 11 4
  r join /tmp/bm27/w6b python3 join_check.py $B; r weekend /tmp/bm27/w6b python3 weekend_check.py $B
  for d in 27 18 19; do r day$d /tmp/bm27/w6b python3 day_check.py $B $d; done
  r p5retry_break /tmp/bm27/w6b python3 /tmp/bm27/probes/p5retry_break.py /tmp/bm27/off_both_9.html $B ) &
wait; echo ALLDONE >> $L/summary.md
