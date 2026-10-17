# Makes plans/traditions-calendar.html (the Traditions calendar for check-in A) from content/traditions/*.trad and
# the twelve hand-written traditions. The traditions engineer's. Run: python3 plans/traditions-calendar-gen.py
import sys, re, json, html
import os; ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(ROOT, 'plans')); import trad_parse as tp
G = open(os.path.join(ROOT, 'starship-cadet.html')).read()
NAMES = {m.group(1): m.group(2) for m in re.finditer(r'\{"id": "([a-z-]+)", "name": "([^"]+)"', G)}
WD = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
hm = lambda m: f'{m//60:02d}:{m%60:02d}'
esc = html.escape
trads = tp.read_all(os.path.join(ROOT, 'content', 'traditions'))
SEAT = {}
for f, seat in [('weekly',('tiles-night','tasting-table','garden-hour','late-piano','long-breakfast','sunday-table','letters')),
                ('monthly',('talent-night','department-cup','crossover-supper','mending-day','rummage-day','open-lab','bridge-hour','book-circle')),
                ('seasons',('sowing','first-fruits','harvest-supper','lantern-walk','midtour','years-end','new-hands-tea','one-week-aboard','four-weeks-aboard'))]:
    for i in seat: SEAT[i] = f
DECKN = {1:'Bridge',2:'Command',3:'Commons',4:'Quarters',5:'Operations',6:'Engineering'}
def place(w):
    w = w['where'][0]
    r = w.get('room'); r = r.strip('^$').replace('\\','') if r else {'garden':'the garden','garden-tend':'the garden beds','gym':'the gym','music':'the music room','common-room':'the junior common room'}.get(w.get('pool'), w.get('pool'))
    return f"{r}, Deck {w['deck']}"
def when(w):
    if 'weekday' in w and 'every' not in w and 'after' not in w: return 'Every ' + ' and '.join(['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'][x] for x in (w['weekday'] if isinstance(w['weekday'], list) else [w['weekday']]))
    if w.get('every') == '2weeks': return f"Every other {['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'][w['weekday']]}" + (f" from day {w['from']}" if w.get('from') else '')
    if w.get('every') == '4weeks': return f"Every 4 weeks, {['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'][w['weekday']]} of week {w.get('week',1)}"
    if w.get('every') == 'quarter':
        s = f"week {w['week']} {['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'][w['weekday']]}" if 'week' in w else f"day {w['quarterDay']}"
        return (f"{w['season'].title()}, " if w.get('season') else 'Each season, ') + s
    if w.get('every') == 'year': return f"Once a year, day {w['dayOfYear']}" if 'dayOfYear' in w else f"Once a year, week {w['week']}"
    if w.get('after'): return f"{w['days']} days after you arrive" if 'days' in w else f"Your {['first','second','third','fourth','fifth'][w.get('nth',1)-1]} Friday aboard" if w['weekday']==4 else 'after you arrive'
    return str(w)
def day_of(w):
    # first day in a year it falls on (1..364), worked out like the game
    for d in range(0, 365):
        wd = (d-1) % 7; yd = (d-1) % 364 + 1
        if w.get('after'):
            if 'days' in w: return w['days']
            k = 1 + (w['weekday'] - 0) % 7  # first weekday after day 0 (day 0 is Sunday)
            return w['weekday'] + 1 + 7*(w.get('nth',1)-1)
        if w.get('every') == 'quarter':
            if d>=1 and w.get('season') in (None, ['sowing','greening','harvest','lanterns'][(yd-1)//91]) and wd == w['weekday'] and ((yd-1)%91)//7+1 == w['week']: return d
        if w.get('every') == 'year' and d>=1 and yd == w.get('dayOfYear'): return d
    return None
OLD = [  # the twelve hand-written in section 18
 ('Running club', 0, 1155, 1200, 'the gym, Deck 3', 'Rina Deshi'), ('Quiz night', 3, 1200, 1290, 'the bow lounge, Deck 3', 'Tomas Lind'),
 ('Works Friday tea', 4, 1125, 1170, 'the tea corner, Deck 5', 'Chief Ines Calder'), ('Music jam', 4, 1185, 1275, 'the music room, Deck 4', ''),
 ('Film night', 5, 1200, 1320, 'the junior common room, Deck 4', 'Pell Okafor'), ('Observatory night', 5, 1275, 1355, 'the observatory, Deck 2', 'Dr. Imra Sato'),
 ('Sunday swap meet', 6, 630, 750, 'the promenade, Deck 3', '')]
weekly = [t for t in trads if 'weekday' in t['when'] and 'every' not in t['when'] and 'after' not in t['when']]
cyc = [t for t in trads if t['when'].get('every') in ('2weeks','4weeks')]
seas = [t for t in trads if t['when'].get('every') in ('quarter','year')]
life = [t for t in trads if t['when'].get('after')]
def line(t, k):
    l = (t.get('text') or {}).get(k) or []
    if not l: return ''
    d = day_of(t['when']) or 1
    host = NAMES.get(t.get('host',''), '')
    return (l[0]['t'].replace('{time}', hm(t['at'][0])).replace('{trad}', t['name']).replace('{host}', host.split(' ')[-2] if host else 'the host')
            .replace('{season}', ['Sowing','Greening','Harvest','Lanterns'][((d-1)%364)//91]).replace('{weekday}', ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'][(d-1)%7]))
def card(t, new=True):
    host = NAMES.get(t.get('host',''), '')
    needs = []
    ti = t.get('ties') or {}
    if t.get('meal'): needs.append(f"the {t['meal']} itself (sim)")
    if 'galley' in ti: needs.append('the galley')
    if 'decor' in ti: needs.append(f"props: {ti['decor']}")
    if 'tally' in ti: needs.append('a vote (tally)')
    if t.get('trace'): needs.append(f"a keepsake: {t['trace']}")
    if t.get('flag'): needs.append('a story beat first (flag ' + t['flag'] + ')')
    return (f'<div class="card"><b>{esc(t["name"])}</b><div class="when">{esc(when(t["when"]))}, {hm(t["at"][0])}-{hm(t["at"][1])}</div>'
            f'<div class="where">{esc(place(t))}{" · host " + esc(host) if host else ""}</div>'
            f'<p class="q">“{esc(line(t,"mail") or line(t,"ask"))}”</p>'
            + (f'<div class="needs">Needs: {esc(", ".join(needs))}</div>' if needs else '') + f'<div class="tag">{SEAT.get(t["id"],"")}</div></div>')
# the week grid
rows = {i: [] for i in range(7)}
for n, wd, a, b, where, host in OLD: rows[wd].append((a, f'<li class="old"><span>{hm(a)}</span> {esc(n)} <i>{esc(where)}</i></li>'))
for t in weekly:
  for wdx in (t['when']['weekday'] if isinstance(t['when']['weekday'], list) else [t['when']['weekday']]): rows[wdx].append((t['at'][0], f'<li class="new"><span>{hm(t["at"][0])}</span> {esc(t["name"])} <i>{esc(place(t))}</i></li>'))
week = ''.join(f'<div class="day"><h3>{WD[i]}</h3><ul>{"".join(x for _, x in sorted(rows[i]))}</ul></div>' for i in range(7))
# the 4-week cycle
cycrows = ''
for wk in range(1,5):
    cells = []
    for i in range(7):
        it = [t for t in cyc if t['when']['weekday'] == i and (t['when'].get('week',1) == wk if t['when']['every']=='4weeks' else (wk-1) % 2 + 1 == t['when'].get('week',1))]
        it_txt = '<span class="old">Hull-lights 21:00</span><br>' if wk == 4 and i == 2 else '<span class="old">Harvest morning 09:30</span><br>' if wk in (1, 3) and i == 5 else ''
        cells.append('<td>' + it_txt + '<br>'.join(f'{esc(t["name"])} {hm(t["at"][0])}' for t in it) + '</td>')
    cycrows += f'<tr><th>Week {wk}</th>{"".join(cells)}</tr>'
# the year
yr = sorted([(day_of(t['when']), t) for t in seas], key=lambda x: x[0] or 999)
old_year = [(100, 'Founding Day', 'cake and a few words from the Captain'), (300, 'The quiet watch', 'a quiet while at the windows')]
marks = ''.join(f'<div class="mk" style="left:{(d-1)/364*100:.2f}%" title="{esc(t["name"])}"><span>{esc(t["name"])}</span><em>day {d}</em></div>' for d, t in yr if d) + ''.join(f'<div class="mk old" style="left:{(d-1)/364*100:.2f}%"><span>{esc(n)}</span><em>day {d}</em></div>' for d, n, _ in old_year)
SEAS = lambda d: ['Sowing','Greening','Harvest','Lanterns'][((d-1)%364)//91]
allyr = sorted([(d, t['name'], True) for d, t in yr if d] + [(d, n, False) for d, n, _ in old_year])
yrows = ''.join(f'<tr><td>{d}</td><td>{SEAS(d)}</td><td class="{"" if new else "old"}">{esc(n)}{"" if new else " (already aboard)"}</td></tr>' for d, n, new in allyr)
lifec = ''.join(card(t) for t in sorted(life, key=lambda t: day_of(t['when']) or 0))
page = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Traditions Calendar</title>
<style>
:root{{--bg:#121a27;--ink:#e8eef0;--muted:#93a6ae;--teal:#4cc3b5;--gold:#e9c46a;--glass:rgba(13,21,33,.78);--line:rgba(150,200,196,.22);--card:rgba(255,255,255,.025);--new:#bdeee6;--old:#93a6ae}}
@media (prefers-color-scheme: light){{:root:not([data-theme="dark"]){{--bg:#f4f1ea;--ink:#1d2830;--muted:#5f6d73;--teal:#1f8f82;--gold:#a87b10;--glass:rgba(255,255,255,.85);--line:rgba(30,80,80,.18);--card:rgba(0,0,0,.02);--new:#0f6b61;--old:#6b787d}}}}
*{{box-sizing:border-box}} html,body{{margin:0;background:var(--bg);color:var(--ink);font-family:"Avenir Next","Segoe UI",system-ui,sans-serif;line-height:1.5}}
header,main{{max-width:1100px;margin:0 auto;padding:16px}} h1{{font-size:21px;margin:0}} h2{{font-size:17px;margin:0 0 8px;color:var(--new)}} h3{{font-size:14px;margin:0 0 4px}}
.sub,.note{{color:var(--muted);font-size:13.5px}} section{{background:var(--glass);border:1px solid var(--line);border-radius:14px;padding:14px 16px;margin:14px 0}}
.week{{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:8px}} @media (max-width:760px){{.week{{grid-template-columns:1fr 1fr}}}}
.day{{border:1px solid var(--line);border-radius:10px;padding:8px;background:var(--card)}} .day ul{{list-style:none;margin:0;padding:0;font-size:13px}} .day li{{margin:5px 0}}
.day li span{{display:block;font-variant-numeric:tabular-nums;color:var(--muted);font-size:12px}} .day li i{{display:block;font-style:normal;color:var(--muted);font-size:11.5px}}
li.new{{color:var(--new);font-weight:600}} li.old{{color:var(--ink)}} .key b{{color:var(--new)}}
table{{width:100%;border-collapse:collapse;font-size:13px}} .tw{{overflow-x:auto}} th,td{{border:1px solid var(--line);padding:6px;vertical-align:top;text-align:left}} th{{color:var(--muted);font-weight:600}} td .old,.mk.old span{{color:var(--old)}}
.year{{position:relative;height:26px;margin:10px 4px 6px;border-top:2px solid var(--line);overflow:hidden}} .seasons{{display:flex;font-size:12px;color:var(--muted)}} .seasons div{{flex:1;border-left:1px solid var(--line);padding:2px 6px}}
.mk{{position:absolute;top:0;width:0;border-left:2px solid var(--teal);height:22px}} .mk span{{display:none}} .mk em{{display:none}} .mk.old{{border-color:var(--old)}}
.grid{{display:grid;gap:10px;grid-template-columns:repeat(auto-fill,minmax(250px,1fr))}} .card{{border:1px solid var(--line);border-radius:12px;padding:10px 12px;background:var(--card);font-size:13px}}
.card b{{display:block;color:var(--new);font-size:14px}} .when,.where,.needs{{color:var(--muted);font-size:12.5px}} .q{{margin:6px 0;font-size:13px}} .tag{{font-size:11px;color:var(--gold);text-transform:uppercase;letter-spacing:.05em;margin-top:4px}}
ol{{font-size:14px}} li{{margin:4px 0}}
</style></head><body>
<header><h1>Traditions calendar</h1><div class="sub">Pillar 4, check-in A: the ship's traditions as the three designers drafted them, for you to keep, cut or add to. {len(trads)} new ones plus the twelve already aboard. Built from the files in <code>content/traditions/</code> (claude/ship-events).</div></header>
<main>
<section><h2>Your choices</h2><ol>
<li><b>Keep, cut or add.</b> Everything below is in the game already (it runs on paper and passes the checks); anything you cut simply goes.</li>
<li><b>Garden hour</b> clashes with the Monday evening set (book circle, talent night, department cup), so it rarely happens. The weekly designer is moving it, probably to Saturday afternoon.</li>
<li><b>Shared meals</b> (Sunday long table, the tasting table, the crossover supper, the suppers, long breakfast) work, but few people sit down yet. The sim engineer is making going count as that person's dinner or breakfast.</li>
<li><b>Not yet built:</b> the props most traditions ask for (only Tiles boards, the tasting chalkboard, the lanterns and your seedling exist), the votes (tasting, department cup, harvest best) and the Sunday "This week aboard" Mail. The farewell supper and crew welcome tea wait for crew coming and going.</li>
</ol><p class="note">The rule that keeps the ship from getting noisy: at most two traditions an evening and never two at once on the same deck; when they meet, the rarer one wins (so a monthly beats a weekly, a yearly beats both). Birthdays never move.</p></section>
<section><h2>A normal week</h2><div class="sub key"><b>Bold teal</b>: new in Pillar 4. Plain: already aboard. Birthdays (20:15, the mess) come on top, about once a week.</div><div class="week">{week}</div></section>
<section><h2>Every few weeks</h2><div class="sub">A four-week cycle counted from Day 1 (week 1 is days 1-7).</div><div class="tw"><table><tr><th></th>{"".join(f"<th>{d}</th>" for d in WD)}</tr>{cycrows}</table></div>
<div class="grid" style="margin-top:10px">{"".join(card(t) for t in cyc)}</div></section>
<section><h2>The ship's year</h2><div class="sub">364 days in four seasons named for the garden. You arrive on day 0, the last evening of Lanterns.</div>
<div class="seasons"><div>Sowing (1-91)</div><div>Greening (92-182)</div><div>Harvest (183-273)</div><div>Lanterns (274-364)</div></div><div class="year">{marks}</div><div class="tw"><table><tr><th>Day</th><th>Season</th><th>Tradition</th></tr>{yrows}</table></div>
<div class="grid">{"".join(card(t) for _, t in yr)}</div></section>
<section><h2>Your first weeks</h2><div class="sub">Counted from your arrival (day 0, a Sunday evening).</div><div class="grid">{lifec}</div></section>
<section><h2>Each week's new traditions</h2><div class="grid">{"".join(card(t) for t in weekly)}</div></section>
</main></body></html>'''
open(os.path.join(ROOT, 'plans', 'traditions-calendar.html'), 'w').write(page)
print(len(page), 'bytes', len(trads))
