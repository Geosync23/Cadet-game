# 0.99.9 gates (BM27): check_fast, then events | cadet vs 0.99.8, then EV1's blink probe
cd /home/user/wt999; B=$PWD/starship-cadet.html; L=/tmp/bm27/g9; R="bash /home/user/Cadet-game/plans/build-master/run1.sh"
sha256sum $B > $L/sha.txt
CHECK_LOGS=$L/cf $R check_fast $L /tmp/bm27/gc bash check_fast.sh
( $R events $L /tmp/bm27/ga python3 events_check.py $B ) &
( bash /home/user/Cadet-game/plans/build-master/bm25/cad.sh /tmp/bm27/old-0998.html $B $L/cad8; echo "| cadet vs 0.99.8 | $(grep -E 'IDENTICAL|DIFFERENCES' $L/cad8/cadet.log | tail -1) |" >> $L/summary.md
  $R blinkprobe $L /tmp/bm27/gb python3 plans/ev1-probes/blinkprobe.py $B $L/shots ) &
wait; echo GATESDONE >> $L/summary.md
