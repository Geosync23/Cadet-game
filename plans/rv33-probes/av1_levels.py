# RV33 AV1 probe: what you hear at late piano and the jam (RMS of the live music after its distance gain and wall
# filter, and of the whole mix), the ship's music ducked, who is at the piano; the film on the auditorium screen at phone size.
import sys, json, re, pathlib
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
src, out = sys.argv[1], sys.argv[2]
h = pathlib.Path(src).read_text()
for a, b in [('const SND_LIVE = false;', 'const SND_LIVE = true;'), ('const SND_DISC = false;', 'const SND_DISC = true;'), ('const REC_FILM = false;', 'const REC_FILM = true;')]:
    assert a in h; h = h.replace(a, b)
on = out + '/on.html'; pathlib.Path(on).write_text(h)
R3_AT = r"""(([t, deck, room]) => { skipTo(t); goToDeck(deck); const R = DECKS[deck].rooms, k = R[room] ? room : Object.keys(R).find(x => R[x].name === room);
  const tl = ROOM_TILES[k]; if (!tl || !tl.length) return 'no tiles for ' + room; player.obj.position.copy(cellPos(...tl[(tl.length / 2) | 0])); return k; })"""
TAP = r"""(() => { const A = window.__an || (window.__an = (() => { const c = SND.ctx, a = c.createAnalyser(), m = c.createAnalyser(); a.fftSize = 2048; m.fftSize = 2048; SND.bus.master.connect(m); const hu = c.createAnalyser(), mu = c.createAnalyser(); hu.fftSize = mu.fftSize = 2048; SND.bus.hum.connect(hu); (SND.bus.duck || SND.bus.music).connect(mu); return { a, m, hu, mu, src: null }; })());
  const o = SND.live.out; if (o && A.src !== o.muff) { try { if (A.src) A.src.disconnect(A.a); } catch (e) {} o.muff.connect(A.a); A.src = o.muff; } return !!o; })()"""
HI = r"""(an => { const b = new Float32Array(an.frequencyBinCount); an.getFloatFrequencyData(b); const hz = SND.ctx.sampleRate / 2 / b.length; let s = 0; for (let i = 0; i < b.length; i++) if (i * hz >= 250 && i * hz <= 5000) s += Math.pow(10, b[i] / 10); return s; })"""
RMS = r"""(an => { const b = new Float32Array(2048); an.getFloatTimeDomainData(b); let s = 0; for (const v of b) s += v * v; return Math.sqrt(s / b.length); })"""
def db(x): import math; return round(20 * math.log10(max(x, 1e-6)), 1)
def listen(g, sec=3):
    lv, mv, hv, uv, hi = [], [], [], [], []
    for _ in range(int(sec * 4)):
        g.page.wait_for_timeout(250); g.step(2); g.ev(TAP)
        lv.append(g.ev(f"window.__an.src ? ({RMS})(window.__an.a) : 0")); mv.append(g.ev(f"({RMS})(window.__an.m)")); hv.append(g.ev(f"({RMS})(window.__an.hu)")); hi.append(g.ev(f"({HI})(window.__an.m)")); uv.append(g.ev(f"({RMS})(window.__an.mu)"))
    st = g.ev("(({kind, n, near, duck, inRoom, bar}) => ({kind, n, near: Math.round(near*100)/100, duck: Math.round(duck*100)/100, inRoom, bar}))(SND.live)")
    return {'live_dB': db(sum(lv) / len(lv)), 'hum_dB': db(sum(hv) / len(hv)), 'music_dB': db(sum(uv) / len(uv)), 'mix_dB': db(sum(mv) / len(mv)), 'mix_250_5k_dB': round(10 * __import__('math').log10(max(sum(hi) / len(hi), 1e-12)), 1), **st}
with sync_playwright() as pw:
    g = Game(pw, on, w=390, h=844)
    g.page.goto('file://' + str(g.tmp) + '?nosave&debug&sound'); g.page.wait_for_function('window.__sc !== undefined || window.__err', timeout=60000)
    g.step(30); g.page.mouse.click(195, 420); g.step(3)
    g.page.wait_for_function("window.__sc('SND._.state()') === 'running'", timeout=10000)
    g.ev("SND.music.setEnabled && SND.music.setEnabled(true)")
    days = g.ev("[...Array(14)].map((_, i) => i + 1).map(d => [d, eventsOn(d).filter(e => ['late-piano','jam'].includes(e.id)).map(e => [e.id, e.from])]).filter(x => x[1].length)")
    print('days:', days)
    def quiet(tag):
        g.ev("SND.live.forced = { kind: null }"); g.ev("SND.live.forced = null")
    g.ev("SND.bus.hum.gain.value = 0")
    g.ev("goToDeck(3)"); g.step(10); g.ev("SND.music.setEnabled(true); SND.music.next()")
    for k in range(4): r = listen(g, 3); print('ship music, Deck 3, hum muted:', g.ev("JSON.stringify(SND.music.state())")[:80], {x: r[x] for x in ('mix_dB', 'mix_250_5k_dB', 'music_dB')})
    for name in ['late-piano', 'jam']:
        d, m = next((d, e[1]) for d, es in days for e in es if e[0] == name)
        for late in (18,):
            print(name, f'Day {d} +{late} min:', g.ev(f"({R3_AT})({json.dumps([(d - 1) * 1440 + m + late, 4, 'n'])})")); g.step(40)
            who = g.ev("DECK_CREW.filter(a => a.settled && a.spot && (PLACE_OF.get(a.spot.id)||{}).room === 'n').map(a => a.p.name.split(' ').slice(-1)[0] + '@' + a.spot.id + ':' + a.pose)")
            print('  in the music room:', who)
            print('  in the room, middle:', listen(g))
            g.ev("(() => { const p = player.obj.position; p.x = SND.live.x + 1.2; p.z = SND.live.z; })()"); g.step(2)
            print('  beside the music:', listen(g))
            if name == 'late-piano' and late == 18: g.page.screenshot(path=out + '/piano.png')
        # just outside the room: the nearest tile on this deck that is not in it
        print('  outside:', g.ev("""(() => { const pc = cellPos(...ROOM_TILES['n'][0]); let best = null, bd = 1e9;
            for (const k of Object.keys(ROOM_TILES)) { if (k === 'n') continue; for (const t of ROOM_TILES[k]) { const p = cellPos(...t), dd = Math.hypot(p.x - SND.live.x, p.z - SND.live.z); if (dd < bd) { bd = dd; best = [k, t]; } } }
            player.obj.position.copy(cellPos(...best[1])); return best[0] + ' ' + bd.toFixed(1) + ' m'; })()"""), listen(g))
        g.ev("goToDeck(3)"); g.step(20); print('  on Deck 3:', listen(g))
