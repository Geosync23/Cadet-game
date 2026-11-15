import json, sys
l = json.load(open(sys.argv[1])); d = sys.argv[2]; cut = int(sys.argv[3]) if len(sys.argv) > 3 else 400
kinds = sys.argv[4].split(',') if len(sys.argv) > 4 else None
rows = [(e[0], e[1], e[2][:50], e[3][:cut]) for e in l['ev']] + [(a[0], 'ARROW', '', str(a[1])) for a in l['arrows']] + [(a[0], 'ACT', '', str(a[1])[:160]) for a in l['acts'] if not str(a[1]).startswith('read on')] + [(a[0], 'STATE', '', str(a[1:])) for a in l['state']]
def key(r):
    p = r[0].split(' '); day = int(p[1].rstrip(',')); h, m = p[-1].split(':'); return day * 1440 + int(h) * 60 + int(m)
prev = None; seen = set(); FROM = sys.argv[5] if len(sys.argv) > 5 else '00:00'
for r in sorted(rows, key=key):
    if not r[0].startswith('Day ' + d + ','): continue
    if kinds and r[1] not in kinds: continue
    line = (r[0].split(' ')[-1], r[1], r[2], r[3])
    if line[1:] == prev or line[0] < FROM: continue
    if r[1] in ('TOAST','ACT') and (r[1], r[3]) in seen and r[1]=='TOAST': continue
    seen.add((r[1], r[3]))
    prev = line[1:]; print(*line)
