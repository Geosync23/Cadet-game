import os, sys, json, re, pathlib
S = '/tmp/claude-0/-home-user/a4344e06-66ec-50a3-8125-a9cc15d32fe0/scratchpad'
exec(open(S + '/probe/pp.py').read())
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844)
    g.ev("setShipNow(10 * 1440 + 9 * 60); needsT = null"); g.step(3)
    print(g.ev("(() => { machinesNow(); return SHIP.jobs.filter(j => j.machine && j.kind === 'service' && j.status !== 'done').map(j => [j.id, j.status, j.posted]).slice(0, 8); })()"))
    r = g.ev("""(() => { const j = SHIP.jobs.find(j => j.machine === '7-aud-seats' && j.status !== 'done'); if (!j) return 'no aud job'; j.claimedBy = null; j.status = 'open'; delete j.start; for (const p of j.parts) SHIP.stores[p] = 2; return claimJob(j.id); })()""")
    print('claimed', r)
    g.ev("goToDeck(7)"); g.step(5)
    print(g.ev("""(() => { const s = placeSpot(panelPlace(myJob().machine)); return [s.x, s.z, ITEMS.map(i => { i.hit.getWorldPosition(_wp); return [i.t, i.kind || i.type || '', +Math.hypot(_wp.x - s.x, _wp.z - s.z).toFixed(2)]; }).sort((a, b) => a[2] - b[2]).slice(0, 6)]; })()"""))
    print('tap nearest', g.ev("(() => { const s = placeSpot(panelPlace(myJob().machine)), it = ITEMS.map(i => { i.hit.getWorldPosition(_wp); return [i, _wp.clone()]; }).sort((a, b) => Math.hypot(a[1].x - s.x, a[1].z - s.z) - Math.hypot(b[1].x - s.x, b[1].z - s.z))[0]; return [it[0].t, playerTap(it[0], it[1].clone(), it[1].clone())]; })()"))
    for t in ('Seats',):
        print('tap', t, g.ev("(() => { const it = ITEMS.find(i => i.t === '%s'); it.hit.getWorldPosition(_wp); return playerTap(it, _wp.clone(), _wp.clone()); })()" % t))
        for k in range(80):
            g.step(30)
            if k > 1 and not g.ev("!!ACT || player.path.length > 0"): break
        print(' ->', g.ev("JSON.stringify([ACT && [ACT.kind, ACT.placeId], SHIP.player.work, document.getElementById('tt').textContent + ': ' + document.getElementById('tx').textContent])"))
    print('rec open?', g.ev("typeof recOpenNow === 'function' ? recOpenNow() : 'n/a'"), g.ev("document.getElementById('tt').textContent + ': ' + document.getElementById('tx').textContent"))
    print(g.errors[:3])
