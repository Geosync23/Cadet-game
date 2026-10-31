# RV29: PL2 note 3, the real game (Dev, a save, so SEAT_BTN_ALL on): stand by a free lounge seat on Deck 4's common room and
# Deck 3's promenade, shot the screen, read the button, click it, shot again. usage: seat_shot.py WORKTREE BUILD OUT
import sys, os, json
WT, BUILD, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
sys.argv = [sys.argv[0], BUILD]
src = open(WT + '/devmode_check.py').read().split("\ndef part_off")[0].replace("__file__.replace('devmode_check.py', 'cadet_test.py')", repr(WT + '/cadet_test.py'))
exec(src)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get('CADET_CHROME'), args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    pg = Page(ctx, '#dev'); pg.sign(); pg.step(20)
    print('jump', pg.ev("devmodeRun('Jump', () => devmodeSetCareerTo(3, { id: 'rv29s', label: 's', day: 3, by: 2, at: 1150, where: { deck: 4, room: 'K' } }))")); pg.step(30)
    for deck, typ in [(4, 'common-room'), (3, 'bench')]:
        r = pg.ev(f"""(() => {{ if (deckDef.num !== {deck}) goToDeck({deck}); const pl = [...PLACE_OF.values()].find(q => q.type === '{typ}' && q.pose === 'sit' && !privatePlace(q) && !heldBy(q.id)); if (!pl) return null;
          const sp = placeSpot(pl.id); let best = null; for (let i = 0; i < W; i++) for (let j = 0; j < D; j++) {{ if (!free(i, j)) continue; const c = cellPos(i, j), d = Math.hypot(c.x - sp.x, c.z - sp.z); if (d > .5 && (!best || d < best[1])) best = [c, d]; }}
          player.stop && player.stop(); player.obj.position.set(best[0].x, 0, best[0].z); return [pl.id, SEAT_BTN_ALL]; }})()"""); pg.step(30)
        btn = pg.ev("(() => { const b = document.getElementById('seatBtn'); return b ? [b.hidden, b.textContent, b.getBoundingClientRect().toJSON()] : null; })()")
        print(deck, typ, r, 'button', json.dumps(btn)); pg.shot(f'{OUT}/seat_{deck}_before.png')
        if btn and not btn[0]:
            pg.page.click('#seatBtn'); pg.step(60); print('  after click', pg.ev("ACT ? [ACT.kind, ACT.placeId, ACT.phase, ACT.o && ACT.o.title, ACT.def && ACT.def.title, roomAt(...player.here()), (PLACE_OF.get(ACT.placeId) || {}).room, ((deckDef.rooms || {})[(PLACE_OF.get(ACT.placeId) || {}).room] || {}).name] : null"), pg.ev("(document.querySelector('#act, #actCard, .act') || {}).innerText || null"), pg.ev("document.getElementById('seatBtn').hidden")); pg.shot(f'{OUT}/seat_{deck}_sat.png')
            pg.ev("ACT && actEnd(true)"); pg.step(20)
    print('errors', pg.errors[:5]); b.close()
