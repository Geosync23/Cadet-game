#!/usr/bin/env python3
"""affected.py: which checks a change needs (the optimization plan's item 1; the user's cadence, 2026-10-21: every turn
runs check_fast plus the checks this prints; the full round runs at every release and at least once a day).

    python3 tools/affected.py                    your branch since it left claude/integration, uncommitted changes included
    python3 tools/affected.py A                  A to now (uncommitted included)
    python3 tools/affected.py A B                A to B (e.g. a merge: M~1 M)
    --why                                        say which change picked each check
    --cmd                                        print the commands to run them (one browser check at a time)
    --map FILE                                   the map from real runs (default tools/check_map.json; missing: rules only)
    python3 tools/affected.py --merge OUT.json COVER.json ...   make the map from tools/check_cover.py runs

How it picks (the union of two lists; it never picks fewer than either):
  1. The rules: DEV_NOTES "Testing"'s "run it whenever ..." lines, by section (RULES below). Sections everything reads
     (setup, the deck builder, the current deck, ship time and save, the main loop) run every check.
  2. The map from real runs: each check run once under tools/check_cover.py, recording the game's functions it made
     run after the page was up. A change inside a top-level function picks the checks that ran it; a change to a table
     or other top-level name picks the checks that ran any function that uses it (tools/fn_index.js's refs); a new
     function picks the checks of the functions that use it. Code that only runs while the page opens picks LOAD_CHECKS.
  Files outside the game: a check's own file picks that check; cadet_test.py (every check's runner) picks all;
  content/ picks the lines checks and section 22's rules; tools/, plans/ and notes pick nothing.
check_fast.sh always runs on top (words baked, names, deck, machine, leave, device), so those four aren't listed.
Changes nothing. Exits 0.
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAME = 'starship-cadet.html'
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import section as S                                  # tools/section.py: the section headings

# check -> (command, minutes alone on 4 cores; plans/opt-measure.md section 4, rounded up)
CHECKS = {
    'cadet': ('python3 cadet_test.py OLD.html {g}', 2), 'player': ('python3 player_check.py {g}', 37),
    'intro': ('python3 intro_check.py {g}', 11), 'day1': ('python3 day_check.py {g} 1', 8),
    'interactions': ('python3 interactions_check.py {g}', 8), 'perf': ('python3 perf_check.py {g} OLD.html', 15),
    'mech': ('python3 mech_check.py {g}', 6), 'events': ('python3 events_check.py {g}', 6),
    'bubble': ('python3 bubble_check.py {g}', 5), 'devmode': ('python3 devmode_check.py {g}', 5),
    'disc': ('python3 disc_check.py {g}', 3), 'tiles': ('python3 tiles_check.py {g}', 3),
    'join': ('python3 join_check.py {g}', 3), 'clothes': ('python3 clothes_check.py {g}', 2),
    'path': ('python3 path_check.py {g}', 2), 'puzzle': ('python3 puzzle_check.py {g}', 2),
    'food': ('python3 food_check.py {g}', 2), 'career': ('python3 career_check.py {g}', 2),
    'social': ('python3 social_check.py {g}', 1), 'talk': ('python3 talk_check.py {g}', 1),
    'arc': ('python3 arc_check.py {g}', 1), 'lines': ('python3 lines_check.py {g}', 1),
    'bigevents': ('python3 bigevents_check.py {g}', 5),
    # in check_fast already (listed only so a check file of theirs is known)
    'deck': ('python3 deck_check.py {g}', 4), 'machine': ('python3 machine_check.py {g}', 1),
    'leave': ('python3 leave_check.py {g}', 1), 'device': ('python3 device_check.py {g}', 4),
}
FAST = {'deck', 'machine', 'leave', 'device'}
FILE_OF = {'cadet': 'cadet_test.py', 'day1': 'day_check.py'}
ALL = {c for c in CHECKS if os.path.exists(os.path.join(ROOT, FILE_OF.get(c, c + '_check.py')))}
LOAD_CHECKS = {'cadet', 'deck'}                       # code that runs only while the page opens: the pictures and the decks

# section -> checks: DEV_NOTES "Testing"'s run-it-whenever lines (as plans/opt-probes/affected_estimate.py, reviewed by
# ER2; '*' = every check). A section not listed runs every check, so a new section is never missed.
RULES = {
    'page': ['cadet', 'interactions', 'bubble'], '1': ['*'], '2': ['cadet', 'deck'], '3': ['cadet', 'deck'], '4': ['*'], '4a': ['*'],
    '4b': ['cadet', 'deck', 'perf'], '4c': ['*'], '4d': ['cadet', 'deck', 'day1', 'events', 'path'], '4e': ['cadet', 'deck', 'disc', 'day1'],
    '5': ['cadet', 'perf'], '13': ['*'], '14': ['day1', 'events', 'food', 'machine', 'intro', 'cadet', 'join', 'bigevents'],
    '19': ['device', 'puzzle', 'player'], '15': ['player', 'interactions', 'clothes', 'leave'], '15b': ['interactions', 'player', 'join'],
    '15r': ['deck', 'disc', 'interactions'], '16': ['food', 'day1'], '17': ['machine', 'mech', 'career', 'puzzle'],
    '22': ['lines', 'talk', 'bubble'], '18': ['events', 'join', 'intro', 'bigevents'], '20': ['social', 'arc', 'bubble', 'lines'],
    '20c': ['social', 'arc'], '21': ['intro', 'clothes'], '21b': ['clothes'], '23': ['tiles'], '23b': ['disc'], '6': ['cadet', 'bubble'],
    '7': ['path', 'day1'], '8': ['cadet', 'perf'], '8b': ['cadet', 'perf', 'day1'], '9': ['day1', 'events', 'cadet', 'deck'],
    '10': ['day1', 'cadet', 'deck', 'events'], '8c': ['disc', 'day1', 'perf'], '11': ['cadet', 'interactions', 'bubble'],
    '25': ['devmode'], '12': ['*'],
}
for k in ['24', '24a', '24b', '24c', '24d', '24m', '24n', '24g', '24i', '24j', '24t', '24s', '24e', '24f', '24h', '24l', '24o', '24q', '24r', '24p']:
    RULES[k] = ['career', 'mech', 'leave']
RULES['24k'] = ['puzzle', 'mech', 'career']


def git(*a):
    return subprocess.run(['git', *a], cwd=ROOT, capture_output=True, text=True).stdout


def show(rev, path):
    """a file's text at a revision (None: the working tree)"""
    if rev is None:
        try:
            return open(os.path.join(ROOT, path), encoding='utf-8').read()
        except OSError:
            return ''
    r = subprocess.run(['git', 'show', f'{rev}:{path}'], cwd=ROOT, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ''


def index(text):
    """tools/fn_index.js on a copy of the game"""
    tmp = os.path.join(os.environ.get('TMPDIR', '/tmp'), f'_affected_{os.getpid()}.html')
    open(tmp, 'w', encoding='utf-8').write(text)
    try:
        out = subprocess.run(['node', os.path.join(ROOT, 'tools', 'fn_index.js'), tmp], capture_output=True, text=True)
        if out.returncode:
            return None
        return json.loads(out.stdout)
    finally:
        os.remove(tmp)


def changed_lines(a, b):
    """game lines changed: (old lines, new lines), from git diff -U0"""
    args = ['diff', '-U0', a] + ([b] if b else []) + ['--', GAME]
    old, new = set(), set()
    for m in re.finditer(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', git(*args), re.M):
        o, on, n, nn = int(m[1]), int(m[2] or 1), int(m[3]), int(m[4] or 1)
        old.update(range(o, o + on)); new.update(range(n, n + nn))
        if on == 0: old.add(o)                        # a pure insertion: the line it follows
        if nn == 0: new.add(n)
    return old, new


def container(decls, n):
    """the top-level declaration holding game line n (decls sorted by first line; they don't overlap)"""
    lo, hi = 0, len(decls)
    while lo < hi:
        m = (lo + hi) // 2
        if decls[m][0] <= n: lo = m + 1
        else: hi = m
    d = decls[lo - 1] if lo else None
    return d if d and d[0] <= n <= d[1] else None


def merge(out, covers):
    """the map: for each check, the top-level declarations whose functions it ran (after load, and at load)"""
    m = {'made_from': [], 'checks': {}}
    idx = {}
    for c in covers:
        j = json.load(open(c))
        game = next((x for x in j['args'] if x.endswith('.html')), None)
        key = j.get('game_sha1')
        if key not in idx:
            idx[key] = index(open(game, encoding='utf-8').read()) if game and os.path.exists(game) else None
        fi = idx[key]
        if not fi:
            print('no game file for', c); continue
        decls = sorted(fi['decls'])
        name = 'day1' if j['check'] == 'day_check' else 'cadet' if j['check'] == 'cadet_test' else j['check'].replace('_check', '')
        e = m['checks'].setdefault(name, {'run': set(), 'load': set(), 'exit': [], 'seconds': 0})
        for part in ('run', 'load'):
            for a, b, fname in j[part]:
                d = container(decls, a)
                if d: e[part].add(d[2])
        e['exit'].append(j['exit']); e['seconds'] += j['seconds']
        m['made_from'].append({'cover': os.path.basename(c), 'check': name, 'args': j['args'], 'game_sha1': key, 'exit': j['exit']})
    for e in m['checks'].values():
        e['run'], e['load'] = sorted(e['run']), sorted(e['load'] - e['run'])
    json.dump(m, open(out, 'w'), indent=0)
    print(f"map: {len(m['checks'])} checks -> {out}")


def pick(a, b, mp):
    """{check: [reasons]} for the change a..b (b None: the working tree)"""
    why = {}
    def add(cs, reason):
        for c in (ALL if '*' in cs else cs):
            if c in ALL and c not in FAST and reason not in why.get(c, []):
                why.setdefault(c, []).append(reason)
    files = [f for f in (git('diff', '--name-only', a, *( [b] if b else [])).split()) if f]
    if b is None:
        files += [f for f in git('ls-files', '--others', '--exclude-standard').split() if f not in files]
    for f in files:
        base = os.path.basename(f)
        if f == GAME:
            continue
        if f == 'cadet_test.py':
            add(['*'], 'cadet_test.py (every check runs on it)')
        elif re.fullmatch(r'[a-z0-9]+_check\.py', f) or f == 'day_check.py':
            c = 'day1' if f == 'day_check.py' else f[:-9]
            add([c], f)
        elif f.startswith('content/'):
            add(RULES['22'], f + ' (the words; content_gen --check is in check_fast)')
    if GAME not in files:
        return why, files
    old_t, new_t = show(a, GAME), show(b, GAME)
    old_l, new_l = changed_lines(a, b)
    fis = {'old': index(old_t) if mp and old_t else None, 'new': index(new_t) if mp and new_t else None}
    for side, text, lines in (('old', old_t, old_l), ('new', new_t, new_l)):
        if not lines:
            continue
        secs = S.sections(text.split('\n'))
        for s in sorted({S.where(secs, n)[0] for n in lines if S.where(secs, n)}):
            add(RULES.get(s, ['*']), f'section {s} (the rules)')
        if not mp:
            continue
        fi = fis[side]
        if not fi:
            add(['*'], f'the {side} game does not parse'); continue
        decls = sorted(fi['decls']); refs = fi['refs']
        names = {}
        for n in lines:
            d = container(decls, n)
            if d: names[d[2]] = d[3]
        o = fis['old' if side == 'new' else 'new']
        other = {d[2] for d in o['decls']} if o else set()
        for nm, kind in sorted(names.items()):
            users = [nm] if kind in ('function', 'class', 'statement') else []
            if kind not in ('function', 'class', 'statement') or nm not in other:
                users += refs.get(nm, [])             # a table, or a new / removed function: whoever uses it
            hit = False
            for c, e in mp['checks'].items():
                if any(u in e['run'] for u in users):
                    add([c], f'{nm} (the map: {c} ran {"it" if nm in e["run"] else "code that uses it"})'); hit = True
            if not hit and any(any(u in e['load'] for u in users) for e in mp['checks'].values()):
                add(LOAD_CHECKS, f'{nm} (the map: runs only while the page opens)')
    return why, files


if __name__ == '__main__':
    argv = sys.argv[1:]
    if argv[:1] == ['--merge']:
        merge(argv[1], argv[2:]); sys.exit(0)
    flags = {x for x in argv if x.startswith('--')}
    mpath = os.path.join(ROOT, 'tools', 'check_map.json')
    if '--map' in argv:
        mpath = argv[argv.index('--map') + 1]
    revs = [x for i, x in enumerate(argv) if not x.startswith('--') and (i == 0 or argv[i - 1] != '--map')]
    if not revs:
        base = git('merge-base', 'origin/claude/integration', 'HEAD').strip() or 'HEAD'
        revs = [base]
    a, b = revs[0], (revs[1] if len(revs) > 1 else None)
    mp = json.load(open(mpath)) if os.path.exists(mpath) else None
    why, files = pick(a, b, mp)
    mins = sum(CHECKS[c][1] for c in why)
    print(f"changes {a}..{b or 'now'}: {len(files)} file(s){'' if mp else ' (no map: the rules only)'}")
    print(f"run: check_fast + {len(why)} check(s), about {mins} min alone: {' '.join(sorted(why)) or '(nothing more)'}")
    if len(why) == len(ALL - FAST):
        print('  (that is every check: the full round)')
    if '--why' in flags:
        for c in sorted(why):
            print(f'  {c}: ' + '; '.join(why[c][:6]) + (f' (+{len(why[c]) - 6} more)' if len(why[c]) > 6 else ''))
    if '--cmd' in flags:
        print('  bash check_fast.sh')
        for c in sorted(why, key=lambda c: CHECKS[c][1]):
            print('  ' + CHECKS[c][0].format(g=GAME))
