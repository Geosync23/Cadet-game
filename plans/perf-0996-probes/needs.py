exec(open('/tmp/pf/scripts/common.py').read())
from playwright.sync_api import sync_playwright
path=sys.argv[1]
with sync_playwright() as pw:
    g=Game(pw,path,390,844); g.page.evaluate(REALNOW)
    g.ev(f"skipTo({17*1440+9*60+10})")
    print(g.ev("""(() => { const P = schedPeople().slice(0, 40), t = shipNow(); const W = {};
      const wrap = n => { const f = eval(n); try { eval(n + ' = function (...a) { const s = window.__realNow(); try { return f.apply(this, a); } finally { W[n] = (W[n] || 0) + window.__realNow() - s; } }'); } catch (e) { W[n + ' (const, not timed)'] = 0; } return f; };
      const o = ['planDay', 'shipEffectsAt', 'evAt'].map(n => [n, wrap(n)]);
      const a = window.__realNow(); for (const p of P) crewNeeds(p, t); const tot = window.__realNow() - a;
      for (const [n, f] of o) try { eval(n + ' = f'); } catch (e) {}
      let segs = 0; const d1 = Math.floor(t / 1440) + 1; for (const p of P) for (let d = d1 - 7; d <= d1; d++) segs += planDay(p, d).length;
      return { people: P.length, totalMs: +tot.toFixed(1), perCall: +(tot / P.length).toFixed(2), parts: Object.fromEntries(Object.entries(W).map(([k, v]) => [k, +v.toFixed(1)])), segsPerPerson: segs / P.length }; })()"""))
