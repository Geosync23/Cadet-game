# Handover: publisher 1 (PUB1)

Session session_01GnpjFR6oumvuvTrmcXSqeg, branch `claude/publish-25` (this note only). Started under lead 25; now reports to **lead 40** (session_01NXybH7NNqM8M4ngiyidq6m). **At the stopping point (the user's call, 2026-10-26): both current pages on 0.93.3, nothing published after that.**. Before taking orders from a new lead or build master, check that TEAM.md on the previous lead's branch records the handover, or ask the previous lead.

## The user's standing rules for the pages
- **The old Dev page https://claude.ai/artifact/6daNCLCJAcsLCZn27CEthq (Version 11 = 0.92.2) holds the user's longer playthrough save. Never publish over it unless the user explicitly says so** (lead 34, 2026-10-24).
- The old Playtest page https://claude.ai/artifact/Wn6mUGcxatoWVqhCNTa1vs (Version 11 = 0.92.2) also keeps a save of the user's: the user asked (2026-10-24, via lead 33) that it not be updated. Leave both Version 11 pages alone.
- Publish only on a lead's go (or a build master relaying it), from the exact commit named, after checking the full sha256 of the game file. If anything differs, stop and tell the lead.

## Pages (all private to the user's account; sharing is the user's, from each page's Share menu)
| Page | Link | Now | Scratchpad source (same path = same link) |
|---|---|---|---|
| Playtest (current) | https://claude.ai/artifact/3HqM5XiXaHXzgrpq7JbesJ | v7 = 0.93.3 (staging-0.93.3 19400976, game ec93b94d…d085), capabilities {downloads: true} | play-0.92.3/starship-cadet-playtest-0.92.3.html |
| Dev (current) | https://claude.ai/artifact/9ZWAgqiZCvkJvVjjhjVkEr | v7 = 0.93.3, capabilities {downloads: true} | dev-0.92.3/starship-cadet-dev-0.92.3.html |
| Playtest (old, user's save) | https://claude.ai/artifact/Wn6mUGcxatoWVqhCNTa1vs | v11 = 0.92.2, **don't touch** | play/starship-cadet-playtest.html |
| Dev (old, user's longer save) | https://claude.ai/artifact/6daNCLCJAcsLCZn27CEthq | v11 = 0.92.2, **don't touch** | dev/starship-cadet-dev.html |
| Sim Bay Preview | https://claude.ai/artifact/G1fpE2YeMtPukqTZ2J3u77 | v1 = claude/rec-simbay cb4387e8 | simbay-preview/sim-bay-preview.html |
| Appointments pitch (db: answers/user) | https://claude.ai/artifact/CTLouY4DK2gFuWBF8YwS3L | v1 = claude/appointments-pitch 52dd1cc1 | appointments/appointments-pitch.html |
| Dev: promotion preview (#dev.p5s5 set by its first-line script; downloads) | https://claude.ai/artifact/AvpWrMumcGiw4UYUpXd2X5 | v1 = claude/p5s5-promo 5703dfb6 (GAME_BUILD 0.93.2, game 2731893e…9337) | promo/starship-cadet-dev-promotion-preview.html |
| Sim Flight Prototype | https://claude.ai/artifact/RMgibsuh2KdxcF3kd8vuJr | v2 = claude/simflight 7bf86392 | simflight/sim-flight-prototype.html |

History of the old pairs: 0.64.12 (v1), 0.64.13, 0.64.14, 0.64.15, 0.64.16, 0.64.17 (v6), rolled back to 0.64.16 at the user's request (v7), 0.91.0, 0.92.0, 0.92.1, 0.92.2 (v11). Then 0.92.3 went on new links (the user's wish, to keep the old saves), and 0.92.4 updated those.

## The recipe
1. `git fetch origin <branch>`; `git show <commit>:starship-cadet.html > <scratchpad>/srcN.html`; `sha256sum` it against the lead's sha. Check `GAME_BUILD` and any switches the lead names (`grep -n -E '\b(POINT_ON|GUIDE_ON|PAD_ON|EV_LINE_ON|EVENTS_ON|SIM_BAY)\s*=[^=]'`; each set once).
2. Scan: only `<script src>` is cdnjs three.js r128; no fetch/XMLHttpRequest/WebSocket/eval/new Function/iframe/img/link/object/embed; the only URLs are that and the SVG namespace. The `atob` calls are save decoding and the one `<form>` is the shuttle name manifest.
3. A short Python replace that asserts each target occurs once: Playtest title `Starship Cadet Playtest X.Y.Z`; Dev title `Starship Cadet Dev` plus, right after `<meta charset="utf-8">`, the first-line script `<script>/* published Dev page: Dev mode always on (not in the repo) */try{if(!location.hash.slice(1).split(".").some(t=>(t.includes("-")?t.slice(0,t.indexOf("-")):t)==="dev"))history.replaceState(null,"",location.pathname+location.search+"#dev");}catch(e){}</script>`. `diff` against the source to prove nothing else changed.
4. Publish to the page's scratchpad path (above) with a `label` of the build; a new path makes a new link. Report the link, version and version id to the lead.
- The Sim Bay Preview turns the sim bay on with `#simbay` (the build reads it, line ~9025), set by a first-line script like the Dev one, plus a small fixed "Sim Bay Preview · not yet fully tested" label; no game code changed.
- Small standalone pages (the sim flight prototype) are published byte for byte; read the whole file (or the whole diff from the last version read) first.
- The game file (~6.4 MB) is never printed whole into context; the 16 MB limit is far off.
- From a new session the scratchpad is gone: read each page first (Artifact action read, `url`), then publish with `url`.
</content>
</invoke>
<invoke name="Bash">
<parameter name="command">cd /home/user/Cadet-game && git add plans/handover-publisher-1.md && git commit -q -m "Publisher 1 handover: all pages, the user's save-keeping rules, the recipe

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01GnpjFR6oumvuvTrmcXSqeg" && git push -q -u origin claude/publish-25 2>&1 | tail -1; git log --oneline -1- **Phone-size check** (when a lead asks): headless Chromium (Playwright, NODE_PATH=$(npm root -g)) at 390x844 with touch, opening the scratchpad file; cdnjs is blocked in the container, so serve three.js from `npm pack three@0.128.0` with page.route, as cadet_test.py does. A fresh game opens on the shuttle manifest: fill the name and click "Sign and go aboard" to see the HUD. The build number is on screen only in Dev mode's Speed card.
- **From 0.93.2 both current pages declare `capabilities: {downloads: true}`** (the Saves app's Download my save). A non-empty capabilities object replaces the stored set: keep passing it on every republish, or omit `capabilities` to carry it forward.
- **Sound test**: the game mutes itself under automated browsers (navigator.webdriver) unless the link has `#sound` (`#dev.sound` on Dev); for Settings, Music and Saves, use a test-only copy with cadet_test.py's eval hook (`window.__sc = src => eval(src);` before the last `})();`), `introFlagSet('intro.device')`, then `deviceShow('settings' | 'music' | 'saves')`. Scripts: tools/build_pages.py, tools/instrument.py, tools/sound2.js in the scratchpad (rebuild them from this note in a new session).
- Since 0.93.3 Settings has a three-way **Doors** row ("Doors. Private rooms are…": All open by themselves / Private rooms: tap to open / All doors: tap to open) in place of 0.93.2's Auto doors On/Off; test for that wording.
- Loose end for the user: the live claude.ai download prompt (Saves → Download my save) has never been seen by a publisher; the local test only reaches the plain-link fallback.
- The game's switches read `?query` OR `#hash` tokens (`#a.b-c`), but in the claude.ai viewer only the plain `#hash` reaches the page; a preview page sets its tokens with a first-line `history.replaceState` script, as the Dev and promotion-preview pages do.

## Moving to another account (lead 40, 2026-10-27)
The user is moving the project to another account. Every live page below is owned by **this** account. A session on the new account **cannot update any of them**: it must publish **new links**, unless this account shares edit access to a page with the new account from that page's Share menu. Saves live in each page's own browser storage, so a new link starts with no save (Saves → Download my save on an old page, then Load a save file on the new one, carries a game across).

| Page | Link | Version / build | Capabilities | Rule |
|---|---|---|---|---|
| Playtest (current) | https://claude.ai/artifact/3HqM5XiXaHXzgrpq7JbesJ | v7 = 0.93.3 (staging-0.93.3 19400976) | downloads | updated each release |
| Dev (current) | https://claude.ai/artifact/9ZWAgqiZCvkJvVjjhjVkEr | v7 = 0.93.3 | downloads | updated each release |
| Dev: promotion preview | https://claude.ai/artifact/AvpWrMumcGiw4UYUpXd2X5 | v1 = claude/p5s5-promo 5703dfb6 (0.93.2 base, #dev.p5s5) | downloads | early preview |
| Dev (old, the user's current save) | https://claude.ai/artifact/6daNCLCJAcsLCZn27CEthq | v11 = 0.92.2 | none | **never publish over it** unless the user explicitly says so |
| Playtest (old, a save of the user's) | https://claude.ai/artifact/Wn6mUGcxatoWVqhCNTa1vs | v11 = 0.92.2 | none | leave alone |

Also live on this account (no capabilities unless noted): Sim Bay Preview https://claude.ai/artifact/G1fpE2YeMtPukqTZ2J3u77, Sim Flight Prototype https://claude.ai/artifact/RMgibsuh2KdxcF3kd8vuJr, appointments pitch https://claude.ai/artifact/CTLouY4DK2gFuWBF8YwS3L (db: the user's answers at answers/user, readable with ArtifactData only from this account).
