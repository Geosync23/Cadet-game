import sys, os, json, types
src = open('cadet_test.py').read(); src = src[:src.index('import sys, json, hashlib')]
ct = types.ModuleType('ct'); exec(src, ct.__dict__)
from playwright.sync_api import sync_playwright
WRAP = r"""(() => { window.__L = []; const f0 = SND.fx; SND.fx = (name, o = {}) => { const r = f0(name, o); __L.push({ name, x: o.x == null ? null : +o.x.toFixed(2), z: o.z == null ? null : +o.z.toFixed(2), crew: !!o.crew, played: r, t: shipNow(), deck: deckDef.num }); return r; }; return 1; })()"""
with sync_playwright() as pw:
    g = ct.Game(pw, sys.argv[1]); url = g.page.url.split('?')[0]
    g.page.goto(url + '?nosave&debug&sound&soundlog'); g.page.wait_for_function('window.__sc !== undefined', timeout=60000); g.ev(ct.SKIP_SWITCH); g.step(30)
    g.page.mouse.click(200, 400); g.page.wait_for_function("window.__sc('SND._.state()') === 'running'", timeout=10000)
    print('ctx', g.ev("SND._.state()"), 'webdriver', g.ev('navigator.webdriver'))
    g.ev(WRAP)
    # 1. a busy deck at a busy time: Deck 3 at 12:20, real frames (crew walking through doors)
    g.ev("skipTo(2 * 1440 + 740)"); g.ev("goToDeck(3)"); g.step(5); g.page.wait_for_timeout(300); g.ev("__L.length = 0")
    for k in range(40): g.step(30)   # 1200 frames = 40 s game time
    L = g.ev("__L")
    doors = [e for e in L if e['name'].startswith(('door', 'hatch'))]
    print('busy deck 3: door events', len(doors), 'played', sum(e['played'] for e in doors), 'crew', sum(e['crew'] for e in doors), 'mine', sum(not e['crew'] for e in doors))
    seq = {}
    bad = []
    for e in doors:
        k = (e['x'], e['z']); last = seq.get(k)
        kind = 'open' if 'Open' in e['name'] else 'close'
        if last == kind: bad.append((k, kind))
        seq[k] = kind
    print('  same door twice in a row (open-open or close-close):', bad[:6], len(bad))
    print('  other names:', sorted(set(e['name'] for e in L if not e['name'].startswith(('door', 'hatch')))))
    # 2. deck change: no burst
    g.ev("__L.length = 0; goToDeck(4)"); g.step(3); print('deck change burst:', [e['name'] for e in g.ev('__L')])
    # 3. real lift ride from the lobby
    g.ev("__L.length = 0; (() => { const b = ROOM_BOX['@']; if (b) player.obj.position.copy(cellPos(b.i0 + 1, b.j0 + 1)); })(); startRide(3)")
    for k in range(10): g.step(10)
    print('lift ride:', [e['name'] for e in g.ev('__L') if not e['name'].startswith('step')])
    # 4. heads-up and mail over a stretch of play (to 14:30 on Day 2, then 200 frames)
    g.ev("__L.length = 0"); 
    for k in range(20): g.step(30)
    L = g.ev('__L'); print('heads', sum(e['name'] == 'heads' for e in L), 'mail', sum(e['name'] == 'mail' for e in L), 'hu now', g.ev("JSON.stringify(DEV.hu && DEV.hu.title)"))
    # 5. pause and resume with a door changing while paused
    g.ev("pauseSet(true)"); g.step(5); g.page.wait_for_timeout(300); g.step(2); print('paused state', g.ev("SND._.state()"))
    g.ev("pauseSet(false)"); g.step(5); g.page.wait_for_timeout(300); g.step(2); print('resumed state', g.ev("SND._.state()"))
    # 6. Sound Off in Settings: suspended, nothing plays; the key not written under nosave
    g.ev("SND.settingsAct('sound', false)"); g.step(5); g.page.wait_for_timeout(300); g.step(2)
    print('sound off state', g.ev("SND._.state()"), 'fx returns', g.ev("SND.fx('tap')"), 'key', g.ev("localStorage.getItem('starship-cadet-sound')"))
    print('errors', g.errors[:5])
    g.close()
