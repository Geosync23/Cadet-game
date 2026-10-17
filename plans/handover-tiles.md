# Handover: the Tiles engineer (seat 10, section 23)

Written 2026-10-17 at build 0.46.3, updated at 0.46.4 (`claude/tiles`) by session_01DG3in6CvFFta6NrLpoVCJV, for a fresh session taking over this seat. Read it with `plans/tiles-plan.html` (the approved design and the user's decisions at the top), DEV_NOTES rows 0.46.0-0.46.3, and the "Tiles" lines in `plans/pillar4-plan.md` (Part 5, seat 10 in Part 6).

## Role and chain
- Tiles engineer, Pillar 4 seat 10. Report ONLY to the lead (now session_01KPJMYjXAPkNUcrQ8VRkhLE, from ~04:35; before that session_01PJtmxWgAPLebXSZKP6ZRpG) with send_message after each push (commit, checks, memory %). Never contact the user. Reviewer: reviewer 2 (session_0142TQw4ke8caPSyAC93VT98).
- Branch `claude/tiles`, builds 0.46.x. Hash keys 800-829. Commit messages end with the Co-Authored-By line only; no model names anywhere else.
- Started from ship integration 0.60.0 (e3ee66b), merged into this branch at 578dcbe.

## What I own
- `// 23. TILES` in `starship-cadet.html`, between section 21 (ARRIVAL) and section 6 (CAMERA).
- `plans/tiles-plan.html` (approved; "Decided" section), `plans/tiles-sim.py` (the throwaway Python simulator; `python3 plans/tiles-sim.py` prints the plan's table), `tiles_check.py`, `plans/handover-tiles.md`.

## What's built (0.46.0-0.46.3)
| Build | Commit | What |
| --- | --- | --- |
| 0.46.0 | 5643c14 | Rules and crew play on paper: `tilesRng`, `tilesDeal`, `tilesNew(mode, rng, teach, first)`, `tilesMoves`, `tilesApply`, `tilesStep`, `tilesFinish`, `tilesAI(s, level, rng, style)`, `tilesSimGame`, `tilesStyle(p)` |
| 0.46.1 | 32ed900 | The board on the device: a Tiles app (`deviceApp` id 'tiles'), `tilesPlay(opponentId, where, mode)`, `tilesDraw` (one persistent DOM element; CSS injected from section 23), `tilesTap`, `tilesDo`, `tilesCrewSoon` / `tilesCrewMove` (0.7 s setTimeout), `tilesOver`, `TL_TALK` stand-in lines |
| 0.46.2 | acb9bc8 | Sitting down: `tilesWorldTap` (unshifted into `PLAYER_TAPS`), `PLAYER_ACTS.tiles` (sit:play, `until` Done), `tilesLeft`, `tilesReward`, `tilesLoad` / `save.tiles` |
| 0.46.5 | (see git log) | The shelf trophy's trace when you first beat Rina |
| 0.46.4 | 891721d | Review fixes: first player turns about per opponent (`SHIP.tiles.first`), crew lines on their own stream (key 807), friendship once a day per opponent (`SHIP.tiles.relDay`), tables and boards only on Tiles night (`tilesNightNow`), the ship's time on the board, tiles_check judges balance only at 4000 games |
| 0.46.3 | beee494 | Tiles night on paper: `TL_ODDS`, `tilesNight(day, came)`, `tilesNightNews`, `onSim('tradition')` for ids starting `tiles`, `tilesTrophy()` |

## Shared formats
- Board: 36 cells, `i = y*6 + x`, y 0 = the player's home row. Tile `t = o*3 + m + 1` (o seat 0 you / 1 crew; m 0 Planet, 1 Ship, 2 Star). `tlO`, `tlM`, `tlT`.
- State: `{ b, hold: [[marks],[marks]], sc, p, first, plies, last, mode: 'full'|'quick', over, win, why, reached }`. Moves `{ k: 's'|'j'|'l', from, to, over, m }`.
- `TL_MODES = { full: { target 7, turns 14 }, quick: { target 5, turns 12, finish: true } }` (quick: equal turns; tie = more tiles left, else whoever reached 5 first).
- `SHIP.tiles = { played, won, lost, vs: { id: [w, l] }, firstWin, beatRina, night: { last, rina, games: [[a, b, win]] } }` in `save.tiles`.
- `simNote('tiles', { opp, win, sc, mode, where })` at the end of each of your games.
- Hash keys: 800 a game's seed, 801 night pairings, 802 night rolls, 803-806 a crew member's style (bold, patient, chatty, level), 807 chatter (unused so far: chatter uses the game's rng), 808-829 free.
- Lines the writers can add: `lineFor(who, 'tiles.start' | 'tiles.dock' | 'tiles.miss' | 'tiles.win' | 'tiles.lose')`; stand-ins in `TL_TALK` until then.

## Loose ends
1. **interactions_check** passes again since 0.46.4: tables and boards only open Tiles during a Tiles night.
2. **The opponent isn't held in their seat:** if their schedule moves them, they walk off while the game carries on on the device. Needs a small hold on the walker (section 10, the sim engineer). Offered to the lead.
3. **Ship time:** ruled (the lead): a game takes its real time on the normal clock (about 1.5 ship hours). Done in 0.46.4.
4. **Quick game balance:** Medium first player 52.2-52.5% in 10,000-game JS runs (just over 52%); tiles_check allows 53% for the quick game. Turn-about who goes first (built) cancels it for the player.
5. **The trophy:** done in 0.46.5. The deck architect's DECK_DRESS `tilesTrophy` (decks 0.38.17) shows from section 18's lasting traces; `tilesReward` adds the trace when you first beat Rina (`traceAdd` if present, else the string pushed once to `SHIP.traces`). After the combine with 0.38.17, check that the trace format matches theirs (they described `{ id, day }` objects; this base keeps strings) and that `dressingOn()` lists it on Deck 4.
6. **The bow-lounge station and Tiles-night boards** live on `claude/decks-p3` (names `TILES_KIT`, `tilesBoardGeo`, `tilesSeats`, `DECKS[3].tiles`, places 3-tiles-1/2). My tap handler matches items titled /^Tiles (table|station|board)\b/i with sit places within 2.4 tiles; asked the architect to title theirs that way. Only the Deck 4 junior common room's "Tiles table" exists on my base.
7. **Tiles night tradition data** is `content/traditions/tiles-night.trad` (id `tiles-night`, Tuesday 20:00-21:30, host Rina; attendance tag `ev-tiles-night`). My listener takes any id starting `tiles`. The traditions engineer asked where results live: section 23 (`tilesNight(d, came)`, `SHIP.tiles.night`); my reply bounced (their session is inactive), so it went to the lead.
9. **TL_TALK stand-ins** should move into `content/` as `tiles.*` lines (writers / dialogue engineer) before release, so lines_check sees them (reviewer 2, LOW).
8. No Record-app API: the Tiles record (tally, by opponent, first win, beating Rina, last night) shows in the Tiles app.

## Gotchas
- Never declare `TILES` or `tilesSeats` at top level (decks-p3 has `TILES_KIT`, `tilesSeats`); two same-name consts merge silently and break the whole script.
- Section 23 runs before section 9: `ROSTER` is in its TDZ at load. Only touch it at runtime, and wrap reads in try/catch where the device might draw at load.
- No `R()` or `Math.random` in section 23 (tiles_check scans for them). All crew randomness comes from `schedU` keys 800-829 or a game's `tilesRng`.
- The device redraws dom-block views every ship minute; `tilesDraw` reuses one element, so keep state in `TL_GAME`, not in the DOM.
- The device's look rules (device_check): no text under 15px, buttons 44px, no CSS filter.
- In tiles_check, clear `TL_GAME.timer` before stepping by hand, or the 0.7 s crew move fires mid-check.

## How to test
Setup as in DEV_NOTES "Testing" (three@0.128.0 in /tmp/cadet-work/three; `pip install playwright`). Then, one browser check at a time:
- `CADET_CHROME=/opt/pw-browsers/chromium python3 tiles_check.py starship-cadet.html` (about 4 minutes; pass a smaller game count, e.g. 300, for a quick run: the skill checks can then dip under 60% by chance)
- `cadet_test.py OLD NEW` (expect ALL IDENTICAL: nothing in section 23 draws on the 3D scene), `device_check.py`, `player_check.py`, `events_check.py`, `interactions_check.py` (expect the three Tiles table rows above).

## Open questions for the user (via the lead)
- Whether Tiles lines should also appear in the Record app (needs the device engineer).
