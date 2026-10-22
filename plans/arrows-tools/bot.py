# a follow-the-arrow player: goes where the arrow points (teleport = walking), reads meetings through, clocks in when
# the arrow says so, takes the job the arrow / board offers (training jobs first), does its steps, turns it in.
import sys, json
from harness import *
BOT = r"""(() => {
  const now = Math.floor(shipNow()), m = now % 1440, d = Math.floor(now / 1440) + 1;
  const out = [];
  if (typeof DIALOGUE !== 'undefined' && DIALOGUE) { const v = dialogueView(); if (v && v.choices) dialogueChoose(0); else dialogueNext(); return 'dialogue'; }
  if (typeof ACT !== 'undefined' && ACT) return 'busy';
  if (m < 360 || m > 1260) return 'night';
  const W = SHIP.works, c = W && W.cur;
  // a meeting asked: go to its room at its time (the arrow says where; if no arrow, the bot still goes: noted)
  if (c && c.st === 'meet') { const r = SHIP.occasions.find(x => x.key === c.occ);
    if (r && now >= r.at - 10 && now < r.at + r.len) { const here = deckDef.num === r.deck && roomAt(...player.here()) === r.room;
      if (!here) { devmodeMove(r.deck, () => ixGoalWorld({ room: r.room }), x => x === r.room); return 'to meeting ' + r.id + (goalNow() ? '' : ' (NO ARROW)'); } return 'at meeting'; } }
  if (c && c.st === 'watch') { const j = SHIP.jobs.find(x => x.id === c.j), s = trainSpot(j); if (s && !trainNear(s)) { devmodeMove(s.deck, () => cellPos(...s.tile), x => x === s.room); return 'to watch ' + (goalNow() ? '(arrow: ' + goalNow().label + ')' : '(NO ARROW)'); } return 'watching'; }
  const g = goalNow();
  if (g && /clock in/i.test(g.label || '')) { if (careerClock(shipNow(), true) === 'in') return 'clocked in'; }
  // a job: training ones first
  if (typeof myJob === 'function' && !myJob() && typeof playerShiftOn === 'function' && playerShiftOn(d) && m >= 480 && m < 1020 && careerClockedIn(d)) {
    const list = openJobs('you'); const pick = list.find(j => { const x = SHIP.jobs.find(y => y.id === j.id); return x && (x.train || x.reserved); }) || list[0];
    if (pick && claimJob(pick.id)) return 'took ' + pick.title;
  }
  const j = typeof myJob === 'function' && myJob();
  if (j) {
    const cs = W && W.cases && (W.cases.open || []).find(x => x.job === j.id);
    if (cs && typeof caseCall === 'function' && !cs.called) { caseCall(cs.id, cs.cause); return 'called case ' + cs.id; }
    if (j.workDone) { const r = turnInJob(j.id); return 'turned in ' + j.title + ' ' + r; }
    const st = jobStops(j); const k = st.findIndex(x => !x.done);
    if (k >= 0) { const s = st[k]; if (s.deck && deckDef.num !== s.deck) devmodeMove(s.deck, () => g ? ixGoalWorld(g) : null) ; const r = jobStepDone(j.id, k); return 'step ' + s.step + ' ' + r; }
    if (j.machine) { // a repair: fetch parts, then repair at the panel (paper)
      const P = SHIP.player; const need = jobNeeds(j, P.work && P.work.job === j.id ? P.work : { fitted: [], make: null }, P.carry);
      if (need.length) { for (const p of need) if (takePart(p)) P.carry.push(p); }
      if (typeof workFinish === 'function') { try { workFinish(j); } catch (e) {} }
      return 'repair ' + j.title + ' need ' + need.join(',');
    }
  }
  if (g && g.deck) { const w = ixGoalWorld(g); const [pc, pr] = player.here(); if (w && (deckDef.num !== g.deck || Math.hypot(player.obj.position.x - w.x, player.obj.position.z - w.z) > 2.5)) { devmodeMove(g.deck, () => ixGoalWorld(g)); return 'follow arrow: ' + g.label; } }
  return 'idle';
})()"""
def play_day(g, day, until=1140, quiet=False):
    acts = []
    def hook(g):
        r = g.ev(BOT)
        if r not in ('idle', 'night', 'busy', 'watching', 'at meeting') and (not acts or acts[-1][1] != r): acts.append((g.ev('clockText()'), r))
    g.run_min(until - g.ev('Math.floor(shipNow()) % 1440'), hook=hook)
    return acts
if __name__ == '__main__':
    day = int(sys.argv[1]); out = sys.argv[2] if len(sys.argv) > 2 else None
    with sync_playwright() as pw:
        g = G(pw)
        if day > 2: print(g.ev(f"devmodeRun('Set', () => devmodeSetCareerTo({day - 1}))")); g.step(10)
        g.ev(f"devmodeRun('Clock', () => devmodeSkipTo({(day - 1) * 1440 + 5 * 60 + 50}))"); g.step(10)
        print('start', g.ev('clockText()'), g.ev('JSON.stringify({tr: SHIP.works && SHIP.works.tr, rank: SHIP.works && SHIP.works.rank, xp: SHIP.works && SHIP.works.xp})'))
        n0 = len(g.log())
        acts = play_day(g, day)
        L = g.log()[n0:]
        merged = sorted([(a[0], 'BOT', a[1]) for a in acts] + [tuple(l) for l in L], key=lambda x: x[0])
        for l in L: print(*l)
        print('--- bot')
        for a in acts: print(*a)
        print('errors', g.errors[:6])
        print('end', g.ev('JSON.stringify({tr: SHIP.works && SHIP.works.tr, use: SHIP.works && SHIP.works.use, cur: SHIP.works && SHIP.works.cur, op: SHIP.works && SHIP.works.op, xp: SHIP.works && SHIP.works.xp})'))
        g.close()
