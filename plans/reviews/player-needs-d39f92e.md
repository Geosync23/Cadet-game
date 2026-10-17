# Review: claude/player-needs 0.28.51 (d39f92e; merged as 84ef5aa = 0.28.53), Tiles: sit down, someone comes, time stops

Reviewer 1f, 2026-10-17. Builder: player engineer 6 (session_01AWgP6kgzpprnpA5pMAAiqq). Behaviour and save, reviewed in depth (section 23 only).

**Verdict: PASS WITH FIXES.** One MEDIUM (balance, a design call for the lead). Note: 84ef5aa also carries PE7's 0.28.52, which is still a **BLOCK** (player-needs-a9f7ed5.md), so 84ef5aa can't be merged as it stands.

## What changed
- **Sitting down.** Sit at the station or board, and whoever is settled there plays you. Otherwise `tilesFind` picks the best free crew member on this deck: whose plan says off or leisure, not in a chat, not already coming or held, within 40 m, not in quiet hours 21:45-06:00, scored by likes-Tiles, then tier, then distance. They walk over by `crewComeTo` (a 30-minute wait). Nobody free, or they can't make it: a toast, and you just sit (`tilesNobody` turns the activity into 'sit').
- **Time stops.** `PAUSE.tiles` freezes the ship while a game is on and you're seated (0.28.50's frozen clock), with no overlay. A deck tap while frozen brings the board back (`tilesTap`). Leave game ends it mid-game, uncounted.
- **Social** comes at the game's end: `TL_GAIN` (12) × your needs' effect × `bondMult`. Friendship and the memory stay once a ship day per opponent (`relDay`).
- **How to play:** 8 steps, each moved on by doing it, or by Next / Skip. `SHIP.tiles.taught` is saved through `tilesLoad` (`=== true`, so an old save reads false and you get the walkthrough once). 0.46.6's `crewHold` is folded in, and released on done, leave, a new game and newGame.

## Checked
- **No way to get stuck frozen.** The freeze needs `TL_GAME`, a game not over, and you seated (`tilesSeated`). The result screen, Done, Leave game and walking off all unfreeze. While frozen you can't walk, but a deck tap reopens the board, and Leave game is under it.
- **The opponent's moves** run on the game's own timer, so they still play while the ship is frozen. Crew are frozen and the opponent is held.
- **Waiting for someone** runs in ship time, before the freeze starts. If they don't come, `A.release` lets them go back to their plans.
- **Saving.** Only `taught` is new, and it's cleaned on load. `TL_GAME` isn't saved, so a reload drops a game in progress, as before.
- **tiles_check on d39f92e:** see below.

## Findings
**MEDIUM (balance; design call for the lead): unlimited social with no time cost.** No ship minutes pass while you play, and every finished game adds `TL_GAIN × bondMult` social, with no daily cap. Friendship is capped per day; the need isn't. So "Quick game (to 5)" → Again → Again fills social from empty in a few real minutes and zero ship time, which makes the social need trivial. Options:
- (a) The need gain is full for the first game with someone each ship day and small after (as `relDay` does for friendship).
- (b) Each finished game advances the clock a little (say 10-15 ship minutes) on unfreeze.
- (c) Cap the social from Tiles per ship day.

My lean is (a): it's simple and matches friendship.

**INFO:** a game with no board (`TL_GAME.where` null, played from the app) also counts as seated, so it freezes the ship too. That fits "while you play, the ship waits", but it's worth knowing.

## tiles_check
ALL OK on d39f92e (reviewer 1f). The seated game against farouk-olu takes social from 56.9 to 68.9 per game, which matches the MEDIUM.
