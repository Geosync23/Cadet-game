# Handover: seat K1, the rec mini-game prototypes (kayak, wall, pool)

Session: session_018UqUAihUx3VEpAvBwds2on. Reported to lead 17, then lead 18 (session_01CBur9nrJ411pFkHopF96RL). Never contact the user, start sessions, publish, or push outside `claude/kayak-proto`.

## Branch and builds
- Branch `claude/kayak-proto`, started from `claude/p5-cand-pt1` (0.63.3 Step 3, f3ab7e5). New files only; `starship-cadet.html` untouched.
- db0dd08: kayak. 7addcf2: wall, plus a kayak fix (a menu button kept focus, so Space restarted the go). 685d6ad: pool.
- Published by the lead, each on its own link:
  - Kayak "White water": https://claude.ai/artifact/K593iZT8A2XSZ1KnSMwhCq (v2 = 7addcf2).
  - Wall "Reach": https://claude.ai/artifact/SphYWohHzdRtDZxrsnKRPY (7addcf2).
  - Pool "Lengths": https://claude.ai/artifact/4TGLSKY8FA2jVMbQ6ePsoY (685d6ad).
- Status: the user hasn't tried them yet (overnight). Next: changes once they do, then integration (a separate job, after approval).

## What I own and built
Each is one page, laid out like `lightdisc-proto.html`, in the same numbered sections:

1. setup
2. the room or wall
3. people or props
4. the place (loop, routes, strokes)
5. **the rules (pure)**
6. events
7. camera
8. the flow (menu, result, bests in words)
9. input
10. drawing
11. test hooks

Full notes are in DEV_NOTES ("Kayak prototype", "Wall prototype", "Pool prototype").

- **`kayak-proto.html`**
  - Rules: `kyNew`, `kyStep`, `kyPaper`, `kyClone`.
  - The water is a function of place: `loc(x, z)` gives `s` (round the loop) and `d` (out from the island); `water()` gives the flow.
  - Stamina, then drift when empty.
  - Crew: `aiInput`.
  - Hooks: `window.KY`.
- **`wall-proto.html`**
  - Rules: `wlNew`, `wlStep`, `wlPaper`, `wlClone`.
  - Routes are fixed by `hash()` in `HOLDS` / `ROUTE_HOLDS`.
  - Reach: within .6 of the other hand and at most .28 above it.
  - Grip, then the belay lowers you.
  - Hooks: `window.WL`.
- **`pool-proto.html`**
  - Rules: `plNew`, `plStep`, `plPaper`, `plClone`.
  - Beats: a press timed at the touch; the breath beat is held; a swipe in the turn zone turns you.
  - Hooks: `window.PL`. `PL.toBeat`, `PL.toWall` and `PL.live` let a test step to exact moments.
- Checks: `tools/kayak_proto_check.js`, `tools/wall_proto_check.js`, `tools/pool_proto_check.js`. Shots: `plans/shots-kayak|wall|pool/`.

## Shared formats (for integration later)
- Fixed 60 Hz steps. The seeded stream is plain state in `g.rs` (a mulberry stepped by `rnd(g)`), so `JSON.parse(JSON.stringify(g))` clones a live go.
- Events go in `g.ev` (`evOn` is off on paper).
- Summaries (`kySummary` / `wlSummary` / `plSummary`) are what the frame-rate tests compare.
- Seeds: game keys 833-838 are proposed by the plan; the lead confirms them at integration.
- Crew chat lines are stand-ins in `CREW[k].lines`.
- Bests live in `localStorage` (`ky.best`, `wl.best`, `wl.bestf`, `wl.board`, `pl.best`). In the game they'd move to `SHIP`.

## Judgement calls (all accepted by the leads)
- **Kayak**
  - Slow loop = pumps low.
  - Up to 2 crew beside you; the regatta heat of four starts in two rows, with heat 2 worked out on paper.
  - The kayak is 0.8 of the game's size.
  - The dock is on the bank.
- **Wall**
  - Reach is short (.28 above your other hand) from a sit start, giving 10-15 moves on the 3.52 m wall.
  - Only your route's colour can be grabbed.
  - A friend climbs the next route, and the camera leans toward them.
  - The camera follows your held hands only, so the wall doesn't slide under a still thumb.
- **Pool**
  - The game's lanes, 6 m lengths.
  - Windows: clean .08 s, good .16 s, ok .3 s.
  - A breath every 3rd beat (breaststroke) or 4th (crawl).
  - Turn zone 1.2 m.
  - Crawl is a menu switch.
  - Crew: Rina, Tomas, Pell.
  - "Keeping with Rina" = within ~1.2 m.

## Gotchas
- Don't put a `//` comment mid-line before more code: it swallows the rest. It broke the wall once; a quick syntax check catches it: `node -e "new Function(require('fs').readFileSync(F,'utf8').split('<script>')[1].split('</script>')[0])"`.
- The software renderer is slow:
  - Real-time waits in checks need slack (`waitForFunction`), never fixed short sleeps.
  - The pool's rhythm tests step the go exactly instead.
- Blur the clicked menu button on start, or Space presses it again.
- `.gitignore` ignores `*.png`: add shots with `git add -f`.
- Camera framing in portrait is tight; check shots after any camera change.

## How to test
- three.js: `mkdir -p /tmp/cadet-work/three && cd /tmp/cadet-work/three && npm pack three@0.128.0 && tar xzf three-0.128.0.tgz` (or set `THREE_JS=path`).
- Run each check: `NODE_PATH=$(npm root -g) node tools/<name>_proto_check.js`. Each takes 1-2 minutes and prints ALL OK.

## Open questions for the user (via the lead)
- Are the paces right (kayak ~50-90 s a lap, wall 10-15 moves, pool 50-80 s)?
- Is the camera framing good on a real phone?
- Wall: is .28 m enough reach to feel like climbing?
- Pool: is the rhythm generous enough?
