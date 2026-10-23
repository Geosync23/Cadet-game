# RV10 probe: FX5 call-home booth arrow (Day 0 Track it, and the Tracked row), real taps at phone sizes
import sys, os, re, pathlib, json
GAME, CT, OUT = sys.argv[1], sys.argv[2], pathlib.Path(sys.argv[3]); OUT.mkdir(parents=True, exist_ok=True)
exec(open(CT + '/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
TMP = WORK / 'test' / ('_rv10_' + pathlib.Path(GAME).name); TMP.write_text(instrument(pathlib.Path(GAME).read_text()))
G = "(typeof IX_GOAL !== 'undefined' && IX_GOAL ? { label: IX_GOAL.label, place: IX_GOAL.place || null, trk: IX_GOAL.trk || null } : null)"
def run(pw, W, H):
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': W, 'height': H}, device_scale_factor=1, has_touch=True, is_mobile=True)
    pg = ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
    pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    pg.add_init_script(INIT)
    ev = lambda s: pg.evaluate('s => window.__sc(s)', s)
    def step(n):
        pg.evaluate('s => { if (window.__skip === undefined && window.__sc) window.__sc(s); }', SKIP_SWITCH)
        if n > 1: pg.evaluate(f'window.__skip = true; window.__step({n - 1}, 33); window.__skip = false')
        pg.evaluate('window.__step(1, 33)')
    pg.goto('file://' + str(TMP)); pg.wait_for_function('window.__sc !== undefined', timeout=120000)
    pg.add_style_tag(content='*,*::before,*::after{transition:none!important;animation:none!important}')
    step(10); ev('localStorage.clear()'); ev('newGameStart(true)'); step(5)
    pg.fill('form input[maxlength="24"]', 'Sam'); pg.locator('form button').first.tap(); step(5)
    ev("skipTo(introAbs(0, INTRO_START.min + 70))"); ev("(() => { goToDeck(3); player.obj.position.copy(cellPos(28, 2)); })()"); step(5)
    ev("(() => { if (DIALOGUE) dialogueEnd(); INTRO_UI.chiefD = null; SHIP.intro.done['chief:met'] = SHIP.intro.done['chief:end'] = Math.floor(shipNow()); SHIP.player.tray = 'Stew'; delete SHIP.intro.done['ate:last']; clearGoal(); })()"); step(20)
    card = ''
    for i in range(12):
        step(15); card = ev("(() => { const c = document.getElementById('devDlg'); return c && !c.hidden ? c.textContent : ''; })()")
        if 'Call home' in card: break
    tapped = False
    if 'Call home' in card:
        print('  card buttons:', pg.locator('#devDlg button').all_text_contents()); btn = pg.locator('#devDlg button', has_text=re.compile('track', re.I)).first; txt = btn.text_content(); btn.tap(); tapped = txt; step(20)
    print(f'{W}x{H} card up {"Call home" in card}, tapped {tapped!r}: arrow', ev(G))
    def into_room_and_call(tag):
        ev("(() => { actEnd(true); player.path.length = 0; player.obj.position.copy(cellPos(37, 18)); })()"); step(30)   # just inside the booths' room
        r1 = ev("({ g: " + G + ", room: roomAt(...player.here()), end: SHIP.intro.done['call:end'] !== undefined })")
        # walk in further by a real floor tap towards the booths
        pin = ev("(() => { const e = document.getElementById('ixGoal'); if (!e || e.hidden) return null; const m = /translate\\(([-\\d.]+)px, ?([-\\d.]+)px/.exec(e.style.transform); const pinShown = getComputedStyle(e.children[1]).display !== 'none'; return m ? [+m[1], +m[2], pinShown] : null; })()")
        pg.screenshot(path=str(OUT / f'{W}x{H}-{tag}-inroom.png'), timeout=120000)
        print(f'{W}x{H} {tag} in the room:', r1, 'pin', pin)
        mid = None
        for attempt in range(3):
            pin = ev("(() => { const e = document.getElementById('ixGoal'); if (!e || e.hidden) return null; const m = /translate\\(([-\\d.]+)px, ?([-\\d.]+)px/.exec(e.style.transform); return m && getComputedStyle(e.children[1]).display !== 'none' ? [+m[1], +m[2]] : null; })()")
            if attempt == 2:   # the booth itself on screen, not the pin
                pin = ev("(() => { const it = ITEMS.find(i => i.t === 'Booth ' + ((IX_GOAL && IX_GOAL.place) || '1').slice(-1)); const p = new THREE.Vector3(); it.hit.getWorldPosition(p); const v = p.project(camera); return [(v.x + 1) * innerWidth / 2, (1 - v.y) * innerHeight / 2 + 8]; })()"); print('    tapping the booth itself at', [round(v) for v in pin])
            if pin: pg.touchscreen.tap(pin[0], pin[1] - 8)
            else: print('  pin not on screen: tapping the booth item instead'); ev("(() => { const it = ITEMS.find(i => i.t === 'Booth ' + ((IX_GOAL && IX_GOAL.place) || '1').slice(-1)); it.hit.getWorldPosition(_wp); playerTap(it, _wp.clone(), _wp.clone()); })()")
            for i in range(40):
                step(10)
                if ev("!!ACT && ACT.kind === 'call' && ACT.phase === 'walk'") and mid is None: mid = ev(G)
                if ev("!!ACT && ACT.kind === 'call' && ACT.phase !== 'walk'"): break
            if ev("!!ACT && ACT.kind === 'call'"): break
            who = ev("(() => { const s = placeSpot(IX_GOAL && IX_GOAL.place || '3-callhome-2'); return DECK_CREW.filter(a => Math.hypot(a.x - s.x, a.z - s.z) < 1.6).map(a => [a.p.id, a.goalId, +Math.hypot(a.x - s.x, a.z - s.z).toFixed(2), a.settled, a.pose]); })()")
            card = ev("(() => { const c = [...document.querySelectorAll('.devdlg, #devDlg, .crewcard, #card')].find(e => !e.hidden && e.textContent); return c ? c.textContent.slice(0, 60) : null; })()")
            print('    near the booth:', who, '| card:', card)
            x = pg.locator('button.x:visible'); print(f'  attempt {attempt + 1}: no call (a crew card took the tap: {x.count()} close buttons); arrow now', ev(G))
            if x.count(): x.first.tap(); step(5)
        step(20)
        r2 = ev("({ g: " + G + ", act: ACT && ACT.kind, phase: ACT && ACT.phase, end: SHIP.intro.done['call:end'] !== undefined })")
        pg.screenshot(path=str(OUT / f'{W}x{H}-{tag}-call.png'), timeout=120000)
        print(f'{W}x{H} {tag} while walking to the booth: {mid}; call begun: {r2}')
        ev("actEnd(true)"); step(10)
        if ev("typeof homeClose === 'function'"): ev("homeClose()")
    into_room_and_call('day0')
    # the Tracked list's "The call booths" row, Day 1 evening
    ev("(() => { SHIP.intro.done['call:end'] = SHIP.intro.done['call:end'] || 1; skipTo(introAbs(1, 19 * 60)); goToDeck(3); player.obj.position.copy(cellPos(28, 2)); clearGoal(); })()"); step(20)
    ok = ev("(() => { const r = TRK_PLACES.find(x => x.key === 'place:calls'); if (!r) return 'no row'; return typeof trkTap === 'function' ? 'trkTap' : Object.keys(r).join(','); })()")
    print('  tracked row:', ok)
    try:
        for _ in range(4):   # tap device tips away, as a player would
            tb = ev("(() => { const c = document.getElementById('devTip'); if (!c || c.hidden || getComputedStyle(c).display === 'none') return null; const r = c.getBoundingClientRect(); return [r.x + r.width / 2, r.y + r.height / 2]; })()")
            if not tb: break
            pg.touchscreen.tap(tb[0], tb[1]); step(5)
        bb = ev("(() => { const e = [...document.querySelectorAll('span')].find(x => x.textContent === 'Tracked'); const b = e && (e.closest('button') || e); const r = b && b.getBoundingClientRect(); const top = r && document.elementFromPoint(r.x + r.width / 2, r.y + r.height / 2); return r ? [r.x + r.width / 2, r.y + r.height / 2, top ? top.tagName + '#' + top.id + '.' + top.className : null] : null; })()")
        print('  Tracked button at', bb); pg.touchscreen.tap(bb[0], bb[1]); step(5)
        rows = pg.get_by_text('The call booths').all(); print('  call-booth rows found:', len(rows))
        L = pg.get_by_text('The call booths')
        for k in range(L.count()):
            try: L.nth(k).scroll_into_view_if_needed(timeout=3000)
            except Exception: pass
        bx = [L.nth(k).bounding_box() for k in range(L.count())]; bx = [x for x in bx if x and x['width'] > 0]
        rb = [bx[0]['x'] + bx[0]['width'] / 2, bx[0]['y'] + bx[0]['height'] / 2] if bx else [0, 0]
        print('  row at', rb); pg.touchscreen.tap(rb[0], rb[1]); step(10)
        print('  after the row tap:', ev(G))
        for _ in range(3):
            if ev("typeof deviceClose === 'function' && DEV && DEV.open"): ev("deviceClose()"); step(3)
        pg.screenshot(path=str(OUT / f'{W}x{H}-trk-picked.png'), timeout=120000)
        into_room_and_call('trk')
    except Exception as e: print('  tracked row failed:', str(e)[:300])
    print(f'{W}x{H} errors:', errs[:4]); return pg, ev, step, b, into_room_and_call
with sync_playwright() as pw:
    for W, H in ((320, 640), (390, 844)):
        pg, ev, step, b, f = run(pw, W, H); b.close()
