# the late game three ways, at the same moment and place: a fresh page skipped there (nosave), and a page reloaded from the long run's save
exec(open('/tmp/pf/scripts/common.py').read())
from playwright.sync_api import sync_playwright
path=sys.argv[1]; savef=sys.argv[2]; OUT=sys.argv[3]
SAVE=open(savef).read(); sv=json.loads(SAVE); D=sv['time']['day']
PUT=r"""(() => { if (deckDef.num !== 3) goToDeck(3);
  const k = Object.keys(ROOM_BOX).find(k => ROOMS[k] && /^Mess/i.test(ROOMS[k].name)), b = ROOM_BOX[k], mid = cellPos(Math.floor((b.i0 + b.i1) / 2), Math.floor((b.j0 + b.j1) / 2));
  const at = nearestOpen(mid.x, mid.z, player); player.obj.position.copy(cellPos(...at)); target.copy(player.obj.position).setY(.7);
  camera.zoom = 1.5; camera.updateProjectionMatrix(); return true; })()"""
def sample(g, tag):
    r={'tag':tag}; r.update(g.page.evaluate("s => window.__sc(s)(20)", MEASURE_JS)); gc(g); r.update(g.ev(STATS_JS)); r['heap']=g.heapMB
    s=g.ev(SAVE_JS); r['save']=s['len']; r['saveMs']=round(s['msBase']+s['msExtra']+s['msJson'],1); return r
rows=[]
with sync_playwright() as pw:
    for rep in range(2):
        # A: fresh, skipped straight to the save's moment (state built in one jump)
        g=Game(pw,path,390,844); g.page.evaluate(REALNOW)
        g.ev(f"skipTo({(D-1)*1440+10*60})"); g.ev(PUT); g.step(90); rows.append(sample(g,'fresh-skip day %d'%D)); print(rows[-1],flush=True)
        # B: the long run's save, loaded
        g.ev(f"localStorage.setItem('starship-cadet-save', {json.dumps(SAVE)}); localStorage.setItem('starship-cadet-save-slot','1')")
        g.page.goto('file://' + str(g.tmp) + '?debug'); g.page.wait_for_function('window.__sc !== undefined', timeout=90000)
        g.page.evaluate(REALNOW); g.step(30)
        print('loaded day', g.ev("SHIP.time.day + ' ' + Math.round(SHIP.time.min)"))
        g.ev(f"localStorage.clear()")
        g.ev(f"skipTo({(D-1)*1440+10*60})"); g.ev(PUT); g.step(90); rows.append(sample(g,'reload-from-save day %d'%D)); print(rows[-1],flush=True)
        g.close()
    json.dump(rows,open(OUT,'w'))
