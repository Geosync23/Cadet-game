# cad.sh OLD NEW LOGDIR : cadet_test alone
mkdir -p $3/cw/test; ln -sfn /tmp/cadet-work/three $3/cw/three; cp $1 $3/old.html; cp $2 $3/new.html; cd $3
CADET_WORK=$3/cw CADET_CHROME=/opt/pw-browsers/chromium python3 /home/user/Cadet-game/cadet_test.py old.html new.html > cadet.log 2>&1; echo "exit $?" >> cadet.log
