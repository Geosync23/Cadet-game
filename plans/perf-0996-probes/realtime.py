# a long real-time stretch on one deck: the mess, from Monday 07:00, sampled every ship hour; then a fresh page skipped to the same moment
exec(open('/tmp/pf/scripts/common.py').read())
from playwright.sync_api import sync_playwright
path=sys.argv[1]; HOURS=int(sys.argv[2]); OUT=sys.argv[3]; START=int(os.environ.get('START', str(7*60)))
PUT=r"""(() => { if (deckDef.num !== 3) goToDeck(3);
  const k = Object.keys(ROOM_BOX).find(k => ROOMS[k] && /^Mess/i.test(ROOMS[k].name)), b = ROOM_BOX[k], mid = cellPos(Math.floor((b.i0 + b.i1) / 2), Math.floor((b.j0 + b.j1) / 2));
  const at = nearestOpen(mid.x, mid.z, player); player.obj.position.copy(cellPos(...at)); target.copy(player.obj.position).setY(.7);
  camera.zoom = 1.5; camera.updateProjectionMatrix(); return true; })()"""
def sample(g, tag):
    r={'tag':tag}; r.update(g.page.evaluate("s => window.__sc(s)(20)", MEASURE_JS)); gc(g); r.update(g.ev(STATS_JS)); r['heap']=g.heapMB; r['lis']=g.ev(LIS_JS)
    r['bubbles']=g.ev("document.querySelectorAll('.bubble, [class*=bubble]').length")
    return r
rows=[]
with sync_playwright() as pw:
    g=Game(pw,path,390,844); g.page.evaluate(REALNOW)
    g.ev(f"skipTo({START})"); g.ev(PUT); g.step(90)
    rows.append(sample(g,'h0'))
    print(rows[-1], flush=True)
    for h in range(1,HOURS+1):
        t=time.time()
        for _ in range(10): g.step(300)   # one ship hour: 3000 frames at 30 a second
        g.ev("if (deckDef.num !== 3) 0"); 
        rows.append(sample(g,'h%d'%h)); rows[-1]['wall']=round(time.time()-t,1); json.dump(rows,open(OUT,'w'))
        r=rows[-1]; print(h,{k:r[k] for k in ('js','calls','crew','heap','objs','geo','tex','dom','timers','day','min','deck','bubbles','wall')}, r['lis']['add']-r['lis']['rem'], r['lis']['liveTO'], flush=True)
    now=g.ev("shipNow()"); place=g.ev("[deckDef.num, ...player.here()]"); g.close()
    g=Game(pw,path,390,844); g.page.evaluate(REALNOW)
    g.ev(f"skipTo({now})"); g.ev(PUT); g.step(90)
    rows.append(sample(g,'fresh-same-time')); json.dump(rows,open(OUT,'w')); print('fresh',rows[-1], flush=True)
