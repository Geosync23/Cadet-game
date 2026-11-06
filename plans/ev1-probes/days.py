import sys
exec(open("/home/user/Cadet-game/cadet_test.py").read().split("a, shots = run(")[0])

from playwright.sync_api import sync_playwright
path = sys.argv[1]; days = [int(x) for x in sys.argv[2].split(',')]
with sync_playwright() as pw:
    g = Game(pw, path)
    for d in days:
        r = g.ev(f"""(() => {{ const hm = m => String(Math.floor(m/60)).padStart(2,'0')+':'+String(m%60).padStart(2,'0');
          const o = eventsOn({d}).map(e => hm(e.from)+'-'+hm(e.to)+' '+e.id+' @'+e.ev.where.map(w=>w.deck+(w.room?' '+w.room.source:' '+(w.pool||''))).join('/')+(e.ev.host?' host '+e.ev.host:''));
          const dr = EV_DROPPED.get({d}) || [];
          const ev = typeof eventOn==='function' ? JSON.stringify(eventOn({d})) : '';
          return 'Day {d} wd ' + (({d}-1)%7) + ' event ' + ev + '\\n  ' + o.join('\\n  ') + (dr.length ? '\\n  dropped: '+dr.join(', ') : ''); }})()""")
        print(r)
    print(g.errors[:5])
    g.close()
