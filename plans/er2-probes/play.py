import os,sys,json
os.environ.setdefault('CADET_CHROME','/opt/pw-browsers/chromium')
os.environ['CADET_WORK']='/tmp/cw-er2'; os.makedirs('/tmp/cw-er2/test',exist_ok=True)
if not os.path.exists('/tmp/cw-er2/three'): os.symlink('/tmp/cadet-work/three','/tmp/cw-er2/three')
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0])
H="""
window.__near = (id, d) => { const a = DECK_CREW.find(a => a.p && a.p.id === id); if (!a) return 'absent'; const c = new THREE.Vector3(a.x + (d||0.8), 0, a.z); player.obj.position.copy(c); target.copy(player.obj.position).setY(.7); return [a.x.toFixed(1), a.z.toFixed(1), (whereIs(a.p, shipNow())||{}).tag || (whereIs(a.p, shipNow())||{}).act]; };
window.__dlg = (pick) => { const out=[]; let n=0; while (DIALOGUE && n++ < 40) { const l = DIALOGUE.queue[DIALOGUE.i]; if (l && l.choice) { out.push('CHOICE->'+pick); dialogueStep(pick); } else { out.push(l ? (l.who||'')+': '+(typeof l.text==='function'?'(fn)':l.text) : '(end)'); dialogueStep(); } } if (DIALOGUE) dialogueEnd(true); return out; };
"""
with sync_playwright() as pw:
    g=Game(pw, sys.argv[1], w=390, h=844)
    g.ev(H)
    def at(day,m): return (day-1)*1440+m
    def go(day,m,deck):
        g.ev(f"skipTo({at(day,m)})"); g.ev(f"goToDeck({deck})"); g.step(10)
    def run(steps=150):
        for i in range(steps//30): g.step(30)
    go(12,17*60+40,3)
    print('event', g.ev("JSON.stringify(SHIP.event && {id:SHIP.event.id, phase:SHIP.event.phase, day:SHIP.event.startDay})"))
    print('lukas', g.ev("__near('dlamini-lukas')")); run(150)
    print('dlg', g.ev("DIALOGUE && DIALOGUE.id"))
    print(g.ev("__dlg(0)"))
    print('mine', g.ev("JSON.stringify(SHIP.event.mine)"))
    go(13,15*60+5,3); print('lukas sat', g.ev("__near('dlamini-lukas')")); run(150)
    print('dlg', g.ev("DIALOGUE && DIALOGUE.id")); print(g.ev("__dlg(1)"))
    g.ev("goToDeck(4)"); g.step(10); print('brennan', g.ev("__near('brennan', 0.7)")); run(150)
    print('dlg', g.ev("DIALOGUE && DIALOGUE.id")); print(g.ev("__dlg(0)"))
    g.ev("goToDeck(3)"); g.step(10); print('lukas', g.ev("__near('dlamini-lukas')")); run(150)
    print('mine', g.ev("JSON.stringify(SHIP.event.mine)"))
    go(13,18*60+25,3); 
    g.ev("player.obj.position.copy(cellPos(30,6)); target.copy(player.obj.position).setY(.7)"); run(240)
    print('dlg supper', g.ev("DIALOGUE && DIALOGUE.id")); print(g.ev("__dlg(0)"))
    print('supper crowd', g.ev("(() => { const t=shipNow(); let n=0, st=0; for (const p of schedPeople()) { const w=whereIs(p,t); if (w && /^ev-lanternSupper/.test(w.tag||'')) { n++; if (/crowd/.test(w.placeId||'')) st++; } } return [n, st]; })()"), 'calls', g.ev("renderer.info.render.calls"))
    print('errors', g.errors[:5])
    g.close()
