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
#             teaching entries, 'off' refuses teaching entries
#   toasts:   five pop-ups in one frame show in order, each for at least 2.5 s, at most 3 waiting, repeats merged; an
#             urgent one ({ now: true }) at once
#   settings: the Teaching arrows row (All / First time only / Off) under Tips, saved
#   size:     SHIP.guide in the save stays small with 400 seen ids (300 kept)
# Later parts (pieces C-F) add the pointer and the played shift and lessons, following only the arrow.
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
    pg.ev("deviceShow('settings')"); pg.step(2)
    txt = pg.ev("document.getElementById('devBody').textContent")
    check('Teaching arrows' not in txt, 'off: the Settings row shows with the queue off')
    pg.ev("deviceClose()")
    pg.ev('saveGame()'); sv = pg.ev("JSON.parse(localStorage.getItem(SAVE_KEY))")
    check(sv is not None and 'guide' not in sv, f'off: the save has a guide key ({sorted(sv)[:8] if sv else sv})')
    print('  off: inert, toast at once, no Settings row, no save key')

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
    ask(pg, id='d2', level=2); a = shown(pg); ask(pg, id='d1', level=1); b = shown(pg); done(pg, 'd1'); c = shown(pg)
    check(a == 'mine' and b == 'd1' and c == 'mine', f'direct: {a}, {b}, {c}')
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
    pg.ev("GUIDE_ON = true; SHIP.guide.seen = {}; SHIP.guide.arrows = 'first'; window.__d = {}")
    counts = []
    for k in range(3):
        r = ask(pg, id='twice', level=3, once=2); s = shown(pg); counts.append((r, s))
        done(pg, 'twice'); shown(pg); pg.ev("window.__d = {}")
        if k == 0:
            pg.ev('saveGame()'); pg.reload(); pg.ev("GUIDE_ON = true; window.__d = {}; clearGoal()")
    check(counts[0] == (True, 'twice') and counts[1] == (True, 'twice') and counts[2][0] is False, f'once: {counts}')
    check(pg.ev("SHIP.guide.seen.twice") == 2, f'once: seen {pg.ev("SHIP.guide.seen.twice")}')
    pg.ev("SHIP.guide.arrows = 'all'"); r = ask(pg, id='twice', level=3, once=2); check(r, "once: 'all' should ignore once for teaching")
    pg.ev("guideDrop('twice'); SHIP.guide.arrows = 'off'"); r3 = ask(pg, id='t3', level=3); r2 = ask(pg, id='t2', level=2)
    check(r3 is False and r2 is True, f"once: 'off' should refuse level 3 only ({r3}, {r2})")
    pg.ev("SHIP.guide.arrows = 'first'")
    # settings row
    pg.ev("deviceShow('settings')"); pg.step(2)
    txt = pg.ev("document.getElementById('devBody').textContent")
    check('Teaching arrows' in txt and 'First time only' in txt, f'settings: no Teaching arrows row: {txt[:200]}')
    order = pg.ev("(() => { const t = document.getElementById('devBody').textContent; return [t.indexOf('Tips'), t.indexOf('Teaching arrows'), t.indexOf('Quiet off shift')]; })()")
    check(order[0] < order[1] < order[2], f'settings: the row should sit under Tips: {order}')
    pg.ev("deviceDo({ app: 'settings', do: 'arrows', arg: 'off' })"); check(pg.ev("SHIP.guide.arrows") == 'off', 'settings: the Off button did not set it')
    pg.ev("deviceDo({ app: 'settings', do: 'tips', arg: true })"); check(pg.ev("SHIP.guide.arrows") == 'off', 'settings: another setting changed it')
    pg.ev('saveGame()'); pg.reload()
    check(pg.ev("SHIP.guide.arrows") == 'off', 'settings: not kept by the save')
    pg.ev("GUIDE_ON = true; SHIP.guide.seen = {}; for (let i = 0; i < 400; i++) SHIP.guide.seen['id' + i] = 1; saveGame()")
    sv = pg.ev("JSON.parse(localStorage.getItem(SAVE_KEY)).guide")
    check(sv and len(sv['seen']) == 300 and len(json.dumps(sv)) < 4000, f'size: {len(sv["seen"]) if sv else None} ids, {len(json.dumps(sv)) if sv else 0} bytes')
    check(not pg.errors, f'once: page errors {pg.errors[:3]}')
    pg.page.close()
    print('  once, settings, size: twice then refused across a reload; all / off; the Settings row under Tips, saved; 300 ids kept, under 4 KB')

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
    pg.ev("toast('U1', 'x'); toast('U2', 'urgent', { now: true })")
    check(pg.ev("document.getElementById('tt').textContent") == 'U2', 'toasts: an urgent one waited')
    pg.ev("GUIDE_ON = false; PAUSE.on = false"); pg.step(3)
    check(pg.ev('GUIDE.tq.length') == 0 and not pg.ev('GUIDE.loop'), 'toasts: switching off left the queue running')
    print(f'  toasts: {names}, gaps {gaps} ms; urgent at once')

with sync_playwright() as pw:
    path = sys.argv[1]
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    print('== queue (piece B)')
    try:
        pg = Page(ctx, path); pg.day2()
        if not check(pg.ev("typeof guideAsk === 'function' && typeof GUIDE_ON !== 'undefined'"), 'no arrow queue in this build'): raise SystemExit
        part_off(pg); part_queue(pg); part_toasts(pg)
        check(not pg.errors, f'queue: page errors {pg.errors[:3]}')
        pg.page.close()
        part_once(ctx, path)
    except SystemExit: pass
    except Exception as e: fail(f'stopped: {str(e)[:300]}')
    b.close()

print('ARROWS CHECK OK' if ok else 'ARROWS CHECK FAILED')
sys.exit(0 if ok else 1)
