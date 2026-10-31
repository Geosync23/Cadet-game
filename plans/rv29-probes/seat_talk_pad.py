# CT5 (0.99.5): probes for the user's controller notes 2 (seated talk), 5 (heads-up Go there), 6 (right stick turning).
# Run: CADET_CHROME=/opt/pw-browsers/chromium CADET_WORK=/tmp/cadet-work python3 plans/ct5-probes/notes_2_5_6.py GAME.html
# Prints ok/FAIL per claim and "PROBE OK" at the end; on 0.99.4 (8976965e) every note fails.
import sys, os, json
sys.path.insert(0, sys.argv[2])
os.environ.setdefault('CADET_WORK', '/tmp/cadet-work')
os.environ.setdefault('CADET_CHROME', '/opt/pw-browsers/chromium')
import types
_CC = sys.argv[2] + '/controller_check.py'
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


# RV29 (CT5 note 2): seated in the mess hall with a controller: D-pad right through the ring, then A on the 2nd and 3rd person.
# usage: seat_talk_pad.py GAME.html WORKTREE   (harness: CT5's notes_2_5_6.py / controller_check)
SEL = "(() => ({ sel: PAD_PICK.sel && PAD_PICK.sel.key, hint: (document.getElementById('padHint') || {}).textContent, act: ACT && [ACT.kind, ACT.phase] }))()"
with sync_playwright() as pw:
    for pick in (1, 2):
        r, t = C.crowded_setup(pw, src, 'rv29seat' + str(pick))
        seat = t['name'].split(' ')[0]
        r.ev(f"actStart('sit', '{seat}')"); r.step(400)
        r.ev("toastEl.classList.remove('show'); typeof TOAST_AT !== 'undefined' && (TOAST_AT = -1e9)"); r.step(12)
        ring = [r.ev(SEL)]
        for k in range(5): r.press('RIGHT'); r.step(4); ring.append(r.ev(SEL))
        print('ring', [(x['sel'], (x['hint'] or '')[:30]) for x in ring])
        people = []
        for x in ring:
            if x['sel'] and x['sel'].startswith('crew:') and x['sel'] not in people: people.append(x['sel'])
        print('people in the ring, in order', people)
        if len(people) > pick:
            want = people[pick]
            for k in range(8):
                if r.ev(SEL)['sel'] == want: break
                r.press('RIGHT'); r.step(4)
            h = r.ev(SEL); r.press('A'); r.step(60)
            chat = r.ev("(() => { const c = document.getElementById('chat'); return c && !c.hidden ? c.innerText.replace(/\\s+/g, ' ').slice(0, 80) : null; })()")
            nm = r.ev(f"(DECK_CREW.find(a => 'crew:' + a.p.id === '{want}') || {{p:{{}}}}).p.name")
            print(f'A on person {pick + 1}: {want} ({nm}) hint {h["hint"]!r} -> chat {chat!r}; still seated {r.ev("ACT && ACT.kind === \'sit\'")}')
            print('  ', 'OK' if chat and nm and nm.split(' ')[0] in chat else 'FAIL')
        else: print('  fewer than', pick + 1, 'people in the ring')
        print('  errors', r.errors[:3]); r.close()
