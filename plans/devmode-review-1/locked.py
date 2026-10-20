# DR1: Take me to every room of every deck (Dev on): which rooms leave you somewhere you can't walk back to the lift from?
import sys, os, re, json, pathlib
os.environ.setdefault('CADET_CHROME','/opt/pw-browsers/chromium')
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("class Game")[0])
from playwright.sync_api import sync_playwright
tmp = WORK / 'test' / '_dr1_locked.html'; tmp.write_text(instrument(pathlib.Path(sys.argv[1]).read_text()))
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ['CADET_CHROME'], args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    pg = b.new_page(viewport={'width':390,'height':844}); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:150]))
    pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    pg.add_init_script(INIT); pg.goto('file://' + str(tmp) + '#dev')
    pg.wait_for_function('window.__sc !== undefined', timeout=90000)
    ev = lambda s: pg.evaluate('s => window.__sc(s)', s)
    ev("(() => { renderer.render = () => {}; })()"); pg.evaluate('window.__step(10, 33)')
    ev("(INTRO_BOOT = false, newGameStart(false), introSkip(), skipTo(shipNow() + 240), 0)")
    r = ev(r"""(() => { const out = [];
      for (const n of DECK_ORDER) { if (!DECKS[n] || (n === 7 && !REC_DECK)) continue;
        for (const k of Object.keys(DECKS[n].rooms || {})) { if (devmodeSpine(n, k) || !DECKS[n].rooms[k].name) continue;
          DM_HOLD = true; let c = null; try { c = devmodeMove(n, () => ixGoalWorld({ room: k }), r => r === k); } finally { DM_HOLD = false; }
          if (!c) { out.push([n, DECKS[n].rooms[k].name, 'no spot']); continue; }
          const lobby = (DECKS[n].lift || null), inRoom = roomAt(...c) === k;
          // can you walk out to the lift lobby from here?
          const tiles = []; for (let a = 0; a < W; a++) for (let b = 0; b < D; b++) if (free(a, b) && roomAt(a, b) === '@') tiles.push([a, b]);
          let back = false; for (const t of tiles.slice(0, 6)) if (findPath(c, t, null, player)) { back = true; break; }
          if (!inRoom || !back) out.push([n, DECKS[n].rooms[k].name, inRoom ? 'in room' : 'NOT in room (put elsewhere)', back ? 'can walk to lift' : 'CAN\'T walk to the lift']);
        } }
      return out; })()""")
    for x in r: print(x)
    print('errors', errs[:3]); b.close()
