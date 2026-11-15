import sys, time, json, copy
from h import *
serve(8780)
b35 = json.loads(open(S / 'save_d35.json').read()); b10 = json.loads(open(S / 'save_d10.json').read())
print('d35 ship.end:', json.dumps(b35['ship'].get('end'))[:300], 'time', b35['time'])
with sync_playwright() as pw:
    g = G(pw, 8780, pre="window.addEventListener('error', e => window.__errs.push('STACK: ' + (e.error && e.error.stack || '').slice(0, 700)));"); g.load()
    def run(name, s):
        g.page.evaluate('t => { localStorage.clear(); localStorage.setItem("starship-cadet-arrived", "1"); localStorage.setItem("starship-cadet-save", t); }', json.dumps(s))
        ok = g.load(); r = {'started': ok}
        if ok: g.step(60); r['day'] = g.ev('SHIP.time.day')
        r['errs'] = g.errs()[:4]; print('\n##', name, json.dumps(r)[:1800], flush=True)
    for d in (400, 60, 36):
        s = copy.deepcopy(b10); s['time']['day'] = d; run(f'day-10 save with time.day = {d}', s)
    s = copy.deepcopy(b35); s['ship'].pop('end', None); run('day-35 save without ship.end', s)
    s = copy.deepcopy(b35); s['ship'].pop('end', None); s['ship'].pop('works', None); run('day-35 save without ship.end and ship.works', s)
    s = {'v': 2, 'time': {'day': 35, 'min': 600}, 'player': {k: b10['player'][k] for k in ('deck', 'tile', 'facing')}}; run('bare day-35 save', s)
