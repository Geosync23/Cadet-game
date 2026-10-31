# Handover: publisher 3 (PUB3)

Session session_014zyJYQ6fZqmqTjgzdCaumh, branch `claude/publish-pub3` (this note and the two test scripts only). Reports to **lead 47** (session_014zyJYM4mt9ZDCD5H9JZDtN, claude/lead-47). Read `plans/handover-publisher-1.md` (the recipe, the user's save rules) and `plans/handover-publisher-2.md` (branch claude/publish-26) first.

## This account is new
This session runs on the user's newest claude.ai account. Every link in PUB1's and PUB2's notes belongs to an earlier account: this account **cannot update them, and must never publish over them**. New pages on this account start with no save; to carry a game across, on the old page use Saves, Download my save, and on the new page Saves, Load a save file.

## Pages on this account
| Page | Link | Version / build | Capabilities | Rule |
|---|---|---|---|---|
| Playtest (current) | https://claude.ai/artifact/CqUGjQXerhSKxuu4umhK41 | v1 = 0.99.4, version id 1793458485-59d3 | downloads | updated each release |
| Dev (current) | https://claude.ai/artifact/Sm86UjQMH1NmBj5ybNnB2b | v1 = 0.99.4, version id 1793458487-af6d | downloads | updated each release |

## Old accounts' links (untouchable from here)
| Page | Link | Last known |
|---|---|---|
| Playtest (previous account) | https://claude.ai/artifact/7hQ14AcwZHCi5EvL1AKiMU | v9 = 0.99.3 |
| Dev (previous account) | https://claude.ai/artifact/KEyaHvon6ZaVHHFRdAe18m | v9 = 0.99.3 |
| 0.99.1 on its own link (previous account) | https://claude.ai/artifact/YaJsaCgvpb3QXvcgestTSt | v1 = 0.99.1 |
| Controller test (previous account) | https://claude.ai/artifact/JV6CSUWQHftaDkSisYjQCG | 0.96.0 pad |
| Title screen preview (previous account) | https://claude.ai/artifact/GLSzgGfn55Kk9LFCaoGevR | title-on-099 |
| Dev, the user's longer save (oldest account) | https://claude.ai/artifact/6daNCLCJAcsLCZn27CEthq | v11 = 0.92.2, never publish over it |
| Playtest, a save of the user's (oldest account) | https://claude.ai/artifact/Wn6mUGcxatoWVqhCNTa1vs | v11 = 0.92.2, leave alone |
| Others of the oldest account | 3HqM5XiX..., 9ZWAgqiZ..., AvpWrMum..., G1fpE2Ye..., RMgibsuh..., CTLouY4D... | see PUB1/PUB2 notes |

## 0.99.4 release (2026-10-31)
The user: "Yes, publish 0.99.4" (via lead 47). Source claude/staging-0994 596712bc, game file sha256 a01d1a4c7864801b19541d70b9358089fba1ed84cee5145ca85931ea3012bc4a (checked, matches), GAME_BUILD 0.99.4.
- Pages: Playtest title `Starship Cadet Playtest` (the lead's wording; no version number in the title from now on); Dev title `Starship Cadet Dev` plus PUB1's Dev first-line script. `diff` against the game: only those lines. Published page sha256: Playtest 7f2640b0...0043, Dev 57a7d4e9...fa8c.
- Scan: only `<script src>` is cdnjs three.js r128; the only URLs are that and the SVG namespace; no fetch( call (the two hits are words in comments), no XMLHttpRequest/WebSocket/eval/new Function/iframe/img/link/object/embed.
- Phone test, 390x844 with touch, headless Chromium, local copies with the eval hook: PASS on both, 0 console errors.
  - Playtest (opened with #title): tap to wake shows, NEW GAME after a tap, manifest, Sign and go aboard, HUD up, GAME_BUILD 0.99.4, Saves shows Download my save and Load a save file.
  - Dev: the first-line script sets #dev, GAME_BUILD 0.99.4, manifest, HUD, Saves as above, Dev panel opens and the Jump to tab switches on.
- Not tested: the live claude.ai download prompt (still a loose end since PUB1).

## How to rebuild and test (scripts in tools/publish/ on this branch)
1. `git show <commit>:starship-cadet.html > src.html`, sha256sum it against the lead's.
2. `python3 build.py src.html` (run from a folder with play/ and dev/): writes play/starship-cadet-playtest.html and dev/starship-cadet-dev.html, asserting each target occurs once.
3. Test copies: insert `window.__sc = src => eval(src);\n` before the last `})();`, into t/test-play.html and t/test-dev.html. `npm pack three@0.128.0 && tar xzf three-0.128.0.tgz` beside phone.js (cdnjs is blocked in the container).
4. `NODE_PATH=$(npm root -g) node phone.js t/test-play.html '#title' play` and `... t/test-dev.html '' dev` (about a minute each; run them one after the other, with `timeout 150`).
Gotchas: the device stays locked until the flag `intro.device` is set (`introFlagSet('intro.device')`); its first open shows the boot screen, so call `deviceShow('saves')` twice; the Saves buttons are drawn in capitals, so match their words ignoring case.
5. Publish updates from this session by the same file path; from a new session read each page first (Artifact read, `url`), then publish with `url` and `capabilities: {downloads: true}` (or omit capabilities to keep it).
