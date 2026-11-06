# Handover: SC1 for 0.99.7 (social life and crew stories; not the older SC1 of plans/handover-sc1.md)

Role: builder for the user's playtest notes 17, 32, 38, 39 (plans/patch-0997.md on claude/lead-49). Lead: lead 49
(session_01GKuymjjreuZtZeDMBX79xn). Reviewer: RV33 (session_01GKuymoAK9gACR31MRd1CMX). TB6 (hosted traditions):
session_01GKuymj43WbsuRbKgL2mYc2.

Branch: claude/p997-social, from claude/integration d7ad4c58 (0.99.6, game f6ff5ec1...db8a8). Build numbers untouched.

## What's built (all behind `var P997_SOCIAL_ON = false;`, section 20c's slot, end of the Social engineer slot)
- **17, Get to know.** `p997Buttons(C, buttons)` (called from section 20's chatShow) adds "Get to know" second in the
  main row whenever `p997Beat(C)` finds a beat: `momentReady(p)` (the arrow's own test), else the card's goodbye moment.
  Removes "Sit with them" and "Ask about…"; adds "Do you know…?" (introductions) when `introOptions(p)` has anyone.
  chatDo `'getknow'` plays it (momentShow). After an introduction the card goes back to the main row.
  Cause: the arrow (storyArrows) asks momentReady only; the old Sit with them needed the card's opening line to be the
  hint, which chatLine only reaches after many other kinds and only after week 1 (socGate('done')), and Say hello
  replaced the line so the button vanished.
- **Ask about: cut and parked** (design-doc.md "Social life", 2026-11-06). Code kept; off with the switch on.
- **32, the arrow once a day.** `p997WordOk(id, mid, now, peek)` in storyArrows and its done; `p997WordSeen(p)` from
  chatOpen; only opening their card shuts it for the day (RV33: not the beat flickering off as they walk). `P997_WORD` (crew id -> { day, shut }) is in memory, not saved. Say hello skips the 'hint' line with the
  switch on (chatDo 'chat' loop).
- **38, the curious reply.** The words were the cause: 572 of 575 `listen:` replies asked about their story instead of
  answering the ask. Every talk in content/talkpack has a `listen2:` line (answer first, then the same question; the old
  indented answer still fits). content_gen.py: new optional key `listen2` (after listen:, own indented answer optional,
  baked as replies.listen2). lines_check: listen2 checked as a button (44). Section 22's talkPackFill swaps it in only
  with the switch on.
- **39, hosts.** Section 20's socApply calls `p997HostNote(d, t)` on the 'tradition' note (section 18's eventsNoted
  passes host = e.ev.host, you = joined): +4 (`P997_HOST_PTS`) to the host, once a ship day a host (`P997_HOSTED`,
  in memory), not when their kept invitation for that tradition (apptList, kind 'invite', trad) already gave +5, nor for an appointment's event (ev.appt or an appt- id: apptKeep gives its own; TB6 confirmed 07:25, hosts are ev.host).
  TB6 asked whether their hosts are ev.host; if a hosted thing of theirs bypasses the bus they can call
  p997HostNote({ id, you: true, host }, shipNow()).

## Tests
- Off: `cadet_test.py` old 0.99.6 vs the build: ALL IDENTICAL.
- On (a copy with the switch line flipped): stories_check (36 days), social_check, talk_check, day_check OK;
  lines_check PASS (112 warnings, as before); names_check OK; check_fast OK on the build.
- Probe: scratchpad p997_probe.py (on/off), copied to `tools/p997_probe.py`: `python3 tools/p997_probe.py BUILD on|off`.

## Loose ends / questions for the user
- 38's default (lead listed it for the user): the curious reply answers then asks back.
- P997_WORD and P997_HOSTED aren't saved (a reload can show the arrow once more that day, or let a host give twice).
  Saving them would change section 20's save shape: ask the lead first if wanted.
- 4 talks don't fill listen2 in the probe's context (the probe fills every talk for one speaker; likely
  placeholders that need the right speaker). Not checked further.

## Status (2026-11-06 ~07:55 UTC)
RV33 PASS on 77e573f (game 6df22594...1705), including RV33's note 32 fix (6c39f3b) and TB6's appointment rule
(77e573f). Ready for the build master. RV33's stories_check runs showed 14 FAIL lines that are identical on the
unchanged 0.99.6 build (not this branch; RV33 and the lead are settling it); my own stories_check 36 on the
switched-on copy said STORIES CHECK OK. SC1 standing by.

## Later work (2026-11-06, for leads 49 and 50)
- Reviewed GM1 (claude/p997-games): FIXES NEEDED on 9175156, PASS on 98e612e (plans/review-sc1-gm1.md).
- TB6's words: claude/p997-words ab0e13e (content/works/trad-0997.lines), RV33 PASS.
- Round FAIL I (controller, Day 34 "About the transfer"): check-side. With Ask about gone the card's row 2 has two
  buttons over a full-width one, and controller_check's pad_to bounced between them (bigger-gap steering). Fix:
  claude/p997-padsteer 2ce2a48 (FOCUS_ON: an axis counts as 0 when the target spans the highlight across the way).
  'ending' passes with it; 'tiles' needs GM1's 3966a4a (J) as well.
- Round FAIL O (Leila's Day 2 booths scene "missing"): check-side. It plays at 18:13 as bubbles (traced:
  intro done 'd2-booths:said'); fresh_walk's record doesn't log bubbles. A should for TP1: the TP997 arrow points at
  Booth 1 from 17:45, so you're mid-call when Leila "shows you how"; at Leila from 18:00 would be better.
- 0.99.8 review (lead 50): TP1's claude/p997-tips 913ba6c (TP998_ARROW_ON, TP998_BOOTH_ON): PASS, sent to BM27, lead 50
  and TP1. Off identical (cadet vs 0.99.7 ALL IDENTICAL); both on: player_check OK (alone; beside three other checks
  it failed 5 save lines from load, 0.99.7 alone also OK), arrows default and week OK, check_fast OK on build and
  copy, fresh_walk Day 2: arrow at 18:00 to the room, no booth call, Leila's beat at 18:11. Small note to TP1: the
  booth guard at the top of actStart shows the screen without walking over.

## Standing down (2026-11-06 ~19:45 UTC, about 55% memory, at lead 50's request)
Nothing open. Branches: claude/p997-social (notes 17, 32, 38, 39; merged into 0.99.7), claude/p997-words (TB6's
words, RV33 PASS), claude/p997-padsteer (controller_check fix for FAIL I). Gotchas for a successor: run heavy browser
checks two or three at a time at most (six at once timed out page loads; four at once made player_check's save part
fail); controller_check's 'reach' part runs over two hours beside other runs; fresh_walk's record has no speech
bubbles (use FW_TRACE with SHIP.intro.done for beats).
