# RV21 probe: VB2's vessel looks at phone size with the switch on and a stand-in event (VB1's block not in yet)
import sys, os, re
G = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
exec(open(os.path.join(os.path.dirname(G), 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
src = open(G).read().replace('const P926_APPT = true;', 'const EV_VESSEL_ON = true;\nconst P926_APPT = true;', 1)
vp = WORK / 'test' / '_rv21_vsky.html'; vp.write_text(src)
STUB = """(() => { SHIP_EVENTS.veyliVessel = { title: 'A Veyli vessel needs help', days: 4, commend: false, threads: [], pause: [], keep: [], settle: 'resolution',
  phases: [{ id: 'warning', at: [0, 340] }, { id: 'onset', at: [1, 480] }, { id: 'escalation', at: [2, 0] }, { id: 'resolution', at: [3, 540], clears: true }, { id: 'afterglow', at: [3, 600], clears: true }],
  systems: {}, routines: {}, galley: {}, status: {}, news: [] };
  vesselLooksInit(); return !!SHIP_EVENTS.veyliVessel.dressing; })()"""
def go(g, day, m, deck, room, tag, extra=''):
    g.ev(f"for (let t = Math.max(shipNow() + 1, {day - 1} * 1440 + {m} - 3); t <= {day - 1} * 1440 + {m}; t++) {{ setShipNow(t); EV_MIN = -1; eventsTick(); }}")
    g.ev(f"(() => {{ goToDeck({deck}); const tl = ROOM_TILES['{room}'], c = cellPos(...tl[Math.floor(tl.length / 2)]); player.obj.position.copy(cellPos(...nearestOpen(c.x, c.z, player))); player.stop(); target.copy(player.obj.position).setY(.7); {extra} eventsDress(shipNow()); }})()")
    g.step(45)
    info = g.ev("({ calls: renderer.info.render.calls, sky: !!VSKY.m, look: VSKY.m ? { k: VSKY.m.material.uniforms.uK.value, E: VSKY.m.material.uniforms.uE.value, F: VSKY.m.material.uniforms.uF.value, P: VSKY.m.material.uniforms.uP.value.toArray().map(Math.round) } : null, dress: [...DRESS.on.keys()].filter(k => /^vessel/.test(k)), clock: clockText() })")
    g.shot(f'{OUT}/{tag}.png'); print(tag, info)
with sync_playwright() as pw:
    g = Game(pw, str(vp), 390, 844)
    print('on', g.ev("vesselOn()"), 'stub', g.ev(STUB))
    g.ev("if (typeof GUIDE_ON !== 'undefined' && GUIDE_ON) { GUIDE.tq.length = 0; guideToast = () => false; }")
    g.ev("skipTo(26 * 1440 + 600); SHIP.event = null; eventStart('veyliVessel', 27)")
    go(g, 27, 13*60+50, 3, 'L', '01_sat1350_bow_before')
    go(g, 27, 15*60, 3, 'L', '02_sat1500_bow')
    go(g, 27, 11*60, 5, 'w', '03_sat1100_works_sheet')
    go(g, 28, 11*60, 5, 'w', '04_sun1100_works_crate_part')
    go(g, 28, 13*60+30, 5, 'w', '05_sun1330_works_chain')
    go(g, 29, 11*60, 5, 'f', '06_mon1100_shop_old')
    g.ev("SHIP.event.mine['vessel:part'] = 1")
    go(g, 29, 14*60, 5, 'f', '07_mon1400_shop_new')
    go(g, 29, 17*60+20, 3, 'L', '08_mon1720_bow_dark')
    go(g, 29, 17*60+40, 3, 'L', '09_mon1740_bow_flash')
    g.ev("for (let t = shipNow(); t < 28 * 1440 + 1060.6; t += .1) { setShipNow(t); }"); g.step(3)
    print('flash 17:40.6', g.ev("JSON.stringify(vesselShipFlash())"))
    go(g, 29, 18*60, 3, 'L', '10_mon1800_bow_lit')
    go(g, 30, 9*60+2, 3, 'L', '11_tue0902_bow_leaving')
    go(g, 30, 9*60+10, 3, 'L', '12_tue0910_bow_gone')
    go(g, 30, 10*60, 5, 'w', '13_tue1000_works_wall_sketch')
    g.ev("vesselShelve()")
    go(g, 30, 22*60, 4, 'a', '14_tue2200_bunk_shelf')
    print('errors', g.errors[:6])
    g.close()
