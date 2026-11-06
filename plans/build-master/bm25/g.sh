# g.sh COMMIT NAME : worktree, check_fast alone, then cadet alone vs 0.99.6; summary in /tmp/bm24/NAME/summary.md
C=$1; N=$2; W=/tmp/bm24/wt-$N; L=/tmp/bm24/$N; mkdir -p $L
cd /home/user/Cadet-game && git worktree add -q -f $W $C 2>/dev/null; cd $W
sha256sum starship-cadet.html > $L/sha.txt
bash /home/user/Cadet-game/plans/build-master/run1.sh check_fast $L /tmp/bm24/w-$N bash check_fast.sh
bash /tmp/bm24/cad.sh /tmp/bm24/old-0996.html $W/starship-cadet.html $L/cad
echo "| cadet | $(grep -E 'ALL IDENTICAL|DIFFER|differ' $L/cad/cadet.log | tail -1) $(tail -1 $L/cad/cadet.log) |" >> $L/summary.md
echo GATEDONE >> $L/summary.md
