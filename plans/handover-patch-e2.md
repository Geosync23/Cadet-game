# Handover: patch batch E part 2 (#30, #29 done; #26 First Light Cocoa to build)

From DB1 (the Dev mode engineer, also patch builder for E2), 2026-10-20, for the fresh builder lead 20 starts for #26.

## Role, branch, builds
- **Branch:** `claude/devmode`, which carries the E2 work. The lead merges from it; it's the only branch this session could push to. It was started from `claude/integration` 0.64.3 (da5e2aa, Dev mode merged).
- **Commits:**
  - #30: c6f1158 (15 hook), 4420bff (15b hook), 05314b6 (the code)
  - #29: the 15b hook (`mugAlso` in ixSide), then the #29 commit (barTap's serve line, the slot, the words)
- **Build number:** untouched.
- **Reviews:** PP1 (session_01QfLuMmrJSgMQ3A4tBtXAmf) reviews each turn, through lead 20 (session_019UJSCUCdtC1kTpYiABWKhs).

## What's built (#30 and #29)
- **The switch:** `MUG_ON` (section 15's slot) = `URL_FLAGS.has('mug')`. Off, the game is unchanged (cadet_test ALL IDENTICAL). `#mug` on the link turns it on for a test. Switching it on (`const MUG_ON = true`) is its own reviewed step.
- **Section 15's slot:**
  - `MUG` = `{ drink, from }`; `MUG_DRINKS` (cocoa, tea); `MUG_MINS` = 20.
  - `mugTick()`: run each frame from the player tick. It finishes the mug after 20 ship minutes, or at once when your hands are wanted.
  - `mugHeld()`: the hold, 'mug'.
  - `mugPose()`: 'cocoa' for 15b's stool pose.
  - `mugPut()`: used by Put down.
  - `mugFinish()`: gives the stool's gains when you finish it.
  - `mugAlso(d, also)`: cocoa is leisure +8.
  - `mugText`: reads the words.
- **8b's slot, only with MUG_ON:**
  - `PROP_KIT.mug`: the body at 1.6x life size, a torus rim, cocoa .005 below the rim, the handle sunk into the wall. Its top is the +z end in the hand's space.
  - `HOLDS.mug`.
  - `ACTS.cocoa`: the drink pose with the mug; added to `ACT_SEATED` and `CROWD_ANIMS`.
- **Hooks:**
  - section 15's player tick: `mugTick`; the hold expression: `mugHeld`.
  - 15b: `putWhat`, `putDown`, `ixPose` (`mugPose`), and ixSide's drink line (`mugAlso`).
  - barTap (section 15): cocoa's serve line, and "or drink it as you go".
- **Words:** `content/banks/bar.lines` has `bar.serve.cocoa`, `bar.finish.cocoa`, `bar.finish.tea` and `bar.putdown`. Run `python3 content_gen.py starship-cadet.html` after editing.

## #26 First Light Cocoa: what's left
Read these first:
- `plans/patch-plan.md` and `.html` (#26), on `claude/patch-plan` b2e7220.
- `plans/patch-plan-first-light-cocoa.md`: the draft `.trad` and `.meet`, which go into `content/traditions/first-light-cocoa.trad` and `content/meetings/firstLightCocoa.meet` via content_gen.

The new pieces, each the traditions engineer's or the dialogue engineer's to agree first:
- `ties: meeting <id>`: play a meeting when you join.
- `anim: cocoa`: the crew hold mugs. `ACTS.cocoa` exists, but only with MUG_ON. #26 needs MUG_ON on (or its own switch that implies it).
- An invite from a non-host: Zeke at the Day 1 dinner.
- The lounge dim: a decor tie, at most 6 draw calls.
- `? pick 3`: three tips from five, picked per save (the dialogue engineer's).
- The tradition key `k`: pick an unused one (not 1039; backlog #10).
- `when: arrival monday`, 20:00-20:45.

Also:
- The intro's bed arrows wait until the tradition is over.
- At the tradition you hold a mug for the whole moment and hand it back as it ends. Set `SHIP.player.drink = 'cocoa'` when you join, and clear it at the end without gains, or give it free.
- Checks: events_check, join_check, day_check (Day 1), intro_check, lines_check, cadet_test, perf_check (a lounge scene).

## Gotchas
- Every check copies the build into `$CADET_WORK/test/`, so parallel runs need their own `CADET_WORK`.
- cadet_test's first shot (`a_start`) once differed with the state identical; the rerun was identical. Run cadet_test alone, not beside other browser checks.
- A fake `SHIP.player.tray` set in a test is cleared by the game before `mugTick` sees it; test "hands wanted" with `SHIP.player.carry.push('filter')`.
- Dev mode (`#dev`) helps for testing:
  - Clock "To a time…" on Day 1.
  - Take me to: the bow lounge (Deck 3).
  - Both links can be combined: `#dev.mug`.

## How to test the mug
On a link with `#mug`:
1. Buy a cocoa at the bow lounge bar (17:30-23:00), or in the console: `SHIP.player.drink = 'cocoa'`.
2. You hold the mug. After 20 ship minutes it's drunk, with a toast.
3. Put down sets it down.
4. At a stool, the pose shows the mug.

Close-ups are in `plans/patch-e2-shots/`.

## Open questions for the user
None from #30 or #29.
