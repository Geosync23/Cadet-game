# RV8 probe: "Turn it in at the job board" pin, four camera turns, a real click on the pin icon (and on the anchor point);
# logs which tap path ran. p_board.py GAME CT_DIR W H [crewoff]
import sys, json
exec(open(sys.argv[2] + '/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
W, H = int(sys.argv[3]), int(sys.argv[4])
TURN = r"""(() => { actEnd(true); for (const k of NEED_KEYS) SHIP.player.needs[k] = 100; needsT = null; NEED_GOAL = null; clearGoal(); const b = document.getElementById('ixBoard'); if (b) b.hidden = true;
  if (deckDef.num !== 5) goToDeck(5); setShipNow(1440 * 2 + 10 * 60); const c = cellPos(...placeById('5-jobboard-1').at); player.obj.position.set(c.x + 1, 0, c.z + 2.5); player.stop();
  setGoal({ deck: 5, item: /job board/i, room: 'w', label: 'Turn it in at the job board' }); })()"""
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], W, H); g.step(5)
    g.ev("(() => { if (SHIP.device && SHIP.device.settings) SHIP.device.settings.tips = false; const t = document.getElementById('devTip'); if (t) t.hidden = true; })()")
    if len(sys.argv) > 5: g.page.click('#crew'); g.step(5)
    g.ev("""(() => { window.__l = []; for (const n of ['playerTap', 'playerFloorTap', 'ixGoalTap', 'ixPinTap']) { if (typeof window[n] !== 'function') continue; const f = window[n]; window[n] = function () { const r = f.apply(this, arguments); __l.push(n + (n === 'playerTap' ? ':' + arguments[0].t : '') + '=' + r); return r; }; } })()""")
    for mode in ('icon', 'anchor'):
        for rot in range(4):
            g.ev(TURN); g.step(80)
            p = g.ev("""(() => { const el = document.getElementById('ixGoal'), pin = el.children[1], r = pin.getBoundingClientRect(), m = (el.style.transform.match(/translate\\(([-\\d.]+)px, ?([-\\d.]+)px\\)/) || []).slice(1).map(Number);
              return el.hidden ? null : { on: pin.style.display !== 'none', tap: el.classList.contains('tap'), icon: [r.left + r.width / 2, r.top + r.height / 2], anchor: m }; })()""")
            if not p or not p['on']: print(f'  {mode} turn {rot}: pin not on screen', p); g.page.click('#rot'); g.step(30); continue
            x, y = p[mode]
            at = g.ev(f"(e => e && (e.className || e.id || e.tagName))(document.elementFromPoint({x}, {y}))")
            g.ev("__l.length = 0"); g.page.mouse.click(x, y); opened = False
            for _ in range(40):
                g.step(10)
                if g.ev("!document.getElementById('ixBoard').hidden"): opened = True; break
            print(f'  {mode} turn {rot}: tap-class {p["tap"]} at {[round(x), round(y)]} on {at!r} -> opened {opened}; calls {g.ev("__l.slice(0, 6)")}')
            g.page.click('#rot'); g.step(30)
    print('errors', g.errors[:3]); g.close()
