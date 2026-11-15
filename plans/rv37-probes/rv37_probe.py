# RV37's probes for FR1's review fixes (05adee4): the cases robust_check.py does not cover.
# It prints what happens; it judges nothing by itself (the notes, plans/review-rv37.md, do).
# Run from the repository's folder, like robust_check:  python3 plans/rv37-probes/rv37_probe.py starship-cadet.html [part ...]
# Parts: loop keep tell tab memo walls load lib. Screenshots land in plans/rv37-probes/.
import sys, os, re, json, pathlib, time, hashlib
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parent.parent
src = (ROOT / 'robust_check.py').read_text().split('def part_loop')[0].replace("os.path.dirname(os.path.abspath(__file__))", repr(str(ROOT)))
src = src.replace("self.b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=1)", "self.b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1).new_page()")   # a context of its own, so a second tab can share its storage
exec(src)
ALL = ['LOOP_GUARD_ON', 'SAVE_KEEP_ON', 'SAVE_TELL_ON', 'SLEEP_SAFE_ON', 'LOAD_SAFE_ON', 'EVON_MEMO_ON', 'WALLS_STILL_ON', 'SAVE_TAB_ON']
REFUSE = "window.__refuse = false; (() => { const s = Storage.prototype.setItem; Storage.prototype.setItem = function (k, v) { if (window.__refuse && this === localStorage) { const e = new Error('rv37: storage refuses'); e.name = 'QuotaExceededError'; throw e; } return s.call(this, k, v); }; })();"
def say(*a): print(*a, flush=True)
def shot(t, name): t.page.evaluate('window.__skip = false; window.__step(1, 33.3)'); t.page.screenshot(path=str(HERE / name))
def top_at_card(t): return t.page.evaluate("(() => { const c = document.getElementById('loopCard'); if (!c) return 'no card'; const r = c.getBoundingClientRect(), e = document.elementFromPoint(r.left + r.width / 2, r.top + 20); return (c.contains(e) ? 'card on top' : 'covered by ' + (e && (e.id || e.className))) + ' ' + Math.round(r.width) + 'x' + Math.round(r.height); })()")

def part_loop(pw):
    p = build('rv_loop', on=ALL)
    # 1. an error on every other frame, 600 frames
    t = Tab(pw, p, '?nosave&debug'); logs = []; t.page.on('console', lambda m: logs.append(m.text[:60]) if m.type == 'error' else None)
    t.step(30); m0 = t.ev('shipNow()')
    t.ev("(() => { const u = crowd.update.bind(crowd); let n = 0; crowd.update = (a, b) => { if (n++ % 2 === 0) throw new Error('rv37: every other frame'); return u(a, b); }; })()")
    t.step(600); say(f"loop 1, every other frame bad, 600 frames: card {t.page.evaluate('!!document.getElementById(\"loopCard\")')}, bad frames counted {t.ev('typeof LOOP_SUM !== "undefined" ? LOOP_SUM : LOOP_BAD')}, ship minutes passed {t.ev('shipNow()') - m0:.1f}, errors logged {len(logs)}")
    t.close()
    # 2. 19 bad frames then one good, over and over
    t = Tab(pw, p, '?nosave&debug'); logs = []; t.page.on('console', lambda m: logs.append(m.text[:60]) if m.type == 'error' else None)
    t.step(30); m0 = t.ev('shipNow()')
    t.ev("(() => { const u = crowd.update.bind(crowd); let n = 0; crowd.update = (a, b) => { if (n++ % 20 !== 19) throw new Error('rv37: 19 of 20'); return u(a, b); }; })()")
    t.step(600); say(f"loop 2, 19 of every 20 frames bad, 600 frames: card {t.page.evaluate('!!document.getElementById(\"loopCard\")')}, ship minutes passed {t.ev('shipNow()') - m0:.1f} (a healthy 600 frames: about {600 / 30 * t.ev('SHIP_RATE'):.1f}), errors logged {len(logs)}")
    t.close()
    # 2b. one bad frame in five; one in eight
    for every in (5, 8):
        t = Tab(pw, p, '?nosave&debug'); t.step(30)
        t.ev("(() => { const u = crowd.update.bind(crowd); let n = 0; crowd.update = (a, b) => { if (n++ % EVERY === 0) throw new Error('rv37: one in EVERY'); return u(a, b); }; })()".replace('EVERY', str(every)))
        t.step(600); say(f"loop 2b, one bad frame in {every}, 600 frames: card {t.page.evaluate('!!document.getElementById(\"loopCard\")')}"); t.close()
    # 3. the card under ?nosave (nothing is ever saved there), its look, what is under it
    t = Tab(pw, p, '?nosave&debug'); t.step(30); t.ev("crowd.update = () => { throw new Error('rv37: all bad'); }"); t.step(25)
    say('loop 3, ?nosave, every frame bad: card text:', t.page.evaluate("document.getElementById('loopCard').textContent"), '|', top_at_card(t), '| focus on', t.page.evaluate("document.activeElement && (document.activeElement.id || document.activeElement.tagName)"))
    t.page.screenshot(path=str(HERE / 'loop-card.png')); t.close()
    # 4. with saving refused (SAVE_TELL on): the card still says saved
    t = Tab(pw, p, before=REFUSE, plant=ARRIVED); t.step(30); t.ev("if (typeof introOn === 'function' && introOn()) introSkip()"); t.step(10); t.page.evaluate('window.__refuse = true'); t.ev('skipTo(shipNow() + 125)'); t.step(5)
    t.ev("crowd.update = () => { throw new Error('rv37: all bad'); }"); t.step(25)
    say('loop 4, storage refusing then every frame bad: SAVE_ST.fail', t.ev('SAVE_ST.fail'), '| card:', t.page.evaluate("document.getElementById('loopCard').textContent"), '| stored save:', (lambda s: 'none' if s is None else 'Day %s %s' % (json.loads(s)['time']['day'], json.loads(s)['time']['min']))(t.store(t.ev('SAVE_KEY'))), '| game now Day', t.ev('SHIP.time.day'), round(t.ev('SHIP.time.min')))
    t.close()
    # 5. during the night skip's fade
    t = Tab(pw, p, '?nosave&debug'); t.step(30); t.ev('skipTo(1440 + 21.5 * 60)'); t.step(10); t.ev('sleepGo(360)'); t.ev("crowd.update = () => { throw new Error('rv37: all bad'); }"); t.step(25)
    say('loop 5, card while the night fade is up: fade', t.ev('fadeEl.style.opacity'), '|', top_at_card(t)); t.page.wait_for_timeout(2600); t.step(3)
    say('   after the night: fade', t.ev('fadeEl.style.opacity'), 'sleeping', t.ev('sleeping'), '|', top_at_card(t)); t.page.screenshot(path=str(HERE / 'loop-card-night.png')); t.close()
    # 6. with the title up
    t = Tab(pw, p, '?title', plant=None); t.step(5)
    say('loop 6, title up:', t.page.evaluate("(() => { const x = document.getElementById('title'); return x && !x.hidden ? 'title shown' : 'title hidden'; })()"))
    t.ev("crowd.update = () => { throw new Error('rv37: all bad'); }"); t.step(25); say('   ', top_at_card(t)); t.page.screenshot(path=str(HERE / 'loop-card-title.png')); t.close()
    # 7. Reload: does the page come back, and what was saved on the way out
    t = Tab(pw, p, plant=ARRIVED); t.step(30); t.ev("if (typeof introOn === 'function' && introOn()) introSkip()"); t.step(10); t.ev('saveGame()'); t.ev('skipTo(shipNow() + 30)'); t.step(3); now = t.ev('shipNow()')
    t.ev("crowd.update = () => { throw new Error('rv37: all bad'); }"); t.step(25)
    with t.page.expect_navigation(timeout=120000): t.page.click('#loopCard button')
    t.page.wait_for_function('window.__sc !== undefined', timeout=120000)
    say(f'loop 7, Reload pressed: the page came back at ship minute {t.ev("shipNow()"):.0f} (it was {now:.0f} when the error began); card now {t.page.evaluate("!!document.getElementById(\'loopCard\')")}'); t.close()

def part_keep(pw):
    p = build('rv_keep', on=ALL); key, good = good_save(pw, p); bad = key + '-bad'
    A = good[:len(good) // 2]; B = good.replace('"v":2', '"v":3', 1)
    t = Tab(pw, p, plant={key: A, **ARRIVED}); t.step(60); say('keep 1, first unreadable save (cut short): kept copy is A:', t.store(bad) == A, '| told:', t.toast()[:60])
    t.page.evaluate('([k, v]) => localStorage.setItem(k, v)', [key, B]); t.page.evaluate("window.__hold = 1"); t.ev('SLOT_HOLD = true')   # nothing saved on the way out
    t.page.reload(); t.page.wait_for_function('window.__sc !== undefined', timeout=120000); t.ev(SKIP_SWITCH); t.step(60)
    say('keep 2, a second unreadable save (unknown version) while the first copy is still there: kept copy is A:', t.store(bad) == A, ', is B:', t.store(bad) == B, '| told:', t.toast()[:110])
    say('   Saves app:', re.findall(r'"text": "([^"]*)", "mark": "urgent"', json.dumps(t.ev('slotsView()'))))
    t.ev("if (typeof introOn === 'function' && introOn()) introSkip()"); t.ev('skipTo(shipNow() + 61)'); t.step(5)
    say('   Saves app buttons:', re.findall(r'"label": "([^"]*)"', json.dumps(t.ev('slotsView()'))))
    if t.ev("typeof SAVE_BAD_KEY") == 'string':
        before = t.store(bad) is not None; t.ev("slotsAct('baddel')"); say('   Throw it away, one tap: the first copy was there:', before, '| after one tap it is there:', t.store(bad) is not None, '| the Saves app then says:', re.findall(r'"text": "([^"]*)", "mark": "urgent"', json.dumps(t.ev('slotsView()'))))
    say('   an hour on: B still anywhere in storage:', t.page.evaluate('v => Object.keys(localStorage).some(k => localStorage.getItem(k) === v)', B)); t.close()
    # slot 2
    t = Tab(pw, p, plant={key + '-slot': '2', key + '-2': A, **ARRIVED}); t.step(60)
    say('keep 3, slot 2 unreadable: keys in storage', sorted(t.page.evaluate('Object.keys(localStorage)')), '| slots seen:', [(x['n'], x['used'], x['ok']) for x in t.ev('slotInfo()')]); t.close()
    # the real way in: the title up, an unreadable save
    t = Tab(pw, p, '?title', plant={key: A, **ARRIVED}); t.step(10)
    say('keep 4, title with an unreadable save: menu', t.page.evaluate("[...document.querySelectorAll('#tiMenu button')].filter(b => !b.hidden && b.offsetParent).map(b => b.textContent.trim())"), '| line:', t.page.evaluate("document.getElementById('tiLine').textContent"), '| found:', t.page.evaluate("document.getElementById('tiFound').textContent"))
    t.page.screenshot(path=str(HERE / 'keep-title.png')); t.close()

def part_tell(pw):
    # 1. the save's text, old code and new, after the same play
    texts = {}
    for tag, on in (('rv_tell_off', []), ('rv_tell_on', {'all': ALL, 'save': ['SAVE_TELL_ON', 'SAVE_TAB_ON', 'SAVE_KEEP_ON'], 'none': []}[os.environ.get('RV_TELL1', 'all')])):
        t = Tab(pw, build(tag, on=on), plant=ARRIVED); t.step(30); t.ev("if (typeof introOn === 'function' && introOn()) introSkip()"); t.step(30); t.ev('skipTo(3 * 1440 + 600)'); t.step(30); t.ev('saveGame()'); texts[tag] = t.store(t.ev('SAVE_KEY')); t.close()
    a, b = texts['rv_tell_off'], texts['rv_tell_on']
    def paths(x, y, at=''):
        if type(x) != type(y): return [at]
        if isinstance(x, dict): return [q for k in set(x) | set(y) for q in (paths(x[k], y[k], at + '.' + k) if k in x and k in y else [at + '.' + k])]
        if isinstance(x, list): return [at + ' (length)'] if len(x) != len(y) else [q for i in range(len(x)) for q in paths(x[i], y[i], at + f'[{i}]')]
        return [] if x == y else [f'{at}: {x!r} / {y!r}']
    say(f'tell 1, the save written by the old code and by the new after the same play: {len(a)} and {len(b)} characters, same text: {a == b}', paths(json.loads(a), json.loads(b))[:12])
    if os.environ.get('RV_TELL1'): return
    p = build('rv_tell_on2', on=ALL); key, good = good_save(pw, p)
    # 2. a handler that writes inside save.player fails (credits, locker, chats)
    t = Tab(pw, p, plant={key: good, **ARRIVED}); t.step(30); t.ev('saveGame()')
    i = t.ev("SAVE_EXTRA.findIndex(f => /p\\.credits = /.test(String(f)))"); before = t.ev('({ credits: SHIP.player.credits, locker: SHIP.player.locker.length })'); t.ev('SHIP.player.credits += 500')
    t.ev(f"SAVE_EXTRA[{i}] = () => {{ throw new Error('rv37: the credits handler fails'); }}"); t.ev('skipTo(shipNow() + 61)'); t.ev("toast('x', 'y')"); t.step(5); r = t.ev('saveGame()'); t.step(5); s = json.loads(t.store(key))
    say(f"tell 2, the handler for credits (number {i}, parts {t.ev('SAVE_ST.parts ? SAVE_ST.parts[%d] : null' % i)}) fails: saveGame answers {r}; saved player has credits: {'credits' in s['player']}, locker: {'locker' in s['player']}, chats: {'chats' in s['player']}; told: {t.toast()[:40]!r}; SAVE_ST.fail {t.ev('SAVE_ST.fail')}")
    t.ev('SLOT_HOLD = true'); t.page.reload(); t.page.wait_for_function('window.__sc !== undefined', timeout=120000); t.ev(SKIP_SWITCH); t.step(30)
    say(f"   after a reload: credits {t.ev('SHIP.player.credits')}, locker {t.ev('SHIP.player.locker.length')} (before the fault: {before}; then 500 were earned); errors {t.errors[:1]}"); t.close()
    t = Tab(pw, p, plant={key: good, **ARRIVED}); t.step(30); t.ev('saveGame()'); i = t.ev("SAVE_EXTRA.findIndex(f => /p\\.credits = /.test(String(f)))"); c0 = t.ev('SHIP.player.credits'); t.ev('SHIP.player.credits += 500')
    t.ev(f"(() => {{ const f = SAVE_EXTRA[{i}]; SAVE_EXTRA[{i}] = s => {{ s.player.credits = 1; s.player.locker = 'half'; throw new Error('rv37: fails half way'); }}; }})()"); t.ev('skipTo(shipNow() + 61)'); t.ev("toast('x', 'y')"); t.step(5); r = t.ev('saveGame()'); t.step(5); s = json.loads(t.store(key))
    say(f"tell 2b, the credits handler fails half way after a good save this sitting: saveGame {r}; Download my save gives minute {json.loads(t.ev('slotText()'))['time']['min']:.0f}; stored credits {s['player'].get('credits')} (were {c0}, now {c0 + 500} in play), locker {s['player'].get('locker')!r}, stored minute {s['time']['min']:.0f} against {t.ev('SHIP.time.min'):.0f} now; told {t.toast()[:30]!r}; Saves app: {re.findall(r'\"text\": \"([^\"]*)\", \"mark\": \"urgent\"', json.dumps(t.ev('slotsView()')))}"); t.close()
    # 3. a top-level handler fails at the first save after loading (nothing kept yet this sitting)
    t = Tab(pw, p, plant={key: good, **ARRIVED}); t.step(30)
    i = t.ev("SAVE_EXTRA.findIndex(f => /s\\.social = socSave/.test(String(f)))"); met = t.ev("Object.values(SHIP.rel).filter(r => r.met !== null).length")
    t.ev(f"SAVE_EXTRA[{i}] = () => {{ throw new Error('rv37: the social handler fails'); }}"); t.ev("toast('x', 'y')"); r = t.ev('saveGame()'); t.step(5); s = json.loads(t.store(key))
    say(f"tell 3, the social handler fails at the first save after loading: saveGame answers {r}; 'social' in the stored save: {'social' in s} (it was in the save loaded: {'social' in json.loads(good)}); told: {t.toast()[:40]!r}")
    t.ev('SLOT_HOLD = true'); t.page.reload(); t.page.wait_for_function('window.__sc !== undefined', timeout=120000); t.ev(SKIP_SWITCH); t.step(30)
    say(f"   after a reload: people met {t.ev('Object.values(SHIP.rel).filter(r => r.met !== null).length')} (before: {met}); errors {t.errors[:1]}"); t.close()
    # 4. the same fault with the switch off (today's game): nothing saved, the old save whole
    t = Tab(pw, build('rv_tell_off2', on=[]), plant={key: good, **ARRIVED}); t.step(30)
    i = t.ev("SAVE_EXTRA.findIndex(f => /s\\.social = socSave/.test(String(f)))"); t.ev(f"SAVE_EXTRA[{i}] = () => {{ throw new Error('rv37'); }}"); t.ev('skipTo(shipNow() + 61)'); t.step(5); t.ev('saveGame()')
    say("tell 4, same fault, switches off: the stored save is still the one loaded, whole:", t.store(key) == good); t.close()

def part_tab(pw):
    p = build('rv_tab', on=ALL); key, good = good_save(pw, p)
    def at(day): s = json.loads(good); s['time']['day'] = day; return json.dumps(s)
    # 1. a new game over a Day 10 save, same tab (the title's "New game", "start over")
    t = Tab(pw, p, plant={key: good, **ARRIVED}); t.step(30); t.ev('newGameStart(false); if (typeof introSkip === "function") introSkip()'); t.step(30); r = t.ev('saveGame()'); t.ev('skipTo(shipNow() + 61)'); t.step(5)
    say(f"tab 1, new game over a Day 10 save in the same tab: saveGame {r}, stopped {t.ev('SAVE_ST.other')}, stored Day {json.loads(t.store(key))['time']['day']}"); t.close()
    # 2. Load a save file into the slot being played: an older file, then a newer one
    for name, day in (('older (Day 4)', 4), ('newer (Day 20)', 20)):
        t = Tab(pw, p, plant={key: good, **ARRIVED}); t.step(30); t.ev('saveGame()')
        try:
            with t.page.expect_navigation(timeout=120000): t.ev(f"slotPut(SAVE_SLOT, {at(day)})")
        except Exception as e: say('   (reload wait:', str(e)[:80], ')')
        t.page.wait_for_function('window.__sc !== undefined', timeout=120000); t.ev(SKIP_SWITCH); t.step(30); t.ev('skipTo(shipNow() + 61)'); t.step(5); r = t.ev('saveGame()')
        if os.environ.get('RV_DBG'): say('   dbg: stored after reload', json.loads(t.store(key))['time'], 'SAVED', t.ev('SAVED && SAVED.time'), 'errors', t.errors[:2], 'toast', t.toast()[:80])
        say(f"tab 2, Load a save file, {name}, into the slot being played: now Day {t.ev('SHIP.time.day')}, saveGame {r}, stopped {t.ev('SAVE_ST.other')}, stored Day {json.loads(t.store(key))['time']['day']}"); t.close()
    # 3. a stopped tab: what Download my save hands over two hours later
    t = Tab(pw, p, plant={key: good, **ARRIVED}); t.step(30); t.ev('saveGame()'); t.page.evaluate('([k, v]) => localStorage.setItem(k, v)', [key, at(12)]); t.ev('saveGame()'); t.step(5); m0 = t.ev('shipNow()')
    t.ev('skipTo(shipNow() + 125)'); t.step(5); x = json.loads(t.ev('slotText()'))
    say(f"tab 3, stopped tab, two ship hours later: Download my save hands over Day {x['time']['day']} minute {x['time']['min']:.0f}; this tab is at Day {t.ev('SHIP.time.day')} minute {t.ev('SHIP.time.min'):.0f}; the other tab's save is Day 12"); t.close()
    # 4. the other way: the other tab started a new game (Day 1); this tab at Day 10 saves
    t = Tab(pw, p, plant={key: good, **ARRIVED}); t.step(30); t.ev('saveGame()'); t.page.evaluate('([k, v]) => localStorage.setItem(k, v)', [key, at(1)]); r = t.ev('saveGame()')
    say(f"tab 4, another tab started a new game (Day 1) in this slot: this tab's saveGame {r}, stored Day {json.loads(t.store(key))['time']['day']} (the new game is written over, as today)"); t.close()
    # 5. two real tabs on one browser
    t = Tab(pw, p, plant={key: good, **ARRIVED}); t.step(30); t.ev('saveGame()')
    pg = t.page.context.new_page(); pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript')); pg.add_init_script(INIT); pg.goto(t.url, timeout=180000); pg.wait_for_function('window.__sc !== undefined', timeout=120000)
    ev2 = lambda s: pg.evaluate('s => window.__sc(s)', s)
    pg.evaluate('window.__step(30, 33.3)'); ev2('skipTo(shipNow() + 200)'); pg.evaluate('window.__step(5, 33.3)'); r2 = ev2('saveGame()')
    t.ev('skipTo(shipNow() + 61)'); t.step(5); r1 = t.ev('saveGame()'); t.step(5)
    say(f"tab 5, two real tabs: the second plays 200 minutes on and saves ({r2}); the first, 61 minutes on, saves: {r1}, stopped {t.ev('SAVE_ST.other')}, told {t.toast()[:40]!r}")
    r2b = ev2('skipTo(shipNow() + 61); saveGame()'); say(f"   the second tab keeps saving: {r2b}, stopped {ev2('SAVE_ST.other')}"); t.close()

def part_memo(pw):
    t = Tab(pw, build('rv_memo', on=ALL), '?nosave&debug'); t.step(30)
    CHK = "(() => { const a = evonFlagged(), b = SHIP_TRADITIONS.filter(e => e.flag || e.unflag); return a.length === b.length && a.every((x, i) => x === b[i]); })()"
    bad = 0; n = 0
    for h in range(0, 24 * 24, 3):
        t.ev(f'skipTo(1440 + {h} * 60)'); t.step(2); n += 1
        if not t.ev(CHK): bad += 1
    say(f"memo 1, 24 ship days in 3-hour steps: the kept list differed from a fresh one {bad} times of {n}; kept {t.ev('EVON_L.length')} of {t.ev('SHIP_TRADITIONS.length')} traditions")
    # a tradition replaced in place (as the words loader does), one added, one taken out
    r = t.ev("(() => { const out = []; const fresh = () => SHIP_TRADITIONS.filter(e => e.flag || e.unflag).length; const i = SHIP_TRADITIONS.findIndex(e => !e.flag && !e.unflag); const old = SHIP_TRADITIONS[i]; SHIP_TRADITIONS[i] = { ...old, flag: 'rv37.x' }; out.push([evonFlagged().length, fresh()]); SHIP_TRADITIONS[i] = old; out.push([evonFlagged().length, fresh()]); const x = { id: 'rv37', flag: 'rv37.y', when: {}, at: [0, 1] }; SHIP_TRADITIONS.push(x); out.push([evonFlagged().length, fresh()]); SHIP_TRADITIONS.pop(); out.push([evonFlagged().length, fresh()]); return out; })()")
    say('memo 2, replaced in place / put back / added / removed: [kept, fresh] =', r)
    r = t.ev("(() => { const f = SHIP_TRADITIONS.find(e => e.unflag).unflag; const a = EV_ARR; eventsOn(5); const b = EV_ARR; flagSet(f); eventsOn(5); const c = EV_ARR; return [f, a === b, b !== c]; })()")
    say('memo 3, a flag set between two calls in one frame: [flag, same before, changed after] =', r); t.close()
    # a Dev jump
    t = Tab(pw, build('rv_memo2', on=ALL), '#dev', plant=None); t.step(30)
    say('memo 4, Dev mode up:', t.ev('DEVMODE'), '| kept list right after load:', t.ev(CHK))
    try:
        t.ev("skipTo(20 * 1440 + 600)"); t.step(5); say('   after a jump to Day 21:', t.ev(CHK), '| errors', t.errors[:1])
    except Exception as e: say('   jump failed:', str(e)[:120])
    t.close()

def part_walls(pw):
    seqs = {}
    for tag, on in (('rv_walls_off', []), ('rv_walls_on', ['WALLS_STILL_ON'])):
        t = Tab(pw, build(tag, on=on), '?nosave&debug&crew', wait=True); h = []
        def snap(label):
            t.page.evaluate('window.__skip = false; window.__step(1, 33.3)'); h.append((label, hashlib.sha256(t.page.screenshot()).hexdigest()[:12]))
        for k in range(4): snap(f'first frame {k + 1}')
        t.page.click('#walls')
        for k in range(14): snap(f'walls pressed, frame {k + 1}')
        t.page.click('#walls')
        for k in range(14): snap(f'walls pressed again, frame {k + 1}')
        while t.ev("wallsMode !== 'auto'"): t.page.click('#walls')
        for k in range(6): snap(f'walls back to auto, frame {k + 1}')
        for d in (3, 6, 5, 7, 4):
            t.ev(f'goToDeck({d})')
            for k in range(5): snap(f'Deck {d}, frame {k + 1}')
            t.page.click('#walls'); snap(f'Deck {d}, walls pressed, frame 1'); snap(f'Deck {d}, walls pressed, frame 2')
            while t.ev("wallsMode !== 'auto'"): t.page.click('#walls')
            snap(f'Deck {d}, walls auto')
        t.ev('skipTo(1440 + 7 * 60 + 50)')                # the morning: people through doors
        for k in range(60):
            t.page.evaluate('window.__skip = false; window.__step(3, 33.3)'); snap(f'morning, step {k + 1}')
        doors = t.ev("DOOR_OBJS.filter(d => d.open > .02 || (d.k || 0) > .02).length")
        # rotate the view, which lowers other walls
        for k in range(4):
            t.ev("typeof rotateView === 'function' ? rotateView(1) : document.getElementById('rot') && document.getElementById('rot').click()")
            for j in range(6): snap(f'turn {k + 1}, frame {j + 1}')
        seqs[tag] = h; say(f'walls: {tag}: {len(h)} pictures, errors {t.errors[:1]}, doors moving at the end {doors}'); t.close()
    a, b = seqs['rv_walls_off'], seqs['rv_walls_on']; diff = [x[0] for x, y in zip(a, b) if x[1] != y[1]]
    say(f'walls 1: {len(a)} pictures, every frame drawn, switch off against on: {len(diff)} differ', diff[:10], '| different pictures in the run:', len(set(x[1] for x in a)))

def part_load(pw):
    p = build('rv_load', on=ALL); key, good = good_save(pw, p); base = json.loads(good); now = base['time']['day'] * 1440 - 1440 + base['time']['min']
    def mk(f):
        s = json.loads(good); f(s); return json.dumps(s)
    C = {
        'stories.cs is a number': lambda s: s['social']['stories'].__setitem__('cs', 5),
        'stories.cs is a list': lambda s: s['social']['stories'].__setitem__('cs', []),
        'stories is a number': lambda s: s['social'].__setitem__('stories', 7),
        'cs.book is text, told is null': lambda s: s['social']['stories']['cs'].update(book='x', told=None),
        'garden is a number': lambda s: s['galley'].__setitem__('garden', 5),
        'garden beds hold junk': lambda s: s['galley']['garden'].__setitem__('beds', [[0, 'x', 1], None, [0.5, 1, 1], [0, None, None], 'bed', [-1, 1, 1]]),
        'garden crates hold junk': lambda s: s['galley']['garden'].__setitem__('crates', [None, {'at': 1, 'items': 'x'}, {'at': 'soon', 'items': []}, 5]),
        'cold produce is text': lambda s: s['galley']['cold'].__setitem__('produce', 'x'),
        'cold is a list of one': lambda s: s['galley'].__setitem__('cold', {'meals': 5, 'produce': [[0, 1]]}),
        'a repair note with no data': lambda s: s['social'].setdefault('noteq', []).insert(0, [now - 10, 'repair', None]),
        'a repair note with empty data': lambda s: s['social'].setdefault('noteq', []).insert(0, [now - 10, 'repair', {}]),
        'a tradition note with empty data': lambda s: s['social'].setdefault('noteq', []).insert(0, [now - 10, 'tradition', {}]),
        'a tradition note whose data is text': lambda s: s['social'].setdefault('noteq', []).insert(0, [now - 10, 'tradition', 'x']),
        'a note that is not a list': lambda s: s['social'].setdefault('noteq', []).insert(0, 'x'),
        'ship.machines missing': lambda s: s['ship'].pop('machines', None),
        'the day far ahead (Day 80)': lambda s: s['time'].__setitem__('day', 80),
    }
    for name, f in C.items():
        try: bad = mk(f)
        except Exception as e: say(f'load: {name}: could not be made ({str(e)[:60]})'); continue
        t = Tab(pw, p, plant={key: bad, **ARRIVED}); res = 'did not start'
        if t.up:
            try: t.step(30); m = t.ev('shipNow()'); t.ev('skipTo(shipNow() + 125)'); t.step(60); res = 'plays two hours on' if not t.errors and t.ev('shipNow()') > m + 125 else 'started, then trouble'
            except Exception as e: res = 'started, then stopped: ' + str(e)[:100]
        say(f'load: {name}: {res}; errors {[e[:90] for e in t.errors[:2]]}; card {t.page.evaluate("!!document.getElementById(\'loopCard\')") if t.up else None}'); t.close()
    # a sound game: the guard must change nothing, day after day
    t = Tab(pw, p, '?nosave&debug'); t.step(30); changed = 0; n = 0; seen = 0
    for h in range(0, 16 * 24, 2):
        t.ev(f'skipTo(1440 + {h} * 60 + 7)'); t.step(2); n += 1
        r = t.ev("(() => { if (!SHIP.galley) return null; const a = JSON.stringify(SHIP.galley), c = JSON.parse(a); galleySafe(c); return [a === JSON.stringify(c), !!(c.garden && (c.garden.crates.length || c.cold.produce.length))]; })()")
        if r is None: continue
        if not r[0]: changed += 1
        if r[1]: seen += 1
    say(f'load, a sound game over 16 days in 2-hour steps: galleySafe changed the galley {changed} times of {n} (crates or produce present in {seen} of them)'); t.close()

def part_lib(pw):
    s = SRC; assert s.count(LIB + 'false;') == 1; s = s.replace(LIB + 'false;', LIB + 'true;'); p = WORK / 'test' / (RUN + 'rv_lib.html'); p.write_text(s)
    for name, q, plant in (('first visit', '', None), ('with a save', '', 1)):
        b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=ARGS); page = b.new_page(viewport={'width': 390, 'height': 844}); errs = []
        page.on('pageerror', lambda e: errs.append(str(e)[:80]))
        if plant: page.add_init_script("localStorage.setItem('starship-cadet-save', JSON.stringify({ v: 2, time: { day: 5, min: 600 }, player: { deck: 4, tile: [10, 10], facing: 0 } })); localStorage.setItem('starship-cadet-arrived', '1')")
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', { get: () => false })")
        page.route(re.compile(r'.*three\.min\.js'), lambda r: r.abort()); page.goto('file://' + str(p) + q, timeout=120000); page.wait_for_timeout(1500)
        rd = lambda: page.evaluate("(() => { const t = document.getElementById('title'); return (t && !t.hidden ? 'shown' : 'hidden') + ' | ' + document.getElementById('tiLine').textContent + ' | found: ' + document.getElementById('tiFound').textContent.trim().slice(0, 60) + ' | menu ' + (document.getElementById('tiMenu').hidden ? 'hidden' : 'shown') + ' | asleep ' + t.classList.contains('asleep'); })()")
        say(f'lib, {name}: {rd()}')
        page.mouse.click(195, 420); page.keyboard.press('Enter'); page.mouse.click(195, 600); page.wait_for_timeout(2500)
        say(f'   after taps, a key and 2.5 s: {rd()} | page errors {errs[:2]}'); page.screenshot(path=str(HERE / f'lib-{name.replace(" ", "-")}.png')); b.close()

PARTS = [('loop', part_loop), ('keep', part_keep), ('tell', part_tell), ('tab', part_tab), ('memo', part_memo), ('walls', part_walls), ('load', part_load), ('lib', part_lib)]
if __name__ == '__main__':
    with sync_playwright() as pw:
        for name, f in PARTS:
            if ONLY and name not in ONLY: continue
            say(f'-- {name}')
            try: f(pw)
            except Exception as e: say(f'PROBE PART STOPPED {name}: {str(e)[:400]}')
