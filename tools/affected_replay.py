#!/usr/bin/env python3
"""affected_replay.py: proves tools/affected.py on real history (the optimization plan's item 1; option (a), the user's
"Careful", 2026-10-21 19:15: the rules + the coverage map as it is).

    python3 tools/affected_replay.py [--map FILE] [--last N] [--branch REF] [--middle]

--middle: option (b) on trial (the user, 2026-10-21 21:45): also replays affected.py --middle beside (a); it is
adopted only if it too picks every known failure.

1. The last N (default 20) commits that changed the game on REF (default origin/claude/integration; merges left out):
   for each, the checks affected.py picks for C~1..C, rules alone and rules + map, and their minutes alone.
2. The known failures (plans/opt-cover/failures.md: a commit and the checks it really broke): each failed check must be
   picked for that commit, by affected.py's list or by check_fast (deck, machine, leave, device). Any miss is a hole in
   the rules or the map, to be fixed there, never here.
Exits 1 if any known failure is missed.
"""
import os, re, sys, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import affected as A

argv = sys.argv[1:]
def opt(name, default):
    return argv[argv.index(name) + 1] if name in argv else default
mpath = opt('--map', os.path.join(ROOT, 'tools', 'check_map.json'))
last, ref = int(opt('--last', '20')), opt('--branch', 'origin/claude/integration')
MID = '--middle' in argv
mp = json.load(open(mpath)) if os.path.exists(mpath) else None
if not mp:
    print(f'no map at {mpath}: the rules only')
FULL = sum(A.CHECKS[c][1] for c in A.ALL - A.FAST)
mins = lambda cs: sum(A.CHECKS[c][1] for c in cs)

print(f'1. The last {last} game commits on {ref} (full round: {len(A.ALL - A.FAST)} checks, {FULL} min; check_fast on top of each)')
rows = []
for c in A.git('log', '--no-merges', f'-n{last}', '--format=%h %s', ref, '--', A.GAME).splitlines():
    h, subj = c.split(' ', 1)
    rules, _ = A.pick(f'{h}~1', h, None)
    both, _ = A.pick(f'{h}~1', h, mp) if mp else (rules, None)
    mid, _ = A.pick(f'{h}~1', h, mp, True) if mp and MID else (both, None)
    rows.append((len(rules), mins(rules), len(both), mins(both), len(mid), mins(mid)))
    extra = sorted(set(both) - set(rules))
    print(f'  {h} rules {len(rules):2} ({mins(rules):3} min)  (a) {len(both):2} ({mins(both):3} min)'
          + (f'  (b) {len(mid):2} ({mins(mid):3} min){" FULL" if any("safeguard" in r for v in mid.values() for r in v) else ""}' if MID else '')
          + f'  {subj[:55]}')
    if extra:
        print(f'      the map adds: {" ".join(extra)}')
if rows:
    n = len(rows)
    print(f'  average: rules {sum(r[0] for r in rows) / n:.1f} checks ({sum(r[1] for r in rows) / n:.0f} min); '
          f'(a) {sum(r[2] for r in rows) / n:.1f} checks ({sum(r[3] for r in rows) / n:.0f} min)'
          + (f'; (b) {sum(r[4] for r in rows) / n:.1f} checks ({sum(r[5] for r in rows) / n:.0f} min)' if MID else ''))

print('2. Known failures (plans/opt-cover/failures.md): each must be picked')
missed, missed_b, total = [], [], 0
for line in open(os.path.join(ROOT, 'plans', 'opt-cover', 'failures.md')):
    m = re.match(r'\|\s*([0-9a-f]{7,40})\s*\|\s*([^|]+)\|', line)
    if not m:
        continue
    h = m[1]
    inh = re.search(r'Inherited from ([0-9a-f]{7,40})', line)   # a failure the commit only carried from an earlier one (proved)
    if inh:
        print(f'  {h}: its failure was inherited from {inh[1]} (failures.md): checked against {inh[1]}')
        h = inh[1]
    want = [w.split('(')[0].strip() for w in m[2].split(',')]
    want = [('day1' if w in ('day', 'day_check') else w) for w in want if w]   # 'day1', 'day13': a day of its own
    if A.git('cat-file', '-t', h).strip() != 'commit':
        print(f'  {h}: not in this clone (git fetch --unshallow)'); missed.append((h, '?')); continue
    rules, _ = A.pick(f'{h}~1', h, None)
    both, _ = A.pick(f'{h}~1', h, mp) if mp else (rules, None)
    mid, _ = A.pick(f'{h}~1', h, mp, True) if mp and MID else (None, None)
    for w in want:
        total += 1
        how = 'check_fast' if w in A.FAST else 'rules' if w in rules else 'map' if w in both else None
        line = f'  {h} {w:13} (a) {"picked by " + how if how else "MISSED"}  ({len(both)} checks, {mins(both)} min)'
        if not how:
            missed.append((h, w))
        if mid is not None:
            hb = 'check_fast' if w in A.FAST else 'rules' if w in rules else ('safeguard' if any('safeguard' in r for r in mid.get(w, [])) else 'map') if w in mid else None
            line += f'  (b) {"picked by " + hb if hb else "MISSED"} ({len(mid)} checks, {mins(mid)} min)'
            if not hb:
                missed_b.append((h, w))
        print(line)
print(f'(a): {total - len(missed)} of {total} known failures picked' + (': ' + ', '.join(f'{h} {w}' for h, w in missed) if missed else ''))
if MID:
    print(f'(b): {total - len(missed_b)} of {total} known failures picked' + (': ' + ', '.join(f'{h} {w}' for h, w in missed_b) if missed_b else ''))
sys.exit(1 if missed or missed_b else 0)
