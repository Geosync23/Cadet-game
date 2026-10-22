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
# in for the walk), tap the thing it points at, press the button a panel offers (the clock screen's, the board's Take it /
# Turn it in, a meeting's Go on, a card's choices in turn), read meetings through, sleep at night.
#   shift: one ordinary workday (Day 9, nothing new taught): clocked in by 09:05, at least three jobs turned in, never
#          stuck (the arrow on the same spot for 45 ship minutes with the player there), clocked out by the player
#   week:  Days 2-8 in a row: clocked in every workday; each lesson learned on its day by following the arrow (Rounds
#          Day 2, Hauling and the drill Day 3, the inspection and Tuning Day 4, the scanner and the first head-scratcher
#          Day 5); the scanner counted as used; Making it safe opened on Day 8 and learned; no arrow left up after its
#          moment (the same label for over 3 ship hours)
# On 0.64.15 (2b4a05db) both FAIL: that is the point. Which fixer turns which line green is printed with each FAIL.
# Run one part:  python3 arrows_check.py BUILD.html shift   (parts: queue, shift, week; default all, about 15 minutes)
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
    print('  done: until, done, a throw dropped; from waits')
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
    pg.ev("toast('U1', 'x'); toast('U2', 'urgent', { now: true })")
    check(pg.ev("document.getElementById('tt').textContent") == 'U2', 'toasts: an urgent one waited')
    pg.ev("GUIDE_ON = false; PAUSE.on = false"); pg.step(3)
    check(pg.ev('GUIDE.tq.length') == 0 and not pg.ev('GUIDE.loop'), 'toasts: switching off left the queue running')
    print(f'  toasts: {names}, gaps {gaps} ms; urgent at once')


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
  if (typeof pointNow === 'function') { try { const p = pointNow(); const el = p && p.el && p.el(); if (el && el.offsetParent !== null) { el.click(); return 'pointer: ' + (el.textContent || '').slice(0, 30); } } catch (e) { /* piece C */ } }
  if (ACT) return null;
  const cs = document.getElementById('clockScreen');
  if (cs && !cs.hidden && getComputedStyle(cs).display !== 'none') {
    const gl = (goalNow() || {}).label || '', want = /clock out|shift over/i.test(gl) ? /clock out/i : /clock in/i;
    const b = [...cs.querySelectorAll('button')].find(b => want.test(b.textContent)) || [...cs.querySelectorAll('button')].find(b => /close/i.test(b.textContent));
    if (b) { const t = b.textContent; b.click(); return 'clock screen: ' + t; }
  }
  const bd = document.getElementById('ixBoard');
  if (bd && !bd.hidden) { const b = [...bd.querySelectorAll('#ixBoardL button')].find(b => /turn it in/i.test(b.textContent)) || [...bd.querySelectorAll('#ixBoardL button')].find(b => /take/i.test(b.textContent));
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
  const pin = () => { const v = new THREE.Vector3(w.x, .05, w.z).project(camera); return { click: [(v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight], label: g.label }; };
  if (window.__tapKey2 === key) return pin();             // the thing didn't answer: a real tap on the floor at the pin, as a player would
  if (it && it[2] < 2.5) { const r = playerTap(it[0], it[1].clone(), it[1].clone()); if (!r) window.__tapKey2 = key; return 'tap ' + it[0].t + ': ' + r; }
  return pin();
})()"""
STATE = r"""(() => { const W = SHIP.works, d = SHIP.time.day, g = goalNow();
  return { clock: clockText(), day: d, min: Math.floor(SHIP.time.min), arrow: g ? g.label : null, deck: deckDef.num, at: player.here().join(','),
    tr: W ? Object.assign({}, W.tr) : {}, use: W ? Object.assign({}, W.use) : {}, op: W ? W.op : {}, cur: W && W.cur ? W.cur.id + ':' + W.cur.st : null,
    inn: typeof careerClockedIn === 'function' ? !!careerClockedIn(d) : null, log: (SHIP.player.clockLog || {})[d] || 0,
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
    pg.ev(f"devmodeSkipTo({(day - 1) * 1440 + 5 * 60 + 50}); clearGoal(); SHIP.player.track = 'arrows-check-yesterday'; for (const k of NEED_KEYS) SHIP.player.needs[k] = Math.max(SHIP.player.needs[k], 85)"); pg.step(10)   # a normal evening before: washed, fed, rested

def hhmm(m): m = int(m) % 1440; return f'{m // 60:02d}:{m % 60:02d}'

def part_shift(ctx, path):
    pg = Page(ctx, path); real_game(pg, 9); f = Follower(pg)
    f.run(8 * 1440 + 9 * 60 + 5); s = json.loads(json.dumps(pg.ev(STATE)))
    check(s['inn'], f'shift: not clocked in by 09:05 following the arrow (fix: {FIX["clock in"]}); arrow now "{s["arrow"]}"')
    f.run(8 * 1440 + 17 * 60 + 40); s = pg.ev(STATE)
    check(s['done'] >= 3, f'shift: {s["done"]} jobs turned in on Day 9 following the arrow (want 3 or more)')
    out = pg.ev("(() => { const L = SHIP.mail.filter(m => /didn.t clock out/i.test(m.subject || '')); return L.length; })()")
    check(not s['inn'] and not out, f'shift: not clocked out by the player at the end (still in: {s["inn"]}, the clock signed you out: {bool(out)}) (fix: {FIX["clock out"]})')
    for t, lab, dk in f.stuck: fail(f'shift: stuck from {hhmm(t)} at "{lab}" (Deck {dk}): the arrow points where nothing can be done (fix: {stuck_fix(lab)})')
    print(f'  shift: Day 9, {s["done"]} jobs, stuck {len(f.stuck)}; last actions: {[a[1] for a in f.acts[-4:]]}')
    check(not pg.errors, f'shift: page errors {pg.errors[:3]}')
    pg.page.close()

WEEK = [(2, ['m1']), (3, ['m4', 'm3d']), (4, ['m3i', 'm5']), (5, ['m7', 'p3']), (8, ['m6'])]
def part_week(ctx, path):
    pg = Page(ctx, path); real_game(pg, 2); f = Follower(pg)
    want = dict(WEEK); fails = []
    for d in range(2, 9):
        f.run((d - 1) * 1440 + 21 * 60 + 30)
        s = pg.ev(STATE)
        work = pg.ev(f"playerShiftOn({d})")
        log = pg.ev(f"(SHIP.player.clockLog || {{}})[{d}] || 0")
        if work: check(log > 0, f'week: Day {d}: never clocked in following the arrow (fix: {FIX["clock in"]})')
        for m in want.get(d, []):
            check(s['tr'].get(m) is not None, f'week: Day {d}: "{m}" not learned by following the arrow (fix: {FIX.get(m, "?")}); training {s["cur"]}, opened {s["op"].get(str(d))}')
        if d == 5: check((s['use'].get('m7') or 0) >= 1, f'week: Day 5: the scanner never counted as used (fix: {FIX["scan"]})')
        if d == 8: check('m6' in (s['op'].get('8') or []), f'week: Day 8: Making it safe did not open (fix: {FIX["m6"]})')
        print(f'  week: Day {d}: learned {sorted(k for k in s["tr"])}, training {s["cur"]}, clocked {log} min, stuck so far {len(f.stuck)}')
        f.night(d)
    for t, lab, dk in f.stuck: fail(f'week: stuck from Day {t // 1440 + 1} {hhmm(t)} at "{lab}" (Deck {dk}) (fix: {stuck_fix(lab)})')
    for t, lab in f.long: fail(f'week: the arrow "{lab}" stayed up over 3 ship hours from Day {t // 1440 + 1} {hhmm(t)} (fix: {FIX["stale"]})')
    check(not pg.errors, f'week: page errors {pg.errors[:3]}')
    pg.page.close()

PARTS = set(sys.argv[2:]) or {'queue', 'shift', 'week'}
with sync_playwright() as pw:
    path = sys.argv[1]
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    if 'queue' in PARTS:
        print('== queue (piece B)')
        try:
            pg = Page(ctx, path); pg.day2()
            if not check(pg.ev("typeof guideAsk === 'function' && typeof GUIDE_ON !== 'undefined'"), 'no arrow queue in this build'): raise SystemExit
            part_off(pg); part_queue(pg); part_toasts(pg)
            check(not pg.errors, f'queue: page errors {pg.errors[:3]}')
            pg.page.close()
            part_once(ctx, path)
        except SystemExit: pass
        except Exception as e: fail(f'queue: stopped: {str(e)[:300]}')
    for name, part in (('shift', part_shift), ('week', part_week)):
        if name not in PARTS: continue
        print(f'== {name} (following only the arrow)')
        try: part(ctx, path)
        except Exception as e: fail(f'{name}: stopped: {str(e)[:300]}')
    b.close()

print('ARROWS CHECK OK' if ok else 'ARROWS CHECK FAILED')
sys.exit(0 if ok else 1)
