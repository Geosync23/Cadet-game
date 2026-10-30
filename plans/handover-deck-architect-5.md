# Handover: deck architect 5 (DA5)

Session_01CHRbUTZc18m7eBck8eWhXj, 2026-10-18. Written at about 60% memory while Step 3 is on hold. Read it with CLAUDE.md, DEV_NOTES.md (rows 0.47.3-0.47.10, "Places for Pillar 5 Step 3"), and the earlier architects' note `plans/handover-deck-architect.md` (on `claude/deck-0607`; its Gotchas still apply).

## Role and chain
- The one architect for every deck's data and kit (places, machines, rooms, dress, wall kit), plus whatever the lead hands over (this session also did poses, lighting and the speech bubbles).
- Lead: lead 15 (session_01TfFnwP88RmL4MhCWAMdSGn), before that leads 14, 13, 12. Helpers never contact the user. Report finished pieces (hash, build, checks) to the lead, the build master and the reviewer.
- Build series: 0.47.x (HUD build line + `GAME_BUILD`, a DEV_NOTES build-table row per turn). The next free number is **0.47.11**.

## Branches
| Branch | What | State |
|---|---|---|
| `claude/deck-p5s3` | Step 3: 0.47.3 air line (0df7011), merged with 0.63.2 (fe27dc7), WIP patch saved (675316d) | **Step 3 on hold** (no game edits until the lead's GO) |
| `claude/deck-tern2` | 0.47.4 the Tern's second pass (484f160, shots cf51d67) | in 0.63.2 |
| `claude/deck-pt1` | playtest update 1: 0.47.4-0.47.10 (head 080b0b8) | all reviewed PASS (R2/R3), in 0.63.2 |

## What I built
- **0.47.3, the air line** (plans/mechanics/architect-air-line.html): the air plant's existing hatch `h,38,5` into the Fan hall opens (tier 2 service hatch); `5-fan-1` is a real machine (at [36,8], panel/`-svc` [36,9]); the big fan blocks its six tiles, keep-clear outline, tap item; `5-damper-1`/`-2` on the Fan hall's west wall ([34,6], [34,9]), kind `damper`, wall kit `ductDamper` (wallFixed). **The dampers are dropped from the machine list until seat S2 adds `MACHINE_KINDS.damper`**: machine_check FAILs "unknown kind damper" until then (expected).
- **0.47.4, Tern pass 2**: tapered tail (constants TZ/TF/TW in the `shuttle` kit), engine pods, shaped roof spine (`slab()`, `mirror()` helpers inside the kit), rounded corners, lockers/floor/roof follow the taper. Same draw calls (Deck 5 179).
- **0.47.5**: bike pedals forward (`ACTS.cycle`); bench press activity `bench` (`3-gym-6` `anim: 'bench'`, prop `barbell`, the rack bar hides via `BENCH_BAR`); seated talk without arm-waving; the night a little brighter (`NIGHT`).
- **0.47.6-0.47.8**: Name on the Beam in first names, the west end's 2 × 2 grid for you + the 3 newest (`BEAM.slots`, `DECK_DRESS.nameYours` / `nameNew`, planes 6 mm apart); garden stretch places `3-stretchg-1..8` (tag `stretch-garden`); old `3-stretch-*` retagged `stretch-promenade`.
- **0.47.9-0.47.10, speech bubbles** (the user's "flicker" = shake/jump on a phone): `bubbles.tick(dt)` only counts down; `bubbles.place()` runs in the main loop just before `renderer.render` with `camera.updateMatrixWorld()`; translate3d fractional px; a pair keeps its sides/stacking (24/12 px hysteresis); layout changes ease, capped at 900 px/s. New **`bubble_check.py`** (phone size, DPR 3, 17/33 ms frames).

## Step 3: DONE as 0.47.11 (1f50d8f, tap tweak 3803e63) on 0.63.2r 898d58d
The held places were applied (the plans/wip copy is removed) and the bridge hook is `YOU_LOCKS` / `youLock(key, who)` / `youLockTap(key)`; C2 defines `bridgeInvitedNow()` and `bridgeDoorTap(key)` (asked C2 to drop its own edgeBlocks change so the two don't fight). What follows is the original plan, kept for the record.

## (Was) waiting for GO (Step 3, brief plans/brief-p5s3.md on claude/lead-pillar1, row "DA5")
1. Apply `plans/wip/step3-places.py` (it edits `starship-cadet.html` in place; **change its build bump from 0.47.3→0.47.4 to the current line → 0.47.11 first**). It adds: team-job spots (`3-recycler-team-1..4`, `4-washer-team-1..3`, `5-manifold-team-1..3`, `4-heater-team-1..3`, `4-scrubber-team-1..3`, `DECKS[n].teamSpots`, `event: 'team-job'`, `works: true`), Calder's office (`5-office-visit-1`, `5-office-stand-1`), the ceremony (`1-ceremony-captain`, `-you`, `-guest-1..6`), cabin 4-23's keepsake shelf (`placeWall('W', 'keepsakeShelf', 'n', .5)`, place `4-23-keepsake`, `DECKS[4].homeKeepsakes['4-23']`) and its door plate (your name once `SHIP.works.home === '4-23'`, read at deck build). The `.patch` beside it is the same change as a diff, for reference. **Not yet tested**: run deck_check (all of them reachable; office room `o` has a closed door, check it), the crew-plan comparison (they must be inert), cadet_test (Deck 4 shows the new shelf in 4-23 only if a shot sees it).
2. The bridge door's tap hook for C2 (the career seat): C2 owns `SHIP.bridgeInvited`; the deck side is the bridge room's door on Deck 1 saying "you need permission" until invited. Agree the shape with C2 (session_014yREkgPvuwMyxBtoqB1P14) first: e.g. a `DECKS[1]` door entry whose tap text and passability come from a function C2 defines (`bridgeLocked()`), so nothing else changes before the flag exists.

## Open item after 0.47.12 (not built: the lead said stop)
- **Keepsakes to 4-23** (C2, 2026-10-19): when `worksHome() === '4-23'` (SHIP.works.home, set Day 10 ~17:00-17:30), the keepsakes section 8b draws (its one instanced mesh at `DECKS[4].keepsakes.slots`) should use `DECKS[4].homeKeepsakes['4-23']` instead (same shape; the framed commission arrives Day 11). Smallest change: where 8b reads `DECKS[4].keepsakes`, read `(typeof worksHome === 'function' && DECKS[4].homeKeepsakes[worksHome()]) || DECKS[4].keepsakes`, and redraw on C2's `simNote('moved')`. The door plate already follows SHIP.works.home (read at Deck 4's build).

## Gotchas (new this session)
- **cadet_test's `Game` injects `animation:none; transition:none`** for every element: visual CSS problems (pop-ins, slides) never show in it. For those, exec cadet_test's top half and replace the `add_style_tag(...)` line with `pass` (see how bubble_check does a replace on the source).
- Don't name anything `HOOK` in a script that execs cadet_test (the page never gets `__sc`).
- `?nosave&debug` starts with the intro off (Day 1 06:00). A real arrival needs `localStorage.clear()` and `?debug` only, then fill the manifest form (intro_check section 9). That run is slow (over 10 min for 150 s).
- A tradition fills its spots from every place tagged with its own id first: a new place with an existing event tag changes crew plans. Give new places their own tag, and let the traditions engineer point at them.
- Traces: `traceAdd` keeps one per id; repeated traces (like `nameNew`) are pushed directly.
- `plans/shots-*/*.png` are git-ignored: `git add -f`.
- Merging others' branches: resolve only the build lines (keep yours) and DEV_NOTES rows (keep both). Never `git checkout --ours` a whole file (it drops their changes).

## How I test
Scratch scripts (in the scratchpad, not committed): `shoot.py` (goToDeck, place the player, set `az`/zoom, screenshot; env DK/PX/PZ/ZM), `plans.py` (hash every person's `planDay` for days 1-8, 12, 35 in two builds; must be 0 differing for inert places), `free.py` (free tiles and used place tiles around a spot), `beamtex.py` (pull a canvas texture out as a PNG). Then deck_check, cadet_test (explain every differing shot by cropping the diff box), interactions_check, machine_check (compare against the base: only expected lines differ), player_check (long: give it 40 min), bubble_check.

## Open questions for the user
- None of mine outstanding. (The Tern pass and the playtest items are approved and shipped.)
