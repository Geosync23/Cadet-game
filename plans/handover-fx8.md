# Handover: FX8 (fixer), 2026-10-24

Session session_01GQ33Xh5J5WxwXieiWPwPq1. Reported to lead 31, then leads 32, 33 and 34 (session_019RdVfeRPRiJpHGjKujZZJA).
Memory about 62% at writing: a fresh fixer should take the next big job.

## What I built
| Branch / commit | What | Reviewer | State |
|---|---|---|---|
| claude/fx8-day0-sim 87e3174a (from integration-next 54efee21) | Day 0: once a diner stands up from the Sunday table (day0Trickle's staggered minute, unchanged) their evening is planned again from that minute, everyone else fixed: no bunk or standing-about filler (the user: "let them do what they will do"). Section 14: day0Trickle, DAY0_LEAVE (read by tradLeave and tradMeal), shipDay passes `leave`. events_check 1a: two lines (no filler; nothing before the goodnight changes) | RV10 | sent for 0.92.2; check where it went (replaces day0-stay 583af9ed, which the user dropped) |
| claude/p923-fx8 9fd5b500 (from integration 364c80cb) | 0.92.3 #22: a tap on the person you're due to meet keeps the appointment (Rina's health check), only if they're there for it (its room, or within 2.5 tiles of their spot), never an occasion's. Section 14 apptTapKeep + one line in tapCrew. interactions_check: last part (real tap on Rina; Rina in a corridor; Calder's progress talk). #28 (galley crew "appearing"): checked, no change | RV11 PASS | BM15, 0.92.3 |
| claude/p924-fx8 69356d11 (from integration 3866c8f3; game file as 83808812) | 0.92.4 C: crew glide off a seat/bed/station (up to CREW_UP_MAX 1.2 tiles) at CREW_UP_V 2.5 tiles/s instead of hopping; drawn only (hx/hz in CrewAgent, crewUpEase beside walkLaneStep); longer moves jump as before (lead 34). day_check: "getting up from a place" line per deck (UP_JUMP 0.35), measured on the drawn body (a.h.pos: RV11's fix, which their planted fault now fails). Plus RV11's typeof-guard nit in interactions_check | RV11 | waiting for the verdict; BM16 for 0.92.4 |

## Gotchas
- cadet_test's a_start shot can differ when another browser check runs at the same time; run it alone.
- A background Bash command stops at its time limit (30 min by default): give interactions_check (~35 min) `timeout` 7200000.
- p924's cadet_test vs 3866c8f3 has crew-only pixel diffs (b_wander10s, c_rotated, d_wallslow, i_tap0/1/2/4, j_steer2); proof they're the glide alone: the build with `CREW_UP_V = 1e9` gives ALL IDENTICAL.
- One plan step found on paper that changes deck without a lift ride: Day 5, v-jaramillo-ulla, 'off' on Deck 5 then leisure on Deck 3 at 10:10 (a visitor; section 10 brings visitors by lift, so probably harmless). Not filed.

## Filed
- Backlog FX8-1: a swimmer leaving the pool (8c's moving places) hops up to about 5 tiles when they get up, as on 0.92.3; day_check counts those apart.

## Open for the user
- Long get-ups (rec-deck stands 4 tiles, some mess seats ~2) still jump at once; a fade or a path-following glide would be its own item if wanted.
