# Turn 4 (furniture that differs only in colour, drawn together): what changes on screen

RB1, 2026-10-29, for lead 45 and the user. Build: claude/opt-098-render 48d4d34 against the turn 3 build 8d7a314.

**Gain:** Sunday dinner in the mess, wide phone view: furniture draws 142 to 85, the picture's draw calls 357 to 300.

**What differs:** 252 shots (every deck, up to 6 rooms each, the four phone views, day and night) plus cadet_test's 15.
12 of the 252 and 2 of the 15 differ, by **1 to 8 pixels each** (14 shots, 26 pixels in all). The largest change is
63 of 255 shades, on a single pixel. Every changed pixel is on a corner or edge where two surfaces meet at exactly the
same depth. Which one shows there depends on which is drawn last, and the merge changes the drawing order
(vertex-coloured furniture needs its own shader, and three.js draws shader by shader). Nothing is recoloured, moved or
lost; colours and shading are otherwise the same to the shade.

`turn4-before-after.png`: one row per shot: where (pink box), before x8, after x8, the changed pixels in white.

**Why it can't be made exact here:** keeping the old order would mean controlling three.js's drawing order for the
whole scene. Turn 3 could be exact because a body's draws had no ties with anything else.
