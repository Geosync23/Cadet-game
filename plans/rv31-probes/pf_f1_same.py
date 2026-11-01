# RV31: PF1's F1 (shipEffectsAt keeps fxFrom's answers on the hour's record). Run from the repo root:
#   python3 plans/rv31-probes/pf_f1_same.py BASE.html PF.html [DAYS]
# Both builds: a new game, skipped ship day by day (skipTo in 10-hour steps) to DAYS; at 07:30, 13:00 and 21:00 each day:
#   (PF) every deck x every recorded hour: shipEffectsAt(deck, h*60) equal (JSON) to a fresh fxFrom(deck, record);
#   (both) a fingerprint of the ship (machines, jobs, flags, crew state, the player's needs, R()'s seed) to compare.
import sys, json, hashlib
exec(open('cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
DAYS = int(sys.argv[3]) if len(sys.argv) > 3 else 10
CMP = r"""(() => { let n = 0, bad = 0, ex = null; const hs = [...MACH_HIST.keys()];
  for (let d = 1; d <= 7; d++) for (const h of hs) { n++; const a = JSON.stringify(shipEffectsAt(d, h * 60)), b = JSON.stringify(fxFrom(d, MACH_HIST.get(histHour(h * 60)) || null)); if (a !== b) { bad++; ex = ex || [d, h, a.slice(0, 120), b.slice(0, 120)]; } }
  return [n, bad, ex]; })()"""
FP = r"""(() => { const rep = (k, v) => v instanceof Map ? [...v] : v instanceof Set ? [...v] : v;
  const s = JSON.stringify([SHIP.time, SHIP.machines, SHIP.jobs, SHIP.flags, typeof crewState === 'function' ? crewState(SHIP.time.day) : null, SHIP.player && SHIP.player.needs, seed, MACH_REV], rep);
  return s; })()"""
def run(path, cmp):
    out, checks = [], [0, 0, None]
    with sync_playwright() as pw:
        g = Game(pw, path, 390, 844); g.step(3); g.ev("newGameStart(false)")
        for d in range(1, DAYS + 1):
            for m in (450, 780, 1260):
                g.ev(f"(() => {{ const end = {d - 1} * 1440 + {m}; while (shipNow() < end) skipTo(Math.min(end, shipNow() + 600)); }})()")
                fp = g.ev(FP); out.append((d, m, hashlib.sha1(fp.encode()).hexdigest()[:12]))
                if cmp:
                    c = g.ev(CMP); checks[0] += c[0]; checks[1] += c[1]; checks[2] = checks[2] or c[2]
        errs = [e for e in g.errors if e.startswith('pageerror')]; g.close()
    return out, checks, errs
A, _, ea = run(sys.argv[1], False)
B, ck, eb = run(sys.argv[2], True)
diff = [(a, b) for a, b in zip(A, B) if a != b]
print('fingerprints', len(A), 'differ', len(diff), diff[:3])
print('F1 checks', ck[0], 'mismatches', ck[1], ck[2])
print('page errors', ea[:2], eb[:2])
print('PF F1 SAME OK' if not diff and not ck[1] and ck[0] and not ea and not eb else 'PF F1 SAME FAILED')
