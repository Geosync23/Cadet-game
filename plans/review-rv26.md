# RV26 review notes (second reviewer for 0.99, hired by lead 45, session_01GKuymnu4NeXJhwPe21FWk7)

Style as RV25's (plans/review-rv25.md on claude/review-rv25): code read, targeted checks, cadet_test against the base,
verdict PASS or FIXES with exact reasons. Base for all three: claude/staging-pad 610ad7f1 (0.97.0, live game).
Builds and logs in my scratchpad (not committed). Probes kept in plans/rv26-probes/ when worth keeping.

Queue (lead 45, 2026-10-29): 1. TB1 title screen claude/title-099; 2. EV2 seated dinner + vessel words claude/visit-099;
3. SD3 title music claude/title-music-099 (on top of title-099). RV25 keeps 0.98 (OP1, RB1); told RV25 I took TB1/EV2.

## TB1 title screen, claude/title-099 8d2a708 (session_01GKuymo2ikX7y7GA88GPXQP)
- cadet vs 610ad7f1 ALL IDENTICAL. names_check (branch's, with the two-switch rule) OK. title_check OK (switched-on copy
  it makes itself; the switch as built: no title, nothing held, even with ?title).
- Code read: off, the page's first script returns at once (TITLE_EARLY false), titleBoot only hides #title; titleHold() in
  freezeSync/saveGame is false (TITLE is a var, undefined until section 30 runs, then on: false). No listeners, no pad
  panel, no onSim when off. The CSS only adds #title to the phosphor lists and #title rules (hidden). On: the first
  script reads only (no writes); a pick made before load waits in data-pick; Continue waits for the first frame (READY);
  saves refused under the title are made on hand-over; Escape/B keep playing; Start is Continue (unshifted ahead of Pause).
- **VERDICT TB1 8d2a708: PASS** (sent to TB1, lead 45, BM20).

## EV2 seated dinner + vessel words, claude/visit-099 b21a531 (session_01GKuymn7YSDpEbeNYGxup6N)
- cadet vs 610ad7f1 ALL IDENTICAL; day_check 18 OK; names_check OK.
- Code read: VISIT_DINNER_ON = EVENTS_ON && EV_SWAP_ON (on); OCCASIONS.veyliDinner due on vdDay() (evCalPlan + 2 = Day 18);
  occasionAdd copies o.places onto the appointment (only when the occasion has places: other occasions unchanged); two
  event-only seats 2-captable-7/-8; EV_BEATS 'beat' 18:45-20:15 Day 18; the dressing is the visit's only escalation
  dressing (nothing overwritten); vdTick: arrow from 18:45, seated once from 18:55 (q.f.sat, saved with the occasion).
  V-2 words: five lines, the visit "last week".
- Play probe (plans/rv26-probes/vd_play.py, Dev jump to Day 18 18:40, 390x844):
  in room C: everyone walks to their own chair (marrow -5, teshavi -7, saruth -1, vance -2, kesrin -8, moleth -4,
  ithra -3), all seated sit:talk by 19:05; you seated and eating at 18:55 (2-captable-6); the scene from 19:00, the
  choice, all 11 lines; the meal ends ~19:31; kept at 20:15, the diners leave by the lift. Shot: the table with food.
  in the galley: the arrow vd:dinner from 18:45 to 20:15; missed at 20:15 with the gist. (A Dev-jump-only promo:home
  arrow, from a cabin move you never walked into, hid it in the first run; cleared by setting promo.sight.home.)
- Notes (not blocking): the Captain, Kesrin and Ithra are still walking in when the scene opens at 19:00 (the Captain
  says "There you are" on the way to her chair); after the 40-minute meal you stand up at ~19:31 while the dinner runs
  to 20:15; Dev mode's jump label "the formal dinner, from the galley" (and its comment "nobody sits there") is now stale
  (the user said no Dev work: a backlog row); EV_BEATS takes the day from EV_CALENDAR, vdDay from evCalPlan (differ only
  if the visit ran late).
- **VERDICT EV2 b21a531: PASS** (with the notes above).

## SD3 title music, claude/title-music-099 19798c3 (on title-099 8d2a708; session_01GKuymir9eBj7X6kLtwLRmq)
- cadet vs 610ad7f1 ALL IDENTICAL (title off as built; SND_TITLE 'A' only acts while SND.titleOn, which only section 30
  sets with the title on). names_check OK. sound_check (branch's, with the new title part) SOUND CHECK OK: candidates
  64 / 71 / 58 s, 'Event', not on the Music list; on: running, one copy, hum hushed; off: [0, False].
  title_check on the SD3 build: TITLE CHECK OK, no page errors.
- Real flow (plans/rv26-probes/tm_flow.py, title switched on in a copy, ?title&nosave&sound): loaded, ship held
  (06:00); a tap on the title: context running, titleA playing, hum:quarters hushed, clock still 06:00; NEW GAME: title
  gone, ship runs, title track list empty, hum back. No page errors.
- Code read: S.frame keeps the context running only while SND.titleOn; the rooms' once-a-second sounds wait under the
  title; titleTick runs only while on or fading; the hum bus's gain is set back to 1 (its own default; nothing else sets
  it). Music app off: no title track (the hum still hushed: a silent title). SND_TITLE 'A' is the provisional pick
  until the user chooses on plans/sound/title-music.html.
- **VERDICT SD3 19798c3: PASS.**

## EV2 follow-up, claude/visit-099 60287f2 (my four notes)
- Diff: occasionAdd's optional `early` (appointment from at - early, len + early; only veyliDinner sets it, 10);
  your meal lasts to the dinner's end (min 20); comment on the hold's day; backlog EV2-1 (Dev jump). Others unchanged.
- cadet vs 610ad7f1 ALL IDENTICAL; day_check 18 OK.
- Probe (vd_play.py now takes VD_AT): from 18:40 in room C, all seven seated by ~18:55, the scene at 19:00 with the
  table full, you eating (80 min) to ~20:08, kept 20:15, diners leave. Walk-in at 19:05 (VD_AT 1145): seated at once
  (70 min), the scene starts for you from its first line, eating to ~20:10, kept. No page errors.
- Note: the Schedule row shows 18:50 while the Mail says 19:00 (EV2 flagged it); arriving early is harmless.
- **VERDICT EV2 60287f2: PASS.**

## EV2 follow-up 2, claude/visit-099 3dda559 (appointment back at 19:00; a.early read by section 14's apptWhere)
- Diff: occasionAdd books at the occasion's own time and sets a.early (like a.places); apptWhere (section 14, the sim
  engineer's): go = a.at - min(30, a.early if > 0) - walk; the end unchanged; no a.early = as before (Number() guards junk).
- Read: only the set-off time moves (they're shown at their chair from go); apptFree/apptReply and the 'kept' rule still
  use a.at; only section 18's occasions set early, so day plans without one are untouched (cadet identical).
- cadet vs 610ad7f1 ALL IDENTICAL; day_check 18 OK; probe from 18:40: all seven seated by 18:55, scene 19:00, you eating
  to ~20:07, diners leave 20:15. No page errors.
- **VERDICT EV2 3dda559: PASS.** Section 14 line: fine on my read; per owners.md the sim engineer may still want a look.

## Handover from RV25 (lead 45, ~06:55): RB1's 0.98 render turns, BB1 FX8-1 swim look, BAL2's new tip. RV25 idle.
- OP1 claude/join-timeout c27ebb88 (join_check's real reload waits 120 s): PASS on a read. a.early across save/reload:
  confirmed on 3dda559 (deviceLoad maps { ...a, named fields }), for OP1's section 14 owner note.

## RB1 0.98 turn 3, claude/opt-098-render 8d7a314 (base b9b7e3d7 = 0.97.0; session_01GKuymkqMpME5GQvc5vTBqR)
- Code read: bake collects each joint's corners; bodyBake makes one mesh (bodyJ attribute, a 16x32 float DataTexture,
  NearestFilter by default, so texels are exact); bodyTick on scene.onBeforeRender (r128 calls it after
  scene.updateMatrixWorld and before the shadow pass) writes matrixWorld, camera inverse x matrixWorld, its normal
  matrix and the sun's shadow camera x matrixWorld in float64 then float32, as three does per mesh; the shader swaps
  project_vertex, defaultnormal_vertex and worldpos_vertex (r128's own lines, instancing parts unused). One
  renderer.render in the game; no other scene.onBeforeRender; nothing else on layer 1. Joints never drawn (layer test in
  both passes); taps via the joints' meshes. isShown skips hidden roots (player.obj hidden in activities; crowd
  visibility). playerUniformTint swaps every joint, the body follows the first. All rig disposals traverse and dispose
  geometry (player swaps, recBody, V.opp, ROOF.mate, crew swaps), so BODIES never leaks. No float vertex textures: the
  old code verbatim.
- cadet vs b9b7e3d7 run alone: 0 px in all 15 shots, taps same; state differs only in calls 173 -> 142 and memory
  (geometries 453 -> 422, textures 34 -> 36), as intended.
- pix_rb.py (mine): 7 scenes on Decks 1, 2, 3 (dinner, breakfast), 4 (night), 5, 7 (rec Day 6), each plain and rotated,
  390x844: 0 px in all 14; draw calls 15-30 fewer per scene.
- deck_check OK; Deck 4 memory flat over the round trips (346 geometries, 39 textures each time).
- **VERDICT RB1 turn 3 8d7a314: PASS.**

## BB1 FX8-1 swimmer look (claude/backlog-triage 564b8a5): in progress (paused for RB1)
- swim_up.py fixed to read the drawn spot (rdx/rdz) on a place with moves. Day 6 14:00: Holt off the kayak glides
  74 frames, biggest step 0.08, no wall; Ishikawa off the float: 4 frames, one step 0.67, no wall. Day 6 16:00: Halloran
  out of lane 3 glides 51 frames across the pool to the changing rooms, biggest step 0.12, no wall; two fans off the
  stands 0.075 / 0.09. Day 7 10:00: a fan 0.09. No glide through a wall anywhere.
- **FX8-1 look: no wall glide, BB1's PASS stands.** Note: the float's get-up is short (4 frames) with one 0.67 step.
  RV25-1 (564b8a5) was already PASS from RV25 (code read): nothing more needed.

## TB1 title-on-099 b980518 (title switched ON over SD3's 19798c3)
- Diff: only TITLE_EARLY and TITLE_ON to true (plus DEV_NOTES, build table). names_check OK (the switches agree).
- cadet vs 610ad7f1 ALL IDENTICAL (1-level renderer noise only; run beside a probe): every check runs under webdriver,
  so no title there; title_check (as built, switched on) TITLE CHECK OK.
- The hum (lead's question): tm_flow2.py on this build, reading the hum bus's real gain: 0.33 at 0.4 s after the tap
  (ramping down before the hum has even started), then 0 while the title is up with hum:quarters running: the hum is
  started but silent. After New game: track list 0, hush off, gain 1 within 2 s. (One earlier reading at +4 s still
  showed the title's state: taken under load before a frame had run; not seen again.)
- **VERDICT title-on-099 b980518: PASS.** Note: with the title on, only title_check ever sees it (every other check runs
  under webdriver).

## OP1 claude/s5cases-fix 34adecc (check only; the 0.98.0 blocker, staging-pad 7a2ae7d2)
- Reproduced on 7a2ae7d2 with the old check: s5cases FAIL (the D-pad never reached a suspect; never reached Call it).
- Diff: the suspect regex is built from the P4 case's own c.sus (first letter capitalised) instead of a cooler's four.
  Game file identical to 7a2ae7d2. With the fix: s5cases OK ('Relay', 'Call it: relay'), CONTROLLER CHECK OK.
- Note (not blocking): c.sus holds ids; the chips show caseSus(c, s).label. They match except P4's 'sensor' (label
  "temperature sensor"), so on a cooler the regex has "Sensor" where the chip says "Temperature sensor"; harmless while
  any other suspect matches. caseSus(c, s).label would be exact.
- **VERDICT s5cases-fix 34adecc: PASS.**
- s5cases-fix 1086518 (second check-only commit): puzzle_check p6's first measures its save size as this case plus the
  shared record (as p4's does), so a second p6 a fault opened by 09:05 on 0.98 isn't counted; out.others names it;
  saveSame still round-trips the whole SHIP.works.cases. My run on 7a2ae7d2's game (byte-identical): PUZZLE CHECK OK,
  saveBytes 1924, others ['p6']. The whole save's size stays player_check --long's job. **PASS.**

## OP1 claude/nights-dayarrow 79a87ea (0.99 game fix; base 1086518 = 7a2ae7d2's game; sha256 9eb28dce...)
- Diff (28a p5nGuide, 3 lines): with no day part (S.day null) the day-sleep block runs too, unless you worked a night
  the day before (its own ask stays); `from` = S.day end, else min(now, 12:30) as a whole minute. With S.day set: as before.
- arrows_check step6 asis: FAIL on 7a2ae7d2 ("sleep by day: its level-1 arrow (p5n:bed:22) never led"); OK on the fix.
- cadet vs 7a2ae7d2 ALL IDENTICAL; day_check 22 OK (the branch's own day_check).
- My slip, for the record: day_check 22 first FAILed for me on both builds ("the Commons hold fewer ... 61 v 62") because I
  ran my branch's older day_check, without OP1's 0.98 walk-led rule (3307e84). Merged staging-pad into claude/review-rv26;
  from now on I run each build's own checks.
- Note (not blocking): p5nDayBed counts the day sleep from 05:30 when there's no day part, so on a Day 22 with no day
  shift at all (a leave or sick morning with the night still on, if that can happen) the arrow and the "Sleep now" notice
  would come from 05:30 (from = now). That matches p5nDayBed's own rule (the bed already offers it); only worth a look
  if a whole-day-off-but-night case exists.
- **VERDICT nights-dayarrow 79a87ea: PASS.**
- AS1 (11:52): the whole arrows_check on nights-dayarrow 79a87eac (sha matched), alone: ARROWS CHECK OK, 0 FAIL (2629 s).
  Supports the PASS.

## BAL2 0.99 balance pass, claude/balance-099 96dd584 (whole diff vs 610ad7f1; session_01GKuymm7ApobKpq9JW9FJgF)
- Code read: NEED_DRAIN hunger asleep 6 -> 4, fitness 1.4/.35 -> .9/.3; Lonely adds task .95; the gym tip "every other
  day"; eventJoin leisure +25. pu4ResWhen: the old loop is pu4ResNext unchanged; when its time falls after the day after
  the test (days off next), the result is the test day's 13:30 (pu4ResEve = 12:30 + 60), before the Friday address.
  pu4ResLate drives the "this afternoon" words (new keys only; old keys unchanged), set after T.passed and T.day, so in
  order. pu4Script's stand-in names the real test day (pu4TestDay(today), the same rule pu4Offered sets T.day with); no
  writer pu4.offer scene exists, so the stand-in is what plays. pu4OfferTick and pu4DevNext as in 610ad7f1.
- Checks (each build's own): cadet vs 610ad7f1 ALL IDENTICAL; career_check OK (busy: "Relied on" from Day 4, printed,
  backlog 12/17 closed); career_check --s6 OK (late Trusted: D22 trusted, t4 day 26, res 26, badge 27, T4 from D26);
  player_check OK; promo_beats_check OK.
- Notes (not blocking): the stand-in says the weekday even when the test is tomorrow ("Tuesday", not "tomorrow"); a
  Friday test's badge is a Saturday 16:30 (the lead's call, as RV25 noted); the ".eve" lines are placeholders until a
  writer words them.
- **VERDICT BAL2 96dd584: PASS** (the full six-runner round still needed before the merge, as BAL2 says).
- BAL2 follow-up 6eacbe1 (words in 24u only): the four ".eve" lines worded (Calder: lunch, "this afternoon, about half
  past one"); the stairs stand-in after an afternoon result says "tomorrow afternoon ... Torres" (pu4ResLate, still valid
  with T.res set); the offer stand-in says "Tomorrow" when the test is the next day (capitalised at the line's start), else
  the weekday. career_check --s6 OK on 6eacbe1 (my run). **PASS.**

## SD3 claude/title-music-c febdf8a (the user's pick C; on staging-099 33a3afe, title on)
- Diff: SND_TITLE 'A' -> 'C' (one line), design-doc Sound, audio-todo, build table.
- tm_flow2.py on this build: a tap on the title plays titleC with the ship held and the hum's gain 0; after New game the
  track clears and the hum is back (gain 0.86 at +4 s, 1 by +12 s; the +2 s reading still showed the title's state:
  slow first frames in headless, as on title-on-099). No page errors.
- **VERDICT title-music-c febdf8a: PASS.**

## Lead 46 (session_01GKuymiks9CC1WYr2may5nM) took over from lead 45 (~13:00): report to lead 46 and BM21.

## RB1 222ec28 (controller_check day only: clear the last toast before reading the bedtime ring's line)
- Diff: 3 lines, the same clearing as the check's own load-time line (RV5, line 169); the game's toastTimer / toastEl
  exist at top level. Game unchanged.
- controller_check day with the fix on 0.98.0's game (7a2ae7d2), twice side by side: CONTROLLER CHECK OK both
  (bedtime: "ABunk", the alarm card, Set alarm by pad ok).
- **VERDICT 222ec28: PASS** (cherry-pick alone; the branch head carries turn 4 WIP).

## RB1 turn 4, claude/opt-098-render e7bce5a (furniture that differs only in colour drawn together; base staging-099 536748f; sha256 8a0cbb86... matched)
- Code read: mergeMeshes(root, tint) only from buildDeck's furniture merge; mergeTint keys every own property but
  uuid/id/name/color/version (textures by uuid), '' (own bucket, as before) for non-Standard/Basic, see-through, alpha
  test, not FrontSide, shadowSide, vertex colours, hidden, own onBeforeCompile, GD.leaves, RK.film, PULSES, or no WebGL2.
  The twin is white with vertexColors and a flat colour varying: white x texel x c = the old c x texel (1 x t exact),
  per piece one colour so flat loses nothing. The risk is a merged material changed while you play (the twin is a copy):
  every runtime material change in the file is on an excluded material (GD.leaves, RK.film, PULSES), a noMerge object
  (MED screen, belt, Lightdisc's V.*, the cake), a transparent one (marker, 21265's glow; never merged), the tall
  pieces' own clones (merged on their own, not tinted), or a light (hemi/sun for night, events' feel), so none reaches a
  tinted bucket. RB1's probe (every deck at 06:00, 13:00, 22:30) agrees.
- cadet vs 536748f: d_wallslow 8 px (max 18), i_tap2 1 px (max 24): the corners the user approved; state differs in
  mem (geometries 422 -> 414), calls, tris only.
- pix_rb.py, 7 scenes x 2 views (Decks 1, 2, 3, 4 night, 5, 7): 0 px in all 14; draw calls 3-25 fewer per scene.
- deck_check (the branch's own) OK; Deck 4 memory flat (322 geometries, 39 textures each round trip).
- **VERDICT RB1 turn 4 e7bce5a: PASS.**
