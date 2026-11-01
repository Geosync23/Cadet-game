# time every frame across a ship hour change at day D, hour H (fresh page, the mess); profile the slowest frame's hour
exec(open('/tmp/pf/scripts/common.py').read())
from playwright.sync_api import sync_playwright
path=sys.argv[1]; D=int(sys.argv[2]); H=int(sys.argv[3]); PROF=len(sys.argv)>4
SCENE=open('/tmp/pf/scripts/long.py').read().split('SCENE=r"""')[1].split('"""')[0].replace("10 * 60", str(H-1)+" * 60 + 58")
FR=r"""(n => { window.__skip = true; const out = []; for (let k = 0; k < n; k++) { const t0 = SHIP.time.min, a = window.__realNow(); window.__step(1, 1000 / 30); const v = window.__realNow() - a; if (v > 15) out.push([k, hhmm(t0), +v.toFixed(1)]); } window.__skip = false; return out; })"""
with sync_playwright() as pw:
    g=Game(pw,path,390,844); g.page.evaluate(REALNOW)
    g.page.evaluate(f"s => window.__sc(s)({D})", SCENE); g.step(30)
    if PROF:
        c=g.page.context.new_cdp_session(g.page); c.send('Profiler.enable'); c.send('Profiler.setSamplingInterval',{'interval':100}); c.send('Profiler.start')
    print(g.page.evaluate("s => window.__sc(s)(250)", FR))
    if PROF:
        p=c.send('Profiler.stop')['profile']; json.dump(p,open('/tmp/pf/spike.cpuprofile','w'))
        nodes={n['id']:n for n in p['nodes']}; self_={}
        dt=p['timeDeltas']; 
        for s,d in zip(p['samples'],dt): self_[s]=self_.get(s,0)+d
        agg={}
        for i,t in self_.items():
            n=nodes[i]['callFrame']; k=n['functionName']+':'+str(n['lineNumber']); agg[k]=agg.get(k,0)+t
        for k,v in sorted(agg.items(),key=lambda x:-x[1])[:25]: print(round(v/1000,1),'ms',k)
