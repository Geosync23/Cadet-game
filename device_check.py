# Starship Cadet: device check (keep in the repo, next to player_check.py)
# Checks section 19 (the device engineer): the device's two layers, the apps and the skin.
#   every app registered with deviceApp opens, draws something, and leaves no errors (DEV.errors, the page's errors)
#   the home screen shows the time and a tile for every app, with badges (unread mail on the Mail tile and the button)
#   tapping a tile opens the app; Back goes home; Close and the button close it; deviceOn('open' / 'close') fire once each
#   deviceDo runs an app's action (Mail: reading marks it read); deviceNotify badges an app until it's opened
#   calendar reminders (0.35.2): 25 minutes before a tradition, not 45; Don't and Remind me; Jobs only tracks
#   Maps (0.35.3): every deck draws; picking a room and Go there sets the goal arrow (setGoal)
#   Memos (0.35.4): the form, pin to Home, Remember this on Mail, saved; tips once each with a switch; the phone's
#   camera framing while the sheet is open (deviceFrame), none on wide screens
#   a need's bar pulses while section 15's needPulse says it just rose (0.35.19)
#   the Schedule lists only what really happens (0.35.18): every ship item and tradition for a week has people there
#   deviceChoose (0.35.23): a question with buttons for section 13's New game; Not now and the × give -1; refused while
#   a meeting is up, cancelled by a meeting drawn over it (0.35.25)
#   Pillar 4 pages (0.35.22): the season, reputation in the Record, keepsakes in the Wallet, Left the Wren in the Roster
#   the arrival (0.35.21): locked until handed over, the first switch-on, Settling in with Go there and the end button
#   days off (0.35.17): section 14's playerShiftOn shows Day off in Schedule, the strip and the Calendar
#   never opens by itself (0.35.15): a ship day of reminders, tips, notices, an address, a dialogue, an invitation
#   and a drag up from the bottom edge leave it shut; only the Device button opens it
#   0.35.14: the Maps plan kept between ship minutes, unknown appointment fields kept
#   the phone review (0.35.12): tap the ship to close (a drag doesn't), the bezel's grip and swipe, no rebuild when unchanged
#   Quiet off shift and the #seek chip's look (0.35.11)
#   Calendar days and group meetings (0.35.10): See the day, Make an appointment that day, pick the place on Maps,
#   two or more people (a seat each, kept and cancelled together)
#   the Roster (0.35.16): everyone by department, where they are, quarters for sleepers, Go there; Maps has no people
#   Ship news (0.35.8): section 20's shipNews feed in the Ship app
#   Appointments (0.35.6): ask someone for tomorrow at a meeting place; an answer, booked or offered; saved
#   the meeting panel (deviceDialogue(view, onTap)) and the Captain's address (deviceAddress) draw and report taps
#   the shim: device.addSection(id, title, render) still draws, and never replaces a native app
#   the look (0.35.1): nothing under 15px, buttons 44px high, no blur or backdrop filter, the screen's text 7:1
#   phone and wide sizes: the panel fits on screen; opening it adds nothing to the 3D scene, draw calls stay under 450
# Setup and environment as for cadet_test.py.
# Run:  python3 device_check.py BUILD.html
import sys, json
exec(open(__file__.replace('device_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

ok = True
def check(cond, msg):
    global ok
    if not cond: ok = False; print('FAIL', msg)
    return cond

SIZES = [('phone', 390, 844), ('wide', 1280, 800)]
# the look rules: nothing under 15px, every button 44px high, no blur or backdrop filter, text 7:1 on the screen
LOOK = r"""(() => {
  const dev = document.getElementById('device'), lum = c => { const v = c.match(/[\d.]+/g).slice(0, 3).map(x => +x / 255).map(x => x <= .04045 ? x / 12.92 : ((x + .055) / 1.055) ** 2.4); return .2126 * v[0] + .7152 * v[1] + .0722 * v[2]; };
  const small = [], tiny = [], blur = [];
  for (const e of dev.querySelectorAll('*')) {
    const cs = getComputedStyle(e); if (e.offsetParent === null) continue;
    if (e.childNodes.length && [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) && parseFloat(cs.fontSize) < 15) small.push(e.tagName + ':' + e.textContent.slice(0, 20));
    if (e.tagName === 'BUTTON' && e.getBoundingClientRect().height < 44) tiny.push(e.textContent.slice(0, 20));
    if ((cs.backdropFilter && cs.backdropFilter !== 'none') || (cs.webkitBackdropFilter && cs.webkitBackdropFilter !== 'none') || (cs.filter && cs.filter !== 'none')) blur.push(e.tagName);
  }
  const st = getComputedStyle(dev), ink = lum(st.getPropertyValue('--crt-ink').trim().replace(/^#(..)(..)(..)$/, (m, r, g, b) => `rgb(${parseInt(r, 16)},${parseInt(g, 16)},${parseInt(b, 16)})`)),
    bgc = getComputedStyle(dev.querySelector('.crt')).backgroundColor, bg = lum(bgc);
  return { small: small.slice(0, 4), tiny: tiny.slice(0, 4), blur: blur.slice(0, 4), contrast: Math.round((Math.max(ink, bg) + .05) / (Math.min(ink, bg) + .05) * 10) / 10 };
})()"""

def run(path):
    with sync_playwright() as pw:
        for name, w, h in SIZES:
            print(f'{name} ({w} x {h}):')
            g = Game(pw, path, w, h)
            g.step(3)
            apps = g.ev("deviceApps().map(a => a.id)")
            print('  apps:', apps)
            check(len(apps) >= 4 and all(a in apps for a in ['needs', 'jobs', 'mail', 'wallet']), f'the first apps are there: {apps}')
            MEM = "[scene.children.length, renderer.info.memory.geometries, renderer.info.memory.textures]"
            mem0 = g.ev(MEM)
            g.ev("window.__ev = []; deviceOn('open', () => __ev.push('open')); deviceOn('close', () => __ev.push('close'))")
            # the home screen
            g.page.click('#devBtn'); g.step(2)
            home = g.ev("""(() => { const b = document.getElementById('devBody'); return { open: !document.getElementById('device').hidden, app: DEV.app,
              tiles: [...b.querySelectorAll('.apps .app')].map(t => t.dataset.app), text: b.textContent, back: !document.getElementById('devBack').disabled }; })()""")
            check(home['open'] and home['app'] == 'home' and not home['back'], f'the button opens the home screen: {home["app"]}')
            check(home['tiles'] == apps, f'a tile for every app, in order: {home["tiles"]}')
            check('Day ' in home['text'], 'the home screen shows the day and time')
            mem1, calls1 = g.ev(MEM), g.ev("renderer.info.render.calls")
            check(mem1[0] == mem0[0] and calls1 < 450, f'no 3D objects added while open, draw calls under 450: {mem0} -> {mem1}, {calls1} calls')
            # (on a phone the framing shows a little more of the deck, so the first open may upload a few shared things once)
            # every app opens and draws
            for a in apps:
                g.page.click(f'#devBody .apps .app[data-app="{a}"]'); g.step(1)
                r = g.ev("""(() => { const b = document.getElementById('devBody'); return { app: DEV.app, kids: b.children.length, text: b.textContent.slice(0, 80),
                  head: document.getElementById('devT').textContent, back: !document.getElementById('devBack').disabled, failed: b.textContent.includes('failed to draw') }; })()""")
                print(f'  {a}: {r["head"]!r} {r["text"]!r}')
                check(r['app'] == a and r['kids'] > 0 and r['back'] and not r['failed'], f'{a} opens and draws: {r}')
                lk = g.ev(LOOK)
                check(not lk['small'] and not lk['tiny'] and not lk['blur'] and lk['contrast'] >= 7, f'{a}: the look rules (15px+, 44px targets, no blur, 7:1): {lk}')
                g.page.click('#devBack'); g.step(1)
                check(g.ev("DEV.app") == 'home', f'Back from {a} goes home')
            # mail: badge, read through deviceDo, tile badge clears
            ml = g.ev("""(() => { SHIP.mail = []; mailSend({ from: 'Stores', subject: 'Filters low', body: 'Two left.' }); deviceRefresh();
              const out = { btn: document.getElementById('devMail').textContent, tile: (document.querySelector('#devBody .app[data-app="mail"] b') || {}).textContent };
              deviceShow('mail'); document.querySelector('#devBody button.row').click();
              out.read = mailUnread(); out.body = document.getElementById('devBody').textContent.includes('Two left.'); deviceShow('home'); return out; })()""")
            check(ml == {'btn': '1', 'tile': '1', 'read': 0, 'body': True}, f'mail: badges, tap to read: {ml}')
            # notify: a badge until the app is opened; urgent ones toast
            nt = g.ev("""(() => { deviceNotify({ app: 'wallet', text: 'Paid', urgent: true }); const t = (document.querySelector('#devBody .app[data-app="wallet"] b') || {}).textContent;
              const toast = document.getElementById('tx').textContent; deviceShow('wallet'); deviceShow('home');
              return [t, toast, !!document.querySelector('#devBody .app[data-app="wallet"] b')]; })()""")
            check(nt == ['1', 'Paid', False], f'deviceNotify: badge, toast, cleared on opening: {nt}')
            # calendar reminders: about 30 ship minutes before a tradition; a toast off shift, a quiet badge on shift,
            # none for one marked Don't; Remind me chirps even on shift
            rm = g.ev("""(() => { const t0 = shipNow(), d = SHIP.time.day, R = SHIP.device.calendarRemind, out = {};
              const tr = devTraditions(t0, t0 + 14 * 1440); if (!tr.length) return 'no traditions in two weeks';
              const x = tr[0], save = { day: SHIP.time.day, min: SHIP.time.min };
              const at = (m, f) => { SHIP.time.day = Math.floor(m / 1440) + 1; SHIP.time.min = ((m % 1440) + 1440) % 1440; DEV_REMINDED.clear(); delete DEV.notes.calendar;
                document.getElementById('tx').textContent = ''; devTickMin = -1; f && f(); deviceTick(); return [DEV.notes.calendar || 0, document.getElementById('tx').textContent]; };
              out.kind = x.kind; out.when = devWhen(x.at);
              out.before = at(x.at - 25); out.early = at(x.at - 45);
              R.per[x.kind] = false; out.dont = at(x.at - 25);
              const onShift = (x.at % 1440) - 25 >= DEV_SHIFT.from && (x.at % 1440) - 25 < DEV_SHIFT.to;
              R.per[x.kind] = true; out.remind = at(x.at - 25); delete R.per[x.kind];
              out.onShift = onShift;
              SHIP.time.day = save.day; SHIP.time.min = save.min; DEV_REMINDED.clear(); delete DEV.notes.calendar; devTickMin = -1; return out; })()""")
            print('  reminders:', rm)
            if check(isinstance(rm, dict), f'reminders: {rm}'):
                check(rm['before'][0] == 1 and (rm['onShift'] or rm['when'] in rm['before'][1]), f'a reminder 25 minutes before (a toast unless on shift): {rm["before"]}')
                check(rm['early'][0] == 0, f'nothing 45 minutes before: {rm["early"]}')
                check(rm['dont'][0] == 0, f"nothing for one marked Don't: {rm['dont']}")
                check(rm['remind'][0] == 1 and rm['when'] in rm['remind'][1], f'Remind me always chirps: {rm["remind"]}')
            # Jobs tracks only: no Take it on the device; Track switches the arrow off and on
            jb = g.ev("""(() => { deviceShow('jobs'); const t = document.getElementById('devBody').textContent; deviceShow('home'); return [t.includes('Take it'), t.includes('job board')]; })()""")
            check(jb == [False, True], f'Jobs: no taking on the device, points to the board: {jb}')
            # Maps: every deck draws; tap a room on the plan, Go there points the goal arrow at it
            mp = g.ev("""(() => { const out = {}; deviceShow('maps');
              for (const n of Object.keys(DECKS)) { deviceDo({ app: 'maps', do: 'deck', arg: +n }); out[n] = document.querySelectorAll('#devBody .devmap rect[data-room]').length; }
              deviceDo({ app: 'maps', do: 'deck', arg: 3 }); const r = [...document.querySelectorAll('#devBody .devmap rect[data-room]')].find(x => DECKS[3].rooms[x.dataset.room] && /galley|mess/i.test(DECKS[3].rooms[x.dataset.room].name));
              r.dispatchEvent(new MouseEvent('click', { bubbles: true }));
              const go = [...document.querySelectorAll('#devBody .btns .act')].find(b => b.textContent === 'Go there'); go && go.click();
              out.goal = IX_GOAL && [IX_GOAL.deck, IX_GOAL.room, IX_GOAL.label]; clearGoal(); deviceShow('home'); return out; })()""")
            print('  maps:', mp)
            check(all(mp[n] > 5 for n in mp if n != 'goal'), f'every deck draws its rooms: {mp}')
            check(mp['goal'] and mp['goal'][0] == 3 and isinstance(mp['goal'][1], str), f'Go there sets the goal arrow: {mp["goal"]}')
            # Maps has no people (0.35.16, the user's answer); the plan is kept between ship minutes (0.35.14); appointments
            # keep fields other sections add (socKept)
            pp = g.ev("""(() => { deviceShow('maps'); const out = [];
              for (const n of Object.keys(DECKS)) { deviceDo({ app: 'maps', do: 'deck', arg: +n }); out.push(document.querySelectorAll('#devBody .devmap circle.m-per').length); }
              const s1 = document.querySelector('#devBody .devmap'); deviceRefresh(); DEVICE_SKIN.draw('maps', Object.assign(deviceView('maps'), { title: 'Maps again' }));
              const s2 = document.querySelector('#devBody .devmap'); deviceDo({ app: 'maps', do: 'deck', arg: deckDef.num }); deviceShow('home');
              return [out.every(x => x === 0), s1 === s2, !document.getElementById('devBody').textContent.includes('On duty on this deck'),
                deviceLoad({ device: { appts: [{ id: 1, with: ['calder'], at: 9000, where: '3-mess-1', status: 'kept', socKept: true }] } }).appts[0].socKept === true]; })()""")
            check(pp == [True, True, True, True], f'Maps: no people on any deck, the plan kept between ship minutes; other sections\' appointment fields kept: {pp}')
            # the Roster (0.35.16): everyone by department, people you know first; tap a name for where they are; asleep or
            # washing reads "In their quarters"; Go there aims the arrow at their room; Maps' old person links open it
            rs = g.ev("""(() => { const save = { day: SHIP.time.day, min: SHIP.time.min }, out = {}, ps = rosterPeople(); out.n = ps.length;
              deviceShow('roster'); const t = document.getElementById('devBody').textContent; out.depts = ['Command', 'Works', 'Galley'].every(d => t.includes(d));
              SHIP.time.min = 120; const sleeper = ps.find(x => { try { const w = whereIs(x.p, shipNow()); return w && w.act === 'sleep'; } catch (e) { return false; } });
              out.sleep = sleeper ? rosterWhere(sleeper.p).line : 'nobody asleep';
              SHIP.time.min = 600; const worker = ps.find(x => rosterWhere(x.p).room && /^On duty/.test(rosterWhere(x.p).line));
              if (worker) { deviceDo({ app: 'roster', do: 'pick', arg: worker.p.id }); out.line = document.getElementById('devBody').textContent.includes(rosterWhere(worker.p).line);
                const go = [...document.querySelectorAll('#devBody .btns .act')].find(b => b.textContent === 'Go there'); go && go.click();
                const w = rosterWhere(worker.p); out.goal = !!(IX_GOAL && IX_GOAL.deck === w.deck && IX_GOAL.room === w.room); clearGoal(); }
              deviceShow('home'); deviceDo({ app: 'maps', who: ps[0].p.id }); out.who = [DEV.app, rosterPick === ps[0].p.id];
              deviceShow('home'); deviceDo({ app: 'maps', do: 'person', arg: ps[1].p.id }); out.person = [DEV.app, rosterPick === ps[1].p.id];
              rosterPick = null; SHIP.time.day = save.day; SHIP.time.min = save.min; deviceShow('home'); return out; })()""")
            print('  roster:', rs)
            check(rs.get('n', 0) >= 20 and rs.get('depts') and rs.get('sleep') == 'In their quarters.' and rs.get('line') and rs.get('goal')
                  and rs.get('who') == ['roster', True] and rs.get('person') == ['roster', True], f'Roster: everyone by department, quarters for sleepers, where and Go there, Maps links: {rs}')
            # Memos: write one with the form, it's saved in SHIP.device and pins to Home; Mail's Remember this makes one
            mm = g.ev("""(() => { SHIP.device.memos = []; deviceShow('memos'); deviceDo({ app: 'memos', do: 'new' });
              const f = document.querySelector('#devBody form.devform'); if (!f) return 'no form';
              f.querySelector('input').value = 'Ask Pell'; f.querySelector('textarea').value = 'About the fan hall.'; f.requestSubmit();
              const out = [SHIP.device.memos.map(m => m.title)]; deviceDo({ app: 'memos', do: 'pin', arg: SHIP.device.memos[0].id }); deviceShow('home');
              out.push(document.getElementById('devBody').textContent.includes('Ask Pell: About the fan hall.'));
              mailSend({ from: 'Galley', subject: 'Cake tonight', body: 'Tomas turns 24.' }); const id = SHIP.mail[0].id;
              deviceDo({ app: 'mail', do: 'remember', arg: id }); out.push(SHIP.device.memos[0].title);
              const sv = JSON.parse(JSON.stringify({ device: SHIP.device })); out.push(sv.device.memos.length, deviceLoad(sv).memos.length, deviceLoad({ device: { memos: [7, null, { title: 3 }] } }).memos.length);
              SHIP.device.memos = []; return out; })()""")
            check(mm == [['Ask Pell'], True, 'Cake tonight', 2, 2, 0], f'memos: the form, pin to Home, Remember this, saved and read back, junk refused: {mm}')
            # tips: once each, saved, off in Settings; the card closes on a tap
            tp = g.ev("""(() => { const D = SHIP.device; while (TIP_Q.length) tipDone(); D.tipsSeen = {}; const out = [tipShow('t1', 'First tip'), tipShow('t1', 'Again')];
              const c = document.getElementById('devTip'); out.push(!c.hidden && c.textContent.includes('First tip')); c.click(); out.push(c.hidden);
              D.settings.tips = false; out.push(tipShow('t2', 'Off')); D.settings.tips = true; out.push(!!D.tipsSeen.t1); D.tipsSeen = {}; return out; })()""")
            check(tp == [True, False, True, True, False, True], f'tips: once each, a tap closes, the switch: {tp}')
            # Ship news (0.35.8): section 20's shipNews, newest first (a stand-in when this build has none)
            sn = g.ev("""(() => { const own = typeof shipNews === 'function'; if (!own) window.shipNews = n => [{ text: 'The scrubber on Deck 4 is rattling.', from: 'Pell Varga', at: shipNow() - 30 }].slice(0, n);
              const out = [own, devNews().length]; deviceShow('ship'); const t = document.getElementById('devBody').textContent;
              out.push(t.includes('Ship news'), !devNews().length || t.includes(devNews()[0].text)); if (!own) delete window.shipNews; deviceShow('home'); return out; })()""")
            print('  ship news:', sn)
            check(sn[1] >= (0 if sn[0] else 1) and sn[2] and sn[3], f'Ship news: the feed shows in the Ship app: {sn}')
            # an action with no verb opens its app (the social engineer's Meet up: { app: 'appointments', with })
            ap = g.ev("(() => { deviceDo({ app: 'appointments', with: 'calder' }); const a = DEV.app; deviceShow('home'); return a; })()")
            check(ap == 'appointments', f'deviceDo with no verb opens the app: {ap}')
            # Appointments: who, when, where, ask; the answer comes from section 14's apptReply when it's there
            at = g.ev("""(() => { SHIP.device.appts = []; deviceShow('appointments'); deviceDo({ app: 'appointments', do: 'new' });
              const who = apptPeople()[0], pl = apptPlaces(); if (!who || !pl.length) return ['no people or places', !!who, pl.length];
              deviceDo({ app: 'appointments', do: 'who', arg: who.id }); deviceDo({ app: 'appointments', do: 'day', arg: SHIP.time.day + 1 });
              deviceDo({ app: 'appointments', do: 'where', arg: pl[0].id }); deviceDo({ app: 'appointments', do: 'ask' });
              const out = [pl.length, typeof apptSay, SHIP.device.appts.length + (apptDraft && apptDraft.later ? 1 : 0) + (/Sorry/.test(apptSay || '') ? 1 : 0)];
              const sv = JSON.parse(JSON.stringify({ device: SHIP.device })); out.push(deviceLoad(sv).appts.length === SHIP.device.appts.length);
              apptDraft = null; apptSay = null; SHIP.device.appts = []; deviceShow('home'); return out; })()""")
            print('  appointments:', at)
            check(at[0] >= 5 and at[1] == 'string' and at[2] == 1 and at[3] is True, f'appointments: places, an answer, booked or offered, saved: {at}')
            # group meetings (0.35.10): two people, a seat each, one grp; one row in Coming up; cancelling drops both;
            # meeting one of them keeps them all
            gm = g.ev("""(() => { const D = SHIP.device; D.appts = []; deviceShow('appointments'); deviceDo({ app: 'appointments', do: 'new' });
              const ps = apptPeople().slice(0, 2), pl = apptPlaces().find(x => /mess|lounge/i.test(x.name)) || apptPlaces()[0];
              for (const p of ps) deviceDo({ app: 'appointments', do: 'who', arg: p.id });
              deviceDo({ app: 'appointments', do: 'day', arg: SHIP.time.day + 1 }); deviceDo({ app: 'appointments', do: 'where', arg: pl.id });
              const out = [apptDraft.with.length, [...document.querySelectorAll('#devBody .btns .act')].some(b => b.textContent === 'Ask all 2')];
              deviceDo({ app: 'appointments', do: 'ask' });
              out.push(typeof apptSay === 'string' && (apptDraft === null ? D.appts.length === 2 : !!(apptDraft.later || apptDraft.some || /another time/.test(apptSay))));
              D.appts = []; apptDraft = { with: ps.map(p => p.id), day: SHIP.time.day + 1, min: 1140, where: pl.id }; const at = SHIP.time.day * 1440 + 1140;
              apptBook(apptDraft.with, at, 30, 'social'); apptDraft = null; apptSay = null; deviceShow('appointments');
              const A = D.appts; out.push(A.length, A[0].grp === A[1].grp && !!A[0].grp, A[0].where !== A[1].where);
              const sv = JSON.parse(JSON.stringify({ device: D })); out.push(deviceLoad(sv).appts.every(a => a.grp === A[0].grp));
              const t = document.getElementById('devBody').textContent; out.push(t.includes(apptName(ps[0].id) + ', ' + apptName(ps[1].id)));
              const save = { day: SHIP.time.day, min: SHIP.time.min }; SHIP.time.day = Math.floor(at / 1440) + 1; SHIP.time.min = at % 1440 + 3;
              A[0].status = 'kept'; devTickMin = -1; deviceTick(); out.push(A[1].status);
              SHIP.time.day = save.day; SHIP.time.min = save.min; devTickMin = -1; DEV_REMINDED.clear();
              A[0].status = A[1].status = 'yes'; deviceDo({ app: 'appointments', do: 'drop', arg: A[0].id }); out.push(A.map(a => a.status).join());
              D.appts = []; deviceShow('home'); return out; })()""")
            print('  group meeting:', gm)
            check(gm == [2, True, True, 2, True, True, True, True, 'kept', 'no,no'], f'group meetings: ask all, a seat each, saved, one row, kept together, cancelled together: {gm}')
            # a need's bar pulses (0.35.19) while section 15's needPulse(k) says it just rose (a stand-in when there's none)
            # with section 15's own needPulse (it reads NEED_PULSE[k], a time, and a const can't be swapped) the check sets that
            # time; without it, a stand-in function
            g.ev("""(() => { window.__ownPulse = typeof needPulse === 'function' && typeof NEED_PULSE !== 'undefined';
              if (__ownPulse) { for (const k in NEED_PULSE) delete NEED_PULSE[k]; NEED_PULSE.energy = performance.now() + 1e9; }
              else { window.__pk = 'energy'; window.needPulse = k => k === window.__pk; } deviceShow('needs'); })()"""); g.step(2)
            p1 = g.ev("[...document.querySelectorAll('#devBody .need.pulse')].map(r => r.getAttribute('aria-label'))")
            g.ev("if (window.__ownPulse) delete NEED_PULSE.energy; else window.__pk = null"); g.step(2)
            p2 = g.ev("document.querySelectorAll('#devBody .need.pulse').length")
            g.ev("if (!window.__ownPulse) delete window.needPulse; deviceShow('home')")   # (0.35.20: works with the real needPulse too)
            check(p1 == [g.ev("NEED_LABEL.energy")] and p2 == 0, f'Needs: the bar pulses while it has just risen, then stops: {p1} {p2}')
            # the Schedule only lists what really happens (0.35.18, the user: "the schedule says there is a Works meeting but
            # nothing happened"): for a week, every ship item and tradition has at least two people there doing it (an
            # event's tag, the drill, the bunk tidy) within its first half hour, on its deck
            sh = g.ev("""(() => { const S = schedData(), bad = [], seen = []; const d0 = SHIP.time.day;
              for (let d = d0; d < d0 + 7; d++) for (const x of devDay(d)) {
                if (x.kind !== 'ship' && x.kind !== 'tradition') continue;
                const m = /Deck (\\d)/.exec(x.where), deck = m ? +m[1] : null; let best = 0;
                for (let k = 0; k <= 30; k += 5) { let n = 0; const t = (d - 1) * 1440 + x.from + k;
                  for (const p of S.people) { let w = null; try { w = whereIs(p, t); } catch (e) {} if (w && w.tag && /^(ev-|drill$|inspection$)/.test(w.tag) && (!deck || w.deck === deck || x.kind === 'ship')) n++; }
                  best = Math.max(best, n); }
                seen.push(x.title); if (best < 2) bad.push(d + ' ' + hhmm(x.from) + ' ' + x.title + ' (' + best + ')'); }
              return [seen.length, bad, seen.some(t => /briefing/i.test(t))]; })()""")
            print('  schedule items checked:', sh[0], 'not happening:', sh[1])
            check(sh[0] >= 5 and not sh[1] and not sh[2], f'the Schedule lists only what really happens: {sh}')
            # days off (0.35.17): section 14's playerShiftOn(d) (a stand-in here: Saturday and Sunday off) shows "Day off" in
            # Schedule, the strip and the Calendar, with no shift that day
            do = g.ev("""(() => { const own = typeof playerShiftOn === 'function'; if (!own) window.playerShiftOn = d => weekday(d) < 5;
              let d = SHIP.time.day; while (weekday(d) !== 5) d++; const out = [own, devDay(d).some(x => x.kind === 'shift'), devDay(d).some(x => x.title === 'Day off')];
              let w = SHIP.time.day; while (weekday(w) >= 5) w++; out.push(devDay(w).some(x => x.kind === 'shift'));
              const save = { day: SHIP.time.day, min: SHIP.time.min }; SHIP.time.day = d; SHIP.time.min = 600;
              deviceShow('schedule'); out.push(document.getElementById('devBody').textContent.includes('Day off'), devNow().now.startsWith('Day off'));
              SHIP.time.day = save.day; SHIP.time.min = save.min; deviceShow('calendar'); out.push(document.getElementById('devBody').textContent.includes('Day off'));
              if (!own) delete window.playerShiftOn; deviceShow('home'); return out; })()""")
            check(do[1:] == [False, True, True, True, True, True], f'days off: no shift, "Day off" in Schedule, the strip and the Calendar: {do}')
            # the Calendar's days (0.35.10): tap a day, See the day (Schedule shows it), Make an appointment (that day);
            # Pick on the map, then Meet here sets the place
            cd = g.ev("""(() => { const d = SHIP.time.day + 4, out = []; deviceShow('calendar'); deviceDo({ app: 'calendar', do: 'day', arg: d });
              const bs = [...document.querySelectorAll('#devBody .btns .act')].map(b => b.textContent); out.push(bs.includes('See the day') && bs.includes('Make an appointment'));
              deviceDo({ app: 'schedule', day: d }); out.push(DEV.app, document.getElementById('devBody').textContent.includes(WEEKDAYS[weekday(d)] + ', Day ' + d));
              deviceDo({ app: 'appointments', day: d }); out.push(DEV.app, apptDraft && apptDraft.day === d, apptDraft && apptDraft.min);
              deviceDo({ app: 'appointments', do: 'map' }); out.push(DEV.app, mapFor);
              const k = Object.keys(DECKS[3].rooms).find(x => /mess/i.test(DECKS[3].rooms[x].name || '')); deviceDo({ app: 'maps', do: 'deck', arg: 3 }); deviceDo({ app: 'maps', do: 'pick', arg: k });
              const meet = [...document.querySelectorAll('#devBody .btns .act')].find(b => b.textContent === 'Meet here'); meet && meet.click();
              out.push(DEV.app, !!(apptDraft && apptDraft.where && apptDeckOf(apptDraft.where) === 3), mapFor);
              apptDraft = null; calDay = null; schedDay = null; deviceShow('home'); return out; })()""")
            print('  calendar days:', cd)
            check(cd == [True, 'schedule', True, 'appointments', True, 1080, 'maps', 'appointments', 'appointments', True, None], f'Calendar days: see the day, an appointment that day, a place from Maps: {cd}')
            # Quiet off shift (0.35.11): off shift, a work notice is a badge, not a toast; on shift it still toasts.
            # Section 20's #seek chip in the screen's style (a stand-in chip when the build has none)
            qt = g.ev("""(() => { const st = SHIP.device.settings, save = SHIP.time.min, tx = () => document.getElementById('tx').textContent, out = [];
              st.quiet = true; SHIP.time.min = 1200; document.getElementById('tx').textContent = ''; deviceNotify({ app: 'jobs', text: 'Quiet test', urgent: true }); out.push(DEV.notes.jobs, tx().includes('Quiet test'));
              SHIP.time.min = 600; deviceNotify({ app: 'jobs', text: 'Shift test', urgent: true }); out.push(tx().includes('Shift test'));
              st.quiet = false; SHIP.time.min = 1200; deviceNotify({ app: 'jobs', text: 'Loud test', urgent: true }); out.push(tx().includes('Loud test'));
              SHIP.time.min = save; delete DEV.notes.jobs; document.getElementById('tx').textContent = '';
              out.push(deviceLoad({ device: { settings: { quiet: true } } }).settings.quiet, deviceLoad({}).settings.quiet);
              let sk = document.getElementById('seek'), made = false; if (!sk) { sk = document.createElement('div'); sk.id = 'seek'; sk.innerHTML = '<b>Tomas</b> waves you over.'; document.body.appendChild(sk); made = true; }
              const was = sk.hidden; sk.hidden = false; const cs = getComputedStyle(sk); out.push(cs.fontFamily.includes('monospace'), parseFloat(cs.fontSize) >= 15, cs.backdropFilter === 'none' || !cs.backdropFilter, sk.getBoundingClientRect().height >= 44);
              sk.hidden = was; if (made) sk.remove(); return out; })()""")
            check(qt == [1, False, True, True, True, False, True, True, True, True], f'Quiet off shift, saved; the #seek chip in the screen style: {qt}')
            # the meeting panel and the Captain's address: they draw, and taps report back
            dl = g.ev("""(() => { const got = []; deviceDialogue({ title: 'Briefing', name: 'Chief Ines Calder', who: 'calder', text: 'Gather round.', choices: null, i: 0, n: 2 }, k => got.push(k === undefined ? 'next' : k));
              const p = document.getElementById('devDlg'); const out = [!p.hidden, p.textContent.includes('Gather round.')]; p.querySelector('.next').click();
              deviceDialogue({ title: 'Briefing', name: 'You', text: '', choices: ['Yes', 'No'], i: 1, n: 2 }, k => got.push(k)); p.querySelectorAll('.btns .act')[1].click();
              deviceDialogue(null); out.push(p.hidden, got.join(','));
              deviceAddress({ from: 'Captain Odile Marrow', text: 'All hands, the storm has passed.' }); const a = document.getElementById('devAddr'); out.push(!a.hidden && a.textContent.includes('storm has passed'));
              a.click(); out.push(a.hidden); return out; })()""")
            check(dl == [True, True, True, 'next,1', True, True], f'meeting panel and address: {dl}')
            # the shim
            sh = g.ev("""(() => { device.addSection('test', 'Test', el => { el.textContent = 'shim works'; }); device.addSection('mail', 'Old inbox', el => { el.textContent = 'old'; });
              device.show('test'); const a = document.getElementById('devBody').textContent; device.show('mail'); const b = document.getElementById('devT').textContent;
              DEVICE_APPS.delete('test'); device.show('status'); return [a, b, DEV.app]; })()""")
            check(sh == ['shim works', 'Mail', 'home'], f'addSection shim: {sh}')
            # it fits on screen
            box = g.ev("(() => { const r = document.getElementById('device').getBoundingClientRect(); return [r.left, r.top, r.right, r.bottom]; })()")
            check(box[0] >= 0 and box[1] >= 0 and box[2] <= w and box[3] <= h, f'the panel fits on screen: {box}')
            g.page.click('#devClose'); g.step(1)
            check(g.ev("document.getElementById('device').hidden && !DEV.open"), 'Close closes it')
            g.page.click('#devBtn'); g.step(1); g.page.click('#devClose'); g.step(1)   # wide: the side panel covers the button; Close is the way out
            g.step(60)
            fr = g.ev("[DEV.frOn, Math.round(DEV.fr * 100) / 100, Math.round((camera.top + camera.bottom) * 1000) / 1000]")
            check(fr[0] is False and fr[2] == 0, f'after closing, the camera is centred again: {fr}')
            g.ev("deviceShow('home')"); g.step(60)
            fo = g.ev("[DEV.frOn, Math.round(DEV.fr * 100) / 100, Math.round((camera.top + camera.bottom) * 1000) / 1000]")
            if name == 'phone': check(fo[0] is True and fo[1] == 1 and fo[2] < 0, f'phone: the view eases so you stay above the sheet: {fo}')
            else: check(fo[0] is False and fo[2] == 0, f'wide: no reframing for the side panel: {fo}')
            g.ev("deviceClose()"); g.step(60)
            m1 = g.ev(MEM); g.ev("deviceShow('home')"); g.step(60); g.ev("deviceClose()"); g.step(60); m2 = g.ev(MEM)
            check(m1 == m2, f'opening again adds nothing (no leak): {m1} -> {m2}')
            ev = g.ev("__ev")
            check(ev == ['open', 'close', 'open', 'close', 'open', 'close', 'open', 'close'], f'deviceOn fires once per open and close: {ev}')
            # the arrival (0.35.21): locked until it's handed over (section 15's deviceLocked, section 21's flag), the first
            # switch-on once, Settling in (section 21's SETTLE) with Go there and "I know my way around" (introEnd).
            # Stand-ins when the build has no sections 15/21 for this; with them, their real state is set and put back
            g.ev("deviceClose()"); g.step(1)
            ar = g.ev("""(() => { const out = {}, real = typeof SETTLE !== 'undefined' && typeof introOn === 'function' && typeof deviceLocked === 'function';
              const keepIntro = SHIP.intro ? JSON.parse(JSON.stringify(SHIP.intro)) : undefined, keepBoot = SHIP.device.booted;
              const lock = on => { if (real) { SHIP.intro.on = true; SHIP.intro.ended = false; if (typeof introFlagSet === 'function') introFlagSet('intro.device', on ? null : true); } else window.deviceLocked = () => on; };
              if (!real) { SHIP.intro = { on: true, skipped: false, ended: false, settle: {} }; window.introOn = () => true; window.introEnd = () => { window.__ended = true; };
                window.SETTLE = [{ id: 'washed', title: 'Washed and fed', teacher: 'tomas', place: { deck: 4, room: 'Port washroom' } }, { id: 'eat', title: 'Eat with the crew', teacher: 'brennan', place: { deck: 3, room: 'Mess hall' } }, { id: 'friend', title: 'Make a friend', teacher: 'pell', place: null }]; }
              else { window.__ended = false; SHIP.intro.settle = {}; }
              lock(true); mailSend({ from: 'Stores', subject: 'Locked test', body: '.' }); deviceRefresh();
              document.getElementById('devBtn').click(); out.locked = [DEV.open, document.getElementById('devMail') ? document.getElementById('devMail').hidden : true];
              devTickMin = -1; deviceTick(); out.bootReset = SHIP.device.booted === false;
              lock(false); document.getElementById('devBtn').click(); out.boot = [DEV.open, DEV.app, document.getElementById('devBody').textContent.includes('Assigned to')];
              deviceClose(); document.getElementById('devBtn').click(); out.second = DEV.app;
              const L = SETTLE; SHIP.intro.settle = { [L[0].id]: 100 };
              out.listed = deviceApps().some(a => a.id === 'settle'); deviceShow('settle'); const t = document.getElementById('devBody').textContent;
              out.count = t.includes('1 of ' + L.length); out.done = t.includes('✓ ' + L[0].title);
              const go = [...document.querySelectorAll('#devBody .row button')].find(b => b.textContent === 'Go there'); out.go = !!go; if (go) { go.click(); out.goal = !!IX_GOAL; clearGoal(); }
              deviceShow('home'); out.home = document.getElementById('devBody').textContent.includes('Settling in: 1 of ' + L.length);
              if (real) { const endF = introEnd; window.__endCalls = 0; }
              deviceShow('settle'); const endB = () => [...document.querySelectorAll('#devBody .btns .act')].find(b => /way around|end the welcome/.test(b.textContent));
              endB().click(); out.firstTap = /end the welcome/.test(endB().textContent);
              deviceShow('home'); deviceShow('settle'); out.reset = /way around/.test(endB().textContent);   // 0.35.24: leaving clears the confirm
              endB().click(); endB().click();
              out.ended = real ? !!SHIP.intro.ended : !!window.__ended;
              SHIP.intro.settle = { all: 1 }; out.hiddenWhenAll = !deviceApps().some(a => a.id === 'settle');
              deviceShow('home');
              if (real) { SHIP.intro = keepIntro; } else { SHIP.intro = keepIntro; for (const k of ['deviceLocked', 'introOn', 'introEnd', 'SETTLE', '__ended']) delete window[k]; }
              SHIP.device.booted = keepBoot; SHIP.mail = SHIP.mail.filter(m => m.subject !== 'Locked test'); settleSure = false; return out; })()""")
            print('  arrival:', ar)
            check(ar.get('locked') == [False, True] and ar.get('bootReset') and ar.get('boot') == [True, 'boot', True] and ar.get('second') == 'home'
                  and ar.get('listed') and ar.get('count') and ar.get('done') and ar.get('go') and ar.get('goal') and ar.get('home')
                  and ar.get('firstTap') and ar.get('reset') and ar.get('ended') and ar.get('hiddenWhenAll'), f'the arrival: locked, the first switch-on once, Settling in, the end button: {ar}')
            # deviceChoose (0.35.23): a question in the panel's style (section 13's New game asks it); the choice's index, -1 for
            # Not now and for the ×; the panel goes
            ch = g.ev("""(() => { const got = [], q = { title: 'New game', text: 'How do you want to start?', choices: ['Arrive by shuttle (Sunday evening)', 'Skip to Monday morning'] };
              deviceChoose(q, k => got.push(k)); const p = document.getElementById('devDlg'), out = [!p.hidden, p.textContent.includes('How do you want to start?'), p.querySelectorAll('.btns .act').length];
              p.querySelectorAll('.btns .act')[1].click(); out.push(p.hidden);
              deviceChoose(q, k => got.push(k)); p.querySelectorAll('.btns .act')[2].click();
              deviceChoose(q, k => got.push(k)); p.querySelector('.x').click(); out.push(p.hidden, got.join(','), !DEV.choose); return out; })()""")
            check(ch == [True, True, 3, True, True, '1,-1,-1', True], f'deviceChoose: the question, a choice, Not now, the ×: {ch}')
            # 0.35.25 (reviewer 2): one panel for both. A question is refused while a meeting is up; a meeting drawn over a
            # question cancels it (-1) and keeps its own taps and ×
            cm = g.ev("""(() => { const got = [], taps = [], q = { title: 'New game', text: 'Start?', choices: ['A', 'B'] }, p = document.getElementById('devDlg');
              deviceDialogue({ title: 'Briefing', name: 'Chief', text: 'Gather round.', choices: null, i: 0, n: 1 }, k => taps.push(k === undefined ? 'next' : k));
              const out = [deviceChoose(q, k => got.push(k)), p.textContent.includes('Gather round.')];
              deviceDialogue(null); out.push(deviceChoose(q, k => got.push('q' + k)));
              deviceDialogue({ title: 'Briefing', name: 'Chief', text: 'Over here.', choices: null, i: 0, n: 1 }, k => taps.push(k === undefined ? 'next' : k));
              out.push(got.join(','), !DEV.choose, p.textContent.includes('Over here.')); p.querySelector('.next').click(); out.push(taps.join(','));
              deviceDialogue(null); out.push(p.hidden); return out; })()""")
            check(cm == [False, True, True, 'q-1', True, True, 'next', True], f'deviceChoose and meetings share the panel safely: {cm}')
            # Pillar 4 pages (0.35.22): the season on Home and the Calendar (section 18's seasonOf), reputation in the Record
            # (section 20's repView, words only), keepsakes in the Wallet (keepsakes), "Left the Wren" in the Roster
            # (movedOn; they leave the lists). Stand-ins without them; with them, section 20's own state is set and put back
            p4 = g.ev("""(() => { const out = {}, has = n => { try { return eval('typeof ' + n) === 'function'; } catch (e) { return false; } };
              const own = { season: has('seasonOf'), rep: has('repView'), keep: has('keepsakes'), moved: has('movedOn') };
              if (!own.season) window.seasonOf = d => ({ id: 'sowing', name: 'Sowing', day: d, week: Math.ceil(d / 7) });
              if (!own.rep) window.repView = () => ({ depts: [{ dept: 'works', band: 'known', name: 'They know your name' }, { dept: 'helm', band: 'new', name: 'New face' }],
                ship: { work: 'Work: steady', kindness: 'Kindness: kind', spirit: 'Spirit: cheerful' }, knownFor: ['fixing fans'], notes: [{ day: 3, from: 'Chief Calder', text: 'Good work on the scrubber.' }] });
              const keepSoc = own.keep || own.moved ? JSON.stringify({ k: SHIP.social.keepsakes || null, m: SHIP.social.moved || null }) : null;
              if (own.keep) (SHIP.social.keepsakes = SHIP.social.keepsakes || []).push({ from: 'tomas', what: 'a brass compass', day: 4 });
              else window.keepsakes = () => [{ from: 'tomas', what: 'a brass compass', day: 4, name: 'Tomas' }];
              if (own.moved) (SHIP.social.moved = SHIP.social.moved || []).push({ id: 'pell', day: 9 });
              else { window.movedOn = () => [{ id: 'pell', name: apptName('pell'), role: 'Works technician', day: 9, to: null }]; window.movedOff = id => id === 'pell'; }
              const sn = seasonOf(SHIP.time.day).name;
              deviceShow('home'); out.home = document.getElementById('devBody').textContent.includes('Season: ' + sn);
              deviceShow('calendar'); out.cal = document.getElementById('devBody').textContent.includes('Season: ' + sn);
              deviceShow('record'); const r = document.getElementById('devBody').textContent; out.rep = r.includes('Reputation') && (own.rep || r.includes('They know your name') && r.includes('Known for: fixing fans'));
              deviceShow('wallet'); out.keep = document.getElementById('devBody').textContent.includes('A brass compass');
              deviceShow('roster'); const ro = document.getElementById('devBody').textContent; out.left = ro.includes('Left the Wren') && !rosterPeople().some(x => x.p.id === 'pell');
              if (keepSoc) { const k = JSON.parse(keepSoc); if (own.keep) { if (k.k) SHIP.social.keepsakes = k.k; else delete SHIP.social.keepsakes; } if (own.moved) { if (k.m) SHIP.social.moved = k.m; else delete SHIP.social.moved; } }
              for (const n of ['seasonOf', 'repView', 'keepsakes', 'movedOn', 'movedOff']) if (Object.prototype.hasOwnProperty.call(window, n)) delete window[n];
              // 0.35.24 (reviewer 2): rows with missing fields don't break the pages
              if (own.keep) (SHIP.social.keepsakes = SHIP.social.keepsakes || []).push({ from: 'tomas' }); else window.keepsakes = () => [{ from: 'tomas' }, null];
              if (own.moved) (SHIP.social.moved = SHIP.social.moved || []).push({ id: 'pell' }); else window.movedOn = () => [{ id: 'pell' }, null];
              deviceShow('wallet'); out.keepBad = !document.getElementById('devBody').textContent.includes('failed to draw');
              deviceShow('roster'); out.movedBad = !document.getElementById('devBody').textContent.includes('failed to draw');
              if (keepSoc) { const k = JSON.parse(keepSoc); if (own.keep) { if (k.k) SHIP.social.keepsakes = k.k; else delete SHIP.social.keepsakes; } if (own.moved) { if (k.m) SHIP.social.moved = k.m; else delete SHIP.social.moved; } }
              for (const n of ['keepsakes', 'movedOn']) if (Object.prototype.hasOwnProperty.call(window, n)) delete window[n];
              deviceShow('home'); out.own = own; return out; })()""")
            print('  pillar 4 pages:', p4)
            check(all(p4.get(k) for k in ['home', 'cal', 'rep', 'keep', 'left', 'keepBad', 'movedBad']), f'season on Home and Calendar, reputation, keepsakes, Left the Wren: {p4}')
            g.ev("deviceClose(); window.__opens = 0"); g.step(1)
            # never opens by itself (0.35.15, the user: "sometimes it just pops up"): a whole ship day of reminders, tips,
            # notices, an address, the meeting panel and an invitation, and a drag up from the bottom edge (the old swipe)
            g.ev("deviceClose()"); g.step(2)
            g.ev("""(() => { window.__opens = 0; deviceOn('open', () => { window.__opens++; });
              const D = SHIP.device, save = { day: SHIP.time.day, min: SHIP.time.min }, t0 = shipNow(); D.tipsSeen = {}; D.calendarRemind.on = true;
              D.appts.push({ id: 900, with: ['calder'], at: t0 + 600, len: 30, where: (apptPlaces()[0] || {}).id || 'x', kind: 'social', status: 'asked', by: 'calder' });
              D.appts.push({ id: 901, with: ['calder'], at: t0 + 300, len: 30, where: (apptPlaces()[0] || {}).id || 'x', kind: 'social', status: 'yes', by: null });
              for (let m = t0; m < t0 + 1440; m += 5) { SHIP.time.day = Math.floor(m / 1440) + 1; SHIP.time.min = m % 1440; devTickMin = -1; deviceTick(); device.refresh(); }
              tipShow('auto1', 'A tip.'); deviceNotify({ app: 'jobs', text: 'A job broke.', urgent: true }); deviceNotify({ app: 'mail', text: 'Mail.' });
              deviceAddress({ from: 'Captain', text: 'All hands.' }); deviceAddress(null);
              deviceDialogue({ title: 'Briefing', name: 'Chief', text: 'Gather round.', choices: null, i: 0, n: 1 }, () => {}); deviceDialogue(null);
              while (TIP_Q.length) tipDone(); D.appts = D.appts.filter(a => a.id < 900); D.tipsSeen = {};
              SHIP.time.day = save.day; SHIP.time.min = save.min; devTickMin = -1; DEV_REMINDED.clear(); for (const k in DEV.notes) delete DEV.notes[k]; })()""")
            g.page.mouse.move(w / 2, h - 10); g.page.mouse.down(); g.page.mouse.move(w / 2, h - 200, steps=8); g.page.mouse.up(); g.step(2)
            self_open = g.ev("[window.__opens, DEV.open, document.getElementById('device').hidden]")
            check(self_open == [0, False, True], f'the device never opens by itself (a day of reminders, tips, notices, an address, a dialogue, an invitation; a drag up from the bottom): {self_open}')
            g.page.click('#devBtn'); g.step(1)
            check(g.ev("[window.__opens, DEV.open]") == [1, True], 'the Device button still opens it')
            g.ev("deviceClose()"); g.step(1)
            # the phone review (0.35.12): a drag over the ship leaves it open, a tap closes it; a swipe down on the bezel
            # closes it, its grip is 44px tall; an unchanged screen isn't rebuilt
            if name == 'phone':
                g.ev("deviceShow('home')"); g.step(2)
                bz = g.ev("(() => { const r = document.getElementById('devBez').getBoundingClientRect(); return [r.left + r.width / 2, r.top, r.bottom]; })()")
                pt = [w / 2, max(140, bz[1] - 120)]
                same = g.ev("(() => { const f = document.getElementById('devBody').firstChild; deviceRefresh(); deviceRefresh(); return document.getElementById('devBody').firstChild === f; })()")
                g.page.mouse.move(*pt); g.page.mouse.down(); g.page.mouse.move(pt[0] + 60, pt[1] + 40, steps=5); g.page.mouse.up(); g.step(1)
                drag = g.ev("DEV.open")
                g.page.mouse.click(*pt); g.step(1)
                tapped = g.ev("!DEV.open")
                g.ev("deviceShow('home')"); g.step(2)
                grip = g.ev(f"(() => {{ const e = document.elementFromPoint({bz[0]}, {bz[1]} - 12); return !!(e && e.closest('#devBez')); }})()")
                g.page.mouse.move(bz[0], bz[1] + 8); g.page.mouse.down(); g.page.mouse.move(bz[0], bz[1] + 90, steps=5); g.page.mouse.up(); g.step(1)
                swiped = g.ev("!DEV.open")
                check([same, drag, tapped, grip, swiped] == [True] * 5, f'phone: no rebuild when unchanged, a drag leaves it open, a tap closes it, the grip reaches 44px, a swipe down closes it: {[same, drag, tapped, grip, swiped]}')
            errs = g.ev("DEV.errors")
            check(not errs, f'no app errors: {errs}')
            check(not g.errors, f'no page errors: {g.errors[:5]}')
            g.close()
    print('device_check:', 'OK' if ok else 'FAILED')
    return ok

if __name__ == '__main__':
    sys.exit(0 if run(sys.argv[1]) else 1)
