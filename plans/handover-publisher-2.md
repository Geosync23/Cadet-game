# Handover: publisher 2 (PUB2)

Session session_01GKuymkDxLVyt4rjtcJxdab, branch `claude/publish-26` (this note only), on the **new claude.ai account**. Reported to lead 41; now **lead 42** (session_01GKuymjnCHnpwDqB94PVwmV, claude/lead-42). Read `plans/handover-publisher-1.md` first: the recipe, the Dev first-line script, the phone test and the user's save rules are all there and unchanged.

## Pages
| Page | Link | Version / build | Capabilities | Rule |
|---|---|---|---|---|
| Playtest (current, new account) | https://claude.ai/artifact/7hQ14AcwZHCi5EvL1AKiMU | v8 = 0.99.2 (staging-0992 d180a704 = 60d477e8 + docs, game 27d605e7…3920), version id 1793321288-c15c (v7 = 0.99.1, v6 = 0.99.0, v5 = 0.98.0, v4 = 0.97.0, v3 = 0.96.0, v2 = 0.95.0, v1 = 0.94.0) | downloads | updated each release |
| Dev (current, new account) | https://claude.ai/artifact/KEyaHvon6ZaVHHFRdAe18m | v8 = 0.99.2, version id 1793321290-5cf0 (v7 = 0.99.1, v6 = 0.99.0, v5 = 0.98.0, v4 = 0.97.0, v3 = 0.96.0, v2 = 0.95.0, v1 = 0.94.0) | downloads | updated each release |
| Playtest (old account) | https://claude.ai/artifact/3HqM5XiXaHXzgrpq7JbesJ | v7 = 0.93.3 | downloads | old account: can't be updated from here |
| Dev (old account) | https://claude.ai/artifact/9ZWAgqiZCvkJvVjjhjVkEr | v7 = 0.93.3 | downloads | old account |
| Dev: promotion preview (old account) | https://claude.ai/artifact/AvpWrMumcGiw4UYUpXd2X5 | v1 = p5s5-promo 5703dfb6 | downloads | old account |
| Dev (old account, the user's longer save) | https://claude.ai/artifact/6daNCLCJAcsLCZn27CEthq | v11 = 0.92.2 | none | old account; never publish over it |
| Playtest (old account, a save of the user's) | https://claude.ai/artifact/Wn6mUGcxatoWVqhCNTa1vs | v11 = 0.92.2 | none | old account; leave alone |

New links start with no save. To carry a game across: on the old page, Saves, Download my save; on the new page, Saves, Load a save file.

The scratchpad files keep their 0.94.0 names (same path = same link); `build.py <src> <version>` and `phone.js` there rebuild and test.

## Sources (scratchpad of this session; gone in a new session)
Playtest `play/starship-cadet-playtest-0.94.0.html` (title `Starship Cadet Playtest 0.94.0`), Dev `dev/starship-cadet-dev-0.94.0.html` (title `Starship Cadet Dev` + the Dev first-line script). Diff against the game: only those lines. A new session publishes updates by passing the `url` (read the page first), with `capabilities: {downloads: true}` or omitted.

## 0.94.0 test (2026-10-27)
Scan clean (only cdnjs three.js r128 and the SVG namespace; no fetch/eval/iframe and the like). Phone size 390x844 with touch, headless Chromium, local copies of both pages with the eval hook: loads, manifest signed, HUD up, GAME_BUILD 0.94.0, Dev page gets `#dev` (DEV badge on), Settings opens with the three-way Doors row, Saves shows Download my save and Load a save file, no console errors on either page. Not tested: the live claude.ai download prompt (still a loose end from PUB1).

## 0.95.0 (2026-10-28)
GO from lead 42 (BM19 on hold). sha256 checked, scan clean, published over the same two links as v2. Phone test 390x844 on both: PASS (same checks as 0.94.0, GAME_BUILD 0.95.0, 0 console errors). 6daN... untouched.

## 0.96.0 controller test (2026-10-28)
Lead 44 asked for a separate page for the user's real-controller test (not the release): https://claude.ai/artifact/JV6CSUWQHftaDkSisYjQCG v1 = claude/staging-pad fe11cd66 (game 33292500…129e, PAD_ON true), {downloads}, title "Starship Cadet 0.96.0 controller test", no Dev. Scratchpad source pad/starship-cadet-0.96.0-controller-test.html. Load check at 390x844: PASS, 0 console errors. Lead 44 is the lead now (session_01GKuymj3tKpX7xwDZwBh8RM).

## 0.96.0 release (2026-10-28)
The user said publish (via lead 44). sha256 checked, published over the same two links as v3, {downloads}. Phone check 390x844 on both: PASS, 0 console errors. 6daN untouched.

## 0.97.0 release (2026-10-29)
The user said publish (via lead 44). sha256 checked, published over the same two links as v4, {downloads}. Phone check 390x844 on both: PASS, 0 console errors; on Dev the phone.js script now also opens the Dev panel (devmodeOpen(true)) and clicks the Jump to tab (.dmTabs button[data-tab=jump]). 6daN untouched.

## Title screen preview (2026-10-29)
Lead 45 asked for a preview page (not a release): https://claude.ai/artifact/GLSzgGfn55Kk9LFCaoGevR v1 = claude/title-on-099 b980518 (game 4390780e…0303, TITLE_ON true, GAME_BUILD still 0.97.0), {downloads}, title "Title screen preview". Scratchpad source title/title-screen-preview.html. The title screen is hidden under automated browsers (navigator.webdriver) unless the link has #title: the headless check opens it with #title. 390x844: shows, 0 console errors. Lead 45 is the lead now (session_01GKuymnu4NeXJhwPe21FWk7).

## 0.98.0 release (2026-10-29)
The user OK'd it (via lead 45). sha256 checked, published over the same two links as v5, {downloads}. Phone check 390x844 on both: PASS, 0 console errors (Dev: Jump to tab opens). 6daN untouched.

## 0.99.0 release (2026-10-29)
The user said "Publish .99" (via lead 46, session_01GKuymiks9CC1WYr2may5nM). sha256 checked, published over the same two links as v6, {downloads}. Phone check 390x844 on both: PASS, 0 console errors; the title screen is on from 0.99.0 (hidden under automated browsers and in Dev mode; checked on Playtest with #title, titleplay.js). 6daN untouched.

## 0.99.1 release (2026-10-29)
The user pre-approved it (via lead 46). sha256 checked, published over the same two links as v7, {downloads}. Phone check 390x844 on both: PASS, 0 console errors. The title now opens on "> TAP TO WAKE THE TERMINAL"; titleplay.js taps once (195,600) and screenshots both. 6daN untouched.

## 0.99.2 release (2026-10-30)
The user pre-approved it (via lead 46). sha256 checked, published over the same two links as v8, {downloads}. Phone check 390x844 on both: PASS, 0 console errors. titleplay.js now also taps NEW GAME and screenshots (newgame.png): the shuttle manifest on a dark screen, no old deck behind it. 6daN untouched.

## 0.99.1 on its own link (2026-10-30)
The user asked for a link to 0.99.1 (via lead 46): https://claude.ai/artifact/YaJsaCgvpb3QXvcgestTSt v1 = claude/staging-0991 bc4579aa (game 8e4ac545…2d9d), {downloads}, title "Starship Cadet 0.99.1", Playtest style (no Dev). Scratchpad source v0991/starship-cadet-0.99.1.html. 390x844 load + title tap + New game: PASS, 0 console errors.
