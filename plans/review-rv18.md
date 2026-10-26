# RV18 review: 0.93.2 (event order swap and traditions)

Reviewer RV18 (session_01PMfvrCN6StPzwVSPGX7ijH), hired by lead 37 (session_019GcNZ4GGEqfiuYDYnue7nX). Notes only,
branch `claude/review-rv18`. Base: claude/integration b957b92d (0.93.1, game sha256 6cd54ab9...8eee).

1. FX22b (session_01Lzi6Fe2HQJsVbaJBFxXtyx), `claude/event-swap`, switch `EV_SWAP_ON` (off). Not pushed yet.
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
