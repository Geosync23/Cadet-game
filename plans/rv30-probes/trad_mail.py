# RV30 probe (SW4's Mail rewording): the Mail the evening before Tap night, Talent night and Midtour, as the game sends it
# (eventsMail over the evening before each one's first day, read from EV_MAILBOX). Usage: trad_mail.py WORKTREE BUILD
import sys, os
wt = sys.argv[1]; os.chdir(wt)
exec(open('cadet_test.py').read().split('a, shots = run(')[0])
with sync_playwright() as pw:
    g = Game(pw, sys.argv[2]); g.step(10)
    print(g.ev("""(() => { const out = {}, want = ['tap-night', 'talent-night', 'midtour'];
      for (let d = 2; d < 420 && Object.keys(out).length < 3; d++) for (const e of eventsOn(d)) if (want.includes(e.id) && !out[e.id]) {
        const at = (d - 2) * 1440 + EV_MAIL_AT; EV_MAILBOX.length = 0; eventsMail(at - 1, at, true);
        const m = EV_MAILBOX.find(x => x.event === e.id + '@' + d); out[e.id] = m ? ['Day ' + d, m.from, m.subject, m.body] : ['Day ' + d, 'no Mail']; }
      return out; })()"""))
    print('errors', [e for e in g.errors if 'pageerror' in e][:3]); g.close()
