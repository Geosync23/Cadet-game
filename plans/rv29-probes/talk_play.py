# RV29: PL2 note 12 in the real game: Dev jump (TALK_DAY, default 3) 12:35 in the mess hall, Talk a while with the nearest
# crew member (TALK_WHO to pick one) at real frame pace; logs the meter text, each line, the question, the end and the
# rewards (social, friendship points). usage: talk_play.py WORKTREE BUILD [N talks]
import sys, os, json
WT, BUILD = sys.argv[1], sys.argv[2]; NT = int(sys.argv[3]) if len(sys.argv) > 3 else 3
sys.argv = [sys.argv[0], BUILD]
src = open(WT + '/devmode_check.py').read().split("\ndef part_off")[0].replace("__file__.replace('devmode_check.py', 'cadet_test.py')", repr(WT + '/cadet_test.py'))
exec(src)
S = """(() => { const C = typeof CHAT !== 'undefined' ? CHAT : null, T = C && C.talk, m = document.querySelector('#chat .tmeter span, #chat [class*=meter] span');
  const el = document.getElementById('chat'), txt = el ? [...el.querySelectorAll('span')].map(s => s.textContent).find(s => /^(Talking|A good talk|You talked|Your turn)/.test(s)) : null;
  return { t: hhmm(SHIP.time.min), who: C && C.p && C.p.id, line: C && C.line && C.line.text, meter: txt || null, mins: T ? Math.round(T.mins * 10) / 10 : null, endAt: T ? T.endAt : null, u: T && T.u != null ? Math.round(T.u * 10) / 10 : null,
    ask: T ? !!T.ask : null, end: T ? T.end || null : null, pts: T ? Math.round(T.pts * 10) / 10 : null, gained: T ? Math.round(T.gained * 10) / 10 : null,
    buttons: el ? [...el.querySelectorAll('button')].map(b => b.textContent).slice(0, 5) : null }; })()"""
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get('CADET_CHROME'), args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    pg = Page(ctx, '#dev'); pg.sign(); pg.step(20)
    day = int(os.environ.get('TALK_DAY', '3'))
    print('jump', pg.ev(f"devmodeRun('Jump', () => devmodeSetCareerTo({day}, {{ id: 'rv29t', label: 'talk', day: {day}, by: {day - 1}, at: 755, where: {{ deck: 3, room: 'M' }} }}))")); pg.step(30)
    done = set()
    for n in range(NT):
        who = pg.ev("""((skip) => { const pp = player.obj.position, c = DECK_CREW.filter(a => a.p && !skip.includes(a.p.id) && !(SHIP.rel[a.p.id] && SHIP.rel[a.p.id].talkDay === SHIP.time.day)).map(a => [a, Math.hypot(a.x - pp.x, a.z - pp.z)]).sort((x, y) => x[1] - y[1])[0];
          if (!c) return null; const a = c[0], r0 = relGet(a.p.id).pts, s0 = SHIP.player.needs.social; chatOpen(a.p, false, null, { tap: true }); window.__t0 = [r0, s0]; return [a.p.id, Math.round(c[1]), r0, Math.round(s0)]; })""" + '(' + json.dumps(sorted(done)) + ')')
        if not who: print('nobody'); break
        done.add(who[0]); pg.step(10)
        print('TALK with', who, 'buttons', pg.ev(S)['buttons'])
        pg.ev("chatDo('talk')"); last = None
        for i in range(900):
            pg.step(6); s = pg.ev(S)
            key = (s['line'], s['meter'], s['ask'], s['end'])
            if key != last: print('  ', json.dumps(s)[:600]); last = key
            if s['ask']:
                pg.step(30); r = pg.ev("(() => { const b = [...document.querySelectorAll('#chat button')].find(x => !/Stop/.test(x.textContent)); if (b) { b.click(); return b.textContent; } return null; })()"); print('   reply', r)
            if s['end'] or s['who'] is None: break
        pg.step(60)
        print('  after', json.dumps(pg.ev(f"(() => ({{ pts: Math.round((relGet({json.dumps(who[0])}).pts - window.__t0[0]) * 10) / 10, social: Math.round((SHIP.player.needs.social - window.__t0[1]) * 10) / 10 }}))()")))
        pg.ev("chatClose && chatClose()"); pg.step(30)
    print('errors', pg.errors[:5]); b.close()
