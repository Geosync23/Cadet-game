import os,sys,json
os.environ.setdefault('CADET_CHROME','/opt/pw-browsers/chromium')
os.environ['CADET_WORK']='/tmp/cw-er2'
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0])
H=open('play.py').read().split('H="""')[1].split('"""')[0]
with sync_playwright() as pw:
    g=Game(pw, sys.argv[1], w=390, h=844); g.ev(H)
    at=lambda d,m:(d-1)*1440+m
    def go(d,m,deck): g.ev(f"skipTo({at(d,m)})"); g.ev(f"goToDeck({deck})"); g.step(10)
    def run(n=150):
        for i in range(n//30): g.step(30)
    # Saturday fix branch, no Friday moment
    go(13,15*60+5,3); g.ev("__near('dlamini-lukas')"); run(150)
    print('dlg', g.ev("DIALOGUE && DIALOGUE.id")); g.ev("__dlg(0)")
    print('jobs', g.ev("JSON.stringify((SHIP.jobs||[]).filter(j=>j.event==='ionStorm').map(j=>[j.eventJob||j.id,j.status,j.claimedBy,j.reserved||'',hhmm(j.posted%1440)]))"))
    print('flags', g.ev("[flag('storm.lukas.fixed'), flag('storm.lukas.promised')]"))
    # Sunday all-clear and party
    go(14,10*60+20,1); print('mine14', g.ev("JSON.stringify(Object.keys(SHIP.event?SHIP.event.mine:{}))"), 'phase', g.ev("SHIP.event && SHIP.event.phase"))
    print('mail', g.ev("JSON.stringify((typeof MAIL!=='undefined'?MAIL:(SHIP.mail||[])).slice(-8).map(m=>(m.subject||m.title||'')+' @'+(m.at!=null?hhmm(m.at%1440):'')))"))
    go(14,19*60+40,3); g.ev("player.obj.position.copy(cellPos(44,10)); target.copy(player.obj.position).setY(.7)"); run(60)
    print('party at once', g.ev("(() => { const t=shipNow(); let n=0; for (const p of schedPeople()) { const w=whereIs(p,t); if (w && /^ev-party/.test(w.tag||'') && !w.moving) n++; } return n; })()"), 'calls', g.ev("renderer.info.render.calls"))
    go(15,18*60+10,3); print('mail15', g.ev("JSON.stringify((typeof MAIL!=='undefined'?MAIL:(SHIP.mail||[])).slice(-5).map(m=>(m.subject||m.title||'')))"))
    print('on15', g.ev("JSON.stringify(eventsOn(15).map(e=>e.id+' '+hhmm(e.from)))"), 'on14', g.ev("JSON.stringify(eventsOn(14).map(e=>e.id+' '+hhmm(e.from)))"))
    go(16,1,3); print('event after', g.ev("JSON.stringify(SHIP.event)"), 'log', g.ev("JSON.stringify(SHIP.eventLog.map(l=>[l.id,l.band||l.result]))"))
    print('errors', g.errors[:5]); g.close()
