# TR1: every tradition / event on Days 1-120 is on the device Calendar's list for its day (devTraditions), at its time
import sys, json
sys.argv, ARGS = sys.argv[:1], sys.argv[1:]
exec(open("/home/user/cadet-game/cadet_test.py").read().split("a, shots = run(")[0].replace("timeout=60000", "timeout=240000"))
with sync_playwright() as pw:
    g = Game(pw, ARGS[0], 600, 500)
    print(g.ev("""JSON.stringify((() => { const miss = [], bad = [], seen = new Set();
      for (let d = 1; d <= 120; d++) { const B0 = (d - 1) * 1440, cal = devTraditions(B0, B0 + 1439);
        for (const e of eventsOn(d)) { const c = cal.find(x => x.title === e.name || (x.title || '').includes(e.name) || x.id === e.id || x.key === e.id + '@' + d);
          if (!c) { if (!seen.has(e.id)) miss.push(d + ' ' + e.id + ' (' + e.name + ')'); seen.add(e.id); }
          else if (c.at !== B0 + e.from) bad.push(d + ' ' + e.id + ' cal ' + hhmm(c.at % 1440) + ' vs ' + hhmm(e.from)); } }
      return { missingFirst: miss, wrongTime: bad.slice(0, 20), sample: devTraditions(0, 1439).slice(0, 2) }; })())"""))
    g.close()
