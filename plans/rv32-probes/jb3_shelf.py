# RV32 probe (0.99.7, JB3 note 3): a real tap at the fetch arrow's pin for each storage shelf (Deck 5 main storage), at
# the view's four turns (#rot), phone size 390x844, standing in front of the aisle. shelfNeed() is stubbed to the part
# (a real job of the right part claimed: a fetch step asks); counts the "No X on the Y shelf ... lit up" toasts (a wrong shelf) and what the tap started.
# Usage (repo root): jb3_shelf.py BUILD.html
import sys, json
sys.argv, BUILD = [sys.argv[0]], sys.argv[1]
exec(open('cadet_test.py').read().split('\ndef run(')[0])
PARTS = [('5-parts-1', 'relay'), ('5-parts-1', 'lamp'), ('5-parts-2', 'cartridge'), ('5-parts-3', 'valve'), ('5-parts-4', 'element')]
res = []
with sync_playwright() as pw:
    g = Game(pw, BUILD, 390, 844); g.step(5)
    g.ev("(() => { goToDeck(5); window.__t = []; const o = toast; toast = function (a, b) { window.__t.push(String(a) + ' | ' + String(b || '')); return o.apply(this, arguments); }; })()"); g.step(10)
    for turn in range(4):
        for pid, part in PARTS:
            g.ev(f"""(() => {{ if (ACT) actEnd(true); window.__t = []; try {{ const m = myJob(); if (m) {{ m.claimedBy = null; m.status = 'open'; SHIP.player.work = null; }} }} catch (e) {{}}
              const j = SHIP.jobs.find(x => x.machine && x.status === 'open' && !x.claimedBy && (x.parts || []).length); if (j) {{ j.parts = [{json.dumps(part)}]; claimJob(j.id); }}
              window.__need = typeof shelfNeed === 'function' ? shelfNeed() : null;
              const s = placeSpot({json.dumps(pid)}), w = cellPos(...s.walk); player.obj.position.set(w.x, 0, w.z); player.stop(); target.copy(player.obj.position).setY(.7); }})()""")
            g.step(15)
            xy = g.ev(f"(() => {{ const s = placeSpot({json.dumps(pid)}), v = new THREE.Vector3(s.x, .05, s.z).project(camera); return [(v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight]; }})()")
            g.page.mouse.click(*xy); g.step(10)
            t = g.ev('window.__t.slice()'); wrong = [x for x in t if 'lit up for you' in x]
            res.append([turn, pid, part, g.ev('window.__need'), bool(wrong), g.ev('ACT ? ACT.kind : null'), (wrong or t or [''])[0][:90]])
        g.page.click('#rot'); g.step(20)
    for r in res: print(json.dumps(r))
    print('wrong', sum(1 for r in res if r[4]), 'of', len(res)); print('errors', g.errors[:4])
