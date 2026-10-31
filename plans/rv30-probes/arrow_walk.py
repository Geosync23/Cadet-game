# RV30 probe (0.99.5 round, arrows_check week FAILs): arrows_check's own walker (Follower, FOLLOW) from a set career day, with
# its every action and the arrow logged, plus what a real tap does. Usage (from a worktree): arrow_walk.py WORKTREE BUILD DAY
# FROM_HHMM TO_HHMM [realtap]: 'realtap' makes a crew arrow's step a real screen tap on that person (tapCrew), not chatOpen.
import sys, os
WT, BUILD, DAY, FR, TO = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5]; REAL = 'realtap' in sys.argv[6:]
src = open(WT + '/arrows_check.py').read().split('\nwith sync_playwright() as pw:')[0]
sys.argv = [sys.argv[0], BUILD]
exec(src)
if REAL:
    FOLLOW = FOLLOW.replace("chatOpen(a.p); return 'talk to: ' + a.p.id; }", "const v = new THREE.Vector3(a.x, 1.2, a.z).project(camera); return { click: [(v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight], label: 'real tap on ' + a.p.id }; }")
    assert 'real tap on' in FOLLOW
hm = lambda s: int(s[:2]) * 60 + int(s[3:])
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME'), args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 900, 'height': 760}, device_scale_factor=1)
    pg = Page(ctx, BUILD); real_game(pg, DAY); f = Follower(pg)
    f.run((DAY - 1) * 1440 + hm(FR)); f.acts.clear()
    if os.environ.get('AW_PRE'): print('pre', pg.ev(open(os.environ['AW_PRE']).read()))   # JS run once at FROM (e.g. hand you a job)
    t0 = (DAY - 1) * 1440 + hm(FR); last = None
    while pg.ev('shipNow()') < (DAY - 1) * 1440 + hm(TO):
        f.run(pg.ev('shipNow()') + 3)
        s = pg.ev("""(() => { const g = goalNow(), j = (() => { try { return myJob(); } catch (e) { return null; } })();
          return [clockText(), g ? g.label : null, g ? (g.crew || g.place || (g.item && String(g.item)) || '') : '', deckDef.num, player.here().join(','), ACT ? ACT.kind : null, DIALOGUE ? DIALOGUE.id : null,
            typeof CHAT !== 'undefined' && CHAT ? 'chat' : null, j ? [j.id, j.status, !!j.workDone] : null, (SHIP.events.joined || []).slice(-2)]; })()""")
        key = str(s[1:9])
        if key != last: print(s, '| acts:', [a[1] for a in f.acts[-3:]]); last = key
        f.acts.clear()
    print('stuck', f.stuck, 'long', f.long, 'errors', pg.errors[:3]); b.close()
