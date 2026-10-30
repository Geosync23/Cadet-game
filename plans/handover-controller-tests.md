# Handover: CTT, the controller test builder

**Role:** writes and proves `controller_check.py` for the controller support work (plans/controller-plan.html section 10).
Never changes the game. Branch `claude/controller-tests` (from claude/controller at 7dcfab0). Session
session_01SgEbMMMNPRP2E7DbiDyiw4.
**People:** lead 27 session_017UHW78qnvRTQwYpDxpodHz (report to it); CT1 (turns 1-3, now idle) session_019sqDowb6QNf3KZAYMSx1jM
on claude/controller; package builders (plans/controller-team.md on claude/lead-26): CP1 panels + merges into claude/controller
session_015ZhJRKCEditHrVhwdhszYq (claude/controller-p1), CP2 mini-games session_016zb2DTsTLqNNNeuegePDgE, CP3 marks + connect
session_01AkfeDe7MBN8RYd5n6obGRm (claude/controller-p3), CP4 settings session_01VTXDwLqWGJVRh95HozqhCu, CP5 accessibility + docs
session_01VcdDgzyHa1dqdmcRLELbiS (claude/controller-p5); reviewers PR9 session_01B1FUTc4sJR4Q5FFnx7L6Db (foundation, p1-p2) and
RV2 session_01E1TTHbhLzy2U6pAoGh7E9a (p3-p5 and this check; notes in plans/review-controller.md on claude/review-controller).
**Memory rule (lead 26, the user's):** from about 60% judge case by case; hand over before a big task; never above 80%.

## How the check works
- A pretend controller replaces `navigator.getGamepads` before the game loads (`FAKEPAD`): four slots, a fresh frozen
  copy each read, `window.__pads.plug/unplug/set/clear`. Modes: `none` (the browser's own, untouched), `api` (no pad),
  hidden-until-the-first-press (mode a, Chrome's way), present at load (mode b), drifting sticks (+-0.05, triggers .02).
  CT1's helper names (`__padPlug`, `__padHello`, `__padBtn`, `__padAxes`, `__padUnplug`) also work.
- Every run gets its own browser (a second page in one browser drew a speech bubble's layer differently).
  `Math.random` is seeded (the career's seed gs reads it). The quiet style is in the page from the start, speech bubbles
  are out of pictures (`.bubw` opacity 0; their DOM is still compared). Waits for section 17's machine averages at load.
- `CENSUS` wraps addEventListener: listener counts, and which elements have click-like listeners (for the sweep), and
  the last click's target (for A).
- Packages: `PAD_BUILT` in section 26 if present, else found from the code (`FOUND_BY`: PAD_ON, PAD_DECK, PAD_PICK).
  A part whose packages aren't built: "not yet". A built package with no part: FAIL.
- Controller parts run on the switch-on copy; idle, save and calls test off and on themselves.
- `--mutants`: each part's planted faults (MUTANTS) must each add a failure the clean run didn't have.
- `--selftest`: plants the check's own small stand-in driver (STANDIN; only for a game without section 26) so parts can be
  proved before CT1's code exists.
- `reach --inventory`: the touch half of the sweep alone (slow: about an hour; CTL_PRESSES caps presses).

## Status (keep current; 2026-10-22 ~10:40)
The single controller_check.py is THIS file (agreed with CP1, who merges claude/controller). This seat keeps: the sweep
(reach), the whole day by pad (day), games, perf; package builders send their own parts.
| Part | Package | State | Proof |
|---|---|---|---|
| idle | (none) | OK on 0.64.14; on CT1 0.90.2 mode b adds 3 hand-back listeners before a press (CT1 told) | 6 own faults + PR9 c6 |
| save | (none) | OK, all of storage | 2/2 |
| calls | (none) | OK | 1/1 |
| walk | deck | OK on 0.90.2 and the stand-in | 6/6 stand-in; PR9 c1-c3 running |
| touch | base | OK on 0.90.2 (visible page compared; ring and #padHint kept hidden: info) | 2/2 stand-in; PR9 c4 running |
| unplug | deck, marks | stand-in only | 3/3 |
| odd | deck | OK on 0.90.2 | 2/2 |
| pick | pick | crew, machine, sealed door, lift (the D-pad didn't offer the lift from 2 m on 0.90.2: CT1 told) + a crowded seat in the Deck 3 mess at breakfast (new, untested) | 3/3 own on 0.90.2; PR9 c5, c7 running |
| reach | panels | touch half: works, a full run on turn 4 (a2c80df) in progress (scratchpad logs/reach10.txt); pad half: works on the stand-in, + readable names (CP5) | 2 faults written, not run |
| games | games | OK on the stand-in (Tiles 9 moves to the end, Done; Lightdisc how-to, stick, B leaves) | 3 faults: the run was cut off by a time limit, rerun into a log file |
| day | all | written (lift to breakfast, eat, talk, Take it at the job board, lift home, Set alarm), never run | none |

Results of PR9's and RV2's faults on 1ec1612: see "Reviewers' faults" at the end of this note (or rerun: `CTL_MUT=PR9 python3 controller_check.py
g.html idle walk touch pick --mutants`, g.html = `git show 1ec1612:starship-cadet.html`).

## To fold in (the next big job)
Old-shape parts (def part_X(pw), a Pad class, check()/fail() globals, GAME/ON paths) from other branches, to bring in
unchanged through an adapter (a function that sets GAME/ON to the part's src files, runs part_X(pw) and collects check()
failures as the part's list):
- CT1, claude/controller 1ec1612+: off, quiet, base, deck, pick (white-box: PAD.log, padLayer, padZoom0).
- CP1, claude/controller-p1 93093a8: api, panels. Take the game from claude/controller-p1 for runs.
- CP3, claude/controller-p3 efbe62a: marks, touch (register as 'touch3'), drop. NEEDS ['marks'].
- CP5, claude/controller-p5 fc8ccd5: part_a11y + NAMELESS, as 'a11y', NEEDS ['panels', 'pick']; its faults (outline 3px,
  padStill false, no toast role) as MUTANTS.
Then ask CP1 for the PAD_BUILT line (and each CP to add its package name when done).

## Gotchas
- `pkill -f PATTERN` kills your own shell when the pattern is also in the command line: run pkill in its own call.
- JS strings in the check: a `//` comment inside a one-line script swallows the rest of the line. After editing, check
  every `X = r"""..."""` parses (the snippet in this note's history: node `new Function`).
- Two browser checks at once at most, each in its own CADET_WORK.

## How to test
`CADET_CHROME=/opt/pw-browsers/chromium python3 controller_check.py GAME.html [parts] [--mutants] [--selftest]`.
CT1's build: `git show origin/claude/controller:starship-cadet.html > g.html`.

### CP3's update (10:32): tip claude/controller-p3 958421a (merges P1's helper)
Register 'marks', 'touch3', 'drop' all with NEEDS ['marks']. CP3's planted faults (each line once in the game at 958421a):
```
MUTANTS['marks'] = {
  'marks shown without the pad in use': ('src', "'body.pad .padk{display:inline-flex}", "'.padk{display:inline-flex}body.pad .padk{display:inline-flex}"),
  'Nintendo marks in Xbox places': ('src', "nin: { a: ['B', '#e6f0f1', 'B'], b: ['A', '#e6f0f1', 'A'],", "nin: { a: ['A', '#e6f0f1', 'A'], b: ['B', '#e6f0f1', 'B'],"),
  'Controller connected said at every press': ('src', "if (!PAD_MARK.said) { PAD_MARK.said = true;", "if (true) { PAD_MARK.said = true;"),
}
MUTANTS['drop'] = {
  'no pause after a drop-out': ('src', "if (PAD.goneUsed && !PAUSE.on) {", "if (false) {"),
  'the card keeps saying disconnected': ('src', "else if (!on && PAD_MARK.line) {", "else if (false) {"),
}
```

### CP2's parts (10:42): claude/controller-p2 e62efcc (built on CP1's file at 86d45aba)
Old-shape parts 'tiles', 'disc', 'screens' (plus CP1's 'api', 'lists'), to fold in the same way. NEEDS ['games'] for tiles and
disc, ['panels'] for screens. tiles waits 1.5 s real time after a game ends (Tiles redraws on its own timer). disc uses a real
DECK_CREW member. screens stubs pressPanel for the lift ride. Ask CP2 for planted faults if it hasn't listed them.

### CP1 (10:53): claude/controller-p1 825378d2
PAD_BUILT = ['base', 'deck', 'pick', 'panels'] is in. The highlight is always the real focus (document.activeElement); on the
screen-edge layer it can land on plain divs (seek chip, heads-up, address card, tip), which get tabIndex -1 at that moment.
CP1's old-shape parts in that commit's controller_check.py: api, lists, panels (30 panels). CP1 asks this seat to own the
conversion and to tell it the commit so it runs its parts from this file. A suggested way to fold (CT1's, CP1's, CP2's,
CP3's, CP5's old-shape parts): copy each part function in under its name, with one shared adapter giving them what CT1's
file gave (GAME/ON paths set per call, a Pad class over cadet_test's Game with plug/btn/axes/press/log, check()/fail()
appending to a list the adapter returns), then register NEEDS and MUTANTS as in this note.

### CP4 (11:23): claude/controller-p4 db80eb0
Old-shape part 'settings' (part_settings with helpers SV and SAVE_NOW above it; uses Pad and sweep()). A real reload with
saving on (writes a save in the game's shape, page.goto without ?nosave, clears localStorage at the end); defines
window.PAD_LAYOUTS as a stand-in for P5's. About 2 minutes. NEEDS ['settings'].

## Reviewers' faults on 1ec1612 (11:30, logs in the scratchpad: pr9.txt, pr9b.txt)
Caught: PR9 c1 (walk), c2 (walk), c3 (walk: the deck takes nothing while the device is open, added for it), c4 (touch),
c5 (pick), c6 (idle: scene 14 -> 15 with the switch on and no pad); RV2 t3_noop_crew (pick: the chat card / who's talking,
added for it), t3_noface (pick: the facing test, added for it).
NOT caught: PR9 c7 (a seat ringed where the tap reaches a person). Cause, the check's: the crowded-seat case (Deck 3 mess at
07:40, a free mess seat beside someone seated) stood the player where the ring offered Lift / Dr. Imra Sato / Deck directory
/ Spine ladder, never the seat: STAND_BY's nearestOpen near 3-mess-2 seems to land by the lift. Next: stand on the tile
beside the seat spot (try the four neighbours of the seat's own tile, pick the one nearest the spot), then rerun
`CTL_MUT='PR9 c7' python3 controller_check.py g.html pick --mutants`.
Open in the clean run on 1ec1612 (for CP1 to judge, may be the check's): facing the Wardrobe (Deck 4, the spot FACING_SPOT
chose), the ring starts on "Bed", not the Wardrobe; the lift still not offered from 2 m (CT1 told; CP1 now owns pick).
Not yet run: the games faults (rerun into a log file; the earlier run was cut off by a time limit), the reach faults, the
day part (never run), the full reach sweep on turn 4 (scratchpad logs/reach10.txt was in progress).
The turn-4 sweep (a2c80df, CTL_PRESSES=900) was stopped at the handover after 611 presses and 81 loads in about 95 min:
39 screens, reaching Decks 1, 2, 3 and 7 and, by deck taps, Booth 1, the lift panel, the servery, the Spine ladder, the Tiles
table and the toilet. It never finished, so the completeness list (panels hidden at load never seen open) is still to come;
expect to run it in a slot of its own for about 2 hours.
