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
  chatOpen. `P997_WORD` (crew id -> { day, shut }) is in memory, not saved. Say hello skips the 'hint' line with the
  switch on (chatDo 'chat' loop).
- **38, the curious reply.** The words were the cause: 572 of 575 `listen:` replies asked about their story instead of
  answering the ask. Every talk in content/talkpack has a `listen2:` line (answer first, then the same question; the old
  indented answer still fits). content_gen.py: new optional key `listen2` (after listen:, own indented answer optional,
  baked as replies.listen2). lines_check: listen2 checked as a button (44). Section 22's talkPackFill swaps it in only
  with the switch on.
- **39, hosts.** Section 20's socApply calls `p997HostNote(d, t)` on the 'tradition' note (section 18's eventsNoted
  passes host = e.ev.host, you = joined): +4 (`P997_HOST_PTS`) to the host, once a ship day a host (`P997_HOSTED`,
  in memory), not when their kept invitation for that tradition (apptList, kind 'invite', trad) already gave +5.
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
