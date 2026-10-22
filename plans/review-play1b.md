# Review: playtest patch 1, branches G, H, I (RV4)

Reviewer RV4 (session_01GpAWYxQbS4y8rcB5LWDVE7), for lead 26. All three branches start from `claude/integration`
32b699a6 (0.64.14, game sha256 94f32868...881e9). Base check_fast in this container: OK (239 s).

For each branch: is the note really fixed (driven in the browser), did anything else change (every cadet_test
difference explained), were the checks run and OK, and is the design doc updated.

## H: every ladder room can be entered (note 15; LR1, claude/patch-play1-h)

**Tip reviewed: d0f96def** (game sha256 0ad2fe98...b8a7; tested at 002e41e3, and d0f96def only adds screenshots,
the build-table results and DEV_NOTES: the game file is the same). **Verdict: PASS.**

What it does: on all seven decks the ladder room (room Z beside the lift) gets a sliding door where its hatch was;
the ladder's hole becomes a narrow well with the cage starting above head height, so you stand beside the ladder;
the tile on the far side of the well is blocked. Deck 4's harness rack moves out of the doorway. A small table of
door and standing tile per deck (`LADDER_ROOMS`, `ladderStand()`) in the deck architect's slot; section 15's
`ladderHatch()` falls back to the ladder room's door.

Driven in the browser (390 x 844, every deck): from the lift lobby, tapping the ladder walks you into the ladder room
and the Spine ladder panel opens; climbing to the next deck lands you inside that deck's ladder room on a free tile;
seven climbs in a chain (1 to 2, 2 to 1, 3 to 2, 4 to 3, R to 4, 5 to R, 6 to 5), no errors. Every room Z tile but
the blocked one is reachable. Close-up shots of all seven rooms, old and new, from both sides: door in place,
player stands beside the ladder, nothing clipping or flickering.

Rules for a map change:
- **Coplanar surfaces:** the new well and its hazard stripes keep the old kit's pattern (the stripes 0.0065 above
  the well's top; touching faces only back to back). OK.
- **col() and R():** no new colours outside the existing `std()` and `WM` materials; nothing new calls `R()`
  (data and kit geometry only). OK.
- **Draw calls:** +1 per deck by the lift (door instead of hatch), e.g. Deck 4 176 to 177, Deck 3 209 to 210.
  day_check's peaks are far under the 450 budget (highest 251, Deck 4). OK.
- **Checks:** check_fast OK (334 s; deck_check: room Z no longer listed as "nobody can get into" on any deck),
  path_check OK (3000/3000 on every deck, 3102/3102 real calls), day_check (Day 1) OK, tiles_check OK.
- **cadet_test vs base:** screenshots all identical (0 pixels). Differences, all on Deck 4's ladder room and
  explained by note 15: edges/doors (h,20,14 hatch to door), blocked (+21,11), roomTiles (room Z loses 21,11),
  closed (the Spine ladder text gone), and 9 of 3000 collision probes, every one starting inside room Z or on its
  wall (checked probe by probe; three that start inside the newly blocked tile are pushed out north across the wall,
  as any blocked tile against a wall does).
- **Design doc:** "The spine" updated in the same commit.

Notes for the build master and owners:
- Edits outside LR1's listed sections: two lines in section 15 (`ladderHatch()`, Deck 5's LADDER.d5 door) and
  section 4e's rec deck ladder room. Small, but per the owners rule the section 15 and 4e owners should see them.
- **Order of merging with E (LD1, ladder taps):** E calls H's `ladderStand()` behind `typeof ladderStand ===
  'function'`, so merging E first (the plan's order) is safe. A test merge of integration + E + H + G + I: the game
  file merges with no conflict (only plans/build-table.md, where every branch appends a row; keep all rows), names_check
  OK, and the ladder drive on the merged build passes on all seven decks (with E you now walk to the spot beside the
  ladder, and land there).
- tiles_check is sensitive to load in this container: it failed twice on H (and would on any build) with a click
  timeout on "Quick game (to 5)" while other checks ran beside it, and passed on H and on the base when run alone.
  Not H's fault; worth telling the runners.

## G: more jobs on the board (note 13; JB1, claude/patch-play1-g)

**Tip reviewed: 3ffb604f** (game sha256 0ef144c3...e159). **Verdict: PASS.**

What it does: each hour of your shift (45 minutes or more left), if fewer than 2 jobs you may take are on the board,
small no-part chores at your tier are posted (vent, calibrate, delivery, small fault; seals first for an officer),
held for you to the end of the shift and gone after it, so the crew's own work is unchanged; no Works reputation
(`xp: 0`, the existing "paid elsewhere" route). 3ffb604f adds: none while a job kept for you that day (Day 1's two with
Zeke, a training job) is due within the hour or untaken (the lead's ask).

Driven in the browser (390 x 844, the first tip 1b3e18f1): a quick player on Day 1, taking the top job and finishing it
in its minutes + 20, checked every 15 minutes when idle:
- base: 8 jobs; the board was empty at 12 of 20 checks (13:00-16:55 mostly nothing).
- G: 13 jobs; the board was never empty (13 of 13 checks had 1-5 jobs). Extras seen: "Calibrate the cold store
  chiller", "Clean a vent: lift lobby", "Calibrate the cart dock 1", "Reset a tripped breaker: light relays 2",
  "Take dry goods to the galley, Deck 3". The same chiller calibration came up twice in one afternoon (13:01 and
  16:30): a small repeat, worth knowing, not a fault.

Code: data and logic in section 17's slot and one line in `jobsHour`; it only touches the job list (live state, which
the machines already use; the crew's planner never reads it). Extras keep their fields through the save (the job list
is saved whole) and lapse before the crew's claim step in the same hour, so the crew never take one (machine_check 5z
confirms). `j.xp === 0` is honoured by 24 core's turn-in.

Checks, on the first tip 1b3e18f1 and again on 3ffb604f (all the same results): check_fast OK (239 s; machine_check: steady player 9.0 a day, range now
7-12; 5z: Days 1-5 10/0 10/0 10/0 10/0 8/0 jobs/empty minutes, off 3/300; ship health lowest 93.5), intro_check OK,
career_check OK (steady player Relied on by Day 5 at 45 xp, base 48: pace about the same), interactions_check OK,
player_check OK (first tip), cadet_test vs base ALL IDENTICAL. On 3ffb604f: check_fast OK (243 s, 5z the same),
cadet_test ALL IDENTICAL, intro_check --week OK, career_check OK, and the Day 1 drive the same (13 jobs, never empty).

machine_check's expectations moved (each explained in the file): the steady player's range 3-7 to 7-12, and the ship
meters part no longer counts a job without meter gain once the board reads 97 or more (13 such jobs: the ship's
upkeep is all done by about Day 11). Both follow from the note; the second is in the design doc's open questions for
the user's balancing pass, with "should the extra jobs earn reputation?".

## I: toilet queue (note 19; TQ1, claude/patch-play1-i)

**Tip reviewed: 0c05e856** (game sha256 89f593a6...beb7). **Verdict: PASS** (one follow-up for the user, below).

Base repro, before the fix: on Deck 3 with all four toilets empty (nobody in them) but each "targeted" by a crew
member in another room, tapping a toilet says "Occupied: the little light is red". Cause: `playerTap` (section 15)
asks `heldBy()`, which counts anyone whose goal is that toilet, wherever they are on the deck.

Driven in the browser:
- The same probe on I: the toilet visit starts ("About 3 minutes; walk away to stop"). Fixed.
- Live on Deck 3, Day 2 18:50-19:26 (a planned rush after a supper talk), with you taking toilet 1 at 19:05: you go
  in; the two crew planned to queue stand in the washroom's line; the two whose toilet you took join the line (no
  free toilet nobody else was heading for), then at 19:20 the line clears into toilets 2 and 3 (one moves to another
  toilet because you're still in theirs). Nobody ever sat on a toilet with someone else; two moments of two crew
  passing within 0.25 m (the old build had four in the same window).
- Live on Deck 4, Day 1 21:15-22:05: Shah Dara queues alone 21:25-21:56 for the washroom's one toilet, then goes in.

Crew plans, compared on paper for every crew member, Days 0-14: 68 person-days differ, every one only by the new
toilet-line wait (`toiletq`); outside each wait the day is identical, and the toilet visit itself keeps its place and
end. Shower and booth plans are unchanged (the walk-lead reorder in `schedBuild` changes nothing there in 15 days).

Checks: check_fast OK (310 s), cadet_test vs base ALL IDENTICAL (renderer noise only), interactions_check (I's own
copy, with the new "the toilets" section) OK, day_check 2 OK (stuck 0.0 on every deck), events_check OK,
food_check OK. TQ1 also ran day_check 0, 1, 5, 12, 13, player_check and path_check. Design doc updated (the toilet
rule, under "Showers only on Decks 2 and 4").

**Follow-up for the user (not a fail):** the crew's planned toilet waits are now visible as a line, and some are
long while the toilet's light is off. Shah Dara stands in the line from 21:25 to 21:56 although the toilet is empty
21:25-21:29 and 21:38-21:56: the planner books toilet slots that the live crew reach late (TQ1's judgement call 4:
the walk-time estimate is about twice the real walk), and it gives later arrivals earlier slots (two others are booked
in before her on paper). The old build had the same timing (she waited beside the toilet until 21:55, which is what
blocked you), so this isn't new waiting, only now you can see it. A possible fix, runtime only (plans unchanged):
whoever is at the front of a toilet line goes into any toilet in that washroom whose light is off and that nobody
else is heading for, as you can. Suggest a backlog row; section 14/10's owner (PB2) to decide.

Owners: TQ1 touches sections 10 and 14 (PB2, who agreed the lines), 15 (the player's tap, 5 lines) and 22 (baked
words).

## Answers from the user

(space for the user's comments)
