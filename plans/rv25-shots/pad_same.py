# RV25: is the simulation the same with PAD_ON true and false? A hash of the crowd and deck crew at Sunday dinner.
import sys, os, json
G = os.path.abspath(sys.argv[1])
exec(open(os.path.join(os.path.dirname(G), 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
src = open(G).read(); off = src.replace('const PAD_ON = true;', 'const PAD_ON = false;', 1)
pon = WORK / 'test' / '_rv25_padon.html'; pon.write_text(src); poff = WORK / 'test' / '_rv25_padoff.html'; poff.write_text(off)
H = """(() => { let h = 0; const mix = s => { for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) | 0; };
  for (const a of DECK_CREW) mix((a.p ? a.p.id : '?') + Math.round(a.x * 100) + ',' + Math.round(a.z * 100));
  const st = crowd.stats(); mix(JSON.stringify(st)); return { h, people: st.people, crew: DECK_CREW.length, calls: renderer.info.render.calls }; })()"""
with sync_playwright() as pw:
    for tag, path in (('on', pon), ('off', poff), ('on', pon)):
        g = Game(pw, str(path)); g.page.set_viewport_size({'width': 390, 'height': 844})
        out = [g.ev(H)]
        g.ev("skipTo(6 * 1440 + 18 * 60 + 30); if (deckDef.num !== 3) goToDeck(3)"); g.step(30); out.append(g.ev(H))
        g.step(60); out.append(g.ev(H)); print(tag, out, flush=True); g.close()
