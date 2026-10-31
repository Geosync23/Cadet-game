# RV30 reviews (0.99.5 playtest patch)

RV30 session_014zyJYNFR7ewWJGvEQNUAHr, branch claude/review-rv30. Lead 47 (session_014zyJYM4mt9ZDCD5H9JZDtN). Base for every review:
claude/staging-0994 8976965e (game a01d1a4c...bc4a). Probes in plans/rv30-probes/.

## SD5 sound, claude/p995-sound d26a11a (game d785aea6...30ff, verified): FIXES NEEDED (small)

Notes 9 (suspend on hide, no switch), 4 (MESS_SCALE, off), 17 (SND_LONG, off in branch).

Passing:
- sha256 matches. Diff read: every MESS_SCALE / SND_LONG line is behind its switch; hideNow is the only unswitched change.
- cadet_test vs 8976965e, alone: ALL IDENTICAL. names_check OK. sound_check (SD5's own, whole): SOUND CHECK OK.
- Note 9, real game loop (hide_loop.py; this container's browsers never really hide a tab, tried another tab, a
  minimised window under Xvfb and a CDP freeze, so the hide is played and no frame is drawn after it): 0.99.4 keeps playing
  ("running") for all three of visibilitychange, pagehide, freeze; SD5 suspends at once for all three; back, the sound
  follows the pause (paused: stays off till Resume; pagehide/freeze: plays on).
- Note 4, MESS_SCALE on (mess_day.py, real crew Day 2, 12 times): empty and 2 people (you + one): no scene; 11 people
  level 0.52, 15: 0.66, 21: 0.86, 40-49: 1; emptied: gain to 0 then the scene goes. As designed.
- Note 17, SND_LONG (stall_real.py, real loop, mess at the rush with music, 6 stalls of 1.2 s): off: 42 late starts (worst
  1.50 s), 1604 gain moves in the past; on: 0 and 0. Music and mess still playing.

Fixes:
1. Note 9 race (hide_loop.py "race 2"): if the page hides while ctx.resume() is still in flight (Resume tapped, any tap's
   gesture() resume, then away at once), hideNow sees state 'suspended' and returns; the resume then finishes and the sound
   plays on hidden with no frames to stop it. Probe: "hidden while the resume was in flight: sound running, paused True".
   Fix: in hideNow suspend whenever ctx exists and isn't 'closed' (drop the 'running' test). Tested in this Chromium: resume()
   then suspend() at once ends 'suspended'.
2. SND_LONG music lookahead 2 s (music_x.py): at a hand-over the old track's notes already queued play on under the fade:
   now up to 2.1 s after the fade starts (0.7 s with it off). That changes the Music app's skip/off (2 s fade), every
   time-of-day / event cross-fade (pendingChange at a section end: bars past the change point are queued 2 s deep, not
   0.5) and after a sleep jump. design-doc says "It doesn't change how anything sounds". Fix suggested: never queue past a
   pending change point (tick to min(now + 2, change.at + 0.45) while a change is pending), so section-end hand-overs are
   as 0.99.4; or the lead accepts it and the design-doc line is corrected.
3. sound_check check_long can't fail on the bug: its own off run prints late starts [0, 0, 0, 0] too, so a build where
   SND_LONG did nothing would pass. Count gain moves in the past as well (stall_real.py: off 1604, on 0) and require the off
   run to show some when the build has it off.

### Re-review: PASS claude/p995-sound ec312a9 (game ff19f794116a7a7ab2eebf00f39e404bea8781ed94d6f98a756449a8dbc0a8ad)
Fixes 1-3 in, plus SND_BUF_ON (off, latencyHint 'playback'). sound_check hide|long|buf|mess_scale OK (long off [37, 27, 84,
42], on [0, 0, 0, 0]; buf latency 0.042 -> 0.095 s; hide while resuming: suspended); hide_loop race 2: suspended; stall_real
on 0/0; names OK; cadet_test vs 8976965e ALL IDENTICAL. Not blocking: a time-of-day change within ~2 s of a section end
can still let up to 2 s of already-queued bars run past it. Sent to SD5, lead, BM22.

## OB2 onboarding + appointments, claude/p995-onboarding 82e9cc5 (game 842b5ff5...0688): FIXES NEEDED (early, sent)

Passing so far: cadet_test vs 8976965e alone ALL IDENTICAL; names_check OK; lines_check PASS; tip words (note 1) have no
weekday; health arrow on from 13:59; a tap on Rina in the infirmary plays introHealth (health_tap.py).

1. Note 16 blocker: the clock runs during the scene (~0.6 ship min / real s). health_tap.py WT BUILD 18 3: tap 14:18, ~3 s a
   card, scene 14:19-14:32; 14:30 apptTick marks it missed, introHealthMissed rebooks Day 3 14:00; scene end sets met but
   can't keep it. Day 2 missed, Settling-in not ticked, Day 3 booking can never be kept (introHealthDue refuses once met).
2. Note 11: accepted tradition invitations (socialInvite { trad }) read "Invitation with Captain Odile Marrow" in Coming up;
   the Calendar shows "06:30 Sunrise stretch" and "06:30 Invitation with Captain Odile Marrow · booked" (appt_views.py).
Checks on 82e9cc5 (later): intro_check whole OK, appt_check OK, device_check OK.
Note 7: a skipped game stays on the arrival evening's steps (zeke_end.py is not a fair state; kept for the record).

## TB3 traditions, claude/p995-traditions 88db900 (game 5e4c65cc...8623): FIXES NEEDED (one)

Passing: switch off: cadet_test vs 8976965e alone ALL IDENTICAL (code read: o.sit false, skipSpots / TRAD_JOIN / places /
SAVE_EXTRA only when on). Switch-on copy: events_check (28) OK; p926_check OK (taps the supper); TB3's beam_tea995.py OK
(you paint at x -7.02 under the name at -7.02, no bubble over the name painting or cheering; 13:00 tea 30 seated
minute-people, nobody at 5-tea-3 or on the doorway, a way out every minute); screenshots look right.

1. Note 19: the reveal waits only 5 ship minutes for your guess card, but the clock runs during the card (~8 real s for 5 ship
   min). spice_paced.py (TB3's probe, the card read at ~3.3 s a card): card open 18:32-18:38, Brennan's first reveal ("Dr.
   Nandakumar's jar, loves. The dried chilli.") at 18:37, while the card is still open; a slower reader sees the answer
   before picking. Fix: hold the reveal while the card is open, with the cap in real seconds (e.g. 60 s), not ship minutes.
   (The same run has 13 bubbles, under TB3's 15: fewer guesses while the card is open; adjust the check, not a bug.)

### OB2 re-review 6c926f4 (game 572e9c6d...8cb4): fixes 1, 2 work; one more (sent)
health_tap 18/3: kept, no rebook. appt_views: "Sunrise stretch, with Captain Odile Marrow"; Calendar folds it into the
tradition row. New: health_tap 28/6: the scene runs 14:28-14:56; Rina walks off at 14:38 (her place ends 14:30), 20 m away in
the Washrooms while her lines play. Fix: crewHold('rina', null) for the scene, released in its onEnd (as storyHolds).
Checks on 6c926f4: appt_check OK, device_check OK (intro_check running).
Not blocking: Vance's 19:32 First Light Cocoa invite not folded into the 20:00 row (different minute).

### TB3 final 872fec0 (game fbf74a320ebf8d4a9c02f26db31ab209b7e0314287e515c0e9fe25d58c8a9420): still FIXES NEEDED (fix 1)
Adds TR1 items 5 (TJ_ALL, stars), 8 (one notice), 4 (Off the Tern), 2 (milestones + MS995 stand-in words); seats-only tea
dropped. cadet_test vs 8976965e alone ALL IDENTICAL (switch off). TB3's twotrads995, toast995, tern995, milestones995 OK.
Spice code unchanged: fix 1 stands (sent to TB3 and lead; TB3 is handing over).
TB3 872fec0 switch-on: stories_check 36 OK (incl. Tomas 8 across its booking's end).

### SD5 a5ce274 (game 79f0142196007b2fd091bb5d1b1f5f2a5d1cb51e092136212c2f9367743bd86c): PASS (supersedes ec312a9)
Only change: music lookahead back to cur.tick(now + 0.5) (0.99.4's line; lead 47). sound_check hide|long|music OK (long off
[70, 70, 110, 84], on [0, 0, 0, 0]); stall_real off 40 / 1695, on 0 / 0. Sent to lead and BM22.

### TB3 4037a26 (game 135a79af09ad5c23aedfddbb2df13cbc5c0c92dab48e1334cfd890f2bcef519b): PASS
Fix 1: the reveal waits while the card is open (60 real s cap) and 2.5 s after. spice_paced.py Day 2: pace 5: card
18:32-18:38, reveals 18:43/45/47; pace 9: card 18:32-18:43, reveals 18:48/50/52; OK. Only spiceFrame995 changed (switch-on
code). names OK. Sent to TB3, lead, BM22.
TR1 re-probe of 4037a26: PASS; edge (card left open 40-60 s near 18:40 loses the reveals past 19:15): sent to the lead for TB5's follow-up (cap the wait by ship time too, ~e.to - 8). Not blocking.

### OB2 fb81b79 (game 7e66e20d746f0c539bd84a0429dbf17231adfd8dfae2559c7d0b272bb8d7d2dc): PASS
crewHold('rina', null) for the scene, released in onEnd (and if dialogueShow fails). health_tap 28/6: Rina in the infirmary
1 m away to 14:56 (scene end), kept, no rebook, no errors. intro_check whole OK on 6c926f4 (and 82e9cc5); names OK.
Sent to OB2, lead, BM22. Queue: TB5's follow-up (TR1's spice edge) when it comes.

### SW4 words, claude/p995-traditions-words 181d86a (game 62d3602b6fc35e3d58ad78b17424e3e22519a4374a9665e9e7effb4b0ce32d3c): PASS
4037a26 + content/banks/milestones-995.lines baked (LINES only). names OK, lines PASS, milestones995 (switch on) OK with the
new lines on the cards. Word note (not blocking): the new hand's tea close mentions Halloran's mug, already handed over at 13:00.
check_fast on 181d86a: QUICK CHECK OK (329 s).

### SW4 fac5e56 (game 0b047d75acc513507cb4d044db441aa13fa8df09e35997e7cb48be4b9f25ed1c): PASS
Three tradition Mails reworded (Talent night, Tap night, Midtour; the user's "change the Mail to match"); only text.mail[0].t
changed in each row. lines PASS, names OK, check_fast OK (326 s); trad_mail.py shows the three as sent (Days 5, 152, 182).

### SW4 52ea327 (game b815c01de8b8712bcc7f18fddc8b887061d9dcd178fab7e5ec4e152d1b216bd0): PASS
New hand's tea close (mug on the rack), Tap night ask, Midtour invite line; only those fields changed. lines, names, check_fast (317 s), milestones995 OK.

### TB5 b7af35a (game 6a8cae19b186c451779bbe0d9e909f97c9f66dbe3f7d1bc3d7902e084bcea504): PASS
On 4037a26: wait capped at e.to - 8; no guesses once the reveal is due; seat toast names the supper's end (all TRAD995_ON).
spice995_paced (TB5) never/hold 90 s: reveals 19:07-19:11; reload OK. spice_paced pace 5: none while open. names OK.
Test merge with 52ea327: clean, file 37d8c3aa98dc801bd9eed2c2f18cfebd89ac4b698c106fe7d8e35ef0a62a6a25. Sent to TB5, lead, BM23.
Queue empty.

### BM23 sound_check r3mess edit (0.99.5 candidate, MESS_SCALE on by the user's pick): PASS with a change
3 am: expect the scene only when M.at(n).voices > 0 (not n == 0: you + one crew also gives none); at(0) compare without level, level == 0. Off: unchanged.
BM23 96d902e: the edit as agreed, PASS (check-only). Sent to BM23 and lead.
