# Handover: reviewer R2 (stopped at ~70% memory, ~18:05 UTC)

# Handover: reviewer R2 (Pillar 5 Step 2, then playtest update 1 = 0.63.2)

- **Role:** reviewer. session_01DZoxp9pxhp63Wye1Kr2MsZ, branch `claude/reviews-p5-step2` (push only there). All verdicts are in `plans/reviews-p5-step2.md`, newest first. The "Passing tips" list at the top is the live state; "Failing / waiting on a fix" lists what's open.
- **Lead:** lead 13, session_015UkCGSS9FyGoBdkePhrKbC (took over from lead 12 at ~15:52). Lead 13's rule: send the lead **only FAILs, design calls, and a one-line summary when a seat's whole package is through**. PASS verdicts go to the seat and BM5 only.
- **Build master:** BM5, session_01DbBJ7iK6TrrADyEw7qbCsQ (claude/p5-cand-s2 for 0.63.1, claude/p5-cand-pt1 for 0.63.2). **BM5's session was inactive at ~18:05**: the P 587a2cd PASS didn't reach it, so ask lead 13 who builds 0.63.2 now and send them the tips list. BM4 is inactive.
- **Never** contact the user, start sessions, or push outside the branch.

## The job now: playtest update 1 (0.63.2)
Spec: `plans/brief-playtest1.md` on claude/lead-pillar1 (12b1b87); the user's answers there are binding. Base: 0.63.1 = claude/p5-cand-s2 cb7d30a. Review behaviour and saves in depth; lines and tests skim. Merge order (BM5): C2, X, P, O4, T, U, A5, W.

| Seat | Session | Branch | State |
|---|---|---|---|
| W head writer | session_013DdpJv4AKFJcvuBBqjSXms | claude/writer-p5 | **package through**: 6a00d9c (0.48.91) |
| C2 works career | session_014yREkgPvuwMyxBtoqB1P14 | claude/works-career | **package through**: a5d5c4c (0.44.14-0.44.16) |
| U HUD | session_01FcMPTX7mMTHkyr4pxDfNcS | claude/hud-pt1 | **package through**: 73b40cb (0.72.0) |
| X crew sim | session_01SNaWA6X5E9i2ZKfMnPTHJf | claude/crew-pt1 | 2223cb7 (0.71.0) PASS, 1 LOW (walk-ups into a washroom/toilet/shower). Still to come from X: the 13:00 tea for Works crew, the crew's 09:00 shift and breakfast 06:00-09:00 (MEALS), finishing work on time; plus the four game-code breakfast texts (menu-board canvas ~2403, Servery/Menu items ~5228/5231, servery-closed ~11313) → 06:00-09:00 |
| O4 onboarding | session_01MeEsh5sp4RyuD7KwdQEbLC | claude/arrival-0607b (→ onboard-pt1) | 7a2bc5d (0.42.48) PASS. Zeke's tea explanation and walk may still come (with X's tea and P's tea activity); O5 builds the Day 1 arrows and the call-home tip |
| T traditions | session_01X4SZJFeHprDF21NZqU5fGi | claude/traditions-pt1 | 1e254bd (0.70.0) **read, verdict not written**: waiting on 0.70.1 (T said a hash follows; SHIP.traces nameNew entries). Points to raise: Sunday dinner's extra tables going away afterwards (brief item; not in 0.70.0); Tomas/Rina as hosts change plans, so want day_check on a Sunday and a Mon/Wed/Fri; cadet_test differs only via the lap's content move (T: with 3 content lines reverted, ALL IDENTICAL); U calls `tradGoal(x)`, which T doesn't define (harmless). W's join texts say Lap of the Wren on Sundays: T has `weekday: 6` at 20:30 ✓ |
| A5 deck architect | session_01CHRbUTZc18m7eBck8eWhXj | claude/deck-pt1 | 1b41751 (0.47.4-0.47.7) **FAIL, item 1**: the beam's name planes are 3 mm apart (canvas .126, nameNew .129, nameYours .132). Fix sent: nameNew .132, nameYours .138. Re-check on the fix (read the two lines; deck_check) |
| P player | session_0153WUGRakJnNzUCNNHf1E8X | claude/player-p5 | **package through**: 587a2cd (0.28.74) PASS |

## How I test
- Setup in a fresh container: `pip install playwright`; `mkdir -p /tmp/cadet-work/three && cd /tmp/cadet-work/three && npm pack three@0.128.0 && tar xzf three-0.128.0.tgz`; then `export CADET_WORK=/tmp/cadet-work CADET_CHROME=/opt/pw-browsers/chromium`.
- Per piece, in a scratch folder: `git show <hash>:starship-cadet.html > new.html`, `git show cb7d30a:starship-cadet.html > old.html` (the 0.63.1 base), and the checks from the same hash. Run cadet_test plus the piece's own checks (career/leave/mech/machine for C2, social/day_check for X, interactions/device for U, clothes for O4, join/events for T, deck_check for A5, player/interactions for P). Text: `D=$(mktemp -d); git archive <hash> | tar x -C $D; cd $D && python3 content_gen.py && python3 lines_check.py`.
- **One browser job at a time.** Two at once made cadet_test show a false text-shift on the top buttons; re-run alone. Chain them in one background command, or wait on an output file with `until grep -q ... file`. Never `pgrep -f` in a loop.
- `rm -rf` on a glob after `cd` is blocked: use a fresh `mktemp -d` folder instead.
- A seat's own commits on a branch that merged a candidate: diff from the commit's parent (`git diff <hash>^ <hash>`), or from the base where the branch started.
- Mechanics needing A's places (the drill) only run on a scratch merge with A 6cc826b; only the build-number lines conflict.

## Step 2 (0.63.1) is done
Every Step 2 piece passed (see the tips list): S 0e18118, P f2156f1, C 8cc07a5, O4 96649fe, M1 ec9b498, M2 c9b211a, W ac60c8d. Open LOW: M2's incidents should skip promotion days (Step 3).

## Arrived after I stopped (18:07)
- A5: the fix for item 1 is 0.47.8 **56db3dc** (nameNew .132, nameYours .138, beam names .126); branch head ff26b6d merges the final 0.63.1 a9fad20 (A5: player_check OK, deck_check OK). To do: read the two z values, then PASS and update the tips list.
- X: the washroom LOW is fixed for 0.71.1 (`seekPrivate()`); the hash comes with 0.71.1.
