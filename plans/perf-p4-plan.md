# End-of-Pillar-4 optimization pass: plan

The performance engineer, 2026-10-17, measured on the 0.60.3 candidate (claude/cand-0603 8b4bbd6). The user asked for "some serious optimization at the end of Pillar 4". Goal: noticeably smoother on phones and a faster first load, with every cadet_test difference explained.

## What the measurements say

All on a phone-sized view (390×844), headless Chromium with software rendering. Draw calls and object counts are exact. Times are from a desktop CPU; a mid-range phone is roughly 4 to 5 times slower.

**1. The shadow pass costs more draws than the picture.** The 450 budget counts only the picture (the main pass). Counting every real draw sent to the graphics chip:

| Moment | Picture | Shadows | Total |
| --- | --- | --- | --- |
| Sunday dinner, mess, usual zoom | 213 | 264 | 477 |
| Sunday dinner, zoomed out | 347 | 471 | 818 |
| Quiz night, bow lounge, usual zoom | 211 | 261 | 472 |
| Junior common room, usual zoom | 198 | 459 | 657 |
| Junior common room, zoomed out | 429 | 646 | 1,075 |

Every piece of furniture that casts a shadow is drawn a second time into the shadow map, piece by piece (512 shadow-casting meshes on Deck 3, 667 on Deck 4).

**2. Game code per frame: about 3.1 ms on a desktop at Sunday dinner (65 people), so roughly 12 to 15 ms on a mid phone.** That leaves little of a 16.7 ms frame for drawing. About a third of it is three.js recomputing the position of every object in the scene every frame (`updateMatrixWorld`): 1,363 objects on Deck 3 and 1,951 on Deck 4, all marked "may move". Almost all of them never move, and 112 to 161 of them are empty groups left behind after the furniture was merged. The crowd's own skeletons (about 21 bones a person) have to move, and they're already updated separately.

**3. First load: about 6.5 s headless.** Most of it is the first frame: uploading textures and compiling shaders, which is software work here, so it isn't comparable to a phone's GPU. Then come painting the procedural textures (about 1 s: `grain` draws a random number for every pixel, which keeps the textures deterministic) and parsing the 3 MB script (about 0.8 s).

**4. File size: 3.01 MB, of which the dialogue (section 22: VOICE about 0.70 MB, LINES about 0.41 MB) is 1.1 MB.** The whole file gzips to 0.85 MB. If the artifact host serves it compressed (most do), a phone downloads under 1 MB.

**5. Memory: flat over deck round trips** (547 geometries, 42 textures). The heap after load is about 105 to 125 MB. A long-play check (a week of days and deck changes) isn't in perf_check yet; item 6 adds it.

## The changes, safest first

| # | Change | Expected gain | Section, owner | Risk |
| --- | --- | --- | --- | --- |
| 1 | **Shadow stand-ins.** After a deck is built, copy the geometry of everything that never moves and casts a shadow (the merged furniture, walls, hull) into a few depth-only meshes, one per 8×8 m block of the deck. Put them on a layer only the sun's shadow camera sees, and turn shadow casting off on the originals. Moving or fading things (doors, crowd, carts, props, tall furniture while it fades) keep their own shadows. | Shadow pass from 260–650 draws to about 30–60. Total draws at Sunday dinner from about 477 to about 260; junior common room zoomed out from 1,075 to about 480. Same shadows. | 4c (deck build) and 5 (the sun's layer). Mine, as with 0.27.20–22, if the lead agrees. | Low to medium. cadet_test should stay identical (same depth geometry); I'll explain any edge pixels. |
| 2 | **Freeze what never moves.** After the build, mark the furniture, walls and wall decor "doesn't move" (`matrixAutoUpdate = false`, computed once), except anything that spins, slides, pulses or fades. Drop the empty groups left after merging. | Roughly a third of the per-frame game code at busy moments: about 1 ms desktop, 4 to 5 ms on a mid phone. | 4c. Mine. | Low. Pictures identical. |
| 3 | **Measure like a phone.** perf_check adds a 4× CPU slowdown (Chrome's throttle, standing in for a mid phone), a long-play run (7 ship days, 30 deck changes, heap and memory at the end), and a count of real draws including shadows. | Numbers that match what the user feels. | perf_check.py. Mine. | None. |
| 4 | **Dialogue as JSON text.** Store the baked VOICE and LINES blocks as one `JSON.parse('…')` string each instead of JavaScript object literals. Browsers parse JSON several times faster than code, and the data is identical, so determinism and tests are unchanged. | A few hundred ms off first load on a phone, and less parse memory. | 22, the content/dialogue owner (it's generated, so it's a change to their generator). | Low. |
| 5 | **Check the host compresses.** Confirm the playable link is served gzipped. If it is, the download is already 0.85 MB and nothing more is needed. If not, tell the lead before anything clever. | Up to 2 MB less to download. | The publisher / lead. | None. |
| 6 | **Cache the painted textures.** Keep the painted canvases (floors, walls, fabrics) in the browser's storage after the first load, keyed by build number. The second and later opens skip about 1 s of painting (more on a phone). Same pixels, because they're the same canvases. | Faster every open after the first. | 2 and 4b (textures and shared kit). The deck architect, or me with their OK. | Medium: storage quotas, and a cache keyed wrongly would show old textures. Later, after 1 to 4. |
| 7 | (Optional; the user decides.) **Smaller shadow map on phones:** 1,024 instead of 2,048 on small screens. | Less GPU fill per frame. | 5. | Visible: softer, blockier shadows. Only if items 1 and 2 aren't enough. |

Not proposed: updating far-away crowd people at half rate (cheap, but risks visible stutter), and thinning decor (the user prefers no popping).

## Order and checks

Items 3 and 1 first (measure, then the biggest win), then 2, each as its own build (0.27.25 and up) with cadet_test, deck_check, day_check 1, events_check and perf_check. Items 4 and 5 go to their owners through the lead. Item 6 comes after the user plays the result. A short before/after table goes to the lead with each build.
