from pp import *
import sys
WAKE = int(sys.argv[1])
g = start(); g.step(10); sign(g); g.secs(2)
g.ev("""(() => { for (let t = shipNow(); t <= 20*60+30; t++) { setShipNow(t); introAdvance(t, null); } })()""")
g.ev("skipTo(21*60 + 30)")   # Day 1 21:30
g.ev("goToDeck(4)"); g.step(5)
g.ev("(() => { const b = (DECKS[4].places||[]).find(p => p.id === playerBed()); const n = nearestOpen(cellPos(...b.at).x, cellPos(...b.at).z, player); player.obj.position.copy(cellPos(...n)); target.copy(player.obj.position).setY(.7); })()")
# as after Day 1: changed into the spare outfit that morning, none left
g.ev("(() => { const C = SHIP.clothes; C.clean = 0; C.changed = 1; C.kit = false; C.hamper = null; SHIP.player.carry.length = 0; })()")
g.ev(f"sleepGo({WAKE})"); g.secs(3)
log = []
def st(lbl):
    r = g.ev(r"""(() => ({ t: clockText(), tips: Object.keys(SHIP.device.tipsSeen).filter(k => /laund|clothes/.test(k)), card: (document.getElementById('devTip')||{}).hidden === false ? (document.getElementById('devTip').textContent||'').slice(0,140) : null,
       toast: (document.getElementById('toast')||{}).textContent.slice(0,160), goal: typeof IX_GOAL !== 'undefined' && IX_GOAL ? IX_GOAL.label : null, h: SHIP.clothes.hamper && SHIP.clothes.hamper.state + '@' + SHIP.clothes.hamper.at, clean: SHIP.clothes.clean, uni: uniformState(), said: Object.keys(SHIP.clothes.said) }))()""")
    print(lbl, r)
st('woke')
for i in range(6):
    g.secs(10); st(f'+{10*(i+1)}s')
g.snap(f'28-woke-{WAKE//60:02d}{WAKE%60:02d}')
g.ev("wardrobeUse()"); g.secs(2); st('wardrobe')
g.snap(f'28-hamper-{WAKE//60:02d}{WAKE%60:02d}')
g.ev("(() => { const w = washerList().find(m => washerBusyUntil(m.id) <= shipNow() && !washerBroken(m.id)); window.__w = w && w.id; washerUse(w, 'Washer'); })()"); g.secs(2); st('washer ' + str(g.ev('window.__w')))
for i in range(3): g.secs(20); st('later')
print(g.errors[:5])
