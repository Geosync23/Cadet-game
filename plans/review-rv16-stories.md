# RV16 review: crew stories stage 1 (FX21, 0.92.6 item 19)

Reviewed: claude/p926-stories fac10f39 (game 042f1659), against frozen 0.92.5 claude/staging-0.92.5 53c11f8.
Words: CS1 (claude/crew-stories-pitch 94f8c1b7). STORIES_ON is off as shipped; S7 (switching it on) waits for the user.

## Verdict: FIXES NEEDED (two placement problems seen in the browser; all checks pass)

## Checks
Switch off (the build as it is):
- check_fast: QUICK CHECK OK (words baked, names, deck, machine, device, leave).
- cadet_test vs 53c11f8: ALL IDENTICAL (renderer noise only). Note: a first run made beside check_fast showed
  differences in shots f, g, h (max 157); run alone it is identical. Run cadet_test on its own.
- lines_check: PASS (0 errors, 49 warnings, none about the stories).

Switch-on copy (`sed 's/var STORIES_ON = false;/var STORIES_ON = true;/'`):
- stories_check 30: STORIES CHECK OK. Play: Saad 4 Day 13, Halloran 5 Day 18, Kovac 4 Day 19, Theo 5 Day 21, Pell 7
  Day 22, Basil 4 Day 25. Miss: every quiet ending, Theo's by Mail. Same as FX21's numbers.
- day_check Days 13, 16, 17, 18, 19, 21, 22, 24, 25: DAY CHECK OK, all nine.
- events_check 28: EVENTS CHECK OK.
- player_check (saving): PLAYER CHECK OK.
- Save and reload mid-story (plans/rv16/save_probe.py, a real reload with saving on): played to the end of Day 18
  with Kovac's lift booked for Day 19, saved, reloaded: the story state came back identical, then Days 19-30 ended
  every story on the same days as the unbroken run (the probe's one FAIL line is the harness: Kovac's invite Mail
  went out before the save point).
- Browser at phone size 390 x 844 (plans/rv16/look_probe.py): Halloran 5, Kovac 4, Theo 5, Saad 4, Basil 4 each
  opened and played through to "told". Story scenes play in the panel, not in bubbles; the bubbles that were up
  (Captain, Commander Vance, crew chatter) sat on their speakers' heads (0 px off). No page errors.

Code (diff against 53c11f8): no R() anywhere in the stories code; nothing at load but the STORY_VOICE lay-over
behind `if (STORIES_ON)`; no new colours or meshes (no col() or coplanar concerns); every hook in old code is behind
STORIES_ON or returns null while off; the new `day:` and `here:` line conditions clash with no existing words.

## Findings for FX21 (and CS1 where words are involved)

1. **Kovac 4 never happens at the lift (fix before S7).** Her invite says "The Deck 5 lift lobby, 15:50", but by her
   own plan she is already sitting in the auditorium (Deck 7, seat 7-seat-17) from 15:40, so at 15:50 nobody is at
   any lift lobby. The scene about riding the lift ("Four, please", "Lovely lift", "Nobody's holding the rail")
   then plays in her auditorium seat while the Captain's address is going on (plans/rv16/kovac_strip.png).
   Why the checks pass: storyAtSlot accepts `t < b.from + lead` anywhere, or the ev-captains-address tag, so the
   named room is never needed (stories_check's own diag shows her only at "leisure:ev-captains-address:7:A").
   Ways to fix (lead and CS1 to pick): (a) book from her own set-off time (the first minute her plan has her leaving
   for the address) to her arrival, put that time and her lift lobby in the invite, and offer it only while she is
   on her way; or (b) CS1 re-places the beat at the auditorium (for example the ride down afterwards; "Again on the
   way down?" is already a reply). Either way, add a stories_check rule: a crescendo whose `where:` names a room must
   be in that room, by their plans, at least once inside its booking.

2. **Saad 4's times don't match the storm (fix before S7).** The storm starts Day 12 at 14:00 (onset) and is in its
   escalation all of Day 13 from 06:00. The booking is Day 13 06:00-22:00, so: the invite arrives Day 12 at 18:00
   saying "Tomorrow ... Storm's due at two" while the storm has been on for four hours; the Calendar says "06:00 The
   coolant loop with Saad"; and from 05:45 the arrow points at Saad asleep in Bunk 7 until 07:20 (tapping him only
   says he's fast asleep). Fix: CS1 re-words the invite for a storm that's already on; FX21 starts the slot once he
   is up (for an event crescendo, skip sleep and wash in storyAtSlot) so the Calendar time and the arrow match.

3. **Closing a no-reply scene early still counts it (small).** momentShow's new rule ("a story beat with no reply
   counts when it ends") ignores the `finished` flag dialogueEnd passes to onEnd, so closing Basil 5, Halloran 6 or
   Theo 6 with the X after the first line marks it told. Use `onEnd: f => { ...; else if (f && STORIES_ON && ...) }`.

4. **Theo's own chatter over his send-off (small, may be older).** During the farewell panel his overheard line
   "Have you heard? The air scrubber on Deck 2 is rattling again." pops up over him (plans/rv16/theo_strip.png).
   Keep the scene's speaker out of overheard chatter while their moment is open; if older moments do the same,
   a backlog row is fine.

Notes, no change asked:
- A booked crescendo skips momentReady's usual checks (gates, when, where, one a day) and relies on the booking's
  checks; fine by design, but it is why `where: calm` doesn't stop finding 2.
- A few non-story crew snap 0.7-0.9 tiles in one frame near seats during the scenes (Kowalczyk, Janssen, Walsh,
  Alvarez, Hart, Pell): matches the known "seated one-frame snaps" backlog, not the stories.
- Halloran 5 is offered only while he's seated (half of its 07:40-08:30 booking); he's in the serving queue at first.
