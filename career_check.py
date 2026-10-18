# Starship Cadet: career check (keep in the repo, next to cadet_test.py and the other checks)
# Checks Pillar 5's Works career, section 24 core (the Works career engineer, 0.44.x; plans/mechanics/foundation.html
# "For the builder · tests"), on paper: each run steps ship hours, calling the game's own functions at the hours they'd
# run (machinesNow, worksTick: the ladder each hour, the training each minute), with no walking; the player takes jobs
# off the real board with claimJob / jobStepDone / turnInJob.
#   (a) Step 1 as built: with no mechanic sub-block in the build, no row ever opens (Days 2-14), nothing trains, and
#       the Works app stays hidden until Day 1's shift has ended
#   (b) a steady player (the board's top job each hour of the shift, each trained mechanic used once a workday, the drill
#       and the inspection attended), with every row given a stand-in sub-block: the ladder opens as the table (each
#       row on its day), never more than one big and one small on a workday, nothing on Days 6-7; training: the
#       ask (an appointment and Mail), the meeting, the teacher's job (done by them), then yours, then trained; tools
#       given; "Relied on" by the end of Day 8 and the test job on Day 9
#   (c) a very busy player (every job on the board, every hour, weekends too) never reaches "Relied on" before Day 5
#   (d) a lazy player (one job a workday, misses the first ask of each training, uses things every other workday):
#       each row later, none lost
#   (e) reputation bands from xp, careerSpeed's words (skillWord), tools and their wear, missed shifts and abandoned jobs
#   (f) the save: worksClean round trip mid-training, junk, a real reload mid-training (saving on), an old save
#       loading as Tier 1 with nothing trained and the ladder opening from its day; ship.works under 3 KB by Day 30
#   (g) the whole steady run twice, identical
# Not yet (waiting for section 17's 17.2, seat S): reserved-rank jobs never taken below their rank, crew or you.
# Setup and environment as for cadet_test.py.
# Run:  python3 career_check.py BUILD.html
import sys, json, os, re, pathlib
exec(open(__file__.replace('career_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

ok = True
def fail(msg):
    global ok
    ok = False
    print('FAIL', msg)
def check(cond, msg):
    if not cond: fail(msg)
    return cond

# one run on paper. plan: 'none' (no sub-blocks), 'steady', 'busy', 'lazy'. Returns the day-by-day story.
PAPER = r"""(({ plan, days }) => {
  const t0 = (SHIP_START.day - 1) * 1440 + SHIP_START.min;
  SHIP.works = null; SHIP.occasions.length = 0; SHIP.notes = []; SHIP.flags = {}; SHIP.jobs = []; SHIP.mail = []; SHIP.rep = null;
  JOBS_ON = true; MACH_HOUR = null; MACH_SEEN = -1; WORKS_TICK.m = WORKS_TICK.h = -1;
  for (const k in WORK_MECH) delete WORK_MECH[k];
  if (plan !== 'none') for (const r of CAREER_LADDER) WORK_MECH[r.id] = r.id === 't2' ? { noJob: true } : { reserve: (d, at, slot, o) => jobReserve('washer', d, at, slot, o) };   // stand-ins: the default training job
  const at = t => { setShipNow(t); machinesNow(); };
  const days_ = [], trained = {}, asks = {}, teach = {}, mails = [], band = {}, seen = { meet: 0, watch: 0, do: 0 }, bad = [];
  const stop = [onSim('trained', n => { trained[n.mech] = Math.floor(n.t / 1440) + 1; })];
  const doJob = id => { if (!claimJob(id)) return false; const j = SHIP.jobs.find(x => x.id === id);
    const cs = SHIP.works && SHIP.works.cases && (SHIP.works.cases.open || []).find(c => c.job === id);   // a head-scratcher (24k): call it right first
    if (cs && typeof caseCall === 'function') caseCall(cs.id, cs.cause);
    jobStops(j).forEach((s, k) => jobStepDone(id, k)); return turnInJob(id); };
  const lazySkip = new Set();                            // the lazy player misses each training's first ask
  let firstJob = null;
  for (let d = 1; d <= days; d++) {
    let jobs = 0, used = [];
    const work = playerShiftOn(d), wd = weekday(d);
    for (let h = 6; h <= 22; h++) {
      const t = (d - 1) * 1440 + h * 60; at(t);
      if (plan === 'none' && h === 18) { worksCareerTick(t); continue; }
      worksCareerTick(t);
      if (typeof DIALOGUE !== 'undefined' && DIALOGUE && typeof dialogueEnd === 'function') dialogueEnd(true);   // the player reads it through (a meeting on screen holds the training)
      const W = SHIP.works, c = W && W.cur;
      if (c && c.mail && !mails.includes(c.by + ': ' + c.mail)) mails.push(c.by + ': ' + c.mail);
      // the training: be there for the meeting, watch, do your one
      if (c && c.st === 'meet') { const r = SHIP.occasions.find(x => x.key === c.occ);
        if (r) { asks[c.id] = asks[c.id] || []; if (!asks[c.id].includes(d)) asks[c.id].push(d); }
        if (r && t >= r.at && t < r.at + r.len + 60) {
          if (plan === 'lazy' && !lazySkip.has(c.id)) { lazySkip.add(c.id); }
          else { r.met = true; seen.meet++; }
        }
        if (r && t >= r.at + r.len) { occasionsTick(t, true); }
        worksCareerTick(t + 1);
      }
      const c2 = W && W.cur;
      if (c2 && c2.st === 'watch') { c2.w = TRAIN_WATCH; seen.watch++; worksCareerTick(t + 2); const j = SHIP.jobs.find(x => x.id !== c2.j && x.train === c2.id && x.status === 'done');
        teach[c2.id] = teach[c2.id] || {}; const dj = SHIP.jobs.filter(x => x.train === c2.id && x.status === 'done').pop(); if (dj) teach[c2.id].by = dj.doneBy; }
      const c3 = SHIP.works && SHIP.works.cur;
      if (c3 && c3.st === 'do' && work && h >= 8 && h < 17) { seen.do++; if (!myJob() && doJob(c3.j)) { jobs++; (teach[c3.id] = teach[c3.id] || {}).you = (SHIP.jobs.find(x => x.id === c3.j) || {}).doneBy; } worksCareerTick(t + 3); }
      // the player's own work
      const shift = work && h >= 8 && h < 17;
      if (plan === 'steady' && shift && !myJob()) { const x = openJobs('you')[0]; if (x && doJob(x.id)) { jobs++; if (!firstJob) firstJob = d; } }
      if (plan === 'busy') for (let k = 0; k < 3 && !myJob(); k++) { const x = openJobs('you')[0]; if (x && doJob(x.id)) jobs++; else break; }
      if (plan === 'lazy' && shift && jobs === 0 && h === 10 && !myJob()) { const x = openJobs('you')[0]; if (x && doJob(x.id)) jobs++; }
      // using what you're trained in (a sub-block calls worksUse); the drill and the inspection, attended
      if (SHIP.works && work && h === 14 && plan !== 'none' && (plan !== 'lazy' || d % 2 === 0))
        for (const r of CAREER_LADDER) if (r.size === 'big' && SHIP.works.tr[r.id] !== undefined && r.id !== 't2') { worksUse(r.id); used.push(r.id); }
      if (SHIP.works && plan !== 'none' && (plan !== 'lazy' || d % 2 === 0)) for (const r of CAREER_LADDER) if (r.fixed && h * 60 <= r.fixed.at && r.fixed.at < h * 60 + 60 && worksOpened().has(r.id) && weekday(d) + 1 === r.fixed.wd) { worksUse(r.id); used.push(r.id); }
      if (SHIP.works && plan !== 'none' && h === 16 && work && d >= (plan === 'lazy' ? 9 : 5)) flagSet('works.oily', d);   // an oily job turned in (the uniform's sub-block will say)
      if (SHIP.works && SHIP.works.tr.p3 === undefined && worksOpened().has('p3') && h === 15) { worksUse('p3'); used.push('p3'); }
      if (SHIP.works && SHIP.works.tr.m2 === undefined && worksOpened().has('m2') && h === 16) { worksUse('m2'); used.push('m2'); }
    }
    const W = SHIP.works;
    if (W) band[d] = worksBand();
    days_.push({ d, wd, work, jobs, op: W ? (W.op[d] || []) : [], xp: W ? Math.round(W.xp) : null, band: W ? worksBand() : null, cur: W && W.cur ? W.cur.id + ':' + W.cur.st : null, used });
  }
  stop.forEach(f => f());
  const W = SHIP.works;
  const occ = SHIP.occasions.filter(r => /^works\./.test(r.id)).map(r => ({ id: r.id, day: Math.floor(r.at / 1440) + 1, at: hhmm(r.at % 1440), by: r.by, status: r.status }));
  return { days: days_, trained, asks, teach, seen, occ, firstJob, mail: mails,
    works: W ? JSON.parse(JSON.stringify(W)) : null, size: W ? JSON.stringify(W).length : 0, head: (worksRecordHead() || { text: null }).text, locker: worksLockerText(),
    view: W ? ['training', 'log', 'tools'].map(tab => { WORKS_TAB = tab; return worksView().blocks.filter(b => b.kind !== 'buttons').map(b => b.text || (b.rows || []).map(r => r.text + ' (' + r.sub + ')').join('; ')).join(' | '); }) : null };
})"""

LADDER = {'m1': 2, 'm4': 3, 'm3d': 3, 'm5': 4, 'm3i': 4, 'm7': 5, 'p3': 5, 'm6': 8, 'm2': 8, 't2': 9}

def story(r):
    for x in r['days']:
        print(f"    Day {x['d']} ({'MTWTFSS'[x['wd']]}{'' if x['work'] else ', off'}): jobs {x['jobs']}, opened {x['op']}, xp {x['xp']} ({x['band']}), training {x['cur']}, used {x['used']}")

def opened_on(r):
    out = {}
    for x in r['days']:
        for i in x['op']:
            out.setdefault(i, x['d'])
    return out

def pacing(r, name):
    from collections import Counter
    for x in r['days']:
        sizes = Counter()
        for i in dict.fromkeys(x['op']):
            sizes[next(s for s in (('big' if i in ('m1', 'm4', 'm5', 'm7', 'm6', 't2') else 'small'),))] += 1
        check(sizes['big'] <= 1 and sizes['small'] <= 1, f"{name}: Day {x['d']} opened {x['op']} (more than one big or one small)")
        check(x['work'] or not x['op'], f"{name}: Day {x['d']} is a day off and opened {x['op']}")

with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    errors = g.errors
    ev = g.ev

    print('(a) Step 1 as built: no sub-blocks, nothing opens:')
    hidden = ev("deviceApps().some(a => a.id === 'works')")
    r = ev(f"({PAPER})({{ plan: 'none', days: 14 }})")
    ops = [x['op'] for x in r['days'] if x['op']]
    print(f"  the Works app on Day 1 morning: {'shown' if hidden else 'hidden'}; opened {ops}, trained {r['trained']}, head: {r['head']}")
    check(not hidden, 'the Works app shows before Day 1\'s shift has ended')
    check(not ops and not r['trained'] and not r['occ'], 'with no mechanic in the build a ladder row opened')
    check(r['works'] is not None, 'SHIP.works not made after Day 1')
    shown = ev("deviceApps().some(a => a.id === 'works')")
    check(shown, 'the Works app is hidden once SHIP.works exists')

    print('(b) A steady player, every row with a stand-in sub-block, Days 1-9:')
    st = ev(f"({PAPER})({{ plan: 'steady', days: 9 }})")
    story(st)
    op = opened_on(st)
    print(f"  opened: {op}\n  trained: {st['trained']}\n  asked on: {st['asks']}\n  teacher's job and yours: {st['teach']}\n  meetings: {st['occ']}\n  Mail: {st['mail']}")
    print(f"  Record: {st['head']}\n  locker: {st['locker']}\n  Works app: {st['view']}")
    for k, d in LADDER.items():
        check(op.get(k) == d, f"steady: {k} opened on Day {op.get(k)}, the table says Day {d}")
    pacing(st, 'steady')
    for k in ('m1', 'm4', 'm5', 'm7', 'm6'):
        t = st['teach'].get(k, {})
        check(k in st['trained'], f'steady: {k} never trained')
        check(t.get('by') not in (None, 'you') and t.get('you') == 'you', f"steady: {k}'s training: the teacher's job then yours ({t})")
    check(st['teach'].get('m7', {}).get('by') == 'halloran-emeka', f"steady: the scanner on Day 5 is Emeka Halloran's to teach ({st['teach'].get('m7')})")
    check(st['works']['tools'].get('clipboard') and st['works']['tools'].get('scanner'), f"steady: tools given {st['works']['tools']}")
    check(len(st['mail']) >= 5 and len(st['occ']) >= 5 and all(o['status'] != 'missed' for o in st['occ']), f"steady: an ask (Mail and appointment) for each big training: {st['occ']}")
    b = {x['d']: x['band'] for x in st['days']}
    check(b.get(8) == 'relied', f"steady: not 'Relied on' by the end of Day 8 ({b.get(8)}, xp {st['days'][7]['xp']})")
    check(b.get(4) != 'relied', 'steady: "Relied on" before Day 5')
    check('Relied on' in (st['head'] or '') or b.get(9) == 'relied', 'the Record says the band')

    print('(c) A very busy player:')
    bz = ev(f"({PAPER})({{ plan: 'busy', days: 8 }})")
    print('   ', ', '.join(f"Day {x['d']}: {x['jobs']} jobs, xp {x['xp']} {x['band']}" for x in bz['days']))
    check(all(x['band'] != 'relied' for x in bz['days'] if x['d'] <= 4), 'busy: "Relied on" before Day 5')
    pacing(bz, 'busy')

    print('(d) A lazy player, Days 1-28:')
    lz = ev(f"({PAPER})({{ plan: 'lazy', days: 28 }})")
    lop = opened_on(lz)
    print(f"  opened: {lop}\n  trained: {lz['trained']}\n  asked on: {lz['asks']}")
    pacing(lz, 'lazy')
    for k, d in LADDER.items():
        if k == 't2': continue
        check(k in lop and lop[k] >= d, f'lazy: {k} lost or early ({lop.get(k)})')
        check(k in lz['trained'], f'lazy: {k} never trained')
    check(any(len(v) >= 2 for v in lz['asks'].values()), f"lazy: a missed ask isn't offered again: {lz['asks']}")
    check(sum(lop.values()) > sum(op.get(k, 0) for k in lop), 'lazy: no later than the steady player')

    print('(e) Bands, skill words, tools, penalties:')
    e = ev("""(() => { SHIP.works = null; setShipNow(1440 + 600); const W = worksInit(), out = {};
      out.bands = [0, 7, 8, 17, 18, 29, 30, 39, 40, 90].map(x => { W.xp = x; return worksBand(); });
      W.rank = 'officer'; W.xp = 0; out.officer = worksBandWord(); W.rank = 'junior';
      out.words = [0, 4, 5, 14, 15].map(n => { W.sk.oven = n; return skillWord('oven'); });
      out.give = toolGive('scanner'); out.again = toolGive('scanner'); out.has = hasTool('scanner'); W.tr.m7 = 5; for (let k = 0; k < 10; k++) worksUse('m7'); out.wear = toolWear('scanner');
      W.xp = 10; simNote('shiftMissed', { day: 2 }); out.missed = W.xp; simNote('jobAbandoned', { machine: null, id: 'x' }); out.aband = W.xp; W.xp = 1; simNote('shiftMissed', { day: 3 }); out.floor = W.xp;
      out.before = (() => { SHIP.works = null; setShipNow(1000); return worksInit(); })();
      SHIP.works = null; return out; })()""")
    print('  ', e)
    check(e['bands'] == ['new', 'new', 'steady', 'steady', 'reliable', 'reliable', 'trusted', 'trusted', 'relied', 'relied'], f"bands {e['bands']}")
    check(e['officer'] == 'New officer', 'after a promotion the band reads "New officer"')
    check(e['words'] == ['new to you', 'new to you', 'getting the hang of these', 'getting the hang of these', 'you know these well'], f"skill words {e['words']}")
    check(e['give'] and not e['again'] and e['has'] and abs(e['wear'] - .2) < 1e-9, 'tools: given once, worn by use')
    check(e['missed'] == 7 and e['aband'] == 5 and e['floor'] == 0, 'a missed shift -3, an abandoned job -2, never below 0')
    check(e['before'] is None, 'SHIP.works made before Day 1\'s shift ended')

    tb = ev("""(() => { const r = worksTabAdd({ id: 'test', title: 'Test', order: 40, view: () => [{ kind: 'text', text: 'hello' }], act: (v, a) => { window.__tabAct = v + ':' + a; } });
      WORKS_TAB = 'test'; const v = worksView(); deviceDo({ app: 'works', do: 'poke', arg: 7 }); const got = window.__tabAct;
      WORKS_TABS.splice(WORKS_TABS.findIndex(x => x.id === 'test'), 1); WORKS_TAB = 'training';
      return { r, tabs: v.blocks[0].items.map(x => x.label), body: v.blocks[1] && v.blocks[1].text, got }; })()""")
    print('  worksTabAdd:', tb)
    check(tb['r'] and tb['tabs'][:3] == ['Training', 'Work log', 'Tools'] and tb['tabs'][-1] == 'Test' and tb['body'] == 'hello' and tb['got'] == 'poke:7', 'worksTabAdd: a tab shows, in order, and gets its verbs')

    eh = ev("""(() => { SHIP.works = null; setShipNow(4 * 1440 + 600); const W = worksInit(); W.cur = { id: 'm7', st: 'do', d: 5, by: 'halloran-emeka', occ: null, j: 'jx', w: 15 }; W.cases = { open: [{ id: 'cjx', job: 'jx' }], done: [] };
      const out = { hold: worksEscortHold('m7') }; worksDone('m7', shipNow()); out.st = W.cur && W.cur.st; out.trainedEarly = W.tr.m7 !== undefined;
      out.esc = (() => { SHIP.jobs.push({ id: 'jx', machine: machineList()[0].id, status: 'done', doneBy: 'you' }); const e = worksEscort({ id: 'halloran-emeka' }, shipNow()); return e && e.mode; })();
      out.clean = JSON.stringify(worksClean(JSON.parse(JSON.stringify(W))).cur) === JSON.stringify(W.cur);
      W.cases.open = []; simNote('caseCalled', { train: true }); out.after = W.tr.m7; out.cur = W.cur; SHIP.works = null; SHIP.jobs = SHIP.jobs.filter(j => j.id !== 'jx'); return out; })()""")
    print('  the escort hold (Day 5):', eh)
    check(eh['hold'] and eh['st'] == 'held' and not eh['trainedEarly'] and eh['esc'] == 'follow' and eh['clean'] and eh['after'] == 5 and eh['cur'] is None, 'worksEscortHold / caseCalled')

    rv = ev("""(() => { SHIP.works = null; SHIP.occasions.length = 0; SHIP.mail = []; for (const r of CAREER_LADDER) WORK_MECH[r.id] = { reserve: (d, at, slot, o) => jobReserve('washer', d, at, slot, o) };
      setShipNow(1440 + 300); const W = worksInit(); W.log.push(['x', 1, 0, 'service']); const out = {};
      skipTo(1440 + 460); WORKS_TICK.m = -1; out.st = W.cur && W.cur.st; out.toldAsleep = W.cur && W.cur.told;
      worksCareerTick(shipNow() + 1); out.toldUp = W.cur && W.cur.told; out.goal = !!(typeof IX_GOAL !== 'undefined' && IX_GOAL);
      W.cur = { id: 'm7', st: 'held', d: 2, by: 'calder', occ: null, j: null, w: 0, hold: true }; ladderTick(Math.floor((2 * 1440 + 400) / 60)); out.heldTrained = W.tr.m7;
      deviceDo({ app: 'works', tab: 'tools' }); out.tab = WORKS_TAB; WORKS_TAB = 'training';
      for (const k in WORK_MECH) delete WORK_MECH[k]; SHIP.works = null; return out; })()""")
    print('  asked while asleep, told when up; a stale hold; open on a tab:', rv)
    check(rv['st'] == 'meet' and rv['toldAsleep'] is False and rv['toldUp'] is True and rv['goal'], 'an ask made during a sleep is told (toast, goal) when you are up')
    check(rv['heldTrained'] is not None, 'a hold left from an earlier day trains you on the next workday')
    check(rv['tab'] == 'tools', 'the Works app opens on a given tab')

    print('(f) The save:')
    sv = ev(f"""(() => {{ const r = ({PAPER})({{ plan: 'steady', days: 2 }}); const W = SHIP.works;
      W.cur = {{ id: 'm4', st: 'do', d: 3, by: 'esposito-yara', occ: 'works.m4@3', j: 'reserve11:x@1', w: 15 }};
      const core = Object.fromEntries(Object.entries(W).filter(([k]) => k in worksClean({{ v: 1 }}))), raw = JSON.stringify(core), back = JSON.stringify(worksClean(JSON.parse(raw)));   // 24 core's fields (sub-blocks keep their own)
      const junk = worksClean({{ v: 1, tier: 'x', rank: 'admiral', xp: -5, tr: {{ m1: 'a', zz: 3 }}, log: 5, tools: {{ bogus: [1, 2], scanner: [3, 7] }}, op: {{ 2: ['m1', 'nope'], x: [] }}, cur: {{ id: 'm1', st: 'eh' }} }});
      return {{ same: raw === back, raw: raw.length, junk, bad: worksClean(null) }}; }})()""")
    print('  round trip:', sv['same'], f"({sv['raw']} bytes); junk:", sv['junk'])
    check(sv['same'], 'worksClean changes a good save')
    j = sv['junk']
    check(j and j['tier'] == 1 and j['rank'] == 'junior' and j['xp'] == 0 and j['tr'] == {} and j['log'] == [] and j['tools'] == {'scanner': [3, 1]} and j['op'] == {'2': ['m1']} and j['cur'] is None, 'worksClean on junk')
    check(sv['bad'] is None, 'worksClean(null) should be none')
    # a real reload, saving on: mid-training, then an old save (no ship.works)
    tmp = WORK / 'test' / '_career_save.html'
    tmp.write_text(instrument(pathlib.Path(sys.argv[1]).read_text()))
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    page = b.new_page(viewport={'width': 600, 'height': 500})
    page.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    page.add_init_script(INIT)
    page.on('pageerror', lambda e: errors.append(f'pageerror (save): {e}'))
    def load():
        page.goto('file://' + str(tmp)); page.wait_for_function('window.__sc !== undefined', timeout=60000)
        return lambda s: page.evaluate('s => window.__sc(s)', s)
    ev2 = load(); ev2("localStorage.clear()"); ev2 = load()
    w0 = ev2(f"""(() => {{ for (const r of CAREER_LADDER) WORK_MECH[r.id] = {{}}; setShipNow(1440 + 400); const W = worksInit(); W.xp = 12; W.sk.oven = 6; W.log.push(['oven-2@30', 2, 1, 'repair']);
      W.tr.m1 = 2; W.use.m1 = 1; W.op[2] = ['m1']; toolGive('clipboard'); setShipNow(2 * 1440 + 400); WORKS_TICK.h = -1; worksCareerTick();
      const c = W.cur; saveGame(); return {{ works: JSON.stringify(W), cur: c && c.st, occ: SHIP.occasions.filter(r => /^works/.test(r.id)).length }}; }})()""")
    ev2 = load()
    w1 = ev2("(() => { const W = SHIP.works; return { works: JSON.stringify(W), occ: OCCASIONS['works.m4'] ? 'made' : 'missing', ok: !!W } })()")
    print(f"  reload mid-training ({w0['cur']}, {w0['occ']} appointment): same {w0['works'] == w1['works']}, its occasion {w1['occ']}")
    check(w0['cur'] == 'meet' and w0['works'] == w1['works'], 'a reload mid-training changes SHIP.works')
    check(w1['occ'] == 'made', "a reload mid-training loses the training's occasion")
    ev2("localStorage.setItem(SAVE_KEY, JSON.stringify({ v: 2, build: '0.60.7', time: { day: 10, min: 300 }, player: { deck: 4, tile: [7, 3], facing: 0 }, ship: { decks: {} }, crew: {} })); Storage.prototype.setItem = () => {}")
    ev2 = load()
    old = ev2("""(() => { const out = { works: SHIP.works }; for (const r of CAREER_LADDER) WORK_MECH[r.id] = { reserve: (d, at, slot, o) => jobReserve('washer', d, at, slot, o) }; SHIP.jobs.push({ id: 'old', status: 'done', doneBy: 'you', kind: 'service' });
      WORKS_TICK.h = -1; setShipNow(9 * 1440 + 360); worksCareerTick(); const W = SHIP.works; out.tier = W && W.tier; out.tr = W && W.tr; out.op = W && W.op; return out; })()""")
    print('  an old save on Day 10:', old)
    check(old['tier'] == 1 and old['tr'] == {} and old['op'].get('10', [None])[0] == 'm1' and list(old['op']) == ['10'], 'an old save loads as Tier 1, nothing trained, rounds on its next workday')
    ev2("localStorage.clear()"); b.close()
    lg = ev(f"(() => {{ const r = ({PAPER})({{ plan: 'busy', days: 30 }}); return {{ size: r.size, log: r.works.log.length }}; }})()")
    print(f"  ship.works after 30 busy days: {lg['size']} bytes, log {lg['log']}")
    check(lg['size'] < 3000 and lg['log'] == 30, 'ship.works over 3 KB by Day 30, or the log not cut to 30')

    print('(g) The steady run twice:')
    again = ev(f"({PAPER})({{ plan: 'steady', days: 9 }})")
    same = json.dumps(again, sort_keys=True) == json.dumps(st, sort_keys=True)
    print('  identical:', same)
    check(same, 'the steady run differs the second time')

    ev("for (const k in WORK_MECH) delete WORK_MECH[k]; SHIP.works = null")
    if errors: fail('page errors: ' + ' | '.join(errors[:5]))
    g.close()

print('CAREER CHECK OK' if ok else 'CAREER CHECK FAILED')
sys.exit(0 if ok else 1)
