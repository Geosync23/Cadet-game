# RV31: tries to break FX30's P5_RETRY_ON (backlog P5-1). Run from the repo root:
#   python3 plans/rv31-probes/p5retry_break.py OFF.html ON.html
# A: the line stays low for 3 ship days (3-recycler-1 forced low every hour): never given up, nothing booked, and each
#    p5Stage call leaves SHIP.machines, SHIP.jobs, the flags and R()'s seed exactly as they were. Then fixed: staged.
# B: a reload mid-wait (a real save, page reloaded without ?nosave): still waiting, then staged after the fix.
# C: the pump has an ordinary unclaimed 'bearing' fault job open (a cause on no line): OFF vs ON.
# D: a save from before with case.p5.first 'none' stays 'none' (the flag is read first).
import sys, json, os, pathlib
exec(open('cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
OFFB, ONB = sys.argv[1], sys.argv[2]
PREP = r"""(() => {
  if (!SHIP.works) { if (shipNow() < WORKS_START) setShipNow(WORKS_START); worksInit(); }
  const C = caseState(), W = SHIP.works;
  C.open = []; delete SHIP.flags['case.p5.first']; W.rank = 'senior'; W.tier = 3; W.tr = { t3: 15, m19: 17, m18: 18 }; W.tools = Object.assign({}, W.tools, { pipekit: [12, 0] });
  worksSay = () => {}; W.op = { 18: ['p5'] }; setShipNow(17 * 1440 + 330); machinesNow();
  for (const x of ['water', 'heat', 'air'].flatMap(lineIds)) if (SHIP.machines[x]) { SHIP.machines[x].cond = 90; SHIP.machines[x].state = machineState(90); }
  SHIP.jobs = SHIP.jobs.filter(x => !(x.machine && lineOf(x.machine) && x.status !== 'done'));
  window.__low = () => { const s = SHIP.machines['3-recycler-1']; s.cond = 20; s.state = machineState(20); };
  window.__fix = () => { const s = SHIP.machines['3-recycler-1']; s.cond = 90; s.state = machineState(90); };
  window.__fl = () => { const v = flag('case.p5.first'); return v === undefined ? null : v; };
  return true; })()"""
STAY = r"""(() => {
  const bad = []; let calls = 0, ready = 0;
  const real = caseSolve; caseSolve = (...a) => { ready++; return real(...a); };
  for (let h = 0; h < 72; h++) {
    setShipNow(17 * 1440 + 330 + h * 60); machinesNow(); __low();
    for (const mm of [0, 1, 30]) {
      setShipNow(17 * 1440 + 330 + h * 60 + mm); machinesNow(); __low();   // the hour's catch-up first, then the line held low at the try
      const a = JSON.stringify([SHIP.machines, SHIP.jobs, SHIP.flags, seed, caseState()]);
      if (mm === 0) WORK_MECH.p5.open(ladderRow('p5'), 18); else p5Stage(); calls++;
      const b = JSON.stringify([SHIP.machines, SHIP.jobs, SHIP.flags, seed, caseState()]);
      if (a !== b) bad.push(h + ':' + mm);
      if (__fl() !== null) bad.push('flag ' + __fl() + ' at ' + h);
    }
  }
  caseSolve = real;
  return { calls, ready, bad: bad.slice(0, 5), nbad: bad.length, flag: __fl(), held29: SHIP.jobs.filter(j => j.reserved === 29).length };
})()"""
FIXED = r"""(() => { __fix(); setShipNow(shipNow() + 60); p5Stage(); const id = __fl(), c = id && caseById(id), j = c && caseJob(c);
  return { flag: id, machine: j && j.machine, cause: c && c.cause, reserved: j && j.reserved, pump: SHIP.machines['3-pump-1'].cond }; })()"""
ok = True
def check(c, m):
    global ok
    print('ok  ' if c else 'FAIL', m); ok = ok and bool(c)
def reload(g, nosave):
    g.page.goto('file://' + str(g.tmp) + ('?nosave&debug' if nosave else '?debug'))
    g.page.wait_for_function('window.__sc !== undefined || window.__err', timeout=60000); g.ev(SKIP_SWITCH)
src = pathlib.Path(ONB).read_text()
with sync_playwright() as pw:
    # A
    g = Game(pw, ONB, 390, 844); g.step(3); g.ev(PREP)
    A = g.ev(STAY); print('A', A)
    check(A['nbad'] == 0 and A['flag'] is None and A['held29'] == 0, 'A: 3 days of a low line: waits, books nothing, each call leaves machines/jobs/flags/seed/cases as they were')
    check(A['ready'] <= 73, f"A: at most one dry run (caseSolve) a ship hour: {A['ready']} for {A['calls']} calls over 73 clock hours")
    F = g.ev(FIXED); print('A fixed', F)
    check(F['machine'] == '3-pump-1' and F['cause'] == 'seal' and F['reserved'] == 29, 'A: after the fix, a later hour stages it')
    g.close()
    # B: reload mid-wait
    g = Game(pw, ONB, 390, 844); reload(g, False); g.ev('localStorage.clear()'); reload(g, False); g.ev('newGameStart(false)'); g.step(3); g.ev(PREP)
    print('B save', g.ev("(() => { __low(); setShipNow(shipNow() + 60); p5Stage(); saveGame(); return [__fl(), SAVE_KEY, (localStorage.getItem(SAVE_KEY) || '').length, NOSAVE, SLOT_HOLD, typeof titleHold === 'function' && titleHold()]; })()"))
    t0 = g.ev('shipNow()'); reload(g, False); g.step(3)
    B = g.ev("(() => ({ t: shipNow(), flag: (flag('case.p5.first') === undefined ? null : flag('case.p5.first')), h: P5_RETRY.h, pump: SHIP.machines['3-pump-1'].cond, works: !!SHIP.works }))()")
    print('B after reload', B, 'saved at', t0)
    check(B['works'] and B['flag'] is None and B['pump'] > 80 and abs(B['t'] - t0) < 5, 'B: after a reload mid-wait: same time, still waiting, the pump not left at 40 (normal wear only)')
    g.ev(PREP.replace("delete SHIP.flags['case.p5.first'];", '').replace('setShipNow(17 * 1440 + 330); machinesNow();', 'machinesNow();').replace("for (const x of ['water', 'heat', 'air'].flatMap(lineIds))", "for (const x of [])"))
    g.ev("(() => { __low(); p5Stage(); setShipNow(shipNow() + 60); p5Stage(); })()")
    B2 = g.ev(FIXED); print('B fixed', B2)
    check(B2['machine'] == '3-pump-1' and B2['reserved'] == 29, 'B: after the reload and the fix, it stages')
    g.page.evaluate('localStorage.clear()'); g.close()
    # C: an ordinary unclaimed bearing job on the pump, line fine otherwise
    C = {}
    for name, b in (('off', OFFB), ('on', ONB)):
        g = Game(pw, b, 390, 844); g.step(3); g.ev(PREP)
        C[name] = g.ev(r"""(() => { const m = machineById('3-pump-1'); SHIP.jobs.push({ id: 'rv31b', machine: m.id, deck: m.deck, kind: 'repair', urgency: 1, posted: shipNow(), found: shipNow(), until: shipNow() + 1440, claimedBy: null, cause: 'bearing', parts: ['bearing'], status: 'open' });
          const s = SHIP.machines[m.id]; s.cond = 45; s.state = machineState(45);
          WORK_MECH.p5.open(ladderRow('p5'), 18); return [__fl(), SHIP.jobs.some(j => j.id === 'rv31b')]; })()""")
        g.close()
    print('C', C)
    check(True, f"C (note only): OFF {C['off']}  ON {C['on']}")
    # D
    g = Game(pw, ONB, 390, 844); g.step(3); g.ev(PREP)
    D = g.ev("(() => { flagSet('case.p5.first', 'none'); __low(); setShipNow(shipNow() + 60); p5Stage(); const a = [__fl(), flag('case.p5.reset')];"
             " flagSet('case.p5.first', 'none'); setShipNow(shipNow() + 60); __fix(); p5Stage(); return a.concat([__fl()]); })()")
    # 042f57e on (lead 49's ask): a save given up by the old rule waits again once (case.p5.reset), the line low: still waiting; 'none' a second time stays
    check(D == [None, 1, 'none'], f"D: an old 'none' save waits again once (line low: still waiting); 'none' after the reset stays: {D}")
    pe = [e for e in g.errors if e.startswith('pageerror')]; check(not pe, f'no page errors {pe}'); g.close()
print('RV31 P5 BREAK OK' if ok else 'RV31 P5 BREAK FAILED')
