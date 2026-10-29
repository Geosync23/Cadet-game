# RV26: RB1 turn 3, pixel compare old vs new on decks other than cadet_test's Deck 4 start: busy scenes with full bodies.
# Usage: pix_rb.py OLD.html NEW.html OUTDIR   (cadet_test.py's Game harness; same steps in both builds)
import sys, os, json
OLD, NEW, OUT = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2]), sys.argv[3]; os.makedirs(OUT, exist_ok=True)
sys.argv = [sys.argv[0]]
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
SCENES = [('mess_dinner', 1 * 1440 + 18 * 60 + 20, 3), ('galley_bfast', 2 * 1440 + 7 * 60 + 30, 3), ('rec_d6', 5 * 1440 + 14 * 60 + 30, 7),
          ('bridge', 1 * 1440 + 10 * 60, 1), ('deck2_eve', 3 * 1440 + 20 * 60, 2), ('deck5', 2 * 1440 + 11 * 60, 5), ('deck4_night', 2 * 1440 + 22 * 60 + 30, 4)]
def run(path, tag):
    info = {}
    with sync_playwright() as pw:
        g = Game(pw, path, 390, 844)
        g.page.evaluate("s => { try { window.__sc(s); } catch (e) {} }", "SHIP.device && SHIP.device.settings && (SHIP.device.settings.tips = false)")
        for name, t, deck in SCENES:
            g.ev(f"skipTo({t}); goToDeck({deck})"); g.step(90)
            g.shot(f'{OUT}/{tag}_{name}.png')
            info[name] = g.ev("[renderer.info.render.calls, DECK_CREW.filter(a => a.h && a.h.full).length, DECK_CREW.length]")
            g.page.click('#rot'); g.step(30); g.shot(f'{OUT}/{tag}_{name}_rot.png'); g.page.click('#rot'); g.step(5)
        info['errors'] = [e for e in g.errors if 'pageerror' in e][:3]; g.close()
    return info
a = run(OLD, 'old'); b = run(NEW, 'new')
print('old', a); print('new', b)
bad = 0
for name, *_ in SCENES:
    for suf in ('', '_rot'):
        x = np.asarray(Image.open(f'{OUT}/old_{name}{suf}.png').convert('RGB')).astype(int); y = np.asarray(Image.open(f'{OUT}/new_{name}{suf}.png').convert('RGB')).astype(int)
        d = np.abs(x - y).max(axis=2); n = int((d > 0).sum()); bad += n
        print(f'{name + suf:22s} differing px {n:6d}  max {int(d.max())}')
print('PIX SAME' if bad == 0 else 'PIX DIFFER')
