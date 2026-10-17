# Handover: Adversarial reviewer 2 (Pillar 4)

**Written:** 2026-10-17 ~06:40 UTC. **Refresh this right before an actual handover** (latest hashes, anything in flight).
**Branch:** `claude/reviews-2` (review notes only, under `plans/reviews/`). I write NO game code.
**Report to:** the lead, session_01KPJMYjXAPkNUcrQ8VRkhLE (since ~04:35; earlier leads 01PJtmxW... and 01PxXKwc...),
and for anything going into a combined build, also build master 2, session_01F8ph7FKqViF3heRn94YgBr.
Chain of command: only the lead talks to the user.

## My seats and their state (last verdicts)
| Seat | Branch | Engineer (session) | Last passed | Open from me |
| --- | --- | --- | --- | --- |
| Dialogue (section 22, content_gen, lines_check) | claude/dialogue | dialogue eng 2, 01S26bs4oMahyGJkuVaCKQGT | b8cf2d9 (0.43.21) | none |
| Traditions (section 18, .trad, events_check) | claude/ship-events | traditions eng (01018WZcc... was 1; check TEAM.md) | f78dd03 (0.34.41) | meal-tradition turnout waits on the sim's `meal` work (not this seat's) |
| Device (section 19) | claude/device | device eng 3, 01SskqNx45iEGyQq2W9Fjg5Y | be8e2ab (0.35.28) | none |
| Decks (DECKS, DECK_DRESS) | claude/decks-p3 | deck architect 2, 01ToE6RJFCw9deB3HcJRLKxS | 9377551 (0.38.17) | Tern plan sketch 8e8894b: PASS WITH FIXES (to the plan; reviews/decks-p3-8e8894b-tern-plan.md); check the build against it |
| Tiles (section 23) | claude/tiles | Tiles eng (idle; handover plans/handover-tiles.md) | 45bdfff (0.46.5) | none |
| Content (head writer's bakes) | claude/content | not reviewed yet | - | next: the writers' batches |
Combined builds: 0.60.2 released (142b503); build master 2 is combining 0.60.3 on claude/cand-0603.

## Known issues outside my seats (reported, for others)
- events_check FAIL `231 dayReport double: 3-store-1 esposito-yara/ishikawa-orla@14:30` is pre-existing (it reproduces on
  0.60.0): the store till's 14:30 hand-over (sim/store owner).
- Meal traditions (Sunday table, harvest supper) draw few people until section 14 treats `meal: dinner` as the dinner.

## Rules I enforce (and found broken before)
- **Duplicate top-level consts across branches** merge silently and break the parse (TRADITIONS, TILES): trial-merge
  and `node --check` the script whenever two seats add generated blocks or kit names.
- **Generated blocks:** content_gen.py must be re-run after merging dialogue (its branch bakes only Sowing).
- **No romance with the player, ever:** lines_check's BANNED list plus the head writer's read. Couple words are allowed
  only in overheard pair:couple/bond:couple lines with no player reference; calls home exempt only plain "love you";
  home contacts limited to mum/gran/jo/sam. Probe new kinds with lines like "in love with the new hand", "my love",
  "Are you seeing anyone, {me}?", "Rumour is {me} and Pell are dating".
- Determinism: plans must be pure (affinityPlan, not affinity); crew randomness via schedU in the seat's key range.
- Rewards: daily caps per person (chat is once a day; Tiles copies it).

## How I test (all in my scratchpad; recreate as needed)
- three r128: `mkdir -p $W/three && cd $W/three && npm pack three@0.128.0 && tar xzf three-0.128.0.tgz`; run checks with
  `CADET_WORK=$W CADET_CHROME=/opt/pw-browsers/chromium-1194/chrome-linux/chrome python3 events_check.py starship-cadet.html [DAYS]`
  (use an absolute CADET_WORK; 7 days fails hull-lights by design, so use the default 28 for verdicts).
- Probes: import cadet_test as a module with sys.argv set to [x, path, path] and use Game(pw, path).ev(js).
- Trial merges in a worktree; resolve the build-label conflicts by keeping HEAD; then `node --check` the largest <script>.
- lines_check probes: drop small files into content/banks|overheard|arcs|home of a dialogue worktree, run content_gen
  into a copy of the html, then lines_check (ignore its "out of date" line).
- My independent Tiles simulator: plans/reviews/tiles-5aa442c-sim.py.

## Loose ends / next
- Review the head writer's and the writers' content batches (wave 1b) when the lead sends them: tone, romance, names
  not aboard, serious lines too early (week 1), self-naming, lines_check PASS, byte-stable bakes.
- Re-check the meal-tradition turnout once the sim's `meal` hook lands.
