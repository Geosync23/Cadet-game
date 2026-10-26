# RV18 review: 0.93.2 (event order swap and traditions)

Reviewer RV18 (session_01PMfvrCN6StPzwVSPGX7ijH), hired by lead 37 (session_019GcNZ4GGEqfiuYDYnue7nX); lead 38
(session_01G2y9crUv6vDiiEB2q6Yo9W) from 04:40. Every PASS goes to lead 38 and BM18 (session_01A3S2VBMYmTt2wCZa8ej7XR) with the exact sha. Notes only,
branch `claude/review-rv18`. Base: claude/integration b957b92d (0.93.1, game sha256 6cd54ab9...8eee).

1. FX22b (session_01Lzi6Fe2HQJsVbaJBFxXtyx), `claude/event-swap`, switch `EV_SWAP_ON` (off; the URL flag ?evswap).
2. FX24 (session_017zuWxNJfppnVwkQDtiwnb6), `claude/trad-0932`, switch `TRAD_0932_ON` (off).

The user's rule for every tradition: "a host you click to join, then a simple pose or animation to reflect the event,
and unique dialogue."

## FX24, step 1: 0524738d (game sha256 e02ef0e0...9c8f), and step 2: 149fed5b (4197bbf4...3e39)

Diff read: section 13's switch and tables, section 18's loader lines and evDue's `any`, the Traditions slot (TRAD_JOIN
entries, t932Join, t932Say/t932Frame, tastJoin, tasteName), tradJoin and eventsTick (one line each), section 16's
galleyTasteCut and GALLEY_AT.taste, galleyTasting's label, devmodeWhen, evTagId/eventTags 'fold'. Everything is behind
TRAD_0932_ON except step 2's galleyTwin (M4). Nothing new calls R() at load (TRAD_JOIN entries and tjActs only).

### Checks
| Check | Build | Result |
|---|---|---|
| cadet_test vs b957b92d, alone | 0524738d off | ALL IDENTICAL |
| check_fast | b957b92d (setup) | QUICK CHECK OK |
| names_check | 0524738d on | OK |
| content_gen --check, lines_check | 0524738d | up to date; PASS (0 errors, 69 warnings; base 66) |
| day_check 3, 8, 20, 27 | 0524738d on | DAY CHECK OK, all four |
| weekend_check | 0524738d on | WEEKEND CHECK OK |
| events_check | 0524738d on | FAIL: reading-corner Day 7 not reached (farouk-olu) (S7) |
| events_check | b957b92d | EVENTS CHECK OK (it doesn't walk reading-corner: its rhythm isn't "new" there) |
| join_check | 0524738d on | FAIL on every new one (M2); then a page load timeout (3 browsers) |
| food_check 1 7 | 0524738d on | FAIL: 4n tasting with the tally, Sunday's side (M3) |

### Played at phone size (390 x 844), switch on
Each: from its start + 4 min, the player in its room, a screen tap on the host (two by tradJoinTap where my tap missed:
Row for the board, host on a machine; Playlist duel, host off screen), the card, the activity, its bubbles, the end.
| Tradition | Day | Host card | Your pose (place) | Bubbles | Close line |
|---|---|---|---|---|---|
| Scone morning | 70 | Emeka | drink, standing (tea corner full) | own lines | yes |
| Tasting table | 3 | Brennan (greeting) | sit:drink, 3-mess-41 (mess hall) | own lines | yes |
| Five-minute skills | 8 | Bilal | sit:fold, lounge | own lines | yes |
| Jar day | 20 | Tariq | cook, cook-along spot | own lines | yes |
| Coffee trials | 27 | Maeve | sit:drink, lounge | own lines | yes |
| Seed packet day | 27 | Ravi | fold, garden | own lines | yes |
| Midnight toast | 26 | Greta | sit:drink, mess | own lines | yes |
| Beginners' guitar | 23 | Hamid | play, music room | own lines | yes |
| Whodunnit club | 38 | Lars | sit:read, lounge | own lines | yes |
| Windowsill herbs | 36 | Hugo | water, garden | own lines | yes |
| Sounds from home | 46 | Uma | sit, music room | own lines | yes |
| Row for the board | 51 | Isak | run, 3-gym-15 (a treadmill) | own lines | yes |
| Playlist duel | 57 | Imani | talk, music room | own lines | yes |
| Lamplight paddle (rec.on) | 69 | Bea | a kayak | own lines | yes |
| Ring the bell (rec.on) | 77 | Carmen | the wall (12 min) | own lines | yes |
All 15 meet the user's rule in shape. But see M1: the card closes by itself.

### Findings (priority "next")
**Must**
- M1. The join card closes by itself at the next ship minute (about 1 s): t932Join's and tastJoin's dialogueShow pass no
  `where`, so meetingsTick's `inMeeting(DIALOGUE.m)` is false and calls dialogueClose(). Every join sends a "<name>
  (notes)" Mail (meetingGist); the tasting table never reaches the vote (onPick never runs, no token). Fix: `...cardWhere(e)`
  as the p926 cards, and no gist.
- M2. join_check fails with it on (the card, and rec.on for rec-*). The check must step through the card.
- M3. food_check 1 7 fails with it on: 4n compares labels with key.replace('-', ' '); labels are now tasteName's.
- M4. Step 2's galleyTwin (section 14, schedBuild) is not behind the switch: it changes galley hands' plans with
  everything off. Outside the brief; needs a gate, or lead 37's OK plus the section 14 owner's review and the full round.

**Should**
- S1. Each talker repeats one `here` line all event (tradText: per person and day): Greta's line 5 times in 30 min, Bea's
  6, Isak's 7; Carmen's "Ding!" before anyone climbed. Rotate by R.n.
- S2. Tasting `here` "Go on, love. Tell me the truth." is Brennan's voice, said by Oduya, Ibarra, Salo.
- S3. The tasting table seats you in the mess hall, not the galley (the user's "in the galley").
- S4. Row for the board uses treadmills ('run'); the gym has rowers (anim 'row').
- S5. Rec ones join before recStart: with the wall or kayaks shut you're joined with nothing to do.
- S6. The two build-number lines are the build master's.
- S7. events_check with it on fails on reading-corner Day 7 (backlog FX24-2, section 14's walking time): the switch makes
  the check walk it. Not FX24's code; blocks the switch-on until fixed or accepted (lead's call).

**Verdict on 0524738d: FIXES NEEDED (M1-M4).** Sent to FX24 and lead 37.

### Lead calls (lead 37, then lead 38)
- M4: lead 37 approved the galley fix outside the switch; FX24 then put it behind TRAD_0932_ON; lead 38: keep it there
  (the switch is on in 0.93.2). Proof it's right: 0.93.1 fails day_check 32 (`double: 3-galley-5 walsh-esme/madsen-ivo@16:30`);
  149fed5b (ungated) passes day_check 32, food 1 7 and events_check off, and cadet_test is ALL IDENTICAL. On paper over Days
  1-60 only Esme's last 2 minutes on Day 32 change (16:30-16:32 at 3-galley-5 become off), and that was the only galley
  double booking in those 60 days.
- S7 (reading corner Day 7, FX24-2): accepted as known-old for 0.93.2 (lead 37).
- Tray-seat outside a switch: accepted (lead 38; the user asked for it).

## FX22b, the event swap
Step 1 56fa0ca5 (9387754f...222a), step 2 49cf5dc5 (0d0fb87c...68b6), step 3 4e13d5e3 (eb999383...b853), step 4 05a9e7db
(e8768136...d7be). Diff read: section 13's switch (a URL flag), one `if (EV_SWAP_ON)` block in section 18 (calendar, order,
EV_BEATS, the visit reshaped, the comet's draft, the address Mail), the tea not loaded with it on, friCond's `swap`,
eventGuestDays' guestStay; step 2 Basil's beat 4 as a welcome dinner (outside the switch: lead 37's call) and the comet on
Monday Day 22; steps 3-4 the address lines and fridays_check's swap excuse. Nothing calls R() at load.

| Check | Build | Result |
|---|---|---|
| friSpeech Days 12, 19, 26, EV_CALENDAR, eventsOn 16-26 | 56fa0ca5 off vs b957b92d | identical, word for word |
| the same with the swap on | 56fa0ca5 on | Day 19 "this morning we saw our Veyli guests off"; Day 26 the comet lines; calendar storm 11, visit 16, comet 26 |
| cadet_test vs b957b92d, alone | 49cf5dc5 off | ALL IDENTICAL |
| names_check off and on, content_gen --check, lines_check | 49cf5dc5 | OK, up to date, PASS (0 errors, 66 warnings) |
| fridays_check (CR6) | 56fa0ca5 off / on | one FAIL each: the never-fill excuse missing for swap lines (fixed in 4e13d5e3) |
| fridays_check (CR6) | 4e13d5e3 off / on | OK / FAIL: Day 26 swap line 91 characters, over friFill's 90 (fixed in 05a9e7db) |

## FX24, Take a seat (claude/tray-seat-0932 44ba88d5, game 47b0e1d0...0074)
Diff read (section 15: seatBtnSeat, seatBtnGo, the button, one handTick line). Played at 390 x 844: with a tray in the mess
hall by a free seat the button shows straight above Put down at its size; a real tap sat me at 3-mess-8 and I ate the tray
(ACT eat, fed); the button goes; none on Deck 4 with a tray. No page errors.

## Event swap verdict: PASS at 05a9e7db (game e8768136...d7be), 05:10 UTC
| Check | Build | Result |
|---|---|---|
| cadet_test vs b957b92d (alone) | 05a9e7db off | ALL IDENTICAL |
| events, bigevents, stories, arc, day_check 25 | 49cf5dc5 off | all OK |
| events, bigevents, day_check 16, 19, 22 | 49cf5dc5 on (copy) | all OK |
| fridays_check (CR6) | 05a9e7db off and on | FRIDAYS CHECK OK, both |
| fridays_check (mine) | 05a9e7db | hangs in my container (timeout 2400 s, no output), as FX22b saw even on 0.93.1; CR6's runs count |
Small, no fix needed: the build-number lines (BM18's); Day 26's "a week of guests" for a three-day visit (SW2's).

## FX24 traditions, re-review of the fixes (c7867204, 4d38df29, c536ed00; then 4d1eca54, game ad6fc781...a31a)
| Check | Build | Result |
|---|---|---|
| cadet_test vs b957b92d | 4d1eca54 off | ALL IDENTICAL (1-level noise; another browser was running) |
| food_check 1 7 | 4d1eca54 on | FOOD CHECK OK (M3 fixed) |
| events_check | 4d1eca54 on | only reading-corner Day 7 (FX24-2, accepted as known-old by lead 37) |
| join_check | 4d1eca54 on | all 15 new ones "tap -> joined True" with an activity, no FAIL; then a page-load timeout under load (rerun alone queued) |
Played again at phone size (switch on): the card stays open (3 s and more), every line plays, the tasting vote goes in
("You drop your token in the jar for the ..."), no "(notes)" Mail (M1 fixed); you stand in the galley beside Brennan
(S3); bubbles rotate through the lines, no one line over and over (S1); Brennan's "love" line only from her (S2); Isak
rows on a rower (S4). Left, small: at Row for the board I got a weight bench (lie:lift) because the rowers were booked
by the crew coming: the pose doesn't match the event. Suggest standing by the rowers and cheering when they're full.

## SD1 steps-quiet (claude/steps-quiet 0d41441f, game 1260dfe1...fd79c)
One line: TRIM.steps 1.0 -> 0.5. Only the player's footsteps use the steps bus (S.fx 'step' with layer 'steps', and the
unused startWalk). cadet_test and sound_check queued.

## FX24 auto doors (claude/auto-doors-0932 61893eae, game 76224623...ef16)
Diff read: 15b's slot (AUTO_DOORS_ON on, setting default on), section 4's collide (adoorShut for the player only), the
door-leaf walk test, Walker.goTo (adoorRoute for the player), the tap and cursor, Settings, deviceLoad keeps it only when
off. With the setting on nothing changes. Played at 390 x 844, 03:00, public doors on Decks 2, 5, 3, setting off:
steering into a shut door stops you and it stays shut; a real tap on the door opens it and you walk through; a real tap
in the room beyond walks you through and the door opens as you reach it; setting on: straight through. No page errors.
Should: a door on a near wall is drawn cut away, a low strip your own character mostly covers when you stand at it, so a
tap there hits you (walker) and you walk off instead; suggest a tap on yourself (or the doorway floor) next to a shut door
counts as a tap on that door. A tap beyond works, so not a must. cadet_test and interactions_check queued.

## Verdicts so far (each sent to lead 38 and BM18 with its sha)
| Branch | Verdict | Sha (game sha256) |
|---|---|---|
| claude/event-swap | PASS | 05a9e7db (e8768136...d7be) |
| claude/trad-0932 | PASS | d126a657 (426a79f9...170d) |
| claude/steps-quiet | PASS | 0d41441f (1260dfe1...d79c) |
| claude/auto-doors-0932 | PASS | 98768969 (8f3c0461...a5) |
| claude/tray-seat-0932 | PASS | 5892511c (47b0e1d0...0074) |
| claude/comet (includes sound-comet and event-swap) | PASS (c.2 was FIXES NEEDED: C1) | 157d1cfb (740a63a2...ac50) |
| claude/storm-sat | handed to RV19 (lead 38) after my first look | 41d891b9 then 67e918f2 |
| claude/inspection | PASS (the fix for BM18's FAIL; taken from RV19) | e45b7fe (64c9e6b4...bc0e) |

## trad-0932 final checks (d126a657)
join_check alone with it on: JOIN CHECK OK. interactions_check alone with it on: OK. Row for the board: with the rowers
booked you stand by Isak and shout the numbers (talk), never the weights.

## The comet (FX25, claude/comet), c.2 db72b2a1 (b26d7970...bb6c) played at 390 x 844
Sato's marker/arrow/tip from 21:30; tap Sato joins the bow glass (talk); Sato's naming card at 21:51, the pick kept; the
arrow to Saruth at 22:01, his three knot lines; Mori's scope (ixStars) and lines; Tomas's blankets (sit:talk) and lines; a
Cadet tapping the Captain gets Vance's "best seat's downstairs" and the arrow to the lounge. C1 (must): the lounge's 7
lines all skipped (cometTalk needed `settled`; Sato and Saruth at the Line's lead spots never settled). C2 everyday
chatter in the rooms; C3 catch-up then silence; C4 Record empty (it was still running at Day 23 10:00: FX25's answer).
c.3 d7e19d3 (look) also gated the look-up poses on `settled`. All four fixed in c.4 (FX25's note); re-test queued.
The comet's sound (SD1, sound-comet b6569d19, in claude/sound-comet-c ff8f141d and merged into c.4): a cometTurn swell
and a Comet track; 'Event' isn't in the Music app's TIMES, so the track isn't listed; it plays only while cometMusicOn().

## Storm Saturday (FX26, claude/storm-sat)
7091043 / ea0ace07 played: the stage fix (before: the Captain sunk into the stage at the lectern; after: standing on it,
the bubble above her head); Day 13: Calder's Mail Friday 18:00, on duty, Schedule "On shift: called in for storm repairs"
09:00-17:00, the board only storm repairs in three waves, all 18 Works day crew working. Storm stories by torchlight (Day
13 21:05): a tap on Oduya joins (toast with his line, sit:talk) but S1 the room is full so you stand in the Junior
corridor outside its wall; S2 no storm-story bubbles, only everyday chatter (14 `here` lines and Oduya's close lines
unused); S3 (torchlight look) done in 41d891b9 (torches, room dimmed).

## Process notes for my successor
- Never more than 2 browser checks at once on 4 cores: interactions_check timed out (2400-3000 s) twice with 4-5
  browsers. Chain queues with `pgrep -f "bash /tmp/rv18/queue[N]"` waits; never edit a running queue script (bash keeps
  reading the old file); kill with a bracket pattern so it doesn't match your own shell.
- fridays_check hangs in this container (no output, even on 0.93.1); CR6 runs it.
- Probes (not in the repo): /tmp/rv18/probe/play.py (traditions: tap the host at phone size, card, activity, bubbles,
  close line; args ID:DAY ...; REC=1 sets rec.on), comet.py, doors.py, seat.py, stormsat.py, stage.py, speech.py.

## The comet, final (c.4 fda75fb2 tested; c.5 157d1cfb = c.4 + SW2's words + the look-up gate)
| Check | Build | Result |
|---|---|---|
| cadet_test vs b957b92d alone | c.4 and c.5, as shipped (comet on) and EV_COMET_ON false | ALL IDENTICAL, all four |
| events, bigevents, day_check 22, sound_check | c.4 | OK |
| join_check | c.4 | the four comet joins pass; then a reload page-load timeout under load (CR6 passed it whole on c.2) |
| fridays_check (CR6) | c.4 and c.5, on and off | OK |
| content_gen --check, names_check, lines_check | c.5 | OK, OK, PASS (0 errors) |
Played in real time (no clock jumps): tap Sato 21:31; her lines every ~5 min with Holt and Farouk between (C1 fixed); the
naming card at 21:50, pick kept; Saruth's knot; scope, blankets, a Cadet turned away from the Captain's tea. Shoulds left
for the next comet builder: the bedtime arrow ("Your bunk, Deck 4") holds the goal at 22:02, so the arrow to Saruth never
shows (setGoal only replaces an empty or tradition goal); with one speaker present a room repeats that one line every 4 min.
Note: my early comet probes jumped the clock with setShipNow; the crew only walk while frames run, so hosts looked absent.
Play in real time (comet_real.py) before calling a host missing.

## Take a seat: PASS at 5892511c. interactions_check alone OK (its Take a seat part all true).

## The bunk inspection fix (FX20b, claude/inspection e45b7fe, game 64c9e6b4...bc0e): PASS
Taken from RV19 (lead 38) so RV19 could stay on storm-sat. BM18's FAIL with INSPECT_ON on.
| Check | Build | Result |
|---|---|---|
| events_check | 9b7eae69, INSPECT_ON on | FAIL as BM18 said: rec-dawn-swim without Rina Days 4-39, madsen-ivo short Day 25, the cake second slice |
| events_check | 9b7eae69, INSPECT_ON off | OK |
| cadet_test vs b957b92d alone | e45b7fe off | ALL IDENTICAL |
| events_check | e45b7fe on | EVENTS CHECK OK |
| day_check 4, 11, 18, 25 | e45b7fe on | all OK |
| RV19's live walker probe | e45b7fe on, Days 4 and 11 | all 8 rooms in route order a e b g c h f d (06:10-07:11), your result in person, the done toast |

## The inspection guard for 0.93.3 (claude/inspection 1872153, game b21e0a55...dbb3): PASS
Lead 38 moved it out of 0.93.2 (0.93.2 takes e45b7fe). Seven planner lines in section 14 gain `d >= 1` (the walker's
early bed: `d >= 0`), all behind INSPECT_ON. cadet_test off ALL IDENTICAL; with it on: events_check OK, day_check 4 OK,
machine_check OK.

## Inspection i.9 (claude/inspection 5793626, game f9ba5c6b...beb3): PASS
1872153 plus three lines in inspectWalkDo: when the officer gives your result in person, a player lying in their bunk
(ACT kind 'lie'; sleeping is a different path) gets up first (CR1's arrows_check week FAIL: the follower lay down at the
berth's arrow at 06:29 and stayed there all day). cadet_test off ALL IDENTICAL; with INSPECT_ON on: arrows_check week OK,
events_check OK.
