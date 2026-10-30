# Lower bound for item 1: which checks the DEV_NOTES "run it whenever" rules alone pick, for recent single turns
# (non-merge commits that changed the game on claude/integration's history). The coverage map can only add to these.
import subprocess, re, sys
RULES = {   # section -> checks (DEV_NOTES "Testing" run-it-whenever lines, condensed; '*' = everything)
 'page': ['cadet', 'interactions', 'bubble'], '1': ['*'], '2': ['cadet', 'deck'], '3': ['cadet', 'deck'], '4': ['*'], '4a': ['*'], '4b': ['cadet', 'deck', 'perf'],
 '4c': ['*'], '4d': ['cadet', 'deck', 'day1', 'events', 'path'], '4e': ['cadet', 'deck', 'disc', 'day1'], '5': ['cadet', 'perf'],
 '13': ['*'], '14': ['day1', 'events', 'food', 'machine', 'intro', 'cadet', 'join'], '19': ['device', 'puzzle', 'player'],
 '15': ['player', 'interactions', 'clothes', 'leave'], '15b': ['interactions', 'player', 'join'], '15r': ['deck', 'disc', 'interactions'],
 '16': ['food', 'day1'], '17': ['machine', 'mech', 'career', 'puzzle'], '22': ['lines', 'talk', 'bubble'], '18': ['events', 'join', 'intro'],
 '20': ['social', 'arc', 'bubble', 'lines'], '20c': ['social', 'arc'], '21': ['intro', 'clothes'], '21b': ['clothes'], '23': ['tiles'], '23b': ['disc'],
 '6': ['cadet', 'bubble'], '7': ['path', 'day1'], '8': ['cadet', 'perf'], '8b': ['cadet', 'perf', 'day1'], '9': ['day1', 'events', 'cadet', 'deck'],
 '10': ['day1', 'cadet', 'deck', 'events'], '8c': ['disc', 'day1', 'perf'], '11': ['cadet', 'interactions', 'bubble'], '25': ['devmode'], '12': ['*'],
}
for k in ['24', '24a', '24b', '24c', '24d', '24m', '24n', '24g', '24i', '24j', '24t', '24s', '24e', '24f', '24h', '24l', '24o', '24q', '24r', '24p']: RULES[k] = ['career', 'mech', 'leave']
RULES['24k'] = ['puzzle', 'mech', 'career']
FAST = {'deck', 'machine', 'leave', 'device'}
T = {'player': 2199, 'intro': 669, 'day1': 466, 'interactions': 455, 'perf': 446, 'mech': 310, 'events': 302, 'bubble': 289, 'devmode': 253, 'device': 241,
     'deck': 189, 'disc': 154, 'tiles': 145, 'join': 141, 'cadet': 94, 'clothes': 85, 'path': 84, 'puzzle': 71, 'food': 66, 'career': 63, 'machine': 52,
     'social': 30, 'talk': 28, 'leave': 26, 'arc': 22, 'lines': 4}
ALL = set(T)
log = subprocess.run(['git', 'log', '--no-merges', '--format=%h %s', '-n', sys.argv[1] if len(sys.argv) > 1 else '20', 'origin/claude/integration', '--', 'starship-cadet.html'], capture_output=True, text=True).stdout.splitlines()
tot_n = tot_t = 0; rows = []
for l in log:
    h, msg = l.split(' ', 1)
    out = subprocess.run(['python3', 'tools/section.py', '--diff', h + '~1', h], capture_output=True, text=True).stdout
    secs = sorted({m[1] for m in re.finditer(r'^\s+(\S+)\s+-\d+\s+\+\d+', out, re.M)})
    pick = set()
    for s in secs:
        r = RULES.get(s, ['*']); pick |= ALL if '*' in r else set(r)
    pick -= FAST; full = len(pick) == len(ALL - FAST)
    t = sum(T[c] for c in pick); tot_n += len(pick); tot_t += t
    rows.append(f"{h} | {','.join(secs) or '(comments only)'} | {len(pick)} checks, {t // 60} min{' (everything)' if full else ''} | {msg[:70]}")
print('\n'.join(rows)); n = len(log)
print(f'AVERAGE over {n} turns: {tot_n / n:.1f} checks (plus check_fast), {tot_t / n / 60:.0f} min, against {len(ALL - FAST)} checks / {sum(T[c] for c in ALL - FAST) // 60} min for all of them')
