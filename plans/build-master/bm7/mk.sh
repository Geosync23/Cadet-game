#!/bin/bash
# mk.sh WT OUT TIP...: merge tips onto 2bc08d5 in WT; build lines auto; mech_check keep-both; teach-loop combine; stop on anything else
W=$1; O=$2; shift 2; cd $W || exit 1
git merge --abort 2>/dev/null; git reset -q --hard; git clean -qfd; git checkout -q -B scratch-$(basename $W) 2bc08d5
for c in "$@"; do
  git merge --no-ff -m "WIP 0.63.4: merge $c" $c > /tmp/cw/m.txt 2>&1
  u=$(git diff --name-only --diff-filter=U)
  if [ -n "$u" ]; then
    python3 /tmp/cw/bm/resolve.py starship-cadet.html 0.63.4 >/dev/null; python3 /tmp/cw/bm/resolve.py DEV_NOTES.md 0.63.4 --union >/dev/null
    grep -q '^<<<<<<<' mech_check.py && { python3 /tmp/cw/bm/unionall.py $c mech_check.py; echo "  $c: mech_check keep both"; }
    if grep -q '^<<<<<<<' starship-cadet.html; then python3 /tmp/cw/teach.py $c && echo "  $c: teach loop combined"; fi
    for f in $u; do grep -q "^<<<<<<<" $f && { echo "STOP at $c: $f"; exit 2; }; done
    git add -A; git commit -q --no-edit
  fi
  git merge-base --is-ancestor $c HEAD || { echo "NOT MERGED $c"; cat /tmp/cw/m.txt | tail -3; exit 3; }
done
python3 -c "import ast;ast.parse(open('mech_check.py').read())" || exit 4
python3 /tmp/cw/bm/setbuild.py starship-cadet.html 0.63.4 >/dev/null; git commit -qam "set build 0.63.4" 2>/dev/null
python3 content_gen.py starship-cadet.html | tail -1; cp starship-cadet.html $O; git checkout -q -- .
python3 /tmp/cw/bm/name_check.py $O | tail -1
node -e "const s=require('fs').readFileSync('$O','utf8');require('fs').writeFileSync('/tmp/cw/s.js',s.match(/<script>([\s\S]*?)<\/script>/)[1])" && node --check /tmp/cw/s.js && echo parses
python3 /tmp/cw/bm/verify_merge.py 2bc08d5 HEAD starship-cadet.html "$@" 2>&1 | grep -v "^   "
