#!/bin/bash
# usage: run.sh REPO WORK LOGDIR NAME cmd...   (runs from REPO, 90 min timeout)
REPO=$1; WORK=$2; LOGS=$3; NAME=$4; shift 4
mkdir -p $LOGS; cd $REPO
export CADET_WORK=$WORK CADET_CHROME=/opt/pw-browsers/chromium
s=$(date +%s)
timeout 5400 "$@" > $LOGS/$NAME.txt 2>&1; rc=$?
echo "$NAME exit $rc ($(( $(date +%s)-s )) s) | $(tail -1 $LOGS/$NAME.txt)" >> $LOGS/summary.txt
