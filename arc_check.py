# Starship Cadet: arc check (social engineer B, 0.39.12). Can every story arc reach its last beat?
# Steps DAYS ship days (default 70) on paper (the crew's social hours run too: bonds, rivals), every half hour from 06:00, as a diligent player would play: a chat and a
# meal with each story person a day, a Works job a day (reputation), whatever moment is ready played at once (the first
# reply each time), an appointment booked for 18:00 when a beat waits for one, a bunk visit at 20:00 from whoever's next
# beat wants one (momentWantsVisit), the struggle themes through one crew member each (beats 1-3), and a call home to each of Mum, Gran, Jo and Sam at 20:00. Then lists every arc
# that didn't finish, with its next beat and how often (in the last 7 days) its when and its where held.
# The crew arcs need the writers' baked MOMENTS (a build with claude/dialogue and claude/content, content_gen run).
# Run: CADET_CHROME=/opt/pw-browsers/chromium python3 arc_check.py BUILD.html [DAYS] [arcs|themes]   (themes: one crew
#   member per struggle theme, in a game of their own: one serious moment a day is shared, and nobody's close to 20 people)   (a few minutes)
import sys, os, json, types
os.environ.setdefault('CADET_CHROME', '/opt/pw-browsers/chromium')
from playwright.sync_api import sync_playwright
src=open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cadet_test.py')).read(); src=src[:src.index('import sys, json, hashlib')]
ct=types.ModuleType('ct'); exec(src, ct.__dict__)
DAYS=int(sys.argv[2]) if len(sys.argv)>2 else 70
MODE=sys.argv[3] if len(sys.argv)>3 else 'arcs'   # 'arcs': the story crew and calls home; 'themes': one crew member per struggle theme (a separate game: one serious moment a day is shared)
JS = r"""
([DAYS, MODE]) => {
  socInit();
  const play = () => { let n = 0; while (DIALOGUE && n++ < 80) { const v = dialogueView(); if (!v) break; if (v.choices) dialogueStep(0); else dialogueStep(); } };
  const at = (d, m) => { SHIP.time.day = d; SHIP.time.min = m; return (d - 1) * 1440 + m; };
  const live = (d, m) => { const t = (d - 1) * 1440 + m; if (typeof setShipNow === 'function') setShipNow(t); else at(d, m); if (typeof socialTo === 'function') socialTo(t); return t; };   // the crew's own social hours (bonds, rivals) run too
  const [MO] = momentBaked();
  const ppl = MODE === 'themes' ? [] : [...new Set(Object.values(MO || {}).map(m => m.who).concat(Object.keys(STORY_ARCS)))].map(id => socP(id)).filter(Boolean);
  const last = {}; for (const p of ppl) { let n = 0; for (const k in MO || {}) if (MO[k].who === p.id) n = Math.max(n, MO[k].beat); n = Math.max(n, (STORY_ARCS[p.id] || []).length); last[p.id] = n; }
  const out0 = { appts: 0, visits: 0, partial: {} };
  const TH = momentBaked()[1] || {};                    // the struggle themes: the first crew member with each theme whose beats all apply to them
  if (MODE === 'themes') for (const th of Object.keys(TH).sort()) { const ok = q => !ppl.includes(q) && voiceOf(q.id).thread === th && [1, 2, 3].some(b => momentDef(q.id + ':' + b)), all = q => [1, 2, 3].every(b => momentDef(q.id + ':' + b));
    const p = SOC.crew.find(q => ok(q) && all(q)) || SOC.crew.find(ok);   // all three beats if anyone has them, else whoever has some
    if (p) { ppl.push(p); last[p.id] = 3; out0.partial[th] = [1, 2, 3].filter(b => !momentDef(p.id + ':' + b)); } }
  const told = {}, log = [];
  const beatNow = p => { const th = voiceOf(p.id).thread || ''; return th.startsWith('arc:') ? (SHIP.rel[p.id] ? SHIP.rel[p.id].arc || 0 : 0) : storyM(p.id).b; };
  for (let d = 1; d <= DAYS; d++) {
    for (let m = 360; m < 1440; m += 30) {
      const t = live(d, m);
      if (m === 720) for (const p of ppl) { relAdd(p.id, 'chat', 2); relAdd(p.id, 'meal', 3); }
      if (m === 900) repAdd('works', 1.5, { work: 1 }, 'job');
      const wantsMe = p => { const x = momentNextId(p), dd = x && momentDef(x); return dd && [].concat(dd.where || []).some(w => w === 'appt' || w === 'visit') ? 0 : 1; };
      for (const p of ppl.slice().sort((a, b) => wantsMe(a) - wantsMe(b))) {   // a beat you made time for (an appointment, a visit) goes first, as you'd play it
        const b0 = beatNow(p);
        if (STORY_ARCS[p.id] && arcBeat(p, t)) arcTold(p);
        const nx = momentNextId(p), nd = nx && momentDef(nx), wh = nd ? [].concat(nd.where || []) : [];
        if (wh.includes('appt') && m === 600 && !SHIP.device.appts.some(a => a.with.includes(p.id) && a.at > t)) { const id0 = SHIP.device.appts.reduce((x, a) => Math.max(x, a.id), 0) + 1; SHIP.device.appts.push({ id: id0, with: [p.id], at: (d - 1) * 1440 + 1080, len: 30, where: '3-mess-5', kind: 'social', status: 'yes', by: null }); out0.appts++; }
        let vis = false; if (m === 1200 && momentWantsVisit(p, t)) { VISIT = { p, inside: true, until: Infinity }; vis = true; out0.visits++; }
        const id = momentReady(p, t); if (id) { momentShow(id); play(); }
        if (vis) VISIT = null;
        const b1 = beatNow(p); if (b1 !== b0) log.push(d + ' ' + p.id + ' ' + b1);
      }
      if (m === 1200 && MODE !== 'themes') for (const k of HOME_ORDER) if (homeCall(k, t)) play();
    }
  }
  // why a stalled arc is stuck: the next beat's gates, tried every half hour of the last 7 days
  const t1 = at(DAYS, 1200), out = { last, done: {}, stalled: {}, home: HOME_ORDER.map(k => k + ' ' + homePeekC(k).b), log };
  for (const p of ppl) {
    const n = beatNow(p); if (n >= last[p.id]) { out.done[p.id] = n; continue; }
    const id = momentNextId(p), dd = id && momentDef(id), r = SHIP.rel[p.id];
    const info = { at: n, next: id, tier: r && r.tier, met: metDays(p.id, t1), card: STORY_ARCS[p.id] ? { len: STORY_ARCS[p.id].length, arcDay: r.arcDay, showDay: r.showDay } : null };
    if (dd) {
      info.tone = dd.tone; info.where = dd.where || 'calm'; info.when = dd.when || null;
      let whenOk = 0, whereOk = 0, both = 0;
      for (let d = DAYS - 6; d <= DAYS; d++) for (let m = 360; m < 1440; m += 30) { const t = (d - 1) * 1440 + m; SHIP.time.day = d; SHIP.time.min = m;
        let w = true; if (dd.when) { try { w = !!linesOk(dd.when, p, typeof momentCtx === 'function' ? momentCtx(p, t, id) : { t, moment: id }); } catch (e) { w = false; } }
        const wh = momentWhere(p, t, dd); whenOk += w; whereOk += wh; both += w && wh; }
      Object.assign(info, { whenOk, whereOk, both, of: 7 * 36 });
      const st = storyM(p.id), g = STEP_GATES[dd.tone] || STEP_GATES.heartfelt; info.gate = { tierNeed: dd.tier ?? g.tier, metNeed: dd.metDays ?? g.met, gapNeed: dd.gapDays ?? g.gap, lastAt: st.at, lastHf: st.hf, serious: SHIP.social.stories.serious, appts: SHIP.device.appts.filter(a => a.with.includes(p.id)).slice(-3).map(a => [Math.floor(a.at / 1440) + 1, a.at % 1440, a.status]) };
    }
    out.stalled[p.id] = info;
  }
  out.themes = {}; for (const th of Object.keys(TH).sort()) { const who = SOC.crew.filter(q => voiceOf(q.id).thread === th); out.themes[th] = { crew: who.length, picked: (ppl.find(q => voiceOf(q.id).thread === th) || {}).id || null,
    rivals: th === 'rivalry' ? who.map(q => q.id + ':' + (bondOf(q.id, 'rival') || '-') + ':' + Math.min(...SOC.crew.filter(o => o !== q).map(o => affinity(q.id, o.id)))) : undefined }; }
  out.bonds = {}; for (const b of Object.values(SHIP.social.bonds || {})) out.bonds[b.kind] = (out.bonds[b.kind] || 0) + 1;
  out.rep = repBand('works'); out.sim = out0;
  return out;
}
"""
with sync_playwright() as pw:
    g = ct.Game(pw, sys.argv[1]); g.step(3)
    r = g.page.evaluate('([s, a]) => window.__sc("(" + s + ")(" + JSON.stringify(a) + ")")', [JS, [DAYS, MODE]])
    g.close()
    print('Finished:', ', '.join(f"{k} {v}/{r['last'][k]}" for k, v in r['done'].items()))
    print('Home:', ', '.join(r['home']), '| booked appointments', r['sim']['appts'], '| visits', r['sim']['visits'])
    for k, v in r['stalled'].items(): print('STALLED', k, json.dumps(v))
    print('Themes:', json.dumps(r['themes']))
    print('Crew bonds at the end:', json.dumps(r['bonds']))
    print('Theme beats nobody can have (missing details):', json.dumps({k: v for k, v in r['sim']['partial'].items() if v}))
    print('Days each beat was told:', ' '.join(l.replace(' ', '/') for l in r['log']))
    print('errors', g.errors[:5])
    print('ARC CHECK OK' if not r['stalled'] and not g.errors and all(h.endswith(' 6') or h.endswith(' 0') for h in r['home']) else 'ARC CHECK: STALLS')
