#!/bin/bash
# mg.sh DIR BASE OUT TIP... : merge tips onto BASE in worktree DIR (build lines auto; the 24a/24e block and mech_check PARTS by union), bake to OUT
W=$1; B=$2; O=$3; shift 3; cd $W || exit 1
git merge --abort 2>/dev/null; git reset -q --hard; git clean -qfd; git checkout -q -B scratch $B
for c in "$@"; do
  git merge --no-ff -m "WIP 0.63.4: merge $c" $c > /tmp/cw/m.txt 2>&1
  if git diff --name-only --diff-filter=U | grep -q .; then
    python3 /tmp/cw/bm/resolve.py starship-cadet.html 0.63.4 >/dev/null; python3 /tmp/cw/bm/resolve.py DEV_NOTES.md 0.63.4 --union >/dev/null
    python3 /tmp/cw/union.py $c
    for f in $(git diff --name-only --diff-filter=U); do grep -q "^<<<<<<<" $f && { echo "STOP at $c: $f"; exit 2; }; done
    git add -A; git commit -q --no-edit
  fi
  git merge-base --is-ancestor $c HEAD || { echo "NOT MERGED $c"; exit 3; }
done
python3 /tmp/cw/bm/setbuild.py starship-cadet.html 0.63.4; git commit -qam "set build 0.63.4" ; python3 content_gen.py starship-cadet.html | tail -1; cp starship-cadet.html $O; git checkout -q -- .; git log --oneline -1 | cat
