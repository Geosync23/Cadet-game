# Handover: seat E2 (mechanic engineer 2), Pillar 5 Step 4

Written 2026-10-19 by E2 (session_01Bezat4UU7beoaKsqdSrJBs). Read CLAUDE.md, the brief
(`git show origin/claude/lead-pillar1:plans/brief-p5s4.md`), M2's `plans/handover-mech2.md` (24e/24f/24h, still true)
and H's/H2's notes on claude/mech-cases (the case engine) first. Pages: `git show origin/claude/p5-design:plans/mechanics/<page>.html`
(m13-leak-hunting, m14-irrigation, m15-rewiring, favour-cases, step4-stages; summary step4-summary).

## Role, branch, builds, people

- Branch `claude/mech-incidents`, builds 0.51.4-0.51.12 on the Step 3 base 0.63.3 (claude/p5-cand-pt1 7a6e137). Next build: 0.51.13. Last: 0.51.12 (a leak +1 in all; `playerRigRebuild` is 24l's, so the pin shows).
- Lead 17 session_016bN7x175WBwBL7S9xc2Lpb (was 16). Build master BM7 session_01QbuzvT3TwzMwSWRmakzX8Z. Reviewer R5
  session_01XJyHzg4QvX2nsdtf9zT1TH (R4 before). E1 session_01AHeKjieg3qWjnEVuHecsHd (24 core, claude/mech-rounds), E3
  session_01WkkCvj4yxnMALMQYG2DsWM (places, claude/mech-diagnose), D3 session_0115ZiGhf9s3oYtFdjs7TgYS (pages), W2
  session_01866TWKzGRgZmFcxiYRi4db (lines, claude/writer-p5).
- Reviews: R4 on 0.51.6 and R5 on 0.51.7/0.51.8/0.51.9, all PASS WITH FIXES; every fix is in 6714448 (0.51.11), lead 17's
  calls included (+1 a leak; ONE faded colour; FC_TIER = 3, friend). Notes: plans/reviews-p5-step4.md on claude/reviews-p5-step4.
  0.51.10's checks green (cadet_test, mech, food, career, machine, ...); 0.51.11's cadet_test/mech/career/interactions
  were running at handover: check /tmp results are gone with the container, so re-run them and send 6714448's results
  to lead 17, BM7 and R5 if the lead hasn't had them. DEV_NOTES rows 0.51.4-0.51.11 say what each build did.

## What E2 built (all in section 24, before `// 24p THE FIRST PROMOTION`, in the order 24l, 24o, 24q, 24r)

- **24l favour cases** (`FAVOUR_CASES`, the `'fcase'` side kind; `fcPlan/fcWho/fcCase/fcAsk/fcStops/fcStepDone/fcDone`):
  scripted cases on section 17's favours (D3 de012aa), keys 1019-1021, `side.favours`.
- **24l fault-finder tickets** (`ffState/ffPick/ffPost/ffGrade/ffPin`): Calder's Mail Day 13, a ticket on a Tier 2 machine via
  `jobReserve` slot 23 + 24k's `caseMake` (c.ticket), grade 1 → `W.ms ['ff1', day]`, the pin; keys 1022-1023, `side.ff`.
- **24o leak hunting** (the `'leak'` kind; `leakDay/leakPick/leakPost/leakStops/leakFx/puddleAt`): keys 1013-1014, `side.leaks`.
- **24q rewiring** (the `'rewire'` kind; `rewChart/rewDay/rewJob/rewStops`, `WORK_MECH.m15`): keys 1016-1017, `side.rewire`.
- **24r irrigation** (the `'nozzle'` kind; `nozClogged/nozPost/irrigationBonus`): key 1015, `side.nozzles`.
- **Hooks out** (register): section 16's harvest pick reads `irrigationBonus(d)`; section 8's `makeCharacter` draws `s.pin`;
  24k's `caseHint` holds hints back for `c.ticket` till three clues. Ladder rows m13/m14/m15 are E1's (24 core's table);
  mech_check `ROW_AGREE` fails if they drift from LEAK_*/NOZ_*/REW_*.

## Waiting on others

- **M8 stage 2 team parts: NOT BUILT, yours.** Page step4-stages ("Team jobs stage 2": after 2 team jobs, from Day 18, the
  team job's Mail asks you to bring the parts: a manifest run from stores to the machine before the start; not delivered,
  the lead fetches them and it starts 10 minutes late; never a fail). Function `teamParts(job)` in 24h (M2's code, this
  seat). E1's API (0.45.12, ETA ~07:30): `manifestRun(list, to, o = { at, until, title, for })` → job id | null (a 'haul'
  job held for you only; list = up to 4 part names; to = a place or machine id); delivered → `j.delivered`,
  `simNote('manifestRun', { job, for, to, parts })`, `manifestRunDelivered(id)`; not taken by `until` → withdrawn;
  `manifestRunEnd(id)` to withdraw. Saved count: `SHIP.works.side.parts = n` (the page). W2's keys: `mail.team.parts`
  ({job} {time} {name} {parts}), `team.parts.late` ({name}). Hook it at 24h's posting (`teamJobPost` at 16:00 the day
  before, `mail.team`) and at the start (`teamTick`: not delivered → `team.parts.late`, start + 10, `manifestRunEnd`).
- E1 (done in fb499eb, 0.45.11): flat side-kind pay, `j.xp === 0` skipped, the Record line for `W.ms` 'ffN'. `manifestRun` is
  final in claude/mech-rounds 633eade (0.45.12; also `j.src === 'stores'`, reserved slot 30, `j.for = o.for`).
  `playerRigRebuild()` is E2's (24l), lead 17's call.
- W2: keys all present (1c05127, d1e62d3); tickets' `ticket.nohint` and team parts' `mail.team.parts`/`team.parts.late`
  are W2's names; send W2 any new key in one message.

## Gotchas

- Registered kinds whose stops grow mid-job break `jobStepDone` (it counts stops before the step): keep the list fixed and
  hide places instead (24o hides the damp/joint places till the puddle's looked at).
- Section 17 tidies finished jobs off `SHIP.jobs`: keep "one a week" state in your own saved data (24q's `rewire.week`).
- E3's coordinates are positions (already centred / on the wall); draw wall decals only on an EDGES wall or hull edge and
  register them in `WALL_DECOR` so the cutaway hides them.
- Favours' stops are holds only (jobStopsBase drops how/opts): the clues are a side kind; the favour's fix stop gets its
  place only once solved.
- Don't `pkill -f` with a pattern that matches your own shell.

## How to test

```
pip install playwright; mkdir -p /tmp/cadet-work/three && cd /tmp/cadet-work/three && npm pack three@0.128.0 && tar xzf three-0.128.0.tgz
export CADET_CHROME=/opt/pw-browsers/chromium
python3 mech_check.py BUILD.html m13 m14 m15 fcase ff side   # E2's parts; stand-ins printed where E1/E3 aren't in
python3 cadet_test.py OLD.html BUILD.html                    # ALL IDENTICAL (everything inert before Day 12)
food_check, day_check BUILD 15|17|20, career_check, machine_check, interactions_check   # all OK at 0.51.7
```
A trial with E1's and E3's heads (merge into a scratch worktree; only the build-number lines conflict) runs E2's parts with
no stand-ins and the real save round trip.

## Open questions for the user

None from E2 (the judgement calls are in the DEV_NOTES rows and the lead's reports).
