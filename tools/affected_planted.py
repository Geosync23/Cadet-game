#!/usr/bin/env python3
"""affected_planted.py: planted faults for tools/affected.py (lead 25's ask, 2026-10-21: most known failures come from
commits that pick nearly every check, so they prove less than they sound; these are small faults in ONE section each,
the check they break chosen OUTSIDE that section's rules, so only the map can pick it).

    python3 tools/affected_planted.py            on paper: each fault's picks by the rules, (a) and (b) (--middle)
    python3 tools/affected_planted.py --run      also runs each fault's check on its faulty copy: it must FAIL there
                                                 (one browser check at a time; about 40 min; CADET_CHROME as usual)

Each fault is one exact-string change to the game at HEAD, made in a throwaway git worktree and committed there (local
only, never pushed) so affected.py can diff it. A fault whose check passes on its copy proves nothing: --run says so.
Exits 1 if (a) or (b) misses a fault's check, or (with --run) a fault's check doesn't fail.
"""
import os, re, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import affected as A

# (name, section, the check it must break (not in the section's rules), old, new)
FAULTS = [
    ('escort to a tile goes nowhere', '10', 'intro',
     "  if (Array.isArray(to.tile)) return to.tile;\n  const tiles = to.room && ROOM_TILES[to.room];",
     "  if (Array.isArray(to.tile)) return null;\n  const tiles = to.room && ROOM_TILES[to.room];"),
    ('a crew member seeking you never shows', '20', 'intro',
     "function seekArrive(a) { const c = SEEK_COME; SEEK_COME = null; if (c && !CHAT && !SEEK) seekShow(c.p, c.m, c.why, a); }",
     "function seekArrive(a) { const c = SEEK_COME; SEEK_COME = null; }"),
    ('a work step starts afresh every time', '15', 'mech',
     "  const P = SHIP.player, w = wsFind(j.id, k); if (w && w.how === how) return w;",
     "  const P = SHIP.player, w = wsFind(j.id, k);"),
    ('a gathering finds no tiles', '14', 'career',
     "  for (let k = 1; k <= 3 && tiles.length < ids.length; k++) for (let dj = -k; dj <= k; dj++) for (let di = -k; di <= k; di++) {",
     "  for (let k = 1; k <= 0 && tiles.length < ids.length; k++) for (let dj = -k; dj <= k; dj++) for (let di = -k; di <= k; di++) {"),
    ('every day an event day', '18', 'mech',
     "function eventDay(d) {\n  if (!EV_GUARD_ON) return false;",
     "function eventDay(d) {\n  if (!EV_GUARD_ON) return true;"),
    ('your tasting vote is not kept', '18', 'food',
     "  SHIP.events.votes[id + '@' + d] = choice; return true;\n}",
     "  return true;\n}"),
]


def git(*a, cwd=ROOT):
    return subprocess.run(['git', *a], cwd=cwd, capture_output=True, text=True)


def main():
    run = '--run' in sys.argv
    mp = A.json.load(open(os.path.join(ROOT, 'tools', 'check_map.json')))
    base = git('rev-parse', 'HEAD').stdout.strip()
    tmp = tempfile.mkdtemp(prefix='planted_')
    wt = os.path.join(tmp, 'wt')
    git('worktree', 'add', '-q', '--detach', wt, base)
    bad = []
    try:
        for name, sec, want, old, new in FAULTS:
            game = os.path.join(wt, A.GAME)
            git('checkout', '-q', base, '--', A.GAME, cwd=wt)
            text = open(game, encoding='utf-8').read()
            if text.count(old) != 1:
                print(f'{name}: the line to change is not in the game once ({text.count(old)}): fault out of date'); bad.append(name); continue
            open(game, 'w', encoding='utf-8').write(text.replace(old, new))
            git('commit', '-q', '-am', f'planted: {name}', cwd=wt)
            c = git('rev-parse', 'HEAD', cwd=wt).stdout.strip()
            in_rules = want in A.RULES.get(sec, [])
            rules, _ = A.pick(base, c, None)
            pa, _ = A.pick(base, c, mp)
            pb, _ = A.pick(base, c, mp, True)
            mins = lambda cs: sum(A.CHECKS[x][1] for x in cs)
            ok_a, ok_b = want in pa, want in pb
            print(f'{name} (section {sec}; {want}{" IS in its rules" if in_rules else ", not in its rules"}): '
                  f'rules {"picks" if want in rules else "misses"} it ({len(rules)}); (a) {"picks" if ok_a else "MISSES"} it '
                  f'({len(pa)} checks, {mins(pa)} min); (b) {"picks" if ok_b else "MISSES"} it ({len(pb)} checks, {mins(pb)} min)')
            if not (ok_a and ok_b):
                bad.append(name)
            if run:
                copy = os.path.join(tmp, f'fault_{len(bad)}_{want}.html')
                shutil.copy(game, copy)
                cmd = A.CHECKS[want][0].format(g=copy).split()
                if 'OLD.html' in cmd:
                    cmd[cmd.index('OLD.html')] = os.path.join(ROOT, A.GAME)
                r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
                tail = [l for l in (r.stdout + r.stderr).splitlines() if 'FAIL' in l or 'PROBLEM' in l][:3]
                print(f'    {want} on the faulty copy: exit {r.returncode}' + (': ' + ' | '.join(t.strip()[:140] for t in tail) if tail else ''))
                if r.returncode == 0:
                    print('    the check PASSES with the fault: this fault proves nothing'); bad.append(name + ' (not caught)')
    finally:
        git('worktree', 'remove', '--force', wt)
        shutil.rmtree(tmp, ignore_errors=True)
    print(f'{len(FAULTS) - len(bad)} of {len(FAULTS)} planted faults picked by (a) and (b)' + (' and failed by their check' if run else '')
          + (': not ' + '; '.join(bad) if bad else ''))
    sys.exit(1 if bad else 0)


main()
