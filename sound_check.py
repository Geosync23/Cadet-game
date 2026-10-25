# Starship Cadet: sound check (section 27, the SND block; plans/sound/integration-plan.md "Checks to add")
# Sound is silent in every other check (webdriver). Here the game is opened with ?sound&soundlog, which lets SND start
# on a real (Playwright) click and keeps a list of what it played in SND.log.
# The builders each add their own check functions and one entry each to CHECKS at the bottom:
#   core (SD1): silent by default; starts on a tap with ?sound; Settings rows; pause/hidden suspend; SND.fx never draws on
#   R(); the hum and the core hooks (turns 2-5)
#   activities (FX20) and music (FX22b): their own functions
# Setup and environment as for cadet_test.py.  Run:  python3 sound_check.py BUILD.html
import sys, os, pathlib
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

CHECKS = [check_silent_by_default, check_start_and_fx, check_settings_rows, check_pause_suspends, check_core_hooks]
# (activities and music add theirs here)

with sync_playwright() as pw:
    for c in CHECKS:
        try: c(pw, sys.argv[1])
        except Exception as e: check(False, f'{c.__name__}: {e}')
print('SOUND CHECK OK' if ok else 'SOUND CHECK FAILED')
sys.exit(0 if ok else 1)
