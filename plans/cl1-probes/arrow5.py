import sys, os
os.chdir('/home/user/Cadet-game')
exec(open('cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
G = "(()=>{const g=IX_GOAL; return JSON.stringify({t:clockText(), deck:deckDef.num, goal:g&&{deck:g.deck,room:g.room,label:g.label,cl:g.cl997,tj:g.tj}, rate:CL997_RATE, toast:(document.getElementById('toast')||{}).textContent});})()"
with sync_playwright() as pw:
    g=Game(pw,sys.argv[1], w=390, h=844)
    def at(day, mn, deck=None):
        g.ev(f"(()=>{{ skipTo(({day}-1)*1440+{mn}); {'goToDeck(%d);'%deck if deck else ''} EV_MIN=-1; }})()"); g.step(40)
        print(day, mn, g.ev(G))
    at(5, 925, 5); at(5, 932); at(5, 960)
    g.ev("goToDeck(7)"); g.step(5)
    g.ev("(() => { const M = DECKS[7].map, c = []; for (let j = 0; j < M.length; j++) for (let i = 0; i < M[j].length; i++) if (M[j][i] === 'A') c.push([i, j]); const t = cellPos(...c[Math.floor(c.length / 2)]); player.obj.position.set(t.x, 0, t.z); EV_MIN=-1; })()"); g.step(10)
    at(5, 966)
    m0=g.ev("shipNow()"); g.step(300); m1=g.ev("shipNow()"); print('ship min per 10 real s in auditorium', round(m1-m0,2), g.ev(G))
    g.shot('/tmp/claude-0/sp/addr.png')
    print(g.errors[:5]); g.close()
