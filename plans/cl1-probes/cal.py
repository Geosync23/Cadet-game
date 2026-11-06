import sys, json, os
os.chdir('/home/user/Cadet-game')
exec(open('cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
build=sys.argv[1]; lo,hi=int(sys.argv[2]),int(sys.argv[3]); extra=sys.argv[4] if len(sys.argv)>4 else ''
with sync_playwright() as pw:
    g=Game(pw,build)
    if extra: print(g.ev(extra))
    r=g.ev("""(()=>{const out=[];for(let d=%d;d<=%d;d++){const on=eventsOn(d);out.push(d+' '+WEEKDAYS[weekday(d)].slice(0,3)+': '+on.map(e=>e.id+' '+hhmm(e.from)+'-'+hhmm(e.to)+(TRAD_JOIN[e.id]?'*':'')+(e.names?'('+e.names+')':'')).join(' | ')+'  DROPPED '+(EV_DROPPED.get(d)||[]).join(','));}return out.join('\\n');})()"""%(lo,hi))
    print(r); print(g.errors[:5]); g.close()
