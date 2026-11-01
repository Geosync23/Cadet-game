# a steady player's career (Dev mode's Set career) to Day N, against a fresh Day 1, the same scene; then the page reloaded from the save
exec(open('/tmp/pf/scripts/common.py').read())
from playwright.sync_api import sync_playwright
path=sys.argv[1]; N=int(sys.argv[2]); OUT=sys.argv[3]
SCENE=open('/tmp/pf/scripts/long.py').read().split('SCENE=r"""')[1].split('"""')[0]
FRAMES=open('/tmp/pf/scripts/long2.py').read().split('FRAMES=r"""')[1].split('"""')[0]
SAVET=r"""(() => { const a = window.__realNow(); saveGame(); const b = window.__realNow(); const s = localStorage.getItem(SAVE_KEY) || ''; return { ms: +(b - a).toFixed(2), kb: +(s.length / 1024).toFixed(1), key: SAVE_KEY }; })()"""
def sample(g, tag, d):
    g.page.evaluate(f"s => window.__sc(s)({d})", SCENE); g.step(90)
    r={'tag':tag}; r.update(g.page.evaluate("s => window.__sc(s)(20)", MEASURE_JS))
    r['f']=g.page.evaluate("s => window.__sc(s)(3000)", FRAMES)
    gc(g); r.update(g.ev(STATS_JS)); r['heap']=g.heapMB
    r['save']=[g.ev(SAVET) for _ in range(3)]
    r['career']=g.ev("({ rank: SHIP.works && SHIP.works.rank, band: SHIP.works && SHIP.works.band, jobsDone: (SHIP.jobs || []).filter(j => j.doneBy === 'you').length, cases: SHIP.cases ? JSON.stringify(SHIP.cases).length : null })")
    f=r['f']; print(tag, {k:r[k] for k in ('js','jsAll','crew','heap','objs','geo','day','min','career')}, {k:f[k] for k in ('mean','p99','max','over8','over16')}, 'hour', f['hour'], 'save', r['save'], flush=True)
    return r
rows=[]
with sync_playwright() as pw:
    global URL_SUFFIX
    URL_SUFFIX='#dev.debug'
    g=GameU(pw,path,390,844); g.page.evaluate(REALNOW)
    print('DEVMODE', g.ev("DEVMODE"), flush=True)
    t=time.time(); print(g.ev("devmodeSetCareerTo(1)")[:120]); rows.append(sample(g,'career Day 1',1))
    t=time.time(); msg=g.ev(f"devmodeSetCareerTo({N})"); print('set career', round(time.time()-t), 's:', msg[:200], flush=True)
    rows.append(sample(g,f'career Day {N}',N)); json.dump(rows,open(OUT,'w'))
    g.ev("saveGame()")
    g.page.goto('file://' + str(g.tmp) + '#dev.debug'); g.page.reload(); g.page.wait_for_function('window.__sc !== undefined', timeout=120000); g.page.evaluate(REALNOW)
    print('reloaded at', g.ev("clockText()"), flush=True)
    rows.append(sample(g,f'reloaded Day {N}',N)); json.dump(rows,open(OUT,'w'))
