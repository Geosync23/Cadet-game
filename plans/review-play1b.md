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

(in progress)

## I: toilet queue (note 19; TQ1, claude/patch-play1-i)

(waiting for the branch)

Base repro, before the fix: on Deck 3 with all four toilets empty (nobody in them) but each "targeted" by a crew
member in another room, tapping a toilet says "Occupied: the little light is red". Cause: `playerTap` (section 15)
asks `heldBy()`, which counts anyone whose goal is that toilet, wherever they are on the deck.

## Answers from the user

(space for the user's comments)
