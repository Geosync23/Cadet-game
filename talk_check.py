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
#   (i) repeats over Days 1-3 with a chatty player: filler lines a talk, the most any everyday line comes (DL1, note 21)
#   (j) own pools only (patch 0.92.3 item 15): an "only: own" person never draws the pool, a work pool or small talk,
#       their first-talk scene comes first and is had only once answered, then their own talks, then the least lately
#       had again; their talk.* lines are their own; nobody else's picks change (stand-ins when the content has none)
#   (k) the chat card's opener (patch 0.92.5 item 5): tapped hour after hour, nobody says a greet/near/life line again
#       until every one that fits has been said, their own first, then their voice template's, then the shared ones;
#       a peek marks nothing; the record saves, loads back and a New game clears it
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
      const only = talkOnlyOwn(p);                        // "only: own" (item 15): checked in (j); here only that they keep to their own
      if (only && (!a.talk || a.src !== 'own' || !a.talk.id.startsWith(p.id + '.'))) bad.push(`${p.id} day ${d}: "only: own" but ${a.talk ? a.src + ' ' + a.talk.id : 'small talk'}`);
      if (a.talk) {
        const id = a.talk.id;
        if (firedBy[id] && !(only && a.again)) bad.push(`${id} again (${firedBy[id]}, then ${p.id} day ${d})`);
        firedBy[id] = p.id + ' day ' + d;
        if (a.src === 'own' && !id.startsWith(p.id + '.')) bad.push(`${p.id} said ${id}, someone else's own talk`);
        if (a.src === 'pool' && p.rank === 'guest') bad.push(`${p.id} (a guest) drew the pool: ${id}`);
        if (before && a.src === 'own' && !a.again && !a.talk.first && before.own.filter(x => !(TALKS.own[p.id].find(tk => tk.id === x) || {}).first)[0] !== id) bad.push(`${p.id} day ${d}: own talk ${id}, but ${before.own[0]} was first in file order`);
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
      talkPackFire(p, a && a.talk && a.talk.first ? { ...a, answered: true } : a, t);   // a first-talk scene: as if answered
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
      work: Object.fromEntries(Object.entries(TALKS.work || {}).map(([k, v]) => [k, v.length])), small: Object.fromEntries(Object.entries(TALKS.small).map(([k, v]) => [k, v.length])), fns: [typeof talkPackPick, typeof talkPackFire, typeof talksClean].join(' '),
      ownersAboard: Object.keys(TALKS.own).filter(id => !linesWho(id)) }))()""")
    print(f"  {r['pool']} pool talks on {len(r['topics'])} topics; own: {r['own']}; work: {r['work']}; small: {r['small']}")
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
    # (since TR1's W1 "done" waits until nothing is left to come, and a few talks wait on a friend or a story beat here,
    # so its one-in-four share is checked below with everything used)
    never = ev("TALKS.pool.concat(...Object.values(TALKS.work || {})).map(t => t.id).filter(id => !SHIP.talks.fired[id])")
    print(f"  never fired with everyone a friend ({len(never)}): {', '.join(never)}")
    sar = [x for x in r['log'] if x['p'] == 'saruth']
    print(f"  Saruth: {[x.get('id') or ('small: ' + x['small'][0]) for x in sar[:6]]}")
    check(sar and all(x.get('src') != 'pool' for x in sar), 'Saruth drew the pool')
    sar_small = [x for x in sar if 'small' in x]
    if sar_small:
        allowed = set(ev("TALKS.small['small.saruth'].concat(TALKS.small['done.saruth']).map(e => e.text)"))
        check(all(t in allowed for x in sar_small for t in x['small']), 'Saruth used crew small talk (contractions)')
    ownorder = {}
    for x in talks:
        if x['src'] == 'own' and x['id'] not in ownorder.get(x['p'], []): ownorder.setdefault(x['p'], []).append(x['id'])   # the first time each (an "only: own" person's come round again)
    files = ev("Object.fromEntries(Object.entries(TALKS.own).map(([k, v]) => [k, v.map(t => t.id)]))")
    for p, ids in ownorder.items():
        skip = set(ev(f"(TALKS.own[{json.dumps(p)}] || []).filter(t => t.first || Object.keys(t.when || {{}}).some(k => k !== 'tier')).map(t => t.id)"))   # a first-talk scene comes first; a talk waiting on a day, a time or a mood comes when it's ready (each pick is checked against file order above)
        ids = [i for i in ids if i not in skip]
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

    print('"Talked about everything" only once nothing is left to come (TR1\'s W1): a stranger, 60 days, the pool still waiting:')
    r = ev("""(() => { __TC.reset(0); const p = __TC.people().find(q => q.id === 'abara-rosa') || __TC.people().find(q => !TALKS.own[q.id] && q.rank !== 'guest'); let dn = 0, smalls = 0;
      for (let d = 1; d <= 60; d++) { const t = (d - 1) * 1440 + 720, a = talkPackPick(p, t); if (a && !a.talk) { smalls++; if (a.done) dn++; } talkPackFire(p, a, t); }
      const waiting = TALK_SOURCES.flatMap(s => s.talks(p)).filter(tk => !SHIP.talks.fired[tk.id] && talkPackFits(tk, p, { t: 60 * 1440 })).length;
      for (const s of TALK_SOURCES) for (const tk of s.talks(p)) SHIP.talks.fired[tk.id] = SHIP.talks.fired[tk.id] || [1, 'x'];   // then everything used
      let dn2 = 0; for (let d = 61; d <= 120; d++) { const t = (d - 1) * 1440 + 720, a = talkPackPick(p, t); if (a && a.done) dn2++; talkPackFire(p, a, t); }
      return { p: p.id, smalls, dn, waiting, dn2 }; })()""")
    print(f"  {r['p']}: {r['smalls']} small talks with {r['waiting']} talks still waiting, {r['dn']} \"done\" openers; with everything used, {r['dn2']} in 60 days")
    check(r['waiting'] > 0 and r['dn'] == 0, '"talked about everything" while talks were still waiting')
    check(.12 <= r['dn2'] / 60 <= .35, f'with everything used "done" opens {r["dn2"]} of 60 small talks (about one in four wanted, never twice running)')

    print('(e) A topic talked about lately goes behind the others:')
    r = ev("""(() => { __TC.reset(3); const p = __TC.people().find(q => !TALKS.own[q.id] && q.rank !== 'guest'), t = 5 * 1440 + 720, out = [];
      for (let k = 0; out.length < 6 && k < 14; k++) { const a = talkPackPick(p, t + k * 1440); if (!a || !a.talk) break; if (a.src === 'pool') out.push(a.talk.topic); talkPackFire(p, a, t + k * 1440); }   // the shared pool's topics (work talks take turns in between)
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

    print('(j) Own pools only (item 15): the "only: own" people and their first-talk scene:')
    r = ev("""(() => { const keepOnly = TALKS.only, keepOwn = TALKS.own.marrow, keepV = VOICE.marrow && VOICE.marrow.lines && VOICE.marrow.lines['talk.filler'];
      const real = Array.isArray(TALKS.only) && TALKS.only.length, out = { real: !!real, bad: [] };
      const others = __TC.people().filter(p => !(real && TALKS.only.includes(p.id)) && p.id !== 'marrow'), before = {};
      __TC.reset(3); for (const p of others.slice(0, 12)) before[p.id] = JSON.stringify(talkPackPick(p, 4 * 1440 + 720));
      if (!real) { TALKS.only = ['marrow']; const w = { ...TALKS.own.marrow[0], id: 'marrow.stand-in-welcome', first: 1 }; delete w.when; TALKS.own.marrow = TALKS.own.marrow.concat(w); }   // stand-ins until the writers' files are baked
      out.only = TALKS.only.slice();
      __TC.reset(3); out.othersSame = others.slice(0, 12).every(p => before[p.id] === JSON.stringify(talkPackPick(p, 4 * 1440 + 720)));
      for (const id of out.only) {
        const p = socP(id) || linesWho(id), own = TALKS.own[id] || [], first = own.find(tk => tk.first);
        if (!p) { out.bad.push(id + ': not aboard'); continue; }
        if (own.filter(tk => tk.first).length > 1) out.bad.push(id + ': two first-talk scenes');
        for (const tier of [0, 3]) {
          __TC.reset(tier); const ctx = t => ({ t, trad: talkPackTrad(t) || undefined }), seq = [];
          for (let d = 1; d <= 3 * own.length + 6; d++) {
            const t = (d - 1) * 1440 + 720, a = talkPackPick(p, t), T = SHIP.talks;
            if (!a || !a.talk) { out.bad.push(`${id} tier ${tier} day ${d}: ${a ? 'small talk' : 'nothing'}`); talkPackFire(p, a, t); continue; }
            if (a.src !== 'own' || !a.talk.id.startsWith(id + '.')) out.bad.push(`${id} day ${d}: ${a.src} ${a.talk.id}`);
            const ready = own.filter(tk => (!tk.when || linesOk(tk.when, p, ctx(t))) && talkPackFill(tk, p, ctx(t)));
            if (first && ready.includes(first) && !T.fired[first.id] && a.talk !== first) out.bad.push(`${id} day ${d}: ${a.talk.id} before the first-talk scene`);
            if (a.talk.first && T.fired[a.talk.id]) out.bad.push(`${id} day ${d}: the first-talk scene again`);
            if (a.again) { const fresh = ready.filter(tk => !tk.first && !T.fired[tk.id]); if (fresh.length) out.bad.push(`${id} day ${d}: ${a.talk.id} again while ${fresh[0].id} was never had`);
              const older = ready.filter(tk => !tk.first && T.fired[tk.id] && T.fired[tk.id][0] < T.fired[a.talk.id][0]); if (older.length) out.bad.push(`${id} day ${d}: ${a.talk.id} again before ${older[0].id}, had longer ago`); }
            else if (T.fired[a.talk.id]) out.bad.push(`${id} day ${d}: ${a.talk.id} twice without being a repeat`);
            seq.push(a.talk.id.slice(id.length + 1) + (a.again ? '*' : ''));
            if (a.talk.first && d === 1) { talkPackFire(p, a, t); const b = talkPackPick(p, t + 1440); if (!b || b.talk !== first) out.bad.push(`${id}: the first-talk scene was had without being answered`); }
            talkPackFire(p, a.talk.first ? { ...a, answered: true } : a, t);
          }
          if (tier === 3) out[id] = seq;
          const minGap = (() => { const last = {}; let g = 1e9; seq.forEach((s, i) => { const k = s.replace('*', ''); if (k in last) g = Math.min(g, i - last[k]); last[k] = i; }); return g; })();
          out[id + '.gap.' + tier] = minGap;
        }
        for (const k of ['talk.start', 'talk.sit', 'talk.filler', 'talk.end', 'talk.stop']) { const l = lineFor(p, k, { t: 720, tier: 3, peek: true }), mine = ((VOICE[id] && VOICE[id].lines && VOICE[id].lines[k]) || []).map(e => e.id);
          if (l && !mine.includes(l.id)) out.bad.push(`${id}: ${k} from the shared lines: ${l.text}`); }
      }
      TALKS.only = keepOnly; TALKS.own.marrow = keepOwn; return out; })()""")
    print(f"  {'the real list' if r['real'] else 'stand-ins'}: {r['only']}; nobody else's pick changes {r['othersSame']}")
    for id in r['only']:
        print(f"  {id}, friends ({len(r.get(id, []))} days; * = had again): {' '.join(r.get(id, [])[:24])}{' ...' if len(r.get(id, [])) > 24 else ''}")
        print(f"    the fewest days between the same talk: strangers {r.get(id + '.gap.0')}, friends {r.get(id + '.gap.3')}")
    for b in r['bad'][:12]: print('   ', b)
    check(not r['bad'], f"{len(r['bad'])} own-pool rules broken")
    check(r['othersSame'], 'an "only: own" list changed someone else\'s pick')

    print('(k) The chat card\'s opener, tapped hour after hour (item 5):')
    r = ev("""(() => { socInit(); const out = { people: [], bad: [] }, fresh = typeof LINE_FRESH_KINDS !== 'undefined';
      const ppl = ['torres-zeke', 'mensah', 'tomas'].map(id => socP(id)).concat(SOC.crew.filter(p => p.id !== 'you' && !(VOICE[p.id] && VOICE[p.id].lines && VOICE[p.id].lines.greet)).slice(0, 2));
      if (typeof SHIP.fresh !== 'undefined') SHIP.fresh = {};
      for (const p of ppl) for (const kind of ['greet', 'near']) {
        const r = relGet(p.id); r.tier = 1;
        const v = VOICE[p.id], tp = VOICE_TEMPLATES[(v && v.tpl) || p.tpl], t0 = 3 * 1440 + 10 * 60, ctx = t => ({ t, tier: 1 });
        const lists = [['own', (v && v.lines && v.lines[kind]) || []], ['tpl', (tp && tp.lines && tp.lines[kind]) || []], ['bank', LINES[kind] || []]];
        const fits = lists.map(([src, l]) => [src, l.filter(e => lineQuick(e, p, ctx(t0)) && linesOk(e, p, ctx(t0))).map(e => e.id)]);
        const n = fits.reduce((a, x) => a + x[1].length, 0), seq = [], src = {}; for (const [k, ids] of fits) for (const id of ids) src[id] = k;
        const pk = lineFor(p, kind, { ...ctx(t0), peek: true }), pk2 = lineFor(p, kind, { ...ctx(t0), peek: true });
        if (fresh && pk && pk2 && pk.id !== pk2.id) out.bad.push(`${p.id} ${kind}: a peek marked its line`);
        // one tap an hour from 10:00 (time: conditions change, so what fits is worked out at each tap): a line said
        // before only once nothing that fits is still unsaid; never a template or shared one while one of theirs fits unsaid
        const rank = { own: 0, tpl: 1, bank: 2 }, said = new Set(); let firstAgain = -1, backwards = -1, tplHeard = 0;
        for (let i = 0; i < Math.min(n + 4, 70); i++) { const t = t0 + i * 60, l = lineFor(p, kind, ctx(t)); if (!l) continue;
          const now = lists.flatMap(([s, ls]) => ls.filter(e => lineQuick(e, p, ctx(t)) && linesOk(e, p, ctx(t)) && linesFill(e.text, p, ctx(t)) != null).map(e => [s, e.id]));   // what they could say now (a {room} line needs a room)
          if (now.every(x => said.has(x[1]))) for (const x of now) said.delete(x[1]);   // all said: they start again (as lineFor does)
          const unsaid = now.filter(x => !said.has(x[1]));
          const mine = now.find(x => x[1] === l.id), best = Math.min(...unsaid.map(x => rank[x[0]]));
          if (said.has(l.id) && unsaid.length && firstAgain < 0) firstAgain = i;
          if (mine && unsaid.length && rank[mine[0]] > best && backwards < 0) backwards = i;
          if (mine && mine[0] === 'tpl') tplHeard++; seq.push(l.id); said.add(l.id); }
        out.people.push({ id: p.id, kind, own: fits[0][1].length, tpl: fits[1][1].length, bank: fits[2][1].length, said: seq.length, firstAgain, tplHeard, backwards });
      }
      const s = {}; for (const f of SAVE_EXTRA) { try { f(s); } catch (e) { } }
      out.saved = s.fresh ? JSON.stringify(s.fresh).length : 0; out.keys = s.fresh ? Object.keys(s.fresh).length : 0;
      if (fresh) { out.back = JSON.stringify(freshClean(JSON.parse(JSON.stringify(s.fresh || {})))) === JSON.stringify(SHIP.fresh);
        out.junk = JSON.stringify(freshClean({ 'a|greet': 'zz', 'b|greet': 7, 'c': '1', 'd|near': '1v' }));
        linesNew(); out.cleared = JSON.stringify(SHIP.fresh) === '{}'; }
      return out; })()""")
    for x in r['people']:
        print(f"  {x['id']:16} {x['kind']:5}: fits own {x['own']}, template {x['tpl']}, shared {x['bank']}; {x['said']} taps, first repeat at {x['firstAgain']}, template lines heard {x['tplHeard']}{', OUT OF ORDER at ' + str(x['backwards']) if x['backwards'] > 0 else ''}")
        check(x['firstAgain'] == -1, f"{x['id']} {x['kind']}: a line again at tap {x['firstAgain']} with {x['own'] + x['tpl'] + x['bank']} that fit")
        check(x['backwards'] <= 0, f"{x['id']} {x['kind']}: a template or shared line before their own were all said")
        check(not x['tpl'] or x['said'] < x['own'] + 1 or x['tplHeard'] > 0, f"{x['id']} {x['kind']}: their template's lines never heard")
    for b in r['bad']: fail(b)
    print(f"  the record: {r['keys']} person-kinds, {r['saved']} bytes; loads back {r.get('back')}; junk read back as {r.get('junk')}; New game clears {r.get('cleared')}")
    check(r.get('back') and r.get('cleared') and r.get('junk') == '{"d|near":"1v"}', 'the opener record does not save, load back or clear')
    check(r['saved'] < 3000, f"the opener record is {r['saved']} bytes for a handful of people")

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
    # the first-talk scene on the card (item 15): their own first words, no hello in front; walk off before the
    # question and it comes again; answered, it's had
    STAND = "(() => { if (!(Array.isArray(TALKS.only) && TALKS.only.includes('marrow'))) { TALKS.only = (TALKS.only || []).concat('marrow'); } if (!TALKS.own.marrow.some(tk => tk.first)) { const w = { ...TALKS.own.marrow[0], id: 'marrow.stand-in-welcome', first: 1 }; delete w.when; TALKS.own.marrow = TALKS.own.marrow.concat(w); } SHIP.talks = { fired: {}, small: {} }; return TALKS.own.marrow.find(tk => tk.first).id; })()"
    fid = g.ev(STAND)
    # stand-in own card lines for her (RV13): a hello the first-talk scene must not have in front, and the own lines the
    # card may show; with the talkStart / talkNext hooks off a hello or her usual chat would show up
    OWNL = g.ev("""(() => { const v = VOICE.marrow; v.lines = v.lines || {}; const mk = (k, i) => ({ ...LINES[k][0], id: 'standin.' + k + '.' + i, text: 'Stand-in own ' + k + ' line ' + i + '.' });
      for (const k of ['talk.start', 'talk.sit']) if (!(v.lines[k] || []).length) v.lines[k] = [mk(k, 1)];
      return Object.keys(v.lines).filter(k => k.startsWith('talk.')).flatMap(k => v.lines[k].map(e => e.text)); })()""")
    def only_own(r, who):                                 # every line before the question: the talk's, one of her own talk.* lines (filled), or the ask
        P = r['pack']; allowed = P['lines'] + [P['ask']]
        bad = [x[1] for x in r['steps'] if x[1] not in allowed and not any(x[1] == o or x[1].endswith(' ' + P['lines'][0]) and x[1].startswith(o) for o in OWNL) and not (x[1] in OWNL)]
        check(not bad, f'{who}: lines that are not her own before the question: {bad[:3]}')
    r = g.ev(f"({PLAY})({{ id: 'marrow', tier: 0 }})")
    P = r['pack']
    print(f"  Marrow, the first time: {P and P['id']} (want {fid})")
    for st in r['steps']: print(f"    {st[0]:>5} min: {st[1]!r}")
    check(P and P['id'] == fid, f"the first-talk scene didn't come first: {P and P['id']}")
    if P and P['id'] == fid:
        check(r['steps'][0][1] == P['lines'][0], f"something in front of the first-talk scene: {r['steps'][0][1]!r}")
        only_own(r, 'the first-talk scene')
        check(r.get('asked') and r['asked'][1] == P['ask'], 'the first-talk scene did not reach its question')
        w = g.ev("(() => { chatClose(); return !!SHIP.talks.fired[" + json.dumps(fid) + "]; })()")
        check(not w, 'walking off before answering used up the first-talk scene')
        r2 = g.ev(f"({PLAY})({{ id: 'marrow', tier: 0 }})")
        check(r2['pack'] and r2['pack']['id'] == fid, 'the first-talk scene did not come again after walking off')
        a = g.ev("(() => { chatDo('reply:listen'); return [!!SHIP.talks.fired[" + json.dumps(fid) + "], CHAT.line.text, CHAT.talk.pack.replies.listen.ans]; })()")
        check(a[0] and a[1] == a[2], f'answering did not have the first-talk scene: {a}')
        shot('talk-first')
        r3 = g.ev(f"({PLAY})({{ id: 'marrow', tier: 0 }})")
        print(f"  Marrow, the next time: {r3['pack'] and r3['pack']['id']}")
        check(r3['pack'] and r3['pack']['id'] != fid and r3['pack']['id'].startswith('marrow.'), 'after the first-talk scene: not one of her own talks')
        for st in r3['steps']: print(f"    {st[0]:>5} min: {st[1]!r}")
        check(r3['steps'][0][1].startswith('Stand-in own talk.') or r3['steps'][0][1] == r3['pack']['lines'][0] or any(r3['steps'][0][1].startswith(o) for o in OWNL), 'her ordinary talk opened with a shared hello')
        only_own(r3, 'her next talk')
    # a long first-talk scene (6 lines): the card holds its question until all are said, the last one a while (talkPackHold)
    g.ev("(() => { const w = TALKS.own.marrow.find(tk => tk.first); w.__keep = w.lines; w.lines = [1, 2, 3, 4, 5, 6].map(i => ({ text: 'Stand-in welcome line ' + i + '.' })); SHIP.talks = { fired: {}, small: {} }; })()")
    r = g.ev(f"({PLAY})({{ id: 'marrow', tier: 0 }})")
    g.ev("(() => { const w = TALKS.own.marrow.find(tk => tk.first); w.lines = w.__keep; delete w.__keep; })()")
    said = [x[1] for x in r['steps']]
    last = max((x[0] for x in r['steps'] if x[1] == 'Stand-in welcome line 6.'), default=None)
    print(f"  a six-line first-talk scene: {len([x for x in said if x.startswith('Stand-in')])} lines said, the last at {last} min, the question at {r.get('asked') and r['asked'][0]} min")
    check(all(f'Stand-in welcome line {i}.' in said for i in range(1, 7)), 'a long first-talk scene lost lines before its question')
    check(r.get('asked') and last is not None and r['asked'][0] - last >= 1, 'the question came straight after the first-talk scene\'s last line')
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

    # (i) repeats over the first days (DL1, playtest 1 note 21: "a lot of repeating lines in the talk"): a chatty player
    # says hello and has a whole Talk a while with every crew member aboard, every day from Day 1 to Day 3 (the replies
    # that suit them). Every line the card shows is counted: a talk says at most TALK_FILLER_MAX filler lines, no filler
    # line comes more than FILLER_MOST times, and no everyday line (hello, start, filler, end, small talk) more than
    # LINE_MOST times; the pack's own talk lines never twice
    print('(i) repeats over Days 1-3, talking with everyone every day:')
    FILLER_MOST, LINE_MOST, HOLD_MOST = 3, 25, 5   # HOLD_MOST: ship minutes one line stays (5: before the question at TALK_ASK)
    errors3 = []
    g = Game(pw, sys.argv[1], w=390, h=844, errors=errors3)
    g.ev("(() => { SHIP.time.day = 1; SHIP.time.min = 8 * 60; })()"); g.step(3)
    REP = r"""(({ days }) => {
      socInit(); const log = [], fill = new Set(((LINES['talk.filler']) || []).map(e => e.text)), ppl = SOC.crew.filter(p => p.id !== 'you');
      for (let d = 1; d <= days; d++) ppl.forEach((p, i) => {
        const t0 = (d - 1) * 1440 + 8 * 60 + Math.floor(i * 13 * 60 / ppl.length); setShipNow(t0);
        if (typeof socAboard === 'function' && !socAboard(p, d)) return;
        chatClose(); CHAT = { p, line: chatLine(p), ask: false, fav: null, at: shipNow(), reach: 99, checked: Math.floor(shipNow()) + 999 }; chatShow();
        if (relGet(p.id).chatDay !== d) { chatDo('chat'); log.push({ p: p.id, kind: 'hello', text: CHAT.line.text }); }
        chatDo('talk'); const T = CHAT.talk; if (!T) return;
        const P = T.pack, kind = x => !P ? 'old' : P.small && P.lines.includes(x) ? 'small' : P.lines.includes(x) ? 'pack' : x === P.ask ? 'ask'
          : P.replies && Object.values(P.replies).some(r => r.ans === x) ? 'answer' : fill.has(x) ? 'filler' : 'other';
        let last = CHAT.line.text, n = 0, at = 0, hold = 0, took = 0; log.push({ p: p.id, kind: 'start', text: last });
        for (let k = 1; k <= 60 && !T.end; k++) { setShipNow(t0 + 1 + k * .5); CHAT.checked = Math.floor(shipNow()) + 999; talkStep(CHAT); took = k * .5;
          if (T.ask) chatDo('reply:' + talkSuits(p));
          const l = CHAT.line.text; if (l !== last) { hold = Math.max(hold, k * .5 - at); at = k * .5; last = l; const kd = kind(l); if (kd === 'filler') n++; log.push({ p: p.id, kind: kd, text: l }); } }
        log.push({ p: p.id, kind: 'talk', n, hold, mins: took, small: !!(P && P.small), id: P && P.id, end: T.end, pts: T.pts, gained: Math.round(T.gained) });
      });
      chatClose(); return { log, max: typeof TALK_FILLER_MAX !== 'undefined' ? TALK_FILLER_MAX : 2, saved: JSON.stringify(SHIP.talks.heard || {}).length }; })"""
    r = g.ev(f"({REP})({{ days: 3 }})")
    import collections
    log = r['log']; talks = [e for e in log if e['kind'] == 'talk']; said = [e for e in log if e['kind'] != 'talk']
    by = collections.defaultdict(collections.Counter)
    for e in said: by[e['kind']][e['text']] += 1
    for k in sorted(by, key=lambda k: -sum(by[k].values())):
        c = by[k]; t, n = c.most_common(1)[0]
        print(f"  {k:7} {sum(c.values()):5} said, {len(c):4} different, the most {n}x {t[:56]!r}")
    print(f"  {len(talks)} talks, {len(said)} lines; filler a talk at most {max(e['n'] for e in talks)}; the heard record {r['saved']} bytes")
    check(len(talks) > 100, f"only {len(talks)} talks: the replay didn't run")
    check(all(e['n'] <= r['max'] for e in talks), f"a talk said more than {r['max']} filler lines")
    held = max(e['hold'] for e in talks); hw = max(talks, key=lambda e: e['hold']); print(f"  the longest hold: {hw['p']} {hw.get('id')} small {hw.get('small')}")
    print(f"  the longest one line stayed on the card: {held} ship minutes; ended full {sum(e['end'] == 'full' for e in talks)}/{len(talks)}, after {min(e['mins'] for e in talks)}-{max(e['mins'] for e in talks)} ship minutes; social a talk {min(e['gained'] for e in talks)}-{max(e['gained'] for e in talks)}")
    check(held <= HOLD_MOST, f"a line stayed on the card {held} ship minutes (at most {HOLD_MOST}: a talk with nothing new to say wraps up)")
    check(all(e['end'] == 'full' for e in talks), 'a talk did not finish (the meter and the goodbye)')
    worst = by['filler'].most_common(1)
    check(not worst or worst[0][1] <= FILLER_MOST, f"a filler line {worst and worst[0]} more than {FILLER_MOST} times")
    every = collections.Counter(e['text'] for e in said if e['kind'] in ('hello', 'start', 'filler', 'small', 'other'))
    w = every.most_common(1)
    check(not w or w[0][1] <= LINE_MOST, f"an everyday talk line {w and w[0]} more than {LINE_MOST} times")
    check(all(n == 1 for n in by['pack'].values()), 'a pack talk line twice')
    check(r['saved'] < 8000, f"the heard record is {r['saved']} bytes")
    for e in errors3: fail(f'page error: {e}')
    g.close()

print('TALK CHECK OK' if ok else 'TALK CHECK FAILED')
sys.exit(0 if ok else 1)
