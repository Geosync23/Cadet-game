# Handover: RV25 (reviewer), 2026-10-29 ~07:00 UTC

**Role:** reviewer (took over from RV24 on 2026-10-28 11:27). Lead: lead 45 (session_01GKuymnu4NeXJhwPe21FWk7; leads 43
and 44 before). My session: session_01GKuymnnpKvNH4Ki69KEzwG. Notes-only branch `claude/review-rv25`; the full log and every
verdict is `plans/review-rv25.md`. Never change the game or push to builders' branches. Verdicts to the builder and the
lead, copy BM20 (session_01GKuymiwDEgkwGmjJ2nokvg) for merges. A second reviewer, RV26 (session_01GKuymjwVsweGh8p9EbTGHU),
took the 0.99 reviews on 2026-10-29 05:55 and takes RB1 from me now.

## State at writing: idle on lead 45's word (memory ~65%).
Open, handed to RV26:
1. **RB1's 0.98 render turns 3-4** (session_01GKuymkqMpME5GQvc5vTBqR): never arrived with me. Rule: pixel-identical
   (cadet_test 0 px, run alone), or a picture for the user first.
2. **BB1's FX8-1 swimmer-leaving look** (claude/backlog-triage, PASS sent; this look doesn't hold it unless a swimmer
   glides through a wall). plans/rv25-shots/swim_up.py: Day 6 14:00/16:00 and Day 7 10:00, deck 7, follows whoever gets
   up from a place with moves (kayak, float, ...), logs the drawn spot each frame, the biggest step and any wall tile.
   It steps frame by frame with drawing, so load goes to ~8: run it ALONE (it starved join_check twice).
3. **BAL2's new tip** (claude/balance-099; the user dropped the night-day retest so late players promote Days 29-30). My
   PASS on 2b46f96e and the code read of 12814bd6 (Dev arrow) are in the notes; the new tip needs a full re-review:
   cadet, career_check and --s6 (the late-Trusted dates), player_check, promo_beats, a code read of pu4OfferTick/pu4ResWhen.

## Verdicts this session (details in plans/review-rv25.md)
- EV1 visit-on a1917dd PASS (game 8c91437); visit-pointer 6db1cdd PASS; 6522974 PASS; fe11cd66 (tjFirst Saruth, p9 retry,
  vessel tip) PASS. My finds there: events_check slip, "two formal dinners" words, the join marker "Envoy" vs "Saruth".
- Sound: SD3 667ad05e chime (via the 0.96.0 round), SD3-2 music cache 0b9541c9 + fb603947 PASS, SD3-1 chime across
  reloads 5ba395a1 FIXES (note never cleared on New game) -> 7529b1e4 PASS.
- Dev mode: J4 c7489b5 FIXES (event arrow ignored evInvited) -> de25560 PASS; J2 93449f7 PASS; J5 86958252 PASS.
- PAD_ON perf question: no per-frame pad work without a pad; can't reproduce (noise).
- BAL2 2b46f96e PASS (then held by lead 45 for the user's change); BB1 0.99 backlog 167a07c4/e9637f54/564b8a50 PASS;
  OP1 3307e843 PASS (the join_check reload timeout is the box, 28.5 s on both builds).

## How I test
- Setup: plans/testing-guide.md section 2; /tmp/cadet-work and /tmp/cadet-work2 (two lanes). At most 2 browsers on 4
  cores: a third times out on page load (Page.goto 30 s), and a frame-by-frame drawn probe counts as two.
- Worktrees /tmp/rv25/wt-<name>; bases /tmp/rv25/old0970.html (0.97.0, 610ad7f1). Lanes as small bash scripts writing
  `name exit N secs last-line` to a done.txt, chained with `until grep -q "X END" ...`.
- Probes in plans/rv25-shots/: vis_play.py (visit days at 390x844 via Dev Set career, frames skipped between draws,
  clockPunch to clock in), vp_play.py / vp_gifts.py (pad play via controller_check's Run; QUIET hides #devHu: pass quiet=
  without it), j4_event.py, j2_list.py (Dev jump list), pad_prof.py / pad_time.py / pad_same.py (PAD_ON cost), vd_play.py
  (the Veyli dinner, Day 18), swim_up.py.
- Gotchas: in probes that exec controller_check, never name globals ST, log, D, play (they shadow its own: "game failed to
  start"); `a && b && (x) & (y) & wait` backgrounds the whole first chain (set up first, then start lanes); bash reads a
  running script as it goes (kill and restart a waiting lane, don't edit it); `timeout 60 git push`; *.png are in
  .gitignore (git add -f); never pkill -f with a name in your own command line.

## Open questions for the user
None from me.
