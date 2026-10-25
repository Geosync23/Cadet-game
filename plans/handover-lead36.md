# Handover: lead 36 → lead 37

## START HERE (lead 37)
1. Read CLAUDE.md, this note, plans/patch-0.92.6.md, plans/morning-summary-lead36.md, then the bottom of TEAM.md on claude/lead-36 (from "LEAD 36 took over").
2. Branch `claude/lead-37` from `claude/lead-36`; push only there. Read the game from origin/claude/staging-0.92.6 (or staging-0.92.5), never the lead branch's copy.
3. Make your hourly check-in (create_trigger, cron `57 * * * *`, into your session), then disable lead 36's trig_01KoDEZkuYt3nBtyQS9UMgLd.
4. Message every working seat with your session id (priority "next", never "now"). Tell lead 36 (session_015LyT1p2Kivp1eaMBC7dMQi) you've taken over.
5. User in US Eastern (EDT, UTC-4). Plain words, no emojis, few messages. Cap 8 working seats; during a six-runner round only BM + 6 + 1.

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
