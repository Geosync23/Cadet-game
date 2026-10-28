# Handover: patch builder PE (batch E: #25, #21, #6, #24, #5, #26; owner of the mug #30 and cocoa #29)

From PE (session_01H7weuTSkTfuSAqhxvdx1EK), 2026-10-20, at its memory line. Reports went to lead 20, then lead 21 (session_01KYPEbF745ZQ9g9kr4XJgre). Reviewers: PP1 (stopped), then PR2 (session_013ttt3gV3DaF9y4caBtFnh9); DR1 stood in for owners (stopped).

## Branch and state
- **Branch:** `claude/patch-e`, at b3fed46 at the time of writing. It was started from `claude/integration` 5dd740c.
- **Merged in:**
  - integration 0.64.4 (e3e9ae9)
  - `claude/devmode` up to ada4c5c (a0bd82a, ff528c1): DB1's #30 the mug and #29 cocoa at the bar.
- **Build number:** untouched; the build master sets it.
- **Checks:** check_fast says QUICK CHECK OK on every push.
- **Ready for BM11's merge once:**
  - PR2 confirms its three #26 fixes (b3fed46);
  - intro_check comes back (see Loose ends).

## What's built (all switches off by default: off = identical, cadet_test ALL IDENTICAL)
| Item | Switch (test flag) | Where | Notes |
|---|---|---|---|
| #25 Deck 2 "Officer's Quarters - Science" | none | DECK_NAMES, DECKS[2].name, directory signs/texts | only the directory texts differ in cadet_test, 0 px |
| #21 rank on crew cards | `RANK_CARD_ON` (`?rankcard`) | slot 15 `rankCardRole`; hooks 20 (chat card, Relationships), 19 (roster) | words `card.rank.*` in content/banks/talk.lines |
| #6 time clock confirm + Undo | `CLOCK_UNDO_ON` (`?clockundo`) | slot 15 `clockPunch`/`clockUndo`/`clockUndoSettle`/`clockButtons`; 20's `careerClock(now, quiet, hold)`, `clockScreen(said, ask, after)` | the clock note is held on purpose (up to 5 s late for its listeners); words in content/banks/clockscreen.lines |
| #24 shop buy menu | `SHOP_MENU_ON` (`?shopmenu`) | slot 15 `shopMenu*`; 20's chat card button | words content/banks/shopmenu.lines |
| #5 the ladder | `LADDER_ON` (`?ladder`) | slot 15 `ladder*`; hooks 11 (taps, updateRide), 4d (Deck 5 call panel, two texts) | Deck 5 hatch at v,19,9; Engine control and the Sensor array opened as doors |
| #30 the mug, #29 bar cocoa (DB1's; mine now) | `MUG_ON` (`#mug`) | slot 15 `mug*`; 8b slot PROP_KIT.mug, HOLDS.mug, ACTS.cocoa; hooks 15, 15b | handover-patch-e2.md has the details |
| #26 First Light Cocoa | `FLC_ON` (`?firstlight`; with `#mug` for mugs) | slot 15 `flc*`; content/traditions/first-light.trad, content/meetings/firstLightCocoa.meet; hooks 18 (load gate, eventJoin, TRAD_JOIN, cocoa tag), 5 (dim), 21 (bed arrow) | DEV_NOTES "Patch batch E, first half" |

Probes are in `plans/patch-e-probes/` (see its README). Run them from the repo with `CADET_WORK` set; most take a `Q='&flag'`.

## Switching on (each is its own reviewed step: change `URL_FLAGS.has('x')` to `true`)
- **RANK_CARD_ON, CLOCK_UNDO_ON, SHOP_MENU_ON:** nothing to add. cadet_test differs only where the feature shows.
- **LADDER_ON:**
  - Engine control (Deck 6) and the Sensor array (Deck 2) become doors, which can change crew routes. Run day_check and deck_check with it on; cadet_test should stay identical, since Deck 4 isn't touched.
  - Deck 5 loses its east lift call panel.
  - Backlog-style note: on Deck 1 the relay racks' tap box covers the foot of the ladder hatch, so a player tapping low gets the racks.
- **MUG_ON:** before or with FLC_ON (the mugs at First Light need it).
- **FLC_ON:**
  - events_check, join_check, day_check (Day 1) and interactions_check pass with it on.
  - "Hollis Reach" and "Corvane Drift" in firstLightCocoa.meet are placeholders for the head writer (flagged in DEV_NOTES).
  - The free cocoa is put away quietly when you sit down (DB1's ada4c5c); the seated `sit:cocoa` pose shows the mug.

## Shared formats changed (additive, all agreed)
- `careerClock(now, quiet, hold)`: the 3rd argument is optional.
- `clockScreen(said, ask, after)`: the 3rd argument is optional.
- events_check and section 18's `evTagId` know the crew tag `-cocoa`.
- The First Light tradition id is `first-light`, not `first-light-cocoa`, so its tag parses.

## Loose ends
- **intro_check with FLC_ON + MUG_ON:**
  - Re-running with a 2-hour limit in my container; it was at part 10 at handover. The 25-minute runs timed out at part 10 both off and on, so the limit was too short, not a fault.
  - Its result goes to lead 21 if it lands before I stop. Otherwise re-run: `CADET_WORK=<own> python3 intro_check.py on.html`, on a copy with `FLC_ON` and `MUG_ON` set true, with no short timeout. It takes over 25 minutes.
- **career_check:** fails only on backlog #12 (known and accepted).
- **Owner reviews done** (DR1 stood in, now stopped): hooks in 11, 4d, 19, 20, 18, 5 and 21 all passed. The 15, 15b and 8b mug hooks passed DR1 too.
- **Not built from the #26 draft:** `ties: meeting`, `? pick 3` and a lounge decor tie. They're done in the slot instead (`flcJoin`, `flcScript`, `flcDim`). If the traditions or dialogue engineer adds them to the parsers later, `flc*` can move onto them.

## Gotchas
- **Merging into the player engineer slot:** git once dropped a closing brace where two seats' additions met. After a merge, check `node names_check.js` and compare the slot with both sides.
- **Run browser checks one at a time:** five at once made page loads time out. Give each run its own `CADET_WORK`.
- **Load order:**
  - Code that section 5 or other early sections call must be a function declaration over a `var` (`flcDim`), not a `const` or `let`.
  - `typeof X` on a `let` in its temporal dead zone throws.
- **Comments in one-line `try` blocks:** a `//` comment inside a one-line `try {...}` swallows the rest of the line. Use `/* */`.
- **lines_check prints a huge reading-ease list:** pipe it to `tail -1`.

## Open questions for the user
None. The place names are for the head writer.
