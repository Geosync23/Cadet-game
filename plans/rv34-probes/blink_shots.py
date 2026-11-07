# RV34: phone shots (390x844) before, at the first pulse's peak (with the notice shown) and after, on Deck 3 and Deck 6.
import sys
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
build, out = sys.argv[1], sys.argv[2]
with sync_playwright() as pw:
    for d in [3, 6]:
        g = Game(pw, build, 390, 844); g.step(3)
        g.ev(f"(() => {{ skipTo(3 * 1440 + 14 * 60 + 7); goToDeck({d}, null); if (typeof GUIDE !== 'undefined') GUIDE.tq.length = 0; }})()"); g.step(30)
        g.ev("document.getElementById('toast').style.setProperty('opacity', '0', 'important')"); g.page.screenshot(path=f'{out}/d{d}_before.png')
        while 'beacon' not in g.ev("FEEL_S.kinds.join()"): g.step(1)
        while g.ev("simNow()/1000 - FEEL_S.t0") < .38: g.step(1)
        g.ev("document.getElementById('toast').style.setProperty('opacity', '1', 'important')"); g.page.screenshot(path=f'{out}/d{d}_peak.png')
        print(d, g.ev("[simNow()/1000 - FEEL_S.t0, hemi.intensity, document.getElementById('toast').textContent]"))
        g.close()
