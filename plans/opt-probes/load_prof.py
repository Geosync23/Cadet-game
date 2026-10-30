# Load profile: wall times, CPU self time by section, inclusive time of the main load steps, trace phases.
import sys, os, re, json, time, subprocess, collections
sys.path.insert(0, '/home/user/Cadet-game')
src = open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0]
exec(src)
GAME = sys.argv[1]; W_, H_ = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (390, 844)
sec = subprocess.run(['python3', '/home/user/Cadet-game/tools/section.py'], capture_output=True, text=True, cwd='/home/user/Cadet-game').stdout
SECS = []
for l in sec.splitlines():
    m = re.match(r'\s*(\S+)\s+(\d+)-(\d+)', l)
    if m: SECS.append((int(m[2]), int(m[3]), m[1]))
def secOf(line):
    for a, b, n in SECS:
        if a <= line <= b: return n
    return '?'
html = instrument(pathlib.Path(GAME).read_text()); tmp = WORK / 'test' / '_prof.html'; tmp.write_text(html)
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME'), args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    page = b.new_page(viewport={'width': W_, 'height': H_}, device_scale_factor=1)
    page.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    page.add_init_script(INIT)
    cdp = page.context.new_cdp_session(page)
    cdp.send('Profiler.enable'); cdp.send('Profiler.setSamplingInterval', {'interval': 200}); cdp.send('Profiler.start')
    b.start_tracing(page=page, categories=['devtools.timeline', 'v8', 'disabled-by-default-v8.compile', 'blink.user_timing'])
    t0 = time.time()
    page.goto('file://' + str(tmp) + '?nosave&debug', wait_until='commit')
    page.wait_for_function('window.__sc !== undefined || window.__err', timeout=120000, polling=50)
    t1 = time.time()
    prof = cdp.send('Profiler.stop')['profile']
    tr = json.loads(b.stop_tracing())
    info = page.evaluate("() => window.__sc('({calls: renderer.info.render.calls, tris: renderer.info.render.triangles, mem: renderer.info.memory, heap: performance.memory ? performance.memory.usedJSHeapSize : 0, progs: renderer.info.programs.length, objs: (() => { let n = 0; scene.traverse(() => n++); return n; })()})')")
    b.close()
print(f'wall: goto -> game ready {t1 - t0:.2f} s')
print('first frame:', json.dumps(info))
# CPU profile
nodes = {n['id']: n for n in prof['nodes']}
dt = collections.Counter(); 
ts = prof['timeDeltas']; samples = prof['samples']
for sid, d in zip(samples, ts): dt[sid] += d
selfsec = collections.Counter(); special = collections.Counter(); selffn = collections.Counter()
for nid, us in dt.items():
    cf = nodes[nid]['callFrame']; url = cf['url']
    if '_prof.html' in url:
        s = secOf(cf['lineNumber'] + 1); selfsec[s] += us; selffn[(cf['functionName'] or '(anon)') + '@' + str(cf['lineNumber'] + 1) + ' [' + s + ']'] += us
    elif 'three' in url: selfsec['three.js'] += us
    elif url: selfsec['other:' + url[:40]] += us
    else: special[cf['functionName']] += us
tot = sum(dt.values())
print(f'\nCPU profile total {tot/1e6:.2f} s')
for k, v in special.most_common(): print(f'  {k:28} {v/1e3:8.0f} ms')
for k, v in selfsec.most_common(20): print(f'  self in {k:20} {v/1e3:8.0f} ms')
print('top functions (self):')
for k, v in selffn.most_common(25): print(f'  {v/1e3:7.0f} ms  {k}')
# inclusive times
parent = {}
for n in prof['nodes']:
    for c in n.get('children', []): parent[c] = n['id']
def anc(nid):
    while nid in nodes:
        yield nodes[nid]; nid = parent.get(nid)
incl = collections.Counter()
WANT = ['buildDeck', 'loop', 'render', 'shadowStandIns', 'compileShaders', 'initTextures', 'WebGLRenderer', 'drawScreen', 'applyLight', 'grain', 'freezeStill', 'texImage2D', 'getProgram', 'initMaterial', 'setProgram', 'linkProgram', 'compileShader']
for nid, us in dt.items():
    seen = set()
    for n in anc(nid):
        f = n['callFrame']['functionName']
        if f in WANT and f not in seen: seen.add(f); incl[f] += us
print('inclusive:')
for k, v in incl.most_common(): print(f'  {k:20} {v/1e3:8.0f} ms')
# trace phases (main thread top level)
ev = tr['traceEvents'] if isinstance(tr, dict) else tr
agg = collections.Counter(); cnt = collections.Counter()
for e in ev:
    if e.get('ph') == 'X' and e.get('name') in ('ParseHTML', 'EvaluateScript', 'v8.compile', 'v8.parseOnBackground', 'V8.CompileCode', 'v8.compileModule', 'MajorGC', 'MinorGC', 'V8.GC_MC_BACKGROUND_MARKING', 'Layout', 'Paint', 'FunctionCall', 'v8.run', 'V8.ScriptCompiler', 'v8.produceCache', 'CompositeLayers', 'UpdateLayoutTree', 'V8.ParseProgram', 'V8.CompileLazy', 'V8.ParseFunction', 'V8.CompileFullCode', 'V8.CompileIgnition', 'V8.Execute', 'BlinkGC.AtomicPhase', 'ResourceSendRequest'):
        agg[e['name']] += e.get('dur', 0); cnt[e['name']] += 1
print('trace (summed durations, may nest):')
for k, v in agg.most_common(): print(f'  {k:28} {v/1e3:8.0f} ms  x{cnt[k]}')
