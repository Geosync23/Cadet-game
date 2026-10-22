# Look test (LT1): Bunk 1, and the tea corner before it

A standalone page for judging a higher-fidelity art style. **The game is not changed.**

- Published page (Bunk 1, the room you wake in): https://claude.ai/artifact/XL3oEyLn2eBrJWzhZnQzLT. Version 1 of the same link was the Deck 5 tea corner; the user chose the bunk room instead, so version 2 replaced it.
- Sources: `bunk-room.src.html` + `bunk1.json` (published), `tea-corner.src.html` + `tea-corner.json` (kept as evidence).
- Build: `python3 plans/look-test/build.py` makes `bunk-room-look-test.html` and `tea-corner-look-test.html` (5 MB each; not committed, see `.gitignore`).
- Re-export from the game: `python3 plans/look-test/export/export_bunk.py` (Bunk 1) or `export/export.py` (tea corner). Both need playwright and three r128 in `$CADET_WORK/three`, as for cadet_test.py. `export/export.js` copies every game triangle in a box (`window.__RG`) with its material, texture, lights, tone settings and camera; `window.__LIGHTS_ONLY` returns just the lights (for the night set).
- Screenshots: `LT_OUT=<dir> python3 plans/look-test/export/shoot.py 412x960,792x1080 012 close day|night` (three.js served from `$CADET_WORK/three`; `LT_PAGE=tea-corner-look-test.html` for the tea corner).
- Answers: the page keeps the user's answer in its shared store (`db`, collection `answers`: pick, text, by, at, seen). Read them with the ArtifactData tool (`list`, collection `answers`, url above).

## Bunk 1 (Deck 4, room 'a', tiles 6..10 x 0..3)

Staged on Day 1 in the morning: you at your wardrobe, Tomas up by his bunk, Tran asleep on the berth above his, all as full figures (Lukas is not on the deck at that time; Santos and Quaye are moved out). The night set is the game's own `applyLight(1)` for the same room: sky light and sun down, warmer sun, darker background. The game has no real lamps in this room: its two sconces are glow sprites only.

- **Level 0**: the game's triangles, colours, textures, glow sprites, sun shadow (2048 map round the player), ACES at 1.05 by morning and 1.03 by night. Compare `shots/bunk/L0_792x1080_game_day.png` with `shots/bunk/bunk_game_day_412x960.png` (the game).
- **Level 1** (lamp light and mood): same triangles. The sconces become real lights; at night a reading lamp over your berth with its own shadow, starlight through the hull window, bluer shade and warmer lamps in the grade; by morning a cool ceiling light. Reflections from a generated room (dimmed at night), the sun's shadow fitted to the room, baked contact shade, glow, grading.
- **Level 2** (shapes and surfaces): Level 1 plus code-made kit in the game's colours (through `col()`): rounded bunks with ladders, mattresses, sheets, pillows, knitted duvets that fold over the edges (the spare berth made up tight), locker doors with vents, handles, status light and your name on tape, footlockers with metal corners and berth numbers, lino tiles, skirting, a lit Bunk 1 sign, Tomas's star map, and your things (book, device, headphones, photo, boots, kit bag, mug, towel, a bedside mat). Merged per material.

### Measured (headless Chromium, software renderer, 412x960, Close view)

| Level | Morning: draw calls / triangles | Night: draw calls / triangles | Frame time vs Level 0 (software) |
|---|---|---|---|
| 0 | 183 / 104k | 183 / 104k | baseline (130-250 ms) |
| 1 | 199 / 104k | 255 / 138k | about 3x |
| 2 | 229 / 177k | 290 / 244k | about 4x |

Counts include every pass (shadow maps, glow and grade steps). Night costs more because the reading lamp's shadow redraws the room. The same counts at 792x1080 and 1280x800. The game's view of Deck 4 in the same shot: about 200 draw calls and 285k triangles (budget 450 on phones). Frame times are from a software renderer, so only the ratios mean anything; the page's own panel shows real numbers on the device that opens it.

## Tea corner (Deck 5, version 1 of the page)

Same method; staged at 13:08 with Calder in the armchair, Pell on the stool and Halloran standing. Measured at 412x960, Close: Level 0 163 draw calls / 100k triangles; Level 1 232 / 133k (about 3x the frame time); Level 2 310 / 175k (about 3.5-4x). The room alone was 55k triangles, 45k of them the three crew. Screenshots in `shots/tea-corner/`.
