# Tea corner look test (LT1)

A standalone page for judging a higher-fidelity art style. **The game is not changed.**

- Published page: https://claude.ai/artifact/XL3oEyLn2eBrJWzhZnQzLT
- Source: `look-test.src.html` (the page) + `tea-corner.json` (the room, exported from the game).
- Build the publishable page: `python3 plans/look-test/build.py` makes `tea-corner-look-test.html` (5.3 MB, not committed: it is the two files above put together).
- Re-export the room from the game: `CADET_CHROME=/opt/pw-browsers/chromium python3 plans/look-test/export/export.py` (sets 13:08 on Day 1, seats Calder in the armchair, Pell on the stool and Halloran standing, as full figures, then copies every game triangle in the room with its material, texture, lights, renderer settings and camera).
- Screenshots at any size: `python3 plans/look-test/export/shoot.py 412x960,792x1080 012 close` (three.js served from `$CADET_WORK/three`, as for cadet_test).

## What each level is

- **Level 0**: the game's own triangles, colours, textures, lights (sun with its 2048 shadow map over the whole deck, sky light, the lamp), ACES tone at 1.05, the game's camera. Matches the game's picture (compare `shots/L0_412x960_game.png` with `shots/game_412x960_reference.png`).
- **Level 1**: same triangles. High-range picture with 4x smoothing, glow (UnrealBloomPass), a grading pass (ACES, cool shade, warm light, a little vignette and dither), soft reflections from a generated room (RoomEnvironment), the sun's shadow map fitted to the room, a warm shadow-casting pool under the lamp, cool light through the porthole, baked contact shade (one mesh of soft dark pools under furniture and along the wall feet). No screen-space AO: it would draw the scene twice more a frame.
- **Level 2**: Level 1 plus code-made kit replacing the game's table, armchair, stool, hot-water unit and lamp (the game's triangles in those boxes are trimmed out), painted deck boards, skirting and rails, panel seams, a lit sign, a menu card, the tea rota, mug hooks, kettle, biscuit tin, sugar jar, steam, stars through the porthole. Merged per material like the game. Crew unchanged.

## Measured (headless Chromium, software renderer, 412x960, Close view)

| Level | Draw calls | Triangles | Frame time (software GPU) |
|---|---|---|---|
| 0 | 163 | 100k | 120-200 ms |
| 1 | 232 | 133k | 430-650 ms (about 3x Level 0) |
| 2 | 310 | 175k | 490-790 ms (about 3.5-4x Level 0) |

Draw calls and triangles count every pass of a frame (shadow maps and full-screen steps included). Frame times here come from a software renderer, so only the ratios mean anything; the page's own panel shows the real numbers on whatever device opens it. The room alone has 55k triangles, 45k of them the three crew.

The game's view of Deck 5 in the same shot: about 230 draw calls and 130k triangles (budget 450 on phones).
