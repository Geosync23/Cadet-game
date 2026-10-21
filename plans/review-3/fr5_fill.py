# PR3: FR1 turn 5. Does the auditorium fill by 16:00-16:10 in real play (no jump into the address)? Jump to 15:45 on Day 5,
# stand in the auditorium, then play frames to 16:15, counting crew in the room every ship minute. Shot at 16:05.
import os, sys
os.environ.setdefault('CADET_WORK', '/tmp/work-RV3')
exec(open('/tmp/rv/pp.py').read())
SH = '/home/user/Cadet-game/plans/review-3'
g = start('?nosave&debug'); g.step(20); g.page.add_style_tag(content='.bub{animation:none!important}')
g.ev("skipTo(4 * 1440 + 945)"); g.step(5)
g.ev("(() => { if (deckDef.num !== 7) goToDeck(7); const l = DECKS[7].places.find(p => p.type === 'rec:lectern'); const c = [l.at[0] + 4, l.at[1]]; const p = cellPos(...c); const o = free(...c) ? c : (nearestOpen(p.x, p.z, player) || c); player.obj.position.copy(cellPos(...o)); player.path.length = 0; target.copy(player.obj.position).setY(.7); })()")
CNT0 = "(() => { const A = roomAt(...DECKS[7].places.find(p => p.type === 'rec:lectern').at); let n = 0, s = 0; for (const a of DECK_CREW) { const o = a.obj || a.mesh || a.g; const x = o && o.position ? o.position.x : a.x, z = o && o.position ? o.position.z : a.z; const t = (typeof tileAt === 'function') ? tileAt(x, z) : [Math.round(x), Math.round(z)]; if (roomAt(...t) === A) { n++; if (/sit/.test(a.pose || '')) s++; } } return [clockText().slice(-5), DECK_CREW.length, n, s]; })()"
CNT = "(() => { const l = DECKS[7].places.find(p => p.type === 'rec:lectern'), L = cellPos(...l.at); let n = 0, s = 0, lec = []; for (const a of DECK_CREW) { const P = { x: a.x, z: a.z }; const dd = Math.hypot(P.x - L.x, P.z - L.z); if (dd < 12) { n++; if (/sit/.test(a.pose || a.anim || '')) s++; } if (dd < 2.5 && a.p) lec.push(a.p.id); } return [clockText().slice(-5), DECK_CREW.length, n, s, lec]; })()"
print(g.ev("(() => { const a = DECK_CREW[0]; return a ? Object.keys(a).slice(0, 40) : null; })()"))
shot = False
while True:
    g.shipmins(3); r = g.ev(CNT); print(r, flush=True)
    if not shot and r[0] >= '16:05': g.page.screenshot(path=SH + '/fr5_fill_1605.png'); shot = True
    if r[0] >= '16:45': break
print('errors', g.errors[:3]); g.close()
