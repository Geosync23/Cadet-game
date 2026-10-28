# Handover: FX21 (builder; crew stories stage 1, 0.92.6 item 19)

Lead: lead 36 (session_015LyT1p2Kivp1eaMBC7dMQi; took over from lead 35). Words owner and first contact: CS1, the crew
stories lead (session_01QcPAXHjQZ2HfZKMCTbaW9v; branch claude/crew-stories-pitch). Reviewer: RV16 (to be hired).

## Branch and builds
- `claude/p926-stories`, from staging-0.92.5 (b0916bb1), with the frozen 0.92.5 candidate 53c11f8 merged (b0b3d7f4).
- Build table rows: "p926-stories S1", "S2", "S3-S5", "S6 so far" in plans/build-table.md.
- Everything is behind `var STORIES_ON = false;` (section 20c's slot, "crew stories"). Off = the game as shipped
  (cadet_test ALL IDENTICAL against 53c11f8). S7, switching it on, needs the user's yes.

## What's built (all in section 20c's slot unless named)
- **Words** (content_gen.py): `content/stories/*.arc` bake into section 22's `STORY_MOMENTS`; `content/stories/*.voice` into
  `STORY_VOICE` (laid over VOICE at load, only while on). `content/stories/waiting/*.story` are CS1's later stories
  (not baked). The old `content/arcs/` and `MOMENTS` are untouched (the old Pell 5-8 and Kovac 1-4 still play while off).
- **Grammar** (content/README.md documents it): a script line `if <conditions> | who: text`; conditions `day:` (21,
  19,26, 3-21, 15-, -20) and `here:<crewId>` (section 22's lineCond, lineQ 'storyHere'); beat fields for stories only:
  `crescendo:` (trad:<id>, event:<id>, farewell, meal:breakfast|dinner), `quiet:`, `follows:`, `lead:`, `title:`,
  `invite:`, `cast:`.
- **Order** (`storyNextId`, asked by momentNextId): lowest beat not told and not skipped whose `follows` is told; beats
  up to rel.arc count as told except `follows` ones; before the story file's first beat (Pell 2-4) the old order runs.
- **Crescendos** (`storyTick`, from socialTick): books the next crescendo it can (gates as they'll be then; one a day;
  only when by their plans the person and cast are there, `storyGoes`); Mail at 18:00 the evening before (`invite:`);
  a Calendar row (`storyCalRows`, section 19's Calendar); plays only at its gathering in its booking
  (`storyCrescReady`, from momentReady). Told: its quiet ending skipped (`storyDone`, from momentDone). Missed: the
  booking passes, the day: window passes, or a one-off gathering ends unbooked (on a day its day: allows): skipped
  (`storySkip`); someone who has left gets the quiet ending by Mail (`storyPost`). A plain beat whose day: window
  passes is skipped too (its quiet: next, or counted as passed in rel.arc, CS1's (c)).
- **Planner hook** (lead 35's (A)): section 18's `evArrive` lets a crescendo's teller and cast go to its gathering on its
  day:-named days (`storyCastGoes`, pure: baked words and STORIES_ON only), if free. Proved: day_check OK on Days 17,
  19, 24, 25 and events_check OK (28 days) on a switch-on copy.
- **Favours** (`STORY_FAVOURS_S`, read by 20c's storyFavour): theoCloud, basilPlant (flag `bramwell.plant.done` two days
  after hand-back), emekaJokes (three stops; `halloran.jokes.done`). Flags set by storyTick (SHIP.social.stories.cs.fav).
- **Goodbyes**: `storyOwnBye` (Theo): chatLine's goodbye card and goodbyeMoment leave it to his farewell crescendo.
- **Roster words**: `STORY_ABOUT` (Halloran tier 3, Theo tiers 3 and 4), laid over while on.
- **Arrows**: `storyArrows` (guideAsk: a booked crescendo level 2 from 15 minutes before; a ready beat level 6, "X wants
  a word"); `storyDevNext` adds a "story" row to section 25's dvCareerNext.
- A story beat with no reply counts when it ends (momentShow's onEnd).
- State: `SHIP.social.stories.cs = { told, skip, book, cday, fav }`, saved with SHIP.social.stories, written only while on.

## How to test
- `python3 stories_check.py starship-cadet.html 30` (about 10 minutes): part 1 off; part 2 a switch-on copy played twice
  ("play": every crescendo; "miss": none) with the rules; part 3 a self-test (13 planted faults). It prints each story's
  days, bookings, and for a crescendo due but never booked, why (here, cast, gates, flags).
- Off gates: check_fast; cadet_test against the base. Switch-on proofs for the hook: day_check on the days it touches
  (17, 19, 24, 25), events_check 28. Make the copy with `sed 's/var STORIES_ON = false;/var STORIES_ON = true;/'`.
- Probe pattern used: a small script that loads a page through cadet_test's Game and evals JS (see the scratchpad's
  probe.py idea: exec cadet_test.py up to 'import sys, json, hashlib').

## Last results (042f1659, the sha for RV16)
Switch off: check_fast OK; cadet_test against 53c11f8 ALL IDENTICAL. Switch-on copy: stories_check OK (all six end both
ways: play: Theo 5 Day 21, Kovac 4 Day 19 15:50, Halloran 5 Day 18, Basil 4 Day 25, Saad 4 Day 13 (the storm), Pell 7 Day
22; miss: each quiet ending, Theo's by Mail); day_check Days 17, 19, 24, 25 OK and events_check 28 OK (run on b0b3d7f4;
the planner hook hasn't changed since). Saad 4 is lead 36's (b): where: calm, a call and a walk down; "Saad at the valve
as a day-plan piece" is a later option for the user.

## RV16's review (findings at claude/review-rv16 e4231dbe, plans/review-rv16-stories.md) and the fixes (c1feef46)
1. Kovac 4 at the lift: a crescendo with `lead:` and a named room now books the person's own walk by plan (`storyWalk`:
   lead minutes before their lift ride to the ride; plays only on the deck they ride from, `b.walk`). Open: her cast
   Cruz rides from Deck 3, so it never books; lead 36 to pick (a') drop Cruz from cast (here: lines) or (b) re-place it.
2. Saad 4: an event crescendo's window starts once they're up (storySlots skips sleep and wash). CS1 rewords the invite.
   Invites may use `{at}` (the booked time, as the Calendar shows it).
3. A no-reply story beat counts only when the scene finished (onEnd's flag).
4. `storyInScene`: no overheard chatter from an open story scene's speaker (switch-on only; older moments may do the same:
   backlog if RV16 confirms).
stories_check: a crescendo naming a room must be told there (or on its walk). Checks at c1feef46: stories_check OK,
day_check 12, 13, 19 OK (on), cadet_test ALL IDENTICAL (run alone: beside check_fast it can show f/g/h diffs), check_fast OK.

## Final turn (lead 36's (a') for Kovac; CS1's f4117e20)
Kovac 4 has no cast (Cruz's lines folded into Kovac's); lead: 28 (lead 36: a wider window), so her walk booking is Day 19 15:10-15:39 (Deck 5) plays while she's on
Deck 5 or riding from it; invites use {at}. Saad's storm window starts no earlier than 08:30 (STORY_EVENT_FROM), once he's
up. stories_check tries every minute in a walk booking. Results: stories_check OK (play: Kovac 4 Day 19, Saad 4 Day 13
08:30); day_check 13 and 19 OK (on); cadet_test vs 53c11f8 ALL IDENTICAL (alone, off). Backlog FX21-1 (RV16): socialChatter
has no DIALOGUE guard (older moments and meetings). If RV16 asks for more, a fresh FX21b takes it from here.

## Loose ends
- S7 (switch on, after review and the user's yes): flip STORIES_ON; retire the old Pell and Kovac words (content/arcs
  pell.arc, kovac.arc parked by CS1's rule); kovac-zainab.lines' joy line (the spanner grip, a comment at kovac.story beat
  6); torres.arc waits for stage 2; then the full six-runner round.
- Moments never open in week 1 (chatLine's socGate('done')): Theo's Day 3 beats really start after week 1 (CS1 knows).
- Basil 2's "if beat:torres.5" reads the old Zeke arc's beat 5 (same beat in both versions; CS1 fine with it).
- The Works tea corner has 3 seats: a crescendo there can't seat its cast (why Pell 7 became a Works bay moment).

## Gotchas
- `var` for STORIES_ON, STORY_IDX, STORY_CS0, STORY_CAST and the favour table: voiceOf, momentDef and evArrive may ask
  before the slot's lines have run (a `const` would throw).
- A comment placed mid-line in a minified-looking line cuts the rest of the line (names_check catches it: run it).
- stories_check steps every 10 minutes: Off the Tern lasts 20 minutes.
- Two browser checks at most at a time (the lead's rule); pause everything when the lead announces a round.
