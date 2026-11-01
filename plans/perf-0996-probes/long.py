exec(open('/tmp/pf/scripts/common.py').read())
from playwright.sync_api import sync_playwright
path=sys.argv[1]; DAYS=int(sys.argv[2]); OUT=sys.argv[3]; PLAY=int(os.environ.get('PLAY','3000'))
SIZE_DAYS={1,2,5,10,15,20,25,30,35,40,45,50}
SCENE=r"""(d => { skipTo((d - 1) * 1440 + 10 * 60); if (deckDef.num !== 3) goToDeck(3);
  const k = Object.keys(ROOM_BOX).find(k => ROOMS[k] && /^Mess/i.test(ROOMS[k].name)), b = ROOM_BOX[k], mid = cellPos(Math.floor((b.i0 + b.i1) / 2), Math.floor((b.j0 + b.j1) / 2));
  const at = nearestOpen(mid.x, mid.z, player); player.obj.position.copy(cellPos(...at)); target.copy(player.obj.position).setY(.7);
  camera.zoom = 1.5; camera.updateProjectionMatrix(); return true; })"""
DRAWN=r"""(n => { window.__skip = false; const a = window.__realNow(); window.__step(n, 1000 / 30); return +((window.__realNow() - a) / n).toFixed(1); })"""
rows=[]
with sync_playwright() as pw:
    g=Game(pw,path,390,844); g.page.evaluate(REALNOW)
    decks=[3,4,5,1,2,6,7]
    for d in range(1,DAYS+1):
        t0=time.time()
        if d>1:
            g.ev(f"skipTo({(d-1)*1440+7*60+30})")
        # play: two decks, one ship hour each (real-time frames, drawing skipped)
        for k in range(2):
            dk=decks[(d*2+k)%len(decks)]
            g.ev(f"if (DECKS[{dk}]) goToDeck({dk})"); g.step(PLAY)
        g.page.evaluate(f"s => window.__sc(s)({d})", SCENE)
        g.step(90)
        r={'day':d}
        r.update(g.page.evaluate("s => window.__sc(s)(20)", MEASURE_JS))
        r['drawn']=g.page.evaluate("s => window.__sc(s)(5)", DRAWN)
        gc(g); r.update(g.ev(STATS_JS)); r['heap']=g.heapMB; r['lis']=g.ev(LIS_JS)
        sv=g.ev(SAVE_JS); r['save']=sv['len']; r['saveMs']=round(sv['msBase']+sv['msExtra']+sv['msJson'],1); r['saveParts']=sv['parts']
        r['ship']=g.ev(SHIPSIZE_JS)
        if d in SIZE_DAYS: r['sizes']=g.page.evaluate("([s, n]) => window.__sc(s)(n)", [SIZES_JS, NAMES])
        r['wall']=round(time.time()-t0,1)
        rows.append(r); json.dump(rows,open(OUT,'w'))
        print(d, {k:r[k] for k in ('js','drawn','calls','crew','heap','objs','geo','tex','dom','timers','save','saveMs','wall')}, r['lis']['add']-r['lis']['rem'], r['lis']['liveTO'], flush=True)
    open(OUT.replace('.json','.save.txt'),'w').write(g.ev("window.__lastSave"))
