# Pillar 5 Steps 1-2 brief (lead 11, session_01YKC3CGA9VS4b7wuqLbPT7V, 2026-10-18 ~08:00 UTC)

The user said go for Pillar 5 Steps 1 (Foundation) and 2 (Junior days, Days 2-8) overnight. Overnight the lead approves or rejects everything (plans/overnight-decisions.md, last section); nothing waits for the user.

**Every seat reads, in order:** CLAUDE.md; this brief; `plans/pillar5-plan.md` v9 (Part 6 "the common brief" and your seat) and `plans/mechanics/index.html` + your pages, all on `claude/p5-design` (git fetch origin claude/p5-design; read with git show); DEV_NOTES.md ("Rules that keep it working", "Testing", the build table); TEAM.md.

- **Base:** the 0.60.7 candidate `claude/cand-0607` d3d720b (0.60.7 will be released from it or a doc-only child; if it changes, the lead tells you to merge).
- **Pages are approved** (each has an "Approved by the lead" line). Build exactly what your pages say. A gap or clash → ask the designer (session_01VXENaUt4vdyYtr3KjVZk9z) and copy the lead; a design call beyond the page → the lead.
- **Naming:** Pillar 5 state is `SHIP.works` / `ship.works` (NOT SHIP.career, which is the leave/clock code). Hash keys: your page's range only (850-899, second range 1000-1049).
- **Build numbers:** your seat's series as on your page (C 0.44.x, S 0.33.44+, P 0.28.71+, M1 0.45.x, M2 0.51.x, H 0.55.x, A 0.47.x). Bump the HUD build number and add a DEV_NOTES build-table row per turn.
- **Rules:** small exact-string edits, never rewrite the file; determinism (no R() in shared kit at load); phones first (col(), no coplanar faces, watch draw calls); saves: every new saved field loads old saves (default) and has a round-trip test.
- **Checks:** quick checks for what you touched (DEV_NOTES "Testing"), intro_check on any push touching jobs, the player or the clock; cadet_test differences explained.
- **Report to the lead** (send_message to session_01YKC3CGA9VS4b7wuqLbPT7V): one line when you start, one per finished piece (hash, build number, what, checks), at once if blocked. No narration. Send each finished piece's hash to the Pillar 5 build master and reviewer too (ids in TEAM.md once started).
- **Never** contact the user, start sessions, or push outside your branch.
- **Memory:** tell the lead at ~60%; at ~70% write `plans/handover-<seat>.md`, push, stop.

## Seats (Step 1 first; Step 2 seats start as Step 1 pieces land)
| Seat | Branch | Session |
|---|---|---|
| D designer | claude/p5-design | session_01VXENaUt4vdyYtr3KjVZk9z |
| B build master (BM4 continues after 0.60.7) | claude/cand-0607 → P5 candidates on claude/p5-cand | session_013h22isZZqmJJSEKSbrwabf |
| C works career engineer | claude/works-career | (lead fills in) |
| S systems | claude/ship-systems | (lead fills in) |
| P player | claude/player-p5 | (lead fills in) |
| H case engine + scanner + P3 | claude/mech-cases | (lead fills in) |
| M1, M2, A | Step 2 | later |

Merge order within a step: 17 (S), 15 (P), 24 core (C), mechanics in ladder order, head-scratchers (H), deck architect (A), writer.
Pillar 5 builds go to a NEW preview link; 0.60.7 stays on the main link.
