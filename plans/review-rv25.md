# Review notes: RV25 (reviewer), from 2026-10-28

Took over from RV24 (session_01GKuymnJuoJTWnmYunbN7EP; notes plans/review-rv24.md and plans/handover-rv24.md on
claude/review-rv24). Lead 43 (session_01GKuymjoDoY2kA9yCK12NG1). My session:
session_01GKuymnnpKvNH4Ki69KEzwG. Notes-only branch claude/review-rv25: I never change the game or push to builders' branches.
Verdicts (PASS / FIXES) to the builder, lead 43 and BM20 (session_01GKuymiwDEgkwGmjJ2nokvg).

## Priorities (lead 43)
1. EV1 visit-on (claude/visit-on, session_01GKuymmJANJaZkFuhsM9bBt): the Diplomatic visit in real play, Days 16-19.
2. Dev mode turns (DM1, trunk claude/devmode-j0).
3. Sound update turns (SD3, claude/sound-r3, SND_R3_ON off), including the one-line hooks in other owners' sections.

## Setup (done 2026-10-28)
- playwright (pip) with /opt/pw-browsers/chromium (153), three r128 and acorn 8.12.1 in /tmp/cadet-work; a second lane
  /tmp/cadet-work2 sharing them.

## Log
- Waiting for RV24's word that it has handed over; reading only until then.
- 11:25 SD3 asks me to review sound 667ad05e (room B home chime; plus cacfba97's design-doc "Sound" and the audio-todo
  line), saying RV24 passed it to me. Asked RV24 to confirm the handover (its handover note is still 2026-10-27's).
  Worktrees ready in /tmp/rv25: wt-visit (cf67777), wt-base (staging-pad e01bcee), wt-e158 (e158dcf, the base of
  visit-on and sound-r3), wt-snd (667ad05).
- 11:27 RV24 handed over (handover-rv24.md d199c59f): open are visit-on (not started), DM1 J3 2b88ad2 (RV24 may send its
  verdict; else I re-run devmode_check and dev_arrow_check), sound 667ad05e. My session id is session_01GKuymnnpKvNH4Ki69KEzwG
  (my first commits and messages gave a wrong one; corrected to RV24 and SD3).

## EV1 visit-on cf67777 (base e158dcf)
- Code read: draft cleared under EVENTS_ON in the swap block; gifts 09:00, farewell 09:30 on @gather-shuttle-bay;
  eventGuestDays falls back to evCalPlan() (fixed for the game: the calendar, EV_SKIPPED, endCalClosed), so the planner
  rule holds; they/them words; no she/her left for the Veyli in the game or content.
- Words (should/fix): content/reactions/guests.lines still says two formal dinners: "Brennan's planning two formal
  dinners" (warning, galley), "Second formal dinner tonight" and "Two formal dinners in three days" (escalation). The short
  visit has one dinner (Day 18), and these now show in real play.
- Runs: cadet vs e158dcf ALL IDENTICAL (1-level noise); day_check 16 OK, 17 OK.
- day_check 18 OK. events_check FAILED (1891 s): (a) "the live storm didn't end cleanly": a check slip, D.left = SHIP.event
  (a record) tested against 'diplomatic' (line 847); traces and the 'how it went' Mail present. (b) reading-corner day 7
  "not reached farouk-olu>3-lounge-28 16:00": base e158dcf's events_check queued to compare. Sent to EV1 and lead 43 (12:3x).
- 12:0x lead 43: reading corner (farouk-olu, Day 7) is known-old FX24-2; J3 already PASSed by RV24. Order: visit-on, sound
  (667ad05e + SD3's check commits, tip e748f560), then DM1 J4 (claude/devmode-j4 c7489b5).
- EV1 12:10: check slip fixed in 2e4e070; dinner words fixed in its next push; its own career_check has a NEW fail (steady
  Senior 54 not Trusted 55 by Day 19), sent to lead 43 for a call.
- day_check 19 OK; promo_beats OK; bigevents OK (visit phases and meetings Days 16-19, no clash).
- arrows_check OK (cf67777). New tip 8c91437 (e316a3e words: one formal dinner, new line ids; 8c91437 lead 43's option b:
  the visit's own jobs top up your xp to your tier's worth): game sha256 e82e6955...59ad. Code read: the listener is in the
  swap block (section 18) and calls section 24's worksXp; j.event is set on event jobs; it is registered at load before
  section 24's turn-in listener, so it runs first, not after as its comment says (same xp total; a band word could toast
  twice if both cross a band: note). Re-running on it: cadet, career, events (lane 1); lines, promo_beats, vis_play (lane 2).
- 8c91437 runs: cadet ALL IDENTICAL; career only the old backlog 12; events only the old FX24-2; lines PASS; promo_beats OK.
  cf67777: fridays OK, lines --day PASS, arrows OK.
- vis_play.py (8c91437, Dev career Day 16, frames skipped between draws, clock-in by clockPunch): warning chatter Day 16;
  onset message 10:00 Day 17 (shot visit/d17_1005.png); Veyli aboard Wed-Fri; farewell crowd at the shuttle bay 09:35 Day 19
  (visit/d19_0935.png), gone at 10:00; afterglow chatter; calls 164-184; no page errors. No arrow to the greeting, gifts or
  farewell (by design: notify / tap to join). Dev career Day 16: a Senior told "Your Tier 3 test: tomorrow" (DM1 note).
- **VERDICT visit-on: PASS at a1917dd** (game 8c91437, e82e6955...59ad), sent ~13:5x to lead 44 (now the lead,
  session_01GKuymj3tKpX7xwDZwBh8RM), EV1, BM20. Notes: listener order comment; no arrows to the visit's meetings (question);
  the Dev Day 16 test toast.

## Next: sound 667ad05e + e748f560 (SD3), then Dev mode J4 c7489b5 (DM1, session_01GKuymkR7Z42FfTQyt2VWe3)
- Lead 44 (13:12): run day_check 16-19 and lines --day on the final game too (8c91437 = a1917dd's game): queued (lanes 6, 7).
  bigevents_check edits read as owner: fine.

## Sound 667ad05e + 451e00e5 + e748f560 (SD3): PASS (~14:0x, to lead 44, SD3, BM20)
- cadet vs e158dcf ALL IDENTICAL (off); sound_check OK as is and on an ON copy (r3fx room B: first opening r3Home, second
  not); base e158dcf FAILS the four r3 parts by e748f560's intended rule. Code read section 27 only. design-doc Sound
  (cacfba97) and 667ad05e's lines read: match. Notes: the move flag is memory only; a crew-opened door near you counts.

## Dev mode J4 c7489b5 (DM1): code read
- DV_MORE night, m21 (first), mtcq, end, event; score's `first`; endBye at bayAt + 1. Finding to confirm: 'event' source
  has no evInvited(m) check, so the vessel's meetings (ranks: []) would get an "Event:" arrow.
- 13:59 lead 44: the user wants a player pointer for the visit's three events in 0.96.0 (my note 2). EV1 builds it on
  claude/visit-pointer (from 736b23a); top priority when it arrives, ahead of J4.
- 8c91437: day_check 16, 17, 18, 19 OK; lines --day PASS. visit-on PASS confirmed on the final game (to lead 44, BM20).
- J4 runs: cadet vs e158dcf ALL IDENTICAL; devmode_check OK; dev_arrow_check OK; j4_event.py (rv25-shots/j4_event-c7489b5.txt):
  the "Event:" arrow on the vessel's ranks: [] planning holds (Day 27 09:50-12:00, Day 28 09:25, Day 29 09:15 and 14:25).
- **VERDICT J4 c7489b5: FIXES** (add evInvited(m) to the 'event' source's filter), to DM1, lead 44 (BM20 copied via lead).
- J4 de25560 (evInvited filter, evScriptOf title): cadet ALL IDENTICAL; devmode_check OK; dev_arrow_check OK; j4_event.py:
  the Captain at the glass on, no Event arrow on the vessel's holds. **VERDICT J4 de25560: PASS** (~15:0x, lead 44, DM1).
  Note for DM1: Dev career Day 27 Specialist still offered m17 (lift roof); Dev career Day 16 Senior told of the Tier 3 test.

## EV1 visit-pointer 6db1cdd (game a9364fd, base 44ea40ef, PAD and sound on): PASS (~15:4x, lead 44, EV1, BM20)
- cadet vs 44ea40ef ALL IDENTICAL; check_fast OK (334 s).
- vp_play.py / vp_gifts.py (pad, 390x844): greeting heads-up 09:45 Day 17 and scene 10:00; gift exchange heads-up 08:47
  (pointer/gifts_hu_0848.png) and 09:07, scene in the observation room; Calder's pu4 offer can open first, the gifts then open
  in their 20 minutes; farewell arrow "Tap Saruth to see the Veyli off" with the star marker (pointer/d19_by_saruth.png),
  pad A on crew:saruth joins tj:farewell. tradJoinable: only 'farewell' has a TRAD_JOIN key among the visit's moments.
- Gotchas: controller_check's QUIET hides #devHu (pass quiet= without it to see heads-ups); my probe names must not shadow
  controller_check's globals (ST, log, D...), else "game failed to start".
- 15:1x lead 44: 0.96.0 round on (BM20 + 4 runners); I'm idle until called. Memory ~29%.
- 16:2x EV1 6522974 (mech_check MRUN: SHIP.stores.lamp = 3; the visit's Day 16 lamp job empties the shelf): PASS on a code read, no browser during the round (to EV1, lead 44, BM20). Idle again.
- 16:4x round finding (lead 44): join_check farewell "don't name the same person" on 65229747. Cause: marker '★ ' + tjFirst
  = shortName('Envoy Saruth') = 'Envoy', the tip banked "Tap Saruth". Game gap (also the vessel lights' "Tap Envoy to stand
  at the glass with Saruth" since 0.94.0). Fix proposed: tjFirst gives the second word of a two-word Envoy/Speaker name.
  Scratch copy: JOIN CHECK OK (pointer/join_check-tjFirst-fix.txt). Sent to lead 44, EV1, BM20; EV1 to commit after puzzle.
- 17:3x EV1 fixes on claude/visit-pointer fe11cd66: **PASS** (to lead 44, BM20, EV1). cadet vs 6522974 alone: 0 px in every
  shot (truly identical). puzzle_check OK (p9 staged Day 22 after retries); join_check OK (farewell and vesselLights name
  Saruth). 72bb4a3 owner read (24k): staged sets case.p9.first; trained or open p9 -> 'none'; retry window from saved W.op;
  P9_MISS memory only (one extra look after a load, harmless); t4 needs no p9. 8eef718 check only.
- 18:xx lead 44 asked why PAD_ON costs script time with no pad (perf bisect). Code read: all per-frame pad work is inside
  padTick, which the main loop runs only if PAD.live (set by gamepadconnected); no observers/intervals. Probes
  (rv25-shots/pad_prof.py, pad_time.py, pad_same.py) on fe11cd66, Sunday dinner: PAD.live false; crowd/crew hash identical
  on/off; profile shows no section 26 function; timing medians on 3.21 / off 3.98 ms with ~1-2 ms run-to-run spread.
  Reported: no cause, can't reproduce; suggest re-measuring alone, alternated, several times.

## Dev mode J2 93449f7 (DM2, session_01GKuymoBtAFGaak9qYYXS24): PASS (~22:4x, DM2, lead 44)
- cadet vs fe11cd66 ALL IDENTICAL; devmode_check OK (events1, events2); dev_arrow_check OK.
- j2_list.py: 28 rows on, 5 min before each moment; visit gifts Day 19 08:55 Observation room, farewell 09:25 Shuttle bay.
- Code read: times from event data via evBeatAt/evCalPlan; VESSEL set at load; no R(); dmEvMeet by evInvited; End and
  keep's message names DM2-1's limit. Note: the formal dinner jump lands in the closed, empty Captain's quarters.
- 21:59 lead 44: the 0.96.0 round finished; two browsers fine again.
- J5 86958252 (game 67728794...8cbb): **PASS** (~23:1x, DM2, lead 44, BM20). cadet vs fe11cd66 ALL IDENTICAL; devmode_check
  events1 OK: evVisitDinner Day 18 18:55 Galley (3 'K'). design-doc Dev mode text matches. Dev mode J0-J5 fully reviewed.

## 2026-10-29 01:5x lead 44: 0.97.0 is live. Tonight's queue (as they arrive): RB1 session_01GKuymkqMpME5GQvc5vTBqR (0.98
render turns 3-4: pixel-identical, or a picture for the user first); OP1 (0.98 walk-estimate fix: FX24-2, FX12-1, TQ1-1);
SD3 (SD3-2 music cache); BB1 = BT1 session_01GKuymne2zVMSTZjvCCmXKH (0.99 backlog batches, claude/backlog-099). Two
browsers fine; the user wants faster turnarounds.
- Base ready: /tmp/rv25/old0970.html (0.97.0, claude/integration 610ad7f1, sha256 0bd1b5b6...). Waiting for the first turn.
- Correction (lead 44): BB1's 0.99 backlog fixes land on claude/backlog-triage (restarted from staging-pad 610ad7f1), not claude/backlog-099.
- SD3-2 0b9541c9 (claude/sound-098, music pick cached 0.25 s of the audio clock): **PASS** (~02:2x, SD3, lead 44). cadet vs
  0.97.0 ALL IDENTICAL; sound_check OK. Note: the new rate line saw 0 asks in 0.24 s real (upper bound only).
- Gotcha (mine, twice): `a && b && (x) & (y) & wait` backgrounds the whole first chain; set up first, then start lanes.
- 02:15 lead 45 (session_01GKuymnu4NeXJhwPe21FWk7, claude/lead-45) is the lead now; verdicts to lead 45. Queue adds BAL2.
- SD3-1 5ba395a1 (claude/sound-099; room B chime kept across reloads by a localStorage note per slot, crew openings
  excluded): **FIXES** (~02:4x, SD3, lead 45). cadet ALL IDENTICAL; sound_check OK. The note (= move day, ~always 25) is
  never cleared on New game / Delete / Load file: a second game in the slot never chimes. Suggested onSim('newGame') clear.
