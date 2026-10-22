#!/bin/bash
S=/tmp/claude-0/-home-user-Cadet-game/019501c3-ea82-5c10-ac85-e5cbe4c6d05b/scratchpad; G=/home/user/Cadet-game; export CADET_CHROME=/opt/pw-browsers/chromium
cd $G
r() { local name=$1; shift; local t0=$(date +%s); timeout 3600 "$@" > $S/p5_$name.log 2>&1; echo "$name: exit $? in $(( $(date +%s) - t0 )) s: $(tail -1 $S/p5_$name.log)"; }
(cd $S/ct && r cadet python3 $G/cadet_test.py $S/old5.html $G/starship-cadet.html)
r shots python3 $G/plans/opt-probes/keep_shots.py $S/old5.html $G/starship-cadet.html $S/ks5
r bytes python3 $G/plans/opt-probes/merge_bytes.py $S/old5.html $G/starship-cadet.html
r detach python3 $G/plans/opt-probes/heap_tour.py $G/starship-cadet.html
r day python3 day_check.py starship-cadet.html
r events python3 events_check.py starship-cadet.html
r interactions python3 interactions_check.py starship-cadet.html
(mkdir -p $S/pc5 && cd $S/pc5 && r perf python3 $G/perf_check.py $G/starship-cadet.html)
r player python3 player_check.py starship-cadet.html
r fast bash check_fast.sh
echo ALL DONE
