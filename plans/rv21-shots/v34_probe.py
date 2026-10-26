import sys, os
G = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
exec(open(os.path.join(os.path.dirname(G), 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
src = open(G).read().replace("const EV_VESSEL_ON = URL_FLAGS.has('evvessel');", "const EV_VESSEL_ON = true;", 1)
vp = WORK / 'test' / '_rv21_v34.html'; vp.write_text(src)
GOAL = "(() => { const g = goalNow(); return { clock: clockText(), goal: g && g.label, q: (GUIDE.list||[]).filter(x => /^vessel:/.test(x.id)).map(x => x.id + ':' + x.level), dlg: DIALOGUE && DIALOGUE.id, card: !!document.querySelector('.devChoose, #devChoose, [data-choose]'), calls: renderer.info.render.calls, crew5: deckDef.num === 5 ? DECK_CREW.length : null }; })()"
def to(g, abs, step=1):
    g.ev(f"(() => {{ for (let t = Math.max(shipNow() + 1, {abs} - 2); t <= {abs}; t += {step}) {{ setShipNow(t); EV_MIN = -1; eventsTick(); }} }})()")
with sync_playwright() as pw:
    g = Game(pw, str(vp), 390, 844)
    g.ev("skipTo(26 * 1440 + 360)"); g.step(5)
    g.ev("(() => { for (let t = 26*1440+360; t <= 27*1440 + 760; t += 5) { setShipNow(t); EV_MIN = -1; eventsTick(); } SHIP.event.mine['vessel:met'] = 1; SHIP.event.mine['vessel:roundOne'] = 1; SHIP.event.mine['vessel:signed'] = 1; SHIP.event.mine['vessel:told'] = 1; })()")
    to(g, 27*1440 + 770); g.step(30); print('12:50', g.ev(GOAL)); g.shot(f'{OUT}/v1_sun1250_chain_arrow.png')
    g.ev("(() => { goToDeck(5); const z = placeSpot('5-vchain-call'); player.obj.position.set(z.x + .6, player.obj.position.y, z.z + .6); player.stop(); })()")
    to(g, 27*1440 + 785); g.step(120); print('13:05 at Zeke', g.ev(GOAL))
    print('join', g.ev("(() => { const a = DECK_CREW.find(c => c.p && c.p.id === 'torres-zeke'); if (!a) return 'no zeke'; try { return String(tradJoinTap(a)); } catch (e) { return 'err ' + e.message; } })()"))
    g.step(90); to(g, 27*1440 + 800); g.step(120); print('13:20', g.ev(GOAL)); g.shot(f'{OUT}/v2_sun1320_chain.png')
    # Monday: the job
    g.ev("(() => { for (let t = shipNow(); t <= 28*1440 + 555; t += 5) { setShipNow(t); EV_MIN = -1; eventsTick(); } })()")
    to(g, 28*1440 + 562); g.step(30); print('mon 09:22', g.ev(GOAL)); g.shot(f'{OUT}/v3_mon0922_job_arrow.png')
    print('errors', g.errors[:5]); g.close()
