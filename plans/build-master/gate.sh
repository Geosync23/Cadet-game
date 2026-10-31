# gate.sh WT LOGDIR OLDHTML "laneA cmds;..." "laneB cmds;..."  each cmd: name:script args (BUILD = $B)
WT=$1; L=$2; OLD=$3; A=$4; Bl=$5; S=$(dirname $0); mkdir -p $L; cd $WT; B=$WT/starship-cadet.html
sha256sum $B > $L/sha.txt; R="bash $S/run1.sh"
CHECK_LOGS=$L/cf $R check_fast $L /tmp/wg1-cf bash check_fast.sh
lane() { IFS=';' read -ra C <<< "$1"; for c in "${C[@]}"; do n=${c%%:*}; cmd=${c#*:}; $R $n $L $2 ${cmd//BUILD/$B}; done; }
( lane "$A" /tmp/wg1-a ) &
( lane "$Bl" /tmp/wg1-b ) &
wait; echo LANESDONE >> $L/summary.md
cd $L; cp $OLD old.html; cp $B new.html
mkdir -p /tmp/wg1-cad/test; ln -sfn /tmp/cadet-work/three /tmp/wg1-cad/three
CADET_WORK=/tmp/wg1-cad CADET_CHROME=/opt/pw-browsers/chromium python3 $WT/cadet_test.py old.html new.html > cadet.log 2>&1; echo "| cadet | exit $? , $(tail -1 cadet.log) |" >> summary.md
echo ALLDONE >> $L/summary.md
