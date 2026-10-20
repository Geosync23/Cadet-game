# Handover: Dev mode reviewer (DR1)

DR1, session_01WfFmjT31bVcy4mvsNVi5Mz, 2026-10-20, written at about 47% memory, before any automatic summary. Reports to lead 20 (session_019UJSCUCdtC1kTpYiABWKhs). Never contact the user directly.

## Role
- An adversarial technical reviewer of Dev mode: the plan, then each build step.
- An **owner stand-in** for sections whose owners have no live seat (13, 14, 15, 15b, 19, 20, 21, 4d, 11, 8b slot). I review hooks into those sections as the owner would.
- I push only to `claude/devmode-review-1`. I never push to `claude/devmode`, `claude/patch-e`, main, or other seats' branches. Fixes go into my reply as suggested patches.
- Each review goes to the lead (and to the builder when the lead says), with PASS / PASS WITH FIXES / FAIL and the memory %.

## Where everything is
- **All findings, in order:** `plans/devmode-plan-review-1.md` on `claude/devmode-review-1`. It holds the plan review (v1, v1.1), the re-checks of v2 and v3, owner reviews D1, D2/D3 and D4, the final Stop 1a verdict, and patch E's two reviews. Each section names the commit it reviewed.
- **Scripts and printouts:** `plans/devmode-review-1/`. All use cadet_test's `Game`, `INIT` and `instrument`; run each with its own `CADET_WORK`.
  - `replay.py GAME MODE DAYS`: a steady player, `nosave` or `devsave` (keys with -dev, saving on); prints a fingerprint with the seed zeroed. It showed the random career seed (`gs`).
  - `replan.py`: a tradition started today: what changes (past 0, now 20 of 74, evenings 57).
  - `skiponly.py`: skip-only player: let go on Day 20, career over on Day 21.
  - `setcareer.py` / `setcareer_skip.py`: a rough Set career (v3). The shuttle start pins the clock to Day 0 (`introTick` while `I.step === 'manifest'`); Skip to Monday works. `W.op` must be written as well as `W.tr`.
  - `savecmp.py A B` / `savecmp2.py A B`: the real game's localStorage byte for byte between two builds, in 5 modes (none, #debug, ?nosave, #nosave.dev, #debug.nosave), plus a run with the arrived key and a #dev session over it. Use these for any "switch off = identical" claim about saving.
  - `excuse.py GAME`: Dev clock jumps around 09:00-12:30 on Day 2 and Day 9: excused or not, can you clock in, jobs held.
  - `locked.py GAME`: Take me to every room; the rooms with no walking way back (2:P, 5:d).
  - `slowreload.py GAME SECONDS`: Undo with the page's reload held back over a local http server. It proved the 4 s safety bug, now fixed in fa394b3.
  - `deckswap.py`: goToDeck timings.
  - `undowin.py GAME`: patch #6's clock Undo window with Dev mode merged (scratch merge): a Dev jump or a save settles it.
  - `hud-390x844-day27.png`: the HUD at phone size.

## State of things (end of my run)
- **Dev mode Stop 1a** (claude/devmode fa394b3): final **PASS**. Its six hooks: 13 (`DEVMODE`, `SAVE_KEY`; `freezeSync`/`saveGame` ask `devmodeHold`), 21 (`INTRO_KEY`, `introWanted`), 20 (`careerOff` reads `devmodeExcused`), 15 (needs kept while held), 11 (`deckCrewFill` once). All are proven no-ops with Dev off.
- **Mug and cocoa** (#30, #29) on claude/devmode 375827b: **PASS** (hooks in 15, 15b, 8b slot).
- **Patch E** (claude/patch-e): 2e2575d **PASS** (#6 clock Undo, #21 rank card, #24 shop menu, #25 Deck 2 rename, section 19 roster hook); ab685bb **PASS** (#5 spine ladder hooks in 11 and 4d, 274a31f's guards).
- **Known and accepted, not to "fix":** career_check fails `busy: "Relied on" before Day 5` on integration too (backlog row 12).

## Loose ends for whoever takes over
1. **Stop 2 (Set career) and Stop 3 (Big events)** aren't built yet. When they come, check:
   - Set career starts with Skip to Monday, writes `W.op` for every trained row, lets `INTRO_BOOT`'s first frame pass, and calls `promoPip()`.
   - "End now" needs the ending split out of `eventAdvance` (section 18 owner first). Phase jumps wait for the events plan's F4.
   - The fixed seed was dropped in v3: devmode_check can only compare fields across two Set careers, not save bytes.
2. **The lead's earlier ask (1):** once Dev mode and the patches are both merged into integration, re-run `undowin.py` on the real merge, plus a Dev jump past a held punch and PB's schedule changes.
3. **The lead may send more owner stand-in reviews** for 13/14/15/20 hooks.

## How to test (fresh container)
```
pip install playwright numpy
mkdir -p /tmp/cadet-work/three && cd /tmp/cadet-work/three && npm pack three@0.128.0 && tar xzf three-0.128.0.tgz
mkdir -p /tmp/cadet-work/acorn && cd /tmp/cadet-work/acorn && npm pack acorn@8.12.1 && tar xzf acorn-8.12.1.tgz
export CADET_CHROME=/opt/pw-browsers/chromium
# each parallel run: export CADET_WORK=/tmp/work-<tag>; mkdir -p $CADET_WORK/test; ln -sfn /tmp/cadet-work/three $CADET_WORK/three
```
- `node names_check.js GAME` needs `CADET_WORK` to hold `acorn/` (use /tmp/cadet-work).
- **Run cadet_tests one at a time.** Two side by side on 4 cores gave false pixel differences (f_noshadow, g_nocrew, h_crewback, ~12k px) that disappeared when run alone.
- Pull a build with `git show origin/<branch>:starship-cadet.html > X.html`. Compare against integration with cadet_test (expect ALL IDENTICAL with switches off; patch E's only difference is #25's directory text).
- Dev mode pages need `#dev`; a fresh Dev save starts the arrival on its first frame (`INTRO_BOOT`). Probes set `INTRO_BOOT = false; newGameStart(false); introSkip()` first.

## Gotchas
- `const DEV` belongs to section 19 (the device); Dev mode's switch is `DEVMODE`.
- `NOSAVE` changes the game (no clothes, no arrival, career seed 0). Dev mode uses its own save (keys with "-dev"), not nosave.
- `introTick` holds the clock at Day 0 17:30 while the arrival is on its manifest step.
- `worksOpened` reads only `W.op`.
- `careerOff` feeds `playerShiftOn` (42 readers), so excusing a day makes it a day off. Dev mode excuses only what the game would count as a miss: after Day 7, the jump passing 12:30, not clocked in.
- `saveGame` swallows a full store silently, so Dev storage has a space check that keeps room for the real save.

## Open questions for the user
None of mine are open; the plan's questions were answered by the user on 2026-10-20 (v3).
