# Pillar 5 Step 4 brief (side jobs), lead 16 (session_01UMyfd16GqSdgNyz5PE8qSv), 2026-10-19 ~03:55 UTC

**Overnight mode is ON** (the user is asleep until they check in and ask for the report). The user asked for Step 4 tonight on its OWN preview link (never main, never the main game link). The Step 4 pages were written tonight by designer D3 from the approved Pillar 5 plan v11; they are the spec, flagged for the user's morning review. Where a page says "lead's call", build it that way.

**Every seat reads, in order:** CLAUDE.md; this brief (`git fetch origin claude/lead-pillar1 && git show origin/claude/lead-pillar1:plans/brief-p5s4.md`); the Step 4 summary `git show origin/claude/p5-design:plans/mechanics/step4-summary.html` (https://claude.ai/artifact/A5z6YJqf5psGgUYDzrGU3Y) and YOUR pages in `plans/mechanics/` on claude/p5-design (index `#s4`); `plans/pillar5-plan.md` Part 6 (the common brief) on claude/p5-design; DEV_NOTES.md ("Rules that keep it working", "Testing", the build table); the handover notes of the seats whose code you take over (listed per seat below).

- **Base:** the Step 3 build 0.63.3 (BM6's final green hash on claude/p5-cand-pt1; the lead sends it to you). Until it arrives, read and plan; do not build on 0.63.2r.
- **Rules (unchanged):** small exact-string edits, never rewrite the file; determinism (no `R()` in shared kit at load; anything random seeded from the save's seed); phones first (`col()`, no coplanar faces, watch draw calls); every new saved field lives under `SHIP.works.side`, loads old saves (a default) and gets a round-trip test; bump the HUD build number in your series and add a DEV_NOTES build-table row per turn; quick checks for what you touched; cadet_test differences explained.
- **ONE owner per function (lesson from Step 3: two clashes came from two seats building the same function).** Each page names the owner. If you need a function another seat owns, ask that seat for it or for a one-line hook; never write your own copy. If ownership is unclear, ask the lead before writing it.
- **Hash keys:** Step 4 uses 1010-1026 (claude/p5-design d22c4c6): M10 1010-1011, M12 1012, M13 1013-1014, M14 1015, M15 1016-1017, favours/tickets 1019-1023, cabin/stars 1024-1025, stocktake 1026; 1018 free; 1000-1009 are H2's.
- **Don't touch:** deck key 7 / the rec deck / `disc` / Lightdisc (the rec deck activation comes after Step 4); the main build.
- **Report to lead 17** (send_message to session_016bN7x175WBwBL7S9xc2Lpb; lead 16 handed over ~05:50): one line when you start; one per finished piece (hash, build number, what, checks, memory %); at once if blocked or a design call is needed. No narration. Send each finished piece's hash to the build master and the reviewer (sessions below).
- **Page questions** → designer D3 (session_0115ZiGhf9s3oYtFdjs7TgYS) directly; anything that changes the design → the lead.
- **Never** contact the user, start sessions, or push outside your branch.
- **Long check runs:** log each result as it finishes; after a container restart resume from the first missing result; keep a ~20-min send_later reminder while a run goes (TEAM.md, "Long check runs survive restarts").
- **Memory:** tell the lead at ~60%; at ~70% write `plans/handover-<seat>.md`, push, stop.

## Build rounds (from the summary)
| Round | E1 | E2 | E3 |
|---|---|---|---|
| 1 | 24 core on C's behalf: tool wear functions, WORK_BANDS[2] (keep [0,12,28,45,60]; side jobs max +2 rep a day), the side-job cap; the section-15 Bunk 1 texts read `playerBed()` | M13 leak hunting | the places turn: every Step 4 place on every deck in one turn |
| 2 | M11 tool upkeep, M12 logbook | M14 irrigation, M15 rewiring | M10 workshop + tinkering |
| 3 | rounds stages 2-3, hauling stages 2-3 (with `manifestRun`) | M8 stage 2 team parts (after E1's `manifestRun`), favour cases | cabin touches, star logging (new sub-block 24t) |
| 4 | spare: review fixes | fault-finder tickets and the pin | M17 lift roof (riskiest; if it slips it ships after, on its own) |

Merge order inside a round: 24 core → mechanics in ladder order → cases → places → the writer's lines.

## Seats
| Seat | Session | Branch | Series | Takes over from (read their note) |
|---|---|---|---|---|
| E1 mechanic engineer 1 | session_01AHeKjieg3qWjnEVuHecsHd | claude/mech-rounds | 0.45.x | C2 `plans/handover-works-career.md` (claude/works-career 48efbd6), M1 notes on claude/mech-rounds, P `plans/handover-player.md` (claude/player-p5) |
| E2 mechanic engineer 2 | session_01Bezat4UU7beoaKsqdSrJBs | claude/mech-incidents | 0.51.x | M2 `plans/handover-mech2.md` (15c247c), H2 `plans/handover-puzzles-h2.md` (claude/mech-cases) |
| E3 mechanic engineer 3 | session_01WkkCvj4yxnMALMQYG2DsWM | claude/mech-diagnose | 0.53.x | M3 (claude/mech-diagnose notes), DA5 `plans/handover-deck-architect-5.md` (claude/deck-p5s3) |
| B build master BM7 | session_01QbuzvT3TwzMwSWRmakzX8Z | claude/p5-cand-s4 | 0.63.4 | BM6 notes on claude/p5-cand-pt1 (`plans/cand-p5-s3-results.md`) |
| R reviewer R4 | session_01UGQxniXCxT5TLEE4tgRLfJ | claude/reviews-p5-step4 | — | R3 `plans/handover-reviewer-3.md` (claude/reviews-p5-step2 be4cea4) |
| W2 head writer | session_01866TWKzGRgZmFcxiYRi4db | claude/writer-p5 | content/ | (continues) |
| D3 designer (on call) | session_0115ZiGhf9s3oYtFdjs7TgYS | claude/p5-design | — | (wrote the pages) |
