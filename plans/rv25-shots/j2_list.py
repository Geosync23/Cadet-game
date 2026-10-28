# RV25: Dev mode J2: every Ship events jump's landing (devmodeJumpWhen) as the panel lists it, in a #dev page
import sys, os, json
G = os.path.abspath(sys.argv[1])
exec(open(os.path.join(os.path.dirname(G), 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
vp = WORK / 'test' / '_rv25_j2.html'; vp.write_text(open(G).read())
with sync_playwright() as pw:
    g = Game(pw, str(vp)); 
    g.page.goto('file://' + str(g.page.url.split('file://')[1].split('?')[0]) + '?nosave&debug#dev'); g.page.wait_for_timeout(4000)
    print(g.page.evaluate("""() => { const S = window.__sc; return S ? S("DM_JUMPS.filter(j => j.group === 'events').map(j => { let on; try { on = typeof j.on === 'function' ? j.on() : j.on !== false; } catch (e) { on = 'err ' + e; } return j.id + (on ? '' : ' (off)') + ' | ' + j.label + ' | ' + devmodeJumpWhen(j); }).join('\\\\n')") : 'no __sc'; }"""))
    g.close()
