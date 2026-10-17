# Handover: build master (Pillar 4)

**Role.** Merge the helpers' named commits into combined builds 0.60.x, run every check (with the six check-runner sessions), explain every difference, keep DEV_NOTES' 0.60.x rows and hook register current, and send the lead a green hash. The lead pushes `claude/ship-integration` and publishes; the build master never does. Reports go to the lead only (chain of command: the user → the lead → everyone; TEAM.md "Chain of command" on `claude/lead-pillar1`).

**Lead:** session_01KPJMYjXAPkNUcrQ8VRkhLE (from 2026-10-17 ~04:35; before it session_01PJtmxWgAPLebXSZKP6ZRpG, who released 0.60.1). **Reviewers:** reviewer 1b session_018XY1NbMBxo2SLDPxooe5yx (took over from reviewer 1, session_01HK4m33sUiLuVim8VWaCPMs); reviewer 2 via the lead. **This note:** the first build master, 2026-10-17 ~01:00-04:40; build master 2 (session_01F8ph7FKqViF3heRn94YgBr) from ~04:40, who released 0.60.2 and is combining 0.60.3.

## Branches and builds

- **Candidate branches:** `claude/cand-0600`, `claude/cand-0601`, … one per combined build. Force-pushing `claude/integration-test` is blocked by the session's permission guard, so candidates get their own branch (the lead approved). Always a plain push.
- **0.60.0 "the writers' kit"**: released, `claude/ship-integration` = e3ee66b. Contents and results: DEV_NOTES' 0.60.0 row.
- **0.60.1**: `claude/cand-0601` (see the 0.60.1 row once written; status at the end of this note).
- Build lines: header `build 0.60.x` and `GAME_BUILD` set to the combined number (the resolver does it on conflicts; check both lines after merging).

## Merge order and rules

- Plan order (pillar4-plan Part 6): crew designer → sim → device → player (on call) → social A → social B → traditions → dialogue → arrival → tiles → places (decks) → content.
- **Never merge `claude/ship-systems` again** (the lead's rule, 03:45): the sim engineer owns section 17 now, and `claude/sim-engineer` contains systems' work with a newer section 17. Merging ship-systems after the sim undoes it (broke social_check's time-jump test).
- **Generated blocks** (ROSTER, LINES, MEETINGS, TRADITIONS) are never hand-merged: after merging dialogue or traditions run `python3 content_gen.py`, then `--check` must say "up to date". The ROSTER block is the crew designer's generator output; their newer block wins.
- **Take only reviewed commits** (reviewer 1: session_01HK4m33sUiLuVim8VWaCPMs, sections 13/14/10/20/20c/21 and checks; reviewer 2: dialogue, traditions, device, decks). The lead names what goes in; ask when unsure.
- `merge --no-ff` per helper, message "WIP 0.60.x: <branch> <builds> merged (<what>)"; small glue in its own commit; DEV_NOTES row + hook register in a "DEV_NOTES" commit; the final commit "Combined 0.60.x: …".
- Merge glue in the game file: avoid; send it back to the owner via the lead. Test-only fixes are OK when the lead says so (e.g. machine_check 7ab17bc).

## Tools (this folder, `plans/build-master/`)

- `mergeone.sh COMMIT "message"` (set `BUILD=0.60.x`): merge, auto-resolve build-line-only conflicts with `resolve.py`, stop on anything else. `resolve.py FILE BUILD [--union]`: sets build lines, takes the side that contains the other, `--union` for DEV_NOTES rows. **Caution:** "takes the larger side" can bring back a line one side deleted, so always run:
- `verify_merge.py BASE RESULT FILE TIP...`: every line each helper added is in the result and nothing a helper deleted came back (uses each tip's merge base). "Missing" lines must each be explained (a later commit rewrote them, or the generator replaced them).
- `python3 name_check.py --branches BASE TIP...` and `name_check.py FILE` (reviewer 1's, from `claude/reviews`): two sections declaring the same top-level name = the game doesn't start. "Deleted but still used" on a branch that started before the base is usually a false alarm; check it.
- `smoke_check.py BUILD`: loads the game, opens a chat card with all 74 crew at 08:00, 13:00, 19:00 (chat + ask), visits every deck; fails on any page error. Catches run-time errors the static checks miss.
- `newgame_check.py BUILD`: first-ever load and New game → Day 0, Sunday 17:40, Deck 5, step 'manifest'; test URL `?nosave&debug` → Day 1 06:00 with the intro off.
- `swaproster.py NEW OLD OUT`: put OLD's ROSTER block into NEW. Proves which cadet_test differences come from the roster (days off etc.): swap the base's roster in and expect ALL IDENTICAL.
- `runcommit.sh COMMIT OLD` via `go.sh` (go.sh runs a private copy, so editing the runner never breaks a run): exports the commit's tree to /tmp/cw/run_<sha> and runs name, content_gen --check, smoke, newgame, every *_check.py, day_check 0 and 1, cadet_test vs OLD, one at a time. Use it when the runners are busy.
- Setup in a fresh container: `pip install playwright`; three r128 into /tmp/cadet-work/three (DEV_NOTES "Testing"); `CADET_CHROME=/opt/pw-browsers/chromium`.

## The check-runner pool (report to the build master)

R1 session_01PGFJbAfDYddQRGYQJktgXj cadet_test · R2 session_012zFHAS6jkPUhCrpBn2zW9Q day_check (days 0, 1, 6, 7, and 35 = the first rotation Sunday; later 77, 119) · R3 session_01USkJjdw16L4K2tuK8otcc6 player + interactions · R4 session_01V5ghkKLy1XQkZkKS9yKUkr events + intro · R5 session_01PPVXqo8s4NvK8JkBWt3WoH food + machine + deck · R6 session_01L5Bg1nrCfowojNxeVZJHoi social + device + lines + content_gen --check. Push the candidate, send each its slice with the commit (R1 also gets cadet_test's base), keep name/smoke/newgame yourself. A full round is ~15 minutes. The performance engineer (session_01XAkY9U3mmstHQT2yAMTocA) runs perf_check on each pushed candidate when told the commit and its base.

## Lessons (each cost a round)

- Run every check on every combine, including the short ones; list them all in the report.
- A check that passes on a helper's branch can fail on the combine because its stand-ins are shadowed by the real thing (social_check's `window.lineFor`; intro_check's flag store). Look for test-harness causes first.
- Narrow a failure by running the check on each first-parent merge step (`git log --first-parent`), then pair branches in a scratch worktree.
- Explain every cadet_test difference: the roster swap proves days-off differences; ask the owner to name the crew in a moved shot.
- "Crew count changed" reports: get the exact scene (flags, day, minute, frames) before chasing.
- Never pkill by a pattern that matches your own shell; kill by PID.

## Status at handover (2026-10-17 ~04:40)

- **0.60.0** released (e3ee66b).
- **0.60.1** = `claude/cand-0601` (final candidate 1bc4488 + this note). Contents, fixes and every cadet_test difference: DEV_NOTES' 0.60.1 row. Results on 1bc4488: name, content_gen --check, lines, smoke, newgame (first launch → Day 0) OK; social, device (R6), food incl. the event cake, machine, deck (R5), events, intro (R4) OK; cadet_test vs 0.60.0 = the explained differences, vs 062db7b ALL IDENTICAL (R1). Day 0/1/6/7/35 (R2) and player/interactions (R3) were green on the previous candidates and running on 1bc4488 at handover: check their reports.
- **0.60.2 queue** (named by the lead; take only reviewed commits; re-check each branch's head):
  - dialogue e532f89 (0.43.7) or later.
  - traditions 5fa104f (0.34.33: 24 baked traditions, Sunday Mail, tallies, the birthday fix again). Expect one events_check FAIL already in the base: day 231's double booking at 3-store-1 at 14:30 (the sim engineer has it). Re-run content_gen.py.
  - sim: the `job` payload rename (section 17 notes), 0.26.26+, and the leaver-walks-to-bay polish; anything for section 17 comes from claude/sim-engineer.
  - galley: `galleyBirthdays` through schedPeople + aboard (galley engineer 3).
  - arrival b4f0ac4 (0.42.18 + intro_check part 11; not a86d052). Needs sim 0.26.26 + player 0.28.28.
  - player 0.28.28.
  - social A 0a7ceb8+ (0.36.52+); social B 0.39.4+ (goodbyes, couples).
  - crew designer 4613d43 (0.16.14, data only) after reviewer 1b.
  - the head writer's content (claude/content: 574 lines + 74 voice cards); merge content last, then content_gen.py.
- **Known, not blocking:** the device's `isFinite` → `Number.isFinite` nit (2 places, "Day null"; the device engineer has retired).
- **Pillar 5 planner** (session_01VTbXtWeydYbfNw8fKLpkz8) was told: keys 850-899 free; events 352-399 clash via `k + 100` with the traditions block 434-499 (suggest 950-999); builds 0.44, 0.45, 0.47, 0.49 and 0.51-0.54 free.

## Build master 2 (from ~04:40)

- **0.60.2 released**: `claude/ship-integration` = 142b503 (`claude/cand-0602`). Contents, fixes and every cadet_test difference: DEV_NOTES' 0.60.2 row.
- **0.60.3** on `claude/cand-0603` (from 142b503); head 6e39388 (status 06:40). Candidate 1 = 8b4bbd6 (social A dc80136 0.36.52-59, dialogue 4bfe3a6 0.43.16, Tiles 45bdfff 0.46.2-5, decks 9377551 0.38.17, device be8e2ab 0.35.26-28, traditions f78dd03 0.34.40-41): every check green except player_check's "device marks" (device 0.35.28 lists penalties first; test fixed in 6e39388). cadet_test vs 0.60.2: i_tap0/i_tap1 only, a reaction bubble from 0.43.16. Then added: social B 4222804 (0.39.6-10; carries social A only to 0.36.59), dialogue 47b1bfd (0.43.17-18, merged 0.60.1; New game now reaches section 22 on the bus, `onSim('newGame', linesNew)`, so the 0.60.2 glue line in section 13 was removed; checked in the page that New game empties SHIP.lines.ring). 6e39388 not run by the runners yet (the lead: batch, save usage before the 07:30 reset).
- **Waiting (reviewer 1b):** sim a7673e0 (0.26.29) + 0cf991a (0.26.30: the real food line, trays, sitting to eat); galley 6abd36b; player (claude/player-needs; player engineer 3 session_016EJg9DempByUCWwpszyWmV made "device marks" order-agnostic: take theirs over 6e39388's line); social A 0.36.60-62 (NEVER f75e484 / 0.36.61: favour memory and reputation commented out); arrival (Zeke's tour + bed arrow, not pushed at 06:40). 1b saw social_check's jump test fail on a full merge (repair.recycler, eklund-leila, min 937), not on 3203e81 or 6e39388: likely the sim; check it when the sim goes in. Then content last (no extra review gate; head writer 3 reviews; the newest head when the run starts). Run the batch as candidate 2 and send the lead the hash.
- **0.60.3 final list (the lead, 09:10):** sim 0.26.33 (the stuck-line fix, from sim engineer 4 via 1b), galley 40166d6 (0.29.32), player (1c's verdict on b728101+ / 0.28.36), arrival 0ea5048 (0.42.21), and the device 2ef3cce (0.35.30) + traditions 708c4ca (0.34.45) pair only if 708c4ca's check is done (else drop the pair, don't wait). Then one full run. Everything else is 0.60.4: decks 3e1f4f9 (0.38.21-23, the Tern) + traditions 3d06bcb (0.34.49) together, device dfc1df2 (0.35.33; hold e5d7227/0.35.34 for its HUD fixes), crowd-render d45d019 (0.27.26), the {family} set, content 5e2605e. My probe on 0.60.3 + sim bfcd864 + galley 40166d6 + player b728101 (scratch, /tmp/cw/lineprobe.py) showed the evening line working after the player is served (53 served by 18:30).
- **09:20:** content head fd3db63 (0.48.50; head writer 3 session_01FopKMT2ZKxuWcNDcmF7565): 0.48.49 orders Zeke's tour core lines first per place (pacing A, for arrival 0.42.22, onboarding engineer 2 session_0163dcLt17oTCdR8po9HRo2p); 0.48.50's banks/missing.lines use {missed} and need dialogue 0.43.27 c084a1a+ in the same candidate. Arrival 0ea5048 counts as passed (1c, PASS WITH FIXES; HIGH: tour pacing, 19 of 61 lines heard, fix = 0.42.22): take 0.42.22 into 0.60.3 only if reviewed before c2's full run starts, else release 0.60.3 without it and do 0.60.3b with the tour fix (and its content). The device 0.35.30 + traditions 708c4ca pair is dropped from 0.60.3. The scratch c2 is local branch trial-0603c2 (b1a5b3a): d6fbff6 + sim 6e87e6b + galley 40166d6 + player 9a79f60 + arrival 0ea5048, all checks above OK; push it as cand-0603 once 1b passes the sim and 1c the player.
- **09:30 (the lead):** sim 0.26.34 (236810f, on 0.26.33: mid-meal line catch-up peak 7, no trays outside the mess for lift arrivals) goes into 0.60.3 only if 1b passes 0.26.30-0.26.34 together, else 0.26.33. claude/arrival 0.42.22 (9b37dd9) is the shuttle start = 0.60.4 (needs SHIP_START_ARRIVAL = { tile: [5,7], face: 0 } in the same combine). The 0.60.3/0.60.3b tour fix comes from a side branch claude/arrival-0603 (cut from 0ea5048) plus content/ from 910e88e (lines, voices, overheard, meetings, facts.md; not themes/, traditions/ or banks/missing.lines): take that branch, not claude/arrival.
- **0.60.4 queue (the lead, 08:30):** the {family} set together (dialogue 46e948b 0.43.24-25, content 5dff82a+, social 0811adc 0.36.68, crew designer 3's roster 0.16.15 d53cf40), content/ from 5e2605e (0.48.48, replaces 5d4b810: reviewer 2's fixes, facts.md's days off from ROSTER; sent to reviewer 2 for a delta check), paired with dialogue 46e948b+ and roster 0.16.19 caedef2 (1c reviewing); head writer 3 session_01FopKMT2ZKxuWcNDcmF7565, perf claude/crowd-render cfbfd76 (0.27.25, shadow stand-ins, reviewer 2 PASS), decks 0.38.18 (the Tern) with the start-tile pair (sim 4 + onboarding) once fixed, and whatever of 0.60.3's waiting list misses 0.60.3.
- **Content rule (the lead, 07:32):** only `git checkout <content-hash> -- content/` (+ the writers' plans), never claude/content's game file; and NOT content/traditions/ (claude/content's sowing.trad is the old wave-1a sample; traditions' .trad files come from claude/ship-events). Then content_gen.py and --check on the combined game.
- **Contacts:** traditions engineer 2 session_01WEEoe5DyRegEqVMZgKRHWB; reviewer 2 session_0142TQw4ke8caPSyAC93VT98 handed over at 08:37 (note 5976774); reviewer 2b session_01F93LiFWtciyCLNV34qPsjP covers dialogue, traditions, device, decks, tiles, content and perf; reviewer 1 (1b, session_018XY1NbMBxo2SLDPxooe5yx) sim, galley, social, arrival; reviewer 1c player and roster.
- **The user's rule:** refresh this note right before handing over (latest hashes, what's in flight, decisions); never hand over a stale note.
- **Lessons:**
  - A branch that hasn't merged the latest release can pass its own checks and fail in the combine. In 0.60.2: the new roster put Zeke at work on Sunday day 7, so One week aboard had nobody (device_check's "the Schedule lists only what really happens"), and section 14 brings a host 5 minutes early, which events_check flagged 20 times. Trial-merge the branch onto the release alone (`git worktree add --detach`) to prove whose it is.
  - verify_merge with a branch that started before the base reports 0.60.0/0.60.1 lines that later rewrites removed as MISSING. Re-run it with the release as BASE (the true merge base), or filter out lines present in the release.
  - The scripts in this folder (smoke, newgame) need cadet_test.py beside them: copy them to a run folder.
  - Union merges of DEV_NOTES stack up "## Current build" lines from every helper: leave one.
  - Content moves fast (a new head every ~10 minutes); take the head the lead names when the run starts, and don't restart for a newer one.
  - Save size probe (rebuild the save as `saveGame` does, after `skipTo` days): the social part levels off at 23-27 KB by day 22-50 (social_check's limit 30,000); the whole save is ~95 KB on day 50, with Mail growing.
