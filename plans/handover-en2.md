# Handover: EN2, the ending's builder (E-1 the crossing back, E-4 the endgame)

Role: builder for the ending (plans/ending-spec.html on claude/p5-specs, EP2). Hired by lead 39; now reports to
**lead 40** (session_01NXybH7NNqM8M4ngiyidq6m). Reviewer: **RV21** (session_01AmTyMHLr5UuCY9zo3nQcwS).
EN1 (the offer, the goodbye, the end page; section 29a/29b) is archived; its note is plans/handover-en1.md on
claude/ending 395fe62e. Since then **this branch is the one home of the whole ending**.

## Branch and builds
- **claude/ending-crossing** (the one owner now): EN1's claude/ending 395fe62e + SW5's endgame pool (claude/ending-words-b
  8ed1545a) + SW6's words (claude/ending-words-a b8c89e7a) + my E-1 and E-4 + staging-0.93.3 19400976. See the latest
  sha in TEAM / my last message to lead 40. Everything behind `EV_ENDING_ON` (section 13, `?ending` / `#ending`).
- claude/ending-endgame (5794d693) is superseded (my E-4 before EN1's merge): don't use it.
- Build-table rows: "ending-endgame", "ending-crossing", "ending-crossing turn 2", "turn 3".

## What I own and built
- **E-4, the endgame** (section 29c, EN1's slot 'Endgame'): `endStaySet(day)` (29a's `endSettle` calls it on a Stay with
  the goodbye's day; flag `end.stay` = the endgame's first day, 36 at the earliest), `endgameDay()` / `endgameOn(t)`
  (what readers ask), `endCalClosed(r)` (section 18 evCalPlan: no row after Day 35 once stayed), `endWorksNext(k)`
  (section 24 worksNext hook: "The Wren is home. Live in it."), the Works app's tab `home`, the first morning
  (`OCCASIONS.endFirstMorning`, SW6's script `endingFirstMorning`; notice, level 1 arrow to the mess, a row via
  `END_ITEMS`, which 29a's endItems reads).
- **The line condition** (section 22's lineCond, case `endgame`): `endgame` every hour for the endgame's first 14 days
  then about 4 hours in 10 (schedU k 798); `endgame:early` only the first 14 days; `endgame:false` / `!endgame` not
  stayed. lineFor adds 250 to an endgame line. content_gen.py, lines_check.py and content/README.md know the word.
- **E-1, the crossing back** (section 18): the data block after the comet's (`SHIP_EVENTS.crossingBack`, calendar row
  Day 31, phases Wed 31 08:00 / Sun 35 14:30 / 15:15 / 19:15, the oath meeting `crossingBackOath` 14:40 at the Line's
  venue, crowd k 365, ribbons, standing easy, the Line supper again, `EV_BEATS` crossingBack + endingOffer) and the slot
  'Ending builder' (`crossingBackTick`): Vance comes to find you Wednesday (crossingBackWord), the week's chatter,
  Saturday's ship and Saruth at the glass, Sunday's notices and arrow, Vance fetches you at 14:35 if you're not in the
  lounge (RV21's should), the oath, Saruth's signal, the address (.stay/.go/.ask/.plain) settled through 29a's
  `endSettle(now, answer)` and `end.cb.*`, the record at 15:15. Section 4d: the certificate's and plaque's second line.
  `crossingBackShip(t)` for VB2's sky ship (claude/vessel-sky calls it inside vesselSkyFrame, which needs EV_VESSEL_ON).
  `evLinesOf`: crossing-back bank lines keep only those whose `flag:` holds (the supper by end.stay / end.go).
- **Checks:** ending_check.py parts `endgame` and `crossing` (and the off part's EN2 half); bigevents_check: eventDay
  to Day 60 and a late save's due after the comet follows the plan.
- **29a fix (EN1's code, now mine to keep):** endTick does nothing before the offer's day (`d < W.offer`), so moving the
  clock back (events_check's storm parts, Dev mode) can't play the offer scene.

## Loose ends (in order; lead 40's list)
1. **arrows_check parts `endstay` and `endgo`** (spec section 7): from a Day 30 evening save, a player who only follows
   the arrow and the rings reaches every beat in order, answers Stay (or Go) at the first "Tell the Captain", leads the
   oath, ends in the endgame on Day 36 or at the end page; at every waking minute of a beat's window an arrow or ring
   names it; three ways each (as is, Teaching arrows Off, while tracking another job) + a change-of-mind run (Go, then
   Stay before Sunday's address, ends in the endgame). Look at arrows_check.py's `week` part for the follower loop.
   NOT STARTED.
2. **controller_check presets for the ending** (spec section 8): Dev presets on Days 32, 34, 35, 36; the pad reaches the
   offer's replies, "About the transfer" on chat cards, Stay/Go/Not sure, "Lead the oath", each farewell ring (A), the
   end page's buttons; a whole Monday Day 36 (Go) by pad. NOT STARTED. (EN1's ending_check `pad` part covers the end page.)
3. RV21's verdict on the latest sha (two shoulds done in turn 3).
4. Design doc: the spec's section 10 paragraph goes into design-doc.md in the commit that switches the ending on.
5. VB2's vessel-sky isn't merged here; when it is, check the ship shows Sat 10:00 - Sun 15:00 with EV_VESSEL_ON on.

## Gotchas
- Section 29 is at the end of the file (after 27); its `const`s are in TDZ while sections 18/22 load. E-1 reads them
  only through `cbEnd(() => ...)` at run time. 29c's readers (`endgameDay`, `endCalClosed`) are function declarations.
- `end.stay` must be a day number: SW6's crossingBackAddress.ask choices carry `flag:end.stay|go`; E-1 strips them
  (crossingBackAsk) or they'd overwrite the day with `true`.
- The `endgame` +250 boost: a bank endgame line beats someone's own everyday line; own endgame lines still win.
- events_check with the ending ON: known-old FX24-2 (Farouk Day 7) only, once the 29a guard is in.

## How to test
- Off: `python3 cadet_test.py OLD.html starship-cadet.html` must be ALL IDENTICAL; `bash check_fast.sh`.
- `python3 ending_check.py starship-cadet.html` (all parts, about 10 minutes; `endgame crossing` alone about 2).
- ON copy (`sed "s/^const EV_ENDING_ON = URL_FLAGS.has('ending');/const EV_ENDING_ON = true;/"`): bigevents_check,
  events_check BUILD 38, day_check BUILD 31 / 35 / 36 / 50.
- lines_check, names_check (`CADET_WORK=/tmp/cadet-work node names_check.js`), content_gen.py --check.

## Open questions for the user
None of mine. (The spec's three were answered: no way back from the end page; change your mind until the address;
the post worded by your answer to Calder.)
