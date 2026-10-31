# RV30 probe (OB2 note 16): Rina's new-crew health check in the real game (Dev mode, #dev), intro on. Dev jump to Day 2
# 13:50 in the infirmary, then the game runs: the booking, the arrow; at TAP_AT (minutes after 14:00) you tap Rina (her
# real tap: crewTap path via introTap) and read at PACE loops (~1 real s each) a card. Logs the booking's status, the
# arrow, the scene, Settling-in, Mail. Usage (from the worktree): health_tap.py WORKTREE BUILD [TAP_AT] [PACE]
import sys, os, json
WT, BUILD = sys.argv[1], sys.argv[2]; TAP_AT = int(sys.argv[3]) if len(sys.argv) > 3 else 5; PACE = int(sys.argv[4]) if len(sys.argv) > 4 else 3
sys.argv = [sys.argv[0], BUILD]
src = open(WT + '/devmode_check.py').read().split("\ndef part_off")[0].replace("__file__.replace('devmode_check.py', 'cadet_test.py')", repr(WT + '/cadet_test.py'))
exec(src)
S = """(() => { const I = SHIP.intro, a = SHIP.device.appts.filter(x => x.by === 'rina'), r = DECK_CREW.find(x => x.p.id === 'rina'), P = player.obj.position, v = DIALOGUE && dialogueView();
  return { t: hhmm(SHIP.time.min), day: SHIP.time.day, on: introOn(), room: (ROOMS[roomAt(...player.here())] || {}).name, appts: a.map(x => [x.id, 'D' + (Math.floor(x.at / 1440) + 1) + ' ' + hhmm(x.at % 1440), x.status, x.tap || 0]),
    met: I.done['d2-health:met'], again: I.done['d2-health:again'], arrow: INTRO_UI.arrow, rina: r ? [(ROOMS[roomAt(...cellAt(r.x, r.z))] || {}).name, Math.round(Math.hypot(r.x - P.x, r.z - P.z) * 10) / 10] : null,
    dlg: DIALOGUE ? DIALOGUE.id + ': ' + (v ? (v.text || '').slice(0, 50) : '') : null, mail: SHIP.social && SHIP.social.mail ? SHIP.social.mail.filter(m => /Rina/.test(m.from)).map(m => m.subject) : [] }; })()"""
NEXT = "(() => { const v = dialogueView(); if (!v) return null; if (v.choices) dialogueChoose(0); else dialogueNext(); return true; })()"
GO = """(() => { const r = DECK_CREW.find(x => x.p.id === 'rina'); if (!r) return 'no rina'; const c = cellAt(r.x, r.z);
  for (const [dx, dz] of [[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,-1]]) { const q = cellPos(c[0] + dx, c[1] + dz); if (/infirmary/i.test((ROOMS[roomAt(c[0] + dx, c[1] + dz)] || {}).name || '')) { player.obj.position.set(q.x, player.obj.position.y, q.z); return 'by her'; } }
  return 'no spot'; })()"""
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME'), args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    pg = Page(ctx, '#dev'); pg.sign(); pg.step(20)
    rk = pg.ev("(() => { const R = DECKS[3].rooms; return Object.keys(R).find(c => R[c] && /infirmary/i.test(R[c].name)); })()")
    # a new game (the intro on), the clock moved to Day 2 13:50, you in the infirmary (Dev mode's jump ends the intro)
    pg.ev('newGameStart(true)'); pg.step(5); pg.sign(); pg.step(10)
    print('new', pg.ev("(() => { skipTo(1440 + 13 * 60 + 50); if (SHIP.intro.done['d2-health:appt'] === undefined) introBookHealth(); goToDeck(3); const tl = ROOM_TILES[%s]; player.obj.position.copy(cellPos(...tl[(tl.length / 2) | 0])); return [introOn(), SHIP.time.day, hhmm(SHIP.time.min)]; })()" % json.dumps(rk))); pg.step(10)
    s = pg.ev(S); print(json.dumps(s))
    phase, cards = 'wait', 0
    for i in range(300):
        pg.step(30); s = pg.ev(S)   # ~1 real s of game (0.6 ship min)
        m = int(s['t'][:2]) * 60 + int(s['t'][3:])
        if i % 5 == 0 or s['dlg']: print(json.dumps(s))
        if phase == 'wait' and s['day'] == 2 and m >= 14 * 60 + TAP_AT:
            print('GO', pg.ev(GO)); pg.step(2)
            print('TAP', pg.ev("(() => { const r = DECK_CREW.find(x => x.p.id === 'rina'); return introTap(r.p); })()")); phase = 'scene'; continue
        if phase == 'scene' and s['dlg']:
            if i % PACE == 0: pg.ev(NEXT); cards += 1
        elif phase == 'scene' and not s['dlg'] and cards: print('END', json.dumps(s)); phase = 'after'; after = i
        if phase == 'after' and i - after > 10: break
    print('errors', pg.errors[:4]); b.close()
