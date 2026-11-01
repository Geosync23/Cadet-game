# 40 ship days; each day: the night skip timed, two decks played an hour each (deck changes timed), then in the mess
# 10:00-11:00 every frame timed one by one (drawing skipped): p50, p99, max, frames over 8/16 ms; the hour's autosave timed
exec(open('/tmp/pf/scripts/common.py').read())
from playwright.sync_api import sync_playwright
path=sys.argv[1]; DAYS=int(sys.argv[2]); OUT=sys.argv[3]
SCENE=open('/tmp/pf/scripts/long.py').read().split('SCENE=r"""')[1].split('"""')[0]
FRAMES=r"""(n => { window.__skip = true; const T = new Float64Array(n), tag = [];
  for (let k = 0; k < n; k++) { const m0 = Math.floor(SHIP.time.min), h0 = Math.floor(shipNow() / 60), a = window.__realNow(); window.__step(1, 1000 / 30); T[k] = window.__realNow() - a;
    if (Math.floor(shipNow() / 60) !== h0) tag.push(['hour', k, +T[k].toFixed(2)]); }
  window.__skip = false; const s = [...T].sort((a, b) => a - b), q = p => +s[Math.min(n - 1, Math.floor(p * n))].toFixed(2);
  const top = [...T].map((v, k) => [k, +v.toFixed(1)]).sort((a, b) => b[1] - a[1]).slice(0, 6);
  return { p50: q(.5), p90: q(.9), p99: q(.99), max: q(1), mean: +(T.reduce((a, b) => a + b, 0) / n).toFixed(3), over8: s.filter(v => v > 8).length, over16: s.filter(v => v > 16).length, hour: tag, top };
})"""
SAVEFULL=r"""(() => { const a = window.__realNow(); const NS = window.__lastSaveLen; """ + SAVE_JS.split('const a = window.__realNow();')[1].rsplit('})()',1)[0].replace("return {","const e0 = window.__realNow(); localStorage.setItem('pf-test', s); const e1 = window.__realNow(); JSON.parse(s); const e2 = window.__realNow(); localStorage.removeItem('pf-test'); return { msSet: +(e1 - e0).toFixed(2), msParse: +(e2 - e1).toFixed(2),") + "})()"
rows=[]
with sync_playwright() as pw:
    g=Game(pw,path,390,844); g.page.evaluate(REALNOW); decks=[3,4,5,1,2,6,7]
    for d in range(1,DAYS+1):
        r={'day':d}
        if d>1:
            r['skipMs']=g.ev(f"(() => {{ const a = window.__realNow(); skipTo({(d-1)*1440+7*60+30}); return +(window.__realNow() - a).toFixed(1); }})()")
        r['deckMs']=[]
        for k in range(2):
            dk=decks[(d*2+k)%len(decks)]
            r['deckMs'].append(g.ev(f"(() => {{ if (!DECKS[{dk}] || deckDef.num === {dk}) return null; const a = window.__realNow(); goToDeck({dk}); return [{dk}, +(window.__realNow() - a).toFixed(0)]; }})()"))
            g.step(3000)
        g.page.evaluate(f"s => window.__sc(s)({d})", SCENE); g.step(60)
        r['f']=g.page.evaluate("s => window.__sc(s)(3000)", FRAMES)
        sv=g.ev(SAVEFULL); r['save']=sv['len']; r['saveMs']=[sv['msBase'],sv['msExtra'],sv['msJson'],sv['msSet'],sv['msParse']]
        r['crew']=g.ev("crowd.stats().people")
        rows.append(r); json.dump(rows,open(OUT,'w'))
        f=r['f']; print(d, r.get('skipMs'), r['deckMs'], 'crew',r['crew'], {k:f[k] for k in ('mean','p50','p99','max','over8','over16')}, 'hour',f['hour'], 'save',r['save'],r['saveMs'], flush=True)
