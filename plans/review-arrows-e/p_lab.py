import sys
src = open('/home/user/Cadet-game/arrows_check.py').read().split("GUIDE = 'guide' in")[0]
BUILD = sys.argv[1]; sys.argv = [sys.argv[0]]
exec(src); GUIDE = False
J = r"""(() => { const out = [], lab = document.querySelector('#ixGoal .ixlab'), el = document.getElementById('ixGoal'); el.hidden = false;
  const fit = t => { lab.textContent = t; return [t, lab.scrollWidth, lab.clientWidth, lab.scrollWidth > lab.clientWidth ? 'CUT' : 'fits']; };
  for (const r of CAREER_LADDER.filter(r => r.size === 'big' && r.tier === 1)) {
    const by = r.by[0], who = worksFirst(by), w = r.where || { deck: 5, room: 'w' }, room = (DECKS[w.deck].rooms[w.room] || {}).name || 'the meeting';
    const t1 = 'Meet ' + who + ': ' + room + ', 10:45', t2 = 'Stay close and watch ' + who, t3 = 'Your turn: ' + mechName(r.id).toLowerCase() + ', on the board';
    for (const t of [t1, t2, t3]) { out.push(fit(t)); out.push(fit('Take the lift to Deck ' + w.deck + ': ' + t.charAt(0).toLowerCase() + t.slice(1))); }
  }
  el.hidden = true; return out; })()"""
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    pg = Page(ctx, BUILD); pg.day2()
    for x in pg.ev(J): print(x)
