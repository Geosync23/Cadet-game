# Review log: RV22 (vessel + ending reviewer, replacing RV21)

**Role:** reviewer for "A Veyli vessel needs help" (EV_VESSEL_ON), the ending's checks (EV_ENDING_ON) and B3's M20
shoulds. Lead: lead 40 (session_01NXybH7NNqM8M4ngiyidq6m). Notes-only branch `claude/review-rv22` (from
claude/review-rv21 aa8bce7b); I never change the game or push to builders' branches. RV21's full log and verdicts:
plans/review-rv21.md. Verdicts PASS / FIXES NEEDED (must/should) with the exact sha to the builder and lead 40.

**Builders:** VB1 session_01UsjGN26E88zwrNPWwef4iT (claude/vessel), VB2 session_01KRBGtugjBpv5iGcV5WDvCP
(claude/ending-checks on d1a61402), B3 session_014FBmsiTsA9QymoN2qt4NyL (claude/p5s5-m20).

## Queue
1. VB1's next claude/vessel push (now 5f199dd4, handover only): RV21's open shoulds, VB2's 3fb8eac7 merge, arrows_check
   vessel part, controller presets. Re-run bigevents, events, day_check 27-30 on an ON copy; cadet off identical; phone.
2. VB2's claude/ending-checks (not pushed yet): arrows_check endstay/endgo, controller presets, day_check 31/50 ON copy.
3. B3's claude/p5s5-m20 after f57afcbc: m20 checks on an ON copy, teacher name, Tracked row, in person before 06:20 Mail.

## Verdicts
| Branch | Piece | Verdict | Sha |
|---|---|---|---|

## Log
- 2026-10-26 ~23:30 UTC: started; told lead 40, VB1, VB2, B3. Test kit in /tmp/cadet-work and /tmp/cadet-work2. No new
  pushes on the three branches yet.
- ~23:36 UTC: VB2: ending-checks not pushed; stay path (asis, teachoff, track) passing locally; change-of-mind, go runs and
  controller_check `ending` still in trial. Will send the sha, then day_check 31/50 ON copy.
