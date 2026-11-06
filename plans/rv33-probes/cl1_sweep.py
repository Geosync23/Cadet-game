import sys
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    print(g.ev("""JSON.stringify((() => { const b = [], piano = [], pyo = [], run = [], store = [];
      for (let d = 1; d <= 70; d++) { const es = eventsOn(d);
        for (const e of es) { if (e.ev.when && e.ev.when.birthday) b.push(d + '(wd' + weekday(d) + ') ' + Math.floor(e.from/60) + ':' + String(e.from%60).padStart(2,'0') + ' ' + e.names);
          if (e.id === 'late-piano') piano.push(d); if (e.id === 'saturday-run') run.push(d); if (/store|swap/.test(e.id)) store.push(d + ':' + e.id);
          if (e.id === 'pick-your-own' && d <= 30) pyo.push(d + ':' + schedPeople().filter(p => planDay(p, d).some(s => evTagId(s.tag) === e.id)).map(p => p.id.split('-')[0]).join('/')); } }
      const consec = piano.filter((d, i) => i && piano[i-1] === d - 1);
      return { birthdays: b, piano, pianoBackToBack: consec, pyo, saturdayRun: run, store }; })())"""))
