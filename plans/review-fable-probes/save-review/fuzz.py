import sys, time, json, random, copy
from h import *
W = int(sys.argv[1]); PORT = 8740 + W; DUR = float(sys.argv[2]); NM = int(sys.argv[3]) if len(sys.argv) > 3 else 6
base = json.loads(open(S / ('save_d35.json' if W % 2 else 'save_d10.json')).read())
rnd = random.Random(1000 + W)
JUNK = [None, 'x', {}, [], -1, 1e9, 0.5, True, 'NaN', [None], {'a': None}]
def paths(o, p=()):
    out = []
    if isinstance(o, dict):
        for k, v in o.items(): out.append(p + (k,)); out += paths(v, p + (k,))
    elif isinstance(o, list):
        for i in ([0, len(o) - 1] if len(o) > 1 else range(len(o))): out.append(p + (i,)); out += paths(o[i], p + (i,))
    return out
PROT = {('v',), ('time',), ('time', 'day'), ('time', 'min'), ('player',), ('player', 'deck'), ('player', 'tile'), ('player', 'tile', 0), ('player', 'tile', 1), ('player', 'facing')}
ALL = [p for p in paths(base) if p not in PROT]
def mutate(s, p, j):
    o = s
    for k in p[:-1]:
        try: o = o[k]
        except Exception: return False
    try:
        if j == 'DEL':
            if isinstance(o, dict): o.pop(p[-1], None)
            else: return False
        else: o[p[-1]] = j
    except Exception: return False
    return True
CHECK = """(() => { const out = { ex: [], wrote: false };
  for (const f of SAVE_EXTRA) { try { f({ player: {}, ship: {}, flags: {} }); } catch (e) { out.ex.push(String(e).slice(0, 160) + ' :: ' + f.toString().slice(0, 120)); } }
  localStorage.removeItem(SAVE_KEY); saveGame(); out.wrote = localStorage.getItem(SAVE_KEY) !== null; out.day = SHIP.time.day; return out; })()"""
def trial(g, muts):
    s = copy.deepcopy(base)
    for p, j in muts: mutate(s, p, j)
    g.page.evaluate('t => { localStorage.clear(); localStorage.setItem("starship-cadet-arrived", "1"); localStorage.setItem("starship-cadet-save", t); }', json.dumps(s))
    ok = g.load(); res = {'started': ok, 'errs': []}
    if ok:
        try:
            res['loaded'] = g.ev('!!SAVED')
            g.step(90); res['pending'] = g.page.evaluate('__pending()')
            try: g.ev('skipTo(shipNow() + 1500)')
            except Exception as e: res['errs'].append('SKIP: ' + str(e)[:300])
            g.step(60); res['pending2'] = g.page.evaluate('__pending()')
            res['save'] = g.ev(CHECK)
        except Exception as e: res['errs'].append('HARNESS: ' + str(e)[:300])
    try: res['errs'] += g.errs()
    except Exception: pass
    res['bad'] = (not ok) or bool(res['errs']) or not res.get('pending2') or not res.get('save', {}).get('wrote') or bool(res.get('save', {}).get('ex'))
    return res
build() if W == 0 else time.sleep(3); serve(PORT)
out = open(S / f'fuzz_{W}.jsonl', 'a'); t0 = time.time(); n = 0
with sync_playwright() as pw:
    g = G(pw, PORT); g.load()
    def rec(muts, r): out.write(json.dumps({'muts': [[list(p), j] for p, j in muts], **r}) + '\n'); out.flush()
    if W == 0: rec([], trial(g, []))
    while time.time() - t0 < DUR:
        muts = [(rnd.choice(ALL), rnd.choice(JUNK + ['DEL'])) for _ in range(NM)]
        r = trial(g, muts); n += 1
        if r['bad'] and len(muts) > 1:
            cur = muts
            while len(cur) > 1 and time.time() - t0 < DUR + 240:
                a, b = cur[:len(cur) // 2], cur[len(cur) // 2:]
                ra = trial(g, a)
                if ra['bad']: cur, r = a, ra
                else:
                    rb = trial(g, b)
                    if rb['bad']: cur, r = b, rb
                    else: break
            rec(cur, {**r, 'of': len(muts)})
        else: rec(muts, r)
print('done', W, n)
