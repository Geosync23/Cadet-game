#!/bin/bash
C=/tmp/cand; L=$1; X=/tmp/r3scripts/run.sh; mkdir -p $L
G1="idle save calls touch walk pick lift door day games unplug odd"
G2="shut off quiet base deck pick1 panels api lists tiles disc screens marks touch3 drop settings a11y firstuse cards clock devpad edge savesland sound saves words"
G3="m19 m20 s5cases s6cases vessel ending m21 m24 team m23 deck6 promo4 promo3"
G4="nights mentor props jobs2 beam court"
$X $C /tmp/work-r3b $L sound_alone python3 sound_check.py starship-cadet.html
( $X $C /tmp/work-r3 $L ctl_G3 python3 controller_check.py starship-cadet.html $G3
  $X $C /tmp/work-r3 $L ctl_G2 python3 controller_check.py starship-cadet.html $G2
  echo LANE_A_DONE >> $L/summary.txt ) &
( W=/tmp/work-r3b
  $X $C $W $L devmode python3 devmode_check.py starship-cadet.html
  $X $C $W $L dev_arrow python3 dev_arrow_check.py starship-cadet.html
  $X $C $W $L promo_sight python3 promo_sight_check.py starship-cadet.html
  $X $C $W $L arrows_d python3 arrows_d_check.py starship-cadet.html
  $X $C $W $L arrows_f python3 arrows_f_check.py starship-cadet.html
  $X $C $W $L ending python3 ending_check.py starship-cadet.html
  $X $C $W $L ctl_G4 python3 controller_check.py starship-cadet.html $G4
  $X $C $W $L ctl_G1 python3 controller_check.py starship-cadet.html $G1
  echo LANE_B_DONE >> $L/summary.txt ) &
wait; echo ROUND_DONE >> $L/summary.txt
