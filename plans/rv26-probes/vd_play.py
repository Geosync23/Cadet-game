# RV26: play the Veyli dinner (EV2 V-1) in the real game: Dev jump to Day 18 18:40 in the Captain's quarters, then run.
import sys, os, json, pathlib
sys.argv = [sys.argv[0], sys.argv[1]]
G = '/home/user/Cadet-game/devmode_check.py'
src = open(G).read().split("\ndef part_off")[0].replace("__file__.replace('devmode_check.py', 'cadet_test.py')", "'/home/user/Cadet-game/cadet_test.py'")
exec(src)
OUT = pathlib.Path(os.environ.get('VD_OUT', '.'))
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get('CADET_CHROME'), args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    pg = Page(ctx, '#dev'); pg.sign(); pg.step(20)
    r = pg.ev("devmodeRun('Jump', () => devmodeSetCareerTo(18, { ...devmodeJumpOf('evVisitDinner'), at: 1120, where: " + os.environ.get('VD_WHERE', '{ deck: 2, room: "C" }') + " }))"); pg.step(10)
    print('jump', r)
    if os.environ.get('VD_PRE'): print('pre', pg.ev(os.environ['VD_PRE']))
    S = """(() => { const q = SHIP.occasions.find(x => x.id === 'veyliDinner'); const ids = ['marrow','teshavi','saruth','vance','kesrin','moleth','ithra'];
      const cr = ids.map(id => { const c = DECK_CREW.find(x => x.p && x.p.id === id); if (!c) return [id, 'not on deck'];
        return [id, c.goalId, !!c.settled, c.pose]; });
      return { t: hhmm(SHIP.time.min), day: SHIP.time.day, deck: deckDef.num, room: roomAt(...player.here()), occ: q ? { st: q.status, met: q.met, f: q.f } : null,
        act: typeof ACT !== 'undefined' && ACT ? [ACT.kind, ACT.placeId, ACT.def && ACT.def.mins] : null, dlg: DIALOGUE && dialogueView() ? dialogueView().name + ': ' + dialogueView().text + (dialogueView().choices ? ' [choice]' : '') : null,
        guide: GUIDE.shown, goal: IX_GOAL ? IX_GOAL.label + ' @' + IX_GOAL.deck + (IX_GOAL.place ? '/' + IX_GOAL.place : '') : null, cr }; })()"""
    try: print(json.dumps(pg.ev(S)))
    except Exception as e: print('state err', e)
    for i in range(int(os.environ.get('VD_N', '90'))):
        pg.step(60)
        try: s = pg.ev(S)
        except Exception as e: print('state err', str(e)[:200]); break
        print(json.dumps(s)[:900])
        if s['dlg']:
            try: pg.ev("(() => { const v = dialogueView(); if (v && v.choices) dialogueChoose(0); else dialogueNext(); })()")
            except Exception: pass
        if i in (8, 20, 45): pg.shot(str(OUT / f'vd_{os.environ.get("VD_TAG", "")}{i}.png'))
        if s['t'] >= '20:20': break
    print('errors', pg.errors[:5])
    b.close()
