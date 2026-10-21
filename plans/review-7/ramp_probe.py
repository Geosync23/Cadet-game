# PR7: PT1 T2's Off the Tern scene live with a real save at phone size: the ramp shuts as the Tern comes in, Raman's
# word and the ramp at 17:40, the arrival out of the aisle and down, the greeter at the foot; a reload mid-scene.
# python3 ramp_probe.py BUILD.html OUTDIR
import os, sys, json, re, pathlib
exec(open('/home/user/Cadet-game/plans/review-7/dm_trad_probe.py').read().split("with sync_playwright() as pw:")[0].replace("_dm_trad_probe.html", "_ramp_probe.html"))
ST = r"""(() => { const ag = id => { const a = DECK_CREW.find(a => a.p.id === id); return a ? [Math.floor(a.x + OX), Math.floor(a.z + OZ)].join(',') + (a.p ? '' : '') : null; };
  const w = id => { const p = schedPeople().find(q => q.id === id); const s = p && whereIs(p, shipNow()); return s ? (s.placeId || '') + '/' + (s.tag || '') : null; };
  return { t: hhmm(SHIP.time.min), deck: deckDef.num, ramp: +ternRampOpen().toFixed(2), basil: ag('bramwell-basil'), basilPlan: w('bramwell-basil'), zeke: ag('torres-zeke'), zekePlan: w('torres-zeke'),
    toast: (document.querySelector('#toast') || {}).textContent || '', going: schedPeople().filter(p => { const s = whereIs(p, shipNow()); return s && s.tag && s.tag.startsWith('ev-off-the-tern'); }).length }; })()"""
def minute(pg, n=1):
    for _ in range(n): pg.step(1000, 100)          # 100 s real a ship minute at SHIP_RATE 0.6: 1000 frames of 0.1 s
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    for w, h, reload_at in ((390, 844, None), (360, 780, '17:38')):
        ctx = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1)
        pg = Page(ctx, '?debug'); pg.sign()
        pg.ev('newGameStart(false); introSkip(); skipTo(20 * 1440 + 17 * 60 + 30); goToDeck(5)'); pg.step(10)
        pg.ev('(() => { const c = cellPos(9, 12), at = nearestOpen(c.x, c.z, player); player.obj.position.copy(cellPos(...at)); target.copy(player.obj.position).setY(.7); })()'); pg.step(5)
        log = []; toasts = set()
        while True:
            s = pg.ev(ST); log.append(s); toasts.add(s['toast'][:80])
            print(f"  {w} {json.dumps(s)}", flush=True)
            if s['t'] in ('17:38', '17:41', '17:44', '17:48'): pg.shot(OUT / f"ramp_{w}_{s['t'].replace(':', '')}.png")
            if reload_at and s['t'] == reload_at:
                pg.ev('saveGame()'); pg.page.reload(); pg.reload_ready(); reload_at = None
                s2 = pg.ev(ST); print(f'  {w} after reload: {json.dumps(s2)}', flush=True)
            if s['t'] >= '17:50': break
            minute(pg)
        by = {x['t']: x for x in log}
        def at(t): return by.get(t) or {}
        check(at('17:37').get('ramp', 1) == 0 or at('17:38').get('ramp', 1) == 0, f'{w}: the ramp shut before 17:40 ({at("17:37").get("ramp")}, {at("17:38").get("ramp")})')
        check(any('Raman' in t for t in toasts), f'{w}: Raman\'s word at 17:40 ({[t for t in toasts if t]})')
        check(at('17:42').get('ramp') == 1, f'{w}: the ramp open by 17:42 ({at("17:42").get("ramp")})')
        check((at('17:41').get('basilPlan') or '').startswith('5-tern-aisle'), f'{w}: Basil in the aisle at 17:41 ({at("17:41").get("basilPlan")})')
        check('off-the-tern' in (at('17:47').get('basilPlan') or ''), f'{w}: Basil in the crowd at 17:47 ({at("17:47").get("basilPlan")}, at {at("17:47").get("basil")})')
        check(at('17:40').get('zeke') is not None and 'greet' in (at('17:40').get('zekePlan') or ''), f'{w}: Zeke at the foot at 17:40 ({at("17:40").get("zeke")}, {at("17:40").get("zekePlan")})')
        sv = pg.page.evaluate('() => (window.__sc("saveGame()"), localStorage.getItem("starship-cadet-save"))'); pg.page.reload(); pg.reload_ready()
        s3 = pg.ev(ST); print(f'  {w} reload at 17:50: {json.dumps(s3)}')
        check(s3['ramp'] == 1 and s3['deck'] == 5, f'{w}: after a reload at 17:50 the ramp is open, deck 5')
        check(not pg.errors, f'{w}: errors {pg.errors[:3]}'); ctx.close()
    b.close()
print('RAMP PROBE ' + ('OK' if not BAD else 'FAILED: ' + '; '.join(BAD)))
