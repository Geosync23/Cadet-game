# Handover: FX13 (builder)

Session: session_01KVmjkTUis1ktZ3U7Ryc3jr. Leads over time: 32, 33, 34 (session_019RdVfeRPRiJpHGjKujZZJA). Written at about 57% memory, at lead 34's ask.

## What I built (all reviewed unless marked)

| Work | Branch / sha | Reviewer | State |
| --- | --- | --- | --- |
| 0.92.3 item 15: own Talk a while pools only for the Captain and main characters; the Captain's first-talk welcome | claude/p923-fx13 bc976e7d (engine) | RV13 PASS (incl. section 20 sign-off) | merged in 0.92.3 (BM15 baked CS1's words on top: 11 people `only: own`) |
| 0.92.5 item 5: the chat card's line before hello doesn't repeat till all are said | claude/p925-fx13 04a9385d (dab87131 + merge of 0.92.4 ba836359) | RV11 PASS | with BM16 for 0.92.5 |
| Sim flight landing prototype (standalone, NOT in the game) | claude/simflight 6d5611ee (simflight-proto.html, tools/simflight_proto_check.js, plans/shots-simflight/) | RV12 PASS | PUB1 publishes; on hold per lead 34 |
| 0.92.5 item 20: the Tiles ladder round the Tiles table | claude/p925-fx13b 5e1d82d5 (first push ae8c8bc9; then tladLead) | RV12 PASS (4 planted faults caught) | with BM16 for 0.92.5 |

## How each works (where to look)

- **Own talk pools (section 22's dialogue slot + content_gen.py).** `.talk` files: `only: own` (file level), `first: yes` (1-6 them: lines; section 20's talkStep holds the question: `talkPackHold`), several files a person. `talkOnlyOwn(p)` (function declaration: lineFor asks it), `talkPackOwnAgain` (least lately had again), `talkPackFire` holds a first talk until answered. Section 20 has three one-line hooks (talkStart no hello before a first talk; talkNext no chatLine fallback; talkStep's ask waits). DEV_NOTES Talk pack paragraph; plans/talk-pack-plan.md "Own pools only"; talk_check parts (g) and (j).
- **Fresh openers (section 22: lineFor + dialogue slot).** For `LINE_FRESH_KINDS` (greet, near, life, joy, about) lineFor drops lines that person has said (bit strings over their whole pool, own then template then bank in baked order), clears when everything that fits now is said; peeks never mark. `SHIP.fresh` / `save.fresh` / `freshClean` / linesNew clears; switch `LINE_FRESH_ON`. talk_check part (k). Not covered: crewFeeling's lines and the CHAT_* fallbacks.
- **Sim flight prototype.** Pure rules `fnew`/`fstep` at 60 steps/s; the view in section 2 of the page (17 draw calls); input flips x because the chase camera looks along +z. Check: `NODE_PATH=$(npm root -g) node tools/simflight_proto_check.js`.
- **Tiles ladder (sections 4d, 18, content/traditions/tiles-ladder.trad).** Ring places `3-ladder-1..9` (deck architect slot); the trad's `where: 3 pool @tiles-ladder`; section 18 traditions slot: `tladMinute` (runtime only, Deck 3, crewComeTo two to the stools, 10-minute games, winner stays, k 334/335), `tladJoin` (play/watch card), `tladAgain`, `tladLead` (ev.lead: host 20 minutes early, others 15 when free). join_check's ladder part.

## Gotchas

- Parallel Playwright checks clobber each other's test copy (`/tmp/cadet-work/test/_run_<name>.html`): run join/tiles/events/day checks one after another, or give each its own CADET_WORK. check_fast and cadet_test are fine alongside.
- `.png` is git-ignored: screenshots need `git add -f`.
- names_check needs acorn at /tmp/cadet-work/acorn/package (`npm pack acorn@8`); three.js r128 at /tmp/cadet-work/three/package.
- The ladder's crew walk ~2 m a ship minute; without `tladLead` most of the ring arrived 15:15-15:25.

## Loose ends

- Item 20: PASS (RV12, 5e1d82d5); the set-off-early change (tladLead) was added at lead 34's ask after the first push.
- The ladder card's step counter shows "2/2" (dialogueView counts lines for a choice without a prompt; cosmetic).
- Possible writer work: the host's `ladder.ask`, `ladder.play`, `ladder.watch` lines (stand-ins in tladJoin now).

## How to test

talk_check.py (parts g, j, k), join_check.py (the ladder part), tiles_check.py, events_check.py, day_check.py BUILD 6, lines_check.py, names_check.js, check_fast.sh, cadet_test.py OLD NEW.
