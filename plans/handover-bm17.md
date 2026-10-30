# Handover: build master BM17 (session_01WxdNuUeTUoneMvqKiF6GQL)

Read this first if you take over as build master (BM18). Before me: `plans/handover-bm16.md` (0.92.3-0.92.5).

## Who

- Lead: **lead 36**, session_015LyT1p2Kivp1eaMBC7dMQi (took over from lead 35, session_01VQkkt8RXcvvGs1Dmzn2emM, 2026-10-25 ~06:58 UTC).
- Publisher: PUB1, session_01GnpjFR6oumvuvTrmcXSqeg.
- Check runners: CR1 session_01CsWNjCsy8u5mrHJgTVgCst, CR2 (NEW, from 0.92.6) session_01DsTDi6xJcpdDVhSkELEm24, CR3 session_016oCbvvzgcqzzCTsBFCkYRB, CR4 session_01636CfY2MhB3DzrzZ59dhXz, CR5 session_01CHoEsvv7zMPZDr1ir7uAiz, CR6 session_01B1FwE5sMmHnMPWsGn23nrk (last round done; handover-check-runner-6.md on claude/checks-cr6; a fresh CR6 is needed for the next round). The old CR2 (session_01BgMQaB1LQmhfU1rSJ2ATvv) retired after 0.92.5.
- Reviewers: RV13 session_016ioWtxM6NJRV4Ck3ADwozc, RV14 session_01RwUYVcYt2PP7B7g3ogduFZ, RV15 session_01FJdGhUwL8QBLkF4gJPBauE, RV16 session_01ELg87ZGa4f9GTgTJMx39W5, RV17 session_01CBbf1dZKv1LCrACof9HgyP.
- 0.92.6 builders: FX17 session_01YKeSjUhEnJRbmjyHz2aa6u (traditions), FX18 session_01V2XNs79MARor5fuig48bVF, FX19 session_01VCJjaLf6ZHwNM9YQ5GH9vf (promotion sight, board trades), FX20 session_01FdWDetSihcXZYe2Tp8Kgjy (odd jobs), FX21 session_01PK2uvMjSsonGWpsJpRymqs (crew stories; low memory), FX22 session_013hfW44u1PvirfEXtYYtwVF and FX22b session_01Lzi6Fe2HQJsVbaJBFxXtyx (appointments), FX23 session_01SU6NhoM56vuTMc3d6Pk18D (0.92.5 disc test fix), CS1 session_01QcPAXHjQZ2HfZKMCTbaW9v (words).

## Builds I made

| Build | Commit | Game sha256 | Notes |
| --- | --- | --- | --- |
| 0.92.5 | claude/staging-0.92.5 **39f7741d** | fddc0ef6...5559 | FX15 (item 22) + ZW1's item 8 ("chick") + freeze on BM16's b0916bb1; round all OK after FX23's two test fixes (disc_check #25, controller disc; 404accd9). NOT published on its own: the user wants it to go out with 0.92.6. |
| 0.92.6 | claude/staging-0.92.6 **ec28a7f2** (game as 6b425814) | 10f654de...f266 | From 39f7741d: FX18, FX19, FX21 stories (+Kovac), FX17, FX22 (+FX22b), FX18 test fix, FX20 (+fix), then one commit per switch: P926_TRADS, P926_APPT, PROMO_SIGHT_ON, BOARD_TRADE_ON, STORIES_ON (the user's yes), ODD_ON; build 0.92.6. Round on b78e1e22 (88f4cc8d) + fixes (see build-table row 0.92.6). GO from testing sent to lead 36 at ~17:50 UTC. |

## State right now (2026-10-25 ~17:50 UTC)

- 0.92.6 go/no-go package sent to lead 36 (GO from testing). Waiting for the user's say; PUB1 publishes on lead 36's go. claude/integration untouched (still 0.92.4, ba836359); moving it needs the lead's go.
- CS1's design-doc "Crew stories" section (ae4d60de) cherry-picked onto staging-0.92.6 as 1da1c7b3 (docs only, game unchanged), lead 36's go.
- Known-old for 0.92.6: backlog 12 (career busy pace; numbers in the row), 14, 23, 32, KP1, RV14-1, FX8-1.
- Backlog rows added this session: FX21-2 (arc_check doesn't walk the four new story people), backlog 12's 0.92.6 note. The two rows numbered 17 in backlog.md are left as is (lead 36).
- Round plan for next time: plans/testing-guide.md's six shares plus: CR1 the four arrows checks; CR2 + p926_check; CR3 + arrows_d, arrows_f, controller (every part but reach); CR4 + day 6, 8, appt_check; CR5 + promo_sight_check; CR6 + stories_check. Reach is left out (controller off). The guide's table doesn't list these extras yet: worth adding.

## Gotchas I hit (new ones; BM16's still apply)

- Messages cross a lot. A lead's "do X" can arrive after you've done the opposite. Read every queued notification before acting on any, and say plainly in your next message what you already did.
- A piece reviewed with its switch OFF is not tested ON. When switches go on, run the checks that only bite with the switch on (arc_check with STORIES_ON, machine/interactions odd-jobs parts, bigevents/mech with P926_TRADS, arrows_d with PROMO_SIGHT_ON, join with P926_APPT, career busy pace). The 0.92.6 round found 6 such FAILs (4 stale checks, 2 real clashes).
- Fast isolation: make copies of the candidate's game with ONE switch flipped (python replace of the exact `const X = true` line) and run the failing check on each; then copies of the all-off build with ONE switch on. 2 browser checks at a time. Faster than bisecting merges, and it names the owner.
- Never rewrite a pushed staging branch: when a candidate must change after runners have it, add commits on top and resend the sha + sha256.
- Two pieces adding the same words file (content/works/promo-sight.lines): keep the reviewed one (lead-edited), re-bake with content_gen, tell the lead.
- content_gen.py's `out = {...}` table line clashes when two pieces add keys: keep all keys.
- Build table: when "keep both" leaves the same row twice and one copy is the other plus an appended note, keep the longer copy.
- check_fast before every push, even test-only/docs-only commits.

## How to test (unchanged from BM16)

Test kit as handover-bm16.md. My scripts lived in the scratchpad (gone with this session); the pattern: a side worktree per candidate (/tmp/wt-x), each parallel run its own CADET_WORK with symlinks to three/ and acorn/, cadet_test and perf run from a scratch folder with old.html copied in.

## Open questions for the user (via the lead)

- Backlog 12: should the busy player's career pace be slowed back (odd jobs and a tradition each add a little), or left for the balancing pass? Lead 36 chose the balancing pass for 0.92.6.
