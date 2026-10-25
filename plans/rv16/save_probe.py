# RV16: save and reload mid-story on a switch-on copy. Play days 1..SPLIT (stories_check's "play" loop), save, reload
# (a real page reload with saving on), compare the story state, then play SPLIT+1..30 and apply stories_check's rules
# to the second half's log plus the told/skip state.
import sys, os, json, types, pathlib, re
os.environ.setdefault('CADET_CHROME', '/opt/pw-browsers/chromium')
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'cadet_test.py')).read(); src = src[:src.index('import sys, json, hashlib')]
ct = types.ModuleType('ct'); exec(src, ct.__dict__)
sc = open(os.path.join(HERE, 'stories_check.py')).read()
RUN = re.search(r'RUN = r"""(.*?)"""', sc, re.S).group(1)
RUN = RUN.replace('([DAYS, MODE]) =>', '([D0, DAYS, MODE]) =>').replace('for (let d = 1; d <= DAYS; d++)', 'for (let d = D0; d <= DAYS; d++)')
ns = {'json': json}; exec(sc[sc.index('def rules'):sc.index('def selftest')], ns); rules = ns['rules']
BUILD, SPLIT, DAYS = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 30
SNAP = "JSON.stringify({ cs: SHIP.social.stories && SHIP.social.stories.cs, m: SHIP.social.stories && SHIP.social.stories.m, arcs: Object.fromEntries(['pell','teague-theo','bramwell-basil','halloran-emeka','kovac-zainab','salo-saad'].map(id => [id, SHIP.rel[id] ? [SHIP.rel[id].arc || 0, SHIP.rel[id].tier] : null])), flags: Object.keys(SHIP.flags || {}).filter(k => /pell|kovac|bramwell|halloran|salo|teague/.test(k)).sort(), favs: (typeof myFavours === 'function' ? myFavours() : []).map(j => j.id + ':' + j.status) })"
with sync_playwright() as pw:
    g = ct.Game(pw, BUILD); url = g.page.url.split('?')[0]
    def load():
        g.page.goto(url + '?debug'); g.page.wait_for_function('window.__sc !== undefined', timeout=60000); g.ev(ct.SKIP_SWITCH)
    load(); g.ev("localStorage.clear(); localStorage.setItem(INTRO_KEY, '1')"); load(); g.step(3)
    print('saving on:', g.ev('!NOSAVE'), 'STORIES_ON', g.ev('STORIES_ON'))
    r1 = g.page.evaluate('([s, a]) => window.__sc("(" + s + ")(" + JSON.stringify(a) + ")")', [RUN, [1, SPLIT, 'play']])
    g.ev(f'setShipNow({SPLIT} * 1440 + 360)')
    before = json.loads(g.ev(SNAP)); print('before save, bookings:', before['cs'] and before['cs']['book'])
    print('before save time', g.ev('JSON.stringify(SHIP.time)'), 'intro', g.ev('JSON.stringify(SHIP.intro)')[:200])
    g.ev('introEnd(true)'); before = json.loads(g.ev(SNAP))
    g.ev('saveGame()'); size = g.ev('localStorage.getItem(SAVE_KEY).length'); print('save size', size)
    raw = json.loads(g.ev('localStorage.getItem(SAVE_KEY)')); print('saved keys', list(raw.keys())[:30]); soc = raw.get('social') or {}; print('saved social keys', list(soc.keys())[:30] if isinstance(soc, dict) else type(soc)); print('social hour', soc.get('hour'), 'aff type', type(soc.get('aff')).__name__, 'ids', str(soc.get('ids'))[:40]); print('saved stories', json.dumps(soc.get('stories') if isinstance(soc, dict) else None)[:300])
    load(); print('right after load', g.ev('JSON.stringify(SHIP.time)'), 'intro', g.ev('JSON.stringify(SHIP.intro)')[:200]); g.step(3)
    print('saved time', raw['time'], raw['player']); print('reloaded: SAVED', g.ev('JSON.stringify(SAVED && SAVED.time)'), 'loadGame', g.ev('JSON.stringify(loadGame() && loadGame().time)'), 'intro key', g.ev('localStorage.getItem(INTRO_KEY)'), g.ev('INTRO_KEY'), 'stored time', g.ev('JSON.stringify(JSON.parse(localStorage.getItem(SAVE_KEY) || "null") && JSON.parse(localStorage.getItem(SAVE_KEY)).time)'))
    print('after reload day', g.ev('SHIP.time.day'), 'stories', g.ev('JSON.stringify(SHIP.social.stories)')[:300])
    after = json.loads(g.ev(SNAP))
    same = before == after; print('state after reload identical:', same)
    if not same:
        for k in set(before) | set(after):
            if before.get(k) != after.get(k): print('  DIFF', k, json.dumps(before.get(k))[:300], '\n   ->', json.dumps(after.get(k))[:300])
    r2 = g.page.evaluate('([s, a]) => window.__sc("(" + s + ")(" + JSON.stringify(a) + ")")', [RUN, [SPLIT + 1, DAYS, 'play']])
    errs = g.errors[:5]; g.close()
for half, r in (('1st', r1), ('2nd', r2)):
    for id in r['ids']: print(f'  {half} {id}: told {sorted(r["told"].get(id, []))} skipped {sorted(r["skip"].get(id, []))} log ' + ' '.join(f'{x["beat"]}@{x["day"]}' for x in r['log'] if x['id'] == id))
    print('  bookings:', ', '.join(f'{k} day {v["day"]} {v["from"] % 1440 // 60:02d}:{v["from"] % 60:02d}' for k, v in r['books'].items()))
bad = rules(r2, 'play') + ['page error: ' + e for e in errs]
for b in bad: print('  FAIL', b)
print('SAVE PROBE OK' if same and not bad else 'SAVE PROBE FAILED')
