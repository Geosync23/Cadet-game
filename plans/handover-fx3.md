# Handover: FX3 (fixer), 2026-10-23

Role: fixer under the lead (leads 27 to 32). Session session_01UZWrZRivwQJPKL3x7c8Ft9. Branch: `claude/p5-fix3`
(this session may push only there). Stopped on lead 32's word at about 71% memory; take nothing new from this note
without the lead.

## Where things stand

- **Open: the relay-shelf fix (fresh-eyes 2 item 64, backlog LEAD31-7), with RV11 (session_01EdBKAgQFMexMSs3JbgH5H7) for
  0.92.2.** On `claude/p5-fix3`, one commit on staging-0.92.1 `54efee21` (the sha is in the lead's and BM15's messages
  and in `git log`). It replaces the first version `85b6250a` (on `dbc62255`), which RV11 sent back with two findings,
  both done: (1) the glow tap now comes after section 11's `tapCrew`, so a tap on someone standing in front of the glow
  still talks to them; (2) rebased onto `54efee21`.
  - Cause: the shelf glow in main storage (`SHELF_GLOW`, section 17) reaches down to the floor and out past the shelves,
    so a thumb tap on its lower part or corners met the floor in front of the Lights shelf, or at one camera angle the
    Filters shelf in front ("No relays on the Filters shelf"), and the Day 1 job's relay couldn't be had (FE2's
    screenshots: `claude/fresh-eyes-2` c84bf22, `plans/fresh-eyes-2/d1-186.png`, `d1-187.png`).
  - Fix: `shelfGlowTap(cx, cy)` in section 17, right after `shelfGlowTick`: while a shelf glows, a tap whose ray meets the
    glow box is a `playerTap` on the nearest item of that shelf. Section 11's `tap()` asks it on the line after
    `if (tapCrew(cx, cy)) return;`. Owners to review: HUD seat (section 11, one line), systems seat (section 17).
  - Checks: interactions_check part "FX3: a tap on the glowing shelf takes the part": 216 real taps on the glow's bottom
    and corners at 12 camera angles must all fetch (22 fail on the base), then Calder placed between you and the glow,
    a tap on her body must talk to her (it fetched on 85b6250a). Whole interactions_check, machine_check, player_check,
    check_fast and names_check OK; cadet_test alone was ALL IDENTICAL for 85b6250a (re-run it for the new sha if asked).
  - Known trade-off: none left beyond "a tap on the glow where no person is takes the part even when you meant the floor".
- Nothing else open. Earlier work (fixes 1-19, the inspection arrows, the climbing wall, the tap at the pin over
  someone standing there) is all merged into 0.92.x; its rows are in `plans/build-table.md` under "patch-p5-fix3 (FX3)".

## Gotchas

- `claude/p5-fix3` is reset/rebased onto whatever base the lead names; it carries only my last commit on top.
- Tests that place a crew member (`DECK_CREW` agent `a.x/a.z`) must tap in the same step: the crew move on next frame.
- Real taps: use `page.mouse.move/down/up` at the projected point; `playerTap` called directly with a stale `ray` lies.
- interactions_check now takes about 40 minutes whole; give it a 60-minute timeout.
- Each parallel check needs its own `CADET_WORK` dir with a `three` symlink (`/tmp/cadet-work/wN/three`).

## How to test the relay fix

`CADET_WORK=... CADET_CHROME=/opt/pw-browsers/chromium python3 interactions_check.py starship-cadet.html` and look for
"FX3: a tap on the glowing shelf takes the part" (both lines OK). To see it fail: run the same part on `54efee21`.

## Open questions for the user

None from me.
