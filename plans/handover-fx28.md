# Handover: FX28 (promotion beats), 2026-10-26

**Role:** builder for the promotion beats (the user's playtest notes, 2026-10-26: the Tier 2 test and promotion "very very
hard to miss"; lead 38's plan A-G). Lead 38, then lead 39 (session_019V68fz33UFv4cK5Z4iCDvi). Reviewer RV19 (PASS on
44a4565), words SW2, build master BM18.

**Branch and builds:** `claude/promo-beats` from claude/integration b957b92 (0.93.1). Final tip 44a4565 (HUD 0.93.2-p.1,
game sha256 e88aadfe...3575). Merged and released in 0.93.2. Nothing unpushed.

**What I built (all in 24p's slot, behind `PROMO_BEATS_ON`, which needs `PROMO_SIGHT_ON`; off = 0.93.1 exactly):**
- Before the test: crew bubbles in the bay and at meals (pb.soon by days aboard, pb.luck from friends), two friends'
  luck Mails at 20:00, the morning notice, Calder's word in the bay; Schedule/Tracked rows (promoBeatsItems via devDay).
- During: the board's ring on the test's Take it forced past Teaching arrows Off and named (promoBeatsPtr, `force` in
  section 19's pointAsk); the test's world arrow level 1; a notice once an hour if you hold another job; passers-by;
  Torres's line at the end; Calder's "There it is" at 09:00, once.
- Passing: the result held; Calder's word, Mail and notice name the result's day and 08:15.
- Result: next workday 08:15 in her office (PB_TIMES; promoBeatsApply swaps PROMO and OCCASIONS.promoSummons, script
  promo.result); Mail 06:00, notice, level-1 arrow; she comes out to you anywhere but her office at 08:30; Mail by 09:15.
- Pip: the Captain the same day 16:30 (17:15 Fridays) via promoCerTimes; cake after it (promoCakeWin).
- Cabin: the walk after your dinner (flag pb.ate, out of the mess) or 20:00; she comes to you first (W.mv.met), then leads.
- Details and the hooks in other sections: DEV_NOTES "The promotion's beats"; design: design-doc "The promotion's beats".

**Words:** content/works/promo-beats.lines, content/banks/promo-beats.lines, Calder's `flag:pb.promo.*` lines,
content/meetings/promo.result.meet (SW2 polished). Mail keys are `mail.pb.*` (the 400 limit); placeholders {time}, {day}.

**How to test:** `python3 promo_beats_check.py BUILD [off pointer before passed result cabin talk review]` (about 2-3
minutes). promo_sight_check's move part runs with the switch off; career_check, mech_check and devmode_check expect the
new times when the switch is on.

**Loose ends:**
- backlog FX28-1: career_check "busy: Relied on before Day 5" fails on 0.93.1 too (not looked into).
- RV19's S2 (accepted): the pip's seek fires 15 minutes after the start and the room's booking closes at its own length,
  as in the old flow. Extend the booking if a later playtest finds players miss it.
- bigevents_check's EV_BEATS table still lists the old fixed-day promotion beats (estimates; the events base owns it).

**Gotchas:** a `// comment` pasted mid-line in a check's JS string comments out the rest of that line (use /* */).
Stepping frames after a backward clock jump can drop the reserved test job (backlog BM18-2): draw the pointer with
pointFrame() instead. In wait loops, `pgrep -f day_check` matches the loop's own command.

**Open questions for the user:** none (the result and same-day pip were decided 2026-10-26 05:08 UTC).
