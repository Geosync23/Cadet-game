S=/tmp/claude-0/-home-user-Cadet-game/2d242811-8ee1-50bd-a407-0716185f5cce/scratchpad
P="bash $S/pair.sh $S/ts /home/user/ts"
$P "m_final|python3 $S/mess/interactions_check.py $S/ts/new.html" "m_old|python3 $S/mess/interactions_check.py $S/ts/old.html"
$P "m_f1|python3 $S/mess/interactions_check.py $S/ts/f1.html" "m_f2|python3 $S/mess/interactions_check.py $S/ts/f2.html"
$P "m_f3|python3 $S/mess/interactions_check.py $S/ts/f3.html" "m_g54|python3 $S/mess/interactions_check.py $S/ts/g54.html"
$P "ar_new|python3 arrows_check.py $S/ts/new.html week" "ar_oldgame|python3 arrows_check.py $S/ts/old.html week"
$P "ct|cd $S/ts/ct && python3 /home/user/ts/cadet_test.py $S/ts/old.html $S/ts/new.html" "fast|CADET_WORK=/tmp/cadet-work bash check_fast.sh"
bash $S/pair.sh $S/d0 /home/user/d0 "ev_p1|python3 events_check.py $S/d0/p1.html 2" "d0time|python3 $S/time_probe.py $S/d0/new.html /home/user/d0"
