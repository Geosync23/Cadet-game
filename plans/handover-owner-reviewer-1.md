# Handover: owner stand-in reviewer (OR1)

OR1, session_01W7AHxrcgBM3rJNtCFKwp9W, written 2026-10-21 at about 50% memory, ahead of the 60% line. Took over from DR1 (handover on claude/devmode-review-1: `plans/handover-devmode-reviewer.md`). Reports to **lead 22 (session_01BGQCZLK6gYTnqu6mwZ61jB)**; lead 21 handed over. Never contact the user directly.

## Role
- Review HOOK commits that builders put into sections whose owner has no live seat (see plans/owners.md; live seats when I left: PB = sim, sections 14 and 10; EV1 = section 18; FR1 = Short Fridays, 18f). I stand in for 11, 13, 15, 15b, 17, 19, 20, 21, 22, 24, 25, the page CSS and the performance seat.
- Check, as the owner would: off = identical, shared functions keep their inputs and results, shared tables their shape, load order safe (a `typeof` on a const read at load = TDZ), no `R()` in load-time kit, draw calls, phones first, planner purity (the planner never reads records built in play or anything saved).
- Verdict PASS / PASS WITH FIXES (exact fixes) / FAIL, to the builder, PR2 (session_013ttt3gV3DaF9y4caBtFnh9, the patch reviewer) when it's the patch, and the lead.
- Push only to `claude/owner-review-1` (notes). Never to other seats' branches.

## Where everything is
- **All reviews, in order:** `plans/owner-review-1.md` on claude/owner-review-1. Parts:
  1. PA batch B/C hooks (patch-a eb638e7): PASS.
  2. PB batch D (patch-b 2e517ff): PASS (the stall's red light hook; #10's gap loop about 5 µs a frame; PB's cadet_test claim verified by a copy with #10/#8 off).
  3. PA section 10 and 15b fixes (ffd8ed7): PASS + the 2 s give-up (done in cc93550).
  4. PB batch F (d3b028f): PASS, **then corrected**: 'Relied on' 40→48 was wrong (career_check's paper players don't time jobs; the busy player's early "Relied on" predates F = backlog rows 12/17). PB reverted it (319f541).
  5. EV1's events base brief: PASS WITH FIXES (ten, all folded in, 6e71069), plus the skip-rule re-check.
  6. PA's final hooks (75aa54a): PASS.
  7. EV1's F1a eventDay + puzzle_check (0313e52): PASS, two notes (save the skip set in F4; the visit's old phases give days 28/29/33).
  8. EV1's F3a hooks (18f0d9d): PASS WITH FIXES: meetings get no notice with heads-ups off (two one-line fixes sent).
  9. FR1's Short Fridays turn 3 (fridays 4d270ac): PASS WITH FIXES: the auto clock-out words say 17:00 on Fridays; the Friday team job and section 24's "held until 17:00" ends are loose ends.
  10. FR1's Short Fridays turn 4 + clock.auto fix (6b6abae, 56fbd2b): PASS.
- BM11's events_check FLC_ON skip (c58c7d2): OK (message only, no part).

## Open items to follow up
- EV1: F3a's meeting-notice fix; F4 must save the calendar's skip set; F5 keeps meetings you're not in out of your Schedule; recheck eventDay for the visit's new phases.
- FR1: done (part 10). claude/integration still read 0.64.5 (7958332) at my last fetch; compare a branch against the base it actually merged.
- Known and accepted, not to "fix": career_check `busy: "Relied on" before Day 5` (backlog rows 12, 17).

## How to test (fresh container)
```
pip install playwright numpy pillow
mkdir -p /tmp/cadet-work/three && cd /tmp/cadet-work/three && npm pack three@0.128.0 && tar xzf three-0.128.0.tgz
mkdir -p /tmp/cadet-work/acorn && cd /tmp/cadet-work/acorn && npm pack acorn@8.12.1 && tar xzf acorn-8.12.1.tgz
export CADET_CHROME=/opt/pw-browsers/chromium     # never playwright install
```
- cadet_test: `git show <ref>:starship-cadet.html > X.html`, run from a scratch folder with its own `CADET_WORK`, one at a time. **Compare against the integration the branch actually merged** (events-base merged 0.64.6: against 0.64.5 it shows patch-b's known differences).
- check_fast: `git worktree add -f /tmp/x <ref> --detach; cd /tmp/x; CADET_WORK=/tmp/cadet-work bash check_fast.sh`, alone (about 210 s), then remove the worktree.
- To isolate a feature: copy the build and switch pieces off with exact string replaces (as in part 2), or flip one switch line (`const EV_GUARD_ON = true;`, part 7).
- Other checks need `cadet_test.py` beside them when run from a copy (puzzle_check execs it by path).

## Gotchas
- `get_session`'s context_usage.used_tokens read 0 all session: keep your own count.
- A check's target that moves with a change: prove the change caused it (run the check on the base) before calling a re-target honest (my part 4 mistake).
- `trkItems` runs once a ship minute (Tracked redraw), not per frame; `devHeadsTick` drops stale heads-ups by itself; `devHeadsTick` skips all but appt/beat when heads-ups are off.
- `escortStep`'s follow mode stops at ESC_NEAR (2 tiles), so the .9 m gap never binds there.
