# SC1 probe for 0.99.7 notes 17, 32, 38, 39: python3 p997_probe.py BUILD.html on|off
import sys, os, json, types
os.environ.setdefault('CADET_CHROME', '/opt/pw-browsers/chromium')
from playwright.sync_api import sync_playwright
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'cadet_test.py')).read(); src = src[:src.index('import sys, json, hashlib')]
ct = types.ModuleType('ct'); exec(src, ct.__dict__)
build, mode = sys.argv[1], sys.argv[2]
html = open(build).read()
if mode == 'on':
    assert html.count('var P997_SOCIAL_ON = false;') == 1; html = html.replace('var P997_SOCIAL_ON = false;', 'var P997_SOCIAL_ON = true;')
cp = '/tmp/claude-0/p997_' + mode + '.html'; open(cp, 'w').write(html)
JS = r"""
(() => {
  const out = { mode: P997_SOCIAL_ON, n17: [], n32: [], n38: {}, n39: {} };
  const btns = () => [...document.querySelectorAll('#chat button')].map(b => b.textContent).filter(x => x !== '×');
  socInit();
  // find people with a beat ready: raise friendship, walk the days and hours
  const ids = [...storyIdx().beats.keys()].filter(id => SOC.idx.has(id));
  for (const id of ids) { relAdd(id, 'chat', 40); const r = relGet(id); if (r.met === null) r.met = 0; }
  let found = [];
  for (let d = 2; d <= 12 && found.length < 4; d++) for (let m = 1080; m < 1300 && found.length < 4; m += 10) {
    const t = (d - 1) * 1440 + m; setShipNow(t);
    for (const id of ids) { if (found.some(f => f.id === id)) continue; const p = socP(id), mid = momentReady(p, t); if (mid) found.push({ id, t, mid, intro: socIntroOn(), gate: socGate('done') }); }
  }
  out.found = found;
  for (const f of found.slice(0, 3)) {
    setShipNow(f.t); const p = socP(f.id); chatClose();
    chatOpen(p); const r = { id: f.id, mid: f.mid, line: CHAT && CHAT.line.kind, open: btns() };
    chatDo('chat'); r.afterHello = btns(); r.helloLine = CHAT && CHAT.line.text;
    const k = btns().indexOf('Get to know'); r.getKnow = k;
    if (k >= 0) { chatDo('getknow'); r.dialogue = typeof DIALOGUE !== 'undefined' && DIALOGUE ? String(DIALOGUE.id) : null; let n = 0; while (DIALOGUE && n++ < 80) { const v = dialogueView(); if (!v) break; if (v.choices) dialogueStep(0); else dialogueStep(); } r.toldAfter = momentReady(p, f.t); }
    else { const s = btns().indexOf('Sit with them'); r.sit = s; }
    chatClose(); out.n17.push(r);
  }
  // note 32: the arrow, before and after you've opened their card
  const asks = []; const was = guideAsk; guideAsk = o => { asks.push(o.id); try { return was(o); } catch (e) { return null; } };
  try {
    const f = found[found.length - 1];
    if (f) { const p = socP(f.id); const t0 = Math.ceil(f.t / 5) * 5; setShipNow(t0); storyArrows(t0);
      out.n32.push({ id: f.id, first: asks.filter(a => a === 'story:word:' + f.id).length });
      chatOpen(p); chatDo('chat'); chatClose();
      asks.length = 0; for (let k = 1; k <= 6; k++) { setShipNow(t0 + 5 * k); storyArrows(t0 + 5 * k); }
      out.n32.push({ id: f.id, afterTalk: asks.filter(a => a === 'story:word:' + f.id).length, stillReady: momentReady(p, t0 + 30) });
      asks.length = 0; const t1 = t0 + 1440; setShipNow(t1); storyArrows(t1);
      out.n32.push({ nextDay: asks.filter(a => a === 'story:word:' + f.id).length, readyNextDay: momentReady(p, t1) }); }
  } finally { guideAsk = was; }
  // note 38: every talk's listen reply
  let n = 0, two = 0, same = 0; const ex = [];
  for (const tk of TALKS.pool.concat(...Object.values(TALKS.own), ...Object.values(TALKS.work))) {
    n++; if (tk.replies.listen2) two++;
    const p = socP(Object.keys(TALKS.own).find(k => TALKS.own[k].includes(tk)) || 'tomas') || socP('tomas');
    const said = talkPackFill(tk, p, { t: shipNow(), trad: 'Quiz night' }); if (!said) continue;
    if (said.replies.listen.text === (tk.replies.listen2 || tk.replies.listen).text) same++;
    if (ex.length < 3) ex.push([tk.ask.text, said.replies.listen.text]);
  }
  out.n38 = { talks: n, withListen2: two, listenShown: same, ex };
  // note 39: a hosted tradition you went to, and one you didn't
  const h = 'tomas', b0 = relGet(h).pts; socApply('tradition', { id: 'quiz', day: 3, at: 3 * 1440 - 200, came: ['you', h], you: true, host: h }, 3 * 1440 - 200);
  const b1 = relGet(h).pts; socApply('tradition', { id: 'quiz', day: 4, at: 4 * 1440 - 200, came: [h], you: false, host: h }, 4 * 1440 - 200);
  out.n39 = { before: b0, went: b1, notWent: relGet(h).pts };
  return out;
})()
"""
with sync_playwright() as pw:
    g = ct.Game(pw, cp, 390, 844)
    g.step(5)
    r = g.ev(JS)
    print(json.dumps(r, indent=1))
    print('errors:', g.errors[:5])
    g.close()
