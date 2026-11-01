# Starship Cadet: p5 retry probe (FX30 for lead 49, backlog P5-1, 0.99.6; a one-off targeted check, kept next to the others)
# The first "Follow the line" case (p5Stage, section 24k) when its first set-up can't be fair: another machine on the
# water line reads low as the p5 row opens, so caseSolve rejects the readings.
#   On the build as it is (P5_RETRY_ON off): the case is given up for good ('none'), as backlog P5-1 says.
#   On a copy with P5_RETRY_ON switched on: nothing is booked, the pump's condition is untouched, the same hour doesn't
#   try again, and once the other machine is put right a later ship hour stages the case (3-pump-1's seal, slot 29).
#   With the switch on, having learned p5 from a roll case still gives it up ('none').
#   (lead 49, RV31) With the switch on: an ordinary open job on the pump (a cause on no line, like its bearing) doesn't
#   hold the first case up: it stages at once and that job is dropped, as jobReserve does. A save stuck at 'none' by the
#   old rule (p5 not learned, no p5 case open) waits again once (case.p5.reset) and stages; 'none' after that stays;
#   a 'none' with p5 learned stays. Off: a stuck save stays 'none'.
# Run:  python3 p5retry_probe.py BUILD.html
import sys, json, re, os, pathlib
exec(open(__file__.replace('p5retry_probe.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
ok = True
def check(cond, msg):
    global ok
    print('ok  ' if cond else 'FAIL', msg)
    if not cond: ok = False
    return cond

PREP = r"""(() => {
  if (!SHIP.works) { if (shipNow() < WORKS_START) setShipNow(WORKS_START); worksInit(); }
  const out = {}, C = caseState(), W = SHIP.works;
  C.open = []; delete SHIP.flags['case.p5.first']; W.rank = 'senior'; W.tier = 3; W.tr = { t3: 15, m19: 17, m18: 18 }; W.tools = Object.assign({}, W.tools, { pipekit: [12, 0] });
  worksSay = () => {};
  W.op = { 18: ['p5'] }; setShipNow(17 * 1440 + 330); machinesNow();
  for (const x of ['water', 'heat', 'air'].flatMap(lineIds)) if (SHIP.machines[x]) { SHIP.machines[x].cond = 90; SHIP.machines[x].state = machineState(90); }
  SHIP.jobs = SHIP.jobs.filter(x => !(x.machine && lineOf(x.machine) && x.status !== 'done'));
  const m = machineById(P5_FIRST.machine), f = caseCauses(m).find(x => x.id === P5_FIRST.cause);
  P5_RETRY.h = -1; out.fairAt90 = p5Ready(m, f);
  // the first machine on the water line whose low reading makes the set-up unfair (a second drop)
  for (const x of lineIds('water')) { if (x === m.id || !SHIP.machines[x]) continue;
    const s = SHIP.machines[x]; s.cond = 20; s.state = machineState(20); P5_RETRY.h = -1;
    if (!p5Ready(m, f)) { out.bad = x; break; }
    s.cond = 90; s.state = machineState(90); }
  P5_RETRY.h = -1;
  out.pump0 = SHIP.machines[m.id].cond; out.jobs0 = SHIP.jobs.length;
  WORK_MECH.p5.open(ladderRow('p5'), 18);
  out.flag = flag('case.p5.first') === undefined ? null : flag('case.p5.first'); out.pump1 = SHIP.machines[m.id].cond;
  out.newJobs = SHIP.jobs.length - out.jobs0; out.held29 = SHIP.jobs.filter(j => j.reserved === 29 && !j.released).length;
  return out;
})()"""

LATER = r"""(() => {
  const out = {}, m = machineById(P5_FIRST.machine);
  p5Stage(); out.sameHour = flag('case.p5.first') === undefined ? null : flag('case.p5.first');
  setShipNow(shipNow() + 60); p5Stage(); out.stillBad = flag('case.p5.first') === undefined ? null : flag('case.p5.first');
  const s = SHIP.machines[__bad]; s.cond = 90; s.state = machineState(90);
  setShipNow(shipNow() + 60); p5Stage();
  const id = flag('case.p5.first'), c = id && caseById(id), j = c && caseJob(c);
  out.flag = id; out.machine = j && j.machine; out.cause = c && c.cause; out.reserved = j && j.reserved; out.wait = c && c.wait;
  out.pump = SHIP.machines[m.id].cond;
  return out;
})()"""

# a clean opening with the whole line at 90 (PREP without the low machine), then the extra cases
CLEAN = r"""(() => {
  const C = caseState(), W = SHIP.works, m = machineById(P5_FIRST.machine);
  C.open = []; for (const k of ['case.p5.first', 'case.p5.reset']) delete SHIP.flags[k]; W.tr = { t3: 15, m19: 17, m18: 18 };
  for (const x of ['water', 'heat', 'air'].flatMap(lineIds)) if (SHIP.machines[x]) { SHIP.machines[x].cond = 90; SHIP.machines[x].state = machineState(90); }
  SHIP.jobs = SHIP.jobs.filter(x => !(x.machine && lineOf(x.machine) && x.status !== 'done')); P5_RETRY.h = -1;
})"""
BEARING = r"""(() => {
  const m = machineById(P5_FIRST.machine), f = caseCauses(m).find(g => !g.line && g.part), t = shipNow(); if (!f) return { none: true };
  SHIP.jobs.push({ id: 'fx30-bearing', machine: m.id, deck: m.deck, kind: 'repair', urgency: 1, posted: t, found: t, claimedBy: null, parts: [f.part], status: 'open', cause: f.id });
  const sm = SHIP.machines[m.id]; sm.cond = 30; sm.state = machineState(30); MACH_REV++;   // the pump faulty with its bearing (RV31's case)
  // the dry run as it was in 6c14bc2 (the bearing job seen): lineShare reads the pump full, caseSolve 'answer'
  const old = (() => { const was = { cond: sm.cond, state: sm.state }; try { sm.cond = Math.min(sm.cond, 40); const j = { machine: m.id, cause: P5_FIRST.cause }, seed = machSeed('p5-first');
    const sus = [P5_FIRST.cause].concat(p5Pick(j, seed, 'T3', P5_FIRST.decoys)).map((x, i) => [schedU(seed, i, 893), x]).sort((a, b) => a[0] - b[0]).map(x => x[1]);
    return caseSolve(sus, p5Clues(j, P5_FIRST.cause, sus), 'T3', P5_FIRST.cause, 'p5').why || 'fair'; } finally { sm.cond = was.cond; sm.state = was.state; } })();
  setShipNow(shipNow() + 60); p5Stage();
  const id = flag('case.p5.first'), c = id && caseById(id), j = c && caseJob(c);
  return { cause: f.id, old, flag: id, machine: j && j.machine, kept: (SHIP.jobs.find(x => x.id === 'fx30-bearing') || {}).status || null, by: (SHIP.jobs.find(x => x.id === 'fx30-bearing') || {}).claimedBy || null };
})()"""
STUCK = r"""((learned) => {
  const W = SHIP.works; flagSet('case.p5.first', 'none'); if (learned) W.tr.p5 = 18; setShipNow(shipNow() + 60); P5_RETRY.h = -1; p5Stage();
  const out = { flag: flag('case.p5.first'), reset: flag('case.p5.reset') || null };
  const c = caseById(out.flag); out.machine = c && (caseJob(c) || {}).machine;
  if (!learned && c) { caseClose(c, 0); flagSet('case.p5.first', 'none'); setShipNow(shipNow() + 60); P5_RETRY.h = -1; p5Stage(); out.again = flag('case.p5.first'); }
  return out;
})"""
TRAINED = r"""(() => { delete SHIP.flags['case.p5.first']; caseState().open = []; SHIP.works.tr.p5 = 17; P5_RETRY.h = -1; setShipNow(shipNow() + 60); p5Stage(); return flag('case.p5.first'); })()"""

src = pathlib.Path(sys.argv[1]).read_text()
OFF = 'var P5_RETRY_ON = false;'
if OFF not in src: print('FAIL no P5_RETRY_ON switch line in this build'); sys.exit(1)
on = WORK / 'test' / f'_p5retry_on_{os.getpid()}.html'; on.parent.mkdir(parents=True, exist_ok=True); on.write_text(src.replace(OFF, 'var P5_RETRY_ON = true;', 1))
try:
  with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.step(3)
    A = g.ev(PREP); print('off:', A)
    check(A['fairAt90'] and A.get('bad'), f"set-up: fair with the line at 90, unfair with {A.get('bad')} low")
    check(A['flag'] == 'none', f"switch off: one failed set-up gives the first case up for good, as before: {A['flag']}")
    g.ev(f"({CLEAN})()"); S0 = g.ev(f"({STUCK})(false)")
    check(S0['flag'] == 'none' and S0['reset'] is None, f"switch off: a stuck save stays 'none': {S0}")
    g.close()
    g = Game(pw, str(on), 390, 844); g.step(3)
    B = g.ev(PREP); print('on: ', B)
    check(B['fairAt90'] and B.get('bad') == A.get('bad'), f"set-up: the same machine makes it unfair: {B.get('bad')}")
    check(B['flag'] is None and B['newJobs'] == 0 and B['held29'] == 0 and B['pump1'] == B['pump0'], f"switch on: not given up, nothing booked, the pump untouched: {B['flag']} {B['newJobs']} {B['pump0']}->{B['pump1']}")
    g.ev(f"window.__bad = {json.dumps(B['bad'])}")
    L = g.ev(LATER); print('on later:', L)
    check(L['sameHour'] is None and L['stillBad'] is None, f"switch on: waits while the line still reads wrong: {L['sameHour']} {L['stillBad']}")
    check(L['flag'] and L['flag'] != 'none' and L['machine'] == '3-pump-1' and L['cause'] == 'seal' and L['reserved'] == 29 and L['wait'] and L['pump'] <= 40,
          f"switch on: a later ship hour stages it: {L}")
    g.ev(f"({CLEAN})()"); Br = g.ev(BEARING); print('on bearing:', Br)
    check(Br.get('flag') and Br['flag'] != 'none' and Br.get('machine') == '3-pump-1' and Br.get('old') == 'answer' and not Br.get('kept'), f"switch on: an ordinary open job on the pump ({Br.get('cause')}, no line; the old dry run said {Br.get('old')}) doesn't hold the first case up; that job dropped as jobReserve does: {Br}")
    g.ev(f"({CLEAN})()"); S1 = g.ev(f"({STUCK})(false)"); print('on stuck save:', S1)
    check(S1['flag'] and S1['flag'] != 'none' and S1['machine'] == '3-pump-1' and S1['reset'] == 1, f"switch on: a save stuck at 'none' by the old rule waits again once and stages: {S1}")
    check(S1.get('again') == 'none', f"switch on: 'none' after the one reset stays: {S1.get('again')}")
    g.ev(f"({CLEAN})()"); S2 = g.ev(f"({STUCK})(true)"); print('on learned save:', S2)
    check(S2['flag'] == 'none' and S2['reset'] is None, f"switch on: a 'none' with p5 learned stays: {S2}")
    T = g.ev(TRAINED)
    check(T == 'none', f"switch on: learned p5 from a roll case, still given up: {T}")
    pe = [e for e in g.errors if e.startswith('pageerror')]
    check(not pe, f'no page errors: {pe}')
    g.close()
finally:
  on.unlink(missing_ok=True)
print('P5 RETRY PROBE OK' if ok else 'P5 RETRY PROBE FAILED')
sys.exit(0 if ok else 1)
