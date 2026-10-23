# RV9: add a timed log of everything said and shown to intro_check.py's part 8 (writes RV9_LOG as JSON)
import sys, re
p = sys.argv[1]; t = open(p).read()
INJ = r'''        g.ev(r"""(() => { window.__log = []; const L = (k, x) => window.__log.push([shipNow(), clockText(), SHIP.intro && SHIP.intro.step, k, x]);
          const w = (name, f) => { const old = window[name] || eval(name); const nf = function () { try { f.apply(this, arguments); } catch (e) {} return old.apply(this, arguments); }; eval(name + ' = nf'); };
          const oT = toast; toast = function (a, b) { L('toast', a + ' | ' + b); return oT.apply(this, arguments); };
          const oM = mailSend; mailSend = function (o) { L('mail', (o && o.from) + ' | ' + (o && o.subject)); return oM.apply(this, arguments); };
          const oG = setGoal; setGoal = function (g) { L('goal', g && g.label); return oG.apply(this, arguments); };
          const oC = clearGoal; clearGoal = function () { L('goal', null); return oC.apply(this, arguments); };
          const oB = bubbleSay; bubbleSay = function (h, text) { const who = h && (h.p ? h.p.id : h.spec ? h.spec.name : h.id) || null; L('say', (who || '?') + ' | ' + text); return oB.apply(this, arguments); };
          const oD = dialogueDraw; let lastD = null; dialogueDraw = function () { try { const v = DIALOGUE && dialogueView(); const s = v ? (DIALOGUE.id + ' | ' + JSON.stringify(v)).slice(0, 400) : null; if (s && s !== lastD) { lastD = s; L('dlg', s); } } catch (e) {} return oD.apply(this, arguments); };
          return true; })()""")
'''
anchor = "        g.ev('CLOTHES_ON = true'); g.ev('newGameStart(true)')"
assert anchor in t, 'anchor 1'
t = t.replace(anchor, INJ + anchor, 1)
a2 = "        simnow = g.ev(\"typeof tapCrew === 'function'"
assert a2 in t, 'anchor 2'
t = t.replace(a2, "        import os as _os; json.dump(g.ev('window.__log'), open(_os.environ['RV9_LOG'], 'w'), indent=0)\n" + a2, 1)
a3 = "            r = g.page.evaluate('([s, m]) => window.__sc(s)(m)', [WALK_TICK, 'follow'])\n"
assert a3 in t, 'anchor 3'
t = t.replace(a3, a3 + "            _POS.append([r['t'], r['step'], r['deck'], r['me'], r['esc'][0] if r['esc'] else None, r['esc'][2] if r['esc'] else None, r['dlg']])\n", 1)
t = t.replace("        order, peak, led = [], {}, 0\n", "        order, peak, led = [], {}, 0\n        _POS = []\n", 1)
t = t.replace("json.dump(g.ev('window.__log'), open(_os.environ['RV9_LOG'], 'w'), indent=0)", "json.dump({'log': g.ev('window.__log'), 'pos': _POS}, open(_os.environ['RV9_LOG'], 'w'), indent=0)")
open(p, 'w').write(t)
print('ok')
