# RV25: EV1 visit-on, the Diplomatic visit in real play at 390x844, Days 16-19 (from RV24's cq_play.py).
# Dev 'Set career to Day 16' (no beat), then each visit day: the arrow is followed by moving to its deck and place,
# scenes are played through, toasts, bubbles, Mail and the goal are logged; shots at the big moments.
import sys, os, json, re
G = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
exec(open(os.path.join(os.path.dirname(os.path.abspath(G)), 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
vp = WORK / 'test' / '_rv25_j4.html'; vp.write_text(open(G).read())
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
    g.ev = lambda src: g.page.evaluate('s => window.__sc(s)', src)
    g.ev(SKIP_SWITCH)
    g.step = lambda n, dt=1000/30: g.page.evaluate(f'(() => {{ window.__skip = true; if ({n} > 1) window.__step({n} - 1, {dt}); window.__skip = false; window.__step(1, {dt}); }})()')
    g.step(20)
    if g.page.locator('text=Sign and go aboard').count(): g.page.fill('form input', 'Ada'); g.page.click('text=Sign and go aboard'); g.step(30)
    print('set', g.ev("devmodeRun('Set career to Day 27', () => devmodeSetCareerTo(27))")); g.step(30)
    A = """(() => { const a = dvCareerNext(); const evm = (typeof MEETINGS !== 'undefined' ? MEETINGS : []).filter(m => SHIP.event && m.event === SHIP.event.id).map(m => m.id + ' ' + hhmm(m.at % 1440) + ' ranks=' + JSON.stringify(m.ranks) + ' invited=' + evInvited(m));
      return { clock: clockText(), rank: SHIP.works.rank, ev: SHIP.event && [SHIP.event.id, SHIP.event.phase], arrow: a && [a.label, a.deck, a.room, a.key], meetings: evm }; })()"""
    for t in [D(27, 8, 50), D(27, 9, 50), D(27, 10, 5), D(27, 11, 0), D(28, 9, 25), D(29, 9, 15), D(29, 14, 25), D(29, 14, 45)]:
        g.ev(f"devmodeSkipTo({t})"); g.step(5)
        print(json.dumps(g.ev(A)))
    print('errors', g.errors[:5]); br.close()
