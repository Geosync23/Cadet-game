import os, sys, json
os.environ.setdefault('CADET_CHROME', '/opt/pw-browsers/chromium')
os.environ.setdefault('CADET_WORK', '/tmp/cw-ct')
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0])
S = '/tmp/claude-0/-home-user-Cadet-game/1a3acdee-25ba-54ef-8a48-f94140cf1be8/scratchpad'
H = r"""
window.__at = (d, m) => (d - 1) * 1440 + m;
window.__who = id => schedPeople().find(p => p.id === id);
window.__w = id => { const w = whereIs(__who(id), shipNow()); return w ? { deck: w.deck, place: w.placeId, tag: w.tag || w.act, moving: w.moving } : null; };
window.__dist = id => { const a = DECK_CREW.find(a => a.p && a.p.id === id), P = player.obj.position; return a ? +Math.hypot(a.x - P.x, a.z - P.z).toFixed(1) : null; };
window.__tile = () => cellAt(player.obj.position.x, player.obj.position.z).join(',');
window.__room = () => { try { const r = DECKS[deckDef.num].rooms[roomAt(...player.here())]; return deckDef.num + '|' + (r && r.name || ''); } catch (e) { return deckDef.num + '|?'; } };
window.__put = (i, j) => { const c = cellPos(i, j), at = nearestOpen(c.x, c.z, player); player.obj.position.copy(cellPos(...at)); target.copy(player.obj.position).setY(.7); player.stop && player.stop(); return at; };
window.__toasts = []; { const t0 = toast; toast = function (a, b) { __toasts.push(hhmm(shipNow() % 1440) + ' ' + a + ': ' + b); return t0.apply(this, arguments); }; }
window.__dlg = pick => { const out = []; let n = 0; while (DIALOGUE && n++ < 60) { const v = dialogueView(); if (v.choices) { out.push('CHOICE->' + pick + ' ' + v.choices.map(c => c.text || c).join(' / ')); dialogueStep(pick); } else { out.push((v.who || '') + ': ' + (v.text || '')); dialogueStep(); } } return out; };
1"""
def mk(pw, path, w=390, h=844):
    g = Game(pw, path, w=w, h=h); g.ev(H); g.page.add_style_tag(content='#toast,.nf{pointer-events:none!important}'); return g
def walk(g, i, j, maxs=80):
    r = g.ev(f"playerGo([{i}, {j}])")
    for k in range(maxs):
        g.step(15)
        if g.ev("!player.path.length"): break
    return g.ev("__tile()")
def run(g, mins, until=None, every=10):
    for k in range(int(mins * 50 / every)):
        g.step(every)
        if until and g.ev(until): return True
    return False
def near_walk(g, pid, off=6, reach=2.5):
    """stand `off` tiles from someone (open tile), then walk up next to them with a real path (playerGo)"""
    a = g.ev(f"(() => {{ const a = DECK_CREW.find(a => a.p && a.p.id === '{pid}'); return a ? [a.x, a.z] : null; }})()")
    if not a: return 'not on deck'
    g.ev(f"(() => {{ for (const [dx, dz] of [[{off},0],[-{off},0],[0,{off}],[0,-{off}],[{off/2},{off/2}],[-{off/2},-{off/2}]]) {{ const at = nearestOpen({a[0]} + dx, {a[1]} + dz, player); if (at) {{ const c = cellPos(...at); if (Math.hypot(c.x - {a[0]}, c.z - {a[1]}) >= 3) {{ player.obj.position.copy(c); target.copy(c).setY(.7); return at; }} }} }} }})()")
    d0 = g.ev(f"__dist('{pid}')")
    ok = g.ev(f"(() => {{ const a = DECK_CREW.find(a => a.p && a.p.id === '{pid}'); const cs = []; for (let dx = -2; dx <= 2; dx++) for (let dz = -2; dz <= 2; dz++) {{ const at = nearestOpen(a.x + dx * .8, a.z + dz * .8, player); if (at) {{ const c = cellPos(...at); cs.push([Math.hypot(c.x - a.x, c.z - a.z), at]); }} }} cs.sort((p, q) => p[0] - q[0]); window.__cs = cs.slice(0, 4); for (const [, at] of cs) if (playerGo(at)) return at; return null; }})()")
    for k in range(80):
        g.step(15)
        if g.ev("!player.path.length"): break
    return f"from {d0} m, walked to {ok} ({g.ev('__tile()')}), now {g.ev(f'__dist(\"{pid}\")')} m"
