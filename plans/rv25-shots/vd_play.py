# RV25: EV1 visit-on, the Diplomatic visit in real play at 390x844, Days 16-19 (from RV24's cq_play.py).
# Dev 'Set career to Day 16' (no beat), then each visit day: the arrow is followed by moving to its deck and place,
# scenes are played through, toasts, bubbles, Mail and the goal are logged; shots at the big moments.
import sys, os, json, re
G = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
exec(open(os.path.join(os.path.dirname(os.path.abspath(G)), 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
vp = WORK / 'test' / '_rv25_vd.html'; vp.write_text(open(G).read())
RVHOOK = """(() => { window.__t = window.__t || []; window.__b = window.__b || [];
  if (!window.__hooked) { window.__hooked = 1; const T = toast; toast = (a, b) => { window.__t.push(clockText() + ' ' + a + ': ' + b); return T(a, b); };
  const B = bubbleSay; bubbleSay = (w, t, s) => { try { window.__b.push(clockText() + ' ' + ((w && ((w.p && w.p.id) || w.id || w.name)) || w) + ': ' + t); } catch (e) {} return B(w, t, s); }; } })()"""
ST = """(() => { const g = goalNow(); const vey = ['teshavi','kesrin','moleth','ithra','saruth','marrow','vance'].map(id => { const a = DECK_CREW.find(c => c.p && c.p.id === id); return a ? id + '@' + Math.round(Math.hypot(a.x - player.obj.position.x, a.z - player.obj.position.z) * 10) / 10 : null; }).filter(Boolean);
  return { clock: clockText(), day: SHIP.day, deck: deckDef && deckDef.num, room: (ROOMS[roomAt(...player.here())] || {}).name || roomAt(...player.here()), goal: g && [g.label, g.deck || null, g.place || g.crew || g.room || null], dlg: DIALOGUE && DIALOGUE.id,
    ev: SHIP.event && [SHIP.event.id, SHIP.event.phase], near: vey, crew: DECK_CREW.length, calls: renderer.info.render.calls }; })()"""
def log(g, tag):
    s = g.ev(ST); t = g.ev("window.__t.splice(0)"); b = g.ev("window.__b.splice(0)")
    print(tag, json.dumps(s)); [print('   toast', x) for x in t]; [print('   say', x) for x in b]; sys.stdout.flush(); return s
def play(g, pick=0):
    n = 0; lines = []
    while g.ev("!!DIALOGUE") and n < 80:
        v = g.ev("(() => { const v = dialogueView(); return v ? { who: v.who || v.name || null, text: v.text || null, ch: !!v.choices } : null; })()")
        if v: lines.append(v)
        g.ev(f"(() => {{ const v = dialogueView(); if (v && v.choices) dialogueChoose({pick}); else dialogueNext(); }})()"); g.step(2); n += 1
    for v in lines: print('     |', v.get('who'), ':', (v.get('text') or '')[:150])
    return lines
FOLLOW = """(() => { const g = goalNow(); if (!g || DIALOGUE || ACT) return null;
  if (g.deck && deckDef.num !== g.deck) { goToDeck(g.deck); return 'deck ' + g.deck; }
  let s = null; try { if (g.place) s = placeSpot(g.place); } catch (e) {}
  if (!s && g.crew) { const a = DECK_CREW.find(c => c.p && c.p.id === g.crew); if (a) s = { x: a.x + 0.8, z: a.z }; }
  if (!s && g.room && ROOM_TILES[g.room]) s = cellPos(...ROOM_TILES[g.room][Math.floor(ROOM_TILES[g.room].length / 2)]);
  if (!s && typeof ixGoalWorld === 'function') { try { const w = ixGoalWorld(g); if (w) s = w; } catch (e) {} }
  if (!s) return 'no spot';
  const d = Math.hypot(s.x - player.obj.position.x, s.z - player.obj.position.z); if (d < 1.2) { if (/^Clock (in|out)/.test(g.label)) { try { clockPunch(false); return 'punched'; } catch (e) { return 'punch ' + e; } } return null; }
  player.obj.position.set(s.x, player.obj.position.y, s.z); player.stop(); return 'moved ' + (g.place || g.crew || g.room || '?'); })()"""
D = lambda d, h, m: (d - 1) * 1440 + h * 60 + m
def watch(g, frm, to, tag, shots=(), every_min=5):
    g.ev(f"devmodeSkipTo({frm}); for (const k of NEED_KEYS) SHIP.player.needs[k] = Math.max(SHIP.player.needs[k], 85)"); g.step(10)
    log(g, f'== {tag} from'); last = None; shot = set()
    while g.ev('shipNow()') < to:
        g.step(30, 100)
        if g.ev("!!DIALOGUE"):
            s = log(g, ' scene'); g.shot(f'{OUT}/{tag}_scene_{s["clock"].replace(":", "")}.png'); play(g); g.step(5); log(g, ' after scene')
        f = g.ev(FOLLOW)
        if f: print('   follow', f, g.ev('clockText()')); g.step(10)
        mn = g.ev("Math.floor(shipNow() % 1440)")
        for sm in shots:
            if mn >= sm and sm not in shot: shot.add(sm); s = log(g, f' shot {sm}'); g.shot(f'{OUT}/{tag}_{sm // 60:02d}{sm % 60:02d}.png')
        if last is None or mn - last >= every_min: last = mn; log(g, ' ')
    log(g, f'== {tag} to')
with sync_playwright() as pw:
    class P: pass
    g = P(); br = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    g.page = br.new_page(viewport={'width': 390, 'height': 844}); g.errors = []
    g.page.on('pageerror', lambda e: g.errors.append(str(e)))
    g.page.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    g.page.add_init_script(INIT); html = vp.read_text(); i = html.rfind('})();'); tmp = WORK / 'test' / ('_rv25p_' + vp.name); tmp.write_text(html[:i] + "window.__sc = src => eval(src);\n" + html[i:])
    g.page.goto('file://' + str(tmp) + '#dev'); g.page.wait_for_function('window.__sc !== undefined', timeout=120000)
    g.page.add_style_tag(content='*,*::before,*::after{transition:none!important;animation:none!important}')
    g.ev = lambda src: g.page.evaluate('s => window.__sc(s)', src)
    g.step = lambda n, dt=1000/30: g.page.evaluate(f'(() => {{ window.__skip = true; if ({n} > 1) window.__step({n} - 1, {dt}); window.__skip = false; window.__step(1, {dt}); }})()')
    g.shot = lambda path: g.page.screenshot(path=path)
    g.ev(SKIP_SWITCH)
    g.step(20)
    if g.page.locator('text=Sign and go aboard').count(): g.page.fill('form input', 'Ada'); g.page.click('text=Sign and go aboard'); g.step(30)
    g.ev("SHIP.device && SHIP.device.settings && (SHIP.device.settings.tips = false)")
    print('set', g.ev("devmodeRun('Set career to Day 18', () => devmodeSetCareerTo(18))")); g.step(30); g.ev(RVHOOK)
    print('occ', g.ev("JSON.stringify((SHIP.occasions || []).filter(o => o.id === 'veyliDinner').map(o => [o.status, o.at, o.len]))"))
    SEAT = """(() => ['2-captable-1','2-captable-2','2-captable-3','2-captable-4','2-captable-5','2-captable-6','2-captable-7','2-captable-8'].map(id => { const c = placeSpot(id); if (!c || deckDef.num !== 2) return id.slice(-1) + ':-'; const on = DECK_CREW.filter(a => a.p && Math.hypot(a.x - c.x, a.z - c.z) < 0.45).map(a => a.p.id); return id.slice(-1) + ':' + (PLAYER_PLACE === id ? 'YOU ' : '') + on.join(','); }).join(' | '))()"""
    watch(g, D(18, 18, 35), D(18, 18, 58), 'd18a', shots=(1125,))
    print('seats 18:58', g.ev(SEAT), 'act', g.ev("ACT && [ACT.kind, ACT.placeId]"))
    watch(g, D(18, 18, 58), D(18, 19, 25), 'd18b', shots=(1145, 1150, 1160), every_min=3)
    print('seats 19:25', g.ev(SEAT), 'act', g.ev("ACT && [ACT.kind, ACT.placeId]"))
    print('occ', g.ev("JSON.stringify((SHIP.occasions || []).filter(o => o.id === 'veyliDinner').map(o => [o.status, o.met, o.f]))"))
    print('mail', g.ev("SHIP.mail.slice(-6).map(m => (m.from || '') + ': ' + (m.subject || ''))"))
    print('errors', g.errors[:8]); br.close()
