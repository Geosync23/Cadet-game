# Starship Cadet: crew stories check (FX21, 0.92.6 item 19; stage 1: Pell, Theo, Basil, Halloran, Kovac, Saad; stage 2, ST1:
# Zeke, Calder, Dev Raman, Kowalczyk, behind STORIES2_ON).
# Walks each crew story's beats on paper, the way arc_check does the older arcs, in a copy of the game with STORIES_ON
# switched on by text (the build itself may have it off). Three parts:
#   1. Off: the build as it is. With STORIES_ON off nothing of the stories is read: storyMoment is null, momentDef gives
#      the old MOMENTS words (Pell 5-8, Kovac 1-4), the story people keep their roster threads, no state is written.
#   2. On, twice over DAYS ship days (default 30) as a diligent player: a chat and a meal with each story person a day,
#      a Works job a day; every 10 minutes from 06:00 the stories' clock (storyTick) runs and whatever beat is ready is
#      played (the first reply each time); a favour from a story is done at once. Run "play" goes to every crescendo;
#      run "miss" never does. Rules checked on each run's log:
#        - every beat is told or skipped by the end (else STALLED, with why);
#        - a crescendo is told only inside its booking, on its gathering's day, with a Mail queued from that person by
#          18:00 the evening before (or at booking, if later) and a Calendar row that day; at most one crescendo a day;
#        - a crescendo told means its quiet ending never is; in "miss", every crescendo is skipped and its quiet ending
#          told (by Mail when they've left the ship);
#        - a beat with day: conditions is told inside them;
#        - an afterglow (follows:) comes after one of its beats;
#        - Theo: no ordinary goodbye while his farewell crescendo stands;
#        - no page errors.
#      Stage 2 (ST1): the copy switches STORIES2_ON on too; the paper player is made an Engine Specialist as a steady one
#      is (Monday Day 22, 22:40, as night 1 starts). Part 1 also checks stage 2 off: no stage 2 beat is read, Zeke's and
#      Calder's are the old MOMENTS words, Kowalczyk and Raman aren't story people, nobody's plan has a story beat.
#   3. A self-test: the rules above, fed planted logs that break each one, must catch every one.
# Run: CADET_CHROME=/opt/pw-browsers/chromium python3 stories_check.py BUILD.html [DAYS]   (a few minutes)
import sys, os, json, types, pathlib
os.environ.setdefault('CADET_CHROME', '/opt/pw-browsers/chromium')
from playwright.sync_api import sync_playwright
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cadet_test.py')).read(); src = src[:src.index('import sys, json, hashlib')]
ct = types.ModuleType('ct'); exec(src, ct.__dict__)
BUILD = sys.argv[1]
DAYS = int(sys.argv[2]) if len(sys.argv) > 2 else 30
OFF_LINE, ON_LINE = 'var STORIES_ON = false;', 'var STORIES_ON = true;'
OFF2_LINE, ON2_LINE = 'var STORIES2_ON = false;', 'var STORIES2_ON = true;'   # stage 2 (ST1)

OFF = r"""
(() => {
  socInit();
  const out = { on: STORIES_ON, table: typeof STORY_MOMENTS !== 'undefined' ? Object.keys(STORY_MOMENTS).length : -1, bad: [] };
  for (const k of Object.keys(STORY_MOMENTS || {})) { if (storyMoment(k)) out.bad.push('storyMoment(' + k + ') while off');
    const d = momentDef(k), old = MOMENTS[k]; if (old && d && d.lines.length !== old.lines.length) out.bad.push(k + ': not the old words'); if (!old && d && d.lines === STORY_MOMENTS[k].lines) out.bad.push(k + ': a story beat while off'); }
  for (const id of ['teague-theo', 'bramwell-basil', 'halloran-emeka', 'salo-saad']) { const p = socP(id), th = voiceOf(id).thread; if (p && p.thread && th !== p.thread && !(VOICE[id] && /^arc:/.test(VOICE[id].thread || ''))) out.bad.push(id + ' thread ' + th + ', the roster says ' + p.thread); }
  if (SHIP.social.stories && SHIP.social.stories.cs) out.bad.push('SHIP.social.stories.cs written while off');
  out.bad2 = []; out.on2 = typeof STORIES2_ON !== 'undefined' && STORIES2_ON; out.table2 = typeof STORY_MOMENTS2 !== 'undefined' ? Object.keys(STORY_MOMENTS2).length : -1;
  if (!out.on2 && out.table2 > 0) {   // stage 2 off (ST1): none of its beats is read, wherever stage 1 is
    for (const k of Object.keys(STORY_MOMENTS2)) { if (storyMoment(k) && storyMoment(k) === STORY_MOMENTS2[k]) out.bad2.push('stage 2 beat ' + k + ' read while STORIES2_ON is off');
      const d = momentDef(k), old = MOMENTS[k]; if (d && d.lines === STORY_MOMENTS2[k].lines) out.bad2.push(k + ': a stage 2 beat while off'); }
    for (const id of ['raman', 'kowalczyk', 'calder', 'torres-zeke']) if (storyIdx().beats.has(id)) out.bad2.push(id + ' is a story person while stage 2 is off');
    for (const id of ['kowalczyk', 'mensah']) if (planDay(socP(id), 24).some(x => /^intro-story-/.test(x.tag || ''))) out.bad2.push(id + ': a stage 2 plan beat while off');
    if (storyPlanBeats('kowalczyk', 24).length) out.bad2.push('storyPlanBeats while off'); }
  return out;
})()
"""

RUN = r"""
([DAYS, MODE]) => {
  socInit();
  const nobook = {}, diag = {}, ids = [...storyIdx().beats.keys()], log = [], mails = [], cal = {}, books = {}, byes = [], lines = {}, err = [];
  const play = (id) => { let n = 0; const said = []; while (DIALOGUE && n++ < 80) { const v = dialogueView(); if (!v) break; if (v.text) said.push(v.text); if (v.choices) dialogueStep(0); else dialogueStep(); } lines[id] = said; };
  const live = t => { setShipNow(t); if (typeof socialTo === 'function') socialTo(t); return t; };
  const C = () => storyPeekCS();
  let mailSeen = 0;
  for (let d = 1; d <= DAYS; d++) {
    for (let m = 360; m < 1440; m += 10) {   // every 10 minutes: a gathering can be 20 minutes long (Off the Tern)
      const t = live((d - 1) * 1440 + m);
      if (m === 720) for (const id of ids) { const p = socP(id); if (p && socAboard(p, d)) { relAdd(id, 'chat', 2); relAdd(id, 'meal', 3); } }
      if (m === 900) repAdd('works', 1.5, { work: 1 }, 'job');
      if (d === 22 && m === 1360 && SHIP.works && typeof STORIES2_ON !== 'undefined' && STORIES2_ON) { SHIP.works.tier = 4; SHIP.works.rank = 'specialist'; }   // stage 2: a steady player's Engine Specialist, as night 1 starts
      if (m === 360) for (const id of ids) { const p = socP(id), mid = p && momentNextId(p), dd = mid && momentDef(mid); if (!dd || !dd.crescendo || C().book[id]) continue;   // a crescendo due but not booked: why, today
        const sl = storySlots(dd.crescendo, p, d, dd.lead || 0, dd); if (!sl.length) continue; const s0 = sl[0];
        const cast = {}; for (const c of dd.cast || []) { let n = 0; for (let x = s0.from; x < s0.to; x += 5) if (storyHere(c, p, { t: x })) n++; cast[c] = n; }
        let at = 0; for (let x = s0.from; x < s0.to; x += 5) if (storyAtSlot(p, x, dd, s0)) at++;
        (nobook[mid] || (nobook[mid] = [])).push({ d, at: s0.from % 1440, here: at, cast, gates: storyGates(p, dd, mid, s0.from, s0.trad), flags: (dd.when && dd.when.flag) ? [].concat(dd.when.flag).map(f => f + '=' + !!flag(f)) : undefined }); }
      try { storyTick(t); } catch (e) { err.push('storyTick: ' + e.message); }
      for (const x of SHIP.social.mail.slice(mailSeen)) mails.push({ at: x.at, queued: t, from: x.from, subject: x.subject }); mailSeen = SHIP.social.mail.length;
      for (const id in C().book) { const b = C().book[id], dd = storyMoment(id + ':' + b.beat), p = socP(id);
        if (dd && t >= b.from && t < b.to) { const k = id + ':' + b.beat, x = diag[k] || (diag[k] = { steps: 0, atSlot: 0, cast: {}, where: {}, ready: 0, gates: 0 }); x.steps++;
          if (storyAtSlot(p, t, dd, b)) x.atSlot++; for (const c of dd.cast || []) if (storyHere(c, p, { t })) x.cast[c] = (x.cast[c] || 0) + 1;
          const w = whereIs(p, t); x.where[(w && (w.act + ':' + (w.tag || '') + ':' + (storyRoom(p, t) || 'moving'))) || 'none'] = 1; if (momentReady(p, t)) x.ready++; if (storyGates(p, dd, k, t, b.trad)) x.gates++; }
        books[id + ':' + b.beat] = { ...b };
        const rows = storyCalRows(b.day, (b.day - 1) * 1440); if (rows.length) cal[id + ':' + b.beat] = b.day; }
      for (const id of ids) {
        const p = socP(id); if (!p || !socAboard(p, d)) continue;
        const g = goodbyeMoment(p, t); if (g) byes.push(id + '@' + d);
        if (STORY_ARCS[id] && arcBeat(p, t)) arcTold(p);   // the older card beats (Pell 1-4), told on their chat card
        let mid = momentReady(p, t);
        const wb = C().book[id]; if (!mid && wb && wb.walk != null && t + 10 > wb.from && t < wb.to) for (let k = 1; k < 10 && !mid; k++) { if (t + k < wb.from) continue; live(t + k); mid = momentReady(p, t + k); }   // a walk booking is minutes long: try each minute (the player taps them as they pass)
        if (!mid) { if (shipNow() !== t) live(t); continue; }
        const t1 = shipNow();
        const dd = momentDef(mid);
        if (dd.crescendo && MODE === 'miss') continue;
        const before = (C().told[id] || []).length, bk = C().book[id], room = storyRoomOf(dd), w0 = whereIs(p, t1);
        const atRoom = !dd.crescendo || !room ? null : (storyInRoom(p, t1, room) || (bk && bk.walk != null && w0 && (w0.deck === bk.walk || (w0.moving && w0.fromDeck === bk.walk))));   // RV16: a crescendo that names a room plays there (or on the way, on the deck they ride from)
        momentShow(mid); play(mid);
        if ((C().told[id] || []).length > before) log.push({ id, beat: dd.beat, day: d, t: t1, cres: dd.crescendo || null, atRoom, room, quiet: dd.quiet || null, follows: dd.follows || null, day_: dd.when && dd.when.day || null, book: dd.crescendo ? books[mid] || null : null });
        for (const j of (typeof myFavours === 'function' ? myFavours() : []).filter(j => j.from === id)) { j.workDone = j.workDone || t; if (!favourTurnIn(j.id)) { j.status = 'done'; j.doneAt = t; j.doneBy = 'you'; } }
      }
      SHIP.social.mail = SHIP.social.mail.filter(x => x.at > t); mailSeen = SHIP.social.mail.length;   // delivered (socialMail's job; the device isn't needed on paper)
    }
  }
  for (const k of Object.keys(C().told)) for (const b of C().told[k]) if (!log.some(x => x.id === k && x.beat === b)) log.push({ id: k, beat: b, day: null, posted: true });   // told without a scene (a quiet ending by Mail)
  const beats = {}; for (const id of ids) beats[id] = storyIdx().beats.get(id).map(b => { const d = storyMoment(id + ':' + b); return { beat: b, cres: d.crescendo || null, quiet: d.quiet || null, follows: d.follows || null }; });
  const why = {}; for (const id of ids) { const p = socP(id), mid = p && momentNextId(p), dd = mid && momentDef(mid), r = SHIP.rel[id];
    if (mid) { const w0 = { next: mid, tier: r && r.tier, met: metDays(id), when: dd.when || null, where: dd.where || 'calm', cres: dd.crescendo || null, aboard: socAboard(p, DAYS) };
      let whenOk = 0, whereOk = 0, both = 0, n = 0, rooms = {};   // the last 7 days, every half hour: how often its when and its where held, and where they were off duty
      for (let d = Math.max(1, DAYS - 6); d <= DAYS; d++) for (let m = 360; m < 1440; m += 30) { const t = (d - 1) * 1440 + m; setShipNow(t); n++;
        let a = true; if (dd.when) { try { a = !!linesOk(dd.when, p, momentCtx(p, t, mid)); } catch (e) { a = false; } } const b = momentWhere(p, t, dd); whenOk += a; whereOk += b; both += a && b;
        const w = whereIs(p, t), pl = w && !w.moving && w.placeId && schedData().byId.get(w.placeId), rm = pl && DECKS[pl.deck] && (DECKS[pl.deck].rooms || {})[pl.room]; if (rm && (w.act === 'leisure' || w.act === 'off')) rooms[rm.name] = (rooms[rm.name] || 0) + 1; }
      let gate = null; for (let d = Math.max(1, DAYS - 6); d <= DAYS && !gate; d++) for (let m = 360; m < 1440 && !gate; m += 30) { const t = (d - 1) * 1440 + m; setShipNow(t);   // the first time when and where both held: which other gate said no
        let a = true; if (dd.when) { try { a = !!linesOk(dd.when, p, momentCtx(p, t, mid)); } catch (e) { a = false; } } if (!a || !momentWhere(p, t, dd)) continue;
        const g = STEP_GATES[dd.tone] || STEP_GATES.heartfelt, st = storyPeek(id), S = SHIP.social.stories || {}, last = dd.tone === 'resolution' ? st.hf : st.at;
        gate = { day: d, m, ready: momentReady(p, t), tierOk: relTier(id) >= (dd.tier ?? g.tier), metOk: metDays(id, t) >= (dd.metDays ?? g.met), gapOk: last === null || (t - last) / 1440 >= (dd.gapDays ?? g.gap), oneADay: !(st.at !== null && Math.floor(st.at / 1440) + 1 === d), serious: !(MOMENT_SERIOUS.has(dd.tone) && S.serious === d), dialogue: !DIALOGUE, arcDay: (SHIP.rel[id] || {}).arcDay }; }
      why[id] = { ...w0, whenOk, whereOk, both, of: n, gate, offDuty: rooms }; } }
  return { nobook, diag, ids, log, mails, cal, books, byes, told: C().told, skip: C().skip, beats, why, err, names: Object.fromEntries(ids.map(id => [id, socP(id) ? socP(id).name : id])) };
}
"""

def rules(r, mode):
    """The rules on one run's result -> a list of failures (plain words)."""
    bad = []
    told = {k: set(v) for k, v in r['told'].items()}; skip = {k: set(v) for k, v in r['skip'].items()}
    for id, bs in r['beats'].items():
        for b in bs:
            n = b['beat']
            if n not in told.get(id, set()) and n not in skip.get(id, set()): bad.append(f'{id} beat {n}: never told or skipped (STALLED: {json.dumps(r["why"].get(id))})')
            if b['quiet'] and n in told.get(id, set()) and b['quiet'] in told.get(id, set()): bad.append(f'{id}: beat {n} and its quiet ending {b["quiet"]} both told')
            if mode == 'miss' and b['cres']:
                if n in told.get(id, set()): bad.append(f'{id}: crescendo {n} told in the miss run')
                if b['quiet'] and b['quiet'] not in told.get(id, set()): bad.append(f'{id}: crescendo {n} missed but quiet ending {b["quiet"]} not told')
    days = {}
    for x in r['log']:
        if x.get('posted') or not x.get('cres'): continue
        days.setdefault(x['day'], []).append(x['id'])
        b = x.get('book')
        if not b: bad.append(f'{x["id"]} crescendo {x["beat"]}: told without a booking'); continue
        if not (b['from'] <= x['t'] < b['to']) or b['day'] != x['day']: bad.append(f'{x["id"]} crescendo {x["beat"]}: told outside its booking (day {x["day"]})')
        if x.get('room') and x.get('atRoom') is False: bad.append(f'{x["id"]} crescendo {x["beat"]}: told away from its room ({x["room"]})')
        name = r['names'].get(x['id'])
        eve = (b['day'] - 2) * 1440 + 1080
        if not any(m['from'] == name and m['at'] <= max(eve, m['queued']) and m['queued'] <= x['t'] for m in r['mails']): bad.append(f'{x["id"]} crescendo {x["beat"]}: no Mail from them the evening before')
        if r['cal'].get(f'{x["id"]}:{x["beat"]}') != b['day']: bad.append(f'{x["id"]} crescendo {x["beat"]}: no Calendar row on its day')
    for d, who in days.items():
        if len(who) > 1: bad.append(f'day {d}: {len(who)} crescendos ({", ".join(who)})')
    for x in r['log']:
        if x.get('posted') or not x.get('day_'): continue
        for v in (x['day_'] if isinstance(x['day_'], list) else [x['day_']]):
            if ',' in str(v):
                if x['day'] not in [int(y) for y in str(v).split(',')]: bad.append(f'{x["id"]} beat {x["beat"]}: told on day {x["day"]}, outside day:{v}')
                continue
            lo, dash, hi = str(v).partition('-'); lo = int(lo) if lo else 1; hi = (int(hi) if hi else 10**6) if dash else lo
            if not lo <= x['day'] <= hi: bad.append(f'{x["id"]} beat {x["beat"]}: told on day {x["day"]}, outside day:{v}')
    for x in r['log']:
        if x.get('follows') and not any(y['id'] == x['id'] and y['beat'] in x['follows'] and (y.get('posted') or y['day'] is None or (y['day'], y.get('t', 0)) <= (x['day'], x['t'])) for y in r['log']): bad.append(f'{x["id"]} beat {x["beat"]}: an afterglow before its beats {x["follows"]}')
    if mode == 'play' and any(b.startswith('teague-theo@') for b in r['byes']) and any(b['cres'] == 'farewell' for b in r['beats'].get('teague-theo', [])): bad.append('teague-theo: an ordinary goodbye while his farewell crescendo stands')
    bad += ['error: ' + e for e in r['err']]
    return bad

def selftest():
    """Planted logs: each must be caught."""
    base = lambda: {'ids': ['a'], 'names': {'a': 'A'}, 'beats': {'a': [{'beat': 1, 'cres': None, 'quiet': None, 'follows': None}, {'beat': 2, 'cres': 'trad:x', 'quiet': 3, 'follows': None}, {'beat': 3, 'cres': None, 'quiet': None, 'follows': None}, {'beat': 4, 'cres': None, 'quiet': None, 'follows': [2, 3]}]},
        'told': {'a': [1, 2, 4]}, 'skip': {'a': [3]}, 'why': {}, 'err': [], 'byes': [], 'cal': {'a:2': 5}, 'mails': [{'from': 'A', 'at': 3 * 1440 + 1080, 'queued': 3 * 1440 + 600}],
        'log': [{'id': 'a', 'beat': 1, 'day': 2, 't': 1500}, {'id': 'a', 'beat': 2, 'day': 5, 't': 4 * 1440 + 700, 'cres': 'trad:x', 'book': {'day': 5, 'from': 4 * 1440 + 690, 'to': 4 * 1440 + 750}},
                {'id': 'a', 'beat': 4, 'day': 6, 't': 5 * 1440 + 700, 'follows': [2, 3]}]}
    out = []
    r = base(); out.append(('clean log passes', not rules(r, 'play')))
    r = base(); r['told']['a'] = [1, 2]; r['skip']['a'] = [3]; out.append(('a stalled beat', any('never told' in x for x in rules(r, 'play'))))
    r = base(); r['told']['a'] = [1, 2, 3, 4]; r['skip']['a'] = []; out.append(('beat and its quiet ending both', any('both told' in x for x in rules(r, 'play'))))
    r = base(); r['mails'] = []; out.append(('no Mail', any('no Mail' in x for x in rules(r, 'play'))))
    r = base(); r['cal'] = {}; out.append(('no Calendar', any('Calendar' in x for x in rules(r, 'play'))))
    r = base(); r['log'][1]['t'] = 4 * 1440 + 800; out.append(('outside its booking', any('outside its booking' in x for x in rules(r, 'play'))))
    r = base(); r['log'][1]['book'] = None; out.append(('no booking', any('without a booking' in x for x in rules(r, 'play'))))
    r = base(); r['log'].append({'id': 'b', 'beat': 2, 'day': 5, 't': 4 * 1440 + 720, 'cres': 'trad:y', 'book': {'day': 5, 'from': 4 * 1440 + 700, 'to': 4 * 1440 + 760}}); r['names']['b'] = 'B'; r['cal']['b:2'] = 5; r['mails'].append({'from': 'B', 'at': 0, 'queued': 0})
    out.append(('two crescendos a day', any('2 crescendos' in x for x in rules(r, 'play'))))
    r = base(); r['log'][0]['day_'] = '3-9'; out.append(('day: window', any('outside day:' in x for x in rules(r, 'play'))))
    r = base(); r['log'][2]['day'] = 4; r['log'][2]['t'] = 3 * 1440; out.append(('afterglow too early', any('afterglow' in x for x in rules(r, 'play'))))
    r = base(); out.append(('miss run told a crescendo', any('miss run' in x for x in rules(r, 'miss'))))
    r = base(); r['told']['a'] = [1, 4]; r['skip']['a'] = [2, 3]; out.append(('missed, no quiet ending', any('quiet ending 3 not told' in x for x in rules(r, 'miss'))))
    r = base(); r['beats']['teague-theo'] = [{'beat': 5, 'cres': 'farewell', 'quiet': 6, 'follows': None}]; r['told']['teague-theo'] = [5]; r['skip']['teague-theo'] = [6]; r['byes'] = ['teague-theo@20']
    out.append(('Theo twice goodbye', any('ordinary goodbye' in x for x in rules(r, 'play'))))
    return out

def on_copy():
    s = pathlib.Path(BUILD).read_text()
    if ON_LINE in s and OFF2_LINE not in s: return BUILD
    if OFF_LINE not in s and ON_LINE not in s: print('STORIES CHECK: no STORIES_ON line in this build'); sys.exit(1)
    p = ct.WORK / 'test' / ('_stories_on_' + pathlib.Path(BUILD).name); p.write_text(s.replace(OFF_LINE, ON_LINE, 1).replace(OFF2_LINE, ON2_LINE, 1)); return str(p)

fails = []
st = selftest()
for name, ok in st: print('self-test', 'ok ' if ok else 'MISSED', name)
fails += ['self-test missed: ' + n for n, ok in st if not ok]
with sync_playwright() as pw:
    g = ct.Game(pw, BUILD); g.step(3); r = g.ev(OFF); errs = g.errors[:5]; g.close()
    print(f'Part 1, the build as it is: STORIES_ON {r["on"]}, {r["table"]} story beats baked; STORIES2_ON {r["on2"]}, {r["table2"]} stage 2 beats')
    if r['on'] and not r['on2']:
        for b in r['bad2']: print('  FAIL stage 2 off:', b)
        fails += ['stage 2 off: ' + b for b in r['bad2']]
        if not r['bad2']: print('  stage 2 off: nothing of it read (Zeke and Calder the old words, no plan beats)')
    if not r['on']:
        for b in r['bad']: print('  FAIL off:', b)
        fails += ['off: ' + b for b in r['bad']]
    else: print('  (the build has STORIES_ON on: part 1 skipped)')
    fails += ['off, page error: ' + e for e in errs]
    on = on_copy()
    for mode in ('play', 'miss'):
        g = ct.Game(pw, on); g.step(3)
        r = g.page.evaluate('([s, a]) => window.__sc("(" + s + ")(" + JSON.stringify(a) + ")")', [RUN, [DAYS, mode]])
        errs = g.errors[:5]; g.close()
        print(f'Part 2, run "{mode}" ({DAYS} days):')
        for id in r['ids']:
            got = sorted(x['beat'] for x in r['log'] if x['id'] == id)
            print(f'  {id}: told {sorted(r["told"].get(id, []))}, skipped {sorted(r["skip"].get(id, []))}; days ' + ' '.join(f'{x["beat"]}@{x["day"] if x["day"] else "mail"}' for x in sorted(r['log'], key=lambda x: (x['day'] or 99, x.get('t', 0))) if x['id'] == id))
        print('  bookings:', ', '.join(f'{k} day {v["day"]} {v["from"] % 1440 // 60:02d}:{v["from"] % 60:02d}' for k, v in r['books'].items()) or 'none')
        for k, v in r['nobook'].items(): print('  crescendo', k, 'due, never booked on:', json.dumps(v)[:900])
        for k, v in r['diag'].items():
            if not any(x['id'] + ':' + str(x['beat']) == k for x in r['log']): print('  crescendo', k, 'booked, not told:', json.dumps(v))
        bad = rules(r, mode) + ['page error: ' + e for e in errs]
        for b in bad: print('  FAIL', mode + ':', b)
        fails += [mode + ': ' + b for b in bad]
print('STORIES CHECK OK' if not fails else f'STORIES CHECK FAILED ({len(fails)})')
sys.exit(0 if not fails else 1)
