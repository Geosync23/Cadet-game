# Handover: rec engineer A (RA): the rec deck's crew use (R7) and traditions engine (R11)

Session: session_012mZrFQrGpbNeNWuRg4Bxyp. Reports to lead 19 (session_01FsGspstkG61e9AWadSi36y). Brief: `plans/brief-recdeck.md` on `claude/lead-pillar1` (seat RA). Never contact the user, start sessions or push outside the branch.

## Branch and builds
- `claude/rec-crew`, from the 0.63.4 final (aa4f42c4). Series 0.83.x.
- 0.83.0 (22ff1bb6): R7 round 1. Reviewed by R6: PASS WITH FIXES (all four fixed in 0.83.2).
- 0.83.1 (4c971226, pushed as WIP) and 0.83.2 (from 9abd51fb on; the last commits are WIP until the final check round is logged in DEV_NOTES): the traditions engine, the reviewers' and leads' fixes, RB/RB2/W3 hooks.
- Everything waits for `REC_DECK` (false on this branch; RB2 switches it on last). With it off, cadet_test vs 0.63.4 is ALL IDENTICAL. Test on a copy with `const REC_DECK = true;`.

## What I own and built (see DEV_NOTES rows 0.83.0 and later, and the section "The rec deck's crew")
- **Section 4e:** `REC_CREW_PLACES` (lanes, kayaks, belays, float, waiting spots, lockers, showers, the talks' ring 7-ring-1..8, stool, lectern, acts, booth, the `river-banks` venue spots) and `DECKS[7].gathers`; `playerOnly: !REC_DECK`. Places carry RB's `move: { kind, ... }` and `anim: 'slump'` on seats/beanbags.
- **Section 14:** `REC_HABITS` (layered in `habitsOn`), `recHabit`, `recVisit` / `recSwap` (visits only replace rest or time off the Commons, so the Commons never lose anyone), `REC_CAP` 15/6 via `occ.rec`, `recHostEarly` (an early host wakes), `recRound` (Maeve's round of RB's `<machine>-svc` places), rec-only fixes in `leisureUntil` / `morning` / the off-day morning. The blackout's deck pick stays Decks 1-6 (lead 18).
- **Section 15r (crew-facing):** the queue (`recQueue`, `recWait`, "You're up"), free lanes/belays (`recLanesFree`, `recBelaysFree` with RB's `recShut()`), the court (`recCourtFree`: your baseline 7-disc-1; a lone crew player waits on 7-disc-2 and you play them, `recCourtWaiting`), Winner Stays On's tap (`recWsoTap`), the Cup (`recCupTap`).
- **Section 18:** `REC_TRADS` (rules here; W3's .trad of the same id brings only words: the loader merges them), ids and k W3's (486-498); `TRAD_ROTA` and `REC_TALKS` (the talks' rota, first four only, lead 17's call 4); `REC_BIG` skips; `wsoCourt`, `wsoWhere`, `cupBracket`, `regattaWinner`, `recPickups`, `recCourtNow`; `SHIP.rec` (`recClean`) and the boards (`recBoard`); `recFirstAllHands` (from `captainAddress`), `recShowTick` (calls RB2's `recShow` every ship minute), `recMyTalk`, `recTalkCard`, `recActCard` (W3's baked meetings when present), `recMail` / `recWords` (W3's mail.rec.* keys). Engine: `stay`, `unflag`, `quiet`, `skip`, `whereFor`, `first`, `when.rota`; rec traditions budgeted among themselves (`evBudget`).
- **23b (pairing calls only):** `discAsk(who)`; `discTalk('lose')` one-liner.
- **Checks:** day_check 1b (three ways: off, on without traditions via `REC_TRAD_ON`, on; strict on everyday use, reports the traditions' effect, fails with no visits); events_check 1c (the plan's days for weeks 1-6, hosts, speakers, film's move, all-hands on day 92, the boards) and the rec tweaks in its year scan and flag check (days 92, 99). `plans/trad-format.md` and `plans/trad_parse.py` (new keys).

## Open items
- interactions_check on a REC_DECK=true copy: "the button clears the other HUD buttons on a 320 px phone" (being checked against 0.63.4 flipped; likely the switch/HUD's, RB2).
- W3 keys not wired yet: rec.wso.up, rec.wso.win, mail.rec.allhands.night, mail.rec.talent.signup, mail.rec.talk.next.
- The rest of the talks' rota (`REC_TALKS` rows with `true`) waits for words; the regatta's fun heat is the ordinary kayak tap; the Paddle club fast run isn't gated (lead 17's call 3).
- Crew don't get fitness/social on paper from rec visits (crewNeeds ignores rec types).
- The player and crew can overlap visually in a lane or the float room (the player's moves use spots, not places).
- Reported to the lead: rec traditions draw a little from the Commons in their windows (talent night Day 14: Deck 3 evening mean 43.8 -> 36.0).

## Gotchas
- **Never append a `//` comment in the middle of a line you're replacing.** It swallowed code three times here (`eventTags`' try, `evGoers`' `.sort`, talent night's `at:`). Grep the added lines after every edit; a game that won't load on the REC_DECK=true copy is the sign.
- An id ending like an anim (`rec-chiefs-talk`) needs `evTagId`'s id-first check.
- Run at most two or three checks at once (4 CPUs): page loads time out otherwise. Each run its own CADET_WORK.
- `pkill -f` with a pattern that also appears later in the same shell command kills your shell (exit 144). Kill by pid.
- `typeof X` on a `const` not yet declared throws; ask `EV_READY` (a var) first from section 14.

## How to test
`scratchpad`-style: `sed 's/^const REC_DECK = false;/const REC_DECK = true;/' starship-cadet.html > on.html`; then `day_check.py on.html 7` (and 14, 28), `events_check.py on.html 42`, `events_check.py starship-cadet.html` (dormant), `deck_check.py on.html`, `cadet_test.py <0.63.4> starship-cadet.html` (ALL IDENTICAL), `player_check.py`, `interactions_check.py`.
