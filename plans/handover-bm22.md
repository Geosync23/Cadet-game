# Handover: build master BM22 (session_014zyJYNgBPdEPHLxTGrM889)

Written 2026-10-31 ~14:30 UTC at about 58% memory, in the middle of 0.99.5 (all pieces merged and gated one by one;
the switch-on commit, build turn, gates and round are next). Before me: plans/handover-bm21.md (claude/handover-bm21).

## Who
- Lead 47, session_014zyJYM4mt9ZDCD5H9JZDtN (claude/lead-47). Reviewers: RV28 session_014zyJYQKwGvytfCGdrWMoiZ,
  RV29 session_014zyJYM3D7UBkZN49CsZVuA (JB2, PL2, CT5, TB4), RV30 session_014zyJYNFR7ewWJGvEQNUAHr (SD5, OB2, TB3, words).
- 0.99.4 runners (done): R1 session_014zyJYQ4EiB7CipGp4HsYV8, R2 session_014zyJYMsL5YqKnLb9Q6Lvyz,
  R3 session_014zyJYPN2WU6wpJgghsXiAe, R4 session_014zyJYNRijQBB389vXWxWNJ. The lead hires 0.99.5's runners.

## 0.99.4 (done, waiting for the user's OK to publish)
claude/staging-0994 596712bc (round record on 8976965e), game a01d1a4c7864801b19541d70b9358089fba1ed84cee5145ca85931ea3012bc4a.
= 0.99.3 57eceec4 + ST1 crew stories stage 2 df5057d (RV28) + STORIES2_ON = true + build 0.99.4. All five shares OK.
Lead verified, fast-forward from integration OK. Never publish; never push integration/main.

## 0.99.5: claude/staging-0995 (from 596712bc), state at handover
Every piece was built on 8976965e and merged --no-ff at its reviewer's exact PASS commit, each gated (verify_merge,
names, check_fast, area checks, cadet vs the previous tip ALONE) and pushed:

| Merge commit | Piece (PASS commit, reviewer) | Gates | cadet vs previous tip |
|---|---|---|---|
| 12eddbce | JB2 jobs + SW4 tour words, claude/p995-jobs 1e056bd (RV29) | check_fast, machine (5z), career, day 2, mech whole (round23) | 3 shots differ only in Oona's bubble ("washer's fixed" -> "Water tastes right again": JB2's F1, the scanner's first job is a pump); state identical |
| fd0078f7 | PL2 player, claude/p995-player 6b2f135 (RV29) + backlog PL2-1 | check_fast, player, talk, social | ALL IDENTICAL |
| f2ce55ef | CT5 controller, claude/p995-controller 7c6c2477 (RV29) | check_fast, controller deck/settings/base, pick/pick1 | ALL IDENTICAL |
| 2b0908e9 | SD5 sound, claude/p995-sound a5ce274 (RV30; not ec312a9) | check_fast, sound whole (hide/mess_scale/long), title | ALL IDENTICAL |
| 281d1012 | TB3 traditions, claude/p995-traditions 4037a26 (RV30), switch off | check_fast, join, events, p926, day 2 | ALL IDENTICAL |
| a5bc51af | OB2 onboarding, claude/p995-onboarding fb81b79 (RV30) | check_fast, device whole, intro --dinner/--firsts, appt | ALL IDENTICAL |
| 5ad18a0c | SW4 milestone words + Mails on TB3, claude/p995-traditions-words 52ea327 (RV30) | check_fast, join, events | ALL IDENTICAL |
| 322552de + c2c83483 | TB4 claude/p995-trad926 bd0fa61 (RV29; includes SW4's eight-card words ef310be), TRAD926_JOIN_ON off; + backlog RV29-1 | check_fast, join, p926 | ALL IDENTICAL (switch off) |

Not taken: PL2's docs commit 4de9da1 (handover only); 181d86a/fac5e56 (superseded by 52ea327). TB5's follow-up on
4037a26: only if passed before the switch-on commit (lead 47); otherwise left out.

Game at the handover tip: d8828a090e042bea1b6db5d9e7b15010df06e3341738b27515a058dc742601db (all switches of 0.99.5 still off
except JB2's three). TB4's design-doc merge: the "Joining in" paragraph was hand-combined (TB3's list and two-leaders note +
TB4's eight); verify_merge lists both old versions of that one line as MISSING: expected. Small docs fix for TB4/SW4 (not
done on the side): that paragraph still says "The words are stand-ins until a writer's", but SW4's eight-card words are in.

## Next steps (in order)
1. TB5's follow-up on 4037a26: only if RV30 has passed it by now; otherwise go on without it (lead 47, 14:02).
2. **Switch-on commit** (one commit, the lead's and the user's decisions):
   - `const SND_LONG = true`, `const MESS_SCALE = true`, `const SND_BUF_ON = true` (section 27; SD5, ~line 74000; they
     are `const ... = false;` lines with a comment, flip only the word).
   - `const TRAD995_ON = false || URL_FLAGS.has('trad995')` -> `true || ...` (TB3, ~line 9755).
   - `const TRAD926_JOIN_ON = URL_FLAGS.has('trad926');` (~line 49156) -> `true || URL_FLAGS.has('trad926')` (TB4).
   - JB2's JOBCAP_ON, SPREAD_ON, CHECKS_ON are ALREADY true in JB2's branch (nothing to do).
   - design-doc.md in the same commit: the user's pick 2026-10-31 (Mess Hall Murmur page, via lead 47): MESS_SCALE ON
     (the proposed murmur) and SND_BUF_ON ON. Move the Open questions entry "Mess hall murmur, note 4 (SD5, 0.99.5)"
     (~line 993) into Answered with the date and the pick; in the sound section (~line 880, "Long sessions") say
     SND_LONG and SND_BUF_ON are on, and in the mess hall paragraph that the murmur follows the count (MESS_SCALE on).
3. **Build turn**: header `build 0.99.4` line (~380) and `GAME_BUILD = '0.99.4'` -> 0.99.5; DEV_NOTES paragraph on top
   (0.99.5 = what's in, as in the table above) with 0.99.4 marked published once it is (ask the lead); build-table row.
4. **Gates on the switched-on candidate**: names, check_fast, sound_check whole (the lead asked), events, join, day 2, 9, 16
   (TB3's days), stories 36, machine, mech, then cadet vs 0.99.4 (a01d1a4c...) ALONE: expect differences where the
   switched-on pieces show (jobs bubble as above, traditions spots/seats, onboarding); explain each in the build-table row
   (make a diff picture of differing shots: only the changed area should differ).
5. Push, GO to R1-R4 (the lead hires them; plan below) with commit, game sha256, OLD = 596712bc (a01d1a4c...), what changed.
6. R5 share, then the docs-only round record, final GO to the lead.

## Round plan
plans/round-0995.md on claude/staging-0995 (lead OK'd): round-0994's shares + day 2, 9 (R1), intro --dinner/--firsts (R2),
device whole + day 16 (R4), day 3 (R5); the builders' new checks by share. Add TB4's join/trad926 checks if any (R5,
beside join). stories always `36`. player_check Saving and devmode "real" can flake once (backlog BM22-2/3): rerun first.

## Tools (in plans/build-master/, copied from my scratchpad)
- `run1.sh NAME LOGDIR WORK cmd...`: one check, appends `| name | exit N Ts, last OK/FAIL line |` to LOGDIR/summary.md.
- `gate.sh WT LOGDIR OLD.html "name:cmd BUILD;..." "name:cmd BUILD;..."`: check_fast alone, two lanes, then cadet alone vs OLD.
- `keepboth.py FILE`: resolves table-row clashes (ours, then their rows with a new first cell; drops their stale copies).
- `r5.sh WT LOGDIR`: my R5 share (check_fast alone, two lanes); add day 3 for 0.99.5.
- Setup: pip install playwright numpy pillow; three r128 + acorn 8.12.1 in /tmp/cadet-work (testing-guide 2).
- Run long things as `setsid nohup bash script ... &`, wait with one background until-loop; never change the worktree
  while checks run in it; at most two browsers.

## Gotchas
- verify_merge must run AFTER the merge commit (before it, HEAD is the old tip and everything looks missing).
- Every piece's branch carries an older copy of the 0.99.4 build-table row: keep ours (with the round record).
- A tool-generated FAIL list in the appointments check ("FAIL planted ...") is its self-test: fine when it ends OK.
- lines_check: 112 warnings is normal (same on 0.99.3).
- cadet_test differences: diff the PNGs (A_*.png vs B_*.png in the log folder) and look before explaining.
