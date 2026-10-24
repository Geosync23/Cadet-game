# Starship Cadet: arrows check (the arrows plan, plans/arrows-pillar5-plan.html; briefs plans/arrows-briefs.md)
# Part "queue" (piece B, AR1): the arrow queue in section 15b (GUIDE_ON), its pop-up queue and the teaching-arrows
# setting, on paper in a real page (Dev mode's own save, so the real save is never touched):
#   off:      with GUIDE_ON off (the build's default) guideAsk refuses, goalNow is the old rule, toast shows at once,
#             Settings has no new row and the save has no "guide" key
#   order:    levels 4, 2 and 1 asked at once: 1 shows, then 2, then 4 as each is done; ties by `from`, then ask order
#   done:     `until` passed, `done()` true or throwing: dropped; `from` in the future: waits
#   track:    tracking off shows only levels 1-2
#   direct:   a goal set with setGoal stays over levels 2-6; a level 1 borrows the arrow and gives it back
#   body:     levels 5-6 wait while your job has a step to point at
#   once:     a `once: 2` entry shows twice, survives a reload, and is refused a third time; 'all' ignores it for
#             teaching entries, 'off' refuses teaching entries (set through GUIDE.mode, a test override)
#   toasts:   five pop-ups in one frame show in order, each for at least 2.5 s, at most 3 waiting, repeats merged; an
#             urgent one ({ now: true }) at once
#   mode:     the teaching-arrows setting is read from section 19's teachMode() (AC1's Settings row), 'first' without it
#   size:     SHIP.guide in the save stays small with 400 seen ids (300 kept)
# Parts "shift" and "week" (AR1, for FX1-FX3): play as a player who ONLY follows the arrow (and the pointer, once piece C
# is in) from a real game's state (tracking as after taking a job yesterday): go where the arrow points (a teleport stands
# in for the walk), tap the thing it points at (your job's own steps: a real screen tap at the pin), press the button a panel offers (the clock screen's, the board's Take it /
# Turn it in, a meeting's Go on, a card's choices in turn), read meetings through, sleep at night.
#   shift: one ordinary workday (Day 9, nothing new taught): clocked in by 09:05, at least three jobs turned in, never
#          stuck (the arrow on the same spot for 45 ship minutes with the player there), clocked out by the player
#   week:  Days 2-8 in a row: clocked in every workday; each lesson learned on its day by following the arrow (Rounds
#          Day 2, Hauling and the drill Day 3, the inspection and Tuning Day 4, the scanner and the first head-scratcher
#          Day 5); the scanner counted as used by the next workday; Making it safe opened and learned on Day 8, or on the
#          first workday after the scanner's first use (Day 9 at most); no arrow left up after its
#          moment (the same label for over 3 ship hours)
# On 0.64.15 (2b4a05db) both FAIL: that is the point. Which fixer turns which line green is printed with each FAIL.
# Run one part:  python3 arrows_check.py BUILD.html shift   (parts: queue, clockin, shift, week; default all, about 15 minutes)
# Part "clockin" (patch 0.92.3 item 6, AC3): Days 1-3 into the Works bay before clocking in: the clock-in tip at once (Day 1: after
# Zeke's line), Clock in tracked (not with Teaching arrows Off), both gone the moment you clock in. A real new game.
# Add 'guide' to play shift and week with the arrow queue switched on (GUIDE_ON), e.g. ... BUILD.html week guide
# Setup as cadet_test.py (playwright, three r128 in $CADET_WORK/three). Run:  python3 arrows_check.py BUILD.html
import sys, json, re, os, pathlib
from playwright.sync_api import sync_playwright

WORK = pathlib.Path(os.environ.get('CADET_WORK', '/tmp/cadet-work'))
(WORK / 'test').mkdir(parents=True, exist_ok=True)
THREE = (WORK / 'three/package/build/three.min.js').read_text()
INIT = """(() => { let vt = 1000; const cbs = []; performance.now = () => vt; Date.now = () => vt;
  window.requestAnimationFrame = cb => { cbs.push(cb); return cbs.length; };
  window.__step = (n, dtMs) => { for (let k = 0; k < n; k++) { vt += dtMs; const q = cbs.splice(0); for (const cb of q) cb(vt); } }; })();"""
ok = True
def fail(msg):
    global ok
    ok = False; print('FAIL', msg)
def check(cond, msg):
    if not cond: fail(msg)
    return cond

class Page:
    def __init__(self, ctx, path):
        self.errors = []
        self.page = ctx.new_page()
        self.page.on('pageerror', lambda e: self.errors.append(f'pageerror: {e}'))
        self.page.on('console', lambda m: m.type == 'error' and self.errors.append(f'error: {m.text}'))
        self.page.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
        self.page.add_init_script(INIT)
        html = pathlib.Path(path).read_text(); i = html.rfind('})();')
        self.tmp = WORK / 'test' / ('_arrows_' + pathlib.Path(path).name)
        self.tmp.write_text(html[:i] + "window.__sc = src => eval(src);\n" + html[i:])
        self.page.goto('file://' + str(self.tmp) + '#dev'); self.ready()
    def ready(self):
        self.page.wait_for_function('window.__sc !== undefined', timeout=90000)
        self.ev("(() => { const rr = renderer.render.bind(renderer); renderer.render = (s, c) => { if (window.__draw) rr(s, c); }; })()")
        self.step(20)
        if self.page.locator('text=Sign and go aboard').count():
            self.page.fill('form input', 'Ada'); self.page.click('text=Sign and go aboard'); self.step(30)
    def day2(self):                                   # past the arrival (its own arrows, a locked device, its pop-ups)
        self.ev("devmodeRun('Set career to Day 2', () => devmodeSetCareerTo(2))"); self.step(20); self.ev("clearGoal(); SHIP.player.track = undefined")
    def reload(self):
        self.page.reload(); self.ready()
    def ev(self, src): return self.page.evaluate('s => window.__sc(s)', src)
    def step(self, n, dt=1000 / 30): self.page.evaluate(f'window.__step({n}, {dt})')

# a goal on Deck 5 by label; the entries' done flags live in window.__d so a test can end them
ASK = r"""((o) => { window.__d = window.__d || {};
  return guideAsk({ id: o.id, level: o.level, goal: () => ({ deck: 5, room: 'w', label: o.id }), from: o.from == null ? null : o.from,
    until: o.until == null ? shipNow() + 600 : o.until, once: o.once, owner: 'arrows_check',
    done: o.boom ? () => { throw new Error('boom'); } : () => !!window.__d[o.id] }); })"""
def ask(pg, **o): return pg.ev(f"({ASK})({json.dumps(o)})")
def shown(pg): return pg.ev("(() => { GUIDE.key = ''; const g = goalNow(); return g ? g.label : null; })()")
def done(pg, i): pg.ev(f"window.__d[{json.dumps(i)}] = true")

def part_off(pg):
    st = pg.ev("""(() => { const before = goalNow(); return { on: GUIDE_ON, ask: guideAsk({ id: 'x', level: 1, goal: () => ({ deck: 5, room: 'w', label: 'x' }), until: shipNow() + 60 }),
      same: JSON.stringify(goalNow()) === JSON.stringify(IX_GOAL || (SHIP.player.track === null ? null : ixJobGoal)), list: GUIDE.list.length, loop: GUIDE.loop }; })()""")
    check(st['on'] is False and st['ask'] is False and st['same'] and st['list'] == 0 and not st['loop'], f'off: the queue is not inert: {st}')
    pg.ev("toast('A', 'one'); toast('B', 'two')"); t = pg.ev("document.getElementById('tt').textContent")
    check(t == 'B', f'off: toast no longer shows at once ({t})')
    pg.ev('saveGame()'); sv = pg.ev("JSON.parse(localStorage.getItem(SAVE_KEY))")
    check(sv is not None and 'guide' not in sv, f'off: the save has a guide key ({sorted(sv)[:8] if sv else sv})')
    print('  off: inert, toast at once, no save key')

def part_queue(pg):
    pg.ev("GUIDE_ON = true; GUIDE.list.length = 0; GUIDE.rev++; SHIP.player.track = undefined; clearGoal(); window.__d = {}")
    now = pg.ev('Math.floor(shipNow())')
    for lv, i in ((4, 'q4'), (2, 'q2'), (1, 'q1')): check(ask(pg, id=i, level=lv), f'order: {i} refused')
    seq = [shown(pg)]
    done(pg, 'q1'); seq.append(shown(pg)); done(pg, 'q2'); seq.append(shown(pg)); done(pg, 'q4'); seq.append(shown(pg))
    check(seq[:3] == ['q1', 'q2', 'q4'] and (seq[3] is None or not seq[3].startswith('q')), f'order: {seq}')
    ask(pg, id='t1', level=3); ask(pg, id='t2', level=3, **{'from': now - 30})
    s = shown(pg); check(s == 't2', f'order: the earlier from should win a tie ({s})')
    pg.ev("GUIDE.list.length = 0; GUIDE.rev++")
    ask(pg, id='a', level=3); ask(pg, id='b', level=3); s = shown(pg); check(s == 'a', f'order: the earlier ask should win a tie ({s})')
    print(f'  order: {seq[:3]}, ties by from then ask')
    # done, until, throwing, from in the future
    pg.ev("GUIDE.list.length = 0; GUIDE.rev++")
    ask(pg, id='past', level=1, until=now - 1); ask(pg, id='boom', level=1, boom=True); ask(pg, id='later', level=1, **{'from': now + 30}); ask(pg, id='now', level=2)
    s = shown(pg); ids = pg.ev("GUIDE.list.map(e => e.id)")
    check(s == 'now' and 'past' not in ids and 'boom' not in ids and 'later' in ids, f'done: {s}, live {ids}')
    pg.ev(f"setShipNow({now + 31})"); s = shown(pg); check(s == 'later', f'done: a future from did not start ({s})')
    pg.ev(f"setShipNow({now})")
    # a throwing done() on an entry that isn't picked (behind a lower level) is dropped too (RV2's mutant ar_throwkeeps)
    pg.ev("GUIDE.list.length = 0; GUIDE.rev++")
    ask(pg, id='front', level=1); ask(pg, id='boomback', level=3, boom=True)
    s = shown(pg); ids = pg.ev("GUIDE.list.map(e => e.id)")
    check(s == 'front' and ids == ['front'], f'done: a throwing done() behind a lower level was kept ({s}, live {ids})')
    print('  done: until, done, a throw dropped (picked or not); from waits')
    # tracking off: only 1-2
    pg.ev("GUIDE.list.length = 0; GUIDE.rev++; SHIP.player.track = null")
    ask(pg, id='l3', level=3); s3 = shown(pg); ask(pg, id='l2', level=2); s2 = shown(pg)
    check(s3 is None and s2 == 'l2', f'track: off should show only levels 1-2 ({s3}, {s2})')
    pg.ev("SHIP.player.track = undefined")
    # a direct goal stays over 2-6; a level 1 borrows it
    pg.ev("GUIDE.list.length = 0; GUIDE.rev++; setGoal({ deck: 4, room: 'w', label: 'mine', trk: 'place:bed' })")
    ask(pg, id='d2', level=2); a = shown(pg); cov = pg.ev("guideList().filter(e => e.covered).map(e => e.id)")
    ask(pg, id='d1', level=1); b = shown(pg); done(pg, 'd1'); c = shown(pg)
    check(a == 'mine' and b == 'd1' and c == 'mine' and cov == ['d2'], f'direct: {a}, {b}, {c}, covered {cov}')
    # done between two picks in the same minute: gone at once (RV2)
    pg.ev("clearGoal(); GUIDE.list.length = 0; GUIDE.rev++; window.__d = {}"); ask(pg, id='quick', level=2); s1 = shown(pg)
    done(pg, 'quick'); s2 = pg.ev("(() => { const g = goalNow(); return g ? g.label : null; })()")   # no cache reset: the same minute
    check(s1 == 'quick' and s2 != 'quick', f'direct: a done entry stayed up within its minute ({s1}, {s2})')
    pg.ev("clearGoal(); GUIDE.list.length = 0; GUIDE.rev++")
    print('  track and direct: tracking off shows levels 1-2 only; your goal stays, a level 1 borrows it')
    # body after the job's step
    j = pg.ev("""(() => { const t = shipNow(), m = machineList().find(m => m.deck === 3 && m.kind === 'oven') || machineList()[0];
      const j = { id: 'arrows-job', machine: m.id, deck: m.deck, room: m.room, kind: 'service', urgency: 1, posted: t, found: t, claimedBy: 'you', status: 'claimed', start: t, parts: [], title: 'Service' };
      SHIP.jobs.push(j); MACH_REV++; ixGoalAt = -1; SHIP.player.track = j.id; ixJobGoal = ixJobStep(); return !!ixJobGoal; })()""")
    ask(pg, id='b5', level=5); s = shown(pg)
    check(j and s is not None and s != 'b5', f'body: a level 5 showed over the job ({s})')
    pg.ev("SHIP.jobs = SHIP.jobs.filter(x => x.id !== 'arrows-job'); MACH_REV++; ixJobGoal = null; SHIP.player.track = undefined"); s = shown(pg)
    check(s == 'b5', f'body: a level 5 did not show without a job ({s})')
    pg.ev("GUIDE.list.length = 0; GUIDE.rev++")
    print('  body: levels 5-6 after the job')
    # the training arrows T1-T3 (read from SHIP.works.cur): meet from 15 minutes before at the room (the teacher only once
    # they're in it), watch at the teacher, your turn at the board unless you hold another job (RV6's review of E)
    t = pg.ev("""(() => { if (typeof guideTrain !== 'function' || !SHIP.works) return null; const W = SHIP.works, now = Math.floor(shipNow()), d = Math.floor(now / 1440) + 1, out = {};
      const keep = W.cur, lab = () => { GUIDE.key = ''; const g = goalNow(); return g ? g.label || null : null; }, ent = p => GUIDE.list.find(e => e.id.startsWith(p)) || null;
      const fit = t => { const c = document.createElement('canvas').getContext('2d'); c.font = '12.5px ' + getComputedStyle(document.body).fontFamily; return Math.ceil(c.measureText(t || '').width) + 20; };
      GUIDE.list.length = 0; GUIDE.rev++; clearGoal(); SHIP.player.track = undefined; if (myJob()) dropJob(myJob().id);
      const occ = { key: 'arrows-occ', id: 'works.m4', deck: 5, room: 'r', at: now + 30, len: 15, status: 'asked' }; SHIP.occasions.push(occ);
      W.cur = { id: 'm4', st: 'meet', d, by: 'esposito-yara', occ: 'arrows-occ' };
      guideTrain(); out.early = lab();
      occ.at = now + 10; GUIDE.list.length = 0; guideTrain(); out.meet = lab(); const m = ent('train:m4:meet');
      if (m) { const g = m.goal(); out.meetLevel = m.level; out.meetRoom = [g.deck, g.room]; out.meetCrew = !!g.crew; out.inRoom = guideTeacherIn('esposito-yara', 5, 'r'); out.meetFit = fit(g.label); }
      W.cur.st = 'watch'; out.after = lab();
      const mc = machineList().find(x => !x.stub) || machineList()[0];
      SHIP.jobs.push({ id: 'arrows-tj', machine: mc.id, deck: mc.deck, kind: 'repair', urgency: 1, posted: now, found: now, claimedBy: null, parts: [], status: 'open' });
      W.cur.j = 'arrows-tj'; GUIDE.list.length = 0; GUIDE.rev++; guideTrain(); out.watch = lab(); const w = ent('train:m4:watch');
      if (w) { const g = w.goal(); out.watchLevel = w.level; out.watchCrew = g.crew; out.watchId = w.id; }
      W.cur.st = 'do'; out.watchAfter = lab();
      GUIDE.list.length = 0; GUIDE.rev++; guideTrain(); out.doo = lab(); const o = ent('train:m4:do:' + W.cur.d);   /* (DS1, patch 0.92.5 #12: T3 per day, named) */
      if (o) { const g = o.goal(); out.doLevel = o.level; out.doBoard = !!g && String(g.item) === String(/job board/i); out.doFit = fit(g && g.label); }
      SHIP.jobs.push({ id: 'arrows-mine', machine: mc.id, deck: mc.deck, kind: 'repair', urgency: 1, posted: now, found: now, claimedBy: 'you', parts: [], status: 'claimed' });
      out.otherJob = lab(); out.otherShown = guideNow() ? guideNow().id : null;
      SHIP.jobs = SHIP.jobs.filter(j => j.id !== 'arrows-mine'); out.back = lab();
      Object.assign(SHIP.jobs.find(j => j.id === 'arrows-tj'), { claimedBy: 'you', status: 'claimed' }); out.taken = lab(); out.takenLive = !!ent('train:m4:do:' + W.cur.d);
      const off = Object.keys(WORK_MECH).find(k => WORK_MECH[k].offer && ladderRow(k));
      if (off) { W.cur = { id: off, st: 'do', d, by: 'calder', j: 'arrows-tj' }; GUIDE.list.length = 0; GUIDE.rev++; guideTrain(); out.offer = [off, !!ent('train:' + off + ':do:' + d)]; }
      out.calder = guideWho('calder');
      SHIP.jobs = SHIP.jobs.filter(j => j.id !== 'arrows-tj'); SHIP.occasions.splice(SHIP.occasions.indexOf(occ), 1); W.cur = keep; GUIDE.list.length = 0; GUIDE.rev++; return out; })()""")
    if t is not None:
        print('  train:', t)
        check(t['early'] is None or 'meet' not in str(t['early']), f'train: the meet arrow showed 30 minutes before ({t["early"]})')
        check(t['meet'] and 'meet Yara' in t['meet'] and t['meet'][:5].count(':') == 1, f'train: T1 10 minutes before should say the time first and "meet Yara" ({t["meet"]})')
        check(t.get('meetLevel') == 2 and t.get('meetRoom') == [5, 'r'], f'train: T1 should be level 2 at the meeting room ({t.get("meetLevel")}, {t.get("meetRoom")})')
        check(t.get('meetCrew') == t.get('inRoom'), f'train: T1 should lead to the teacher only once they are in the room (crew {t.get("meetCrew")}, in the room {t.get("inRoom")})')
        check(t['after'] is None or 'meet' not in str(t['after']), f'train: the meet arrow outlived the meeting ({t["after"]})')
        check(t['watch'] and t['watch'].startswith('Stay close and watch Yara') and t.get('watchLevel') == 3 and t.get('watchCrew') == 'esposito-yara', f'train: T2 should follow the teacher at level 3 ({t["watch"]}, {t.get("watchLevel")}, {t.get("watchCrew")})')
        check(str(t.get('watchId', '')).endswith(':' + str(pg.ev('SHIP.time.day'))), f'train: T2\'s once should be per training, its day in the id ({t.get("watchId")})')
        check(t['watchAfter'] is None or not str(t['watchAfter']).startswith('Stay close'), f'train: T2 outlived the watching ({t["watchAfter"]})')
        check(t['doo'] and t['doo'].startswith('Your ') and 'lesson' in t['doo'] and t.get('doLevel') == 3 and t.get('doBoard'), f'train: T3 should point at the board at level 3 ({t["doo"]}, {t.get("doLevel")}, {t.get("doBoard")})')
        check(not str(t['otherShown'] or '').startswith('train:m4:do') and 'lesson' not in str(t['otherJob'] or ''), f'train: T3 should leave the arrow to another job you hold ({t["otherJob"]}, {t["otherShown"]})')
        check('lesson' in str(t['back'] or ''), f'train: T3 should come back when that job is gone ({t["back"]})')
        check('lesson' not in str(t['taken'] or '') and not t['takenLive'], f'train: T3 outlived taking the job ({t["taken"]})')
        if 'offer' in t: check(not t['offer'][1], f'train: T3 for a row with its own offer ({t["offer"]})')
        check(t['calder'] == 'Calder', f'train: Calder should be "Calder" ({t["calder"]})')
        check(t.get('meetFit', 0) <= 258 and t.get('doFit', 0) <= 258, f'train: a label too wide for 390 px (T1 {t.get("meetFit")} px, T3 {t.get("doFit")} px; 258 fit)')
    # the minute tick: guideTick asks the training arrows itself, once a ship minute (no direct call)
    tk = pg.ev("""(() => { if (typeof guideTrain !== 'function' || !SHIP.works) return null; const W = SHIP.works, now = Math.floor(shipNow());
      window.__tk = { keep: W.cur, occ: { key: 'arrows-occ2', id: 'works.m4', deck: 5, room: 'r', at: now + 10, len: 15, status: 'asked' } };
      SHIP.occasions.push(__tk.occ); W.cur = { id: 'm4', st: 'meet', d: Math.floor(now / 1440) + 1, by: 'esposito-yara', occ: 'arrows-occ2' };
      GUIDE.list.length = 0; GUIDE.rev++; guideStart(); return now; })()""")
    if tk is not None:
        for _ in range(40):
            pg.step(15)
            if pg.ev('Math.floor(shipNow())') > tk + 1: break
        got = pg.ev("""(() => { const has = GUIDE.list.some(e => e.id.startsWith('train:m4:meet')); SHIP.works.cur = __tk.keep; SHIP.occasions.splice(SHIP.occasions.indexOf(__tk.occ), 1); GUIDE.list.length = 0; GUIDE.rev++; return has; })()""")
        check(got, 'train: the minute tick did not ask the training arrows')
    # the watch's own arrow with the queue off (lead 29, AR2's find): on the training job's spot, over the job arrow,
    # another direct arrow left alone and ours back after, down at 'do'; with the queue on, none (T2 does it)
    w = pg.ev("""(() => { if (typeof trainWatchArrow !== 'function' || !SHIP.works) return null; const W = SHIP.works, keep = W.cur, on = GUIDE_ON, now = shipNow(), out = {};
      GUIDE_ON = false; GUIDE.list.length = 0; clearGoal(); trainWatchArrow.s = null;
      const mc = machineList().find(x => !x.stub) || machineList()[0], sp0 = { deck: mc.deck, room: mc.room };
      SHIP.jobs.push({ id: 'arrows-wj', machine: mc.id, deck: mc.deck, kind: 'repair', urgency: 1, posted: now, found: now, claimedBy: 'esposito-yara', parts: [], status: 'claimed' });
      W.cur = { id: 'm4', st: 'watch', d: SHIP.time.day, by: 'esposito-yara', j: 'arrows-wj', w: 0 };
      trainWatchArrow(); out.a = IX_GOAL && [IX_GOAL.label, IX_GOAL.deck, IX_GOAL.room, !!IX_GOAL.crew]; out.spot = trainSpot(SHIP.jobs.find(j => j.id === 'arrows-wj'));
      setGoal({ deck: 4, room: 'w', label: 'someone else' }); trainWatchArrow(); out.other = IX_GOAL && IX_GOAL.label;
      clearGoal(); trainWatchArrow(); out.back = IX_GOAL && IX_GOAL.label;
      W.cur.st = 'do'; trainWatchArrow(); out.atDo = IX_GOAL && IX_GOAL.label;
      W.cur.st = 'watch'; GUIDE_ON = true; trainWatchArrow(); out.queueOn = IX_GOAL && IX_GOAL.label;
      GUIDE_ON = on; clearGoal(); W.cur = keep; SHIP.jobs = SHIP.jobs.filter(j => j.id !== 'arrows-wj'); trainWatchArrow.s = null; return out; })()""")
    if w is not None:
        print('  watch arrow (queue off):', w)
        check(w['a'] and w['a'][0].startswith('Watch Yara') and w['a'][1] == w['spot']['deck'] and w['a'][2] == w['spot']['room'] and not w['a'][3], f'watch: the arrow should be on the training job\'s spot, "Watch Yara: ..." ({w})')
        check(w['other'] == 'someone else' and str(w['back'] or '').startswith('Watch Yara'), f'watch: another arrow left alone, ours back after ({w})')
        check(w['atDo'] is None and w['queueOn'] is None, f'watch: down at your turn, and none with the queue on ({w})')

def part_once(ctx, path):
    pg = Page(ctx, path); pg.day2()
    pg.ev("GUIDE_ON = true; SHIP.guide.seen = {}; GUIDE.mode = 'first'; window.__d = {}")
    counts = []
    for k in range(3):
        r = ask(pg, id='twice', level=3, once=2); s = shown(pg); counts.append((r, s))
        done(pg, 'twice'); shown(pg); pg.ev("window.__d = {}")
        if k == 0:
            pg.ev('saveGame()'); pg.reload(); pg.ev("GUIDE_ON = true; window.__d = {}; clearGoal()")
    check(counts[0] == (True, 'twice') and counts[1] == (True, 'twice') and counts[2][0] is False, f'once: {counts}')
    check(pg.ev("SHIP.guide.seen.twice") == 2, f'once: seen {pg.ev("SHIP.guide.seen.twice")}')
    pg.ev("GUIDE.mode = 'all'"); r = ask(pg, id='twice', level=3, once=2); check(r, "once: 'all' should ignore once for teaching")
    pg.ev("guideDrop('twice'); GUIDE.mode = 'off'"); r3 = ask(pg, id='t3', level=3); r2 = ask(pg, id='t2', level=2)
    check(r3 is False and r2 is True, f"once: 'off' should refuse level 3 only ({r3}, {r2})")
    pg.ev("GUIDE.mode = null")
    check(pg.ev("guideMode()") in ('first', 'all', 'off'), 'settings: guideMode without an override')   # section 19's teachMode (AC1) when it's in, else 'first'
    pg.ev("GUIDE_ON = true; SHIP.guide.seen = {}; for (let i = 0; i < 400; i++) SHIP.guide.seen['id' + i] = 1; saveGame()")
    sv = pg.ev("JSON.parse(localStorage.getItem(SAVE_KEY)).guide")
    check(sv and len(sv['seen']) == 300 and len(json.dumps(sv)) < 4000, f'size: {len(sv["seen"]) if sv else None} ids, {len(json.dumps(sv)) if sv else 0} bytes')
    check(not pg.errors, f'once: page errors {pg.errors[:3]}')
    pg.page.close()
    print('  once, mode, size: twice then refused across a reload; all / off (the Settings row is section 19\'s, AC1); 300 ids kept, under 4 KB')

def part_toasts(pg):
    pg.ev("GUIDE_ON = true; GUIDE.tq.length = 0; TOAST_AT = -1e9; PAUSE.on = true")   # the clock held: no game pop-ups in between
    pg.step(2)
    seen = []
    def rec():
        t = pg.ev("document.getElementById('tt').textContent")
        if not seen or seen[-1][0] != t: seen.append((t, pg.ev('performance.now()')))
    pg.ev("toast('T1', 'a'); toast('T2', 'b'); toast('T2', 'b'); toast('T3', 'c'); toast('T4', 'd'); toast('T5', 'e')")
    rec(); waiting = pg.ev('GUIDE.tq.length')
    for _ in range(400): pg.step(1, 50); rec()
    names = [s[0] for s in seen]
    gaps = [round(seen[i + 1][1] - seen[i][1]) for i in range(len(seen) - 1)]
    check(names == ['T1', 'T3', 'T4', 'T5'] and waiting == 3, f'toasts: shown {names}, waiting {waiting} (T2 drops: four waited, three kept)')
    check(all(g >= 2500 for g in gaps), f'toasts: one shown under 2.5 s: {gaps}')
    pg.ev("TOAST_AT = -1e9; toast('R1', 'same')"); t0 = pg.ev('TOAST_AT'); pg.step(10, 50); pg.ev("toast('R1', 'same')")
    check(pg.ev('TOAST_AT') > t0 and pg.ev('GUIDE.tq.length') == 0, 'toasts: the one on screen, again, should show again (its time restarting), not wait')
    # the same words sent twice while they wait: queued once (RV2's mutant ar2_nomerge)
    pg.ev("GUIDE.tq.length = 0; TOAST_AT = -1e9; toast('M0', 'first'); toast('M1', 'twice'); toast('M1', 'twice')")
    mq = pg.ev("GUIDE.tq.map(q => q[0])")
    check(mq == ['M1'], f'toasts: the same pop-up waiting was queued twice ({mq})')
    pg.ev("GUIDE.tq.length = 0")
    pg.ev("toast('U1', 'x'); toast('U2', 'urgent', { now: true })")
    check(pg.ev("document.getElementById('tt').textContent") == 'U2', 'toasts: an urgent one waited')
    # a tradition's join notice is never the one dropped (LEAD31-3): a planted burst around the real eventJoin
    kj = pg.ev("""(() => { if (typeof eventJoin !== 'function' || typeof eventsOn !== 'function') return null; let e = null, d = 1;
      for (; d < 60 && !e; d++) e = eventsOn(d).find(x => !/^(quiz|first-light|rec-)/.test(x.id) && !SHIP.events.joined.includes(x.id + '@' + d)); if (!e) return null; d--;
      GUIDE.tq.length = 0; TOAST_AT = -1e9; toast('K0', 'on screen'); toast('K1', 'b'); eventJoin(e, d, shipNow());
      for (const k of ['K3', 'K4', 'K5', 'K6']) toast(k, 'x'); const q = GUIDE.tq.map(x => x[0]);
      SHIP.events.joined = SHIP.events.joined.filter(k => k !== e.id + '@' + d); return { name: e.name, q }; })()""")
    check(kj is None or (kj['name'] in kj['q'] and len(kj['q']) == 3), f'toasts: a join notice was dropped by a burst of pop-ups ({kj})')
    # the test hook (LEAD31-2): window.cadetPopupsNow shows every pop-up at once; off, they wait again
    pg.ev("GUIDE.tq.length = 0; TOAST_AT = -1e9; window.cadetPopupsNow = true; toast('H1', 'a'); toast('H2', 'b')")
    hk = [pg.ev("document.getElementById('tt').textContent"), pg.ev('GUIDE.tq.length')]
    pg.ev("window.cadetPopupsNow = false; toast('H3', 'c')"); hk.append(pg.ev('GUIDE.tq.length')); pg.ev("GUIDE.tq.length = 0")
    check(hk == ['H2', 0, 1], f'toasts: the test hook cadetPopupsNow (shown, waiting; then off, waiting): {hk}')
    pg.ev("GUIDE_ON = false; PAUSE.on = false"); pg.step(3)
    check(pg.ev('GUIDE.tq.length') == 0 and not pg.ev('GUIDE.loop'), 'toasts: switching off left the queue running')
    print(f'  toasts: {names}, gaps {gaps} ms; urgent at once; join notice kept {kj}; hook {hk}')


# the arrow follower: one action per call; returns what it did (or null)
FOLLOW = r"""(() => {
  const dlg = document.getElementById('devDlg');
  if (dlg && !dlg.hidden) {
    const next = dlg.querySelector('button.next'); if (next) { next.click(); return 'read on'; }
    const bs = [...dlg.querySelectorAll('button.act')]; if (!bs.length) return null;
    // a card: keep pressing the same choice while the card's words change (it's working), try the next when they don't
    const card = !!DEV.choose, txt = dlg.textContent, n = Math.max(1, bs.length - 1);
    if (card && window.__cardTxt === txt) window.__pick = ((window.__pick || 0) + 1) % n;
    window.__cardTxt = txt; let k = card ? (window.__pick || 0) % n : 0;
    const want = /cold|cool|dim|slow/i.test(txt) ? '+' : /hot|flicker|blink|fast/i.test(txt) ? '\u2212' : null;   // a tuning card: read the machine's word, as a player would
    if (card && want) { const i = bs.findIndex(b => b.textContent.trim() === want); if (i >= 0) k = i; }
    const t = bs[k].textContent; bs[k].click(); return (card ? 'card: ' : 'reply: ') + t;
  }
  if (typeof pointNow === 'function') { try { const el = pointNow() && POINT.aim; if (el && el.isConnected && !document.getElementById('ptr').hidden) { el.click(); return 'pointer: ' + (el.textContent || '').slice(0, 30); } } catch (e) { /* piece C */ } }   // pointNow() is the shown pointer's id; POINT.aim its button
  // a head-scratcher (24k's case) waiting for your call while the arrow is your job's own step: Fault notes, as a player
  // reads the toast "Fault notes has the suspects": Where next? while clues are left, Call it once one is left, then Yes (AC2, FX3's gap 1)
  { let j = null, c = null, js = null; try { j = myJob(); c = j && typeof caseOf === 'function' ? caseOf(j) : null; js = ixJobStep(); } catch (e) { c = null; }
    const gl = (goalNow() || {}).label;
    if (c && !c.calls.length && j.scan && js && gl === js.label && !ACT) {
      if (!(DEV.open && DEV.app === 'works' && WORKS_TAB === 'faults')) { worksTabShow('faults'); window.__devN = 0; return 'open Fault notes'; }
      const bs = [...document.querySelectorAll('#devBody button')], by = re => bs.find(b => re.test(b.textContent));
      const yes = by(/^Yes$/), calls = bs.filter(b => /^Call it/.test(b.textContent)), nx = by(/^Where next\?/);
      const b = yes || (calls.length === 1 || !nx) && calls[0] || nx;
      if (b) { const t = b.textContent; b.click(); if (t.startsWith('Where next')) deviceClose(); return 'Fault notes: ' + t; }
    }
  }
  // the phone left open (the Scanner opens it by itself): closed after a moment, as a player would (FX3's gap 2)
  if (DEV.open && !DEV.choose && !ACT) { window.__devN = (window.__devN || 0) + 1; if (window.__devN >= 3) { window.__devN = 0; deviceClose(); return 'close the device'; } } else window.__devN = 0;
  { const gq = typeof GUIDE_ON !== 'undefined' && GUIDE_ON ? goalNow() : null, call = IX_GOAL && /^career:/.test(IX_GOAL.trk || '') ? IX_GOAL : gq && /^inc:/.test(gq.guide || '') ? gq : null;   // FX10 (backlog 15): with the arrows on, Calder's call is the queue's level-1 'inc:m6', not IX_GOAL
    if (ACT && ACT.phase !== 'walk' && call) { const l = call.label; actEnd(true); return 'leave it for: ' + l; } }   // an urgent career arrow (Calder's call) over your work: you stop and go, as a player would (the repair's time is kept; FX4)
  { const c = SHIP.works && SHIP.works.cur, r = c && c.st === 'meet' && SHIP.occasions.find(x => x.key === c.occ), n = shipNow(); if (r && !r.met && r.status === 'asked' && n >= r.at && n < r.at + r.len && deckDef.num === r.deck && roomAt(...player.here()) === r.room && !DIALOGUE && !ACT) return null; }   // in a training meeting's room while it's on: stay a moment for it to start (FX4)
  if (ACT) { if (IX_ACTS[ACT.kind] && ACT.phase !== 'walk' && (ACT.done || 0) >= ((ACT.def && ACT.def.mins) || 0)) { const k = ACT.kind; actEnd(); return 'stand up: ' + k; } return null; }   // a sit-down (tea, a lounge) once its minutes are in: up again, as a player would (AC2)
  const cs = document.getElementById('clockScreen');
  if (cs && !cs.hidden && getComputedStyle(cs).display !== 'none') {
    const gl = (goalNow() || {}).label || '', want = /clock out|shift over/i.test(gl) ? /clock out/i : /clock in/i;
    const b = [...cs.querySelectorAll('button')].find(b => want.test(b.textContent)) || [...cs.querySelectorAll('button')].find(b => /close/i.test(b.textContent));
    if (b) { const t = b.textContent; b.click(); return 'clock screen: ' + t; }
  }
  const bd = document.getElementById('ixBoard');
  if (bd && !bd.hidden) { const bs = [...bd.querySelectorAll('#ixBoardL button')], b = bs.find(b => /turn it in/i.test(b.textContent)) || bs.find(b => /take/i.test(b.textContent) && /asked for you/i.test((b.closest('.ixjob') || b.parentNode).textContent)) || bs.find(b => /take/i.test(b.textContent));   // a job held for you first (your turn at a lesson), as a player reading the arrow would (AC2)
    const t = b ? b.textContent + ': ' + ((b.closest('.ixjob') || b.parentNode).querySelector('b') || { textContent: '' }).textContent : 'nothing to take'; if (b) b.click(); else document.getElementById('ixBoardC').click(); return 'board: ' + t; }
  const g = goalNow(); if (!g) return null;
  if (deckDef.num !== g.deck) { goToDeck(g.deck); return 'lift to Deck ' + g.deck; }
  const w = ixGoalWorld(g); if (!w) return 'arrow with no spot: ' + g.label;
  const p = player.obj.position;
  if (Math.hypot(w.x - p.x, w.z - p.z) > 2.2) { const gl = nearestOpen(w.x, w.z, player); player.obj.position.copy(cellPos(...gl)); player.stop(); return 'walk to: ' + g.label; }
  const key = g.label + '|' + Math.floor(shipNow() / 3); if (window.__tapKey === key && window.__tapKey2 !== key) return null;   // a tap every 3 ship minutes at most
  if (window.__tapKey2 === key && window.__tapDone === key) return null; if (window.__tapKey2 === key) window.__tapDone = key; window.__tapKey = key;
  const sh = /the (.+) shelf/.exec(g.label || ''), its = ITEMS.map(i => { i.hit.getWorldPosition(_wp); return [i, _wp.clone(), Math.hypot(_wp.x - w.x, _wp.z - w.z)]; });
  its.sort((a, b) => a[2] - b[2]);
  const named = its.find(x => x[2] < 3.5 && x[0].t && (g.label || '').toLowerCase().includes(x[0].t.toLowerCase().replace(/\s+\d+$/, '')));   // what the label names, as a player would read it
  const it = sh && its.find(x => x[0].t === sh[1]) || named || its[0];   // a shelf by its name, else the thing named, else the nearest
  const pin = () => {                                     // a tap on the pin as the game draws it when it takes taps (over an item: CP4 38), else the floor under the arrow's spot
    const pe = document.getElementById('ixGoal'), pd = pe && !pe.hidden && pe.children[1];
    // only a pin that takes a tap (over an item); a place's pin lets the tap through to the floor spot under it
    if (pd && pe.classList.contains('tap') && getComputedStyle(pd).display !== 'none') { const r = pd.getBoundingClientRect(); if (r.width > 1 && r.bottom > 0 && r.top < innerHeight) return { click: [r.left + r.width / 2, r.top + r.height / 2], label: g.label }; }
    const v = new THREE.Vector3(w.x, .05, w.z).project(camera); return { click: [(v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight], label: g.label }; };
  if (window.__tapKey2 === key) return pin();             // the thing didn't answer: a real tap on the floor at the pin, as a player would
  { let js = null; try { js = typeof ixJobStep === 'function' ? ixJobStep() : null; } catch (e) { js = null; } let mj = null; try { mj = myJob(); } catch (e) { mj = null; } if (mj && !mj.workDone && js && js.label === g.label && !sh && !g.item && g.place !== '5-timeclock-1' && !its.some(x => x[2] < 2.5)) return pin(); }   // nothing there to tap by name: the pin (a thing there is tapped first, the ray through it, and the floor at the pin only if nothing started: RV7's order)   // your job's own step (a chore's stop, a machine; not the board, the time clock or another named thing, tapped by name: RV7): a real tap at its pin, as a player would (lead 29, RV7's arrows_check_rt; a shelf still by its name)
  if (it && it[2] < 2.5) { try { const v = it[1].clone().project(camera); ray.setFromCamera({ x: v.x, y: v.y }, camera); } catch (e) { /* no ray */ }   // the tap's ray through the thing, as a real tap would set it (a stale one from the last real tap made the board's tap restart a done job: AC2)
    const r = playerTap(it[0], it[1].clone(), it[1].clone()); let held = null; try { held = myJob(); } catch (e) { held = null; }
    if (r && ACT && (IX_ACTS[ACT.kind] && !/tea|biscuits|drink|water/i.test(g.label || '') || held && !held.workDone && /^(rec|sit$|eat$|lie$|hobby|disc|tiles|clothes|craft|bedMake|tidy|roofRide|pay$)/.test(ACT.kind))) { const k = ACT.kind; actEnd(true); window.__tapKey2 = key; return 'tap ' + it[0].t + ': started ' + k + ', not the job: up again'; }   // RV7: anything that isn't the job's stop (the climbing wall all Day 5); a sit-down or laundry instead of the job's stop (a pin by the folding table): the floor at the pin next (AC2)
    if (!r || !ACT && !document.querySelector('#ixBoard:not([hidden]), #clockScreen:not([hidden]), #devDlg:not([hidden])')) window.__tapKey2 = key; return 'tap ' + it[0].t + ': ' + r; }   // answered but nothing started (a machine's "in good order" over the stop's spot): the floor at the pin next (AC2)
  return pin();
})()"""
STATE = r"""(() => { const W = SHIP.works, d = SHIP.time.day, g = goalNow();
  return { clock: clockText(), day: d, min: Math.floor(SHIP.time.min), arrow: g ? g.label : null, deck: deckDef.num, at: player.here().join(','),
    tr: W ? Object.assign({}, W.tr) : {}, use: W ? Object.assign({}, W.use) : {}, op: W ? W.op : {}, cur: W && W.cur ? W.cur.id + ':' + W.cur.st : null,
    inn: typeof careerClockedIn === 'function' ? !!careerClockedIn(d) : null, out: typeof careerClockedOut === 'function' ? !!careerClockedOut(d) : null, log: (SHIP.player.clockLog || {})[d] || 0,
    done: (SHIP.jobs || []).filter(j => j.doneBy === 'you' && Math.floor((j.doneAt || 0) / 1440) + 1 === d).length }; })()"""
FIX = { 'clock in': 'FX1', 'stuck': 'FX1 (arrows and tracking) or FX3 (the lift)', 'clock out': 'FX1', 'm1': 'FX1 (meeting arrows)', 'm4': 'FX3 (Hauling) and FX1',
        'm3d': 'FX2 (the drill)', 'm3i': 'the arrows plan (Day 4 warning) and FX1', 'm5': 'FX1 (meeting arrows) and FX2 (Tuning)', 'm7': 'FX2 (the scanner job)',
        'p3': 'FX2 (the scanner job) and piece C (Fault notes pointers)', 'm6': 'FX3 (the burst pipe) and FX2 (the scanner count)', 'scan': 'FX2', 'stale': 'FX1 (arrows that never clear)', 'need': 'section 15 (the needs arrow): nobody yet' }

def stuck_fix(lab):                                  # who should turn a "stuck at" line green
    if lab.startswith(('A shower', 'A toilet', 'Food', 'Your bunk')): return FIX['need']
    if 'main lift' in lab: return 'FX3 (the lift service)'
    if 'galley plant' in lab: return 'nobody yet (the calibrate chore: its pin sits where the chiller takes the tap; the label says Repair)'
    return FIX['stuck']

class Follower:
    def __init__(self, pg): self.pg = pg; self.acts = []; self.same = None; self.stuck = []; self.long = []
    def run(self, until_min_abs, every=6):
        pg = self.pg
        while pg.ev('shipNow()') < until_min_abs:
            pg.step(every, 50)
            r = pg.ev(FOLLOW)
            if isinstance(r, dict) and r.get('click'):
                pg.page.mouse.click(*r['click']); pg.step(2, 50); r = 'tap the floor at the pin: ' + r['label'] + (' (working)' if pg.ev('!!ACT') else '')
            if r: self.acts.append((pg.ev('clockText()'), r))
            s = pg.ev("(() => { const g = goalNow(); return [Math.floor(shipNow()), g ? g.label : null, player.here().join(','), deckDef.num, !!ACT || !!(DIALOGUE)]; })()")
            if s[4] and self.same: self.same = (s[0], self.same[1], self.same[2], self.same[3]); continue   # busy (working, a meeting): not stuck
            if s[1]:
                if self.same and self.same[1] == s[1]:
                    if s[2] == self.same[2] and s[0] - self.same[0] >= 45 and not any(x[1] == s[1] and x[0] == self.same[0] for x in self.stuck): self.stuck.append((self.same[0], s[1], s[3]))
                    if s[0] - self.same[3] >= 180 and not any(x[1] == s[1] for x in self.long): self.long.append((self.same[3], s[1]))
                    if s[2] != self.same[2]: self.same = (s[0], s[1], s[2], self.same[3])
                else: self.same = (s[0], s[1], s[2], s[0])
            else: self.same = None
    def night(self, day):                               # to bed: the next morning, rested
        self.pg.ev(f"devmodeSkipTo({day * 1440 + 5 * 60 + 50}); for (const k of NEED_KEYS) SHIP.player.needs[k] = Math.max(SHIP.player.needs[k], 85)"); self.pg.step(10)

def real_game(pg, day):                               # the career set to the end of day-1, tracking as in a real game
    pg.ev(f"devmodeRun('Set career', () => devmodeSetCareerTo({day - 1}))"); pg.step(20)
    if TEACHOFF: pg.ev("SHIP.device.settings.teach = 'off'")   # Settings' Teaching arrows: Off (the everyday arrows stay)
    if GUIDE: pg.ev("if (!GUIDE_ON) { GUIDE_ON = true; guideStart(); }")   # the arrow queue on (a build from 0.92.0 has it on already: no override) (its training arrows T1-T3; pieces D-F as they land)
    pg.ev(f"devmodeSkipTo({(day - 1) * 1440 + 5 * 60 + 50}); clearGoal(); SHIP.player.track = 'arrows-check-yesterday'; for (const k of NEED_KEYS) SHIP.player.needs[k] = Math.max(SHIP.player.needs[k], 85)"); pg.step(10)   # a normal evening before: washed, fed, rested

def arrows_off(src):                                 # the build with the teaching arrows switched off (as before 0.92.0), for the parts that test "off"
    return src.replace('const POINT_ON = true;', 'const POINT_ON = false;', 1).replace('var GUIDE_ON = true;', 'var GUIDE_ON = false;', 1)

def hhmm(m): m = int(m) % 1440; return f'{m // 60:02d}:{m % 60:02d}'

def part_shift(ctx, path):
    pg = Page(ctx, path); real_game(pg, 9); f = Follower(pg)
    f.run(8 * 1440 + 9 * 60 + 5); s = json.loads(json.dumps(pg.ev(STATE)))
    check(s['inn'], f'shift: not clocked in by 09:05 following the arrow (fix: {FIX["clock in"]}); arrow now "{s["arrow"]}"')
    f.run(8 * 1440 + 17 * 60 + 40); s = pg.ev(STATE)
    check(s['done'] >= 3, f'shift: {s["done"]} jobs turned in on Day 9 following the arrow (want 3 or more)')
    out = pg.ev("(() => { const L = SHIP.mail.filter(m => /didn.t clock out/i.test(m.subject || '')); return L.length; })()")
    check(s['out'] and not out, f'shift: not clocked out by the player at the end (clocked out: {s["out"]}, the clock signed you out: {bool(out)}) (fix: {FIX["clock out"]})')   # careerClockedIn stays true after clocking out (AC2)
    for t, lab, dk in f.stuck: fail(f'shift: stuck from {hhmm(t)} at "{lab}" (Deck {dk}): the arrow points where nothing can be done (fix: {stuck_fix(lab)})')
    print(f'  shift: Day 9, {s["done"]} jobs, stuck {len(f.stuck)}; last actions: {[a[1] for a in f.acts[-4:]]}')
    check(not pg.errors, f'shift: page errors {pg.errors[:3]}')
    pg.page.close()

WEEK = [(2, ['m1']), (3, ['m4', 'm3d']), (4, ['m3i', 'm5']), (5, ['m7', 'p3'])]
# The scanner's first counted use is your first faulty-machine job after the Day 5 lesson (the lesson's own reading doesn't
# count), so it comes when the board has one: Day 5's afternoon, else the next workday. Making it safe (m6) needs that use
# and opens at a day's start from Day 8: on Day 8, or on the first workday after the use (FX6 for lead 31, 0.92.1: with
# the Line on, Friday Day 5's board was all chores, the first use came on Day 8 and m6 on Day 9; backlog LEAD31-11)
def part_week(ctx, path):
    pg = Page(ctx, path); real_game(pg, 2); f = Follower(pg)
    want = dict(WEEK); fails = []
    workday = lambda d: bool(pg.ev(f"playerShiftOn({d})"))
    use_by = next(x for x in range(6, 20) if workday(x))   # the scanner used by the next workday after Day 5
    used, m6_by, last, d = None, None, 8, 1
    while d < last:
        d += 1
        f.run((d - 1) * 1440 + 21 * 60 + 30)   # a day after Day 8 (Making it safe) runs whole too: LEAD31-14 (FX6) fixed its evening's "Food" arrow with a tray in hand
        s = pg.ev(STATE)
        work = pg.ev(f"playerShiftOn({d})")
        log = pg.ev(f"(SHIP.player.clockLog || {{}})[{d}] || 0")
        if work: check(log > 0, f'week: Day {d}: never clocked in following the arrow (fix: {FIX["clock in"]})')
        for m in want.get(d, []):
            check(s['tr'].get(m) is not None, f'week: Day {d}: "{m}" not learned by following the arrow (fix: {FIX.get(m, "?")}); training {s["cur"]}, opened {s["op"].get(str(d))}')
        if used is None and d >= 5 and (s['use'].get('m7') or 0) >= 1:
            used = d; m6_by = next(x for x in range(max(8, d + 1), 30) if workday(x)); last = max(last, m6_by)
        if used is None and d == use_by: check(False, f'week: the scanner never counted as used by Day {use_by}, the next workday after its lesson (fix: {FIX["scan"]})')
        if m6_by is not None and d == m6_by:
            opened = sorted(int(k) for k, v in s['op'].items() if 'm6' in v)
            check(bool(opened) and opened[0] <= m6_by, f'week: Making it safe did not open by Day {m6_by} (the scanner first used on Day {used}) (fix: {FIX["m6"]})')
            check(s['tr'].get('m6') is not None, f'week: Day {d}: "m6" not learned by following the arrow (fix: {FIX["m6"]}); training {s["cur"]}, opened {s["op"].get(str(d))}')
        print(f'  week: Day {d}: learned {sorted(k for k in s["tr"])}, training {s["cur"]}, clocked {log} min, stuck so far {len(f.stuck)}' + (f'; the scanner first used Day {used}, Making it safe due by Day {m6_by}' if used == d else ''))
        f.night(d)
    if used is None and last < use_by: check(False, f'week: the scanner never counted as used (fix: {FIX["scan"]})')
    for t, lab, dk in f.stuck: fail(f'week: stuck from Day {t // 1440 + 1} {hhmm(t)} at "{lab}" (Deck {dk}) (fix: {stuck_fix(lab)})')
    for t, lab in f.long: fail(f'week: the arrow "{lab}" stayed up over 3 ship hours from Day {t // 1440 + 1} {hhmm(t)} (fix: {FIX["stale"]})')
    check(not pg.errors, f'week: page errors {pg.errors[:3]}')
    pg.page.close()

def part_clockin(ctx, path):                              # patch 0.92.3 item 6 (AC3; RV12's lines): Days 1-3, into the Works bay before clocking in
    pg = Page(ctx, path)
    pg.ev("localStorage.clear()"); pg.ev("newGameStart(true)"); pg.step(5)
    pg.page.fill('form input[maxlength="24"]', 'Sam'); pg.page.click('form button'); pg.step(5)
    IN_BAY = """(() => { if (DIALOGUE) dialogueEnd(); goToDeck(5); SHIP.device.settings.tips = true; const s = placeSpot('5-timeclock-1'),
      t = (ROOM_TILES.w || []).map(c => cellPos(...c)).filter(w => Math.hypot(w.x - s.x, w.z - s.z) > 5)[0]; player.obj.position.copy(t); player.stop(); })()"""
    LOOK = "(() => ({ tip: TIP_Q[0] ? TIP_Q[0].id : null, clockTips: TIP_Q.filter(t => /^career\\.clock/.test(t.id)).map(t => t.id), trk: IX_GOAL ? IX_GOAL.trk || null : null }))()"
    pg.ev("skipTo(introAbs(1, 8 * 60 + 30))"); pg.ev(IN_BAY); pg.step(10); a = pg.ev(LOOK)
    check(a['trk'] == 'clock:in' and not a['clockTips'], f'clockin: Day 1 into the Works bay: Clock in tracked, and no clock-in tip before Zeke says it ({a})')
    pg.ev("SHIP.intro.done['d1-opener'] = Math.floor(shipNow())"); pg.step(5); b = pg.ev(LOOK)
    check(b['tip'] == 'career.clock.1', f'clockin: Day 1 after Zeke\'s line: the clock-in tip on screen at once ({b})')
    pg.ev("careerClock(shipNow())"); pg.step(3); c = pg.ev(LOOK)
    check(c['trk'] != 'clock:in' and not c['clockTips'], f'clockin: clocked in: its arrow and its tip gone at once ({c})')
    pg.ev("skipTo(introAbs(2, 8 * 60 + 20))"); pg.ev(IN_BAY); pg.step(10); d = pg.ev(LOOK)
    check(d['tip'] == 'career.clock.2' and d['trk'] == 'clock:in', f'clockin: Day 2 at 08:20 into the Works bay: the tip on screen and Clock in tracked ({d})')
    pg.ev("clearGoal(); skipTo(introAbs(3, 8 * 60 + 20)); SHIP.device.settings.teach = 'off'"); pg.ev(IN_BAY); pg.step(10); e = pg.ev(LOOK)   # (Day 2's arrow, still due, would carry over)
    check(e['tip'] == 'career.clock.3' and e['trk'] != 'clock:in', f'clockin: Day 3 with Teaching arrows Off: the tip, no tracked arrow ({e})')
    check(not pg.errors, f'clockin: page errors {pg.errors[:3]}')
    print(f'  clockin: Day 1 {a} -> {b} -> {c}; Day 2 {d}; Day 3 (Off) {e}')
    pg.page.close()

GUIDE = 'guide' in sys.argv[2:]                       # run shift and week with the arrow queue switched on
TEACHOFF = 'teachoff' in sys.argv[2:]                 # with 'guide': Settings' Teaching arrows set to Off
PARTS = set(a for a in sys.argv[2:] if a not in ('guide', 'teachoff')) or {'queue', 'clockin', 'shift', 'week'}
with sync_playwright() as pw:
    path = sys.argv[1]; src = pathlib.Path(path).read_text(); off = arrows_off(src)
    if off != src: (WORK / 'test' / ('_off_' + pathlib.Path(path).name)).write_text(off)
    off_path = str(WORK / 'test' / ('_off_' + pathlib.Path(path).name)) if off != src else path   # queue's 'off' part, and shift / week without 'guide': the arrows switched off
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    if 'queue' in PARTS:
        print('== queue (piece B)')
        try:
            pg = Page(ctx, off_path); pg.day2()
            if not check(pg.ev("typeof guideAsk === 'function' && typeof GUIDE_ON !== 'undefined'"), 'no arrow queue in this build'): raise SystemExit
            part_off(pg); part_queue(pg); part_toasts(pg)
            check(not pg.errors, f'queue: page errors {pg.errors[:3]}')
            pg.page.close()
            part_once(ctx, off_path)
        except SystemExit: pass
        except Exception as e: fail(f'queue: stopped: {str(e)[:300]}')
    if 'clockin' in PARTS:
        print('== clockin (patch 0.92.3 item 6)')
        try: part_clockin(ctx, path)
        except Exception as e: fail(f'clockin: stopped: {str(e)[:300]}')
    for name, part in (('shift', part_shift), ('week', part_week)):
        if name not in PARTS: continue
        print(f'== {name} (following only the arrow)')
        try: part(ctx, path if GUIDE else off_path)
        except Exception as e: fail(f'{name}: stopped: {str(e)[:300]}')
    b.close()

print('ARROWS CHECK OK' if ok else 'ARROWS CHECK FAILED')
sys.exit(0 if ok else 1)
