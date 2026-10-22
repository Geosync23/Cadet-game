#!/usr/bin/env python3
"""affected_planted.py: planted faults for tools/affected.py (lead 25's ask, 2026-10-21: most known failures come from
commits that pick nearly every check, so they prove less than they sound; these are small faults in ONE section each,
the check they break chosen OUTSIDE that section's rules, so only the map can pick it).

    python3 tools/affected_planted.py            on paper: each fault's picks by the rules, (a) and (b) (--middle)
    python3 tools/affected_planted.py --run [--only TEXT] [--out DIR]
                                                 also runs each fault's check on its faulty copy: it must FAIL there
                                                 with a FAIL or error the game as it is doesn't print (known FAILs don't count),
                                                 or exit 1 where the game as it is exits 0 (a crash, page errors);
                                                 --only runs the faults whose name holds TEXT; --out keeps each output
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
    ('a typo in the seek chip (seekEl, not seekEl())', '20', 'intro',
     "  const el = seekEl(), U = k => schedU(p.seed ^ seekSalt(), m, k);",
     "  const el = seekEl, U = k => schedU(p.seed ^ seekSalt(), m, k);"),
    ('a due tool no longer slows a look step', '15', 'mech',
     "(o.tool && typeof toolSlow === 'function' ? toolSlow(o.tool) : 1)",
     "1"),
    ('a typo in eventDay (fals)', '18', 'career',
     "function eventDay(d) {\n  if (!EV_GUARD_ON) return false;",
     "function eventDay(d) {\n  if (!EV_GUARD_ON) return fals;"),
    ('a typo in the health check booking (pls.id)', '21', 'player',
     "where: pl.id, kind: 'checkup', status: 'yes', by: 'rina', title: INTRO_HEALTH_TITLE });",
     "where: pls.id, kind: 'checkup', status: 'yes', by: 'rina', title: INTRO_HEALTH_TITLE });"),
    ('your tasting vote is not kept', '18', 'food',
     "  SHIP.events.votes[id + '@' + d] = choice; return true;\n}",
     "  return true;\n}"),
]


def git(*a, cwd=ROOT):
    return subprocess.run(['git', *a], cwd=cwd, capture_output=True, text=True)


def fails(text):
    """a check's FAIL lines, numbers taken out (so a known FAIL with other numbers is still the known one)"""
    return {re.sub(r'[0-9.]+', '#', l.strip())[:120] for l in text.splitlines()
            if (re.search(r'\bFAIL\b|PROBLEM', l) and 'FAILED' not in l) or re.search(r'pageerror|Error:|Traceback', l)}


def run_check(want, game):
    cmd = A.CHECKS[want][0].format(g=game).split()
    if 'OLD.html' in cmd:
        cmd[cmd.index('OLD.html')] = os.path.join(ROOT, A.GAME)
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def main():
    run = '--run' in sys.argv
    only = sys.argv[sys.argv.index('--only') + 1] if '--only' in sys.argv else None
    out_dir = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else None
    if out_dir: os.makedirs(out_dir, exist_ok=True)
    base_fails, done = {}, 0
    mp = A.json.load(open(os.path.join(ROOT, 'tools', 'check_map.json')))
    base = git('rev-parse', 'HEAD').stdout.strip()
    tmp = tempfile.mkdtemp(prefix='planted_')
    wt = os.path.join(tmp, 'wt')
    git('worktree', 'add', '-q', '--detach', wt, base)
    bad = []
    try:
        for f in FAULTS:
            name, sec, want, old, new = f
            if only and only not in name:
                continue
            done += 1
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
                if want not in base_fails:                  # the check on the game as it is: its exit and known FAILs
                    clean = os.path.join(tmp, 'base.html'); shutil.copy(os.path.join(ROOT, A.GAME), clean)
                    c0, o0 = run_check(want, clean); base_fails[want] = (c0, fails(o0))
                    if out_dir: open(os.path.join(out_dir, f'base-{want}.txt'), 'w').write(o0)
                code, out = run_check(want, copy)
                if out_dir: open(os.path.join(out_dir, f'fault-{FAULTS.index(f) + 1}-{want}.txt'), 'w').write(out)
                c0, known = base_fails[want]
                new = sorted(fails(out) - known)
                err = [l.strip() for l in out.splitlines() if re.search(r'pageerror|Error:|error:', l)][:2]
                print(f'    {want} on the faulty copy: exit {code} (the game as it is: {c0}); new FAILs: {len(new)}'
                      + (': ' + ' | '.join(x[:110] for x in new[:3]) if new else '') + (' | errors: ' + ' | '.join(e[:140] for e in err) if err else ''))
                if code == 0 or not (new or c0 == 0):
                    print('    the check shows nothing new with the fault: this fault proves nothing'); bad.append(name + ' (not caught)')
    finally:
        git('worktree', 'remove', '--force', wt)
        shutil.rmtree(tmp, ignore_errors=True)
    print(f'{done - len(bad)} of {done} planted faults picked by (a) and (b)' + (' and failed by their check' if run else '')
          + (': not ' + '; '.join(bad) if bad else ''))
    sys.exit(1 if bad else 0)


main()
