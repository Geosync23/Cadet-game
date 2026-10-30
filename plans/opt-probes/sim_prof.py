# Per-frame game-code cost by section: Sunday dinner in the mess (real main loop, drawing skipped) and
# one ship day of Deck 3's crew logic the way day_check drives it; plus skipTo over a day.
import sys, os, re, json, time, collections, subprocess
src = open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0]
exec(src)
pc = open('/home/user/Cadet-game/perf_check.py').read()
SCENE_JS = re.search(r'SCENE_JS = r"""(.*?)"""', pc, re.S)[1]
DAYSIM = re.search(r'SIM = r"""(.*?)"""', open('/home/user/Cadet-game/day_check.py').read(), re.S)[1]
from playwright.sync_api import sync_playwright
sec = subprocess.run(['python3', '/home/user/Cadet-game/tools/section.py'], capture_output=True, text=True, cwd='/home/user/Cadet-game').stdout
SECS = [(int(m[2]), int(m[3]), m[1]) for m in (re.match(r'\s*(\S+)\s+(\d+)-(\d+)', l) for l in sec.splitlines()) if m]
def secOf(line):
    for a, b, n in SECS:
        if a <= line <= b: return n
    return '?'
LOOPF = ['updateSteer', 'playerUpdate', 'updateDeckCrew', 'update', 'simTimers', 'shadowStep', 'writeWalls', 'updateRide', 'applyLight', 'doorLeavesSync', 'tallSync', 'lamps', 'shipFeelFrame', 'drawScreen', 'tickShip', 'galleyTick', 'worksTick', 'eventsTick', 'socialTick', 'introTick', 'worksCareerTick', 'discFrame', 'place', 'crewNearDoor', 'roomAt', 'recShowTick', 'linesTick', 'findPath', 'rebuild', 'updateMatrixWorld', 'schedBuild', 'shipDay', 'planDay']
def report(prof, title, frames=None):
    nodes = {n['id']: n for n in prof['nodes']}; parent = {}
    for n in prof['nodes']:
        for c in n.get('children', []): parent[c] = n['id']
    dt = collections.Counter()
    for sid, d in zip(prof['samples'], prof['timeDeltas']): dt[sid] += d
    tot = sum(dt.values()); selfsec = collections.Counter(); incl = collections.Counter(); special = collections.Counter(); fn = collections.Counter()
    for nid, us in dt.items():
        cf = nodes[nid]['callFrame']
        if '_run_g0647.html' in cf['url']: s = secOf(cf['lineNumber'] + 1); selfsec[s] += us; fn[f"{cf['functionName'] or '(anon)'}@{cf['lineNumber']+1} [{s}]"] += us
        elif 'three' in cf['url']: selfsec['three.js'] += us
        else: special[cf['functionName'] or '?'] += us
        seen = set(); x = nid
        while x in nodes:
            f = nodes[x]['callFrame']; key = f['functionName']
            if '_run_g0647.html' in f['url'] and key in LOOPF:
                key = f"{key}@{f['lineNumber']+1}[{secOf(f['lineNumber']+1)}]"
                if key not in seen: seen.add(key); incl[key] += us
            x = parent.get(x)
    per = (lambda us: f'{us/1e3/frames:.3f} ms/frame') if frames else (lambda us: f'{us/1e3:.0f} ms')
    print(f'\n### {title}: profile {tot/1e6:.2f} s' + (f', {frames} frames' if frames else ''))
    print('self time by section:'); [print(f'  {k:10} {per(v)}  {100*v/tot:.1f}%') for k, v in (selfsec + special).most_common(16)]
    print('inclusive, main-loop parts:'); [print(f'  {k:40} {per(v)}') for k, v in incl.most_common(22)]
    print('top functions (self):'); [print(f'  {per(v):18} {k}') for k, v in fn.most_common(18)]
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844)
    cdp = g.page.context.new_cdp_session(g.page); cdp.send('Profiler.enable'); cdp.send('Profiler.setSamplingInterval', {'interval': 250})
    r = g.page.evaluate("s => window.__sc(s)({name:'dinner', day:7, time:'18:30', deck:3, room:'^Mess'})", SCENE_JS)
    g.ev("camera.zoom = 1.5; camera.updateProjectionMatrix()"); g.step(90)
    print('crew on deck', g.ev('crowd.stats().people'))
    N = 900
    cdp.send('Profiler.start'); t = time.time(); g.page.evaluate(f'window.__skip = true; window.__step({N}, 1000/30); window.__skip = false'); el = time.time() - t
    report(cdp.send('Profiler.stop')['profile'], f'Sunday dinner, mess, {N} frames sim only (wall {el:.1f} s = {1000*el/N:.2f} ms/frame with profiler)', N)
    g.close()
    g = Game(pw, sys.argv[1])
    cdp = g.page.context.new_cdp_session(g.page); cdp.send('Profiler.enable'); cdp.send('Profiler.setSamplingInterval', {'interval': 500})
    t = time.time(); cdp.send('Profiler.start'); g.ev('skipTo(1440 * 8)'); el = time.time() - t
    report(cdp.send('Profiler.stop')['profile'], f'skipTo 8 ship days on paper (wall {el:.1f} s)')
    g.ev("window.__realTick = tickShip; tickShip = () => {}"); g.ev("player.steer = null; player.stop()")
    t = time.time(); cdp.send('Profiler.start')
    out = g.page.evaluate("s => window.__sc(s)({ n: 3, day: 9, step: 0.05, draw: true })", DAYSIM); el = time.time() - t
    report(cdp.send('Profiler.stop')['profile'], f"day_check's crew logic, Deck 3, one ship day (wall {el:.1f} s, peak crew {out['peakCrew']})")
    g.close()
