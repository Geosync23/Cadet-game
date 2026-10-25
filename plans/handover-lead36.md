# Handover: lead 36 → lead 37

## START HERE (lead 37)
1. Read CLAUDE.md, this note, plans/patch-0.92.6.md, plans/morning-summary-lead36.md, then the bottom of TEAM.md on claude/lead-36 (from "LEAD 36 took over").
2. Branch `claude/lead-37` from `claude/lead-36`; push only there. Read the game from origin/claude/staging-0.92.6 (or staging-0.92.5), never the lead branch's copy.
3. Make your hourly check-in (create_trigger, cron `57 * * * *`, into your session), then disable lead 36's trig_01KoDEZkuYt3nBtyQS9UMgLd.
4. Message every working seat with your session id (priority "next", never "now"). Tell lead 36 (session_015LyT1p2Kivp1eaMBC7dMQi) you've taken over.
5. User in US Eastern (EDT, UTC-4). Plain words, no emojis, few messages. Cap 8 working seats; during a six-runner round only BM + 6 + 1.

## Latest (~18:00 UTC, 2 PM Eastern) — READ THIS FIRST
- **0.92.6 GO** (BM17 package): claude/staging-0.92.6 tip d4be69cf (docs only on ec28a7f2; game sha256 10f654de56f76598c0747530fe5d05185fcc6eb5e91398584d462aafc8ebf266, HUD 0.92.6, all six switches ON incl. crew stories). **USER said publish to BOTH Playtest 3HqM5xiXaHXzgrpq7JbesJ and Dev 9ZWAgqiZCvkJvVjjhjVkEr** (~1:55 PM Eastern); PUB1 (session_01GnpjFR6oumvuvTrmcXSqeg) is publishing; it will report links + versions to lead 36 or you. NEVER over 6daNCLCJAcsLCZn27CEthq. Next: tell the user the links; then ask the user's OK to fast-forward claude/integration to the published commit (a BM does it; BM17 ~60% can do this one small ask, else BM18 from plans/handover-bm17.md). CS1's design-doc stories commit ae4d60de: BM17 may still need to cherry-pick it (docs only).
- 0.92.5 was never published on its own (user: wait for 0.92.6).
- Career pace = backlog 12 (lead call, user told; the user may overrule, e.g. ODD_MIN 2).
- **Sound/music (SD1 session_012DnJzEerXDa6SScxbQZ1q5, claude/sound-sd1)**: all sound decided (Soundscape PP6pDpiZw8jzaNoLygCTgC, Activities 5sjuT5XCJqCvMP68AipdZP, Round 2 1MXY7YxN9DGUChzUhAUyU7). Music: player/test page https://claude.ai/artifact/2eiwTWnoSjg9SWcwi3k6Cy v6 = planetarium space music, no noise, no drums, 21 tracks renamed, 3-4 per time of day, rotation, Music app, on by default, silent Day 0 (just shown to the user; awaiting reaction). Build sound + music into the game only on the user's go AFTER 0.92.6 (plans/sound/integration-plan.md, audio-todo.md; ~1.5 days + music 3.5-5 h). Tradition music held.
- Seats idle and reusable: FX17 (~52%), FX18, FX19 (~45%), FX20, FX22b, RV15, RV16, RV17, CR1-5, SW2, CS1, SD1. Need fresh CR6 (and BM18) before the next round.

## Earlier (~17:15 UTC, 1:15 PM Eastern)
- All round fixes PASSED: FX17 3e8c78a6 + eba4d365 (RV17), FX19 acb36503 (RV15), FX22b join 3d011393 (RV17), arc_check 70813dc8 (in staging). BM17 merging + re-running (bigevents, mech, arrows_d, join alone, p926, events, day 7, check_fast, cadet vs b78e1e22). Career pace = backlog 12 (lead call, told user; user may overrule: e.g. ODD_MIN 2). Then BM17 package → user → PUB1 on the user's say (Playtest 3HqM5xiXaHXzgrpq7JbesJ + Dev 9ZWAgqiZCvkJvVjjhjVkEr; NEVER 6daN…), then the user's OK to fast-forward integration.
- Music: approved, ON by default, no music Day 0, Music app on device; test page https://claude.ai/artifact/2eiwTWnoSjg9SWcwi3k6Cy; module plans/sound/music-module.js (claude/sound-sd1 aef13a0). Sound + music build after 0.92.6 on the user's go (plans/sound/integration-plan.md, audio-todo.md).
- Fresh CR6 needed before the next full round (old CR6 ~60%).

## Earlier (~17:00 UTC, 1 PM Eastern)
- Round fixes: RV15 PASS FX19 acb36503 (arrows_d test fix). Waiting RV17 on FX17 3e8c78a6 (Line clash, game) + eba4d365 (m17 check) and FX22b 3d011393 (join_check test); BM17 bisecting career pace (+1 xp by Day 4 with switches off = backlog 12 edge; ODD_ON adds ~8 jobs/day, 0 xp each). Lead default: keep 0.92.5 pace. Then BM17 merges, re-runs, package → user.
- Sound (all SD1, session_012DnJzEerXDa6SScxbQZ1q5, claude/sound-sd1): decided Soundscape PP6pDpiZw8jzaNoLygCTgC; Activities approved 5sjuT5XCJqCvMP68AipdZP (no on-the-line call sound); Round 2 1MXY7YxN9DGUChzUhAUyU7 (clock C, tap B louder, no mood); Sound Lab Q6j5kSrYRvPxmSZdRB1DMg: music APPROVED, ON by default; SD1 building game-ready music module + Music app mockup + harness (not in game). Sound + music build after 0.92.6 on the user's go. Tradition music held (audio-todo.md).

## Earlier (~16:00 UTC, noon Eastern)
- USER: 0.92.5 not published, waits for 0.92.6. USER YES crew stories ON.
- 0.92.6 round on claude/staging-0.92.6 b78e1e22 (game 88f4cc8d…, all six switches ON); arc_check stale-check fix 9d758ada (test only, CR2 OK). Open: CR6 mech m17 (BM17 isolating by switch) and bigevents Day 7 Captain at Winner-stays stands (FX17 fixing, RV17 reviews). Then BM17 package → user → PUB1 on the user's say (Playtest + Dev; never 6daN…).
- Sound: SD1 session_012DnJzEerXDa6SScxbQZ1q5, page https://claude.ai/artifact/PP6pDpiZw8jzaNoLygCTgC (v2; v3 coming: footsteps like carpet, no crowd chatter) + plans/sound/integration-plan.md (user asked how much work to put it in the game).

## State (~15:00 UTC, 11 AM Eastern)
- **0.92.5**: GO from testing. Candidate claude/staging-0.92.5 39f7741d (game fddc0ef6…5559). Waiting on the user's say to publish (PUB1 session_01GnpjFR6oumvuvTrmcXSqeg: Playtest 3HqM5xiXaHXzgrpq7JbesJ + Dev 9ZWAgqiZCvkJvVjjhjVkEr; confirm with the user; NEVER 6daNCLCJAcsLCZn27CEthq), then the user's OK to fast-forward integration.
- **0.92.6**: all items built and reviewed. claude/staging-0.92.6 1fe6d523 (switches off). BM17 (session_01WxdNuUeTUoneMvqKiF6GQL) holds candidate 48b839b2 locally: switch-ons P926_TRADS, P926_APPT, PROMO_SIGHT_ON, BOARD_TRADE_ON + HUD 0.92.6; ODD_ON joins if RV15 passes FX20 9755ca3f by ~15:30 UTC, else follow-up. STORIES_ON stays off until the user says yes. Round plan in TEAM.md ~14:28 UTC; runners CR1, CR2 (new: session_01DsTDi6xJcpdDVhSkELEm24), CR3, CR4, CR5, CR6 (last round).
- After the round: BM17's package → show the user → publish 0.92.6 only on the user's say.
- Questions open for the user: publish 0.92.5? crew stories on? Saad at the valve later?

## Seats
- Working: BM17 (~33%), FX20 (session_01FdWDetSihcXZYe2Tp8Kgjy, ~26%), RV15 (session_01FJdGhUwL8QBLkF4gJPBauE, ~23%), CR1-6 in the round.
- Idle, may be reused: RV16 session_01ELg87ZGa4f9GTgTJMx39W5 (~28%), RV17 session_01CBbf1dZKv1LCrACof9HgyP (~33%), FX22b session_01Lzi6Fe2HQJsVbaJBFxXtyx (~23%), FX17 (~42%), FX18 (~49%), FX19 (~41%), SW2 (~33%), CS1 (~30%).
- Done for good: FX21 (63%), FX22 (60%), FX23 (10%), RV14 (55%), CR2 old (60%).

## Backlog added tonight
FX17-1 (switch-off talk card + talent night card close at next minute; fixed with P926_TRADS on), FX17-2 (cadet first shot flip; likely shared-copy hole, fixed test-only by FX18; own diff never reproduced), FX18-1 (done), FX21-1 (older moments' chatter over a story speaker), night round reload before 4 stops = missed (fixed by FX22b), plans/backlog.md has two row 17s.

## Gotchas
- When handing a builder's branch to a fresh builder, wait for the old one's "stopped" before hiring the new one (FX22/FX22b did the same work twice).
- cadet_test on a busy machine can flip a_start (FX17-2); rerun alone.
- Never priority "now". Check shas on origin before believing "pushed".
