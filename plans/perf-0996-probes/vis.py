# the visual trade-offs: for each scene and variant, the picture at 390x844 on a 3x screen and the drawing time
# (renderer.render + gl.finish, SwiftShader: a stand-in for the graphics chip's work, compare variants only)
exec(open('/tmp/pf/scripts/common.py').read())
from playwright.sync_api import sync_playwright
path=sys.argv[1]; OUTD=sys.argv[2]; os.makedirs(OUTD, exist_ok=True)
pc=open('/home/user/Cadet-game/perf_check.py').read()
SCENE_JS=pc.split('SCENE_JS = r"""')[1].split('"""')[0]
SCENES_ALL=[('dinner', {'name':'Sunday dinner, the mess 18:30','day':7,'time':'18:30','deck':3,'room':r'^Mess'}),
        ('address', {'name':"Captain's address, auditorium Fri 16:10",'day':5,'time':'16:10','deck':7,'room':r'^Auditorium$','cells':True}),
        ('lounge', {'name':'quiz night, bow lounge 20:30','day':4,'time':'20:30','deck':3,'room':r'^Bow lounge$'})]
VARS_ALL=[('base',''),('pr15','&pfpr'),('sh1024','&pfsh'),('hard','&pfhard'),('noaa','&pfaa'),('all3','&pfpr&pfsh&pfhard')]
VARS=[v for v in VARS_ALL if len(sys.argv)<=3 or v[0] in sys.argv[3].split(',')]
if len(sys.argv)>4: VARS=VARS+[(v[0]+'_2',v[1]) for v in VARS]
SCENES=[x for x in SCENES_ALL if not os.environ.get('ONLY') or x[0]==os.environ['ONLY']]
DRAW=r"""(n => { const gl = renderer.getContext(), px = new Uint8Array(4), sync = () => gl.readPixels(0, 0, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, px); window.__skip = false; const T = [];
  for (let k = 0; k < n; k++) { window.__step(1, 1000 / 30); sync(); }
  const rr = renderer.render.bind(renderer);
  for (let k = 0; k < n; k++) { sync(); const a = window.__realNow(); rr(scene, camera); sync(); T.push(window.__realNow() - a); }
  T.sort((a, b) => a - b); return { med: +T[n >> 1].toFixed(1), min: +T[0].toFixed(1), pr: renderer.getPixelRatio(), map: sun.shadow.mapSize.x, type: renderer.shadowMap.type, aa: renderer.getContextAttributes().antialias, calls: renderer.info.render.calls, px: renderer.domElement.width + 'x' + renderer.domElement.height }; })"""
res={}
global DSF, EXTRA_Q
with sync_playwright() as pw:
    for sname, sc in SCENES:
        for vname, q in VARS:
            DSF=3; EXTRA_Q=q
            g=GameQ(pw,path,390,844)
            g.page.evaluate(REALNOW)
            r=g.page.evaluate(f"s => window.__sc(s)({json.dumps(sc)})", SCENE_JS)
            g.ev("camera.zoom = 1.5; camera.updateProjectionMatrix()"); g.step(90)
            g.shot(f'{OUTD}/{sname}-{vname}.png')
            d=g.page.evaluate("s => window.__sc(s)(7)", DRAW)
            d['room']=r.get('room'); d['crew']=g.ev("crowd.stats().people"); res[sname+'/'+vname]=d
            print(sname, vname, d, flush=True); g.close()
json.dump(res, open(f'{OUTD}/times.json','w'), indent=1)
