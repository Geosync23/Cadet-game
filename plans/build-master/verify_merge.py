#!/usr/bin/env python3
"""verify_merge.py BASE RESULT FILE C1 C2 ...  — every helper's added lines are in RESULT, every removed line is gone
(unless another helper's tip or the base-minus-removals still keeps it). Build lines ignored. Generated blocks reported apart."""
import subprocess, sys, re, collections
base, result, path, tips = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
def show(c):
    return subprocess.run(['git', 'show', f'{c}:{path}'], capture_output=True, text=True).stdout.split('\n')
BUILD = re.compile(r"build \d+\.\d+\.\d+|GAME_BUILD = '|^## Current build")
def diff(a, b):
    a = subprocess.run(['git', 'merge-base', a, b], capture_output=True, text=True).stdout.strip()
    out = subprocess.run(['git', 'diff', '-U0', a, b, '--', path], capture_output=True, text=True).stdout.split('\n')
    add, rem = collections.Counter(), collections.Counter()
    for l in out:
        if l.startswith('+++') or l.startswith('---'): continue
        if l.startswith('+'): add[l[1:]] += 1
        elif l.startswith('-'): rem[l[1:]] += 1
    return add, rem
res = collections.Counter(show(result))
bad = 0
for c in tips:
    add, rem = diff(base, c)
    keep_elsewhere = collections.Counter()
    for o in tips:
        if o != c: keep_elsewhere.update(diff(base, o)[0])
    missing = [l for l in add if l.strip() and not BUILD.search(l) and res[l] < 1]
    stale = [l for l in rem if l.strip() and not BUILD.search(l) and res[l] > 0 and keep_elsewhere[l] == 0
             and collections.Counter(show(base))[l] <= rem[l]]
    print(f'== {c}: +{sum(add.values())} -{sum(rem.values())}; missing {len(missing)}, deleted-but-present {len(stale)}')
    for l in missing[:8]: print('   MISSING ', l[:150])
    for l in stale[:8]: print('   STILL-HERE', l[:150])
    bad += len(missing) + len(stale)
print('problems:', bad)
