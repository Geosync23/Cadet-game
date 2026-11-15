# BM29's R5 share for the Fable review round (plans/round-fable.md). check_fast, events and cadet vs 0.99.91 are gates, run before.
# Re-runnable: skips checks already in summary.md; append "| name | handed to Rn |" to hand one over.
# Needs /home/user/bm29/pre_onebyte.html (the candidate before tools/one_byte.py) and /home/user/bm29/old.html (0.99.91).
W=/home/user/wtfr; cd $W; B=$W/starship-cadet.html; H=/home/user/bm29; L=$H/logs/${1:-r5}; mkdir -p $L; touch $L/summary.md
sha256sum $B >> $L/sha.txt
sed 's/^var FIXTAP_ON = true;/var FIXTAP_ON = false;/; s/^var P5_RETRY_ON = true;/var P5_RETRY_ON = false;/' $B > $H/off_both.html
sed 's/^const TP9991_SD_ON = true;/const TP9991_SD_ON = false;/' $B > $H/tp_off.html
sim() { grep -q '^| simprobe |' $L/summary.md && return; CADET_WORK=$1 CADET_CHROME=/opt/pw-browsers/chromium python3 plans/ev2-probes/simprobe.py $B > $L/simprobe.log 2>&1; echo "| simprobe | exit $? (read by eye: days, tap, card, act) |" >> $L/summary.md; }
r() { n=$1; w=$2; shift 2; grep -q "^| $n |" $L/summary.md && return; bash $W/plans/build-master/run1.sh $n $L $w "$@"; }
( r one_byte $H/w6a python3 tools/one_byte.py --check $B
  r cr2 $H/w6a python3 cr2_check.py $B; r drill $H/w6a python3 plans/tb7-probes/drill.py $B
  r tp9991 $H/w6a python3 plans/tp2-probes/tp9991_probe.py $H/tp_off.html; sim $H/w6a
  r machine $H/w6a python3 machine_check.py $B; r mech $H/w6a python3 mech_check.py $B
  r bigevents $H/w6a python3 bigevents_check.py $B
  r disc $H/w6a python3 disc_check.py $B; for d in 12 17 13 3; do r day$d $H/w6a python3 day_check.py $B $d; done
  r stories $H/w6a python3 stories_check.py $B 36; r tiles $H/w6a python3 tiles_check.py $B ) &
( r fridays $H/w6b python3 fridays_check.py $B; r machine2 $H/w6b python3 machine_check.py $B
  r clothes $H/w6b python3 clothes_check.py $B; r promo_beats $H/w6b python3 promo_beats_check.py $B
  r food_1_7 $H/w6b python3 food_check.py $B 1 7; r food_11_4 $H/w6b python3 food_check.py $B 11 4
  r join $H/w6b python3 join_check.py $B; r weekend $H/w6b python3 weekend_check.py $B
  for d in 27 18 19; do r day$d $H/w6b python3 day_check.py $B $d; done
  r p5retry_break $H/w6b python3 plans/rv31-probes/p5retry_break.py $H/off_both.html $B ) &
wait
grep -q '^| cadet_onebyte |' $L/summary.md || { bash plans/build-master/bm25/cad.sh $H/pre_onebyte.html $B $L/cadob; echo "| cadet_onebyte | $(tail -2 $L/cadob/cadet.log | tr '\n' ' ' | cut -c1-160) |" >> $L/summary.md; }
echo ALLDONE >> $L/summary.md
