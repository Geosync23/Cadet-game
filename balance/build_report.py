# BAL1: builds the balance report page (balance/report/balance-report.html) from the raw tables in balance/data/
# and the needs model (needs_sim.py). Run: python3 balance/build_report.py
import json, pathlib, html, sys
HERE = pathlib.Path(__file__).resolve().parent; DATA = HERE / 'data'
sys.path.insert(0, str(HERE)); import needs_sim as N
J = lambda n: json.loads((DATA / n).read_text())
C = {p: J(f'career_{p}.json') for p in ('quick', 'steady', 'relaxed', 'half', 'lazy', 'slacker', 'skipper')}
NEEDS = J('needs.json'); SWEEP = J('needs_sweep.json'); TR = J('trads_stats.json')
esc = html.escape

# ---------- a small SVG line chart (one scale per axis, ticks only at values the chart reaches) ----------
def chart(series, x0, x1, y0, y1, xt, yt, ylab, refs=(), w=640, h=260, steps=False, xlab='Day', ytick_fmt=str, label_dy=None, jitter=0):
    L, R, T, B = 44, 150, 14, 34
    sx = lambda x: L + (x - x0) / (x1 - x0) * (w - L - R)
    sy = lambda y: T + (1 - (y - y0) / (y1 - y0)) * (h - T - B)
    o = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{esc(ylab)} by {xlab.lower()}" class="chart">']
    for v in yt:
        o.append(f'<line x1="{L}" x2="{w - R}" y1="{sy(v):.1f}" y2="{sy(v):.1f}" class="grid"/><text x="{L - 6}" y="{sy(v) + 4:.1f}" class="tick" text-anchor="end">{ytick_fmt(v)}</text>')
    for v in xt:
        o.append(f'<text x="{sx(v):.1f}" y="{h - B + 16}" class="tick" text-anchor="middle">{v}</text>')
    o.append(f'<line x1="{L}" x2="{w - R}" y1="{h - B}" y2="{h - B}" class="axis"/>')
    o.append(f'<text x="{L}" y="{h - 4}" class="axlab">{esc(xlab)}</text><text x="{L - 40}" y="{T - 2}" class="axlab" dominant-baseline="hanging" transform="rotate(0)"></text>')
    for ri, r in enumerate(refs):
        if r[0] == 'y':
            o.append(f'<line x1="{L}" x2="{w - R}" y1="{sy(r[1]):.1f}" y2="{sy(r[1]):.1f}" class="ref"/><text x="{w - R - 4}" y="{sy(r[1]) - 5:.1f}" class="reflab" text-anchor="end">{esc(r[2])}</text>')
        else:
            o.append(f'<line x1="{sx(r[1]):.1f}" x2="{sx(r[1]):.1f}" y1="{T}" y2="{h - B}" class="ref"/><text x="{sx(r[1]) + 4:.1f}" y="{T + 10 + 14 * ri}" class="reflab">{esc(r[2])}</text>')
    ends = []
    for i, (name, pts, slot) in enumerate(series):
        pts = [(x, y + (i - (len(series) - 1) / 2) * jitter) for x, y in pts if x0 <= x <= x1]
        d = ''
        for k, (x, y) in enumerate(pts):
            if k == 0: d += f'M{sx(x):.1f},{sy(y):.1f}'
            elif steps: d += f'H{sx(x):.1f}V{sy(y):.1f}'
            else: d += f'L{sx(x):.1f},{sy(y):.1f}'
        o.append(f'<path d="{d}" class="ln s{slot}"/>')
        for x, y in pts:
            o.append(f'<circle cx="{sx(x):.1f}" cy="{sy(y):.1f}" r="7" class="hit"><title>{esc(name)}: {xlab} {x}, {ytick_fmt(round(y) if jitter else round(y, 1))}</title></circle>')
        if pts: ends.append([sy(pts[-1][1]), name, slot, w - R])
    ends.sort()
    for k in range(1, len(ends)):
        if ends[k][0] - ends[k - 1][0] < 13: ends[k][0] = ends[k - 1][0] + 13
    for y, name, slot, x in ends:
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="0"/><rect x="{x + 6:.1f}" y="{y - 4:.1f}" width="10" height="3" rx="1.5" class="sw s{slot}f"/><text x="{x + 20:.1f}" y="{y + 1:.1f}" class="dl">{esc(name)}</text>')
    o.append('</svg>')
    return '<div class="chartwrap">' + ''.join(o) + '</div>'

def bars(rows, vmax, unit='%', w=640):   # rows: (label, [(seg name, value, slot)])  horizontal grouped bars
    bh, gap, L = 14, 4, 150
    h = sum(len(r[1]) * (bh + gap) + 12 for r in rows) + 10
    sx = lambda v: L + v / vmax * (w - L - 130)
    o = [f'<svg viewBox="0 0 {w} {h}" class="chart" role="img">']; y = 6
    for lab, segs in rows:
        o.append(f'<text x="{L - 10}" y="{y + bh - 2}" class="tick" text-anchor="end">{esc(lab)}</text>')
        for name, v, slot in segs:
            o.append(f'<rect x="{L}" y="{y}" width="{max(1.5, sx(v) - L):.1f}" height="{bh}" rx="3" class="s{slot}f"><title>{esc(lab)}, {esc(name)}: {v}{unit}</title></rect><text x="{sx(v) + 6:.1f}" y="{y + bh - 3}" class="dl">{v}{unit} {esc(name)}</text>')
            y += bh + gap
        y += 12
    o.append('</svg>'); return '<div class="chartwrap">' + ''.join(o) + '</div>'

STY = [('quick', 'Quick (about 14 jobs a workday)', 1), ('steady', 'Steady (about 9)', 2), ('relaxed', 'Relaxed (about 10, more of them top-ups)', 3),
       ('half', 'Half pace (about 7)', 4), ('lazy', 'One job a day', 5), ('slacker', 'Misses Mon and Fri', 6)]
SHORT = {'quick': 'Quick', 'steady': 'Steady', 'relaxed': 'Relaxed', 'half': 'Half pace', 'lazy': 'One a day', 'slacker': 'Misses 2 shifts a week', 'skipper': 'Misses 1 in 3'}
def tier_series(p, upto=45): return [(x['d'], x['tier']) for x in C[p]['days'] if x['d'] <= upto]
def first_day(p, t):
    for x in C[p]['days']:
        if x['tier'] >= t: return x['d']
    return None
def jobs_per_wd(p, upto=30):
    ds = [x for x in C[p]['days'] if x['d'] <= upto and x['jobs'] > 0]; return round(sum(x['jobs'] for x in ds) / max(1, len(ds)), 1)

# chart 1: tier by day
ch_tier = chart([(SHORT[p], tier_series(p), s) for p, _, s in STY], 1, 45, 1, 4, [1, 8, 15, 22, 29, 36, 45], [1, 2, 3, 4], 'Tier', steps=True,
                refs=[('x', 22, 'Tier 4 test'), ('x', 26, "Calder's question")], jitter=.05, h=300, ytick_fmt=lambda v: f'T{int(v)}' if float(v).is_integer() else v)
# chart 2: Tier 3 reputation points, Days 16-22, against the 55 line
def xp_t3(p): return [(x['d'], x['xp']) for x in C[p]['days'] if 16 <= x['d'] <= 22 and x['tier'] == 3]
ch_t3 = chart([(SHORT[p], xp_t3(p), s) for p, s in (('quick', 1), ('steady', 2), ('relaxed', 3), ('half', 4))], 16, 22, 0, 80, [16, 17, 18, 19, 20, 21, 22],
              [0, 20, 40, 60, 80], 'Tier 3 points', refs=[('y', 55, '"Trusted": 55 points'), ('y', 45, 'what-if 45')])
# chart 3: the two reputations for the shift-misser
sl = C['slacker']['days']
ch_two = chart([('Ship-wide work word (0-100)', [(x['d'], x['srep']['work']) for x in sl if x['d'] <= 22], 2),
                ('Career tier x 25', [(x['d'], x['tier'] * 25) for x in sl if x['d'] <= 22], 1)], 1, 22, 0, 100, [1, 5, 8, 12, 15, 19, 22], [0, 25, 50, 75, 100], 'value',
               refs=[('y', 15, "Chief's talk under 15"), ('y', 5, 'the bottom: under 5')], steps=False)
# chart 4: hunger over two workdays, diligent with and without a lunch bite
def trace(style, need, d0=8, d1=10):
    p = N.P(); p.t = 0
    for d in range(d1): N.day(p, d, style, d % 7 < 5)
    return [((t - d0 * 1440) / 60, v[need]) for t, a, w, v in p.log if d0 * 1440 <= t <= d1 * 1440]
ch_hunger = chart([('Breakfast + dinner', trace('diligent', 'hunger'), 2), ('Plus a bite at noon', trace('diligent+lunch', 'hunger'), 1)], 0, 48, 0, 100,
                  [0, 6, 12, 18, 24, 30, 36, 42, 48], [0, 25, 50, 75, 100], 'Food', xlab='Hours from Tuesday 00:00', refs=[('y', 25, 'Hungry: tasks 15% slower')])
ch_fit = chart([('Gym every day', trace('diligent', 'fitness', 7, 13), 1), ('Gym every other day', trace('average', 'fitness', 7, 13), 2), ('Never', trace('socialiser', 'fitness', 7, 13), 6)],
               0, 144, 0, 100, [0, 24, 48, 72, 96, 120, 144], [0, 25, 50, 75, 100], 'Fitness', xlab='Hours from Monday of week 2', refs=[('y', 25, 'Out of shape: walk at 80%')])
# needs bars
NAMES = {'diligent': 'Diligent', 'diligent+lunch': 'Diligent + lunch bite', 'average': 'Average', 'socialiser': 'Socialiser', 'skipper': 'Skips breakfast', 'slacker': 'Slacker', 'grinder': 'Works, never plays'}
nb = bars([(NAMES[s], [('food', round(NEEDS[s]['red_share']['hunger']), 1), ('fitness', round(NEEDS[s]['red_share']['fitness']), 2), ('leisure', round(NEEDS[s]['red_share']['leisure']), 3)])
           for s in ('diligent', 'diligent+lunch', 'average', 'socialiser', 'skipper', 'grinder')], 100)
# meters
def meters(p, upto=16): return [(x['d'], round(sum(x['meters'].values()) / len(x['meters']), 1)) for x in C[p]['days'] if x['d'] <= upto and x['meters']]
ch_met = chart([(SHORT[p], meters(p), s) for p, s in (('quick', 1), ('steady', 2), ('half', 4), ('lazy', 5))], 1, 16, 60, 100, [1, 4, 7, 10, 13, 16], [60, 70, 80, 90, 100],
               'Average ship meter', refs=[('y', 90, 'the design: about 90 by Day 14')])
# credits
def cred(p, upto=30):
    s, out = 40, []
    for x in C[p]['days']:
        if x['d'] > upto: break
        s += 15 * x['jobs']; out.append((x['d'], s))
    return out
ch_cred = chart([(SHORT[p], cred(p), s) for p, s in (('quick', 1), ('steady', 2), ('half', 4), ('lazy', 5))], 1, 30, 0, 4500, [1, 8, 15, 22, 30], [0, 1000, 2000, 3000, 4000],
                'Credits earned', refs=[('y', 100, 'everything in the store once: under 100')])
# traditions per week
wk = {}
for r in TR: wk.setdefault((r['d'] - 1) // 7 + 1, []).append(r)
trad_rows = ''.join(f"<tr><td>{k}</td><td>{sum(r['all'] for r in v)}</td><td>{sum(r['eve'] for r in v)}</td><td>{sum(r['overlaps'] for r in v)}</td><td>{sum(r['attend'] for r in v)}</td></tr>" for k, v in wk.items())
wde = [r['eve'] for r in TR if r['work']]
career_rows = ''.join(f"<tr><td>{SHORT[p]}</td><td>{jobs_per_wd(p)}</td><td>{first_day(p, 2) or '-'}</td><td>{first_day(p, 3) or 'not by ' + str(C[p]['days'][-1]['d'])}</td><td>{first_day(p, 4) or 'not by ' + str(C[p]['days'][-1]['d'])}</td><td>{40 + 15 * sum(x['jobs'] for x in C[p]['days'] if x['d'] <= 30):,}</td></tr>"
                      for p in ('quick', 'steady', 'relaxed', 'half', 'lazy', 'slacker', 'skipper'))
sweep_rows = ''.join(f"<tr><td>{esc(k)}</td><td>{v['average']['fitness']}%</td><td>{v['average']['walkslow']}%</td><td>{v['diligent']['hunger']}%</td><td>{v['average']['hunger']}%</td><td>{v['average']['leisure']}%</td></tr>" for k, v in SWEEP.items())

ctx = dict(ch_tier=ch_tier, ch_t3=ch_t3, ch_two=ch_two, ch_hunger=ch_hunger, ch_fit=ch_fit, nb=nb, ch_met=ch_met, ch_cred=ch_cred, trad_rows=trad_rows, career_rows=career_rows,
           sweep_rows=sweep_rows, wde_lo=min(wde), wde_hi=max(wde), wde_avg=round(sum(wde) / len(wde), 1))
tpl = (HERE / 'report' / 'template.html').read_text()
for k, v in ctx.items(): tpl = tpl.replace('{{' + k + '}}', str(v))
(HERE / 'report' / 'balance-report.html').write_text(tpl)
print('written', len(tpl), 'bytes')
