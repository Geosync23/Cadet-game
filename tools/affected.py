#!/usr/bin/env python3
"""affected.py: which checks a change needs (the optimization plan's item 1; the user's cadence, 2026-10-21: every turn
runs check_fast plus the checks this prints; the full round runs at every release and at least once a day).

    python3 tools/affected.py                    your branch since it left claude/integration, uncommitted changes included
    python3 tools/affected.py A                  A to now (uncommitted included)
    python3 tools/affected.py A B                A to B (e.g. a merge: M~1 M)
    --why                                        say which change picked each check
    --cmd                                        print the commands to run them (one browser check at a time)
    --map FILE                                   the map from real runs (default tools/check_map.json; missing: rules only)
    --middle                                     option (b), on trial: lines nearly every check runs pick by the rules only,
                                                 and changing one runs the full round
    python3 tools/affected.py --merge OUT.json COMMIT COVER.json ...   the map from tools/check_cover.py runs on COMMIT's game

How it picks (the union of two lists; it never picks fewer than either):
  1. The rules: DEV_NOTES "Testing"'s "run it whenever ..." lines, by section (RULES below). Sections everything reads
     (setup, the deck builder, the current deck, ship time and save, the main loop) run every check.
  2. The map from real runs (tools/check_map.json): each check run once under tools/check_cover.py, recording the game
     lines it made run after the page was up (block coverage). A change picks every check that ran one of the changed
     lines of the old side (a pure insertion: the lines either side), moved into the map's own game by a diff; a changed
     table or other top-level value picks every check that ran a line reading it (tools/fn_index.js's uses). Lines that
     ran only while the page opened pick LOAD_CHECKS. This is option (a), the user's "Careful" (2026-10-21): any check
     that runs a changed line is picked; tools/affected_replay.py proves it on history and the known failures.
  Files outside the game: a check's own file picks that check; cadet_test.py (every check's runner) picks all;
  content/ picks the lines checks and section 22's rules; tools/, plans/ and notes pick nothing.
check_fast.sh always runs on top (words baked, names, deck, machine, leave, device), so those four aren't listed.
Changes nothing. Exits 0.
"""
import hashlib, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAME = 'starship-cadet.html'
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import section as S                                  # tools/section.py: the section headings

# check -> (command, minutes alone on 4 cores; plans/opt-measure.md section 4, rounded up)
CHECKS = {
    'cadet': ('python3 cadet_test.py OLD.html {g}', 2), 'player': ('python3 player_check.py {g}', 6),
    'intro': ('python3 intro_check.py {g}', 11), 'day1': ('python3 day_check.py {g} 1', 8),
    # the event days (lead 25, 2026-10-21: day_check on Day 1 alone misses an event day's own failures): Day 0 the
    # arrival, the first Friday's address 5, the Line 7, the storm's front 12 and its Saturday 13, the comet 16, Day 19's
    # address and night shift, the first crew rotation 21, the diplomatic finale 27 (EV_CALENDAR, EV_BEATS, ROSTER_ROTATIONS)
    **{f'day{d}': (f'python3 day_check.py {{g}} {d}', 8) for d in (0, 5, 7, 12, 13, 15, 16, 17, 19, 21, 22, 23, 24, 25, 26, 27)},   # 15, 16: Pillar 5 Step 5's Tier 3 test and Senior Officer days (S5-1); 23-26: Step 6's nights, the badge, the move, mentoring and Calder's question (W6; 17 and 22 were in EVENT_DAYS but not here, so the picker never offered them)
    'interactions': ('python3 interactions_check.py {g}', 8), 'perf': ('python3 perf_check.py {g} OLD.html', 15),
    'mech': ('python3 mech_check.py {g}', 6), 'events': ('python3 events_check.py {g}', 6),
    'bubble': ('python3 bubble_check.py {g}', 5), 'devmode': ('python3 devmode_check.py {g}', 5), 'dev_arrow': ('python3 dev_arrow_check.py {g}', 2),   # Dev mode's career arrow (DV1)
    'arrows_pointer': ('python3 arrows_pointer_check.py {g}', 4),   # the panel pointer (arrows plan, piece C)
    'disc': ('python3 disc_check.py {g}', 3), 'tiles': ('python3 tiles_check.py {g}', 3),
    'join': ('python3 join_check.py {g}', 3), 'weekend': ('python3 weekend_check.py {g}', 12), 'clothes': ('python3 clothes_check.py {g}', 2),
    'path': ('python3 path_check.py {g}', 2), 'puzzle': ('python3 puzzle_check.py {g}', 2),
    'food': ('python3 food_check.py {g}', 2), 'career': ('python3 career_check.py {g}', 2),
    'social': ('python3 social_check.py {g}', 1), 'talk': ('python3 talk_check.py {g}', 2),
    'arc': ('python3 arc_check.py {g}', 1), 'lines': ('python3 lines_check.py {g}', 1),
    'bigevents': ('python3 bigevents_check.py {g}', 5), 'fridays': ('python3 fridays_check.py {g}', 4),
    'sound': ('python3 sound_check.py {g}', 5),   # section 27, sound and music (0.93.0; ~7.5 min beside two other checks)
    'promo_beats': ('python3 promo_beats_check.py {g}', 3),   # the promotion beats on paper (0.93.2, FX28)   # section 27, sound and music (0.93.0; ~7.5 min beside two other checks)
    'saves': ('python3 saves_check.py {g}', 3),   # the save slots and the Saves app (0.93.2, FX27)
    'ending': ('python3 ending_check.py {g}', 2),   # the ending on paper (EN1; plans/ending-spec.html): off, the offer, your answer
    # in check_fast already (listed only so a check file of theirs is known)
    'deck': ('python3 deck_check.py {g}', 4), 'machine': ('python3 machine_check.py {g}', 1),
    'leave': ('python3 leave_check.py {g}', 1), 'device': ('python3 device_check.py {g}', 4),
}
FAST = {'deck', 'machine', 'leave', 'device'}
EVENT_DAYS = ['day0', 'day5', 'day7', 'day12', 'day13', 'day15', 'day16', 'day17', 'day19', 'day21', 'day22', 'day23', 'day24', 'day25', 'day26']   # 0.93.2, the event swap: the visit's greeting Day 17, the comet Day 22 (were day16, day27); 23-26: Pillar 5 Step 6 (W6, with P5_STEP6 on; off, plain days)
FILE_OF = {'cadet': 'cadet_test.py', 'day1': 'day_check.py', **{d: 'day_check.py' for d in EVENT_DAYS}}
ALL = {c for c in CHECKS if os.path.exists(os.path.join(ROOT, FILE_OF.get(c, c + '_check.py')))}
LOAD_CHECKS = {'cadet', 'deck'}                       # code that runs only while the page opens: the pictures and the decks

# section -> checks: DEV_NOTES "Testing"'s run-it-whenever lines (as plans/opt-probes/affected_estimate.py, reviewed by
# ER2; '*' = every check). A section not listed runs every check, so a new section is never missed.
RULES = {
    'page': ['cadet', 'interactions', 'bubble'], '1': ['*'], '2': ['cadet', 'deck'], '3': ['cadet', 'deck'], '4': ['*'], '4a': ['*'],
    '4b': ['cadet', 'deck', 'perf'], '4c': ['*'], '4d': ['cadet', 'deck', 'day1', 'events', 'path'], '4e': ['cadet', 'deck', 'disc', 'day1'],
    '5': ['cadet', 'perf'], '13': ['*'], '14': ['day1', 'events', 'food', 'machine', 'intro', 'cadet', 'join', 'bigevents', 'fridays', 'day12', 'day21'],
    '19': ['device', 'puzzle', 'player', 'arrows_pointer', 'saves'], '15': ['player', 'interactions', 'clothes', 'leave'], '15b': ['interactions', 'player', 'join', 'arrows_pointer'],
    '15r': ['deck', 'disc', 'interactions'], '16': ['food', 'day1'], '17': ['machine', 'mech', 'career', 'puzzle'],
    '22': ['lines', 'talk', 'bubble'], '18': ['events', 'join', 'weekend', 'intro', 'bigevents', 'fridays', 'day7', 'day12', 'day13', 'day17', 'day22'],
    '18f': ['fridays', 'events', 'join', 'intro', 'bigevents', 'day1', 'food', 'perf', 'day5', 'day19'], '20': ['social', 'arc', 'bubble', 'lines'],
    '20c': ['social', 'arc'], '21': ['intro', 'clothes', 'day0', 'saves'], '21b': ['clothes'], '23': ['tiles'], '23b': ['disc'], '6': ['cadet', 'bubble'],
    '7': ['path', 'day1'], '8': ['cadet', 'perf'], '8b': ['cadet', 'perf', 'day1'], '9': ['day1', 'events', 'cadet', 'deck', 'day21'],
    '10': ['day1', 'cadet', 'deck', 'events'], '8c': ['disc', 'day1', 'perf'], '11': ['cadet', 'interactions', 'bubble'],
    '25': ['devmode', 'dev_arrow', 'saves'], '12': ['*'],
}
for k in ['24', '24a', '24b', '24c', '24d', '24m', '24n', '24g', '24i', '24j', '24t', '24s', '24e', '24f', '24h', '24l', '24o', '24q', '24r', '24p']:
    RULES[k] = ['career', 'mech', 'leave']
RULES['24k'] = ['puzzle', 'mech', 'career']
# Pillar 5 Step 5 (S5-1): picked by the rules alone until the map is remade
RULES['24u'] = ['career', 'mech', 'leave', 'events', 'bigevents', 'saves', 'dev_arrow', 'devmode', 'day15', 'day16']
RULES['24v'] = ['career', 'mech', 'leave', 'machine']
RULES['24w'] = ['career', 'mech', 'leave', 'machine', 'day1', 'food', 'saves']
RULES['24x'] = ['career', 'mech', 'leave', 'machine', 'deck']
# Pillar 5 Step 6 (W6's first turn; plans/p5-step6-spec.html section 8): section 28 and its sub-sections, by the rules alone until the map is remade
RULES['28'] = ['career', 'mech', 'leave', 'events', 'bigevents', 'day22', 'day23', 'day24', 'day25', 'day26']
RULES['28a'] = ['career', 'mech', 'leave', 'player', 'clothes', 'food', 'saves', 'events', 'day1', 'day22', 'day23', 'day24', 'day25']
RULES['28b'] = ['career', 'mech', 'bigevents', 'day22']
RULES['28c'] = ['career', 'mech', 'machine', 'day23']
RULES['28d'] = ['career', 'mech', 'day24']
RULES['28e'] = ['career', 'mech', 'social', 'arc', 'day26']
RULES['28f'] = ['career', 'fridays', 'social', 'arc', 'day26']
RULES['24u'] = RULES['24u'] + ['day22', 'day23', 'day25']   # S6-3's Engine Specialist and the move
# the ending (section 29, EN1; plans/ending-spec.html): picked by the rules alone until the map is remade
RULES['29'] = ['ending', 'events', 'bigevents', 'saves', 'social', 'day1', 'devmode']
RULES['29a'] = ['ending', 'events', 'bigevents', 'social', 'talk', 'saves', 'day1']
RULES['29b'] = ['ending', 'saves', 'devmode', 'deck', 'events', 'bigevents', 'perf', 'day1', 'cadet']
RULES['29c'] = ['ending', 'lines', 'talk', 'social', 'events', 'bigevents', 'career', 'day1']


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


def lines_of(ranges):
    return {n for a, b in ranges for n in range(a, b + 1)}


def merge(out, commit, covers):
    """the map: for each check, the game lines it ran (after the page was up) and those that ran only while it opened"""
    m = {'commit': commit, 'game_sha1': None, 'made_from': [], 'checks': {}}
    want = hashlib.sha1(show(commit, GAME).encode()).hexdigest()
    for c in covers:
        j = json.load(open(c))
        if j.get('game_sha1') != want:
            print(f'{c}: ran on another game than {commit}\'s: left out'); continue
        name = 'day' + (j['args'][1] if len(j['args']) > 1 else '1') if j['check'] == 'day_check' else 'cadet' if j['check'] == 'cadet_test' else j['check'].replace('_check', '')
        m['checks'][name] = {'run': j['run'], 'load': j['load'], 'exit': j['exit'], 'seconds': j['seconds'], 'args': j['args']}
        m['made_from'].append(os.path.basename(c))
    m['game_sha1'] = want
    json.dump(m, open(out, 'w'))
    print(f"map: {len(m['checks'])} checks on {commit} -> {out}")


def translate(src, dst, lines):
    """game lines of revision src -> the same lines in revision dst (a line in a changed stretch -> that whole stretch)"""
    if src == dst or show(src, GAME) == show(dst, GAME):
        return set(lines)
    hunks = [(int(m[1]), int(m[2] or 1), int(m[3]), int(m[4] or 1))
             for m in re.finditer(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', git('diff', '-U0', src, *([dst] if dst else []), '--', GAME), re.M)]
    out = set()
    for n in lines:
        shift = 0
        for o, on, d, dn in hunks:
            o_end = o + on - 1 if on else o
            if on and o <= n <= o_end:                # inside a changed stretch
                out.update(range(d, d + dn) if dn else (d, d + 1)); break
            if (o_end if on else o) < n:
                shift = (d + dn - 1 if dn else d) - o_end
            else:
                out.add(n + shift); break
        else:
            out.add(n + shift)
    return out


SHARED = .8   # option (b): a line that at least this share of the map's checks ran (rounded up; 23 of 28) is everyone's


def pick(a, b, mp, middle=False):
    """{check: [reasons]} for the change a..b (b None: the working tree). middle: option (b), on trial (the user,
    2026-10-21 21:45): the map leaves out lines nearly every check runs (SHARED), and a change to one of those runs the
    full round (the safeguard)"""
    why = {}
    def add(cs, reason):
        for c in (ALL if '*' in cs else cs):
            if c in ALL and c not in FAST and reason not in why.get(c, []):
                why.setdefault(c, []).append(reason)
    files = [f for f in (git('diff', '--name-only', a, *([b] if b else [])).split()) if f]
    if b is None:
        files += [f for f in git('ls-files', '--others', '--exclude-standard').split() if f not in files]
    for f in files:
        if f == GAME:
            continue
        if f == 'cadet_test.py':
            add(['*'], 'cadet_test.py (every check runs on it)')
        elif re.fullmatch(r'[a-z0-9_]+_check\.py', f) or f == 'day_check.py':
            add(['day1'] + EVENT_DAYS if f == 'day_check.py' else [f[:-9]], f)
        elif f.startswith('content/'):
            add(RULES['22'], f + ' (the words; content_gen --check is in check_fast)')
    if GAME not in files:
        return why, files
    old_t, new_t = show(a, GAME), show(b, GAME)
    old_l, new_l = changed_lines(a, b)
    for text, lines in ((old_t, old_l), (new_t, new_l)):
        secs = S.sections(text.split('\n'))
        for s in sorted({S.where(secs, n)[0] for n in lines if S.where(secs, n)}):
            add(RULES.get(s, ['*']), f'section {s} (the rules)')
    if not mp:
        return why, files
    # the map: the old side's changed lines (a pure insertion: the lines either side), in the map's own game
    base = mp['commit']
    fo, fm = index(old_t), index(show(base, GAME))
    if not fo or not fm:
        add(['*'], 'the game does not parse'); return why, files
    od = sorted(fo['decls'])
    here = set(old_l) | {n + 1 for n in old_l}
    at = translate(a, base, here) if a != base else here
    runs = {c: lines_of(e['run']) for c, e in mp['checks'].items()}
    loads = {c: lines_of(e['load']) for c, e in mp['checks'].items()}
    md = sorted(fm['decls'])
    shared = set()
    if middle:
        cnt = {}
        for c in runs:
            for n in runs[c]: cnt[n] = cnt.get(n, 0) + 1
        need = -(-int(SHARED * 100) * len(runs) // 100)
        shared = {n for n, k in cnt.items() if k >= need}
        # the safeguard: a changed shared line (a pure insertion: when the lines both sides of it are shared) runs everything
        hunks = re.finditer(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', git('diff', '-U0', a, *([b] if b else []), '--', GAME), re.M)
        hard = set()
        for m in hunks:
            o, on = int(m[1]), int(m[2] or 1)
            if on:
                hard |= translate(a, base, set(range(o, o + on))) if a != base else set(range(o, o + on))
            else:
                both = translate(a, base, {o, o + 1}) if a != base else {o, o + 1}
                if both and both <= shared: hard |= both
        if hard & shared:
            add(['*'], f'changed lines nearly every check runs ({len(hard & shared)}): option (b)\'s safeguard, the full round')
            return why, files
        runs = {c: r - shared for c, r in runs.items()}
    def name_at(n):
        d = container(md, n); return d[2] if d else f'line {n}'
    # 1. the changed lines themselves: which checks ran them
    hit = {}
    for n in sorted(at):
        for c in runs:
            if n in runs[c]: hit.setdefault(c, set()).add(name_at(n))
    for c, names in hit.items():
        add([c], f'{", ".join(sorted(names)[:3])}{" ..." if len(names) > 3 else ""} (the map: {c} ran the changed lines)')
    if any(n in loads[c] for n in at for c in loads):
        add(LOAD_CHECKS, 'changed lines run only while the page opens (the map)')
    # 2. a changed table or other top-level value: which checks ran a line that reads it
    for n in sorted(old_l):
        d = container(od, n)
        if not d or d[3] not in ('table', 'state'):
            continue
        uses = set(fm['uses'].get(d[2], [])) - shared
        got = [c for c in runs if uses & runs[c]]
        for c in got:
            add([c], f'{d[2]} (the map: {c} ran a line that reads it)')
        if not got and any(uses & loads[c] for c in loads):
            add(LOAD_CHECKS, f'{d[2]} (read only while the page opens, by the map)')
    return why, files


if __name__ == '__main__':
    argv = sys.argv[1:]
    if argv[:1] == ['--merge']:
        merge(argv[1], argv[2], argv[3:]); sys.exit(0)
    flags = {x for x in argv if x.startswith('--')}
    mpath = os.path.join(ROOT, 'tools', 'check_map.json')
    if '--map' in argv:
        mpath = argv[argv.index('--map') + 1]
    revs = [x for i, x in enumerate(argv) if not x.startswith('--') and (i == 0 or argv[i - 1] != '--map')]
    if not revs:
        base = git('merge-base', 'origin/claude/integration', 'HEAD').strip() or 'HEAD'
        revs = [base]
    a, b = revs[0], (revs[1] if len(revs) > 1 else None)
    try:
        mp = json.load(open(mpath)) if os.path.exists(mpath) else None
    except ValueError:
        print(f'{mpath}: not a map (tools/affected.py --merge makes one)'); sys.exit(2)
    why, files = pick(a, b, mp, '--middle' in flags)
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
