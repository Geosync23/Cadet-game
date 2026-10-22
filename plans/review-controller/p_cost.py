# RV2 probe: how many pick() raycasts the controller's ring search does per frame (turn 3), at phone size
import sys, json, pathlib, os
GAMEF = sys.argv[1]
sys.argv = [sys.argv[0]]
exec(open(os.path.join(os.path.dirname(GAMEF), 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
FAKEPAD = r"""
(() => {
  const mk = (i) => ({ index: i, id: 'Xbox Wireless Controller (STANDARD GAMEPAD Vendor: 045e Product: 0b13)', mapping: 'standard', connected: true, timestamp: 0, axes: [0, 0, 0, 0],
    buttons: Array.from({ length: 17 }, () => ({ pressed: false, touched: false, value: 0 })) });
  window.__pads = [null, null, null, null];
  Object.defineProperty(navigator, 'getGamepads', { value: () => window.__pads.slice(), configurable: true });
  window.__plug = i => { window.__pads[i] = mk(i); const e = new Event('gamepadconnected'); e.gamepad = window.__pads[i]; dispatchEvent(e); };
  window.__btn = (i, k, v) => { const b = window.__pads[i].buttons[k]; b.value = v; b.pressed = v > .5; b.touched = v > 0; };
})();
"""
INIT = INIT + FAKEPAD
SPOTS = r"""(() => { const out = []; const pl = padPlaces();
  let dense = null, empty = null;
  for (let j = 1; j < D - 1; j++) for (let i = 1; i < W - 1; i++) { if (!free(i, j)) continue; const c = cellPos(i, j);
    const n = pl.filter(([p, s]) => Math.hypot(s.x - c.x, s.z - c.z) <= 3.2).length;
    const it = ITEMS.filter(t => t.hit).length;
    if (!dense || n > dense[2]) dense = [i, j, n];
    if (n === 0 && (!empty)) empty = [i, j, 0]; }
  return { dense, empty, places: pl.length, deck: deckDef.num }; })()"""
with sync_playwright() as pw:
    g = Game(pw, GAMEF, 390, 844)
    g.ev("SHIP.device && SHIP.device.settings && (SHIP.device.settings.tips = false)"); g.step(10)
    g.ev("window.__pk = 0; { const o = pick; pick = function (a, b) { window.__pk++; return o(a, b); }; } 1")
    g.page.evaluate("window.__plug(0)"); g.step(2)
    g.page.evaluate("window.__btn(0, 1, 1)"); g.step(2); g.page.evaluate("window.__btn(0, 1, 0)"); g.step(2)
    print('used', g.ev("PAD.used"), 'ring', g.ev("!!PAD_PICK.ring"))
    sp = g.ev(SPOTS); print('spots', sp)
    for name, cell in [('start', None), ('dense', sp['dense']), ('empty', sp['empty'])]:
        if cell: g.ev(f"player.obj.position.copy(cellPos({cell[0]}, {cell[1]})); player.stop(); 1"); g.step(3)
        per = []
        for k in range(48):
            g.ev("window.__pk = 0"); g.step(1); per.append(g.ev("window.__pk"))
        raw = g.ev("padRaw().length"); L = g.ev("PAD_PICK.list.map(t => t.key)")
        print(f'{name}: picks per frame max {max(per)}, mean {sum(per)/len(per):.1f}, frames with any {sum(1 for x in per if x)}/48; raw {raw}; list {L[:8]}')
        print('   ', per)
    print('errors', [e for e in g.errors if 'error' in e][:3])
    g.close()
