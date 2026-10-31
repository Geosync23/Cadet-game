# run1.sh NAME LOGDIR WORK cmd...   runs one check, records exit, seconds, last OK/FAIL line
name=$1; logdir=$2; work=$3; shift 3
mkdir -p $work/test; ln -sfn /tmp/cadet-work/three $work/three; ln -sfn /tmp/cadet-work/acorn $work/acorn
t0=$(date +%s)
CADET_WORK=$work CADET_CHROME=/opt/pw-browsers/chromium "$@" > $logdir/$name.log 2>&1; rc=$?
t=$(( $(date +%s) - t0 ))
last=$(grep -E "OK|FAIL" $logdir/$name.log | tail -1 | cut -c1-120)
echo "| $name | exit $rc ${t}s, $last |" >> $logdir/summary.md
grep -n "FAIL" $logdir/$name.log | head -5 | sed "s/^/   $name: /" >> $logdir/fails.txt
