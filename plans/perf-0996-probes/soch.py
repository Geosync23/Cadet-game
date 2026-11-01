exec(open('/tmp/pf/scripts/common.py').read())
from playwright.sync_api import sync_playwright
path=sys.argv[1]
with sync_playwright() as pw:
    g=Game(pw,path,390,844); g.page.evaluate(REALNOW)
    for d in [2,5,10,15,17,18,20,25,30,40,60]:
        r=g.ev(f"""(() => {{ skipTo({(d-1)*1440+10*60+5}); const h = Math.floor(shipNow() / 60) - 1;
          const a = window.__realNow(); socialHour(h); const b = window.__realNow();
          let K = 0; for (const it of NEWS) K += SHIP.knows[it.id] ? SHIP.knows[it.id].size : 0;
          return {{ d: {d}, ms: +(b - a).toFixed(1), news: NEWS.length, knowsTotal: K, heard: SHIP.heard.length, mail: (SHIP.mail || []).length, crew: SOC.n }}; }})()""")
        print(r, flush=True)
