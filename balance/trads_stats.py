# BAL1: stats from balance/data/trads.json (made by trads_sim.py)
import json, pathlib, collections
D = json.loads((pathlib.Path(__file__).parent / 'data' / 'trads.json').read_text())
WD = 'Mon Tue Wed Thu Fri Sat Sun'.split()
def most(lst):   # how many you can attend in full (greedy by end time), each with a 5-minute walk between
    n, end = 0, -1
    for e in sorted(lst, key=lambda e: e['to']):
        if e['from'] >= end + 5: n += 1; end = e['to']
    return n
rows = []
for x in D:
    L = [e for e in x['list'] if e.get('from') is not None]
    # what a day-shift player can reach: not during the shift (09:00-17:00, Fri to 15:30), awake 06:00-23:30
    shift = (540, 930 if x['wd'] == 4 else 1020) if x['work'] else None
    reach = [e for e in L if e['from'] >= 360 and e['to'] <= 1410 and not (shift and e['from'] < shift[1] and e['to'] > shift[0])]
    eve = [e for e in reach if e['from'] >= 1020]
    over = sum(1 for i, a in enumerate(reach) for b in reach[i + 1:] if a['from'] < b['to'] and b['from'] < a['to'])
    rows.append(dict(d=x['d'], wd=WD[x['wd']], work=x['work'], all=len(L), reach=len(reach), eve=len(eve), overlaps=over, attend=most(reach), eve_mins=sum(e['to'] - e['from'] for e in eve)))
for r in rows: print(r)
w = collections.defaultdict(list)
for r in rows: w[(r['d'] - 1) // 7 + 1].append(r)
print('week: on, reachable, evening, overlapping pairs, most you can attend')
for k, v in w.items(): print(k, sum(r['all'] for r in v), sum(r['reach'] for r in v), sum(r['eve'] for r in v), sum(r['overlaps'] for r in v), sum(r['attend'] for r in v))
(pathlib.Path(__file__).parent / 'data' / 'trads_stats.json').write_text(json.dumps(rows))
