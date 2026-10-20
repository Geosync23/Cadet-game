#!/usr/bin/env bash
# proof.sh CHECK VARIANT: run one check, old (the 0.64.2 tip's copy) or new (WW1's), on the real game or a planted one
SP=/tmp/claude-0/-home-user-Cadet-game/20b35820-69de-572a-bcef-edc37077bc59/scratchpad
c=$1; v=$2; G=/home/user/Cadet-game/starship-cadet.html
case $v in old) D=$SP/old ;; *) D=/home/user/Cadet-game ;; esac
W=/tmp/pw-$c-$v; rm -rf $W; mkdir -p $W/test; ln -sfn /tmp/cadet-work/three $W/three
cd $W
if [ $c = cadet_test ]; then A="$G $G"; [ $v = plant ] && A="$G $SP/plant/look.html"
else A=$G; [ $v = plant ] && A=$SP/plant/err.html; fi
X=""
t=$(date +%s)
CADET_WORK=$W CADET_CHROME=/opt/pw-browsers/chromium timeout 2400 python3 $D/$c.py $A $X > $SP/proof/$c.$v.txt 2>&1
echo "exit $? ($(( $(date +%s) - t )) s)" >> $SP/proof/$c.$v.txt
