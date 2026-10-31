# RV29: TB4's 0.92.6 traditions in the real game at a reader's pace (complements TB4's t926_probe.py, which clicks through).
# Per tradition, on its day (switched-on copy): (A) stand in its room from -6; at +6 tap the leader, read each card ~3 s
# (CARD_S), pick answer 2; record the ship minutes the card took, the activity after, and frames to +16. (B) a fresh game,
# a tap at end-LATE (default 4) minutes, read at pace: what happens when the card ends after the tradition. (C) a fresh game,
# a tap at +6, save on the second card and reload: the card, the marker, joined, a second tap.
# usage: t926_pace.py WORKTREE BUILD_ON.html [id ...]   (env CARD_S, LATE, PARTS=ABC)
import sys, os, json, pathlib
WT, BUILD = sys.argv[1], sys.argv[2]; IDS = sys.argv[3:]
src = open(WT + '/plans/tb4-probes/t926_probe.py').read()
head = src.split('def run_one(')[0].replace("sys.argv, ARGS = sys.argv[:1], sys.argv[1:]", "ARGS = [BUILD] + IDS").replace("/home/user/cadet-game/cadet_test.py", WT + '/cadet_test.py')
exec(head)
CARD_S, LATE, PARTS = float(os.environ.get('CARD_S', '3')), int(os.environ.get('LATE', '4')), os.environ.get('PARTS', 'ABC')
V = "(() => { const v = DIALOGUE && dialogueView(); return v ? { who: v.who, text: v.text || '', choices: v.choices ? v.choices.map(c => c.text || c) : null } : null; })()"
def setup(pw, i):
    g = Game(pw, build, 390, 844)
    g.ev("if (typeof GUIDE_ON !== 'undefined' && GUIDE_ON) { GUIDE.tq.length = 0; }")
    f = json.loads(g.ev(FIND % (DAYS.get(i, 1), i)))
    rk = [r.split('|')[1] for r in f['rooms'] if int(r.split('|')[0]) == f['deck']][0]
    return g, f, rk
def go_to(g, f, rk, at):
    g.ev(f"(() => {{ skipTo({at}); goToDeck({f['deck']}, null); }})()"); g.step(5); g.ev(SPY); g.ev(IN % rk)
def wait_leader(g, i, d, until):
    for k in range(4000):
        g.step(10); x = json.loads(g.ev(LOOK % (i, d)))
        if x['m'] >= until and x['tj'] and not x['tj'].startswith('other'): return x
        if x['m'] > until + 30: return x
def read_card(g, label, pick=1, stop_at=None):
    lines, n = [], 0; t0 = g.ev("SHIP.time.min")
    while n < 30:
        v = g.ev(V)
        if not v: break
        lines.append([v['who'], v['text'][:110], v['choices']]); n += 1
        if stop_at is not None and n == stop_at: return lines, t0, True
        g.step(int(CARD_S * 30))
        if v['choices']: g.ev(f"dialogueChoose({pick})")
        else: g.ev("dialogueNext()")
        g.step(3)
    return lines, t0, False
def tap(g):
    return g.ev("(() => tradJoinTap(TJ_NOW.agent))()")
def part_a(pw, i):
    g, f, rk = setup(pw, i); d, fr, to = f['d'], f['from'], f['to']
    print(f'== {i} A: day {d} {fr // 60:02d}:{fr % 60:02d}-{to // 60:02d}:{to % 60:02d}')
    go_to(g, f, rk, (d - 1) * 1440 + fr - 6); x = wait_leader(g, i, d, (d - 1) * 1440 + fr + 6)
    print('   at', x['m'] % 1440 // 60, x['m'] % 60, 'leader', x['tj'], 'mark', x['mark'], 'goal', x['goal'])
    print('   tap', tap(g)); g.step(3)
    lines, t0, _ = read_card(g, 'A'); t1 = g.ev("SHIP.time.min")
    for l in lines: print('     card:', l)
    g.step(30); x = json.loads(g.ev(LOOK % (i, d)))
    print(f'   card took {t1 - t0:.1f} ship min; after: joined {x["joined"]} act {x["act"]} walk {x["walk"]} mark {x["mark"]}')
    if i == 'garden-walk':
        last = None
        for k in range(6000):
            g.step(10); x = json.loads(g.ev(LOOK % (i, d)))
            w = x['walk'] and x['walk'][1]
            if w != last: print('     walk', x['m'] % 1440 // 60, x['m'] % 60, x['walk'], 'here', x['here']); last = w
            if not x['walk'] or x['m'] > (d - 1) * 1440 + to + 20: break
        r = json.loads(g.ev("JSON.stringify({ toasts: window.__toasts })")); print('   toasts', [t for t in r['toasts'] if 'Garden' in t[1] or 'garden' in t[2]][-3:])
    else:
        while json.loads(g.ev(LOOK % (i, d)))['m'] < (d - 1) * 1440 + to + 6: g.step(30)
        x = json.loads(g.ev(LOOK % (i, d))); print(f'   after the end: act {x["act"]} mark {x["mark"]} goal {x["goal"]}')
    print('   errors', g.errors[:3]); g.close()
def part_b(pw, i):
    g, f, rk = setup(pw, i); d, fr, to = f['d'], f['from'], f['to']
    go_to(g, f, rk, (d - 1) * 1440 + to - LATE - 3); x = wait_leader(g, i, d, (d - 1) * 1440 + to - LATE)
    print(f'== {i} B: late tap at', x['m'] % 1440 // 60, x['m'] % 60, '(ends', to // 60, to % 60, ') leader', x['tj'], 'mark', x['mark'])
    if not x['tj'] or x['tj'].startswith('other'): print('   no leader to tap'); g.close(); return
    print('   tap', tap(g)); g.step(3); lines, t0, _ = read_card(g, 'B'); print('   card lines', len(lines), 'ended at', int(g.ev("SHIP.time.min")) % 1440)
    for s in (3, 60, 300):
        g.step(s); x = json.loads(g.ev(LOOK % (i, d))); print(f'   +{s} frames: {x["m"] % 1440 // 60}:{x["m"] % 60:02d} joined {x["joined"]} act {x["act"]} walk {x["walk"]} mark {x["mark"]} goal {x["goal"]}')
    print('   errors', g.errors[:3]); g.close()
def part_c(pw, i):
    g, f, rk = setup(pw, i); d, fr, to = f['d'], f['from'], f['to']
    go_to(g, f, rk, (d - 1) * 1440 + fr - 6); x = wait_leader(g, i, d, (d - 1) * 1440 + fr + 6)
    print(f'== {i} C: tap', tap(g)); g.step(3); lines, t0, stopped = read_card(g, 'C', stop_at=2)
    s = g.ev(SAVEJS); x = json.loads(g.ev(LOOK % (i, d))); print('   saved on card 2: joined', x['joined'], 'dlg', x['dlg'])
    key = g.ev("SAVE_KEY"); url = g.page.url.split('?')[0]
    g.page.add_init_script("try { if (!sessionStorage.getItem('rv29') ) { localStorage.clear(); localStorage.setItem(" + json.dumps(key) + ", " + json.dumps(s) + "); sessionStorage.setItem('rv29', '1'); } } catch (e) {}")
    g.page.goto(url + '?debug', timeout=120000); g.page.wait_for_function('window.__sc !== undefined', timeout=120000)
    g.ev("if (typeof TITLE !== 'undefined' && TITLE.on) titleClose('go')"); g.step(20); g.ev("if (typeof TITLE !== 'undefined' && TITLE.on) { TITLE.on = false; document.getElementById('title').hidden = true; }"); g.step(20)
    x = json.loads(g.ev(LOOK % (i, d)))
    print(f'   reloaded: {x["m"] % 1440 // 60}:{x["m"] % 60:02d} joined {x["joined"]} dlg {x["dlg"]} act {x["act"]} mark {x["mark"]} leader {x["tj"]} goal {x["goal"]}')
    if x['tj'] and not x['tj'].startswith('other'):
        print('   tap again', tap(g)); g.step(3); lines2, _, _ = read_card(g, 'C2'); g.step(30); x = json.loads(g.ev(LOOK % (i, d)))
        print(f'   second tap: card lines {len(lines2)}; joined {x["joined"]} act {x["act"]} walk {x["walk"]}')
    print('   errors', g.errors[:3]); g.page.evaluate("() => localStorage.clear()"); g.close()
with sync_playwright() as pw:
    for i in (IDS or list(DAYS)):
        for p, fn in (('A', part_a), ('B', part_b), ('C', part_c)):
            if p in PARTS:
                try: fn(pw, i)
                except Exception as e: print(f'== {i} {p}: probe error {str(e)[:300]}')
