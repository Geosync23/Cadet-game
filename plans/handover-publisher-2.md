# Handover: publisher 2 (PUB2)

Session session_01GKuymkDxLVyt4rjtcJxdab, branch `claude/publish-26` (this note only), on the **new claude.ai account**. Reports to **lead 41** (session_01GKuymjWR1dqfbCw1MyEP9j). Read `plans/handover-publisher-1.md` first: the recipe, the Dev first-line script, the phone test and the user's save rules are all there and unchanged.

## Pages
| Page | Link | Version / build | Capabilities | Rule |
|---|---|---|---|---|
| Playtest (current, new account) | https://claude.ai/artifact/7hQ14AcwZHCi5EvL1AKiMU | v1 = 0.94.0 (staging-0.94.0 1d5e8845, game 5f4c5415…a0f), version id 1793096315-b01e | downloads | updated each release |
| Dev (current, new account) | https://claude.ai/artifact/KEyaHvon6ZaVHHFRdAe18m | v1 = 0.94.0, version id 1793096317-db3b | downloads | updated each release |
| Playtest (old account) | https://claude.ai/artifact/3HqM5XiXaHXzgrpq7JbesJ | v7 = 0.93.3 | downloads | old account: can't be updated from here |
| Dev (old account) | https://claude.ai/artifact/9ZWAgqiZCvkJvVjjhjVkEr | v7 = 0.93.3 | downloads | old account |
| Dev: promotion preview (old account) | https://claude.ai/artifact/AvpWrMumcGiw4UYUpXd2X5 | v1 = p5s5-promo 5703dfb6 | downloads | old account |
| Dev (old account, the user's longer save) | https://claude.ai/artifact/6daNCLCJAcsLCZn27CEthq | v11 = 0.92.2 | none | old account; never publish over it |
| Playtest (old account, a save of the user's) | https://claude.ai/artifact/Wn6mUGcxatoWVqhCNTa1vs | v11 = 0.92.2 | none | old account; leave alone |

New links start with no save. To carry a game across: on the old page, Saves, Download my save; on the new page, Saves, Load a save file.

## Sources (scratchpad of this session; gone in a new session)
Playtest `play/starship-cadet-playtest-0.94.0.html` (title `Starship Cadet Playtest 0.94.0`), Dev `dev/starship-cadet-dev-0.94.0.html` (title `Starship Cadet Dev` + the Dev first-line script). Diff against the game: only those lines. A new session publishes updates by passing the `url` (read the page first), with `capabilities: {downloads: true}` or omitted.

## 0.94.0 test (2026-10-27)
Scan clean (only cdnjs three.js r128 and the SVG namespace; no fetch/eval/iframe and the like). Phone size 390x844 with touch, headless Chromium, local copies of both pages with the eval hook: loads, manifest signed, HUD up, GAME_BUILD 0.94.0, Dev page gets `#dev` (DEV badge on), Settings opens with the three-way Doors row, Saves shows Download my save and Load a save file, no console errors on either page. Not tested: the live claude.ai download prompt (still a loose end from PUB1).
