# Handover: TB3, the traditions builder (0.99.5 playtest patch)

Role: build the fixes for the ship traditions that TR1 (the traditions reviewer, session_014zyJYMx26ZwoJgqt2dLUYL,
claude/p995-tr1, findings in plans/review-tr1-traditions.md) finds broken. Lead: lead 47 (session_014zyJYM4mt9ZDCD5H9JZDtN,
claude/lead-47). Reviewer: RV30 (session_014zyJYNFR7ewWJGvEQNUAHr; RV28 handed over). Send every commit and its game sha256
to RV30, TR1 and the lead. A second builder, TB4 (session_014zyJYN4DfKL615tM36enbP, claude/p995-trad926), does TR1's item 3
(the eight 0.92.6 traditions) in its own block right after t932Frame, with one line in t932Join and one in tradWalkEnd:
don't touch those.

## Branch and builds
- Branch: claude/p995-traditions, from claude/staging-0994 8976965e (0.99.4 candidate, game a01d1a4c...bc4a).
- Pushed: 88db900 (notes 19, 10, 8), game 5e4c65cc922153486746976187a586de059744c0e0457fd2f59a36fd1d478623.
- Then (see the last push for the sha): be03a8d item 5, 9cff5d3 item 8, 02bcfa1 item 4, 265448a item 2 (+ this note).
- Everything is behind one switch, `TRAD995_ON` (declared at ~9755, with the other switches; `false || URL_FLAGS.has('trad995')`,
  so `?trad995` previews). Off, the game is 0.99.4: cadet_test vs 8976965e ALL IDENTICAL on 88db900.

## What's built (each in the Traditions slot, section 18, in blocks headed "0.99.5 ... (TB3 ...)", above its end line)
1. Note 19, Spice shelf supper (the user: "doesn't trigger, no one to click on"): TRAD_JOIN entry (Brennan); spiceJoin (a free
   mess seat with your dinner: your tray, else foodFrom('servery')); spiceFrame995 (Brennan held at 3-spice-host from 18:05
   to 19:15, the hold re-applied after a deck change: deckCrewClear clears CREW_HELD, which was why she left the shelf after
   a tap; the script timed from her being there and you in the mess: SPICE995_AT; the card once the jars are named, the
   reveal waits up to 5 minutes for it); words (spiceFill: {spice} small mid-sentence, capital at a sentence start;
   spiceJarLine: "First"/"Last" lines in their place; no guess names its speaker); SHIP.spice { joined, asked } saved.
2. Note 10, Tea and biscuits: 5-tea-3 moved from the doorway [21,1] to [23,2]; the 13:00 tea takes seats only (section 14's
   take: `o.sit`, passed from the 'wtea' call).
3. Note 8, Name on the beam: 5-beam-1 at [14,0] under your name; the gathering stands from row 3 back (watchers moved,
   works-bay crowd spots in rows 0-2 skipped through a new `ev.skipSpots` read by eventPools); tradBeamFrame's cheers one at a
   time (2.6 s apart, 2.4 s bubbles, a cheer waits up to 3 s for any bubble before it), the crowd leaves after them.
   Backlog TB3-1: general crew chatter said at the same moment can still lift a cheer onto the name.
4. TR1 item 5: tradJoinMinute keeps every joinable tradition on the deck (TJ_ALL); TJ_NOW is the one whose rooms hold you;
   tjMarks995 draws the others' stars (.tjMark2); tradJoinTap knows their leaders.
5. TR1 item 8: tradJoin's own (`tj:`) acts: one notice ending "On till HH:MM; walk away to stop.", the act starts quietly
   (`o.quiet`, read in actBegin's toast).
6. TR1 item 4: TRAD_JOIN['off-the-tern'] (host Raman; on Day 21 Quinn Zamora leads, Raman isn't on the deck yet).
7. TR1 item 2: TRAD_JOIN for new-hands-tea, four-weeks-aboard, six-weeks-aboard, twelve-weeks-aboard, open-door; MS995 +
   ms995Card (called from eventJoin) for the new hand's tea, six and twelve weeks. The words are stand-ins for the writers
   (keys milestone.<id>.open/mid/reply.N/answer.N/close). Four weeks: no card (Calder's story scene and career question).

## Shared lines touched outside the slot (owners review)
tradJoin (the spice line; `mine`/`until` and the notice), tradJoinMinute and tradJoinTap and tradJoinFrame (TJ_ALL),
eventJoin (ms995Card), spiceFrame's first line, tradBeamFrame (cheers, TJ_FREE.at), eventPools (skipSpots), section 14's
take (o.sit) and its wtea call, section 15's actBegin toast (o.quiet). p926_check.py part 15 taps Brennan when switched on.

## Not done (open)
- TR1 item 7, hosts who don't come (Gym club Day 8, Sunrise stretch Days 8, 12, 15, Pick-your-own, Winner stays on): needs
  section 14's planner to send a free host to their own tradition. Not mine to change; proposed to the lead.
- The rec deck's hosted ones and the other hosted meals (TR1's design questions): lead to decide.
- Open door still has only the tea corner's places (TR1: 3 of 15 who mean to go fit).

## How to test (all on a copy with the switch on; the probes make their own)
- Setup: CADET_WORK with three r128 and acorn (plans/testing-guide.md section 2), CADET_CHROME=/opt/pw-browsers/chromium.
  Run long checks with a background time limit over 30 minutes (two of mine were stopped at 30).
- plans/tb3-probes/: spice995.py BUILD [days] (2 9 16 + a reload), beam_tea995.py BUILD OUT [8] [10], twotrads995.py,
  toast995.py, tern995.py, milestones995.py. Each prints "... OK" or FAILED.
- Also run on the switched-on copy: join_check, events_check 28, bigevents_check, deck_check, day_check 2/3/5,
  food_check 1 7, p926_check 15; and cadet_test 8976965e vs the build (switch off), check_fast before every push.
- Gotchas: a probe that execs cadet_test.py must not define its own HOOK (it replaces the harness's); `pkill -f` with a
  file name kills your own shell too; one browser per lane, two lanes at most.
