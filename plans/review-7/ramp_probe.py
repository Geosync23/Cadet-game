# PR7: PT1's Tern ramp live with a real save at phone size (T2 arrivals, T3 leavers): Day 21.
#  boarding 14:45-15:05: Theo up the ramp into the aisle and gone by 15:00; the ramp shut after; a reload at 14:58
#  (mid-boarding) and at 16:00 (the ramp shuts again once clear);
#  arriving 17:30-17:50: Zeke at the foot, the ramp open at 17:40 with Raman's word, Basil out of the aisle into the
#  crowd; a reload at 17:38 (the 360 run) and at 17:50.   python3 ramp_probe.py BUILD.html OUTDIR
import os, sys, json, re, pathlib
exec(open('/home/user/Cadet-game/plans/review-7/dm_trad_probe.py').read().split("with sync_playwright() as pw:")[0].replace("_dm_trad_probe.html", "_ramp_probe.html"))
ST = r"""(() => { const ag = id => { const a = DECK_CREW.find(a => a.p.id === id); return a ? [Math.floor(a.x + OX), Math.floor(a.z + OZ)].join(',') : null; };
  const w = id => { const p = schedPeople().find(q => q.id === id); const s = p && whereIs(p, shipNow()); return s ? (s.placeId || '') + '/' + (s.tag || '') + '/' + (s.act || '') : null; };
  return { t: hhmm(SHIP.time.min), deck: deckDef.num, ramp: +ternRampOpen().toFixed(2), theo: ag('teague-theo'), theoPlan: w('teague-theo'), basil: ag('bramwell-basil'), basilPlan: w('bramwell-basil'),
    zeke: ag('torres-zeke'), zekePlan: w('torres-zeke'), toast: (document.querySelector('#toast') || {}).textContent || '' }; })()"""
def minute(pg, n=1):
    for _ in range(n): pg.step(50, 1000 / 30)      # a ship minute is 1/0.6 = 1.67 s real (SHIP_RATE): 50 frames at 30 a second
def stand(pg): pg.ev('(() => { const c = cellPos(9, 12), at = nearestOpen(c.x, c.z, player); player.obj.position.copy(cellPos(...at)); target.copy(player.obj.position).setY(.7); })()'); pg.step(5)
def scene(pg, w, t0, t1, reloads, shots):
    log = {}; toasts = set()
    while True:
        s = pg.ev(ST); log[s['t']] = s; toasts.add(s['toast'][:90]); print(f"  {w} {json.dumps(s)}", flush=True)
        if s['t'] in shots: pg.shot(OUT / f"ramp_{w}_{s['t'].replace(':', '')}.png")
        if s['t'] in reloads:
            reloads.remove(s['t']); pg.ev('saveGame()'); pg.page.reload(); pg.reload_ready(); minute(pg)
            s2 = pg.ev(ST); print(f'  {w} after a reload at {s["t"]}: {json.dumps(s2)}', flush=True); log['reload ' + s['t']] = s2
        if s['t'] >= t1: break
        minute(pg)
    return log, toasts
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    for w, h, rl in ((390, 844, ['14:58', '17:50']), (360, 780, ['16:00', '17:38'])):
        ctx = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1)
        pg = Page(ctx, '?debug'); pg.sign()
        pg.ev('newGameStart(false); introSkip(); skipTo(20 * 1440 + 14 * 60 + 45); goToDeck(5)'); pg.step(10); stand(pg)
        A, _ = scene(pg, w, '14:45', '15:05', [x for x in rl if x < '15:10'], ('14:56', '14:59'))
        at = lambda t: A.get(t) or {}
        check(any('5-tern-aisle' in (at(t).get('theoPlan') or '') for t in ('14:57', '14:58', '14:59')), f'{w}: Theo in the aisle 14:57-14:59 ({[at(t).get("theoPlan") for t in ("14:57", "14:58", "14:59")]})')
        check(at('15:02').get('theo') is None and 'away' in (at('15:02').get('theoPlan') or ''), f'{w}: Theo gone by 15:02 ({at("15:02").get("theo")}, {at("15:02").get("theoPlan")})')
        check(at('15:04').get('ramp') == 0, f'{w}: the ramp shut behind him by 15:04 ({at("15:04").get("ramp")})')
        if '16:00' in rl:
            pg.ev('skipTo(20 * 1440 + 16 * 60)'); pg.step(10); stand(pg)
            B, _ = scene(pg, w, '16:00', '16:03', ['16:00'], ())
            check(B.get('16:03', {}).get('ramp') == 0, f'{w}: after a reload at 16:00 the ramp shut again ({B.get("16:03", {}).get("ramp")})')
        pg.ev('skipTo(20 * 1440 + 17 * 60 + 30)'); pg.step(10)
        if pg.ev('deckDef.num') != 5: pg.ev('goToDeck(5)'); pg.step(10)
        stand(pg)
        C, toasts = scene(pg, w, '17:30', '17:50', [x for x in rl if x > '17:00'], ('17:38', '17:41', '17:44', '17:48'))
        at = lambda t: C.get(t) or {}
        check(at('17:37').get('ramp', 1) == 0, f'{w}: the ramp shut before 17:40 ({at("17:37").get("ramp")})')
        check(any('Raman' in t for t in toasts), f'{w}: Raman\'s word at 17:40 ({[t for t in toasts if t]})')
        check(at('17:42').get('ramp') == 1, f'{w}: the ramp open by 17:42 ({at("17:42").get("ramp")})')
        check(any('5-tern-aisle' in (at(t).get('basilPlan') or '') for t in ('17:40', '17:41', '17:42')), f'{w}: Basil in the aisle 17:40-17:42 ({[at(t).get("basilPlan") for t in ("17:40", "17:41", "17:42")]})')
        check('off-the-tern' in (at('17:47').get('basilPlan') or '') and at('17:47').get('basil') is not None, f'{w}: Basil on the deck in the crowd at 17:47 ({at("17:47").get("basilPlan")}, at {at("17:47").get("basil")})')
        check(at('17:39').get('zeke') is not None and 'greet' in (at('17:39').get('zekePlan') or ''), f'{w}: Zeke at the foot at 17:39 ({at("17:39").get("zeke")}, {at("17:39").get("zekePlan")})')
        r = C.get('reload 17:50') or C.get('reload 17:38')
        if r: check(r['deck'] == 5, f'{w}: after the reload, deck 5, ramp {r["ramp"]}')
        check(not pg.errors, f'{w}: errors {pg.errors[:3]}'); ctx.close()
    b.close()
print('RAMP PROBE ' + ('OK' if not BAD else 'FAILED: ' + '; '.join(BAD)))
