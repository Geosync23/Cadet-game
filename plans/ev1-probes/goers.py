import sys
exec(open("/home/user/Cadet-game/cadet_test.py").read().split("a, shots = run(")[0])
path, tid, days = sys.argv[1], sys.argv[2], [int(x) for x in sys.argv[3].split(',')]
with sync_playwright() as pw:
    g = Game(pw, path)
    for d in days:
        print(d, g.ev(f"""(() => {{ const e = eventsOn({d}).find(x => x.id === '{tid}'); if (!e) return 'none';
          const s = evGoers(e, {d}); return [...s].map(id => {{ const p = schedPeople().find(q=>q.id===id); return id + '(' + (p.habits||[]).join('/') + ')'; }}).join(' '); }})()"""))
    g.close()
