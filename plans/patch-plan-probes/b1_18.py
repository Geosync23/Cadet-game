from b1_common import *
g = start(); to_day1(g, 8*60+40)
g.ev("(() => { window.__said = []; const old = bubbleSay; bubbleSay = function (h, text, s) { let who = null; try { const a = DECK_CREW.find(x => x.rig === h || x.obj === h || x === h || (x.body && x.body === h)); who = a && a.p ? a.p.id : (h && h.p ? h.p.id : String(h && (h.id || h.name) || '?')); } catch (e) {} window.__said.push([clockText(), who, text]); return old.apply(this, arguments); }; const ot = toast; toast = function (a, b) { window.__said.push([clockText(), 'TOAST ' + a, b]); return ot.apply(this, arguments); }; return true; })()")
tele(g, 5, [20, 4])
for i in range(40):
    g.secs(2); g.ev(DLG)
    if g.ev("SHIP.time.min") >= 9*60+16: break
g.ev("careerClock()"); g.secs(1)
# jump to 16:00 on shift (skipTo: the sim catches up), back in the Works bay
g.ev("skipTo((SHIP.time.day - 1) * 1440 + 16 * 60)"); tele(g, 5, [20, 4]); g.secs(2)
print(g.ev("clockText()"), g.ev("SHIP.intro.step"), g.ev("(() => { const a = DECK_CREW.find(x => x.p && x.p.id === INTRO_ESCORT); return a ? [a.x.toFixed(1), a.z.toFixed(1), a.esc] : null })()"))
shot = False
while g.ev("SHIP.time.min") < 18*60 + 10:
    g.secs(4); g.ev(DLG)
    m = g.ev("SHIP.time.min")
    if not shot and m >= 17*60 + 2: g.snap('18-end-of-training-day'); shot = True
for x in g.ev("window.__said"): print(x)
g.close()
