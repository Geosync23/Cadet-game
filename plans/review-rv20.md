# RV20 review: Pillar 5 Step 5 (Senior Officer)

Reviewer RV20 (session_01PyJwfvfQVu4oXTYDMGkacw), hired by lead 39 (session_019V68fz33UFv4cK5Z4iCDvi). Every verdict goes
to the builder, lead 39 and BM18 (session_01A3S2VBMYmTt2wCZa8ej7XR) with the exact sha. Notes only, branch
`claude/review-rv20`. Spec: plans/p5-step5-spec.html on claude/p5-specs (db1313c1). Skeleton 5957d244 is RV19's.

Builders: B1 career + promotion (claude/p5s5-career) session_01GeUbys3v6keTivBrcgHznP; B2 mechanics A (claude/p5s5-mech-a)
session_015mjNkxuGoEZGKA2ksBPz9u; B3 shutdowns (claude/p5s5-mech-b) session_014FBmsiTsA9QymoN2qt4NyL; B4 puzzles
(claude/p5s5-puzzles) session_01LV8Q8UV6aJPTgmQ6ub1z8G; SW3 words session_019fcj6w9Nu52A1DyVPZ8DTi.

For each sha: spec followed; switch off = identical (cadet_test vs the base); the piece's own checks; played at 390 x 844
with ?p5s5; the user's three rules: works with a game controller; tons of arrows and super obvious progression (each beat
in the spec's beats table has its ring line, level-1 arrow, notices, said in person before the Mail); key moments are
staged scenes with dialogue.

## Log
- 2026-10-26 ~19:55 UTC: started; told B1-B4, SW3 and lead 39 my session id. Waiting for shas.

## SW3, the words: 46517ab0, then 277b9c15 (content + bake only, from skeleton 5957d244)
Read: the beats-table scenes (pu3.offer, .monday, .party; pu3.result, .fri; pu3.bar; pu3.toast), train.ps / m19 / m18 /
m20, promo-t3 (works and banks), m18, m19, m20, the cases additions, the crew's own lines, the three changed lines.
Voices right; Calder with no "!"; pronouns match content/facts.md (Brennan she, Torres he, Mori she); no emojis; each
scene has its who and where, replies and a close line. The friday-d19 / d26 edits read only with myrank:senior, which the
switch-off game never reaches.

| Check | Build | Result |
|---|---|---|
| content_gen --check, lines_check, names_check | 277b9c15 | up to date; PASS (0 errors); OK |
| check_fast | 277b9c15 | QUICK CHECK OK in 542 s |
| cadet_test vs 5957d244 | 46517ab0 | ALL IDENTICAL (277b9c15 only re-matches M19's words) |

M19 cross-check (RV20 to B2 and SW3): the first words didn't meet B2's code (keys, 12 relays vs 6, battery balancing vs
cell pairs, Calder's flags). SW3 re-matched them in 277b9c15 (B2's keys and design; m19.ring / m19.notice with {name}
{time} {where}, since lines_check has no {ring}). **Verdict on 277b9c15: PASS.** Notes: B1 wires
event.comet.captain.senior and picks the offer / result twins; each builder's keys get the same cross-check.

## B2, M19 power and relays: 3c38a65f (S5-3 turn 1, from 5957d244; game sha256 bfceeac5...7826)
Diff read: section 24v's slot only (PWR_* constants, pwrState, pwrJob, pwrStops, pwrStepDone, pwrDone, pwrDay,
pwrBeats, the P5_M19 block: two job kinds, the stand-in meeting, WORK_MECH.m19 with `at` 11:00 and its own reserve in
slot 32, the tool and repair onSims, the weekly job's WORK_TICK). Off: nothing registers; no R(); schedU keys 1060-1062.

| Check | Build | Result |
|---|---|---|
| cadet_test vs 5957d244 | 3c38a65f off | ALL IDENTICAL |
| mech_check m19 m15 | on copy (P5_STEP5 true) | MECH CHECK OK (ask 11:00 Deck 1 u Calder; notice 10:30; arrow level 1 from 10:45 with the ring line; tester once; weeks; wrong pick reopens) |
| ladder order, paper (plans/rv20-ladder-days.py) | 3c38a65f ?p5s5 | Day 17 opens m15 Rewiring, Day 18 m17 Lift roof, m19 only Day 19 11:00 |
| played live, 390 x 844 (plans/rv20-m19-live.py) | 3c38a65f ?p5s5 | below |
| relay / rewire jobs by real taps (plans/rv20-tap-jobs.py) | 3c38a65f ?p5s5 | below |

Played (a Senior on Day 17 with every earlier row done, in the bay from 08:55, clocked in at 09:01):
- 06:20 the ask by Mail (and a toast when up): "Meet me in the Relay room on Deck 1 at 11:00." Schedule and Tracked show
  "11:00 Training: power and relays with Ines".
- 10:30 the urgent notice "Power and relays with Calder, 11:00: Relay room, Deck 1." Good.
- 10:46 the arrow at level 1: "Tap the lift: Deck 1 · Power and relays ..." and the banner "Training: power and relays
  with Ines starts in 15 min, Relay room, Deck 1, GO THERE". Good, readable at phone size.
- In the relay room from 10:46: **Calder is on Deck 5 at 10:46 and not on Deck 1 at 10:50-11:00.** The meeting card plays
  at 11:00 with nobody there; she reaches the Deck 1 lift at 11:17 ("Follow me. Watch this one." then), when the watch
  step starts. "Your turn" 11:27.
- Your turn: the relay job on the rack, tapped (the rack, then the panel's pin): "You set to work on the bridge relays:
  about 12 minutes" and it's done and turned in (+15 credits) with **no read, pick, swap or test step**. The same happens
  with a Rewiring job (rewJob) on 4-junction-2 in this build: "about 10 minutes", no wire picks. Cause: 15b's `ixChore()`
  takes only jobs with no `j.machine`, so a JOB_KINDS job on a machine never reaches workStep; jobBegin's repair takes it.

### Findings
**Must**
- M1. The ladder order (lead / EP2 decided, B1 builds it): M19 really opens on Day 19, not Day 17. Not B2's to fix; B2's
  mech_check part should then check the lesson opens on Day 17 for a steady Senior without training m15/m17 first.
- M2. Calder must be in the relay room for her 11:00 meeting (the user's rule: a staged scene, the person there). She only
  walks once the watch step starts (worksEscort follows watch / do / held only). Bring her there before 11:00 (Deck 5 to
  Deck 1 takes her about 15-17 minutes) and have the scene start with her in the room; prove it live.
- M3. The relay and battery jobs must play by tapping, with their stops: read the lamps, the pick card (a wrong pick
  reopens it), swap, test. Today a tap does the generic repair and pwrDone counts a use with no pick. The fix touches 15b
  (ixChore's `!j.machine`, the interactions engineer reviews) or the jobs' shape; also check the controller can do each
  stop. The same hole is in M15 Rewiring (0.93.2, pre-existing): told lead 39 separately.

**Should**
- S1. The ask is a Mail and a toast; the beats rule says in person first. Calder could say it in the bay at clock-in (or
  where you are), with the Mail as the record.
- S2. The game arrow during the watch and your turn stayed on an old team job ("Tap the lift: Deck 4 · hold it steady",
  from "Scrubber fan change ... Emeka started without you" at 09:45) while the lesson's step arrow (level 2) waited.
  Likely older than Step 5 (checking on the base); for this beat, the lesson's own step should win while it's on.

**Verdict on 3c38a65f: FIXES NEEDED (M2, M3; M1 is B1's).** The beats around the lesson (the notice, the level 1 arrow
and its ring line) work and read well at phone size; off is identical.
