# after the container restart (21:3x UTC): candidate 2's lost gates: arrows default | cadet vs c1 then vs 0.99.7; then GATESDONE (r5b.sh waits for it)
cd /tmp/bm27/wt-c2; B=$PWD/starship-cadet.html; L=/tmp/bm27/g2; R="bash /home/user/Cadet-game/plans/build-master/run1.sh"
( $R arrows_default $L /tmp/bm27/ga python3 arrows_check.py $B ) &
( bash /home/user/Cadet-game/plans/build-master/bm25/cad.sh /tmp/bm27/c1-0998.html $B $L/cad1; echo "| cadet vs c1 | $(grep -E 'IDENTICAL|DIFFERENCES' $L/cad1/cadet.log | tail -1) |" >> $L/summary.md
  bash /home/user/Cadet-game/plans/build-master/bm25/cad.sh /tmp/bm27/old-0997.html $B $L/cad7; echo "| cadet vs 0.99.7 | $(grep -E 'IDENTICAL|DIFFERENCES' $L/cad7/cadet.log | tail -1) |" >> $L/summary.md ) &
wait; echo GATESDONE >> $L/summary.md
