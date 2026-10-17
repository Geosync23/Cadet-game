#!/bin/bash
# mergeone.sh COMMIT "message"  — merge --no-ff, auto-resolve build-only conflicts, stop on anything else
S="$(cd "$(dirname "$0")" && pwd)"   # this folder (resolve.py)
cd "$(git -C "$S" rev-parse --show-toplevel)"
if git merge --no-ff -m "$2" "$1" >/tmp/m.txt 2>&1; then echo "$1 clean"; exit 0; fi
grep CONFLICT /tmp/m.txt
for f in $(git diff --name-only --diff-filter=U); do
  case $f in *.md) python3 $S/resolve.py $f ${BUILD:-0.60.0} --union;; *) python3 $S/resolve.py $f ${BUILD:-0.60.0};; esac
done
if grep -l '^<<<<<<< ' $(git diff --name-only --diff-filter=U) 2>/dev/null; then echo "STOP: hand-resolve"; exit 1; fi
git add -A && git commit -q --no-edit && echo "$1 resolved"
