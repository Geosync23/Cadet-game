#!/bin/bash
# runcommit.sh COMMIT OLDCOMMIT — export COMMIT's tree to /tmp/cw/run_<sha>, run every check there against OLDCOMMIT's build
set -e
BM=${BM:-$(cd "$(dirname "$0")" && pwd)}
cd "$(git -C "$BM" rev-parse --show-toplevel)"
C=$(git rev-parse --short $1); D=/tmp/cw/run_$C
rm -rf $D; mkdir -p $D; git archive $C | tar -x -C $D
git show $2:starship-cadet.html > $D/old.html
git show origin/claude/reviews:name_check.py > $D/name_check.py; cp "$BM/smoke_check.py" "$BM/newgame_check.py" $D/
cd $D; export CADET_CHROME=/opt/pw-browsers/chromium; B=starship-cadet.html; set +e
python3 name_check.py $B > log_name_check.txt 2>&1; echo "name_check exit=$? 0s" >> summary.txt
python3 content_gen.py $B --check > log_content_gen.txt 2>&1; echo "content_gen_check exit=$? 0s" >> summary.txt
s=$(date +%s); timeout 600 python3 smoke_check.py $B > log_smoke_check.txt 2>&1; echo "smoke_check exit=$? $(( $(date +%s)-s ))s" >> summary.txt
s=$(date +%s); timeout 300 python3 newgame_check.py $B > log_newgame_check.txt 2>&1; echo "newgame_check exit=$? $(( $(date +%s)-s ))s" >> summary.txt
for f in *_check.py; do case $f in name_check.py|smoke_check.py|newgame_check.py|day_check.py) continue;; esac
  n=${f%.py}; s=$(date +%s); timeout 1500 python3 $f $B > log_$n.txt 2>&1; echo "$n exit=$? $(( $(date +%s)-s ))s" >> summary.txt; done
s=$(date +%s); timeout 1500 python3 day_check.py $B 0 > log_day_check0.txt 2>&1; echo "day_check(0) exit=$? $(( $(date +%s)-s ))s" >> summary.txt
s=$(date +%s); timeout 1500 python3 day_check.py $B 1 > log_day_check.txt 2>&1; echo "day_check(1) exit=$? $(( $(date +%s)-s ))s" >> summary.txt
s=$(date +%s); timeout 1500 python3 cadet_test.py old.html $B > log_cadet_test.txt 2>&1; echo "cadet_test exit=$? $(( $(date +%s)-s ))s" >> summary.txt
echo DONE >> summary.txt
