# Handover: GM1, games (Tiles and Lightdisc) for the 0.99.7 playtest patch

Session: session_01GKuymmzSJiWGVamRuV5nSG. Lead: lead 49 (session_01GKuymjjreuZtZeDMBX79xn). Reviewer: SC1 (session_01GKuymk1xmJCgzW4Ee8Drz8; RV33 at first). Build master: BM25 (session_01GKuymnYTNkfxgLvtfFRg7w). Sound: AV1 (session_01GKuymmkjHutWouc88NdLkn).

## Branch and builds
- `claude/p997-games`, from claude/integration d7ad4c58 (0.99.6, game f6ff5ec1...db8a8).
- Reviewed and PASSED by SC1 on 98e612e, game sha256 866743edd135be0910c4f3a9602812ac1d535125b70f7c1b093c201628b13260.
- One switch: `GAMES997_ON` (section 13, after TRAD995_ON; `false || URL_FLAGS.has('games997')`). Off = identical to 0.99.6 (cadet_test ALL IDENTICAL).
- Build-number lines untouched. Build table row: "p997-games".

## What I built (plans/patch-0997.md notes, the user's words on claude/lead-49)
- **12 + 40 Tiles night in rounds** (Games slot, section 23b's): `tnTimes`, `tnNight(e, mine)` (pure: plans, schedU k 808 pairing order, 809 results, TL_ODDS, Rina's rule frozen round by round), `tnOpp`, `tnBoards` (each board's facing seat pair), `tnSend`, `tnMinute` (hooked beside tladMinute in section 18's minute line), `tnJoin` (card "Play in the rounds" / "Watch"), `tnIn`, `tnAgain`, `tnBoardTap`, `tnAppBlocks` (Tiles app), `tnPaper` (the news: crew games only). State `TN.by[key]` (not saved: a reload mid-night loses your rounds).
- **41 How to play**: 15 steps from `content/works/games-0997.lines` (`tip.tiles.tut.1-15`, `tip.tiles.card`); `TL_TUT` replaced with the switch; Next/Skip floated right; a new step scrolls the board's top into view; at game end the score line scrolls into view.
- **44 Winner Stays On**: `TRAD_JOIN['rec-wso']` (watch in the stands), `w997Lead` (Pell on deck, else leader on deck, else anyone at it), `w997Card`, `w997Ask` (after you've watched a game end), `w997Go` (discAsk vs the one who stays on), `w997Minute`, `w997Tap`. Section 18: `WSO_GAME` 20 (was 15), `wsoWhere` puts the next challenger on the gate bench `7-stand-28` and clears the court while you walk to it. Rally on court 44% -> 68% of the time.
- **44 music**: AV1's `SND_DISC` (section 27), not mine (the lead's call). I don't touch SND.frame.

## Check edits
- `tiles_check.py`: How to play part reads the step count and the select step's place, the step's text from its `<p>`, 140 characters with the switch.
- `join_check.py`: Tiles night's card handled like the ladder's; a tradition with `stay` is visited when its leader is there.

## Loose ends / for later
- Backlog GM1-1: the Tiles ladder's card (`tladJoin`) has no `where`, so meetingsTick closes it at the next ship minute. Mine pass `where`.
- Tiles night round 1: your first opponent walks ~10 of the round's 25 minutes (SC1's note; left).
- Your Tiles night games aren't in the news (crew games only); the Tiles app shows them live.
- TP1 writes join notices; mine carry their own (`join.rec-wso.*`); Tiles night's existing notice still says "sit at a board and play a few friendly games".

## Gotchas
- `dialogueShow` cards need `where` or meetingsTick closes them within a ship minute.
- `actStart` refuses a seat someone holds ("In use"): seat yourself only when `heldBy(seat)` is empty (tnMinute's 'seat' state).
- Probes: put the player in the Stands before `tradJoinMinute`, or TJ_NOW stays null.

## How to test
Setup as DEV_NOTES "Testing" (three in /tmp/cadet-work/three; acorn in /tmp/cadet-work/acorn for names_check). Switch on in a copy: `sed "s/const GAMES997_ON = false ||/const GAMES997_ON = true ||/"`. Checks: tiles_check (300 games for speed), join_check, disc_check, events_check, interactions_check (needs ~40 min; give it a long timeout), cadet_test vs 0.99.6 with it off, check_fast.

## Open questions for the user (defaults built)
- Three rounds on Tiles night; your games full (to 7); Winner Stays On games 20 minutes (the lead said yes to all three overnight).
