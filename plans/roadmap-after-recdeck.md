# Roadmap after the rec deck (agreed with the user, 2026-10-19)

The user: "I don't care about usage, we will get it there." Order:
1. Finish the rec deck 0.64.0 (see START-HERE.md).
2. **Split the game file** into pieces (crew, machines, decks, phone screens, content, ...) joined by a small build step into the one playable file. Proof: the joined file is byte-identical to today's. Plan page for the user first (it's a big move). Then a light clean-up of obviously unused code, one area at a time, with checks.
3. Pillar 5, Steps 5 and 6.
4. Ship-wide events, only those up to the end of the promotions (the user cut the rest), one at a time, each built switched off, then switched on. They touch every system: do them after the split.
5. Basic text-based stories for key crew members, written alongside 3 and 4 (mostly content/ files) and added when ready.

## Ways of working to keep quality up on a big codebase (proposals; ask the user before adopting the big ones)
- **Ownership map** (`plans/owners.md`): which seat owns which file/area and which shared functions (with their exact signatures, e.g. recShow(state)). A change outside your area goes through its owner.
- **A fast pre-push check** (`check_fast.sh`): parses the game (node --check), scans for duplicate top-level names, greps for "Deck 7" on screen and runs 3-4 quick checks; under 5 minutes. Every worker runs it before every push. Today's name clash would have been caught hours earlier.
- **Automatic checks on GitHub** (GitHub Actions): the fast check runs by itself on every push, so nothing depends on a session remembering. (Needs a one-time setup; the user approves.)
- **Integrate early, not at the end:** a shared integration branch that each seat merges into after each reviewed piece, with the fast check, instead of one big combine at the end (today's hand merges and the late clash came from combining two days of work at once).
- **Rules that caught us today, written into DEV_NOTES "Rules that keep it working":** the crew planner must never read records that are built while the game runs (the MACH_HIST bug); checks must not assume a deck is empty or a time slot is free (two check fixes today); new features stay gated (switch off = identical) until switched on.
- **A "where things live" map** (`plans/map.md`), kept current by whoever moves code, so a fresh session finds its way in minutes.
- **A small known-bugs list** (`plans/backlog.md`), so things found in passing aren't lost: the unclosed CSS comment (~line 181), the hidden door gear (~line 1724), the double clock hold in the evenings, two wall faults leaving you queued, rec talent night only skipping day 152, the Tracked panel filling small phones, "seven decks" Deck 4 texts not gated.
- **Keep the user's review rhythm:** one step at a time, a plan page before building, the user's sign-off before the next step.
