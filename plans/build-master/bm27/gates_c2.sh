# candidate 2's gates (after player_check): check_fast, then arrows default | fresh_walk to Day 3 22:30, then cadet vs c1 and vs 0.99.7
cd /tmp/bm27/wt-c2; B=$PWD/starship-cadet.html; L=/tmp/bm27/g2; R="bash /home/user/Cadet-game/plans/build-master/run1.sh"
while pgrep -f "player_check.py $B" >/dev/null; do sleep 10; done
CHECK_LOGS=$L/cf $R check_fast $L /tmp/bm27/gc bash check_fast.sh
git -C /home/user/Cadet-game show d7f5bd6:starship-cadet.html > /tmp/bm27/c1-0998.html
( $R arrows_default $L /tmp/bm27/ga python3 arrows_check.py $B ) &
( FW_UNTIL=22:30 $R fresh_walk_d3 $L /tmp/bm27/gb python3 /tmp/bm27/fresh_walk.py $B 3 $L/fw.json ) &
wait
bash /home/user/Cadet-game/plans/build-master/bm25/cad.sh /tmp/bm27/c1-0998.html $B $L/cad1 &
bash /home/user/Cadet-game/plans/build-master/bm25/cad.sh /tmp/bm27/old-0997.html $B $L/cad7 &
wait
echo "| cadet vs c1 | $(grep -E 'IDENTICAL|DIFFERENCES' $L/cad1/cadet.log | tail -1) |" >> $L/summary.md
echo "| cadet vs 0.99.7 | $(grep -E 'IDENTICAL|DIFFERENCES' $L/cad7/cadet.log | tail -1) |" >> $L/summary.md; echo GATESDONE >> $L/summary.md
