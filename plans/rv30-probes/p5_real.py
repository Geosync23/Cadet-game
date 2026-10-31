# RV30 probe (0.99.5 round, puzzle_check p5's first): the real game (Dev mode) with the career set to Day 17's end and then
# played on (the clock runs) to Day 18 16:00: does p5 ("Follow the line") open and its first case get staged and shown?
# Also counts head-scratcher cases offered/posted in Days 17-18. Usage: p5_real.py WORKTREE BUILD
import sys, os, json
WT, BUILD = sys.argv[1], sys.argv[2]; sys.argv = [sys.argv[0], BUILD]
src = open(WT + '/devmode_check.py').read().split("\ndef part_off")[0].replace("__file__.replace('devmode_check.py', 'cadet_test.py')", repr(WT + '/cadet_test.py'))
exec(src)
S = """(() => { const W = SHIP.works, C = caseState(), id = flag('case.p5.first'), c = id && id !== 'none' ? caseById(id) : null;
  return { t: clockText(), rank: W && W.rank, tr18: W && W.tr && W.tr.m18, p5op: W && Object.entries(W.op || {}).filter(([d, l]) => (l || []).includes('p5')).map(([d]) => +d), p5tr: W && W.tr && W.tr.p5,
    flag: id === undefined ? null : id, shown: c ? !c.wait : null, open: C ? C.open.map(x => x.id) : null, stats: { ...CASE_STATS, why: undefined } }; })()"""
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME'), args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    pg = Page(ctx, '#dev'); pg.sign(); pg.step(20)
    print('set', pg.ev("devmodeRun('Set career', () => devmodeSetCareerTo(17))")); pg.step(20)
    print(json.dumps(pg.ev(S)))
    for hm in [6 * 60, 9 * 60, 12 * 60, 16 * 60]:
        pg.ev(f"devmodeSkipTo({17 * 1440 + hm})"); pg.step(30); print(json.dumps(pg.ev(S)))
    print('errors', pg.errors[:3]); b.close()
