# RV30 probe (OB2 note 11): what each appointment says in the Appointments app (Coming up), the Calendar and the
# Schedule: an accepted tradition invitation (socialInvite { trad }), the Captain's table (an occasion's apptAdd),
# a meet-up you booked, and Rina's health check. Usage: appt_views.py WORKTREE BUILD
import sys, os, json
wt = sys.argv[1]; os.chdir(wt)
exec(open('cadet_test.py').read().split('a, shots = run(')[0])
VIEW = """(id => { const a = DEVICE_APPS.get(id), v = a.view(); const out = [];
  const walk = bs => (bs || []).forEach(b => { if (b.kind === 'list') b.rows.forEach(r => out.push(r.text + (r.sub ? ' | ' + r.sub : ''))); else if (b.text) out.push('# ' + b.text); if (b.blocks) walk(b.blocks); });
  walk(v.blocks); return out; })"""
with sync_playwright() as pw:
    g = Game(pw, sys.argv[2]); g.step(20)
    print(g.ev("""(() => { const D = SHIP.device, d = SHIP.time.day, B = (d - 1) * 1440; socInit(); const out = {};
      // a tradition invitation, accepted: the first tradition anyone goes to in the next 3 days
      for (let k = 0; k < 4 && !out.inv; k++) for (const t of TRADITIONS) for (const p of SOC.crew) { const id = socialInvite({ trad: t.id, day: d + k, from: p.id }); if (id) { const a = D.appts.find(x => x.id === id) || D.appts[D.appts.length - 1]; a.status = 'yes'; out.inv = [t.name, p.name, hhmm(a.at % 1440), 'D' + (d + k)]; break; } if (out.inv) break; }
      const pl = apptPlaces()[0]; const m = apptAdd({ with: ['torres-zeke'], at: B + 1440 + 19 * 60, len: 30, where: pl.id, kind: 'social' }); out.meet = !!m;
      introHealthAppt(B + 1440 + 14 * 60); return out; })()"""))
    for app in ['appointments', 'calendar']:
        print('==', app); [print('  ', x[:170]) for x in g.ev(f"({VIEW})('{app}')")]
    print('== schedule (devDay) tomorrow'); [print('  ', x) for x in g.ev("devDay(SHIP.time.day + 1).filter(x => x.kind === 'appt' || x.kind === 'tradition').map(x => hhmm(x.from) + ' ' + x.title + ' | ' + x.kind)")]
    print('errors', [e for e in g.errors if 'pageerror' in e][:3]); g.close()
