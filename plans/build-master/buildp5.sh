#!/bin/bash
# buildp5.sh DIR TIP... (BUILD=x.y.z) — merge tips in order onto origin/claude/p5-cand in worktree DIR, resolve build lines, verify, bake, name check
R="$(cd "$(dirname "$0")" && pwd)"   # plans/build-master (resolve.py, verify_merge.py)
W=$1; shift; cd $W || exit 1; : ${BUILD:?set BUILD}
git show origin/claude/reviews:name_check.py > /tmp/name_check_bm.py 2>/dev/null
git checkout -q -- . 2>/dev/null; git reset -q --hard origin/claude/p5-cand
for c in "$@"; do
  git merge --no-ff -m "WIP $BUILD: merge $c ($(git log --format=%s -1 $c | cut -c1-70))" $c > /tmp/cw/m.txt 2>&1
  if git diff --name-only --diff-filter=U | grep -q .; then
    python3 $R/resolve.py starship-cadet.html $BUILD >/dev/null; python3 $R/resolve.py DEV_NOTES.md $BUILD --union >/dev/null
    for f in $(git diff --name-only --diff-filter=U); do grep -q "^<<<<<<<" $f && { echo "STOP at $c: $f"; exit 2; }; done
    git add -A; git commit -q --no-edit
  fi
  git merge-base --is-ancestor $c HEAD || { echo "NOT MERGED $c"; cat /tmp/cw/m.txt; exit 3; }
done
grep -c "^## Current build" DEV_NOTES.md; grep -n "  build [0-9]\|GAME_BUILD = '" starship-cadet.html | cut -c1-80
python3 $R/verify_merge.py origin/claude/p5-cand HEAD starship-cadet.html "$@" | tail -$(( $# + 1 )) | cut -c1-160
python3 content_gen.py starship-cadet.html | tail -1; python3 /tmp/name_check_bm.py starship-cadet.html | tail -1
