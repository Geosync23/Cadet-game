# RV7: the week (Days 2-8) with arrows_check's follower, logging every toast, every job you take (kind), each
# training learned (when), and any board row with a Take it whose kind is a registered non-side kind other than rounds/haul.
# p_week.py BUILD [guide]
import sys, os, json
BUILD = sys.argv[1]; G = "guide" in sys.argv; sys.argv = [sys.argv[0], BUILD]
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.environ.get('ACHK', 'arrows_check.py'))).read().split("GUIDE = 'guide' in")[0]
exec(src); GUIDE = G
HOOK = r"""(() => { window.__tl = []; const t0 = toast; toast = function (a, b, o) { const r = t0.apply(this, arguments); try { if ((document.getElementById('tx').textContent || '') === String(b)) window.__tl.push([clockText(), Math.floor(shipNow()), String(a), String(b)]); } catch (e) {} return r; };
  window.__jobs = []; window.__new = []; window.__lastJ = null; })()"""
POLL = r"""(() => { const j = myJob(); const id = j ? j.id : null;
  if (id !== window.__lastJ) { if (j) window.__jobs.push([clockText(), Math.floor(shipNow()), j.kind, j.id, j.title || '']); window.__lastJ = id; }
  let L = []; try { L = openJobs('you'); } catch (e) {}
  for (const o of L) { const r = SHIP.jobs.find(x => x.id === o.id); if (!r) continue;
    const reg = JOB_KINDS[r.kind] && !JOB_KINDS[r.kind].side && !r.machine && r.kind !== 'rounds' && r.kind !== 'haul';
    if (reg && ixBoard.doable(r) && !window.__new.some(x => x[2] === r.id)) window.__new.push([clockText(), r.kind, r.id, r.title]); }
  const W = SHIP.works; return W ? JSON.stringify(W.tr) : null; })()"""
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    pg = Page(ctx, BUILD); real_game(pg, 2); pg.ev(HOOK)
    f = Follower(pg); tr_seen = {}
    for d in range(2, 9):
        end = (d - 1) * 1440 + 21 * 60 + 30
        while pg.ev('shipNow()') < end:
            f.run(min(end, pg.ev('shipNow()') + 6))
            tr = json.loads(pg.ev(POLL) or '{}')
            for k, v in tr.items():
                if k not in tr_seen: tr_seen[k] = (d, pg.ev('clockText()')); print(f'  learned {k} on Day {d} {tr_seen[k][1]}')
        f.night(d)
    tl = pg.ev('window.__tl'); jobs = pg.ev('window.__jobs'); new = pg.ev('window.__new')
    print('TRAINED TOASTS:'); [print('  ', t) for t in tl if 'Trained' in t[3] or 'Trained' in t[2]]
    print('REPUTATION TOASTS:'); [print('  ', t) for t in tl if 'reputation' in t[3]]
    print('BOARD WORD:'); [print('  ', t) for t in tl if 'Nothing on the board' in t[3]]
    print('JOBS TAKEN:'); [print('  ', j) for j in jobs]
    print('OTHER KINDS WITH TAKE IT:'); [print('  ', n) for n in new]
    print('learned:', tr_seen); print('stuck:', f.stuck); print('long:', f.long); print('errors:', pg.errors[:5])
    json.dump({'toasts': tl, 'jobs': jobs, 'new': new}, open(BUILD + ('.on' if G else '.off') + '.week.json', 'w'))
