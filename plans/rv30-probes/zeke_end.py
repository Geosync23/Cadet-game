# RV30 probe (OB2 note 7): a new game skipped to Day 1 16:20 on Deck 5, you in the Works bay. Each ~ship minute: Zeke's
# distance and mode. You stand away from the beam till WALK_AT, then walk to the beam (moved there in steps). Two runs:
# 'stay' (you never go to the beam) and 'beam' (you go at 16:50). Usage: zeke_end.py WORKTREE BUILD [stay|beam]
import sys, os, json
WT, BUILD = sys.argv[1], sys.argv[2]; MODE = sys.argv[3] if len(sys.argv) > 3 else 'beam'
sys.argv = [sys.argv[0], BUILD]
src = open(WT + '/devmode_check.py').read().split("\ndef part_off")[0].replace("__file__.replace('devmode_check.py', 'cadet_test.py')", repr(WT + '/cadet_test.py'))
exec(src)
S = """(() => { const z = DECK_CREW.find(x => x.p.id === SHIP.intro.escort), P = player.obj.position, e = z && escortPlan(z.p, shipNow());
  const sp = PLACE_OF.has('5-beam-1') ? placeSpot('5-beam-1') : null;
  return { t: hhmm(SHIP.time.min), deck: deckDef.num, escort: SHIP.intro.escort, zeke: z ? Math.round(Math.hypot(z.x - P.x, z.z - P.z) * 10) / 10 : 'off deck', mode: e ? e.mode : null,
    beam: sp ? Math.round(Math.hypot(sp.x - P.x, sp.z - P.z) * 10) / 10 : null, told: SHIP.intro.done['d1-end:told'], painted: introNamePainted(), arrow: INTRO_UI.arrow, dlg: DIALOGUE ? DIALOGUE.id : null }; })()"""
NEXT = "(() => { const v = dialogueView(); if (!v) return null; if (v.choices) dialogueChoose(0); else dialogueNext(); return true; })()"
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME'), args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    pg = Page(ctx, '#dev'); pg.sign(); pg.step(20)
    pg.ev('newGameStart(true)'); pg.step(5); pg.sign(); pg.step(10)
    print('new', pg.ev("""(() => { skipTo(16 * 60 + 20); goToDeck(5); const R = DECKS[5].rooms, k = Object.keys(R).find(c => R[c].name === 'Works bay'); const tl = ROOM_TILES[k];
      const sp = placeSpot('5-beam-1'); const far = tl.map(c => [c, Math.hypot(cellPos(...c).x - sp.x, cellPos(...c).z - sp.z)]).sort((a, b) => b[1] - a[1])[0][0]; player.obj.position.copy(cellPos(...far)); return [introOn(), SHIP.time.day, hhmm(SHIP.time.min), SHIP.intro.escort]; })()""")); pg.step(10)
    far = []
    for i in range(160):
        pg.step(50); s = pg.ev(S)
        if s['dlg']: pg.ev(NEXT)
        if i % 3 == 0: print(json.dumps(s))
        m = int(s['t'][:2]) * 60 + int(s['t'][3:])
        if isinstance(s['zeke'], (int, float)) and s['zeke'] > 6 and m >= 990 and not s['painted'] and (s['beam'] or 99) > 3: far.append(s['t'])
        if MODE == 'beam' and m >= 16 * 60 + 50 and (s['beam'] or 0) > 2.5:
            pg.ev("(() => { const sp = placeSpot('5-beam-1'), P = player.obj.position; const dx = sp.x - P.x, dz = sp.z - P.z, d = Math.hypot(dx, dz), k = Math.min(1, 0.8 / d); P.x += dx * k; P.z += dz * k; })()")
        if m >= 17 * 60 + 45: break
    print('Zeke more than 6 m away (16:30 on, not at the beam, not painted):', far[:12], len(far)); print('errors', pg.errors[:4]); b.close()
