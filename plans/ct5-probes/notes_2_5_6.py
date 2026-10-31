# CT5 (0.99.5): probes for the user's controller notes 2 (seated talk), 5 (heads-up Go there), 6 (right stick turning).
# Run: CADET_CHROME=/opt/pw-browsers/chromium CADET_WORK=/tmp/cadet-work python3 plans/ct5-probes/notes_2_5_6.py GAME.html
# Prints ok/FAIL per claim and "PROBE OK" at the end; on 0.99.4 (8976965e) every note fails.
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
os.environ.setdefault('CADET_WORK', '/tmp/cadet-work')
os.environ.setdefault('CADET_CHROME', '/opt/pw-browsers/chromium')
import types
_CC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'controller_check.py')
C = types.SimpleNamespace()
_t = open(_CC).read().split("print(f'controller_check on")[0]
_g = {'__file__': _CC, '__name__': 'cc'}
exec(compile(_t, 'controller_check.py', 'exec'), _g)
C.__dict__.update(_g)
from playwright.sync_api import sync_playwright
src = _g['both_builds'](open(sys.argv[1]).read())[-1][1]
LIST = r"""(() => { const P = PAD_PICK, pp = player.obj.position; return { sitting: !!(ACT && ACT.kind), act: ACT ? [ACT.kind, ACT.placeId||null] : null, ride: !!ride, frozen: FREEZE.frozen, layer: !!padLayer(), face: +(player.face||0).toFixed(2),
  list: (P.list||[]).map(t => [t.key, padLabel(t.key), +t.d.toFixed(2), +t.score.toFixed(2)]), sel: P.sel && P.sel.key,
  near: DECK_CREW.filter(a => a.x !== undefined && Math.hypot(a.x - pp.x, a.z - pp.z) < 1.6).map(a => [a.p.name, +Math.hypot(a.x - pp.x, a.z - pp.z).toFixed(2), a.settled ? (a.spot && a.spot.pose) : a.pose]),
  raw: padRaw().slice(0, 30).map(t => [t.key, +t.d.toFixed(2), +t.score.toFixed(2)]) }; })()"""


fails = []
def ok(c, m):
    print(('  ok   ' if c else '  FAIL ') + m)
    if not c: fails.append(m)
with sync_playwright() as pw:
    # note 6: right stick right, both turn modes
    r = C.Run(pw, src, 'p4turn', mode='pad', plug={}, w=390, h=844)
    r.ev("SHIP.device && SHIP.device.settings && (SHIP.device.settings.tips = false)"); r.step(10); C.in_use(r)
    for mode in ('flick', 'hold'):
        r.ev(f"PAD_SET.turn = '{mode}'")
        a0 = r.ev("azT"); r.pad(4, a={2: 1}); a1 = r.ev("azT")
        r.pad(40, a={2: 1}); a2 = r.ev("azT")
        r.pad(4, a={2: -1}); a3 = r.ev("azT")
        print(f'  {mode}: right push {a1 - a0:+.3f}, held 40 frames {a2 - a1:+.3f}, left push {a3 - a2:+.3f}')
        ok(abs((a1 - a0) + 3.14159/2) < 1e-3, f'{mode}: right stick right is a quarter turn the new way (azT -pi/2)')
        ok(abs((a3 - a2) - 3.14159/2) < 1e-3, f'{mode}: right stick left is a quarter turn back (+pi/2)')
        if mode == 'hold': ok(a2 - a1 < -1, 'hold: held right keeps turning the new way')
        else: ok(abs(abs(a2 - a1) - 3.14159/2) < 1e-3, 'flick: a second push is one quarter turn more, same way')
    lb0 = r.ev("azT"); r.press('LB'); ok(abs(r.ev("azT") - lb0 + 3.14159/2) < 1e-3, 'LB still turns left (-pi/2), unchanged')
    print('  errors', r.errors[:3]); r.close()
    # note 5: the heads-up's Go there
    r = C.Run(pw, src, 'p4go', mode='pad', plug={}, w=390, h=844, quiet=C.QUIET.replace('#devHu{display:none!important} ', ''))
    r.ev("SHIP.device && SHIP.device.settings && (SHIP.device.settings.tips = false)"); r.step(10); C.in_use(r)
    r.ev("toastEl.classList.remove('show')")
    r.ev("(() => { window.__go = []; const f = devHeadsDo; devHeadsDo = v => { window.__go.push(v); return f(v); }; const h = { key: 'probe', stage: 'soon', at: shipNow(), title: 'Probe', where: 'Mess hall', goal: devPlaceGoal('3-mess-1') }; HU_Q.unshift(h); DEV.hu = h; DEVICE_SKIN.heads({ text: 'Probe starts in 10 minutes', where: 'Mess hall', go: true }); })()")
    r.step(15)
    mk = r.ev("(() => { const g = document.querySelector('#devHu button.act'); const m = g && g.querySelector(':scope > .padk'); return m ? [m.dataset.k, getComputedStyle(m).display, m.getBoundingClientRect().width > 0] : null; })()")
    print('  mark on Go there:', mk); ok(bool(mk) and mk[0] == 'down' and mk[1] != 'none' and mk[2], 'Go there carries a visible D-pad down mark while the pad is in use')
    r.shot('p4_go_mark')
    r.press('DOWN'); r.step(5)
    print('  devHeadsDo calls', r.ev("window.__go"), 'goal', r.ev("typeof GOAL !== 'undefined' ? JSON.stringify(GOAL) : (typeof IX_GOAL !== 'undefined' ? JSON.stringify(IX_GOAL) : null)"))
    ok(r.ev("window.__go").count('go') == 1, 'D-pad down pressed Go there once')
    ok(r.ev("document.getElementById('devHu').hidden"), 'the strip went away')
    # no strip: D-pad down does nothing on the deck
    log0 = r.ev("window.__go.length"); r.press('DOWN'); r.step(3); ok(r.ev("window.__go.length") == log0 and not r.ev("!!padLayer()"), 'D-pad down with no strip: nothing')
    # touch takes over: the mark hides
    r.ev("document.body.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))"); r.step(3)
    print('  errors', r.errors[:3]); r.close()
    # note 2: seated beside someone
    r, t = C.crowded_setup(pw, src, 'p4seat')
    seat = t['name'].split(' ')[0]; sp = (t['x'], t['z'])
    r.ev(f"actStart('sit', '{seat}')"); r.step(400)
    r.ev("toastEl.classList.remove('show'); typeof TOAST_AT !== 'undefined' && (TOAST_AT = -1e9)"); r.step(12)
    info = r.ev("(() => { const A = ACT; return { act: A && [A.kind, A.phase, A.pose], seat: A && [A.x, A.z], player: [player.obj.position.x, player.obj.position.z], list: PAD_PICK.list.map(t => [t.key, +Math.hypot(t.x - A.x, t.z - A.z).toFixed(2)]), near: DECK_CREW.filter(a => a.x !== undefined && Math.hypot(a.x - A.x, a.z - A.z) <= 1.6).map(a => ['crew:' + a.p.id, +Math.hypot(a.x - A.x, a.z - A.z).toFixed(2)]) }; })()")
    print('  seated', info)
    near = sorted(info['near'], key=lambda x: x[1])
    lst = [k for k, d in info['list']]
    ok(bool(near), 'someone sits within 1.6 m of the seat')
    if near:
        ok(sorted(lst[:len(near)]) == sorted(k for k, d in near) and near[0][0] == lst[0], f'the people beside you come first, nearest first ({lst[:4]})')
        h = r.ev(C.HINT); r.press('A'); r.step(60); o = r.ev(C.OUTCOME)
        print('  A on', h, '->', o['chat'][:60] if o['chat'] else None, 'act', r.ev("ACT ? [ACT.kind, ACT.phase] : null"))
        nm = r.ev(f"(DECK_CREW.find(a => 'crew:' + a.p.id === '{near[0][0]}') || {{p:{{}}}}).p.name")
        ok(bool(o['chat']) and nm in o['chat'], f'A talks to {nm}')
        ok(r.ev("ACT && ACT.kind === 'sit'"), 'still seated')
    r.shot('p4_seated'); print('  errors', r.errors[:3]); r.close()
print('PROBE', 'OK' if not fails else 'FAILED ' + str(fails))
sys.exit(1 if fails else 0)
