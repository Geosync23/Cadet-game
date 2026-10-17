# Handover: adversarial reviewer 1f

- **Role:** adversarial reviewer for 0.60.6. Session_015UH1fbKg2nCRNi9Y3D96YA, which took over from 1e (session_01BcEWju7cay3mnujaL1apzU) about 21:00 on 2026-10-17.
  - Report to **lead 8** (session_01FutyR6xiAmZv29oS4TWKdS) and **build master 3** (BM3, session_01WrXgDfR5dzwktKJfYwVwsV). Give BM3 the hash to merge with every PASS.
  - Also tell the builder.
  - Never change game code, and never contact the user.
- **Second reviewer:** 1g (session_01Pxr7Ei4zeWFuNMauuqb3uJ) has Put down (PE8, claude/player-needs-putdown) and shuffle-aside (PE9, claude/player-needs-shuffle). If a builder sends you those, forward them to 1g.
- **Branch:** `claude/reviews-4`. Notes go under `plans/reviews/`, with probes saved next to them. Pull before every push, because 1g pushes there too.
- **Cost rules (the user and lead 8):** review behaviour and save changes in depth; skim content and test changes. Run only the checks you need. Be quick and to the point.

## Seats (session ids)
| Seat | Session | Branch |
| --- | --- | --- |
| Player engineer 6 | session_01AWgP6kgzpprnpA5pMAAiqq | claude/player-needs (Pause follow-up, Tiles) |
| Player engineer 7 | session_01CrRKCZzVtM68JrPqJByCMk | claude/player-needs (lamp tap fix, Repair button) |
| Player engineer 5 | session_01SyRmwPxQEVKab6re9UgyrD (**inactive**) | its work moved to PE6 |
| Deck architect 3 | session_01NsysH87qqJnf1dBEVRz2fW | claude/poses, claude/clock-fix |
| Career engineer | session_01862tURG1qXAVGj2sdUrVCw | claude/leave (done for 0.60.6) |
| Head writer 5 | session_011KTwL5FVSdmWNAkbkZsrgj | claude/content |

## Done (2026-10-17, from 21:00)
| Item | Note | Verdict |
| --- | --- | --- |
| leave 0.61.18-0.61.19 + handover, da6abc6..**0784b54** | leave-ea89382.md | PASS. One LOW (a 17:00 auto sign-out beats an honest early clock-out); the lead is leaving it as it is. |
| content 0.48.80 d494709 (clock.early) | content-d494709.md | PASS (skim) |
| poses 0.27.44 1845e53 + 0.27.45 6493e5f | poses-1845e53-6493e5f.md (+ walk and plan probes) | PASS. 26 Deck 3 lounge plan steps change, and Deck 6 watch-seat walk tiles move. |
| poses 0.27.46 157c0dd (no seat ray) | poses-157c0dd.md | PASS. perf_check OK (dinner game time 2.1 → 1.6 ms). |
| poses 0.27.47 **8fef4ed** (no tray while waiting for a taken seat) | poses-8fef4ed.md | PASS (the current poses tip) |
| clock-fix **83beaf6** (Works crew clock in by 08:00) | clock-fix-83beaf6.md | PASS |
| player-needs 0.28.48 2e69a13 (Pause) | player-needs-2e69a13.md (+ pause probe) | PASS WITH FIXES. MEDIUM fixed in 0.28.50. |
| player-needs 0.28.49 dae0dfe (trad-id fix, PE5) | player-needs-dae0dfe.md (+ trad probe) | PASS. LOW 1 (lower-cased names) fixed by PE8's tradName in putdown 1116be4 (PASS). LOW 2 (done posts use today/filler lines) still open. |
| player-needs 0.28.50 9a84b79 (Pause follow-up, frozen clock) | player-needs-9a84b79.md (+ dust probe) | PASS WITH FIXES. Three LOWs: dust drifts while frozen, Resume isn't keyboard-usable, Tab reaches the HUD under the card. PE6 says they come in **0.28.55**. |
| player-needs 0.28.52 a9f7ed5 (PE7: job-stop tap, Repair button) | player-needs-a9f7ed5.md (+ near, hijack and locked probes) | **BLOCK.** HIGH softlock: locked in the Captain's quarters after veyliLamp. MEDIUM: job taps take over things within 1.5 m of the panel (Washer 2, the Welding bench). PE7's fix comes as **0.28.54**. |
| player-needs 0.28.51 d39f92e (Tiles) | player-needs-d39f92e.md | PASS WITH FIXES. MEDIUM (balance, the lead's call): unlimited social from repeated games at zero ship time; my lean is a full gain only for the first game with someone each day. tiles_check ALL OK. |

## Open queue
1. **0.28.54 (PE7): re-check the BLOCK.**
   - Rerun `player-needs-18eedb8-locked-probe.py`: a path to the lift must exist after the stops are done.
   - Rerun `player-needs-18eedb8-hijack-probe.py`: Washer 2 must start a load, and the Welding bench must craft, while the nearby repair is held.
   - Check the user's lamp cases still work. interactions_check's "a tap at the stop" covers them.
2. **0.28.55 (PE6): my three LOWs on 0.28.50.**
   - Rerun `player-needs-18eedb8-dust-probe.py`: the paused move must be about the same as running (≈0.1 m a minute).
   - Check Resume works with the keyboard and the HUD is inert while paused.
3. **Tiles' balance MEDIUM:** whatever the lead decides.
4. **BM3** is holding claude/player-needs until 0.28.54 passes. Send BM3 the passing tip hash.

## How I test
- **Setup:** `pip install playwright`. three r128 is in /tmp/cadet-work/three, with `three/package/build` → `../build` (cadet_test reads `WORK/three/package/build/three.min.js`). Set `CADET_WORK=/tmp/cadet-work` and `CADET_CHROME=/opt/pw-browsers/chromium`.
- **Copy files** into a scratch folder with `git show <hash>:<file>`.
- **Probes** exec cadet_test.py's top half: `src = open('cadet_test.py').read().split('import sys, json, hashlib')[0]; exec(src)`, then `Game(pw, path)`, `g.ev(js)`, `g.step(n)` (30 frames a second of virtual time), `g.page.mouse.click(x, y)` for real taps, and `goToDeck(n)`.
- **One browser job at a time.**
- **Timings:** player_check 25+ minutes; leave_check and tiles_check about 20-25 minutes each.
- **Baking the news bank:** `git archive origin/claude/player-needs content content_gen.py plans/trad_parse.py`, plus claude/content's `content/banks/news.lines`, then `python3 -I content_gen.py game.html`.
- **Gotchas:**
  - `DUST` exists only on Deck 3.
  - `MACHINES` isn't a global; use `machineList()`.
  - `placeSpot(id)` gives `{x, z, walk, face}`, and settled crew sit exactly on it.
  - `doorOpenFor` blocks both ways, so a room that opens only "while it's your next stop" traps you.
  - Since 0.28.50, real-time pacing uses `simNow()`/`simTimeout`. A new deadline on `performance.now()` won't wait out a pause.
