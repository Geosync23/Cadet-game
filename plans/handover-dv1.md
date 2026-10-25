# Handover: DV1 (builder; Dev career arrow, Pillar 5 promotion, arrows follower)

Written 2026-10-25 ~01:30 UTC by DV1 at about 60% memory, at lead 35's request. Read CLAUDE.md, DEV_NOTES.md and the
design doc's "Dev mode" and promotion paragraphs first.

## What DV1 built, and where it stands

| Work | Branch / commit | State |
|---|---|---|
| Dev mode's career arrow | claude/dev-career-arrow 9f51257a | RV10 PASS; merged into arrows-c 5f6a19c9, shipped in 0.92.0 |
| Item 81: the Day 2 solo job meeting never started | claude/d2-solo-tap e81ef301 | RV11 PASS; for 0.92.2 (BM15) |
| 0.92.3 items 13 + 23: Name on the beam | claude/p923-dv1 0e329b12 (+ SW2's words bf1496ff, 2bd054f3, 4533c325) | RV13 PASS; for 0.92.3 (BM15) |
| The first promotion in play, on the newer arrows | claude/promo-arrows 81e9065c | RV13 PASS; with BM16 for staging-0.92.5 |
| FX12's Day 9 burst-pipe FAIL in arrows_check's week | claude/m6-day9 e823a74f (on p925-fx12 91b97ee9) | test only; with RV12; BM16 merges it with FX12 |

### Dev career arrow (section 25's slot)
- `dvCareerNext()` (read only) gathers the open career steps and picks the soonest. A timed step counts as now from 15 minutes before (the inspection 30).
  The steps it looks at: the first-week beats, the training under way, the next ladder row's ask or its first missing need, the drill and inspection, the first small row, the test job and the promotion beats.
  While a promotion beat is pending (promo-arrows), other rows' asks are dropped.
- `dvFrame` draws `#dmArrow` (magenta, a DEV tag) with its own animation frame. It keeps 60 px inside the game's arrow frame.
  Where the game's arrow is at the same screen spot (`DV.same`: 16 px to join, 40 px to leave), it draws no arrow of its own and puts its label on the other side.
- The Quick tab has Show it / Hide it (`DV.on`, localStorage `starship-cadet-dev-arrow`).
- Check: `dev_arrow_check.py` (off, walk, look).

### Item 81 (sections 21 and 19)
- `introMeetGo` (introTap asks it first): while a first-week meeting is on, tapping its speaker from outside the room walks you to its standing spot (`b.stand`), and the meeting starts as you enter.
- devDay's beat rows carry `place: b.stand`, and devItemGoal points there.
- Check: intro_check part 18 (`--solotap`).

### Name on the beam (section 18, section 4d)
- `beamGather`: signing opens once 5 crew stand within 5 m of the beam (or 12 minutes after the start) and you're in the Works bay. Then the leader says `join.name-on-the-beam.explain` (SW2's 4 lines), else the event's text.here, one bubble every 4.2 s.
- A late arrival gets only the lines that fit before e.to - 5 (`BEAM_SPARE`).
- `beamWaitTap` shows the "gathering" toast while signing is locked.
- `BEAM.slots` was reordered so your name is the top row's east slot, right-aligned against the painted names (`BEAM.gap`).
- Check: join_check (the lock, the late arrival, item 23's slot line).

### The promotion (24p's slot)
- `promoPartsAside`: the test job's parts are kept on the shelf while it's open.
- `promoGuide` (WORK_TICKS):
  - sets flag 'promoted' once W.tier >= 2;
  - asks the arrow queue for promo:test (level 3, once it's takeable), promo:summons (level 2 from 10:30), promo:move (level 1 during the walk) and promo:ceremony (level 1 from 16:55).
- The old setGoal arrows fire only with the queue off (`promoQueue`).
- The cabin walk starts at 17:00 even mid-job.
- Check: `arrows_check.py GAME promo` (Days 8-12, about 30 minutes; it always uses the build as shipped). It fails on 0.92.3 with 7 lines.

### FX12's Day 9 FAIL (test only)
- The follower runs in a Dev-save page (#dev). A "tap the floor at the pin" click landed under the top-left place-and-clock card, which in Dev mode opens Dev mode's sheet. The follower never closed it, and every later tap hit `#dmSheet`.
- Any change to Day 9's crew plans could shift the timing onto it.
- FOLLOW now closes the Dev sheet and the Ship health panel (the second way to get stuck, also proved).

## Loose ends
- Backlog DV1-1..3 (on promo-arrows' plans/backlog.md):
  - DV1-1: a cart run stuck on "Pick up a hover cart for 1 crate", Deck 3;
  - DV1-2: team job m8 stuck on "brace the housing", Deck 3;
  - DV1-3: a repair whose part is out of stock and can't be made says "Look over the <machine>" instead of saying there are no parts.
  None of them have been looked into.
- Merge note: m6-day9 and promo-arrows both edit arrows_check's FOLLOW block (different lines) and its parts list. That merge is BM16's.
- Dev arrow at 320 px wide: long labels are cut with "..." (the full text is in the Quick tab). Not fixed.

## Gotchas
- Long probes: arrows_check's `Follower` can be imported by exec'ing arrows_check.py up to `with sync_playwright()` (set sys.argv and `__file__` first).
- To save a state mid-run for replay, set `DM_HOLD = true` before writing localStorage and reloading; otherwise the page's last save writes over it. Keep the same CADET_WORK lane, because the file:// path is the storage origin.
- The game's notes bus (simNotes) keeps only a few days. Gather notes each evening in long checks.
- In shell, don't `pkill -f "until grep"`: it kills your own waiting command.

## How to test
check_fast; dev_arrow_check; join_check; intro_check (`--solotap` for part 18); `arrows_check.py GAME promo`; `arrows_check.py GAME week` (queue off) and `... week guide`; career_check; cadet_test against the base.

## Open questions for the user
None outstanding.
