# r5.sh WORKTREE LOGDIR : the R5 share. check_fast alone, then two lanes.
WT=$1; L=$2; S=$(dirname $0); mkdir -p $L; cd $WT; B=$WT/starship-cadet.html
sha256sum $B > $L/sha.txt
R="bash $S/run1.sh"
CHECK_LOGS=$L/cf $R check_fast $L /tmp/w5-cf bash check_fast.sh
( $R fridays $L /tmp/w5-a python3 fridays_check.py $B
  $R mech $L /tmp/w5-a python3 mech_check.py $B
  $R disc $L /tmp/w5-a python3 disc_check.py $B
  for d in 12 17 13 3; do $R day$d $L /tmp/w5-a python3 day_check.py $B $d; done
  $R stories $L /tmp/w5-a python3 stories_check.py $B 36
  echo LANEA >> $L/lanes ) &
( $R events $L /tmp/w5-b python3 events_check.py $B
  $R join $L /tmp/w5-b python3 join_check.py $B
  for d in 27 18 19; do $R day$d $L /tmp/w5-b python3 day_check.py $B $d; done
  $R bigevents $L /tmp/w5-b python3 bigevents_check.py $B
  $R tiles $L /tmp/w5-b python3 tiles_check.py $B
  $R clothes $L /tmp/w5-b python3 clothes_check.py $B
  $R promo_beats $L /tmp/w5-b python3 promo_beats_check.py $B
  $R food_1_7 $L /tmp/w5-b python3 food_check.py $B 1 7
  $R food_11_4 $L /tmp/w5-b python3 food_check.py $B 11 4
  $R machine2 $L /tmp/w5-b python3 machine_check.py $B
  echo LANEB >> $L/lanes ) &
wait; echo ALLDONE >> $L/summary.md
