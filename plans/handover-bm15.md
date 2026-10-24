# Handover: build master BM15 (session_01EH5qkoYriK2Gsrp7hHRoso)

Read this first if you take over as build master (BM16). Older notes: `plans/handover-build-master.md` (BM11-BM14) on claude/integration-next.

## Who

- Lead: **lead 33**, session_014VXwRc3QfqM3cgp1w6VJah (branch claude/lead-33). Earlier: lead 31, lead 32.
- Publisher: **PUB1**, session_01GnpjFR6oumvuvTrmcXSqeg. Give it the commit and the full game sha256, and the switches.
- Check runners: CR1 session_01CsWNjCsy8u5mrHJgTVgCst, CR2 session_01BgMQaB1LQmhfU1rSJ2ATvv, CR3 session_016oCbvvzgcqzzCTsBFCkYRB, CR4 session_01636CfY2MhB3DzrzZ59dhXz, CR5 session_01CHoEsvv7zMPZDr1ir7uAiz, CR6 session_01B1FwE5sMmHnMPWsGn23nrk.
- Reviewers for 0.92.3: RV11 session_01EdBKAgQFMexMSs3JbgH5H7, RV12 session_013JmdoWWEDQde8y1bwrMGnY, RV13 session_016ioWtxM6NJRV4Ck3ADwozc.

## FINAL 0.92.3 CANDIDATE (read this first, BM16)

- **Candidate: claude/staging-0.92.3 0dd4e2e2** (build 0.92.3; build-table row with `Checks: FULLROUND |` as the placeholder; DEV_NOTES line 5 says "in its full round").
- **Game sha256: 4e6538447d13e4c5398fc74844748e1e9d41776afa7bcc83bc99d5eff87cd0a2**
- **OLD = 0.92.2, claude/integration 364c80cb** (game sha256 ca2f908d…e7e4).
- All 0.92.3 pieces are in (all 29 items but 11, a pitch page for the user). After the list further down: AC3 aee83840 (6), FX8 9fd5b500 (22, 28), FX4 97251620 (2, 12, 14, 20, 26; 7 content/lines files clashed with item 15's frames: both appended, kept both), FX12 da1825d2 (19, 27; a design-doc paragraph merged by hand with DV1's edit), DS1 b49a01db + 872d3c2b (1, 7-10), FX10's arrows_check follower fix b75dcf81 (cherry-picked alone), FX10 1bd0a34e (21, 24, 29). Words baked: 11321 lines.
- My checks on 0dd4e2e2: check_fast OK; cadet_test vs a58a154f (all but FX10) ALL IDENTICAL; vs 0.92.2: every shot differs by the wider "Schedule tracker" HUD button, taps 1-2 read "Missing people" not "Bursting" (FX9's faster social), no page errors: both expected; lines_check PASS 0 errors (49 warnings); `arrows_check week guide` OK (m6 Day 9). Earlier on a58a154f: intro_check OK (DS1's part 19, DV1's part 18).
- `claude/integration-next` is still at 364c80cb's line; fast-forward it to the candidate (check it's a fast-forward first) before the round.
- **Round extras** (lead 33): CR1 also runs `arrows_check.py BUILD week guide` on NEW and OLD (backlog 15: OLD fails at Day 9 m6, known-old; NEW must pass now with the follower fix). machine_check FAILs on OLD on purpose for notes 21/24 (FX10's new lines, RV13's ask): expected on OLD only. intro_check part 12's new-game click has flaked (also on OLD; RV11): rerun once before calling it. Known-old list: backlog 12, 14 (lead 33), and 23, 32 (a one-off perf frame-time spike; re-measure), KP1 (Line ceremony 335 draw calls).
- **Publishing: 0.92.3 goes to NEW Playtest and NEW Dev artifacts (the user, 04:07 UTC); the Version 11 pages stay untouched.** PUB1 has the instruction.

## Builds I made

| Build | claude/integration | Game sha256 | Notes |
| --- | --- | --- | --- |
| 0.92.1 | e03505fd | 2dbb11b8…59b18c | Crossing the Line ON; round found 2 FAILs from the Line, both test-only fixes (FX6 m8 54efee21, arrows-week e1f1ec97). Published Version 10. |
| 0.92.2 | 364c80cb | ca2f908d…e7e4 | team-restore, mess-taps, solo tap, day0-sim, relay shelf, tray-seat, controller check fixes. Round clean. Published Version 11. |
| 0.92.3 | in progress | | the user's 29 playtest notes (`plans/patch-0.92.3.md` on claude/lead-32) |

## 0.92.3 state right now

Staging branch **claude/staging-0.92.3**, tip **2cd2d897** (game sha256 e19524be8e666653429ed9d8ea20fbfbd3352b0592f51852e1d09f2d9c7b2dad). Every step got cadet_test against the step before plus its area checks.

In, in this order:
1. f085bcbe DEV_NOTES "where things stand" (0.92.2 live, 0.92.3 next).
2. 5b6f1d34 FX13 own-talks bc976e7d (item 15 engine; RV13 PASS incl. section 20 sign-off).
3. f347035d item 15 talk content: exactly CS1's 22 files (`content/talkpack/<id>.talk` + `content/lines/<id>.lines` for pell, torres-zeke, calder, nandakumar from stories-sw1 01293d50; tomas, rina, brennan, sato from stories-sw2 bf1496ff (= 4533c325 for these); marrow, vance, holt from stories-sw3 15215f8f), checked out file by file, NOT the branches (they carry crew-story .arc/voice files: not in this build). Baked 10642 lines / 575 talks. check_fast, talk, social OK.
4. 6ef1b454 DV1 0e329b12 (items 13, 23; RV13 PASS).
5. 0d5e8372 item 13 words: `content/banks/join.lines` from stories-sw2 4533c325 only (RV13 + CS1 PASS). Baked 10646 lines. check_fast, join, lines OK.
6. 560ec755 FX11 789f1ff0 (items 16, 17, 25; RV13 PASS incl. 15r/8c). disc OK.
7. 2cd2d897 FX9 fb3a5d1a (items 3, 4, 5, 18; RV12 PASS). cadet_test differs from i_tap1 on (the social warning instead of bathroom), proven: with only `social: [3, .25]` put back it is ALL IDENTICAL. player OK.

Waiting (merge each on its reviewer's PASS):
- **FX4** claude/p923-fx4 **97251620** (items 2, 12, 14 rename "Schedule tracker", 20, 26 tip + ZW1's 3 comment commits already baked in; RV11). Take this tip, not 64b28176/9be5c21e. Its cadet_test differs in every shot (the wider HUD button label): expected. Its baked words were made before item 15: the LINES block will clash; take either side, then `python3 content_gen.py starship-cadet.html`, `--check`, lines_check. Only interactions_check read the old "Tracked" text (I grepped all checks: the rest are comments).
- **DS1** claude/p923-ds1 b49a01db (items 1, 7-10; RV11). Trial merge over staging: content files merge clean, baked block consistent (regenerate = no change), only build-table rows clash. Item 7 pairs with **AC3** item 6 on claude/arrows-c 55ec3474 (ask the lead whether they go together).
- **FX8** claude/p923-fx8 **9fd5b500** (items 22, 28; RV11; first version 35c4a252 had FIXES NEEDED).
- **FX12** claude/p923-fx12 123a778d (items 19, 27; RV12).
- **FX10** claude/p923-fx10 (items 21, 24, 29; RV13; sha to come) and, as its OWN commit, the arrows_check follower fix (lead 33 approved: the follower stops for a queued `inc:` career arrow with GUIDE_ON; backlog 15 is a test gap, not a game bug).
- Not in this build: crew stories; DS1 goodnight-words (cancelled in 0.92.2).

Every merge so far clashed only on `plans/build-table.md` rows: keep both (`resolve.py FILE both`, below), but check the incoming side doesn't repeat rows already in (tray-seat did in 0.92.2).

## To finish 0.92.3

1. Merge the waiting pieces as they pass. After each: cadet_test vs the step before, the area checks, content_gen --check if words changed.
2. Build number: line 291 `build 0.92.3` and `GAME_BUILD = '0.92.3'` (around line 9073). Build-table row `| 0.92.3 |` after the 0.92.2 row with `Checks: FULLROUND |` as the placeholder. Refresh DEV_NOTES line 5.
3. check_fast + cadet_test vs 0.92.2 (364c80cb) on the candidate, then fast-forward `claude/integration-next` to it (bring integration-next's extra commits in first if any, so it's a fast-forward).
4. Send all six runners the commit, full sha256, OLD = 364c80cb, and the shares (below). Lead 33 may say start sooner.
5. On a NEW FAIL: isolate (e.g. a copy with one switch or one piece's change undone), send it to the piece's owner and the lead; merge the reviewed fix (test-only fixes fast-forward fine), the runner reruns that check.
6. When all six are OK: write the round into the row, push, fast-forward `claude/integration` on the lead's GO (`git push origin <full sha>:claude/integration`), tell PUB1 commit + sha + switches, tell the lead.

## Round setup (as 0.92.1 and 0.92.2)

- CR1: player, devmode, bubble, puzzle, social, talk, arrows_check, arrows_pointer_check, dev_arrow_check, **plus `arrows_check.py BUILD week guide` on NEW and OLD** (lead 33: OLD's Day 9 m6 stuck at 'ask' is known-old, backlog 15, until FX10's follower fix is in; NEW must not be worse).
- CR2: intro_check (whole), perf_check BUILD OLD, cadet_test OLD BUILD, path, arc, lines, lines_check --day.
- CR3: day_check 0, 1, 5, 7; arrows_d_check, arrows_f_check.
- CR4: day_check 12, 13, 16, 19, 6, 8 (6 and 8 for Crossing the Line). No controller reach (skipped, controller off).
- CR5: day_check 21, 27; interactions, events, career.
- CR6: check_fast, mech, bigevents, fridays, disc, tiles (alone), join (alone), food 1 7, food 11 4, clothes; controller_check minus reach: `idle save calls touch walk pick day games unplug odd off quiet base deck pick1 panels api lists tiles disc screens marks touch3 drop settings a11y firstuse lift`.
- Runners finishing early take checks from slow ones; they agree it directly ("taking: <list>") so nothing runs twice.
- Known items: backlog 14, 23, 32 (a one-off perf frame-time spike; re-measure), KP1 (Line ceremony 335 draw calls), backlog 15 (week guide, above). controller "marks" is deterministic since 0.92.2 (LEAD32-1): any marks FAIL is new.
- Switches: POINT_ON, GUIDE_ON true; EV_LINE_ON = EVENTS_ON (on); PAD_ON false.
- PUB1's links: Playtest https://claude.ai/artifact/Wn6mUGcxatoWVqhCNTa1vs, Dev https://claude.ai/artifact/6daNCLCJAcsLCZn27CEthq (Version 11 = 0.92.2). **The user's instruction for 0.92.3 (04:07 UTC, via lead 33): 0.92.3 goes out as NEW Playtest and NEW Dev artifacts with new links; the Version 11 pages above stay untouched so the user keeps their save.** PUB1 already has it. Timing (lead 33): the round starts after RV12's FX12 verdict (~08:00 UTC), within the 10-worker cap (BM + 6 runners + at most 3 others).

## Gotchas

- Background commands stop at 30 minutes unless you pass a longer timeout (I lost an interactions_check run that way). Use the max for check batches.
- Don't change files in a folder where a check is reading them: I used a second worktree (`git worktree add --detach /tmp/wt-x origin/claude/staging-0.92.3`) for merges while checks ran.
- Run browser checks at most two at a time; with more, cadet_test's first shot can differ once (rerun: identical).
- Type full shas when pushing (a short sha failed once).
- The merge helper (save as scratch `resolve.py`; skips diff3 base sections):

```python
import sys,re
p,mode=sys.argv[1],sys.argv[2]; s=open(p).read()
pat=re.compile(r'<<<<<<< [^\n]*\n(.*?)(?:\|\|\|\|\|\|\| [^\n]*\n.*?)?=======\n(.*?)>>>>>>> [^\n]*\n',re.S)
s,n=pat.subn(lambda m:{'ours':m.group(1),'theirs':m.group(2),'both':m.group(1)+m.group(2)}[mode],s)
open(p,'w').write(s); print(p,mode,n,'hunks')
```

- Owner sign-off rule (lead 31, carried by 32 and 33): where owners.md names a seat that isn't live, the piece's reviewer's PASS is the sign-off; record it in the row.
- Test kit setup: `pip install playwright numpy pillow`; `npm pack three@0.128.0 acorn@8.12.1` untarred WITH `package/` into /tmp/cadet-work/three and /tmp/cadet-work/acorn; `CADET_CHROME=/opt/pw-browsers/chromium`; each parallel run its own CADET_WORK with symlinks to those.
