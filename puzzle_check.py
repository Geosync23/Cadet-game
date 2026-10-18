# Starship Cadet: puzzle check (keep in the repo, next to machine_check.py)
# Checks the head-scratchers (section 24k, seat H; plans/mechanics/case-engine.html on claude/p5-design):
#   the device's chips block (0.55.0): big toggles (44px+), crossed out while on is false, aria-pressed, a tap runs its
#   action; devChips falls back to a buttons block with "✕ " on the crossed ones when the skin has no chips
# Setup and environment as for cadet_test.py.
# Run:  python3 puzzle_check.py BUILD.html
import sys, json
exec(open(__file__.replace('puzzle_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

ok = True
def check(cond, msg):
    global ok
    if not cond: ok = False; print('FAIL', msg)
    return cond

# a stand-in app with a chips block (the case engine's suspects), drawn through the real skin
CHIPS = r"""(() => {
  window.__tap = [];
  deviceApp({ id: 'chiptest', title: 'Chips test', order: 99, hidden: () => true,
    view: () => ({ title: 'Chips test', blocks: [devChips([{ label: 'Door seal', on: false, action: { app: 'chiptest', do: 'tap', arg: 'seal' } },
      { label: 'Drain valve', on: true, action: { app: 'chiptest', do: 'tap', arg: 'valve' } }, { label: 'Pump', action: { app: 'chiptest', do: 'tap', arg: 'pump' } }])] }),
    act: (v, a) => { __tap.push(v + ':' + a); } });
  deviceShow('chiptest');
  const b = document.getElementById('devBody'), cs = [...b.querySelectorAll('.chips .chip')];
  const out = { n: cs.length, labels: cs.map(c => c.textContent), pressed: cs.map(c => c.getAttribute('aria-pressed')),
    off: cs.map(c => c.classList.contains('off')), strike: cs.map(c => getComputedStyle(c).textDecorationLine),
    h: cs.map(c => Math.round(c.getBoundingClientRect().height)), w: cs.map(c => Math.round(c.getBoundingClientRect().width)) };
  cs[0].click(); out.tap = __tap.slice();
  // an older skin without chips: the same toggles as buttons, "✕ " on the crossed ones
  const has = DEVICE_SKIN.has; DEVICE_SKIN.has = () => false; DEV.app = 'home'; deviceShow('chiptest');
  const bs = [...b.querySelectorAll('.btns .act')]; out.fb = bs.map(x => x.textContent); out.fbChips = b.querySelectorAll('.chips').length;
  bs[1].click(); out.fbTap = __tap.slice(1);
  DEVICE_SKIN.has = has; deviceShow('home'); deviceClose();
  return out;
})()"""

def run(path):
    with sync_playwright() as pw:
        g = Game(pw, path, 390, 844)
        g.step(3)
        r = g.ev(CHIPS)
        print('chips:', r)
        check(r['n'] == 3 and r['labels'] == ['Door seal', 'Drain valve', 'Pump'], f'a chip per item: {r["labels"]}')
        check(r['pressed'] == ['false', 'true', 'true'] and r['off'] == [True, False, False], f'crossed out only while on is false: {r["pressed"]} {r["off"]}')
        check('line-through' in r['strike'][0] and 'line-through' not in r['strike'][1], f'a crossed chip is struck through: {r["strike"]}')
        check(min(r['h']) >= 44 and min(r['w']) >= 44, f'chips are big toggles (44px+): {r["h"]} {r["w"]}')
        check(r['tap'] == ['tap:seal'], f'a tap runs the chip\'s action: {r["tap"]}')
        check(r['fb'] == ['✕ Door seal', 'Drain valve', 'Pump'] and r['fbChips'] == 0, f'no chips in the skin: buttons with "✕ ": {r["fb"]}')
        check(r['fbTap'] == ['tap:valve'], f'the fallback buttons run the same actions: {r["fbTap"]}')
        errs = g.ev("DEV.errors.slice()")
        pe = [e for e in g.errors if e.startswith('pageerror')]
        check(not errs and not pe, f'no errors: {errs} {pe}')
        g.close()

run(sys.argv[1])
print('PUZZLE CHECK OK' if ok else 'PUZZLE CHECK FAILED')
sys.exit(0 if ok else 1)
