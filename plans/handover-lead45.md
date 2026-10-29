# Handover: lead 45 -> lead 46

## START HERE (next lead)
Read CLAUDE.md, this note, plans/roadmap-1.0.md on claude/lead-44 (the user's road to 1.0 and decisions), then the bottom
of TEAM.md on claude/lead-45 from "LEAD 45 started". Lead 45 = session_01GKuymnu4NeXJhwPe21FWk7 (~54% memory at
~10:00 UTC Oct 29). Session chain depth is 4 of 8: the USER starts lead 46 from claude.ai (don't create it from a session).
Lead 45's hourly check-in: trig_016UAJtPjwFezry8dEDiEpBK (53 * * * *). Make your own (copy its prompt) and disable it.

## State (~10:00 UTC Oct 29 = 6:00 AM ET)
- 0.97.0 LIVE: Playtest https://claude.ai/artifact/7hQ14AcwZHCi5EvL1AKiMU v4, Dev https://claude.ai/artifact/KEyaHvon6ZaVHHFRdAe18m v4.
  claude/integration = 610ad7f1. NEVER publish over 6daN (the user's save link).
- 0.98.0 (game speed on phones): candidate claude/staging-pad (7a2ae7d2 game, now 10865180 with check-only fixes),
  game sha256 22f8939d...918f = SD3-2 music cache + OP1 walk-time fix (FX24-2/FX12-1) + RB1 turn 3 (one draw per body,
  0 px; calls 173 -> 142) + join_check timeout. Round 07:38 UTC: R2, R4, R5 OK; R3 s5cases and R1 puzzle p6 = check-only
  (fixed, RV26 PASS). R1 arrows step6 = real OLD latent gap in 28a (p5nGuide needs S.day; Day 22 not clocked in -> no
  day-sleep arrow). Plan: (a2) OP1 fixes it (~60 min, RV26, targeted rerun) else (a1) at ~11:00 UTC ship with it as a
  known old gap + backlog row, fix in 0.99. BM20 finishes 0.98 only, then GO -> ask the user's OK (push) -> PUB2 publishes
  over 7hQ1 + KEya -> lead fast-forwards claude/integration (git push origin <sha>:refs/heads/claude/integration).
  Hedge claude/staging-098b (no walk fix) no longer needed.
- 0.99: claude/staging-099 (now BM21) de05b965 = SD3-1 room B chime, EV2 seated formal dinner (V-1/V-2), BB1 26 backlog
  fixes, TB1 title screen B switched ON + SD3 title music (track A provisional), + 0.98 walk fix. Title preview for the
  user: https://claude.ai/artifact/GLSzgGfn55Kk9LFCaoGevR. Left, waiting on the USER:
  1. BAL2 claude/balance-099: 7dda61e3 "drop both" (slow players Engine Specialist Day 29-30 as the user asked; BAL2
     recommends) vs 12814bd6 (Friday same-day result kept: slow players Day 26-27). The user said yes to (b) earlier and
     then asked for 29-30; the two conflict.
  2. RB1 turn 4 claude/opt-098-render 44e6e0c (furniture colours merged: mess 142 -> 85 draws; 14 of 267 shots differ by
     1-8 px at same-depth corners; picture plans/opt098-rb1/turn4-before-after.png sent to the user). Parked unless OK.
  3. Title music pick: https://claude.ai/artifact/XwWvqkL7EdMouqrJ3cRHYm (ArtifactData list collection picks, doc title);
     then SD3 sets SND_TITLE (one line).
  Then BM21: 0.99.0 build turn + full round (5 shares, OLD = 0.98.0), user OK, publish.

## Seats
Working: BM20 session_01GKuymiwDEgkwGmjJ2nokvg (63%, 0.98 finish only), BM21 session_01GKuymkAoLNTFXef9RgiYLn (0.99),
OP1 session_01GKuymkG9JWDcSK9pMb28aj (28a fix; ~55%+), RV26 session_01GKuymjwVsweGh8p9EbTGHU reviewer (~36%),
RB1 session_01GKuymkqMpME5GQvc5vTBqR (turn 4), runners R1 AS1 session_01GKuymmdgtDvbd8P7URXd4z, R2
session_01GKuymmiqCTVdUwF2rf5qBM, R3 DM2 session_01GKuymoBtAFGaak9qYYXS24.
Idle: PUB2 session_01GKuymkDxLVyt4rjtcJxdab (publisher), BAL2, SD3 session_01GKuymir9eBj7X6kLtwLRmq, TB1
session_01GKuymo2ikX7y7GA88GPXQP, EV2 session_01GKuymn7YSDpEbeNYGxup6N, EV1 session_01GKuymmJANJaZkFuhsM9bBt.
Handed over (idle, notes pushed): RV25 (plans/handover-rv25.md), BB1 (plans/handover-bb1.md), OP1 (plans/handover-op1.md).

## Gotchas learned tonight
- *.png is in .gitignore: builders must git add -f screenshots.
- The walk-time fix changes crew plans, so machine wear and which case opens on a day move (deterministically). Checks that
  hardcode a day's machine/suspects break; fix the check, not the game.
- join_check's reload takes ~28.5 s on busy boxes; now 120 s.
- Seats misreport memory; check get_session context_usage yourself.
- Don't run more than two browsers per container; page loads time out.

## User decisions tonight (also in TEAM.md)
Balance GO on all four needs numbers; Friday same-day result yes, then slow players Day 29-30 (conflict, asked); title
defaults kept (Saves on menu, no tap gate, no Back to title); V-1 dinner plan approved by lead; 0.98 = turn 3 only (lead
call for speed; turn 4 to 0.99 picture-first).
