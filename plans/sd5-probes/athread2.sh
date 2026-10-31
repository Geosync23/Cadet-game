#!/bin/bash
# SD5: audio-thread CPU (% of one core over each 10 s) of renderer $1, with log $2's last row
declare -A last
while [ -d /proc/$1 ]; do
  tot=0
  for t in /proc/$1/task/*; do
    [ "$(cat $t/comm 2>/dev/null)" = "AudioOutputDevi" ] || continue
    id=$(basename $t); v=$(awk '{print $14+$15}' $t/stat 2>/dev/null); [ -z "$v" ] && continue
    p=${last[$id]:-$v}; tot=$((tot + v - p)); last[$id]=$v
  done
  echo "$(date +%T) audio ${tot}% $(tail -1 $2 | python3 -c 'import sys,json; r=json.loads(sys.stdin.read()); print(r["wall"], r["where"], r["music"], "live", r["live"], "under", r["under"])' 2>/dev/null)"
  sleep 10
done
