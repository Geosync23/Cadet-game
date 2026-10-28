from pp import *
g = start('?nosave&debug')
for d in range(0, 9):
    r = g.ev(f"""(() => {{ try {{ return eventsOn({d}).map(e => [e.id || e.key, e.name || e.title, e.at != null ? hhmm(e.at) : (e.from!=null?hhmm(e.from):''), e.until!=null?hhmm(e.until):(e.to!=null?hhmm(e.to):''), e.share, e.deck, (e.where&&e.where.room)||e.room||'']); }} catch (x) {{ return String(x); }} }})()""")
    print(d, r)
print(g.ev("Object.keys(eventsOn(1)[0]||{})"))
g.close()
