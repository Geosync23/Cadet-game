from pp import *
import sys
WAKE = int(sys.argv[1]) if len(sys.argv) > 1 else 8*60+20
g = start(); g.step(10); sign(g); g.secs(2)
# idle through the arrival evening on paper (a player who isn't anywhere), then sleep: what a real night's skipTo does
g.ev("""(() => { for (let t = shipNow(); t <= 20*60+30; t++) { setShipNow(t); introAdvance(t, null); } return SHIP.intro.step; })()""")
print(g.ev(STATE))
g.ev(f"skipTo(1440*1 + {WAKE})")   # Day 2 at WAKE (Day 1 skipped: the shadow shift etc. never played)
print(g.ev(STATE), g.ev("introOn()"))
OFFICE = r"""(() => { const a = DECK_CREW.find(x => x.p.id==="calder"); return a ? [cellAt(a.x,a.z), (ROOMS[roomAt(...cellAt(a.x,a.z))]||{}).name] : null; })()"""
CALD = r"""(() => { const d = planDay(ROSTER.find(p => p.id==='calder'), SHIP.time.day); return d.filter(s => s.to > 7*60 && s.from < 10*60).map(s => [hhmm(s.from), hhmm(s.to), s.deck, s.placeId, s.act||'', s.tag||'']); })()"""
print('calder plan', g.ev(CALD))
g.ev("goToDeck(5)"); g.step(5)
# stand inside the office
print(g.ev(r"""(() => { const r = Object.keys(ROOMS).find(k => ROOMS[k].name === "Works Chief's office"); const t = []; for (let x=0;x<W;x++) for (let z=0;z<D;z++) if (roomAt(x,z)===r && free(x,z)) t.push([x,z]); window.__off = t; return [r, t.length, t.slice(0,4)]; })()"""))
for i in range(40):
    g.shipmins(2)
    if i == 4:
        g.ev("(() => { const c = window.__off[Math.floor(window.__off.length/2)]; player.obj.position.copy(cellPos(...c)); target.copy(player.obj.position).setY(.7); })()")
    s = g.ev(STATE)
    print(s['t'], s['me'], s['dlg'], g.ev(OFFICE), g.ev("SHIP.intro.done['d2-solo:met']"))
    if s['dlg']: g.snap('01-probe-fixed-meeting'); break
    pass
print(g.errors[:5])
