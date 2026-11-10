# BM28's R5 share for round 09991 (round 0999's R5 list + cr2_check; check_fast, events and cadet vs 0.99.9 done as gates).
# Re-runnable: skips checks already in summary.md; append "| name | handed to Rn |" to hand one over.
W=/home/user/wt9991; cd $W; B=$W/starship-cadet.html; L=/home/user/bm28logs/r5; mkdir -p $L /home/user/bm28/probes; touch $L/summary.md
sha256sum $B >> $L/sha.txt
git -C $W show bm28-rv31:plans/rv31-probes/p5retry_break.py > /home/user/bm28/probes/p5retry_break.py
sed 's/^var FIXTAP_ON = true;/var FIXTAP_ON = false;/; s/^var P5_RETRY_ON = true;/var P5_RETRY_ON = false;/' $B > /home/user/bm28/off_both.html
r() { n=$1; w=$2; shift 2; grep -q "^| $n |" $L/summary.md && return; bash $W/plans/build-master/run1.sh $n $L $w "$@"; }
( r cr2 /home/user/bm28/w6a python3 cr2_check.py $B
  r machine /home/user/bm28/w6a python3 machine_check.py $B; r mech /home/user/bm28/w6a python3 mech_check.py $B
  r bigevents /home/user/bm28/w6a python3 bigevents_check.py $B
  r disc /home/user/bm28/w6a python3 disc_check.py $B; for d in 12 17 13 3; do r day$d /home/user/bm28/w6a python3 day_check.py $B $d; done
  r stories /home/user/bm28/w6a python3 stories_check.py $B 36; r tiles /home/user/bm28/w6a python3 tiles_check.py $B ) &
( r fridays /home/user/bm28/w6b python3 fridays_check.py $B; r machine2 /home/user/bm28/w6b python3 machine_check.py $B
  r clothes /home/user/bm28/w6b python3 clothes_check.py $B; r promo_beats /home/user/bm28/w6b python3 promo_beats_check.py $B
  r food_1_7 /home/user/bm28/w6b python3 food_check.py $B 1 7; r food_11_4 /home/user/bm28/w6b python3 food_check.py $B 11 4
  r join /home/user/bm28/w6b python3 join_check.py $B; r weekend /home/user/bm28/w6b python3 weekend_check.py $B
  for d in 27 18 19; do r day$d /home/user/bm28/w6b python3 day_check.py $B $d; done
  r p5retry_break /home/user/bm28/w6b python3 /home/user/bm28/probes/p5retry_break.py /home/user/bm28/off_both.html $B ) &
wait; echo ALLDONE >> $L/summary.md
