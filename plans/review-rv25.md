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
