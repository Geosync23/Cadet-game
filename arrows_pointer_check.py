# Starship Cadet: the panel pointer check (the arrows plan, piece C, AC1; plans/arrows-briefs.md "Piece C").
# Checks section 19's panel pointer (pointAsk) in a copy of the build with POINT_ON switched on, at 360 x 640,
# 390 x 844, 844 x 390 and 1280 x 800:
#   the path: with the device shut it sits on the Device button, then the Works tile, then the Tools tab; open it and it's
#     gone, counted once in SHIP.device.pointsSeen, and never asked again (also after a reload of the device's save);
#     from another app it sits on Back
#   the job board: on a held job's Take it; gone once taken.  The time clock: on Clock in; gone once clocked in.
#   a choice card (deviceChoose): on the k-th choice; gone when picked.  A meeting (body.dlgon) hides a device pointer.
#   every time: the ring and the label inside the screen, the ring around the button, one pointer at a time
#   nothing added to the 3D scene (scene children, geometries, textures)
#   Settings: the Teaching arrows switch (Always / First times / Off): Off refuses, Always asks again; pointsSeen capped
# And in the build as it is (POINT_ON false): pointAsk refuses, no #ptr, no pointsSeen or teach saved, no Settings row.
# Screenshots: CADET_WORK/test/pointer-<size>-<target>.png. Fails on a build without the pointer.
# Setup and environment as for cadet_test.py.  Run:  python3 arrows_pointer_check.py BUILD.html
import sys, json, pathlib
exec(open(__file__.replace('arrows_pointer_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

ok = True
def check(cond, msg):
    global ok
    if not cond: ok = False; print('FAIL', msg)
    return cond

SIZES = [('360x640', 360, 640), ('390x844', 390, 844), ('844x390', 844, 390), ('1280x800', 1280, 800)]
# where the pointer is: its ring and label boxes, the target's box, and whether all sit on screen
WHERE = r"""(sel => {
  const g = document.getElementById('ptr'), t = typeof sel === 'string' ? document.querySelector(sel) : null;
  if (!g || g.hidden) return { up: false, now: pointNow() };
  const box = e => { if (!e || e.hidden) return null; const r = e.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; };
  const [ring, arr, lab] = g.children, W = innerWidth, H = innerHeight, rb = box(ring), lb = box(lab), aim = box(POINT.aim);
  const inside = b => !b || b[0] >= 0 && b[1] >= 0 && b[2] <= W && b[3] <= H;
  return { up: true, now: pointNow(), ring: rb, lab: lb, label: lab.textContent, aim, onScreen: inside(rb) && inside(lb),
    around: !!aim && rb[0] <= aim[0] && rb[1] <= Math.max(2, aim[1]) && rb[2] >= Math.min(W - 2, aim[2]) && rb[3] >= Math.min(H - 2, aim[3]),
    target: t ? POINT.aim === t || (POINT.aim && t.contains(POINT.aim)) : null, n: document.querySelectorAll('#ptr').length };
})"""

def arrows_off(src):                                 # the build with the teaching arrows switched off (as before 0.92.0), for the parts that test "off"
    return src.replace('const POINT_ON = true;', 'const POINT_ON = false;', 1).replace('var GUIDE_ON = true;', 'var GUIDE_ON = false;', 1)

def run(path):
    src = arrows_off(pathlib.Path(path).read_text())
    has = 'const POINT_ON = false;' in src
    check(has, 'the build has the panel pointer (const POINT_ON)')
    if not has: return
    off = WORK / 'test' / ('_pointer_off_' + pathlib.Path(path).name); off.write_text(src); path = str(off)
    on = WORK / 'test' / ('_pointer_on_' + pathlib.Path(path).name)
    on.write_text(src.replace('const POINT_ON = false;', 'const POINT_ON = true;', 1))
    with sync_playwright() as pw:
        # ---- off: the build as it is
        print('off (the build switched off):')
        g = Game(pw, path, 390, 844); g.step(3)
        r = g.ev("""(() => { const a = pointAsk({ id: 'x:off', path: [pointDevice()] }); deviceShow('settings'); const txt = document.getElementById('devBody').textContent; deviceClose();
          return { a, ptr: !!document.getElementById('ptr'), seen: 'pointsSeen' in SHIP.device, teach: 'teach' in SHIP.device.settings, row: /Teaching arrows/.test(txt),
            saved: JSON.stringify(deviceLoad({ device: JSON.parse(JSON.stringify(SHIP.device)) })) === JSON.stringify(SHIP.device) }; })()""")
        g.step(3)
        print('  ', r)
        check(r['a'] is False and not r['ptr'] and not r['seen'] and not r['teach'] and not r['row'], f'off: pointAsk refuses, nothing drawn or saved, no Settings row ({r})')
        check(r['saved'], 'off: the device save reads back the same')
        check(not g.errors, f'off: no page errors {g.errors[:3]}')
        g.close()
        for name, w, h in SIZES:
            print(f'{name}:')
            g = Game(pw, str(on), w, h); g.step(3)
            shot = lambda t: g.shot(str(WORK / 'test' / f'pointer-{name}-{t}.png'))
            MEM = "[scene.children.length, renderer.info.memory.geometries, renderer.info.memory.textures]"
            mem0 = g.ev(MEM)
            where = lambda sel=None: g.ev(f"({WHERE})({json.dumps(sel)})")
            # (a) the path: Device button, the Works tile, the Tools tab
            g.ev("""(() => { worksInit(WORKS_START); WORKS_TAB = 'training'; deviceClose(); return pointAsk({ id: 'x:works', once: 1,
              path: [...pointToApp('works', 'Works: your tools'), { open: () => DEV.app === 'works' && WORKS_TAB === 'tools', el: () => buttonFor({ app: 'works', do: 'tab', arg: 'tools' }), label: 'Tools' }],
              done: () => DEV.open && DEV.app === 'works' && WORKS_TAB === 'tools' }); })()""")
            g.step(2); p = where('#devBtn'); shot('device-button')
            check(p['up'] and p['target'] and p['around'] and p['onScreen'] and p['label'] == 'Open your device', f'device shut: on the Device button, on screen ({p})')
            mem1 = g.ev(MEM)
            check(mem1 == mem0, f'nothing added to the 3D scene ({mem0} -> {mem1})')
            g.page.click('#devBtn'); g.step(2)
            tip = g.ev("(() => { const c = document.getElementById('devTip'); return !!c && !c.hidden; })()"); p = where()
            if tip: check(not p['up'] or not g.ev(f"(() => {{ const q = document.getElementById('devTip').getBoundingClientRect(), r = POINT.aim.getBoundingClientRect(); return q.left < r.right && q.right > r.left && q.top < r.bottom && q.bottom > r.top; }})()"), f'a tip over the button hides the pointer ({p})')
            g.ev("while (TIP_Q.length) tipDone()"); g.step(2)   # the device's first tip goes (a tap or 9 seconds)
            p = where('#devBody button.app[data-app="works"]'); shot('works-tile')
            check(p['up'] and p['target'] and p['around'] and p['onScreen'], f'device open: on the Works tile ({p})')
            g.page.click('#devBody button.app[data-app="works"]'); g.step(2)
            tab = g.ev("(() => { const b = buttonFor({ app: 'works', do: 'tab', arg: 'tools' }); if (b) b.id = '__tab'; return !!b; })()")
            p = where('#__tab'); shot('works-tab')
            check(tab and p['up'] and p['target'] and p['around'] and p['onScreen'] and p['label'] == 'Tools', f'Works open: on the Tools tab ({p})')
            g.page.click('#__tab'); g.step(2); p = where()
            seen = g.ev("SHIP.device.pointsSeen")
            check(not p['up'] and p['now'] is None and seen == {'x:works': 1}, f'Tools opened: gone, counted once ({p}, {seen})')
            back = g.ev("""(() => { const D = deviceLoad({ device: JSON.parse(JSON.stringify(SHIP.device)) }); return { seen: D.pointsSeen, again: pointAsk({ id: 'x:works', path: [pointDevice()] }) }; })()""")
            check(back['seen'] == {'x:works': 1} and back['again'] is False, f'read back from the save, never asked again ({back})')
            # from another app: Back
            g.ev("deviceShow('mail'); pointAsk({ id: 'x:back', path: pointToApp('needs', 'Needs'), done: () => DEV.app === 'needs' })"); g.step(2)
            p = where('#devBack'); shot('back')
            check(p['up'] and p['target'] and p['label'] == 'Back to your apps' and p['onScreen'], f'in another app: on Back ({p})')
            g.page.click('#devBack'); g.step(2); p = where('#devBody button.app[data-app="needs"]')
            check(p['up'] and p['target'] and p['label'] == 'Needs', f'then on the Needs tile ({p})')
            g.page.click('#devBody button.app[data-app="needs"]'); g.step(2); p = where()
            check(not p['up'], f'Needs opened: gone ({p})')
            # a meeting hides a device pointer
            g.ev("deviceShow('home'); pointAsk({ id: 'x:meet', path: pointToApp('mail', 'Mail') }); deviceDialogue({ title: 'Test', name: 'Someone', text: 'Hello.' })"); g.step(2)
            p = where(); check(not p['up'] and p['now'] is None, f'a meeting on screen hides it ({p})')
            g.ev("deviceDialogue(null)"); g.step(2); p = where('#devBody button.app[data-app="mail"]')
            check(p['up'] and p['target'], f'and it comes back after ({p})')
            # covered (RV2): the pause card over the Device button, and a panel laid over a tile: no ring while covered
            g.ev("pointDrop('x:meet'); deviceClose(); pointAsk({ id: 'x:cover', path: pointToApp('mail', 'Mail') })"); g.step(2)
            check(where('#devBtn')['up'], 'covered: the pointer is up before the cover')
            g.ev("pauseSet(true)"); g.step(2); p = where(); shot('paused')
            check(not p['up'], f'covered: the pause card over the Device button should hide it ({p})')
            g.ev("pauseSet(false)"); g.step(2)
            check(where('#devBtn')['up'], 'covered: it should come back after the pause')
            g.page.click('#devBtn'); g.ev("while (TIP_Q.length) tipDone()"); g.step(2)
            g.ev("""(() => { const r = tileFor('mail').getBoundingClientRect(), c = document.createElement('div'); c.id = '__cover';
              Object.assign(c.style, { position: 'fixed', left: (r.left - 10) + 'px', top: (r.top - 10) + 'px', width: (r.width + 20) + 'px', height: (r.height + 20) + 'px', zIndex: 4, background: '#123' });
              document.body.appendChild(c); })()"""); g.step(2); p = where()
            check(not p['up'], f'covered: a panel over the tile should hide it ({p})')
            g.ev("document.getElementById('__cover').remove()"); g.step(2)
            check(where('#devBody button.app[data-app="mail"]')['up'], 'covered: back once the panel goes')
            g.ev("pointDrop('x:cover'); deviceClose()"); g.step(2)
            check(not where()['up'], 'pointDrop ends it')
            # (b) a choice card's k-th button
            g.ev("window.__pick = null; deviceChoose({ title: 'Test card', text: 'Which?', choices: ['First', 'Second', 'Third'] }, k => { __pick = k; }); pointAsk({ id: 'x:card', path: pointCard(1, 'This one', 'Test card'), once: 2 })")
            g.step(2); g.ev("document.querySelectorAll('#devDlg .btns button')[1].id = '__k'"); p = where('#__k'); shot('card')
            check(p['up'] and p['target'] and p['around'] and p['onScreen'], f'a card: on its second choice ({p})')
            g.page.click('#__k'); g.step(2); p = where()
            check(not p['up'] and g.ev("__pick") == 1 and g.ev("pointList().length") == 0, f'picked: the pick goes through, the pointer ends ({p})')
            # (c) the job board: a held job's Take it
            job = g.ev(r"""(() => { const t = shipNow(); const m = machineList().find(m => !m.stub && jobTier({ machine: m.id }) <= PLAYER_TIER && !ENGINE_KINDS.has(m.kind) && PLACE_OF && panelPlace(m.id));
              if (!m) return null; const part = MACHINE_KINDS[m.kind].part || 'gasket'; SHIP.stores[part] = Math.max(SHIP.stores[part] || 0, 2);
              if (myJob()) dropJob(myJob().id);
              SHIP.jobs.push({ id: 'ptrtest@1', machine: m.id, deck: m.deck, kind: 'repair', urgency: 2, posted: t, found: t, claimedBy: null, parts: [part], status: 'open' }); MACH_REV++;
              return m.id; })()""")
            check(job, f'a test job posted ({job})')
            g.ev("while (TIP_Q.length) tipDone(); deviceClose()")   # a tip on the same spot hides the pointer (and covers the button)
            g.ev("pointAsk({ id: 'x:board', path: pointBoard('ptrtest@1', 'Take this one'), done: () => (myJob() || {}).id === 'ptrtest@1', once: 3 })"); g.step(2)
            check(not where()['up'], 'the board shut: no pointer (the world arrow leads there)')
            g.ev("ixBoard.open()"); g.step(2)
            g.ev("(() => { const b = boardButton('ptrtest@1'); if (b) b.id = '__take'; })()"); p = where('#__take'); shot('board')
            check(p['up'] and p['target'] and p['around'] and p['onScreen'] and g.ev("(document.getElementById('__take') || {}).textContent") == 'Take it', f'the board: on the job\'s Take it ({p})')
            g.page.click('#__take'); g.step(2); p = where()
            check(not p['up'] and g.ev("(myJob() || {}).id") == 'ptrtest@1', f'taken: gone ({p})')
            g.ev("if (myJob()) dropJob(myJob().id); SHIP.jobs = SHIP.jobs.filter(j => j.id !== 'ptrtest@1'); clearGoal()")
            # (d) the time clock: Clock in
            ck = g.ev("""(() => { let d = SHIP.time.day; while (!playerShiftOn(d) || careerClockedIn(d)) d++;
              const t = (d - 1) * 1440 + 8 * 60 + 30; if (t > shipNow()) skipTo(t); clockScreen();
              pointAsk({ id: 'x:clock', path: pointClock('in', 'Clock in here'), done: () => careerClockedIn(SHIP.time.day) });
              return { d: SHIP.time.day, min: SHIP.time.min, btn: !!clockButton('in') }; })()""")
            g.step(2); g.ev("(() => { const b = clockButton('in'); if (b) b.id = '__in'; })()"); p = where('#__in'); shot('clock')
            check(ck['btn'] and p['up'] and p['target'] and p['around'] and p['onScreen'], f'the clock: on Clock in ({ck}, {p})')
            if ck['btn']:
                g.step(30); g.page.click('#__in'); g.step(3); p = where()   # (AS1) past 0.95.0's 500 ms tap guard on the clock screen (CLOCK_UNDO_ON, patch #6)
                check(not p['up'] and g.ev("careerClockedIn(SHIP.time.day)"), f'clocked in: gone ({p})')
            g.ev("document.getElementById('clockScreen').hidden = true; pointDrop('x:clock')")
            # (d2) the lift's deck picker: one marker for the arrow's deck, the row's own "→ Tracked", with Teaching arrows on
            # First times, Always or Off; no teaching pointer on it (the user, 2026-10-23: two were shown)
            lf = []
            for mode in ('first', 'all', 'off'):
                n = g.ev(f"(() => {{ deviceDo({{ app: 'settings', do: 'teach', arg: '{mode}' }}); deviceClose(); const n = deckDef.num === 5 ? 3 : 5; setGoal({{ deck: n, room: 'w', label: 'Somewhere' }}); openLiftPanel(); const b = liftButton(n); if (b) b.id = '__lift'; return n; }})()")
                g.step(2); p = where('#__lift')
                rows = g.ev("[...document.querySelectorAll('#liftList .goal')].map(b => b.id === '__lift')")
                lf.append([mode, rows, bool(p['up'] and p['target'])])
                if mode == 'first': shot('lift')
                g.ev("closeLiftPanel(); clearGoal()"); g.step(2)
            g.ev("deviceDo({ app: 'settings', do: 'teach', arg: 'first' }); deviceClose()")
            check(all(r == [True] and not up for _, r, up in lf), f'the lift: one marker on the arrow\'s deck (the row\'s → Tracked), no pointer, in each teaching mode ({lf})')
            # (e) one at a time; the Teaching arrows switch; the cap
            r = g.ev("""(() => { deviceClose(); pointAsk({ id: 'x:one', path: [pointDevice()] }); pointAsk({ id: 'x:two', path: [pointDevice()] }); return 0; })()""")
            g.step(2); p = where()
            check(p['up'] and p['now'] == 'x:one' and p['n'] == 1, f'two asked: the first shows, one pointer ({p})')
            g.ev("pointDrop('x:one')"); g.step(2); p = where()
            check(p['now'] == 'x:two', f'then the next ({p})')
            r = g.ev("""(() => { pointDrop('x:two'); const S = SHIP.device.settings; deviceShow('settings'); const row = /Teaching arrows/.test(document.getElementById('devBody').textContent);
              deviceDo({ app: 'settings', do: 'teach', arg: 'off' }); const off = pointAsk({ id: 'x:t', path: [pointDevice()] });
              deviceDo({ app: 'settings', do: 'teach', arg: 'all' }); const all = pointAsk({ id: 'x:works', path: [pointDevice()] }); pointDrop('x:works');
              deviceDo({ app: 'settings', do: 'teach', arg: 'first' }); const mode = teachMode(), saved = deviceLoad({ device: JSON.parse(JSON.stringify(SHIP.device)) }).settings.teach;
              for (let i = 0; i < 250; i++) pointCount('cap' + i); const n = Object.keys(SHIP.device.pointsSeen).length, first = 'cap0' in SHIP.device.pointsSeen;
              deviceClose(); return { row, off, all, mode, saved, n, first }; })()""")
            check(r['row'] and r['off'] is False and r['all'] is True and r['mode'] == 'first' and r['saved'] == 'first', f'Settings: Teaching arrows Off refuses, Always asks again, saved ({r})')
            check(r['n'] == 200 and not r['first'], f'pointsSeen capped at 200, oldest dropped ({r["n"]})')
            # nothing in the 3D scene: the same frame drawn with the pointer up and without (the device shut, no time passing)
            g.ev("pointAsk({ id: 'x:calls', path: [pointDevice()] })"); g.step(1)
            calls = g.ev("(() => { const up = !document.getElementById('ptr').hidden; renderer.info.reset ? renderer.info.reset() : 0; renderer.render(scene, camera); const a = renderer.info.render.calls; pointDrop('x:calls'); pointFrame(); renderer.render(scene, camera); return [up, a, renderer.info.render.calls, document.getElementById('ptr').hidden]; })()")
            check(calls[0] and calls[3] and calls[1] == calls[2], f'the same draw calls with the pointer up as without ({calls})')
            errs = g.ev("DEV.errors.filter(e => /pointer/.test(e))")
            check(not errs, f'no pointer errors {errs[:3]}')
            pe = [e for e in g.errors if 'pageerror' in e]
            check(not pe, f'no page errors {pe[:3]}')
            g.close()

run(sys.argv[1] if len(sys.argv) > 1 else 'starship-cadet.html')
print('arrows_pointer_check: OK' if ok else 'arrows_pointer_check: FAILED')
sys.exit(0 if ok else 1)
