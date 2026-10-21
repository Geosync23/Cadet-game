# PR7: Dev mode D6a (Set career) through the real buttons at phone size, with reloads; the career's shape kept by
# worksClean; the real save untouched; play on from the landing. python3 dm_set_probe.py BUILD.html OUTDIR
import os, sys, json, re, pathlib
exec(open('/home/user/Cadet-game/plans/review-7/dm_trad_probe.py').read().split("with sync_playwright() as pw:")[0].replace("_dm_trad_probe.html", "_dm_set_probe.html"))
SNAP = r"""(() => { const W = SHIP.works; const bed = playerBed(), n = deckOf(bed), b = (DECKS[n].places || []).find(p => p.id === bed);
  return { t: clockText(), rank: W && W.rank, tier: W && W.tier, xp: W && W.xp, band: worksBand(), tr: W && Object.keys(W.tr).sort().join(','), home: W && W.home, bed,
    shape: W ? (C => Object.keys(C).every(k => JSON.stringify(C[k]) === JSON.stringify(W[k])))(worksClean(JSON.parse(JSON.stringify(W)))) : null, deck: deckDef.num,
    inBedRoom: b ? roomAt(...player.here()) === roomAt(...b.at) && n === deckDef.num : false, pip: typeof promoPipOn === 'function' ? promoPipOn() : null,
    asked: (SHIP.occasions || []).filter(r => r.status === 'asked').map(r => r.id), foot: document.querySelector('#dmSheet .dmFoot') && document.querySelector('#dmSheet .dmFoot').textContent }; })()"""
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    for w, h, day in ((390, 844, 12), (360, 780, 10)):
        ctx = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1)
        pg = Page(ctx, '?debug'); pg.sign(); pg.ev('newGameStart(false); introSkip(); saveGame()'); real = {k: v for k, v in store(pg).items() if not k.endswith('-dev') and 'dev-' not in k}; pg.page.close()
        pg = Page(ctx, '#dev'); pg.sign(); pg.ev('newGameStart(false); introSkip()'); pg.step(10)
        pg.ev('devmodeOpen(true); DM_UI.tab = "set"; devmodeDraw()'); pg.step(2)
        check(pg.tap('Day ' + str(day)), f'{w}: the Day {day} shortcut')
        pg.shot(OUT / f'd6a_{w}_tab.png')
        lbl = 'Set career to Day ' + str(day)
        check(pg.tap(lbl), f'{w}: {lbl} (first tap asks)')
        check(pg.tap('Tap again: a new Dev game'), f'{w}: the second tap')
        pg.page.wait_for_timeout(900)
        for _ in range(60):
            if pg.ev('!DM_HOLD'): break
            pg.page.wait_for_timeout(500)
        pg.step(20); s = pg.ev(SNAP); print(f'  {w} after Set career: {json.dumps(s)}'); print('  msg:', pg.ev('DM_UI.msg'))
        check(s['t'].startswith(f'Day {day},') and s['t'].endswith('06:00'), f'{w}: landed {s["t"]}')
        check(s['rank'] == 'officer' and s['tier'] == 2, f'{w}: rank {s["rank"]} tier {s["tier"]}')
        check(s['shape'], f'{w}: SHIP.works keeps its shape through worksClean')
        check(s['inBedRoom'] and s['home'] == '4-23', f'{w}: woke in the bed\'s room ({s["bed"]}, deck {s["deck"]})')
        check(not s['asked'], f'{w}: nothing asked: {s["asked"]}')
        check('approximate' in (s['foot'] or ''), f'{w}: the foot says approximate: {s["foot"]}')
        pg.ev('devmodeOpen(true); DM_UI.tab = "set"; devmodeDraw()'); pg.step(2); pg.shot(OUT / f'd6a_{w}_whatsset.png')
        sv = pg.page.evaluate('() => localStorage.getItem("starship-cadet-save-dev")')
        pg.page.reload(); pg.reload_ready(); s2 = pg.ev(SNAP)
        check({k: v for k, v in s2.items() if k != 'foot'} == {k: v for k, v in s.items() if k != 'foot'}, f'{w}: the same after a reload: {json.dumps(s2)}')
        check(json.loads(sv)['ship'].get('works') == json.loads(pg.page.evaluate('() => (window.__sc("saveGame()"), localStorage.getItem("starship-cadet-save-dev"))'))['ship'].get('works'), f'{w}: ship.works byte-equal across the reload')
        # play on: the rest of the day hour by hour; nothing trained opens again, no first-week meeting
        pg.ev('devmodeOpen(false)')
        for hr in range(7, 21, 2):
            pg.ev(f'skipTo({(day - 1) * 1440 + hr * 60})'); pg.step(15)
        W = pg.ev("(() => { const W = SHIP.works, again = Object.entries(W.op).filter(([d]) => +d >= " + str(day) + ").flatMap(([d, ids]) => ids).filter(id => W.tr[id] !== undefined && W.tr[id] < " + str(day) + "); return { again, cur: W.cur, notes: (SHIP.notes || []).filter(n => /intro|meeting|missed/.test(n.kind)).map(n => n.kind).slice(-6) }; })()")
        print(f'  {w} played on to 19:00: {json.dumps(W)}')
        check(not W['again'], f'{w}: trained rows opened again: {W["again"]}')
        pg.shot(OUT / f'd6a_{w}_played.png')
        # Undo: the game before Set career back
        with pg.page.expect_navigation(timeout=90000):
            pg.ev('devmodeUndo()')
        pg.reload_ready(); t = pg.ev('clockText()'); print('  after Undo:', t, pg.ev('SHIP.works && SHIP.works.rank'))
        st = store(pg); check({k: v for k, v in st.items() if k in real} == real, f'{w}: the real game\'s keys untouched')
        check(not pg.errors, f'{w}: errors {pg.errors[:3]}')
        ctx.close()
    b.close()
print('DM SET PROBE ' + ('OK' if not BAD else 'FAILED: ' + '; '.join(BAD)))
