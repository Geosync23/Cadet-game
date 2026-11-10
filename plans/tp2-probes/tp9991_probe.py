# Starship Cadet: TP2's probe for 0.99.91 piece A (backlog TP1-1; plans/patch-09991.md; TP9991_SD_ON).
# A shutdown booking must keep clear of your night shift. Day 23 is a night (21:00, its check-in arrow from 20:45):
# an hour at 20:00 runs to 21:00, past the arrow. Booked on Day 22 (so the target is Day 23), with the switch on
# (its own copy) and off (the build as given). Each part prints ok / FAIL; the last line says OK or FAILED.
# Run:  python3 plans/tp2-probes/tp9991_probe.py BUILD.html
import sys, json, pathlib
G = str(pathlib.Path(__file__).resolve().parents[2]) + '/'
exec(open(G + 'cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
ok = True
def check(cond, msg):
    global ok
    print('ok  ' if cond else 'FAIL', msg)
    if not cond: ok = False
    return cond

# set up a Senior Officer trained in shutdowns, a junction job needing one, on day `d` at 10:00 (target day d + 1)
SETUP = r"""(d => { introSkip(); SHIP.works = null; SHIP.jobs = []; setShipNow((d - 1) * 1440 + 600); machinesNow(); const W = worksInit(); W.tier = 3; W.rank = 'senior'; W.tr.m18 = 18;
  const id = jobReserve('6-junction-1', d, 600, 43, { tier: 3 }); sdMark(shipNow()); SD_UI.job = null; return id; })"""
PROBE = r"""(d => { const id = (""" + SETUP + r""")(d), out = { target: sdTarget(), night: p5nOf(d + 1), id };
  out.direct = !!sdBook(id, 1200, 'galley', []); sdData().book = [];                       // the booking's own check
  sdDraft(); SD_UI.at = 1200; sdDraft(); out.draft = SD_UI.at;                             // the draft's clamp
  SD_UI.at = 1140; sdAct('sd:hour', 1); out.stepUp = SD_UI.at;                              // the stepper, later from 19:00
  SD_UI.at = 1080; sdAct('sd:hour', 1); out.stepUp2 = SD_UI.at;                             // from 18:00
  sdAct('sd:quiet', 0); out.quiet = SD_UI.at;
  out.quietAll = []; for (let at = 480; at <= 1200; at += 60) out.quietAll.push([at, typeof sdHourOk === 'function' ? sdHourOk(d + 1, at) : null]);
  SD_UI.at = 1200; sdAct('sd:book', id); const b = sdData().book.find(x => x.job === id); out.booked = b ? b.at : null;   // the Book button with 20:00 drafted
  return out; })"""
# play the booking through: settle at 22:00 Day d, then Day d + 1 to 21:00; which sd:day: arrows are asked
PLAY = r"""(d => { const L = window.__ga = [], f = guideAsk; guideAsk = function (o) { if (o && /^sd:day:/.test(o.id)) L.push(o.id); return f.apply(this, arguments); };
  const B = (d - 1) * 1440; for (let t = shipNow(); t <= B + 1325; t += 5) { setShipNow(t); machinesNow(); worksCareerTick(t); }
  for (let t = B + 1440 + 360; t <= B + 1440 + 1260; t += 5) { setShipNow(t); machinesNow(); worksCareerTick(t); }
  return { set: (SHIP.works.sd.set[d + 1] || []).map(x => x.at), asked: [...new Set(L)] }; })"""

def run_on(path, d, play):
    with sync_playwright() as pw:
        g = Game(pw, path, 390, 844); g.step(3)
        g.ev('localStorage.clear()')
        r = g.ev(PROBE + f'({d})')
        if play: r['play'] = g.ev(PLAY + f'({d})')
        g.close() if hasattr(g, 'close') else None
        return r

src = pathlib.Path(sys.argv[1]).read_text()
OFF_LINE = 'const TP9991_SD_ON = false;'
on_path = None
if OFF_LINE in src:
    on_path = pathlib.Path(WORK) / 'test' / ('_tp9991_on_' + pathlib.Path(sys.argv[1]).name)
    on_path.write_text(src.replace(OFF_LINE, 'const TP9991_SD_ON = true;', 1))
else: print('note: no TP9991_SD_ON line (the build before it): the off runs only')

off = run_on(sys.argv[1], 22, True); print('off, Day 22 for Day 23:', json.dumps(off))
check(off['target'] == 23 and off['night'] and off['night']['from'] == 22 * 1440 + 1260, 'setup: target Day 23, a night from 21:00')
check(off['direct'] and off['booked'] == 1200 and 'sd:day:23:1200' in off['play']['asked'], 'off: 20:00 books and its arrow is asked, as in 0.99.9')
if on_path:
    on = run_on(str(on_path), 22, True); print('on, Day 22 for Day 23:', json.dumps(on))
    check(not on['direct'], 'on: sdBook refuses 20:00 on Day 23')
    check(on['draft'] == 1140, 'on: a drafted 20:00 moves to 19:00')
    check(on['stepUp'] == 1140 and on['stepUp2'] == 1140, 'on: Later hour stops at 19:00 (stays put from 19:00, 18:00 to 19:00)')
    check(on['quiet'] != 1200, 'on: Quietest hour never picks 20:00')
    check([a for a, k in on['quietAll'] if not k] == [1200], 'on: only 20:00 is out on Day 23')
    check(on['booked'] == 1140 and on['play']['set'] == [1140], 'on: the Book button with 20:00 drafted books 19:00')
    check('sd:day:23:1200' not in on['play']['asked'] and 'sd:day:23:1140' in on['play']['asked'], 'on: no sd:day:23:1200 arrow asked; 19:00\'s is')
    for d, name in [(20, 'Day 21, not a night'), (21, 'Day 22, a night from 22:45')]:
        r = run_on(str(on_path), d, False); print(f'on, {name}:', json.dumps({k: r[k] for k in ('direct', 'draft', 'booked')}))
        check(r['direct'] and r['draft'] == 1200 and r['booked'] == 1200, f'on: {name}: 20:00 books as before')
    on_path.unlink(missing_ok=True)
print('tp9991 probe: OK' if ok else 'tp9991 probe: FAILED')
sys.exit(0 if ok else 1)
