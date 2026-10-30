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

# ---- music (FX22b) ----
# The module on a test clock: a stand-in AudioContext whose time the check moves (nothing is made or heard), and a pretend
# ship clock. MUSIC_RIG(day, min, onShift) -> window.__mr = { m (the module), clock, ship, run(secs, step) }.
MUSIC_RIG = r"""((day, min, onShift) => {
  const FK = () => { const f = function () { return FK(); }; return new Proxy(f, { get(t, k) { if (k === 'value') return 0; if (k === 'getChannelData') return () => new Float32Array(8); if (k === Symbol.toPrimitive) return () => 0; return FK(); }, set() { return true; } }); };
  const clock = { t: 0 }, ship = { day, min, onShift }, ctx = new Proxy({}, { get(_, k) { return k === 'currentTime' ? clock.t : k === 'sampleRate' ? 8000 : FK(); } });
  let a = 12345; const rnd = () => { a = (a * 1103515245 + 12345) % 2147483648; return a / 2147483648; };   // the check's own numbers (never R())
  const m = SND.makeMusic({ ctx, dest: FK(), shipTime: () => ({ ...ship }), random: rnd });
  const run = (secs, step = 0.5) => { for (let s = 0; s < secs; s += step) { clock.t += step; m.update(); } return m.state(); };
  window.__mr = { m, clock, ship, run }; return 1; })"""

def check_music_schedule(pw, path):
    g = Game(pw, path)
    try:
        seed0 = g.ev('seed')
        sets = g.ev("(() => { " + "window.__x = " + MUSIC_RIG + "; __x(3, 600, false); return __mr.m.SETS; })()")
        for name, minute, shift in [('early morning', 360, False), ('morning', 600, False), ('midday', 720, False), ('afternoon', 900, False),
                                    ('evening', 1100, False), ('night', 1300, False), ('late night', 120, False), ('working', 600, True)]:
            st = g.ev(f"(() => {{ __x(3, {minute}, {str(shift).lower()}); return __mr.run(5); }})()")
            check(st['set'] == name and st['track'] in sets[name], f'music: {name} plays from its own set ({st["set"]}, {st["track"]})')
        # the rotation: 50 picks in a set, never the same twice running, the whole set before any repeats
        r = g.ev("""(() => { __x(3, 600, false); const ks = []; __mr.run(5); ks.push(__mr.m.state().track);
          for (let k = 1; k < 50; k++) { __mr.m.next(); ks.push(__mr.run(3).track); } return ks; })()""")
        n = len(sets['morning'])
        check(all(r[k] != r[k + 1] for k in range(len(r) - 1)), f'music: never the same track twice running over 50 picks')
        check(sorted(set(r[:n])) == sorted(sets['morning']), f'music: the whole morning set before a repeat ({r[:n]})')
        # a new time of day waits for the end of a section (30 s at most); a jump in ship time changes at once
        r = g.ev("""(() => { __x(3, 655, false); __mr.run(20); const a = __mr.m.state().track; __mr.ship.min = 662; let t0 = __mr.clock.t, s = __mr.m.state();
          while (s.set !== 'midday' && __mr.clock.t - t0 < 60) s = __mr.run(0.5); const waited = __mr.clock.t - t0, b = s.track;
          __mr.ship.min = 1000; s = __mr.run(0.5); return { a, b, waited, jump: s.set, jt: s.track }; })()""")
        check(0 < r['waited'] <= 30.5 and r['b'] in sets['midday'], f'music: midday came in at a section end, within 30 s ({r["waited"]:.1f} s, {r["a"]} -> {r["b"]})')
        check(r['jump'] == 'afternoon', f'music: a jump in ship time (sleep) changes over at once ({r["jump"]}, {r["jt"]})')
        # Off and pause go quiet; arrival night is silent and Day 1 starts the music
        r = g.ev("""(() => { __x(3, 600, false); __mr.run(5); __mr.m.setEnabled(false); const off = __mr.run(10); __mr.m.setEnabled(true); __mr.m.pause(); const p = __mr.m.state();
          __x(0, 1200, false); const d0 = __mr.run(120); __mr.ship.day = 1; __mr.ship.min = 400; const d1 = __mr.run(10); return { off: off.track, paused: p.paused, d0: d0.track, rest: d0.resting, d1: d1.track }; })()""")
        check(r['off'] is None and r['paused'], f'music: Off stops it and pause holds it ({r})')
        check(r['d0'] is None and r['rest'] and r['d1'] in sets['early morning'], f'music: nothing on arrival night (Day 0), music on Day 1 ({r})')
        # a chosen track plays and plays again after it ends; Ship schedule goes back to the time of day
        r = g.ev("""(() => { __x(3, 600, false); __mr.m.setMode('lullaby'); let s = __mr.run(5); const a = s.track, total = s.total;
          s = __mr.run(total + 200, 2); const b = s.track || __mr.run(60, 2).track; __mr.m.setMode('schedule'); const c = __mr.run(5).track; return { a, b, c }; })()""")
        check(r['a'] == 'lullaby' and r['b'] == 'lullaby' and r['c'] in sets['morning'], f'music: a chosen track repeats, Ship schedule returns ({r})')
        check(g.ev('seed') == seed0, 'music: never draws on R()')
    finally: g.close()

def check_music_app(pw, path):
    g = Game(pw, path)
    try:
        # under webdriver (no ?sound): no audio, no music; the app still shows and keeps your choices
        click_world(g)
        r = g.ev("""(() => { const v = JSON.stringify(deviceView('music')); return { ctx: !!SND.ctx, music: SND.music, app: DEVICE_APPS.has('music'), order: DEVICE_APPS.get('music').order, v }; })()""")
        check(not r['ctx'] and r['music'] is None and r['app'] and 'Now playing' in r['v'] and 'Ship schedule' in r['v'], f'music: silent under webdriver, the Music app there ({r["ctx"]}, {r["music"]}, {r["app"]})')
        # the app's list is the module's, track for track and time by time
        same = g.ev("""(() => { window.__x = """ + MUSIC_RIG + """; __x(3, 600, false); const L = __mr.m.LIST.map(g => g.time + ':' + g.tracks.map(t => t.key + '=' + t.name).sort().join(','));
          const A = SND.musicList.map(([time, ts]) => time + ':' + ts.map(([k, n]) => k + '=' + n).sort().join(',')); return JSON.stringify(L) === JSON.stringify(A) ? true : [L, A]; })()""")
        check(same is True, f'music: the app lists every track under its time, as the module does ({same})')
        r = g.ev("""(() => { const P = () => JSON.stringify(SND.prefs.music); const out = [P()];
          deviceDo({ app: 'music', do: 'vol', arg: 1 }); deviceDo({ app: 'music', do: 'on', arg: false }); out.push(P()); deviceDo({ app: 'music', do: 'on', arg: true });
          deviceDo({ app: 'music', do: 'browse' }); const v = JSON.stringify(deviceView('music')); deviceDo({ app: 'music', do: 'mode', arg: 'tea' }); const m1 = SND.prefs.music.mode;
          deviceDo({ app: 'music', do: 'next' }); const m2 = SND.prefs.music.mode; const why = JSON.stringify(deviceView('music'));
          deviceDo({ app: 'music', do: 'mode', arg: 'schedule' }); const day = SHIP.time.day; SHIP.time.day = 0; const d0 = JSON.stringify(deviceView('music')); SHIP.time.day = day;
          return { out, list: v.includes('Late night') && v.includes('Nebula'), m1, m2, why: why.includes('Your choice: Zenith, on repeat'), d0: d0.includes('Quiet tonight'), mode: SND.prefs.music.mode }; })()""")
        check(r['out'][0] == '{"on":true,"vol":0.7,"mode":"schedule","heard":{}}', f'music: on, Medium, Ship schedule by default ({r["out"][0]})')
        check('"vol":1' in r['out'][1] and '"on":false' in r['out'][1], f'music: Volume and Off kept in the sound key\'s music part ({r["out"][1]})')
        check(r['list'] and r['m1'] == 'tea' and r['m2'] == 'midday' and r['why'], f'music: Choose a track lists them all; a pick plays it; Next is the next in the list ({r["m1"]} -> {r["m2"]})')
        check(r['d0'] and r['mode'] == 'schedule', f'music: arrival night says Quiet tonight ({r["d0"]})')
        save = g.ev("""(() => { let s = null; const ls = localStorage.setItem; localStorage.setItem = (k, v) => { if (k === SAVE_KEY) s = v; };
          try { eval('(' + saveGame.toString().replace('if (NOSAVE ||', 'if (false &&') + ')')(); } finally { localStorage.setItem = ls; }
          const mine = o => o && typeof o === 'object' && (('mode' in o && 'heard' in o && 'vol' in o) || Object.values(o).some(mine)); return { n: (s || '').length, mine: mine(JSON.parse(s || 'null')) }; })()""")
        check(save['n'] > 1000 and not save['mine'], f'music: nothing of it in the game save ({save})')
        # with ?sound: a tap starts the sound, and the music with it, on the schedule
        open_with(g, '?nosave&debug&sound&soundlog'); g.step(10); click_world(g); g.ev("skipTo(2 * 1440 + 600)")
        g.page.wait_for_function("window.__sc('SND._.state()') === 'running'", timeout=10000)
        for _ in range(10):
            g.page.wait_for_timeout(1000); g.step(3)
            if g.ev("!!(SND.music && SND.music.state().track)"): break
        st = g.ev("SND.music ? SND.music.state() : null")
        check(bool(st) and st['set'] == 'morning' and bool(st['track']), f'music: with sound on, the morning set plays at 10:00 on Day 3 ({st and (st["set"], st["track"])})')
        check(g.ev("JSON.stringify(SND.prefs.music.heard)") != '{}', 'music: the rotation is kept in the sound key')
        check(not [e for e in g.errors if 'pageerror' in e], f'music: no page errors {g.errors[:2]}')
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
             'climb', 'discThrow', 'piano', 'guitar', 'tileShuffle', 'telescope', 'watering', 'storm', 'announce', 'flicker', 'clockIn', 'clockOut', 'hello',
             'kettle', 'chop', 'ovenOpen', 'ovenClose', 'stove', 'mop', 'trowel', 'blanket', 'tilePlace', 'discCatch', 'hingeAfter', 'popper']
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
        g.ev("SND.log.length = 0; window.__lie = { kind: 'lie', o: {}, def: {}, phase: 'in' }; SND.act('begin', window.__lie); SND.act('end', window.__lie, true)")
        g.page.wait_for_timeout(2200); g.step(2)
        quick = g.ev("SND.log.map(e => e.name)")
        g.ev("SND.log.length = 0; window.__lie = { kind: 'lie', o: {}, def: {}, phase: 'in' }; SND.act('begin', window.__lie)")
        g.page.wait_for_timeout(2200); g.step(2)
        stay = g.ev("(() => { const n = SND.log.map(e => e.name); SND.act('end', window.__lie, false); return n; })()")
        check('blanket' not in quick and 'bedLie' in quick and 'blanket' in stay, f'a follow-up (the blanket) is cancelled if you get up first, and comes if you stay: {quick} / {stay}')
        laundry = g.ev("""(() => { goToDeck(4); const s = placeSpot('4-laundry-1'), gl = nearestOpen(s.x, s.z, player); player.obj.position.copy(cellPos(...gl)); player.stop();
          SND.log.length = 0; SND.actTick(); const before = SND.log.filter(e => e.loop).map(e => e.name);
          machineUse('4-washer-1'); MACH_REV++; SND.actTick(); const on = SND.log.filter(e => e.loop).map(e => e.name), loops = [...SND._.LOOPS].map(l => l.label);
          return [before, on, loops]; })()""")
        check('washer' not in laundry[0] and 'washer' in laundry[1] and 'washer' in laundry[2], f'in the laundry a running washer is heard: {laundry}')
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
CHECKS += [check_music_schedule, check_music_app]   # music (FX22b)

def check_comet_sound(pw, path):
    """the comet (0.93.2, FX25 with SD1): its own track while section 18's cometMusicOn() is true, then back to the
    schedule; the turn's swell is registered and soft. (Section 18 gives cometMusicOn; here a stand-in on window.)"""
    g = Game(pw, path)
    try:
        open_with(g, '?nosave&debug&sound&soundlog'); g.step(30); click_world(g)
        g.page.wait_for_function("window.__sc('SND._.state()') === 'running'", timeout=10000)
        g.step(5)
        check(g.ev("!!SND.music && SND.has('cometTurn')"), 'the music is up and the comet swell is registered')
        check(g.ev("SND.music.TRACKS.comet && SND.music.TRACKS.comet.time === 'Event' && !SND.music.LIST.some(x => x.tracks.some(t => t.key === 'comet'))"),
              'the comet track exists and is not on the Music app list')
        # section 18's own cometMusicOn (FX25, a function declaration in the game's scope) shadows a window stub: swap it in
        # scope when it's there (and put it back), else stub it on window as before
        real = g.ev("typeof cometMusicOn === 'function' && !window.hasOwnProperty('cometMusicOn')")
        setc = (lambda v: g.ev(f"cometMusicOn = () => {v}")) if real else (lambda v: g.ev(f"window.cometMusicOn = () => {v}"))
        if real: g.ev("window.__cmReal = cometMusicOn")
        setc('true'); g.step(3)
        check(g.ev("SND.music.eventOn()") == 'comet', 'while cometMusicOn() is true the comet is the event')
        setc('false'); g.step(3)
        check(g.ev("SND.music.eventOn()") is None, 'after, back to the schedule')
        if real: g.ev("cometMusicOn = window.__cmReal"); g.step(2)
        else: g.ev("delete window.cometMusicOn"); g.step(2)
        check(g.ev("SND.music.eventOn()") is None, 'with no cometMusicOn at all (or the real one, on Day 1), nothing changes')
        n = g.ev("(() => { SND.log.length = 0; SND.fx('cometTurn', { long: 22 }); return SND.log.filter(e => e.name === 'cometTurn').length; })()")
        check(n == 1, 'the comet turn plays once')
    finally: g.close()

CHECKS += [check_comet_sound]   # the comet (SD1 for FX25)
# (activities and music add theirs here)

# ---- the sound update (SD2, plans/sound/r3-build-plan.md), behind SND_R3_ON: each part runs on a copy switched on ----
R3_LINE = 'const SND_R3_ON = false;'
def r3_copy(path):
    src = pathlib.Path(path).read_text()
    if 'const SND_R3_ON = true;' in src: return path   # switched on in the build itself (0.96.0): test it as it is
    if R3_LINE not in src: return None
    f = WORK / 'test' / f'_r3on_{os.getpid()}.html'; f.parent.mkdir(parents=True, exist_ok=True); f.write_text(src.replace(R3_LINE, 'const SND_R3_ON = true;', 1)); return str(f)
R3_KEYS = ['beam', 'cup', 'farewellsup', 'goodbye', 'harvest', 'lantern', 'line', 'veyli', 'farewell']
# put the player in a room (deck, room name or key) at an absolute ship minute, then ask which event track fits
R3_AT = r"""(([t, deck, room]) => { skipTo(t); goToDeck(deck); const R = DECKS[deck].rooms, k = R[room] ? room : Object.keys(R).find(x => R[x].name === room);
  const tl = ROOM_TILES[k]; if (!tl || !tl.length) return 'no tiles for ' + room; player.obj.position.copy(cellPos(...tl[(tl.length / 2) | 0])); return k; })"""
def check_r3music(pw, path):
    """turn 1: the picked traditions' and events' own tracks, while you're in their rooms (SND_R3_ON on a copy)"""
    on = r3_copy(path)
    if not on: check(False, 'r3music: no SND_R3_ON line in this build, so nothing was tested'); return
    g = Game(pw, on)
    try:
        open_with(g, '?nosave&debug&sound&soundlog'); g.step(30); click_world(g)
        g.page.wait_for_function("window.__sc('SND._.state()') === 'running'", timeout=10000); g.step(5)
        check(g.ev("!!SND.music && typeof SND.r3Event === 'function'"), 'r3music: the music is up and the event pick is there')
        got = g.ev(f"{json.dumps(R3_KEYS)}.filter(k => !(SND.music.TRACKS[k] && SND.music.TRACKS[k].time === 'Event'))")
        check(got == [], f'r3music: every event track exists (missing {got})')
        check(g.ev(f"!SND.music.LIST.some(x => x.tracks.some(t => {json.dumps(R3_KEYS)}.includes(t.key)))"), 'r3music: none of them is on the Music app list')
        check(g.ev("SND.music.TRACKS.farewell.form().reduce((a, x) => a + x.bars, 0)") == 8, 'r3music: the farewell song is short (8 bars, about 40 s)')
        check(g.ev("(p => p.includes('sDrone') && p.includes('sBronzeLow') && !p.includes('sSwell'))(SND.music.TRACKS.farewell.form().flatMap(x => x.parts))"), 'r3music: the farewell song is the user\'s A (the drone and the bronze bar)')
        def at(name, t, deck, room, want):
            k = g.ev(f"({R3_AT})({json.dumps([t, deck, room])})"); g.page.wait_for_timeout(500); g.step(4)
            got = g.ev("SND.r3Event()"); print(f'  r3music {name}: room {k!r} -> {got!r}')
            check(got == want, f'r3music: {name}: wanted {want!r}, got {got!r}')
            if want: g.step(3); check(g.ev("SND.music.eventOn()") == want, f'r3music: {name}: the music takes the {want} track')
        # a tradition the user picked, found in the calendar (its first day in two weeks), in one of its rooms
        tr = g.ev("""(() => { for (let d = 1; d <= 30; d++) for (const e of eventsOn(d)) if (['lantern-walk', 'name-on-the-beam', 'farewell-supper', 'harvest-supper', 'first-fruits', 'rec-cup', 'department-cup', 'rec-regatta'].includes(e.id)) {
          const r = [...(e.rooms || eventRooms(e.ev))][0]; if (r) return [e.id, (d - 1) * 1440 + e.from + 5, +r.split('|')[0], r.split('|')[1]]; } return null; })()""")
        if not check(tr is not None, 'r3music: no picked tradition in the first 30 days'): return
        key = {'lantern-walk': 'lantern', 'name-on-the-beam': 'beam', 'farewell-supper': 'farewellsup', 'harvest-supper': 'harvest', 'first-fruits': 'harvest', 'rec-cup': 'cup', 'department-cup': 'cup', 'rec-regatta': 'cup'}[tr[0]]
        at('the tradition ' + tr[0], tr[1], tr[2], tr[3], key)
        at('the same room after it', tr[1] + 300, tr[2], tr[3], None)
        at('the Line, the ceremony', 6 * 1440 + 880, 3, 'Bow lounge', 'line')
        at('the Line supper', 6 * 1440 + 1090, 3, 'Mess hall', 'line')
        at('the Line day, the gym', 6 * 1440 + 1090, 3, 'Gym', None)
        # the visit (Days 17-20): under skipTo from a fresh game the events base doesn't start it here, so section 18's
        # eventNow is stood in for (as the comet check stands in for cometMusicOn), and put back after
        g.ev("window.__enReal = eventNow")
        g.ev("eventNow = () => ({ id: 'diplomatic', phase: 'onset', day: 1 })"); at('the Veyli arrival', 17 * 1440 + 610, 5, 'Shuttle bay', 'veyli')
        at('the arrival, the Works bay', 17 * 1440 + 610, 5, 'Works bay', None)
        g.ev("eventNow = () => ({ id: 'diplomatic', phase: 'resolution', day: 3 })"); at('the Veyli farewell', 19 * 1440 + 545, 5, 'Shuttle bay', 'farewell')
        at('after the farewell', 19 * 1440 + 600, 5, 'Shuttle bay', None)
        g.ev("eventNow = window.__enReal")
        g.step(3); check(g.ev("SND.music.eventOn()") is None, 'r3music: back to the schedule after')
        # 0.98 (SD3-2): the pick is asked about 4 times a second, not every frame
        import time as _t
        n0, t0 = g.ev("SND.r3Ev.n"), _t.perf_counter()
        for _ in range(4): g.step(30); g.page.wait_for_timeout(300)   # 120 frames over at least a real second (RV25)
        n1, t1 = g.ev("SND.r3Ev.n"), _t.perf_counter()
        print(f'  r3music: {n1 - n0} asks in 120 frames, {t1 - t0:.2f} s')
        check(1 <= n1 - n0 <= (t1 - t0) / 0.25 + 2 and n1 - n0 < 120, f'r3music: the event pick is asked again, about 4 times a second ({n1 - n0} in 120 frames, {t1 - t0:.2f} s)')
        pe = [e for e in g.errors if e.startswith('pageerror')]
        if pe: check(False, 'r3music: page errors: ' + ' | '.join(pe[:3]))
    finally: g.close()
def check_r3_off(pw, path):
    """off (as shipped): none of the update is there"""
    g = Game(pw, path)
    try:
        open_with(g, '?nosave&debug&sound&soundlog'); g.step(30); click_world(g)
        g.page.wait_for_function("window.__sc('SND._.state()') === 'running'", timeout=10000); g.step(5)
        if g.ev("typeof SND_R3_ON !== 'undefined' && SND_R3_ON"): print('  r3off: SND_R3_ON is on in this build (nothing to check)'); return
        check(g.ev(f"typeof SND.r3Event === 'undefined' && {json.dumps(R3_KEYS)}.every(k => !SND.music.TRACKS[k] || k === 'comet')"), 'r3off: with SND_R3_ON off there are no event tracks and no event pick')
    finally: g.close()
def check_r3mess(pw, path):
    """turn 2: the mess hall (the galley, the clatter and the warm talk), following how many are there; silent when empty; only in the mess"""
    on = r3_copy(path)
    if not on: check(False, 'r3mess: no SND_R3_ON line in this build, so nothing was tested'); return
    g = Game(pw, on)
    try:
        open_with(g, '?nosave&debug&sound&soundlog'); g.step(30); click_world(g)
        g.page.wait_for_function("window.__sc('SND._.state()') === 'running'", timeout=10000); g.step(5)
        check(g.ev("!!SND.r3Mess"), 'r3mess: the mess hall sound is there')
        def at(name, t, deck, room, secs=4):
            k = g.ev(f"({R3_AT})({json.dumps([t, deck, room])})"); g.step(40)
            c0 = g.ev("SND.r3Mess.clinks")
            for _ in range(secs * 2): g.page.wait_for_timeout(500); g.step(2)
            r = g.ev("(M => ({ n: M.n, full: M.full, on: !!M.scene, clinks: M.clinks }))(SND.r3Mess)"); r['per_s'] = (r['clinks'] - c0) / secs
            print(f'  r3mess {name}: room {k!r} {r}'); return r
        night = at('3 am, the mess', 1440 + 180, 3, 'Mess hall')
        check(night['on'], 'r3mess: the scene runs while you are in the mess')
        if night['n'] == 0: check(night['per_s'] == 0, f'r3mess: empty mess is silent (clatter {night["per_s"]}/s)')
        else: print('  r3mess: someone in the mess at 3 am, the empty case is checked by hand below')
        full = at('the dinner rush', 1440 + 1110, 3, 'Mess hall')
        check(full['n'] >= 3, f'r3mess: people in the mess at the dinner rush ({full["n"]})')
        check(full['per_s'] > 0.4, f'r3mess: the clatter at the rush ({full["per_s"]}/s)')
        # every layer follows the count: none at 0, more as the room fills (the scene reads M.at's levels live)
        lv = g.ev("[0, 1, 2, 8, 25, SND.r3Mess.full].map(n => [n, SND.r3Mess.at(n)])"); print('  r3mess layers', lv)
        check(lv[0][1] == {'galley': [0, 0], 'clatter': 0, 'voices': 0}, 'r3mess: no one there, every layer silent')
        for (n0, a), (n1, b) in zip(lv, lv[1:]):
            if n0 == 0: continue
            check(b['clatter'] >= a['clatter'] and b['voices'] >= a['voices'] and b['galley'][0] >= a['galley'][0], f'r3mess: {n1} people no quieter than {n0}')
        check(lv[-1][1]['voices'] == 12 and lv[1][1]['voices'] == 1, 'r3mess: one voice for a couple, all twelve when full')
        g.ev("SND.r3Mess.n = 0"); g.page.wait_for_timeout(1200)
        gone = at('the gym, the same evening', 1440 + 1112, 3, 'Gym', secs=2)
        check(not gone['on'], 'r3mess: it stops (fading) when you leave the mess')
        oth = at('Deck 4, the evening', 1440 + 1114, 4, 'Laundry', secs=2)
        check(not oth['on'], 'r3mess: nothing on another deck')
        log = g.ev("(SND.log || []).filter(x => x.name === 'mess').length")
        check(log >= 1, 'r3mess: the mess scene was logged')
        pe = [e for e in g.errors if e.startswith('pageerror')]
        if pe: check(False, 'r3mess: page errors: ' + ' | '.join(pe[:3]))
    finally: g.close()
CHECKS += [check_r3music, check_r3_off]   # the sound update (SD2), turn 1
R3_FX = ['r3BadgeTake', 'r3BadgeBack', 'r3ReactorDoor', 'r3CoilOff', 'r3CoilOn', 'r3Winding', 'r3Lathe', 'r3Promotion', 'r3Calder', 'r3Stay', 'r3Go', 'r3TernLand', 'r3ShutOff', 'r3ShutOn', 'r3ClockAsk', 'r3TestFit', 'r3Home']
def check_r3fx(pw, path):
    """turn 3: the feature sounds a watcher sees (each moment stood in for, the watcher run directly, then put back)"""
    on = r3_copy(path)
    if not on: check(False, 'r3fx: no SND_R3_ON line in this build, so nothing was tested'); return
    g = Game(pw, on)
    try:
        open_with(g, '?nosave&debug&sound&soundlog'); g.step(30); click_world(g)
        g.page.wait_for_function("window.__sc('SND._.state()') === 'running'", timeout=10000); g.step(5)
        check(g.ev("!!SND.r3"), 'r3fx: the watchers are there')
        # every sound builds without an error (called straight, so a mistake shows)
        bad = g.ev(f"""(() => {{ const out = []; for (const n of {json.dumps(R3_FX)}) {{ const f = SND._.FX[n]; if (!f) {{ out.push(n + ': missing'); continue; }}
          try {{ f(SND.ctx.currentTime + 0.05, {{}}); }} catch (e) {{ out.push(n + ': ' + e.message); }} }} return out; }})()""")
        check(bad == [], f'r3fx: every sound plays ({bad})')
        g.step(2)
        def heard(name, setup, run='SND.r3.watch()', undo=''):
            g.ev(f"(() => {{ SND.log.length = 0; {setup}; {run}; }})()")
            got = g.ev("SND.log.map(x => x.name)"); g.ev(f"(() => {{ {undo}; }})()")
            print(f'  r3fx {name}: {got}')
            return got
        W = 'SND.r3.W'
        # the badge rack
        g.ev("SND.r3.watch()")
        got = heard('badge taken', "dosiState().out = shipNow()"); check('r3BadgeTake' in got, 'r3fx: taking a badge')
        got = heard('badge back', "dosiState().out = null"); check('r3BadgeBack' in got, 'r3fx: hanging it back')
        # the scenes, by line
        got = heard('the test fit', "DIALOGUE = { id: 'vesselTestFit', i: 0, queue: [{}, {}] }; SND.r3.watch(); DIALOGUE.i = 1", undo="DIALOGUE = null; SND.r3.watch()"); check('r3TestFit' in got, 'r3fx: the test fit as you turn it')
        got = heard("Calder's question", "DIALOGUE = { id: 'end.ask', i: 2, queue: [{}, {}, {}, { choice: [] }] }; SND.r3.watch(); DIALOGUE.i = 3")
        check('r3Calder' in got, "r3fx: Calder's question, the pad as the answers show")
        check(g.ev(W + ".duck") is True, "r3fx: the music ducked while she asks")
        g.ev("DIALOGUE = null; SND.r3.watch()"); check(g.ev(W + ".duck") is False, 'r3fx: the music back after')
        got = heard('the engine badge', "DIALOGUE = { id: 'pu4.badge', i: 0, queue: [{}] }", undo="DIALOGUE = null; SND.r3.watch()"); check('r3Promotion' in got, 'r3fx: the engine badge scene')
        # the early clock-out question
        got = heard('the clock asks', "SND.r3.watch(); clockScreen(null, true)", undo="document.getElementById('clockScreen').hidden = true; SND.r3.watch()")
        check('r3ClockAsk' in got, 'r3fx: the early clock-out question')
        # the once-a-second ones: Stay or Go, a promotion, a booked shutdown
        g.ev("window.__keep = { end: SHIP.end, works: SHIP.works }; SHIP.works = { ...(SHIP.works || {}), rank: 'officer' }; SHIP.end = { said: [] }; SND.r3.tick()")
        got = heard('stay', "SHIP.end.said.push([SHIP.time.day, 'stay'])", run='SND.r3.tick()'); check('r3Stay' in got, 'r3fx: Stay')
        got = heard('not sure', "SHIP.end.said.push([SHIP.time.day, 'unsure'])", run='SND.r3.tick()'); check(not any(x in got for x in ('r3Stay', 'r3Go')), 'r3fx: nothing for "not sure"')
        got = heard('go', "SHIP.end.said.push([SHIP.time.day, 'go'])", run='SND.r3.tick()'); check('r3Go' in got, 'r3fx: Go')
        got = heard('promotion', "SHIP.works.rank = 'senior'", run='SND.r3.tick()'); check('r3Promotion' in got, 'r3fx: a promotion')
        g.ev("SHIP.works.sd = { set: { [SHIP.time.day]: [{}] } }; SND.r3.tick()")
        got = heard('power off', "SHIP.works.sd.set[SHIP.time.day][0].st = 'off'", run='SND.r3.tick()'); check('r3ShutOff' in got, 'r3fx: a booked shutdown, power off')
        got = heard('power back', "SHIP.works.sd.set[SHIP.time.day][0].st = 'done'", run='SND.r3.tick()'); check('r3ShutOn' in got, 'r3fx: and back')
        g.ev("SHIP.end = __keep.end; SHIP.works = __keep.works; SND.r3.tick()")
        # rooms: the reactor room's throb, the Tern landing in the shuttle bay (the vessel stood in for)
        g.ev(f"({R3_AT})({json.dumps([1440 + 600, 6, 'R'])})"); g.step(3)
        check(g.ev(W + ".room !== null") and g.ev("SND.log.some(x => x.name === 'reactorRoom')"), 'r3fx: the throb inside the reactor room')
        g.ev(f"({R3_AT})({json.dumps([1440 + 602, 6, 'E'])})"); g.step(3); g.ev("SND.r3.watch()"); check(g.ev(W + ".room === null"), 'r3fx: none outside it')
        # a coil off and on (the Tier 4 test's steps; its stops stood in for), next to coil 1
        g.ev("window.__js = jobStops; jobStops = () => [{ step: 'fetch' }, { step: 'isolate' }, { step: 'read' }, { step: 'wind' }, { step: 'cycle' }]; window.__fj = { id: 'r3test', kind: 'tier4', mach: '6-coil-1', status: 'open', stepsDone: [0] }; SHIP.jobs.push(__fj); SND.r3.tick()")
        got = heard('coil off', "__fj.stepsDone = [0, 1]", run='SND.r3.tick()'); check('r3CoilOff' in got, 'r3fx: the coil off the cycle')
        w = g.ev("(SND.r3.actPick({ kind: 'job' }) || {}).one"); check(w is None, f'r3fx: not winding before the windings are read ({w})')
        g.ev("__fj.stepsDone = [0, 1, 2]; SND.r3.tick()")
        w = g.ev("(SND.r3.actPick({ kind: 'job' }) || {}).one"); check(w == 'r3Winding', f'r3fx: winding in the new coil ({w})')
        got = heard('coil on', "__fj.stepsDone = [0, 1, 2, 3, 4]", run='SND.r3.tick()'); check('r3CoilOn' in got, 'r3fx: and back into the cycle')
        g.ev("SHIP.jobs.splice(SHIP.jobs.indexOf(__fj), 1); jobStops = __js")
        # night 3's team swap: its steps passing (j.cur), the coil slowed and brought back up
        g.ev("window.__tj = { id: 'r3team', kind: 'team', status: 'open', cur: 0, seq: [['you', 'cslow'], [1, 'isolate'], ['you', 'cunbolt'], [1, 'test'], ['you', 'cup']].map(([who, part]) => ({ who, part })) }; SHIP.jobs.push(__tj); SND.r3.tick()")
        got = heard('team: isolate done', "__tj.cur = 2", run='SND.r3.tick()'); check(got == ['r3CoilOff'], f'r3fx: the team swap takes the coil off ({got})')
        got = heard('team: drive back up', "__tj.cur = 5; __tj.status = 'done'", run='SND.r3.tick()'); check(got == ['r3CoilOn'], f'r3fx: and back up at the end ({got})')
        g.ev("SHIP.jobs.splice(SHIP.jobs.indexOf(__tj), 1)")
        g.ev("window.__ev = SHIP.event; SHIP.event = { id: 'x', mine: { 'vessel:step': 3 } }")
        w = g.ev("(SND.r3.actPick({ kind: 'vesselStep', placeId: '5-shop-lathe' }) || {}).one"); check(w == 'r3Lathe', f'r3fx: the lathe for Taavek\'s part ({w})')
        g.ev("SHIP.event = __ev")
        g.ev(f"({R3_AT})({json.dumps([1440 + 610, 5, 'S'])})"); g.step(3)
        g.ev("window.__vn = vesselNow; vesselNow = () => ({ k: 1 }); TERN.target = 0; SND.r3.watch()")
        got = heard('the Tern lands', "TERN.target = 1", undo="vesselNow = __vn"); check('r3TernLand' in got, 'r3fx: the Tern landing while you are in the bay')
        # your new quarters: moved to room B (worksHome 2-B, 24u's move day today, stood in for), then room B's door: not for a
        # crew member at the door; the home chime on your first opening; none the second time (0.99, SD3-1)
        MOVED = "SHIP.works = { ...(SHIP.works || {}), home: '2-B', pu: { t4: { move: { walked: SHIP.time.day } } } }; SND.r3.W.homeHad = undefined; SND.r3.tick()"
        g.ev(f"({R3_AT})({json.dumps([1440 + 615, 2, 'B'])})"); g.page.wait_for_timeout(700); g.step(5)   # the deck first (its build reads the real Tier 4 record)
        g.ev("window.__wk = SHIP.works; " + MOVED)
        check(g.ev(W + ".homeNew") is True, 'r3fx: moved to room B, the chime is waiting')
        DB = "DOOR_OBJS.find(d => [[0.6, 0], [-0.6, 0], [0, 0.6], [0, -0.6]].some(([x, z]) => roomAt(...cellAt(d.cx + x, d.cz + z)) === 'B'))"
        for n, crew in ((0, True), (1, False), (2, False)):
            if crew: g.ev(f"(() => {{ const d = {DB}, a = DECK_CREW.find(x => x.p); window.__cw = [a, a.x, a.z, a.settled]; a.x = d.cx - 0.3; a.z = d.cz - 0.3; a.settled = false; }})()")   # someone walking through it
            g.ev(f"(() => {{ const d = {DB}; player.obj.position.set(d.cx + 0.3, 0, d.cz + 0.3); SND.log.length = 0; }})()")
            for v in (0.0, 0.5, 1.0, 0.5, 0.0):
                g.ev(f"(() => {{ const d = {DB}; d.open = {v}; d.force = {1 if v >= 0.5 else 0}; }})()"); g.step(1)
            if crew: g.ev("(([a, x, z, st]) => { a.x = x; a.z = z; a.settled = st; })(__cw)")
            got = g.ev("SND.log.map(x => x.name)"); print(f'  r3fx room B door, {"a crew member opening it" if crew else "your opening " + str(n)}:', got); g.ev(f"delete {DB}.force")
            check(('r3Home' in got) == (n == 1), f'r3fx: the home chime on your first opening only ({"crew" if crew else n})')
        g.ev("SHIP.works = __wk; SND.r3.tick()")
        # the reactor door: the door watcher, its door opening near you (frames)
        g.ev(f"({R3_AT})({json.dumps([1440 + 620, 6, 'K'])})"); g.page.wait_for_timeout(700); g.step(5)
        D6 = "DOOR_OBJS.find(x => x.e.key === 'v,27,3')"
        dk = g.ev(f"(() => {{ const d = {D6}; if (!d) return null; player.obj.position.set(d.cx + 0.5, 0, d.cz); SND.log.length = 0; return [d.cx, d.cz]; }})()")
        if check(dk is not None, 'r3fx: the reactor door is there'):
            for v in (0.0, 0.5, 1.0, 0.5):   # driven by hand, as the core check does
                g.ev(f"(() => {{ const d = {D6}; d.open = {v}; d.force = {1 if v >= 0.5 else 0}; }})()"); g.step(1)
            got = g.ev("SND.log.map(x => x.name)"); print('  r3fx the reactor door:', got); g.ev(f"delete {D6}.force")
            check(got.count('r3ReactorDoor') == 1 and 'hatchOpen' not in got and 'doorOpen' not in got, 'r3fx: the reactor door has its own sound (once), not the usual door')
        pe = [e for e in g.errors if e.startswith('pageerror')]
        if pe: check(False, 'r3fx: page errors: ' + ' | '.join(pe[:3]))
    finally: g.close()
CHECKS += [check_r3mess]   # the sound update (SD3), turn 2
def check_r3home(pw, path):
    """0.99 (SD3-1): the home chime's note survives a reload (a sound-only note per save slot; the game saving, not ?nosave)"""
    on = r3_copy(path)
    if not on: check(False, 'r3home: no SND_R3_ON line in this build, so nothing was tested'); return
    g = Game(pw, on)
    try:
        MOVED = "SHIP.works = { ...(SHIP.works || {}), home: '2-B', pu: { t4: { move: { walked: SHIP.time.day } } } }; SND.r3.W.homeHad = undefined; SND.r3.tick()"
        def up():
            open_with(g, '?debug&sound&soundlog'); g.step(30); click_world(g)
            g.page.wait_for_function("window.__sc('SND._.state()') === 'running'", timeout=10000); g.step(5)
        up(); g.ev(f"({R3_AT})({json.dumps([615, 2, 'B'])})"); g.page.wait_for_timeout(700); g.step(5)
        g.ev("window.__wk = SHIP.works; localStorage.removeItem('starship-cadet-sound-home:' + SAVE_KEY)"); g.ev(MOVED)
        check(g.ev("SND.r3.W.homeNew") is True, 'r3home: moved, the chime is waiting')
        played = g.ev("(() => { const d = DOOR_OBJS.find(d => [[0.6, 0], [-0.6, 0], [0, 0.6], [0, -0.6]].some(([x, z]) => roomAt(...cellAt(d.cx + x, d.cz + z)) === 'B')); return SND.r3.homeDoor(d); })()")
        note = g.ev("[localStorage.getItem('starship-cadet-sound-home:' + SAVE_KEY), String(SHIP.time.day)]")
        print('  r3home first opening:', played, 'note', note)
        check(played is True and note[0] == note[1], 'r3home: the first opening chimes and keeps its note')
        g.ev("SHIP.works = __wk")   # the stand-in out before the reload (the save keeps the real record)
        up(); g.ev("window.__wk = SHIP.works; " + MOVED)
        check(g.ev("SND.r3.W.homeNew") is False, 'r3home: after a reload it does not chime again')
        g.ev("localStorage.removeItem('starship-cadet-sound-home:' + SAVE_KEY)"); g.ev(MOVED)
        check(g.ev("SND.r3.W.homeNew") is True, 'r3home: without the note (a reload between the move and the door) it is still waiting')
        g.ev("localStorage.setItem('starship-cadet-sound-home:' + SAVE_KEY, String(SHIP.time.day)); SHIP.works = __wk; newGameStart(false)"); g.page.wait_for_timeout(700); g.step(5)
        left = g.ev("[localStorage.getItem('starship-cadet-sound-home:' + SAVE_KEY), SND.r3.W.homeHad]"); print('  r3home after New game:', left)
        check(left == [None, None], 'r3home: a New game clears the note (a second game in the slot hears the chime)')
        pe = [e for e in g.errors if e.startswith('pageerror')]
        if pe: check(False, 'r3home: page errors: ' + ' | '.join(pe[:3]))
    finally: g.close()
R3_HOOKS = [('p5nKnock', 'r3Knock'), ('m24Call', 'r3TeamCall'), ('m24Team', 'r3TeamDone'), ('arrStepDone', 'r3Calibrate'), ('vesselStepStart', 'r3Bronze'), ('clockUndo', 'r3ClockUndo')]
def check_r3hooks(pw, path):
    """turn 4: the one-line hooks in the owners' sections (each behind SND_R3_ON), their sounds, and clock Undo played for real"""
    on = r3_copy(path)
    if not on: check(False, 'r3hooks: no SND_R3_ON line in this build, so nothing was tested'); return
    g = Game(pw, on)
    try:
        open_with(g, '?nosave&debug&sound&soundlog'); g.step(30); click_world(g)
        g.page.wait_for_function("window.__sc('SND._.state()') === 'running'", timeout=10000); g.step(5)
        names = [n for _, n in R3_HOOKS]
        bad = g.ev(f"""(() => {{ const out = []; for (const n of {json.dumps(names)}) {{ const f = SND._.FX[n]; if (!f) {{ out.push(n + ': missing'); continue; }}
          try {{ f(SND.ctx.currentTime + 0.05, {{}}); }} catch (e) {{ out.push(n + ': ' + e.message); }} }} return out; }})()""")
        check(bad == [], f'r3hooks: every hook sound plays ({bad})')
        for fn, n in R3_HOOKS:   # the hook line is in its function, behind the switch
            src = g.ev(f"typeof {fn} === 'function' ? String({fn}) : ''")
            check(f"if (SND_R3_ON) sndFx('{n}'" in src or f"if (SND_R3_ON && s === 2) sndFx('{n}'" in src, f'r3hooks: {fn} calls {n} behind SND_R3_ON')
        # clock Undo, for real: clock in at the clock on Day 2 (08:50), then Undo
        g.ev("skipTo(1440 + 530)"); g.page.wait_for_timeout(500); g.step(10)
        got = g.ev("(() => { SND.log.length = 0; const r = clockPunch(false); const u = clockUndo(); return [r, u, SND.log.map(x => x.name)]; })()")
        print('  r3hooks clock in, Undo:', got)
        check(got[0] == 'in' and got[1] == 'in' and 'clockIn' in got[2] and 'r3ClockUndo' in got[2], 'r3hooks: Undo on the time clock plays the lever back')
        pe = [e for e in g.errors if e.startswith('pageerror')]
        if pe: check(False, 'r3hooks: page errors: ' + ' | '.join(pe[:3]))
    finally: g.close()
CHECKS += [check_r3fx]   # the sound update (SD3), turn 3
CHECKS += [check_r3hooks]   # the sound update (SD3), turn 4
CHECKS += [check_r3home]   # 0.99 (SD3-1): the home chime across a reload

def check_title_music(pw, path):
    """0.99 (SD3): the title screen's track (SND_TITLE, through section 30's SND.title): the three candidates exist and loop
    (about a minute each, not on the Music app's list); with the title on, the track plays while the ship is held (the
    context stays running), the hum hushes and the ship's rooms are quiet; off, it fades and the hum comes back"""
    g = Game(pw, path)
    try:
        open_with(g, '?nosave&debug&sound&soundlog'); g.step(30); click_world(g)
        g.page.wait_for_function("window.__sc('SND._.state()') === 'running'", timeout=10000); g.step(5)
        pick = g.ev("typeof SND_TITLE !== 'undefined' ? SND_TITLE : 'none'")
        if not check(pick != 'none', 'title: no SND_TITLE in this build, so nothing was tested'): return
        tr = g.ev("['titleA', 'titleB', 'titleC'].map(k => { const T = SND.music.TRACKS[k]; return T ? [k, T.time, T.form().reduce((a, x) => a + x.bars, 0) * 4 * 60 / T.bpm] : [k, null, 0]; })")
        print('  title candidates:', tr)
        check(all(t[1] == 'Event' and 45 <= t[2] <= 100 for t in tr), 'title: the three candidates exist, each a loop of about a minute')
        check(g.ev("!SND.music.LIST.some(x => x.tracks.some(t => /^title/.test(t.key)))"), 'title: none of them is on the Music app list')
        if not pick: print('  title: SND_TITLE is null (silent title)'); return
        g.ev("SND.log.length = 0; SND.title(true)"); g.step(5)
        for _ in range(4): g.ev("SND.frame(false)")   # the ship held under the title: run is false
        st = g.ev("[SND._.state(), SND.titleSnd.list.length, SND.titleSnd.hush, SND.log.map(x => x.name)]"); print('  title on:', st)
        check(st[0] == 'running' and st[1] == 1 and st[2] is True and ('title' + pick) in st[3], f'title: on, its track plays with the ship held and the hum hushed ({st})')
        if pick == 'C':   # 0.99.3 (SD4): 0.99.1's song, 16 bars; its first copy starts 5.5 s in (the user's pick "A minus 5.5 s")
            fc = g.ev("(T => [T.bars.length, T.bars.map(b => b.sec.label).filter((x, i, a) => a.indexOf(x) === i), +(T.startAt + T.total - T.endsAt()).toFixed(2), +((T.bars.length * T.len) - (T.endsAt() - T.startAt)).toFixed(2), +(SND.titleSnd.list[0].startAt - (SND.ctx.currentTime)).toFixed(2)])(SND.titleSnd.list[0])")
            print('  title C first copy [bars, sections, -, -, startAt - now]:', fc)
            check(fc[0] == 16 and fc[1] == ['Hum', 'Log', 'Entry', 'Rest'] and -6.5 <= fc[4] <= -4.5, f'title: C is the 0.99.1 song (16 bars, Hum Log Entry Rest) and its first copy starts about 5.5 s in ({fc})')
        g.ev("(L => { const T = L[0], at = SND.ctx.currentTime + 2; T.endsAt = () => at; })(SND.titleSnd.list)"); g.ev("SND.frame(false)")
        check(g.ev("SND.titleSnd.list.length") == 2, 'title: the next copy starts before the last ends (a loop with no gap)')
        if pick == 'C':
            e2 = g.ev("+(SND.titleSnd.list[1].startAt - SND.ctx.currentTime).toFixed(2)")
            check(-0.5 <= e2 <= 0.5, f'title: the next copy plays the whole song from its start ({e2})')
        g.ev("SND.title(false)"); g.step(3)
        st = g.ev("[SND.titleSnd.list.length, SND.titleSnd.hush]"); print('  title off:', st)
        check(st == [0, False], 'title: off, the track fades and the hum comes back')
        pe = [e for e in g.errors if e.startswith('pageerror')]
        if pe: check(False, 'title: page errors: ' + ' | '.join(pe[:3]))
    finally: g.close()
CHECKS += [check_title_music]   # 0.99 (SD3): the title screen's track

if os.environ.get('SOUND_ONLY'): CHECKS = [c for c in CHECKS if re.search(os.environ['SOUND_ONLY'], c.__name__)]   # run only the named checks (a regex), while building
with sync_playwright() as pw:
    for c in CHECKS:
        try: c(pw, sys.argv[1])
        except Exception as e: check(False, f'{c.__name__}: {e}')
print('SOUND CHECK OK' if ok else 'SOUND CHECK FAILED')
sys.exit(0 if ok else 1)
