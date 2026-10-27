# Handover: lead 40 (MOVING TO A NEW ACCOUNT)

## START HERE (the first lead on the new account)
The user moved the project to another claude.ai account on Oct 26-27 (decided ~03:00 UTC Oct 27 = 11 PM Eastern Oct 26). Nothing on the old account (sessions, scheduled tasks, artifacts) can be reached from the new one; only the GitHub repo carries over.
1. Make sure the new account's GitHub connection can reach **Geosync23/Cadet-game** (read + push).
2. Read CLAUDE.md, this note, the bottom of TEAM.md on **claude/lead-40** (from "LEAD 40 started"), then plans/handover-lead39.md for the background (user rules, specs, ending answers).
3. Make your own branch (claude/lead-41 from claude/lead-40), your own hourly check-in, and hire only the seats you need (see "Restart plan").
4. Tell the user, in plain words, US Eastern times, no emojis.

## User rules (all still hold; see CLAUDE.md and handover-lead39.md)
- **Everything ships ON** (the user, 00:38 UTC Oct 27): Step 5, the Veyli vessel, the ending; nothing built switched off.
- Keep the workforce small: no new hires unless a seat is the long pole; archive a seat as soon as its piece passes and its handover is pushed; replace, don't add.
- Full round of checks (six runners) before any game change is published.
- Tons of arrows, staged scenes with dialogue, works with a game controller. Phones first.
- **Talk only when close** (the user, ~01:00 UTC Oct 27): built by B3 on claude/talk-close (see below).
- Weekly usage: the old account was at its seven-day warning; keep the new one lean too.

## Links (owned by the OLD account)
A new account can't update these; it must publish new links (or the user shares edit access from the old account). Ask the user which.
- Playtest https://claude.ai/artifact/3HqM5XiXaHXzgrpq7JbesJ v7 = 0.93.3
- Dev https://claude.ai/artifact/9ZWAgqiZCvkJvVjjhjVkEr v7 = 0.93.3
- Promotion preview https://claude.ai/artifact/AvpWrMumcGiw4UYUpXd2X5 v1 (0.93.2-based, ?p5s5)
- The user's "current save" https://claude.ai/artifact/6daNCLCJAcsLCZn27CEthq v11 = 0.92.2 (never publish over it). Saves live in the browser per link: to carry the playthrough to a new link the user uses Download my save there, then Load a save file on the new link.
- Capabilities on the game links: {downloads}. Details: plans/handover-publisher-1.md on claude/publish-25.

## Code state
- **Live / integration:** 0.93.3. claude/integration = 3fd762cb (game ec93b94d...d085).
- **Combined build:** claude/staging-0.94.0 (BM18; see plans/handover-bm18.md there for the exact head). It merges: 0.93.4 fixes (workstep-tap-fix c79a66dc + b7e84f81 team-arrow, both RV20 PASS; week-guide-fix fa6b7de0 test only), Step 5 (p5s5-promo c3d36cde PASS, mech-a deefa61a PASS, mech-b 98460d79 PASS, m20 247420aa PASS, puzzles 6b07b624 PASS), vessel (claude/vessel 0340b6f9), ending (ending-crossing d1a61402 PASS + ending-checks 571b073f). **All switches still OFF** (cadet identical to 0.93.3).
- **Not merged / open:**
  - B3 claude/talk-close f52e2abc (talk only when close): checks green, RV22 review not done.
  - B3 claude/train-titles 7cbc1ad0 (lesson titles say "with Calder"): RV22 review maybe done (see handover-rv22.md).
  - VB1 claude/vessel 03b63d95 (game 705c6fc5): round-one fallback MUST + 2 shoulds FIXED by VB1 before the move; needs a reviewer re-check, then merge.
  - VB2 claude/ending-checks: RV22 verdict (see handover-rv22.md).

- **Combined build head at the move:** claude/staging-0.94.0 07e033c9 (last game merge 64a1ba76, game 958493d0...; switches OFF; cadet identical to 0.93.3). talk-close, train-titles and VB1 03b63d95 are NOT merged yet.
- **User answered (~03:10 UTC Oct 27): these older switches STAY OFF:** TRAY_TRAVELS (Pick-your-own breakfast tray already travels via P.trayGo, which is all the user wants), INTRO_ASK_ON ("Ask Zeke" stays parked), ZEKE_CABIN_MAIL (stays parked), PAD_ON (controller support stays off "until we update once content complete": turn it on in the update after the content is finished; keep building and testing every piece by pad on a switched copy as now). END_WAY_BACK stays off (ending answer). "Everything on" = P5_STEP5 and its sub-switches, EV_VESSEL_ON, EV_ENDING_ON (+ doors/visit already on).

## Restart plan (on the new account)
1. One reviewer: finish the open reviews above (talk-close, train-titles, VB1's fix, VB2 ending-checks) from plans/handover-rv22.md on claude/review-rv22.
2. One builder: fix whatever is still open (VB1's round-one fallback first), from the builders' handovers (handover-vb1.md on claude/vessel, handover-b3.md on p5s5-mech-b, handover-b3-m20.md, handover-b5.md on p5s5-promo, handover-vb2.md on ending-checks).
3. One build master (from plans/handover-bm18.md on claude/staging-0.94.0): merge the passed pieces, flip ALL switches ON (P5_STEP5 and its sub-switches, EV_VESSEL_ON, EV_ENDING_ON), bump the build (0.94.0), then the full six-runner round (plans/testing-guide.md; old check notes on claude/checks-cr1..6).
4. One publisher: publish to new links (or the old ones if the user shares edit access); tell the user.
5. Then Step 6 (not started; specs in handover-lead39.md).

## Backlog added this shift
P9 true move needs a second section 14 hook (B4-1); interactions_check.py:1262 SyntaxWarning; careerOff read live; perf blips (backlog 32) if they repeat; controller ring can't pick a person hidden behind another in a crowd (VB2); Tomas "Tonight?" Mail body shows function source (old, RV20); What's next sentences use first names (lead: fine).

## Seats on the old account at the move
All archived or idle with handovers pushed: BM18, PUB1, RV22, B3, VB1, VB2 (and lead 40). Archived tonight: EN1, B1, FX30, EN2, B4, RV21, B2, RV20, lead 39, B5, CR1-CR6.
