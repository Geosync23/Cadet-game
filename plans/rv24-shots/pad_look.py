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
        strs = ["Laundry: carry your hamper to a free washer in the Deck 4 laundry and tap it. It runs half an hour, and you can leave. Take the clean washing out and put it away at your wardrobe.",
          "You set your laundry hamper down. Tap it to pick it up again.",
          "Zeke gives you a pair of spare needles and some wool. Knitting is one of your hobbies now: sit down and tap Hobby.",
          "It's on the job board in the Works bay, Deck 5, until 14:00: take it there if you'd like to. A hover cart from the Cart bay, the crates in the cargo hold, then tap any shelf in main storage."]
        for x in strs: print('  words:', r.ev("introTapWords(" + json.dumps(x) + ")"))
        r.js("dispatchEvent(new PointerEvent('pointerdown'))"); r.step(4)
        print('after touch', r.ev("[document.getElementById('devPoint') && document.getElementById('devPoint').textContent, introTapWords('Tap it to pick it up again.')]"))
        r.page.screenshot(path=f'{OUT}/wc_touch.png')
        print('errors', r.errors[:5]); r.close()
        # the Saves app by pad, its hint at 390x844 (setup as part_saves: arrival signed by JS)
        r = Run(pw, ON, 'rv24_wcs', mode='pad', plug={}, w=390, h=844, query='?debug')
        r.ev("introSkip()"); r.step(10)
        for k in range(6):
            r.ev("(() => { const m = typeof INTRO_UI !== 'undefined' && INTRO_UI.manifest; if (m) { const i = m.querySelector('input'); if (i && !i.value) i.value = 'Ash'; } if (m) m.querySelector('form').dispatchEvent(new Event('submit', { cancelable: true })); return !!m; })()"); r.step(10)
        r.ev("SHIP.device && SHIP.device.settings && (SHIP.device.settings.tips = false)"); r.step(4)
        for k in range(3):
            if r.ev("DEV.open"): break
            r.press('Y'); r.step(6)
        ok = s5_pad_to(r, r'Saves'); r.press('A'); r.step(6)
        body = r.ev("document.getElementById('devBody').textContent")
        print('saves reached', ok, 'hint' if 'With a controller' in body else 'NO HINT', body[:200])
        r.page.screenshot(path=f'{OUT}/wc_saves.png')
        print('errors', r.errors[:5]); r.close()
