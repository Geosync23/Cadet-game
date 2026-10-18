#!/bin/bash
# build0607.sh DIR TIP... — merge tips in order onto origin/claude/cand-0606 in worktree DIR (git -C), resolve build lines, carry 068b8db's social_check fix
R="$(cd "$(dirname "$0")" && pwd)"   # plans/build-master (resolve.py, verify_merge.py)
W=$1; shift; cd $W || exit 1
git show origin/claude/reviews:name_check.py > /tmp/name_check_bm.py 2>/dev/null
git checkout -q -- . 2>/dev/null; git reset -q --hard origin/claude/cand-0606
for c in "$@"; do
  git merge --no-ff -m "WIP 0.60.7: merge $c ($(git log --format=%s -1 $c | cut -c1-70))" $c > /tmp/cw/m.txt 2>&1
  if git diff --name-only --diff-filter=U | grep -q .; then
    python3 $R/resolve.py starship-cadet.html 0.60.7 >/dev/null; python3 $R/resolve.py DEV_NOTES.md 0.60.7 --union >/dev/null
    for f in $(git diff --name-only --diff-filter=U); do grep -q "^<<<<<<<" $f && { echo "STOP at $c: $f"; exit 2; }; done
    git add -A; git commit -q --no-edit
  fi
  git merge-base --is-ancestor $c HEAD || { echo "NOT MERGED $c"; cat /tmp/cw/m.txt; exit 3; }
done
python3 - <<'PY'
s=open('social_check.py').read()
old="""          if (jump) { setShipNow(t0 + 2 * 1440); socialTo(t0 + 2 * 1440); } else for (let t = t0 + 60; t <= t0 + 2 * 1440; t += 60) { setShipNow(t); socialTo(t); }"""
new="""          const mn = () => { if (typeof machinesNow === 'function') machinesNow(); };   // as the game's clock does each tick (sim engineer 5, claude/social 068b8db: else the hour-by-hour arm never runs the last hour's machines)
          if (jump) { setShipNow(t0 + 2 * 1440); mn(); socialTo(t0 + 2 * 1440); } else for (let t = t0 + 60; t <= t0 + 2 * 1440; t += 60) { setShipNow(t); mn(); socialTo(t); }"""
if old in s: open('social_check.py','w').write(s.replace(old,new)); print('social_check: 068b8db fix applied')
elif 'mn(); socialTo' in s: print('social_check: fix already there')
else: print('social_check: PATTERN NOT FOUND')
PY
grep -c "^## Current build" DEV_NOTES.md; grep -n "build 0.60\|GAME_BUILD = '" starship-cadet.html | cut -c1-80
python3 $R/verify_merge.py origin/claude/cand-0606 HEAD starship-cadet.html "$@" | tail -$(( $# + 1 )) | cut -c1-160
python3 content_gen.py starship-cadet.html | tail -1; python3 /tmp/name_check_bm.py starship-cadet.html | tail -1
