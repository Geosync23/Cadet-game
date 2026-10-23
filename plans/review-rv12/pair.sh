# usage: pair.sh OUTDIR CODEDIR "name|cmd" ...   runs jobs two at a time, each in its own CADET_WORK, cwd CODEDIR
export CADET_CHROME=/opt/pw-browsers/chromium
OUT=$1; CODE=$2; shift 2; mkdir -p $OUT
run() { local n=${1%%|*} c=${1#*|}; local W=/tmp/work-$n; mkdir -p $W/test; ln -sfn /tmp/cadet-work/three $W/three; ln -sfn /tmp/cadet-work/acorn $W/acorn
  ( cd $CODE && CADET_WORK=$W bash -c "$c" > $OUT/$n.txt 2>&1; echo "$n exit $? $(date -u +%H:%M)" >> $OUT/$n.txt; tail -n1 $OUT/$n.txt >> $OUT/summary.txt ); }
while [ $# -gt 0 ]; do run "$1" & if [ $# -gt 1 ]; then run "$2" & fi; wait; shift; [ $# -gt 0 ] && shift; done
