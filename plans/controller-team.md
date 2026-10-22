# Controller team: the package split (lead 26, 2026-10-22 morning)

The user: "write the controller split yourself and start the builders." CT1 built turns 1-3 (0.90.0-0.90.2, PR9 PASS on 1-2) and a work-in-progress turn 4 (claude/controller a2c80df6, the highlight in panels), but never wrote this page, so the lead wrote it from CT1's plan page (plans/controller-plan.html on claude/controller; published https://claude.ai/artifact/Uhdf3u4fhbXrhb4G7hcQvE). The plan page's sections are the spec: read it first.

## What everyone builds on (claude/controller a2c80df6)
- Section 26 CONTROLLER behind `PAD_ON` (off): reading the pad each frame, dead zones, connect and disconnect, the pad in charge, `padOn` names, `padLayer()` / `PAD_PANELS` (which panel is on top), `PAD_PICK` (the ring, the bottom line, A through `tap()`).
- Walking, turning, zooming, Pause, Device, Tracked (turn 2); picking on the deck (turn 3); turn 4's WIP panel highlight.
- `controller_check.py` with a pretend pad (CT1's) and CTT's richer one on claude/controller-tests: they are being made into one file (CTT + P1 agree it).
- Rules: everything behind `PAD_ON`; with no pad, cadet_test ALL IDENTICAL with the switch off and on; no `R()`, no new saves unless changed from normal, no new page elements until a pad button is pressed; new code only in section 26's slot plus one-line typeof-guarded hooks elsewhere (each owner reviews their hook).

## The packages
Each package branches from claude/controller a2c80df6 (P2-P5 rebase onto P1's panel helper as soon as it lands; see P1), pushes only to its own branch, never touches the build-number lines, adds a build-table row, runs its controller_check parts + check_fast + cadet_test (switch off AND on, no pad: ALL IDENTICAL), and sends its tip to its reviewer and the lead.

| Package | Branch | Plan sections | Scope | Reviewer |
|---|---|---|---|---|
| **P1 Panels** (finishes turn 4) | `claude/controller-p1` | 3 | Which panel is on top, the highlight (real page focus, teal outline), D-pad moves to the nearest button, A presses, B = Escape/tap-outside, scrolling long lists (right stick), page up/down (triggers), the screen-edge buttons via D-pad up, X for the bottom-right action button, typing boxes open the phone keyboard. **First job: push the panel helper's API (how a panel registers, how focus moves) within the first hour, and tell P2-P5.** P1's builder also merges the passed packages into claude/controller and sets the 0.90.x build numbers there. | PR9 |
| **P2 Mini-games and special screens** | `claude/controller-p2` | 4 | Tiles (D-pad square by square, A pick/put), Lightdisc (left stick full range, A Next, B Leave, result card), work steps (choose/turn cards), the lift (goal deck highlighted, A rides, B stays), sleep alarm, Dev mode's sheet, the arrival screens. Start with Tiles and Lightdisc (own screens); use P1's helper for the rest once it lands. | PR9 |
| **P3 Button pictures + connect/disconnect** | `claude/controller-p3` | 5, 6 | Button marks in the pad's family style (Xbox letters, PlayStation shapes, Nintendo places), beside Device/Pause/Tracked/X action/Leave and on the bottom line; only after a pad press, gone at touch/mouse; text-size aware; never over bubbles. "Controller connected" message once a session; disconnect stops walking and pauses (Pause card line "Controller disconnected") if used in the last 30 s; reconnect resumes; two pads: last pressed wins. | RV2 |
| **P4 Controller settings page** | `claude/controller-p4` | 7 | A Controller page in the device's Settings app, shown only once a pad has been seen: rebinding (swap on clash, Back to normal), confirm/back swap, stick dead zone and speed, camera (zoom speed, flip, flick vs hold), button pictures choice, vibration (off by default). Saved only when changed from normal (a save without changes stays byte-identical; ~100 bytes when changed; check the save budget). | RV2 |
| **P5 Accessibility + docs** | `claude/controller-p5` | 8, plus DEV_NOTES and design-doc | No holds or fast presses; menu repeat at a calm pace (0.5 s then 4/s, adjustable via P4's settings hook); any action to any button (with P4); thick high-contrast highlight; the ring pulses unless reduced motion; screen-reader names via real focus; vibration never the only sign. Then DEV_NOTES's controller section and design-doc's controller paragraph (the user's answers from the plan page). Works with CTT on the whole-day-by-pad and the reachability sweep. | RV2 |

**CTT** (claude/controller-tests) keeps the test side: the single controller_check.py, the full reachability sweep, a whole day by pad, games parts, perf at phone size; each package's builder adds the check parts for its own features and tells CTT.

**CT1** (if it returns): advises; turn 4's notes go to P1. **Switch-on (plan turn 9)** is its own reviewed step after all five pass and a six-runner full round, and only on the user's go.

## Order of merging into claude/controller
P1 first (the others depend on its helper), then P3, P2, P4, P5 as each passes. Into claude/integration only when all five are in, reviewed, and a full six-runner round passes (the user's rule).
