# Handover: CTT, the controller test builder

**Role:** writes and proves `controller_check.py` for the controller support work (plans/controller-plan.html section 10).
Never changes the game. Branch `claude/controller-tests` (from claude/controller at 7dcfab0). Session
session_01SgEbMMMNPRP2E7DbiDyiw4.
**People:** lead 26 session_015mHBLCf5jpnzBkFY1iBTqv (took over from lead 25); CT1 (team leader, section 26's builder)
session_019sqDowb6QNf3KZAYMSx1jM on claude/controller; reviewers PR9 session_01B1FUTc4sJR4Q5FFnx7L6Db (foundation, p1-p2) and
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

## Status (keep current)
| Part | Package | State | Proof |
|---|---|---|---|
| idle | (none) | OK on 0.64.14; on CT1 0.90.2: mode b adds 3 hand-back listeners before a press (CT1 told, RV2 note 11) | 6/6 faults caught |
| save | (none) | OK, all of storage compared | 2/2 |
| calls | (none) | OK | 1/1 |
| walk | deck | OK on CT1 0.90.2 and the stand-in | 6/6 (stand-in) |
| touch | base | OK on 0.90.2 (ring and #padHint kept hidden: info) | 2/2 (stand-in) |
| unplug | deck, marks | stand-in only (marks not built) | 3/3 |
| odd | deck | OK on 0.90.2 and the stand-in | 2/2 |
| pick | pick | crew, machine, sealed door OK on 0.90.2; lift not offered by the D-pad from 2 m (CT1 told); no lone seat on Deck 4 | 3/3 on 0.90.2 |
| reach | panels | touch half working (deck taps open Tiles, ladder, lift panel, other decks); pad half written, untested | none yet |
| day, games | | not written | |

## Loose ends
- One file or two: CT1 also has a controller_check.py (white-box: PAD.log, padLayer). Proposed: mine is the file, CT1's
  off/quiet/base folded in. Waiting for CT1's answer.
- PAD_BUILT line asked of CT1.
- NOT_FROM_NEW_GAME (panels that can't open from a new game at a test URL) to fill from the first full sweep, each with
  its reason.
- The sweep is slow (reloads ~15 s each); it is not for check_fast.

## Gotchas
- `pkill -f PATTERN` kills your own shell when the pattern is also in the command line: run pkill in its own call.
- JS strings in the check: a `//` comment inside a one-line script swallows the rest of the line. After editing, check
  every `X = r"""..."""` parses (the snippet in this note's history: node `new Function`).
- Two browser checks at once at most, each in its own CADET_WORK.

## How to test
`CADET_CHROME=/opt/pw-browsers/chromium python3 controller_check.py GAME.html [parts] [--mutants] [--selftest]`.
CT1's build: `git show origin/claude/controller:starship-cadet.html > g.html`.
