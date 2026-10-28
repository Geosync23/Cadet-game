# RV24: a pretend-pad look at 390x844 (controller update reviews): reuses controller_check.py's Run (FAKEPAD) from the game's folder.
# Usage: python3 pad_look.py BUILD.html OUTDIR part   (parts: wavec)
import sys, os, re, json, pathlib
G = sys.argv[1]; OUT = sys.argv[2]; PART = sys.argv[3]; os.makedirs(OUT, exist_ok=True)
cc = os.path.join(os.path.dirname(os.path.abspath(G)), 'controller_check.py')
sys.argv = [cc, G, 'idle']
src = open(cc).read().split('# ---- run ----')[0]
__file__ = cc
exec(src)
from playwright.sync_api import sync_playwright
ON = both_builds(SRC)[-1][1]
with sync_playwright() as pw:
    if PART == 'wavec':
        r = Run(pw, ON, 'rv24_wc', mode='pad', plug={}, w=390, h=844, query='?nosave&debug&sound')
        r.js('window.cadetPopupsNow = true'); r.step(30)
        print('before', r.ev("[document.getElementById('devPoint') && document.getElementById('devPoint').textContent, typeof SND !== 'undefined' && SND.ctx && SND.ctx.state]"))
        r.page.screenshot(path=f'{OUT}/wc_before.png')
        r.press('RS'); r.step(6); r.page.wait_for_timeout(1000); r.step(6)
        print('after', r.ev("[document.getElementById('devPoint') && document.getElementById('devPoint').textContent, document.getElementById('tx') && document.getElementById('tx').textContent]"))
        r.page.screenshot(path=f'{OUT}/wc_after.png')
        print('errors', r.errors[:5]); r.close()
