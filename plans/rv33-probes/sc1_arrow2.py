import sys
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
path, tag = sys.argv[1], sys.argv[2]
with sync_playwright() as pw:
    g = Game(pw, path, w=390, h=844)
    g.ev('localStorage.clear()'); g.ev("newGameStart(true)"); g.step(5)
    g.page.fill('form input[maxlength="24"]', 'Sam'); g.page.locator('form button').first.click(); g.step(10)
    g.ev("introSkip()"); g.step(3)
    g.ev("socInit(); for (const id of ['tomas','pell','torres-zeke','saad-amira','kovac-zainab','brennan','rina','halloran-emeka']) if (SOC.idx.has(id)) { relAdd(id, 'talk', 60); SHIP.rel[id].met = 0; }")
    out = g.ev("""(() => { const res = [];
      for (let d = 9; d <= 22; d++) { const ready = {}, shown = {};
        for (let m = 7*60; m < 23*60; m += 5) { const t = (d-1)*1440 + m; setShipNow(t); storyArrows(t);
          const live = new Set(guideLive(t).filter(e => e.id.startsWith('story:word:')).map(e => e.id.slice(11)));
          for (const id of storyIdx().beats.keys()) { const p = socP(id); if (!p) continue; if (momentReady(p, t)) ready[id] = (ready[id]||0) + 1; if (live.has(id)) shown[id] = (shown[id]||0) + 1; } }
        for (const id of Object.keys(ready)) res.push('Day ' + d + ' ' + id + ': ready ' + ready[id]*5 + ' min, arrow ' + (shown[id]||0)*5 + ' min'); }
      return res.join('\\n'); })()""")
    print('\n'.join(tag + ' ' + l for l in out.split('\n')))
