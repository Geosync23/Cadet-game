# my instrumented fresh walk (based on RV32's fresh_walk): logs tips, toasts, dialogue, mail, arrows, acts, screenshots on arrow change
import sys, os, json
args = sys.argv[1:]; BUILD, LAST, OUT = args[0], int(args[1]), args[2]
SHOTS = os.path.dirname(os.path.abspath(OUT)) + '/shots'
SLEEP = '22:30'
sys.argv = [sys.argv[0], BUILD]
exec(open('/home/user/Cadet-game/arrows_check.py').read().split('\nwith sync_playwright() as pw:')[0])
hm = lambda s: int(s[:2]) * 60 + int(s[3:])
TIPS = """(() => { window.__tips = []; const o = tipShow; tipShow = function (id, t) { const r = o.apply(this, arguments); if (r) window.__tips.push([clockText(), 'TIP', id, String(t)]); return r; };
  const ts = toast; toast = function (a, b) { window.__tips.push([clockText(), 'TOAST', String(a), String(b || '')]); return ts.apply(this, arguments); };
  const dd = dialogueDraw; dialogueDraw = function () { try { const v = DIALOGUE && dialogueView(); if (v) window.__tips.push([clockText(), 'SAY', v.title + ' | ' + v.name, v.text + (v.choices ? ' CHOICES: ' + v.choices.join(' / ') : '')]); } catch (e) {} return dd.apply(this, arguments); };
  const ms = mailSend; mailSend = function (o) { try { window.__tips.push([clockText(), 'MAIL', String(o.from), String(o.subject) + ' :: ' + String(o.body)]); } catch (e) {} return ms.apply(this, arguments); };
  const bs = bubbleSay; bubbleSay = function (who, text) { try { const p = player.obj.position, w = who && (who.obj ? who.obj.position : who); if (w && isFinite(w.x) && Math.hypot(w.x - p.x, w.z - p.z) < 6) window.__tips.push([clockText(), 'BUBBLE', (who.spec && who.spec.name) || (who.p && who.p.name) || '?', String(text)]); } catch (e) {} return bs.apply(this, arguments); };
})()"""
log = {'ev': [], 'arrows': [], 'acts': [], 'state': []}
def shot(pg, name):
    pg.ev('window.__draw = true'); pg.step(1, 20); pg.page.screenshot(path=f'{SHOTS}/{name}.png'); pg.ev('window.__draw = false')
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME'), args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1, has_touch=True, is_mobile=True)
    pg = Page(ctx, BUILD)
    pg.ev('localStorage.clear()'); pg.ev('newGameStart(true)'); pg.step(5)
    pg.page.fill('form input[maxlength="24"]', 'Sam'); pg.page.click('form button'); pg.step(5)
    pg.ev(TIPS)
    print('start', pg.ev('clockText()'), flush=True)
    f = Follower(pg); last_arrow = None; nshot = 0
    f.pre = """(() => { window.__rvDev = DEV.open && !DEV.choose && !DIALOGUE ? (window.__rvDev || 0) + 1 : 0;
      if (window.__rvDev >= 4) { window.__rvDev = 0; deviceClose(); return 'rv32: close the device'; }
      if (ACT && ACT.kind === 'sit' && ACT.phase !== 'walk' && goalNow() && !DIALOGUE) { actEnd(); return 'rv32: get up for ' + goalNow().label; }
      return null; })()"""
    for day in range(0, LAST + 1):
        end = (day - 1) * 1440 + hm(SLEEP)
        lastst = -999
        while pg.ev('shipNow()') < end:
            f.run(min(end, pg.ev('shipNow()') + 10))
            a = pg.ev("(() => { const g = goalNow(); return g ? g.label : null; })()")
            now = pg.ev('shipNow()')
            if a != last_arrow:
                ct = pg.ev('clockText()'); log['arrows'].append((ct, a)); last_arrow = a
                if nshot < 400: nshot += 1; shot(pg, f'd{day:02d}_{int(now) % 1440 // 60:02d}{int(now) % 60:02d}_{nshot:03d}')
            if now - lastst >= 60:
                lastst = now
                log['state'].append(pg.ev("(() => { const P = SHIP.player; return [clockText(), deckDef.num, roomAt(...player.here()), JSON.stringify(P.needs, (k, v) => typeof v === 'number' ? Math.round(v) : v), P.credits, ACT ? ACT.kind : null]; })()"))
            for x in f.acts: log['acts'].append(x)
            f.acts.clear()
            log['ev'] += pg.ev('window.__tips.splice(0)')
        print(f'--- Day {day} done at', pg.ev('clockText()'), len(log['ev']), flush=True)
        log['stuck'] = f.stuck; log['long'] = f.long; log['errors'] = pg.errors[:20]
        json.dump(log, open(OUT, 'w'), indent=0)
        if day < LAST:
            print('  bed', pg.ev("(() => { if (DIALOGUE) dialogueEnd(true); if (DEV.open) deviceClose(); if (ACT) actEnd(true); goToDeck(4); const s = placeSpot(playerBed()); player.obj.position.set(s.x, 0, s.z); player.stop(); sleepGo(360); return [playerBed(), sleeping]; })()"), flush=True)
            for k in range(40):
                pg.page.wait_for_timeout(500); pg.step(2, 50)
                if not pg.ev('sleeping'): break
            print('  awake', pg.ev('clockText()'), flush=True)
print('stuck', log['stuck']); print('errors', log['errors'])
