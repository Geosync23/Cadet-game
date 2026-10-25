# Starship Cadet: sound check (section 27, the SND block; plans/sound/integration-plan.md "Checks to add")
# Sound is silent in every other check (webdriver). Here the game is opened with ?sound&soundlog, which lets SND start
# on a real (Playwright) click and keeps a list of what it played in SND.log.
# The builders each add their own check functions and one entry each to CHECKS at the bottom:
#   core (SD1): silent by default; starts on a tap with ?sound; Settings rows; pause/hidden suspend; SND.fx never draws on
#   R(); the hum and the core hooks (turns 2-5)
#   activities (FX20) and music (FX22b): their own functions
# Setup and environment as for cadet_test.py.  Run:  python3 sound_check.py BUILD.html
import sys, os, pathlib, json
exec(open(__file__.replace('sound_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

ok = True
def check(cond, msg):
    global ok
    if not cond: ok = False; print('FAIL', msg)
    return cond

def open_with(g, query):
    """Reopen the game's page with another query (the Game class opens it with ?nosave&debug)."""
    g.page.goto('file://' + str(g.tmp) + query)
    g.page.wait_for_function('window.__sc !== undefined || window.__err', timeout=60000)

def click_world(g):
    g.page.mouse.click(450, 380)   # a real (trusted) tap on the ship
    g.step(3)

# ---- core (SD1) ----
def check_silent_by_default(pw, path):
    g = Game(pw, path)
    try:
        g.step(30); click_world(g)
        st = g.ev("({ allowed: SND._.allowed, state: SND._.state(), ctx: !!SND.ctx })")
        check(st['allowed'] is False and st['ctx'] is False and st['state'] == 'off', f'silent under webdriver: {st}')
    finally: g.close()

def check_start_and_fx(pw, path):
    g = Game(pw, path)
    try:
        open_with(g, '?nosave&debug&sound&soundlog'); g.step(30)
        check(g.ev('SND.ctx === null'), 'nothing starts before a tap')
        click_world(g)
        check(g.ev('!!SND.ctx'), 'a tap starts the sound')
        seed0 = g.ev('seed')
        names = g.ev('Object.keys(SND._.FX)')
        for n in ['tap', 'open', 'close', 'no', 'jobPosted', 'jobDone', 'mail', 'heads', 'doorOpen', 'doorClose', 'hatchOpen', 'hatchClose',
                  'liftPress', 'liftDoorsOpen', 'liftDoorsClose', 'liftRide', 'liftArrive', 'step']:
            check(n in names, f'core sound {n} is registered')
        g.ev("SND.log.length = 0; for (let k = 0; k < 200; k++) SND.fx(['tap', 'mail', 'doorOpen', 'step'][k % 4], { surface: 'plate' })")
        check(g.ev('seed') == seed0, 'SND.fx never draws on R()')
        check(g.ev('SND.log.length') == 200, 'every fx call is logged with ?soundlog')
        far = g.ev("(() => { const p = player.obj.position; SND.log.length = 0; SND.fx('doorOpen', { x: p.x + 20, z: p.z }); return SND.log.length; })()")
        check(far == 0, 'a door 20 tiles away plays nothing')
        near = g.ev("(() => { const p = player.obj.position; SND.log.length = 0; SND.fx('doorOpen', { x: p.x + 3, z: p.z }); SND.fx('doorOpen', { x: p.x, z: p.z }); return SND.log.map(e => e.g); })()")
        check(len(near) == 2 and near[0] < near[1], f'a nearer door is louder: {near}')
    finally: g.close()

def check_settings_rows(pw, path):
    g = Game(pw, path)
    try:
        open_with(g, '?nosave&debug&sound&soundlog'); g.step(30)
        txt = g.ev("JSON.stringify(SND.settingsBlocks())")
        check('Sound' in txt and 'Volume' in txt and 'Medium' in txt, 'Settings has Sound and Volume rows')
        view = g.ev("JSON.stringify(DEV.apps ? (DEV.apps.settings || {}).id || '' : '')")
        on = g.ev("(() => { SND.settingsAct('sound', false); const a = SND.prefs.on; SND.settingsAct('sound', true); SND.settingsAct('soundvol', 'high'); return [a, SND.prefs.on, SND.prefs.vol]; })()")
        check(on == [False, True, 'high'], f'Sound Off/On and Volume change the settings: {on}')
    finally: g.close()

def check_pause_suspends(pw, path):
    g = Game(pw, path)
    try:
        open_with(g, '?nosave&debug&sound&soundlog'); g.step(30); click_world(g)
        g.page.wait_for_function("window.__sc('SND._.state()') === 'running'", timeout=10000)
        g.ev('pauseSet(true)'); g.step(5)
        g.page.wait_for_function("window.__sc('SND._.state()') === 'suspended'", timeout=10000)
        check(g.ev("SND._.state()") == 'suspended', 'pause suspends the sound')
        g.ev('pauseSet(false)'); g.step(5)
        g.page.wait_for_function("window.__sc('SND._.state()') === 'running'", timeout=10000)
        check(g.ev("SND._.state()") == 'running', 'resume runs it again')
    finally: g.close()

def check_core_hooks(pw, path):
    """turns 2-5: the hum by deck, doors (yours and crew, near only), the lift, footsteps, Mail, a heads-up; seed untouched"""
    g = Game(pw, path)
    try:
        open_with(g, '?nosave&debug&sound&soundlog'); g.step(30); click_world(g)
        g.page.wait_for_function("window.__sc('SND._.state()') === 'running'", timeout=10000)
        g.page.wait_for_timeout(800); g.step(5)   # the hum is checked twice a second (real time)
        hums = g.ev("SND.log.filter(e => e.name.startsWith('hum:')).map(e => e.name)")
        check(len(hums) >= 1, f'a deck hum starts: {hums}')
        g.ev('goToDeck(3)'); g.page.wait_for_timeout(700); g.step(5)
        check(g.ev("SND.log.some(e => e.name === 'hum:commons')"), 'Deck 3 gets the Commons hum')
        g.ev('goToDeck(6)'); g.page.wait_for_timeout(700); g.step(5)
        check(g.ev("SND.log.some(e => e.name === 'hum:engine')"), 'Deck 6 gets the Engineering hum')
        g.ev('goToDeck(4)'); g.page.wait_for_timeout(700); g.step(5)
        # a door next to you opening and closing (driven by hand: open goes 0 -> 1 -> 0)
        res = g.ev("""(() => { const d = DOOR_OBJS.find(x => x.e.type !== 'lift' && !x.svc); if (!d) return null;
          player.obj.position.set(d.cx + 0.5, 0, d.cz); SND.log.length = 0; return [d.cx, d.cz]; })()""")
        if check(res is not None, 'Deck 4 has a door to test'):
            for v in (0.0, 0.5, 1.0, 0.5):
                g.ev(f"(() => {{ const d = DOOR_OBJS.find(x => x.e.type !== 'lift' && !x.svc); d.open = {v}; d.force = {1 if v >= 0.5 else 0}; }})()"); g.step(1)
            names = g.ev("SND.log.map(e => e.name + (e.crew ? ':crew' : ''))")
            check(names.count('doorOpen') == 1 and names.count('doorClose') == 1 and not any(':crew' in n for n in names), f'your door opening and closing play once each: {names}')
            g.ev("DOOR_OBJS.forEach(d => delete d.force)")
        # footsteps: walk the player along by hand
        g.ev("SND.log.length = 0"); g.step(2)
        for k in range(30):
            g.ev("player.obj.position.x += 0.09"); g.step(1)
        steps = g.ev("SND.log.filter(e => e.name === 'step').length")
        check(3 <= steps <= 6, f'about one step every 0.62 tiles walked: {steps} for 2.7 tiles')
        # Mail and a heads-up
        g.ev("SND.log.length = 0; SHIP.mail.push({ at: 0, from: 'Test', subject: 'Test', body: 'Test', read: false })"); g.step(3)
        check(g.ev("SND.log.some(e => e.name === 'mail')"), 'new Mail plays the Mail sound')
        # SND's own per-frame watcher, driven by hand with no game frames between (the game's frames draw on R() themselves)
        same = g.ev("""(() => { const s0 = seed, d = DOOR_OBJS.find(x => x.e.type !== 'lift');
          for (let k = 0; k < 60; k++) { player.obj.position.x += 0.05; if (d) d.open = k % 20 < 10 ? 1 : 0; SND.onFrame.forEach(f => f(true)); }
          SHIP.mail.push({ at: 0, from: 'Test', subject: 'Seed', body: 'x', read: false }); SND.onFrame.forEach(f => f(true));
          return seed === s0; })()""")
        check(same, "SND's watcher never draws on R()")
        ticks = g.ev("(() => { window.__t = [0, 0]; SND.actTick = () => window.__t[0]++; SND.musicTick = () => window.__t[1]++; return 1; })()")
        g.page.wait_for_timeout(2300); g.step(3); g.page.wait_for_timeout(1100); g.step(3)
        t = g.ev('window.__t'); g.ev('SND.actTick = SND.musicTick = null')
        check(t[0] >= 1 and t[1] >= 1, f'the slots get their once-a-second ticks: {t}')
        g.ev("SND.log.length = 0; (() => { const b = ROOM_BOX['@']; if (b) player.obj.position.copy(cellPos(b.i0 + 1, b.j0 + 1)); })(); startRide(3)")
        g.step(80)
        lift = g.ev("SND.log.map(e => e.name).filter(n => n.startsWith('lift'))")
        check(lift == ['liftPress', 'liftDoorsClose', 'liftRide', 'liftArrive', 'liftDoorsOpen'], f'the lift: press, doors shut, ride, arrival, doors open, once each: {lift}')
    finally: g.close()

# ---- activities (FX20): the approved activity sounds, what each activity plays, the hooks, and never R() ----
ACT_NAMES = ['ratchet', 'panelOff', 'panelOn', 'partSwap', 'torch', 'scanA', 'vent', 'unstick', 'hingeSqueak', 'hingeOil', 'drain', 'wipe', 'cratePick', 'crateSet',
             'typing', 'drill', 'cartDock', 'valve', 'hold', 'relay', 'flushVac', 'showerOff', 'sink', 'towel', 'callRing', 'hangUp', 'wardrobe', 'changing', 'hamper',
             'bedLie', 'makeBed', 'sitChair', 'sitCouch', 'cup', 'tray', 'badge', 'locker', 'page', 'pencil', 'knit', 'trayPick', 'pour', 'bench', 'splash', 'kayak',
             'climb', 'discThrow', 'piano', 'guitar', 'tileShuffle', 'telescope', 'watering', 'storm', 'announce', 'flicker', 'clockIn', 'clockOut', 'hello']
# what an activity plays: [kind, extra fields on A.o, expected at the start, the loop, expected at its end]
ACT_CASES = [['shower', {}, None, 'shower', 'showerOff'], ['toilet', {}, None, None, 'flushVac'], ['call', {}, 'callRing', None, 'hangUp'],
             ['gym', {'title': 'Treadmill'}, None, 'treadmill', None], ['gym', {'title': 'Weights bench'}, 'bench', None, None], ['lie', {}, 'bedLie', None, None],
             ['eat', {'fed': True}, 'tray', None, None], ['recSwim', {}, 'splash', 'swim', None], ['recFloat', {}, None, 'float', None], ['pay', {}, 'badge', None, None],
             ['workStep', {'how': 'look'}, 'scanA', None, None], ['workStep', {'how': 'turn'}, 'valve', None, None], ['ixTea', {}, 'cup', None, None]]
def check_activities(pw, path):
    g = Game(pw, path)
    try:
        open_with(g, '?nosave&debug&sound&soundlog'); g.step(30); click_world(g)
        g.page.wait_for_function("window.__sc('SND._.state()') === 'running'", timeout=10000)
        names = g.ev('Object.keys(SND._.FX)')
        missing = [n for n in ACT_NAMES if n not in names]
        check(not missing, f'activity sounds registered (missing {missing})')
        played = g.ev(f"(() => {{ const out = [], t = SND.ctx.currentTime + 0.05; for (const n of {ACT_NAMES!r}) {{ try {{ SND._.FX[n](t, {{}}); }} catch (e) {{ out.push(n + ': ' + e.message); }} }} return out; }})()")
        check(not played, f'every activity sound is made without an error (not: {played[:6]})')
        seed0 = g.ev('seed')
        g.ev(f"for (let k = 0; k < 200; k++) SND.fx({ACT_NAMES!r}[k % {len(ACT_NAMES)}])")
        res = []
        for kind, o, one, loop, end in ACT_CASES:
            got = g.ev(f"""(() => {{ SND.log.length = 0; const A = {{ kind: {kind!r}, o: {json.dumps(o)}, def: {{}}, phase: 'in', placeId: null }};
              SND.act('begin', A); const b = SND.log.map(e => e.name), lp = [...SND._.LOOPS].map(l => l.label); SND.log.length = 0; SND.act('end', A, false);
              return [b, lp, SND.log.map(e => e.name), [...SND._.LOOPS].map(l => l.label)]; }})()""")
            b, lp, e, after = got
            good = (one is None or one in b) and (end is None or end in e) and (loop is None or (loop in b and loop in lp and loop not in after))
            if not good: res.append((kind, o, got))
        check(not res, f'each activity plays its sound, its loop runs till it ends, then stops: {res[:3]}')
        walked = g.ev("(() => { SND.log.length = 0; SND.act('end', { kind: 'toilet', o: {}, phase: 'walk' }, true); return SND.log.length; })()")
        check(walked == 0, 'no flush for a toilet you walked away from before sitting down')
        chore = g.ev("""(() => { const t = shipNow(), mk = (id, title, tool, chore) => ({ id, title, tool, chore: chore || 'fix', kind: 'chore', status: 'open', stops: [] }), out = {};
          for (const [id, title, tool, ch] of [['sc-v', 'Clean the lift lobby vent', 'a vent brush'], ['sc-h', 'Oil a squeaky corridor door', 'an oil can'], ['sc-d', 'Clear a slow basin drain', 'a drain snake'],
              ['sc-u', 'Unstick a gym locker', 'a screwdriver'], ['sc-l', 'Replace a lobby light', 'a step stool', 'lamp'], ['sc-r', 'Tighten a wobbly lobby bench', 'a hex key']]) {
            const j = mk(id, title, tool, ch); SHIP.jobs.push(j); SND.log.length = 0; SND.act('begin', { kind: 'ixStop', o: { job: id, title }, phase: 'in' }); out[id] = SND.log.map(e => e.name)[0]; SND.act('end', { kind: 'ixStop', o: {} }); }
          SHIP.jobs = SHIP.jobs.filter(j => !String(j.id).startsWith('sc-')); return out; })()""")
        check(chore == {'sc-v': 'vent', 'sc-h': 'hingeSqueak', 'sc-d': 'drain', 'sc-u': 'unstick', 'sc-l': 'partSwap', 'sc-r': 'ratchet'}, f'chores and small repairs by what you do: {chore}')
        check(g.ev('seed') == seed0, 'the activity sounds never draw on R()')
        # the hooks, through the game's own functions
        real = g.ev("""(() => { SND.log.length = 0; const pl = [...PLACE_OF.values()].find(p => p.type === 'shower' && !(PRIVATE_TYPES.has(p.type) && privatePlace(p)));
          if (!pl) return null; actStart('shower', pl.id, { title: 'Shower' }); return pl.id; })()""")
        for _ in range(40):
            if g.ev("!ACT || ACT.phase !== 'walk'"): break
            g.step(30)
        began = g.ev("[ACT ? ACT.phase : null, SND.log.map(e => e.name), [...SND._.LOOPS].map(l => l.label)]")
        check(real and 'shower' in began[1] and 'shower' in began[2], f'a real shower (actStart at {real}) starts the running water: {began}')
        g.ev("SND.log.length = 0; actEnd(false)"); g.step(2)
        ended = g.ev("[SND.log.map(e => e.name), [...SND._.LOOPS].map(l => l.label)]")
        check('showerOff' in ended[0] and 'shower' not in ended[1], f'and stepping out turns it off: {ended}')
        ann = g.ev("(() => { SND.log.length = 0; deviceAddress({ text: 'All hands.' }); deviceAddress(null); return SND.log.map(e => e.name); })()")
        check(ann == ['announce'], f'a ship-wide address chimes once: {ann}')
        hello = g.ev("""(() => { const scr = a => { const v = new THREE.Vector3(a.x, (a.y || 0) + 1.0, a.z).project(camera); return [(v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight]; };
          const a = DECK_CREW.find(c => { const [x, y] = scr(c); return x > 40 && x < innerWidth - 40 && y > 80 && y < innerHeight - 80 && crewAtScreen(x, y) === c; }); if (!a) return 'no crew';
          const [x, y] = scr(a);
          SND.log.length = 0; const r = tapCrew(x, y); return [r, SND.log.map(e => e.name)]; })()""")
        check(hello == 'no crew' or not hello[0] or 'hello' in hello[1], f'tapping someone says hello: {hello}')
        clk = g.ev("""(() => { let d = 2; while (!playerShiftOn(d)) d++; setShipNow((d - 1) * 1440 + 485); SND.log.length = 0; const r = clockPunch(false); return [r, SND.log.map(e => e.name)]; })()""")
        check(clk[0] in (None, 'in', 'out') and (clk[0] is None or ('clockIn' if clk[0] == 'in' else 'clockOut') in clk[1]), f'the time clock: {clk}')
        tick = g.ev("typeof SND.actTick === 'function'")
        check(tick, 'the activity slot ticks once a second (SND.actTick: the storm and the blackout)')
        storm = g.ev("""(() => { const en = eventNow, ba = blackoutAt, out = [];
          try { eventNow = () => null; blackoutAt = () => null; SND.actTick(); SND.log.length = 0;
            eventNow = () => ({ id: 'ionStorm', phase: 'warning', day: 0 }); SND.actTick(); out.push(SND.log.map(e => e.name)); SND.log.length = 0;
            SND.actTick(); out.push(SND.log.map(e => e.name)); SND.log.length = 0;
            blackoutAt = () => ({ from: 0, to: 1 }); SND.actTick(); out.push(SND.log.map(e => e.name)); }
          finally { eventNow = en; blackoutAt = ba; } return out; })()""")
        check(storm == [['storm'], [], ['flicker']], f'the storm warning chimes once as it begins, and the lights dip with a blackout: {storm}')
        print('  activities (FX20):', len(ACT_NAMES), 'sounds;', len(ACT_CASES), 'activities; chores', chore, '; shower', began[1], '->', ended[0], '; address', ann, '; hello', hello, '; clock', clk)
    finally: g.close()

def check_activities_silent(pw, path):
    g = Game(pw, path)
    try:
        g.step(30); click_world(g)
        r = g.ev("(() => { const pl = [...PLACE_OF.values()].find(p => p.type === 'shower'); actStart('shower', pl.id, { title: 'Shower' }); return [SND._.state(), SND._.LOOPS.size]; })()")
        g.step(60); r2 = g.ev("[SND._.state(), SND._.LOOPS.size, SND.log === null]"); g.ev('actEnd(true)')
        check(r[0] == 'off' and r2[0] == 'off' and r2[1] == 0, f'under webdriver an activity makes no sound and starts nothing: {r} {r2}')
    finally: g.close()

CHECKS = [check_silent_by_default, check_start_and_fx, check_settings_rows, check_pause_suspends, check_core_hooks, check_activities, check_activities_silent]
# (activities and music add theirs here)

with sync_playwright() as pw:
    for c in CHECKS:
        try: c(pw, sys.argv[1])
        except Exception as e: check(False, f'{c.__name__}: {e}')
print('SOUND CHECK OK' if ok else 'SOUND CHECK FAILED')
sys.exit(0 if ok else 1)
