# RV32 probe (0.99.7; lead 49's rule): a fresh save with the intro ON, played by arrows_check's own follower (it follows
# every arrow, taps the pin, takes the board's job, reads dialogue on), phone size 390x844, from the arrival (Day 0 16:30)
# to the end of a day you name. Logs every tip as it is shown (tipShow), every arrow change and every action.
# Usage (from a worktree of the build, so arrows_check.py and cadet_test.py are beside it):
#   python3 /path/fresh_walk.py BUILD.html LAST_DAY [OUT.json] [--sleep HH:MM]   (to bed at HH:MM each night, default 22:30)
# FW_UNTIL=HH:MM ends the last day early; FW_TRACE=js logs a value whenever it changes
import sys, os, json
args = sys.argv[1:]; BUILD, LAST = args[0], int(args[1]); OUT = args[2] if len(args) > 2 and not args[2].startswith('--') else None
SLEEP = args[args.index('--sleep') + 1] if '--sleep' in args else '22:30'
sys.argv = [sys.argv[0], BUILD]
exec(open('arrows_check.py').read().split('\nwith sync_playwright() as pw:')[0])
hm = lambda s: int(s[:2]) * 60 + int(s[3:])
TIPS = """(() => { window.__tips = []; const o = tipShow; tipShow = function (id, t) { const r = o.apply(this, arguments); if (r) window.__tips.push([clockText(), id, String(t).slice(0, 160)]); return r; };
  const ts = typeof toast === 'function' ? toast : null; window.__toasts = []; if (ts) toast = function (a, b) { window.__toasts.push([clockText(), String(a), String(b || '').slice(0, 160)]); return ts.apply(this, arguments); }; })()"""
log = {'tips': [], 'arrows': [], 'acts': [], 'toasts': [], 'errors': []}
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME'), args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    pg = Page(ctx, BUILD)
    pg.ev('localStorage.clear()'); pg.ev('newGameStart(true)'); pg.step(5)
    pg.page.fill('form input[maxlength="24"]', 'Sam'); pg.page.click('form button'); pg.step(5)
    pg.ev(TIPS)
    print('start', pg.ev('clockText()'), 'intro on:', pg.ev("typeof introOn === 'function' && introOn()"), flush=True)
    f = Follower(pg); last_arrow = None
    for day in range(0, LAST + 1):
        end = day * 1440 + hm(SLEEP if not (day == LAST and os.environ.get('FW_UNTIL')) else os.environ['FW_UNTIL'])
        while pg.ev('shipNow()') < end:
            f.run(min(end, pg.ev('shipNow()') + 20))
            a = pg.ev("(() => { const g = goalNow(); return g ? g.label : null; })()")
            if a != last_arrow: log['arrows'].append((pg.ev('clockText()'), a)); last_arrow = a
            if os.environ.get('FW_TRACE'):                 # FW_TRACE: a JS expression, logged whenever its value changes
                v = pg.ev(os.environ['FW_TRACE'])
                if v != log.get('_tr'): log.setdefault('trace', []).append((pg.ev('clockText()'), v)); log['_tr'] = v; print('  TRACE', pg.ev('clockText()'), v, flush=True)
            for x in f.acts: log['acts'].append(x)
            f.acts.clear()
        t = pg.ev('window.__tips.splice(0)'); log['tips'] += t; log['toasts'] += pg.ev('window.__toasts.splice(0)')
        print(f'--- Day {day} done at', pg.ev('clockText()'), flush=True)
        for x in t: print('  TIP', x, flush=True)
        if day < LAST: f.night(day + 1); pg.ev('window.__tips = window.__tips || []')
    log['stuck'] = f.stuck; log['long'] = f.long; log['errors'] = pg.errors[:20] if hasattr(pg, 'errors') else []
    log['seen'] = pg.ev('Object.keys(SHIP.device.tipsSeen)')
    pg.page.screenshot(path=(OUT or '/tmp/fresh_walk') + '.png')
if OUT: json.dump(log, open(OUT, 'w'), indent=1)
print('stuck', log['stuck']); print('errors', log['errors'])
