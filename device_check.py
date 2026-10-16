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
#   Quiet off shift and the #seek chip's look (0.35.11)
#   Calendar days and group meetings (0.35.10): See the day, Make an appointment that day, pick the place on Maps,
#   two or more people (a seat each, kept and cancelled together)
#   people on Maps (0.35.9): who you may find (crewContacts), dots, { app: 'maps', who }, Go there
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
            # people on Maps (0.35.9): section 20's crewContacts (a stand-in when this build has none); { app: 'maps', who }
            # opens Maps on their deck with them picked; a dot per person; Go there points at their room
            pm = g.ev("""(() => { const own = typeof crewContacts === 'function', mess = Object.values(DECKS[3].rooms).find(r => /mess/i.test(r.name || '')).name;
              if (!own) window.crewContacts = () => [{ id: 'tst-a', name: 'Tess Able', role: 'Cook', tier: 1, tierName: 'acquaintance', where: { deck: 3, room: mess, act: 'dinner' } },
                { id: 'tst-b', name: 'Ben Cole', role: 'Medic', tier: 0, tierName: 'stranger', where: { deck: 3, room: mess, act: 'work' } }, { id: 'tst-c', name: 'Cy Dunn', role: 'Pilot', tier: 0, tierName: 'stranger', where: null }];
              const ps = mapPeople(), q = ps[0]; if (!q) { if (!own) delete window.crewContacts; return [own, 0]; }
              deviceDo({ app: 'maps', who: q.id }); const out = [own, ps.length, DEV.app, mapDeck === q.deck, mapWho === q.id];
              const dots = [...document.querySelectorAll('#devBody .devmap circle[data-who]')]; out.push(dots.length >= ps.filter(x => x.deck === q.deck).length, !!dots.find(d => d.dataset.who === q.id && d.classList.contains('pick')));
              out.push(document.getElementById('devBody').textContent.includes(q.label));
              const go = [...document.querySelectorAll('#devBody .btns .act')].find(b => b.textContent === 'Go there'); go && go.click();
              out.push(!!(IX_GOAL && IX_GOAL.deck === q.deck && IX_GOAL.room === q.room && IX_GOAL.label.includes(q.label)));
              clearGoal(); deviceDo({ app: 'maps', do: 'deck', arg: deckDef.num }); if (!own) delete window.crewContacts; deviceShow('home'); return out; })()""")
            print('  people on maps:', pm)
            check(pm[1] == 0 if pm[0] and len(pm) == 2 else pm[1:] == [pm[1], 'maps', True, True, True, True, True, True] and (pm[0] or pm[1] == 2), f'people on Maps: dots, pick, Go there: {pm}')
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
            errs = g.ev("DEV.errors")
            check(not errs, f'no app errors: {errs}')
            check(not g.errors, f'no page errors: {g.errors[:5]}')
            g.close()
    print('device_check:', 'OK' if ok else 'FAILED')
    return ok

if __name__ == '__main__':
    sys.exit(0 if run(sys.argv[1]) else 1)
