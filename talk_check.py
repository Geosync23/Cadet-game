# Starship Cadet: talk check (keep in the repo, next to cadet_test.py and the other checks)
# Checks the Talk a while pack's picker and its save (section 22, the talk engineer; plans/talk-pack-plan.md "Picking
# a talk"), on paper: talkPackPick / talkPackFire stepped over many ship days with every crew member and guest, no walking.
#   (a) the pack is baked: 100 pool talks on ten topics, own talks for the story crew, small talk and the "done" lines
#   (b) no repeats: a talk fires once a save, whoever says it; own talks only from their owner
#   (c) the run-out order: their own talks first (any that's ready), then the pool, then small talk; a guest never draws
#       the pool; small talk is 3-4 lines, about one in four opens with a "done" line, never twice running with one person
#   (d) conditions: tier, !who:, !thread:, rank:, beat:/flag:/mem: gates hold for every talk picked; nothing unfilled
#   (e) the same pick twice (and after a reload of the record); a topic talked about lately goes behind the others
#   (f) the save: save.talks only once a talk has happened, loads back the same, bad entries dropped, small, New game clears
# Setup and environment as for cadet_test.py.
# Run:  python3 talk_check.py BUILD.html
import sys, json, os
exec(open(__file__.replace('talk_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

SAVE_PER = 48            # bytes a fired talk takes in save.talks (an id, its day and crew id); the cap is the whole pack fired
SAVE_SMALL = 2500        # every crew member's small talk noted
ok = True
def fail(msg):
    global ok
    ok = False
    print('FAIL', msg)
def check(cond, msg):
    if not cond: fail(msg)
    return cond

# helpers in the page: everyone who can talk, a clean record, and one pick checked against the run-out order
HELP = r"""(() => {
  window.__TC = {
    people: () => { socInit(); return SOC.crew.filter(p => p.id !== 'you').concat(typeof ROSTER_GUESTS !== 'undefined' ? ROSTER_GUESTS : []); },   // the Envoy too (not in SOC: see the report)
    reset: tier => { SHIP.talks = { fired: {}, small: {} }; for (const p of __TC.people()) { const r = relGet(p.id); r.tier = tier; } },
    filled: (tk, p, t) => talkPackFill(tk, p, { t, trad: talkPackTrad(t) || undefined }),
    whenOk: (tk, p, t) => !tk.when || linesOk(tk.when, p, { t, trad: talkPackTrad(t) || undefined }),
    // what's ready for p at t, before the pick: own talks and pool talks unfired, passing when: and filling
    ready: (p, t) => { const T = SHIP.talks, ok = tk => !T.fired[tk.id] && __TC.whenOk(tk, p, t) && !!__TC.filled(tk, p, t);
      return { own: (TALKS.own[p.id] || []).filter(ok).map(tk => tk.id), pool: p.rank === 'guest' ? [] : TALKS.pool.filter(ok).map(tk => tk.id),
        work: TALK_SOURCES.find(s => s.id === 'work').talks(p).filter(ok).map(tk => tk.id) }; },
  };
})()"""

# steps days: each day at `min`, every person picks and fires; returns the log and any rule broken
RUN = r"""(({ days, min, tier, check, start }) => {
  __TC.reset(tier); const ppl = __TC.people(), log = [], bad = [], firedBy = {}, smalls = {};
  for (let d = start || 1; d < (start || 1) + days; d++) {
    SHIP.time.day = d; SHIP.time.min = min; const t = (d - 1) * 1440 + min;
    for (const p of ppl) {
      const before = check ? __TC.ready(p, t) : null, a = talkPackPick(p, t), b = talkPackPick(p, t);
      if (JSON.stringify(a) !== JSON.stringify(b)) bad.push(`${p.id} day ${d}: two picks differ`);
      if (!a) { bad.push(`${p.id} day ${d}: no pick`); continue; }
      if (a.talk) {
        const id = a.talk.id;
        if (firedBy[id]) bad.push(`${id} again (${firedBy[id]}, then ${p.id} day ${d})`);
        firedBy[id] = p.id + ' day ' + d;
        if (a.src === 'own' && !id.startsWith(p.id + '.')) bad.push(`${p.id} said ${id}, someone else's own talk`);
        if (a.src === 'pool' && p.rank === 'guest') bad.push(`${p.id} (a guest) drew the pool: ${id}`);
        if (before && a.src === 'own' && before.own[0] !== id) bad.push(`${p.id} day ${d}: own talk ${id}, but ${before.own[0]} was first in file order`);
        if (before && a.src === 'pool' && before.own.length) bad.push(`${p.id} day ${d}: pool ${id} while own ${before.own.join(',')} was ready`);
        if (before && a.src === 'work' && !before.work.includes(id)) bad.push(`${p.id} day ${d}: work ${id} wasn't ready`);
        if (before && a.src === 'work' && before.own.length) bad.push(`${p.id} day ${d}: work ${id} while own ${before.own.join(',')} was ready`);
        if (before && a.src === 'pool' && !before.pool.includes(id)) bad.push(`${p.id} day ${d}: pool ${id} wasn't ready`);
        if (!__TC.whenOk(a.talk, p, t)) bad.push(`${p.id} day ${d}: ${id}'s when: fails`);
        const words = [...a.said.lines, a.said.ask, ...['listen', 'share', 'cheer'].flatMap(k => [a.said.replies[k].text, a.said.replies[k].ans])];
        if (words.some(w => typeof w !== 'string' || !w || /[{}]/.test(w))) bad.push(`${p.id} day ${d}: ${id} has a hole or an unfilled placeholder`);
        log.push({ d, p: p.id, id, src: a.src, topic: a.talk.topic, rank: p.rank, thread: (voiceOf(p.id).thread || p.thread || ''), tier: relTier(p.id) });
      } else {
        if (before && (before.own.length || before.pool.length || before.work.length)) bad.push(`${p.id} day ${d}: small talk while ${before.own.length} own, ${before.work.length} work and ${before.pool.length} pool talks were ready`);
        if (a.small.length < 3 || a.small.length > 4) bad.push(`${p.id} day ${d}: ${a.small.length} small talk lines`);
        if (new Set(a.small.map(x => x.text)).size !== a.small.length) bad.push(`${p.id} day ${d}: a small talk line twice`);
        const last = SHIP.talks.small[p.id];
        if (a.done && last && last[1]) bad.push(`${p.id} day ${d}: "talked about everything" twice running`);
        (smalls[p.id] = smalls[p.id] || []).push(a.done ? 1 : 0);
        log.push({ d, p: p.id, small: a.small.map(x => x.text), done: a.done, rank: p.rank });
      }
      talkPackFire(p, a, t);
    }
  }
  return { log, bad, smalls, fired: Object.keys(SHIP.talks.fired).length };
})"""

with sync_playwright() as pw:
    errors = []
    g = Game(pw, sys.argv[1], errors=errors)
    ev = g.ev
    ev(HELP)

    print('(a) The pack, baked:')
    r = ev("""(() => ({ pool: TALKS.pool.length, topics: [...new Set(TALKS.pool.map(t => t.topic))].sort(), own: Object.fromEntries(Object.entries(TALKS.own).map(([k, v]) => [k, v.length])),
      small: Object.fromEntries(Object.entries(TALKS.small).map(([k, v]) => [k, v.length])), fns: [typeof talkPackPick, typeof talkPackFire, typeof talksClean].join(' '),
      ownersAboard: Object.keys(TALKS.own).filter(id => !linesWho(id)) }))()""")
    print(f"  {r['pool']} pool talks on {len(r['topics'])} topics; own: {r['own']}; small: {r['small']}")
    check(r['fns'] == 'function function function', 'the picker is missing: ' + r['fns'])
    check(r['pool'] >= 100 and len(r['topics']) == 10, 'the pool is not baked (100 talks on ten topics)')
    check(len(r['own']) >= 15 and all(n >= 4 for n in r['own'].values()), 'own talks missing')
    check(all(r['small'].get(k, 0) > 0 for k in ('small', 'done', 'small.saruth', 'done.saruth')), 'small talk kinds missing')
    check(not r['ownersAboard'], f"own talks for people who aren't crew or guests: {r['ownersAboard']}")

    print('(b, c) Friends with everyone: 40 days of talks at 12:00, each checked against what was ready:')
    r = ev(f"({RUN})({{ days: 40, min: 720, tier: 3, check: true }})")
    for b in r['bad'][:12]: print('   ', b)
    check(not r['bad'], f"{len(r['bad'])} rules broken")
    talks = [x for x in r['log'] if 'id' in x]
    small = [x for x in r['log'] if 'small' in x]
    pool = [x for x in talks if x['src'] == 'pool']
    work = [x for x in talks if x['src'] == 'work']
    print(f"  {len(talks)} talks fired ({len(pool)} pool, {len(work)} work, {len(talks) - len(pool) - len(work)} own), {len(small)} small talks; record {r['fired']}")
    check(len(pool) == len(set(x['id'] for x in pool)), 'a pool talk fired twice')
    first_small = min((x['d'] for x in small if x['rank'] != 'guest'), default=None)
    print(f"  the pool ran out on day {max(x['d'] for x in pool) if pool else None}; crew small talk from day {first_small}")
    dn = [v for vs in r['smalls'].values() for v in vs]
    share = sum(dn) / len(dn) if dn else 0
    print(f"  small talk opening with \"done\": {sum(dn)} of {len(dn)} ({share:.0%})")
    check(dn and .12 <= share <= .35, f'"done" opens {share:.0%} of small talk (about one in four wanted)')
    sar = [x for x in r['log'] if x['p'] == 'saruth']
    print(f"  Saruth: {[x.get('id') or ('small: ' + x['small'][0]) for x in sar[:6]]}")
    check(sar and all(x.get('src') != 'pool' for x in sar), 'Saruth drew the pool')
    sar_small = [x for x in sar if 'small' in x]
    if sar_small:
        allowed = set(ev("TALKS.small['small.saruth'].concat(TALKS.small['done.saruth']).map(e => e.text)"))
        check(all(t in allowed for x in sar_small for t in x['small']), 'Saruth used crew small talk (contractions)')
    ownorder = {}
    for x in talks:
        if x['src'] == 'own': ownorder.setdefault(x['p'], []).append(x['id'])
    files = ev("Object.fromEntries(Object.entries(TALKS.own).map(([k, v]) => [k, v.map(t => t.id)]))")
    for p, ids in ownorder.items():
        check(ids == [i for i in files[p] if i in ids], f'{p}: own talks out of file order: {ids}')

    print('(d) Conditions, strangers to friends:')
    cond = ev("""(() => { const by = Object.fromEntries(TALKS.pool.concat(...Object.values(TALKS.own), ...Object.values(TALKS.work || {})).map(t => [t.id, t.when || {}])); return by; })()""")
    allbad = []
    for tier in (0, 1, 2):
        r = ev(f"({RUN})({{ days: 6, min: 720, tier: {tier}, check: true }})")
        allbad += r['bad']
        tl = [x for x in r['log'] if 'id' in x]
        over = [x['id'] for x in tl if cond[x['id']].get('tier', [0, 4])[0] > tier]
        notwho = [x for x in tl if x['p'] in str(cond[x['id']].get('not', {}).get('who', '')).split('|')]
        thr = [x for x in tl if x['thread'] and x['thread'] in str(cond[x['id']].get('not', {}).get('thread', '')).split('|')]
        rank = [x for x in tl if 'rank' in cond[x['id']] and x['rank'] not in str(cond[x['id']]['rank']).split('|')]
        print(f"  tier {tier}: {len(tl)} talks; over their tier {len(over)}, !who: broken {len(notwho)}, !thread: broken {len(thr)}, rank: broken {len(rank)}")
        check(not (over or notwho or thr or rank), f'tier {tier}: a condition broken: {over[:3]} {notwho[:2]} {thr[:2]} {rank[:2]}')
        if tier == 0:
            check(all(not cond[x['id']].get('tier') or cond[x['id']]['tier'][0] == 0 for x in tl), 'a stranger had a talk for acquaintances')
    for b in allbad[:8]: print('   ', b)
    check(not allbad, f'{len(allbad)} rules broken with strangers and acquaintances')
    r = ev("""(() => { __TC.reset(3); const t = 20 * 1440 + 720, out = {};
      for (const [who, id] of [['rina', 'rina.gran'], ['holt', 'holt.saruth'], ['halloran-emeka', 'halloran-emeka.mug-rack'], ['torres-zeke', 'torres-zeke.scarf-rows']]) {
        const tk = TALKS.own[who].find(x => x.id === id); out[id] = tk ? __TC.whenOk(tk, socP(who), t) : 'missing'; }
      return out; })()""")
    print(f"  arc-gated own talks on a fresh save (want all false): {r}")
    check(all(v is False for v in r.values()), 'an arc-gated own talk is ready before its beat or flag')
    r = ev("""(() => { __TC.reset(3); const t = 20 * 1440 + 720, p = TALKS.pool.find(x => x.id === 'pool.tradition.coming'), q = __TC.people()[0];
      const name = talkPackTrad(t), f = __TC.filled(p, q, t); return { name, line: f && f.lines[0] }; })()""")
    print(f"  {{trad}}: the next tradition is {r['name']!r}: {r['line']!r}")
    check(not r['name'] or (r['line'] and r['name'] in r['line']), '{trad} not filled with the next tradition')

    print('(e) A topic talked about lately goes behind the others:')
    r = ev("""(() => { __TC.reset(3); const p = __TC.people().find(q => !TALKS.own[q.id] && q.rank !== 'guest'), t = 5 * 1440 + 720, out = [];
      for (let k = 0; k < 6; k++) { const a = talkPackPick(p, t + k * 1440); if (!a || !a.talk) break; out.push(a.talk.topic); talkPackFire(p, a, t + k * 1440); }
      return { p: p.id, topics: out }; })()""")
    print(f"  {r['p']}, six days running: {r['topics']}")
    check(len(r['topics']) == 6 and len(set(r['topics'])) == 6, 'the same pool topic twice within TALK_TOPIC_DAYS')

    print('(f) The save:')
    r = ev("""(() => { SHIP.talks = { fired: {}, small: {} }; const s0 = {}; for (const f of SAVE_EXTRA) { try { f(s0); } catch (e) { } }
      __TC.reset(3); const ppl = __TC.people(); for (let d = 1; d <= 60; d++) for (const p of ppl) { const t = (d - 1) * 1440 + 720; talkPackFire(p, talkPackPick(p, t), t); }
      const s = {}; for (const f of SAVE_EXTRA) { try { f(s); } catch (e) { } }
      const back = talksClean(JSON.parse(JSON.stringify(s.talks)));
      const junk = talksClean({ fired: { a: [1, 'x'], b: 'no', c: [1.5, 'y'], d: [2] }, small: { x: [3, 1], y: ['z'], z: [4, 7] } });
      const T = SHIP.talks, keep = JSON.stringify(T); SHIP.talks = null; const fresh = talksState(); const fromNone = JSON.stringify(fresh) === '{"fired":{},"small":{}}';
      SHIP.talks = JSON.parse(keep); const p = ppl[3], a1 = JSON.stringify(talkPackPick(p, 61 * 1440 + 720)); SHIP.talks = talksClean(JSON.parse(JSON.stringify(s.talks))); const a2 = JSON.stringify(talkPackPick(p, 61 * 1440 + 720));
      linesNew(); const cleared = JSON.stringify(SHIP.talks) === '{"fired":{},"small":{}}'; const s2 = {}; for (const f of SAVE_EXTRA) { try { f(s2); } catch (e) { } }
      return { none: !('talks' in s0), size: JSON.stringify(s.talks).length, fired: Object.keys(s.talks.fired).length, small: Object.keys(s.talks.small).length,
        same: JSON.stringify(back) === JSON.stringify(s.talks), junk, fromNone, reload: a1 === a2, cleared, none2: !('talks' in s2), sample: JSON.stringify(s.talks).slice(0, 160) }; })()""")
    print(f"  before any talk: no save.talks {r['none']}; after 60 days: {r['fired']} fired, {r['small']} small, {r['size']} bytes: {r['sample']}...")
    print(f"  loads back the same {r['same']}; junk read back as {r['junk']}; a reload picks the same {r['reload']}; New game clears {r['cleared']} (and no save.talks {r['none2']})")
    check(r['none'] and r['none2'], 'save.talks is written before any talk happened')
    check(r['same'] and r['reload'] and r['fromNone'], 'the record does not load back the same')
    check(r['junk'] == {'fired': {'a': [1, 'x']}, 'small': {'x': [3, 1], 'z': [4, 1]}}, f"bad entries not dropped: {r['junk']}")
    cap = SAVE_PER * ev("TALKS.pool.length + Object.values(TALKS.own).flat().length + Object.values(TALKS.work || {}).flat().length") + SAVE_SMALL
    check(r['size'] <= cap, f"save.talks is {r['size']} bytes (at most {cap}: {SAVE_PER} a talk in the pack, {SAVE_SMALL} for small talk)")
    print(f"  the cap with this pack: {cap} bytes")
    check(r['cleared'], 'New game (linesNew) does not clear the record')

    print('(h) Work pools (plans/work-pools-plan.md): own, then work and shared taking turns, then small talk:')
    r = ev("""(() => { const keep = TALKS.work, real = TALKS.work && Object.keys(TALKS.work).length;
      if (!real) TALKS.work = { works: TALKS.pool.filter(t => !/[{}]/.test([...t.lines, t.ask, ...Object.values(t.replies).map(r => r.ans)].map(x => x.text).join(' '))).slice(0, 4).map((t, i) => ({ ...t, id: 'work.works.stand-in-' + i, topic: 'work', when: undefined })) };   // stand-ins until TW1's files are baked
      __TC.reset(3); const out = { real: !!real, pools: Object.fromEntries(Object.entries(TALKS.work).map(([k, v]) => [k, v.length])), seq: [], bad: [] };
      const w = __TC.people().filter(p => TALK_WORK_POOLS[p.dept] && TALKS.work[TALK_WORK_POOLS[p.dept]] && !TALKS.own[p.id]);
      const p = w[0], other = __TC.people().find(q => q.rank !== 'guest' && !TALK_WORK_POOLS[q.dept] || (TALK_WORK_POOLS[q.dept] && !TALKS.work[TALK_WORK_POOLS[q.dept]]));
      out.p = p && p.id; out.pool = p && TALK_WORK_POOLS[p.dept];
      const ready = p ? TALK_SOURCES.find(s => s.id === 'work').talks(p).filter(tk => __TC.whenOk(tk, p, 720) && __TC.filled(tk, p, 720)).length : 0; out.ready = ready;
      for (let d = 1; p && d <= 2 * ready + 6; d++) { const t = (d - 1) * 1440 + 720, a = talkPackPick(p, t); if (!a) break; out.seq.push(a.talk ? a.src : 'small'); talkPackFire(p, a, t); }
      const seq = out.seq, k = seq.filter(s => s === 'work').length;
      out.alternates = seq.slice(0, 2 * k).every((s, i) => s === (i % 2 ? 'pool' : 'work')) && !seq.slice(2 * k).includes('work');   // work first (neither had), then turns
      out.allWork = k >= ready && new Set(Object.keys(SHIP.talks.fired).filter(id => id.startsWith('work.'))).size === k;   // every one ready at the start (more may open with time)
      out.workIds = Object.keys(SHIP.talks.fired).filter(id => id.startsWith('work.')).every(id => SHIP.talks.fired[id][1] === p.id);
      out.guest = (typeof ROSTER_GUESTS !== 'undefined' ? ROSTER_GUESTS : []).every(g => !TALK_SOURCES.find(s => s.id === 'work').talks(g).length);
      out.other = other ? [other.id, other.dept, TALK_SOURCES.find(s => s.id === 'work').talks(other).length] : null;
      __TC.reset(3); const q = w[1] || w[0]; for (let d = 1; d <= 3; d++) { const t = (d - 1) * 1440 + 720; talkPackFire(q, talkPackPick(q, t), t); }
      const again = talkPackPick(p, 10 * 1440 + 720); out.shared = Object.keys(SHIP.talks.fired).filter(id => id.startsWith('work.')).length;
      out.notTwice = !again || !again.talk || !SHIP.talks.fired[again.talk.id];
      TALKS.work = keep; return out; })()""")
    print(f"  {'the real pools' if r['real'] else 'stand-ins'} {r['pools']}; {r['p']} ({r['pool']}, {r['ready']} work talks ready), {len(r['seq'])} days: {r['seq'][:12]}... {r['seq'][-6:]}")
    print(f"  alternates {r['alternates']}, every work talk once {r['allWork']}, only from them {r['workIds']}; guests none {r['guest']}; no pool for {r['other']}")
    check(r['p'] and all(r['pools'].values()), f"nobody to test the work pool with, or an empty pool: {r['pools']}")
    check(r['alternates'], f"work and shared don't take turns: {r['seq'][:12]}")
    check(r['allWork'] and r['workIds'], 'a work talk twice, or not all of them')
    check(r['guest'], 'a guest drew a work pool')
    check(r['notTwice'], 'a work talk fired with one person was offered by another')

    for e in errors: fail(f'page error: {e}')
    g.close()

    # (g) in the game, on a phone (390 x 844): Talk a while through the chat card (section 20 asks section 22): the
    # pack's opener, its more lines, the question with its three replies as buttons, the answer; small talk once
    # everything's used (no buttons but Stop); --shots DIR saves the card at each step
    print('(g) Talk a while on the chat card, on a phone:')
    shots = sys.argv[sys.argv.index('--shots') + 1] if '--shots' in sys.argv else None
    errors2 = []
    g = Game(pw, sys.argv[1], w=390, h=844, errors=errors2)
    g.ev("(() => { SHIP.time.day = 3; SHIP.time.min = 12 * 60 + 30; })()")
    g.step(3)
    def shot(name):
        if shots:
            os.makedirs(shots, exist_ok=True); g.shot(os.path.join(shots, name + '.png'))
    PLAY = r"""(({ id, tier, fireAll }) => {
      const p = SOC.crew[SOC.idx.get(id)], r = relGet(p.id), t0 = shipNow(); r.tier = tier; r.talkDay = 0; r.chatDay = 0;
      if (fireAll) { SHIP.talks = { fired: {}, small: {} }; for (const tk of TALKS.pool.concat(TALKS.own[id] || [], ...Object.values(TALKS.work || {}))) SHIP.talks.fired[tk.id] = [1, 'x']; }
      const a = DECK_CREW.find(x => x.p === p); if (a) { player.obj.position.set(a.x + .9, 0, a.z + .9); target.copy(player.obj.position).setY(.7); }
      chatClose(); CHAT = { p, line: { text: '', say: true }, ask: false, fav: null, at: shipNow(), reach: 99, checked: Math.floor(shipNow()) + 999 }; chatShow();
      chatDo('talk'); const T = CHAT.talk, card = () => [...document.querySelectorAll('#chat button, #chat .btns button')].map(b => b.textContent).filter(x => x !== '×'), said = () => CHAT.line.text;
      const out = { pack: T.pack ? { id: T.pack.id, small: !!T.pack.small, done: !!T.pack.done, lines: T.pack.lines, ask: T.pack.ask, replies: T.pack.replies } : null, steps: [[0, said(), card()]] };
      for (let k = 1; k <= 40 && !T.end; k++) { setShipNow(t0 + k * .5); CHAT.checked = Math.floor(shipNow()) + 999; talkStep(CHAT);
        const l = said(); if (l !== out.steps[out.steps.length - 1][1]) out.steps.push([T.mins, l, card()]);
        if (T.ask) { out.asked = [T.mins, said(), card()]; break; } }
      return out; })"""
    r = g.ev(f"({PLAY})({{ id: 'tomas', tier: 1 }})")
    P = r['pack']
    print(f"  Tomas: {P['id'] if P else None}")
    for st in r['steps']: print(f"    {st[0]:>5} min: {st[1]!r}")
    check(P and not P['small'] and P['id'].startswith('tomas.'), f"Tomas's first talk isn't his own: {P}")
    if P and not P['small']:
        said = [x[1] for x in r['steps']]
        check(any(P['lines'][0] in x for x in said[:1]), 'the opener is not the pack talk\'s first line')
        check(all(l in said for l in P['lines'][1:]), "the pack's more lines were not said before the question")
        check(r.get('asked') and r['asked'][1] == P['ask'], f"the question is not the pack's ask: {r.get('asked')}")
        want = [P['replies'][k]['text'] for k in ('listen', 'share', 'cheer')]
        check(r.get('asked') and r['asked'][2][:3] == want, f"the reply buttons are not the pack's: {r.get('asked') and r['asked'][2]} (want {want})")
        print(f"    the question: {r['asked'][1]!r}; buttons {r['asked'][2]}")
        shot('talk-question')
        k = g.ev("talkSuits(CHAT.p)")
        a = g.ev(f"(() => {{ chatDo('reply:{k}'); return [CHAT.line.text, CHAT.talk.pack.replies['{k}'].ans, Object.keys(SHIP.talks.fired).includes(CHAT.talk.pack.id)]; }})()")
        print(f"    replied {k}: {a[0]!r}")
        check(a[0] == a[1], f"the answer is not the pack's: {a[0]!r} (want {a[1]!r})")
        check(a[2], 'the talk was not fired')
        shot('talk-answer')
    r = g.ev(f"({PLAY})({{ id: 'tomas', tier: 1 }})")
    check(r['pack'] and r['pack']['id'] != P['id'], 'the same talk again the next time')
    r = g.ev(f"({PLAY})({{ id: 'abara-rosa', tier: 2, fireAll: true }})")
    print(f"  everything used, Abara: small talk {r['pack'] and r['pack']['small']}, done opener {r['pack'] and r['pack'].get('done')}")
    for st in r['steps']: print(f"    {st[0]:>5} min: {st[1]!r} {st[2]}")
    check(r['pack'] and r['pack']['small'], 'no small talk once everything is used')
    said = [x[1] for x in r['steps']]
    check(r['pack'] and all(sum(l in x for x in said) == 1 for l in r['pack']['lines']), 'a small talk line said twice in one talk')
    check(not r.get('asked') and all(x[2][:1] == ['Stop'] for x in r['steps'] if x[0] < 15), 'small talk asked a question or showed reply buttons')
    shot('talk-small')
    for e in errors2: fail(f'page error: {e}')
    g.close()

print('TALK CHECK OK' if ok else 'TALK CHECK FAILED')
sys.exit(0 if ok else 1)
