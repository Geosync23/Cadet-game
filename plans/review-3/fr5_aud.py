# PR3: FR1 turn 5. The address on Friday Day 5 at 16:10 in the rec deck auditorium, at phone size (390x844 portrait,
# zoom as the game sets it), with SHORT_FRIDAY on: who's in the room, draw calls, a shot. Run: GAME=on.html python3 fr5_aud.py
import os, sys
sys.path.insert(0, '/home/user/Cadet-game/plans/review-3'); os.environ.setdefault('CADET_WORK', '/tmp/work-RV3')
exec(open('/tmp/rv/pp.py').read())
SHOTS = '/home/user/Cadet-game/plans/review-3'
g = start('?nosave&debug'); g.step(20)
g.page.add_style_tag(content='.bub{animation:none!important}')
for at, name in [(970, 'fr5_aud_1610'), (995, 'fr5_aud_1635')]:
    g.ev(f"skipTo(4 * 1440 + {at})"); g.step(5)
    g.ev("(() => { if (deckDef.num !== 7) goToDeck(7); const l = DECKS[7].places.find(p => p.type === 'rec:lectern'); const c = [l.at[0] + 4, l.at[1]]; const p = cellPos(...c); const o = free(...c) ? c : (nearestOpen(p.x, p.z, player) || c); player.obj.position.copy(cellPos(...o)); player.path.length = 0; target.copy(player.obj.position).setY(.7); })()")
    g.step(90)
    r = g.ev("""(() => { const inA = DECK_CREW.filter(a => a.p && roomAt(Math.round(a.x), Math.round(a.z)) === roomAt(...DECKS[7].places.find(p => p.type === 'rec:lectern').at));
      return { t: clockText(), deck: deckDef.num, crewOnDeck: DECK_CREW.length, inAud: inA.length, lectern: inA.filter(a => ['marrow','vance'].includes(a.p.id)).map(a => a.p.id + ':' + a.pose), calls: renderer.info.render.calls, tris: renderer.info.render.triangles, bubbles: [...document.querySelectorAll('.bub')].filter(b => b.style.display !== 'none').length }; })()""")
    print(name, r, flush=True)
    g.page.screenshot(path=f'{SHOTS}/{name}.png')
print('errors', g.errors[:3])
g.close()
