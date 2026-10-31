# RV30 probe (0.99.5 round, puzzle_check "p5's first ... staged none"): puzzle_check's P5FIRST set-up, then the jobs on 3-pump-1
# just before p5 opens, and which p5Stage condition says 'none'. Usage: p5_first.py WORKTREE BUILD
import sys, os
wt = sys.argv[1]; os.chdir(wt)
exec(open('cadet_test.py').read().split('a, shots = run(')[0])
with sync_playwright() as pw:
    g = Game(pw, sys.argv[2], 390, 844); g.step(3)
    import re as _re; ps = open('puzzle_check.py').read(); SETUP = _re.search(r'^SETUP = r"""(.*?)"""', ps, _re.S | _re.M).group(1); g.ev(SETUP)   # puzzle_check's own set-up first
    print(g.ev("""(() => { const C = caseState(), W = SHIP.works;
      C.open = []; delete SHIP.flags['case.p5.first']; W.rank = 'senior'; W.tier = 3; W.tr = { t3: 15, m19: 17, m18: 18 }; W.tools = Object.assign({}, W.tools, { pipekit: [12, 0] });
      for (const x of ['water', 'heat', 'air'].flatMap(lineIds)) if (SHIP.machines[x]) { SHIP.machines[x].cond = 90; SHIP.machines[x].state = machineState(90); }
      SHIP.jobs = SHIP.jobs.filter(x => !(x.machine && lineOf(x.machine) && x.status !== 'done'));
      W.op = { 18: ['p5'] }; setShipNow(17 * 1440 + 330); machinesNow();
      const m = machineById(P5_FIRST.machine), f = m && caseCauses(m).find(x => x.id === P5_FIRST.cause);
      const js = SHIP.jobs.filter(j => j.machine === m.id && j.status !== 'done').map(j => ({ id: j.id, kind: j.kind, claimedBy: j.claimedBy, case: j.case || null, reserved: j.reserved || null, train: j.train || null, cause: j.cause || null }));
      return JSON.stringify({ first: P5_FIRST, f: !!f, line: !!(f && p5Line(m, f)), trp5: W.tr.p5, jobs: js, scan: typeof fixScanMachine === 'function' ? [5, 6, 12, 18].map(d => [d, fixScanMachine(d)]) : null, reservedAll: SHIP.jobs.filter(j => j.reserved && j.status !== 'done').map(j => [j.id, j.reserved, j.train || null]),
        stage: (() => { const cs = caseSolve, got = []; caseSolve = (...a) => { const r = cs(...a); got.push({ sus: a[0], nclues: a[1].length, band: a[2], why: r.why || null, fewest: r.fewest, clues: a[1].map(k => [k.src && k.src.m, k.src && k.src.flow, (k.kills || []).slice()]) }); return r; };
          const mo = machineById(P5_FIRST.machine); W.op = { 18: ['p5'] }; try { WORK_MECH.p5.open(ladderRow('p5'), 18); } finally { caseSolve = cs; }
          return { flag: flag('case.p5.first'), solve: got, jobMins: (() => { const j = SHIP.jobs.find(x => x.machine === mo.id && x.train === 'p5'); return j && typeof jobMins === 'function' ? jobMins(j) : null; })() }; })() }); })()"""))
    g.close()
