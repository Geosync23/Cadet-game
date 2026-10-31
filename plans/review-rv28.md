# RV28 reviews (crew stories stage 2, 0.99.4)

Reviewer RV28, session session_014zyJYQKwGvytfCGdrWMoiZ, branch claude/review-rv28 (notes only). Lead 47
(session_014zyJYM4mt9ZDCD5H9JZDtN). Builder ST1 (session_014zyJYMy3rmgW9Tv5brJfkM, claude/stories2-st1).
Base: claude/integration 57eceec4 = 0.99.3, game sha256 04c821fe...c2a9 (verified in my base worktree).

## Prep (2026-10-31)
- Tools: playwright 1.64.1 (pip), numpy, pillow; three r128 + acorn 8.12.1 in /tmp/cw-w1, w2, w3 and /tmp/cadet-work;
  CADET_CHROME=/opt/pw-browsers/chromium.
- Read: handover-rv26, review-rv27, handover-fx21, design-doc "Crew stories", TEAM.md tail (lead 47's decisions 1a-5a),
  section 20c's crew stories slot (stage 1), SW4's tomas.arc (af107ba / 4007550).
- Words notes from reading tomas.arc before the build (to check against what ST1 baked):
  beat 8 says "Theo went up this ramp this afternoon": true only if Theo's farewell is Day 21 in the shuttle bay (it is, 14:30).

## ST1 claude/stories2-st1 52bbd91c (game 25d7d426...e84a, verified), from 57eceec4
- cadet_test vs 57eceec4, run alone: ALL IDENTICAL (it plays Day 0-1 only).
- **B1 (blocker, sent 03:58 UTC)**: storyCastGoes's `return` is inside a // comment (line 54677), so it always returns
  undefined. That's stage 1's planner hook, live in 0.99.3 (STORIES_ON true), read by section 18's evArrive. Switch off is
  NOT 0.99.3: probe plans/rv28-probes/castgoes.py: storyCastGoes('captains-address','kovac-zainab',19/26) true/true ->
  null/null; Day 26 Kovac at ev-captains-address 15:43-17:05 on 0.99.3, on Deck 3 (callhome, leisure) on 52bbd91c. With
  the switch on, Raman 5 (cometScope) and Zeke 6 (knit-and-natter) lose the hook too. Fix: return before the comment, and a
  stories_check part 1 row for storyCastGoes on Days 19 and 26.
- Code read (the rest):
  - storyPlanBeats is pure (STORY_MOMENTS2, DECKS, schedPeople roster), laid via introPlan; Tomas Day 21 17:45-17:55, Kowalczyk
    + Mensah (act work, ride tagged round) Day 24 05:35-06:00, Calder + Halloran + Zeke Day 26 18:40-19:05, every game.
  - storyIdx / storyCastGoes / STORY_TAB re-made once section 22's tables are there: fine.
  - storyDone's afterglow skip, STORY_PAIRS, cday as 'id:beat' while on (old saves have 1): fine. No new saved shapes.
  - **F2 (fix suggested)**: storyDayHeld holds the day for another story's exact-day crescendo even when that one can't
    happen: Calder 5 needs myrank:specialist; slower players are Engine Specialist on Day 26-30 (design-doc 658). A
    non-specialist whose Calder story is at beat 5 then loses Kovac 4's Day 26 chance (if Day 19 was missed) for a
    scene that won't play. Same shape for Raman 5 (tier 3) vs Pell 7 on Day 22, Kowalczyk 4 vs Pell 7 on Day 24. Suggest:
    hold only while the holder's gates pass now (storyGates at its slot), or ask lead 47.
  - Note: lineCond myrank reads SHIP.works.rank raw; playerRank() (section 17) validates it. Not blocking.
  - Note: storyDoorOpen runs inside bridgeBarred, which bridgeTick calls per edge each sim step on Deck 1; at night it loops
    every story person's momentNextId. Switch-on, Deck 1 only. Not blocking unless perf shows it.
  - **Q3**: "leave your night shift 20 min early with no penalty" (lead's 1a): nothing in the diff handles it. To measure
    in the Kowalczyk probe (does leaving at 05:35 cost anything?).
- Words:
  - Stage 2 .arc lines = the writers' .story lines, except ST1's additions: Zeke 6 "Engine Specialist. You. Today..." (day:23
    myrank:specialist), Calder 5 "One true sentence first..." (mem onesentence from beat 3), Kowalczyk 5 "You asked if the
    Wren could answer it..." (flag from beat 3's choice); Raman's Sato line given to Mori (lead 47's 3a). In voice.
  - **F4**: Calder 5's first line "Four weeks. Mugs down a minute. Not you, Pell. You can hold yours." plays always, but Pell
    is no longer in cast or planned (52bbd91c: only his own line is `if here:pell`). She talks to someone who isn't there.
  - Note: design-doc says Tomas's scene 17:35-17:55; built at:17:45-17:55 (after Basil is down at 17:43). Doc to match.
    Zeke's line "Ramp's opening" and Basil's first-sight lines then play two minutes after he's down: small, not blocking.
  - Note: Tomas 8 when: beat:tomas.7 is met by rel.arc when 6-7 ran out of days (stories_check play: told 5, 8; 6, 7
    skipped); the invite then says "Holt wrote it in pencil" (beat 7's news, never heard). Small; writer's call (SW4).
