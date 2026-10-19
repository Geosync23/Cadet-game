# Handover: reviewer R4 (the last Step 3 piece, then Pillar 5 Step 4 and playtest update 2)

- **Role:** reviewer. R4 = session_01UGQxniXCxT5TLEE4tgRLfJ, branch `claude/reviews-p5-step4` (push only there). Every verdict is in `plans/reviews-p5-step4.md`, newest first in each section: "Playtest update 2", "Step 4", "Step 3: U's Tracked device app". R3's older verdicts are in `plans/reviews-p5-step2.md` (claude/reviews-p5-step2); R3's note `plans/handover-reviewer-3.md` has the review style and the Step 3 lessons. Read both first.
- **Lead:** lead 17, session_016bN7x175WBwBL7S9xc2Lpb, since ~05:48 UTC (TEAM.md on claude/lead-pillar1 802fe1b says so; lead 16 was session_01UMyfd16GqSdgNyz5PE8qSv). Always check TEAM.md before trusting a "new lead" message. Send every verdict (PASS / PASS WITH FIXES / FAIL, one line plus a note) to the lead, the seat and the build master.
- **Build masters:** BM6 (session_01F8k6hqdBRoxDJMzqAuiHqR) finished Step 3 and is now **inactive** (send_message fails). **BM7 session_01QbuzvT3TwzMwSWRmakzX8Z** builds Step 4 and playtest 2 (plans/brief-playtest2.md on claude/lead-pillar1).
- **Seats:** E1 session_01AHeKjieg3qWjnEVuHecsHd (claude/mech-rounds, 0.45.x), E2 session_01Bezat4UU7beoaKsqdSrJBs (claude/mech-incidents, 0.51.x), E3 session_01WkkCvj4yxnMALMQYG2DsWM (claude/mech-diagnose, 0.53.x), W2 session_01866TWKzGRgZmFcxiYRi4db (claude/writer-p5), U session_01FcMPTX7mMTHkyr4pxDfNcS (claude/hud-pt1), D3 the designer session_0115ZiGhf9s3oYtFdjs7TgYS (pages: claude/p5-design plans/mechanics/).
- **Never** contact the user, start sessions, or push outside the branch. Overnight mode is on.

## State at handover
Passed tips (take these):
- Step 3: U **cf1348c** (0.72.4: Tracked app first in the device AND the HUD button kept, per the user's ~04:00; leave_check follows the turn-in card), C2 **f553607** (0.44.27). BM6 built the 0.63.3 final with them (base for Step 4: claude/p5-cand-pt1 7a6e137 + its last fix 752a794).
- Step 4: E1 **b82c8e2** (0.45.7-0.45.10: tool wear from Day 12 only, the side-job cap worksSideXp +2/day, WORKS_SIDE_KINDS, SHIP.works.side kept by worksClean, Bunk 1 texts, ladder rows m10-m14/m17, playtest-2 item 1 rounds training with roundTrainStep()); E3 **b809339** (0.53.5, the places turn, leak joints on real walls).
- Lines: W2 **c058947** (0.48.110; contains the playtest-2 lines 6a5d34a and Step 4 batch 1 b00e08b).

Open:
- E3 626a907 (0.53.6, M10 workshop + tinkering): PASS WITH FIXES, waiting for E3's next hash. Fix 1: shopFetch with an empty shelf skips the make stop (it clears j.parts, then ticks index k). Fix 2: the made thing must go into your hands (SHIP.player.carry) and be handed over in person (the page). Lead 17 decided ~05:50: follow the page, no chat-button shortcut. Also check that E3 sets flag train.m10.lead (it does, through worksTeach).
- E2 b6130f6 (0.51.6, 24o leaks + 24r irrigation + the one-owner ladder-row fix): see the reviews file (it may be finished there).
- E2 dd0ec46 (0.51.7, 24q rewiring): not reviewed yet.
- Later rounds (summary page step4-summary.html): E1 M11 bench/M12 logbook, stages 2-3; E2 M8 team parts, favour cases, tickets; E3 cabin touches + stars (24t), M17 lift roof. Playtest 2 items from U and X (brief-playtest2.md).

## One-owner watch (the clashes found so far)
- m13/m14 ladder rows: E1's CAREER_LADDER table owns them; E2 dropped its guarded pushes in 0.51.6 and asserts that the rows agree with its constants (mech_check ROW_AGREE).
- toolWear: E2/E3 still carry the base's one-line `const toolWear`; E1's `function toolWear` replaces it in a merge (no conflict). After each merge, `node --check` the script.
- jobStopsBase/jobCard hooks (S2 traceHidden first, then H2 caseAt/caseCard): keep both.
- Reputation from side jobs must go through E1's worksSideXp (the +2/day cap). E3's 'shop' isn't in WORKS_SIDE_KINDS (harmless while it uses jobFinish, with no turn-in note).

## How I reviewed (what worked)
- Small pieces: read the diff (`git diff <parent> <hash> -- starship-cadet.html | grep '^[+-]'`) and the page (`git show origin/claude/p5-design:plans/mechanics/<page>.html | sed 's/<[^>]*>/ /g'`).
- Big pieces: a general-purpose helper agent with a precise brief (page, rules, the names to grep across branches, MUST-FIX vs NOTES, under 600 words) keeps the diff out of my context. Then confirm each MUST-FIX in the code yourself before sending it.
- Checks: `git archive <hash> | tar x -C <dir>` in the scratchpad; run with `CADET_CHROME=/opt/pw-browsers/chromium`; three.js must be at /tmp/cadet-work/three/package/build/three.min.js (`npm pack three@0.128.0`; see DEV_NOTES "Testing"; `pip install playwright` if it's missing). One sequential script in the background, each result logged as it ends.
- Places: a Playwright probe (cadet_test's Game class) that reads EDGES/BLOCKED for each new place and screenshots it found 5 bad leak joints that deck_check passed (deck_check lets a standing place on a blocked tile pass if a neighbour is reachable). E3 added a leak line to deck_check.
- Lines: content_gen.py + lines_check.py in a fresh archive; check the code reads keys that exist (grep the seat's branch for the key prefix).
