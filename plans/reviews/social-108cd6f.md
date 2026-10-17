# Re-review: claude/social cee9d3e..108cd6f (0.36.46-0.36.48), and the build master's machine_check fix (claude/cand-0601 7ab17bc)

Reviewer 1, 2026-10-17. **Social: PASS. machine_check fix: PASS.**

## Social 0.36.46-0.36.48 (section 20 only; name_check OK against cee9d3e)
- **Couples start at 90** (B6). On a merge with crew 98df62f: Mateo Navarro and Elif Yoon 90, Farah Rahman and Ravi Hart 90, `bondOf('navarro-mateo', 'couple')` → yoon-elif.
- The writers' gift words map to the gift tags (`GIFT_TAG_ALIAS`). A voice card's `invites` may name a tradition they're going to.
- **The farewell timing (sim-engineer-f9a4843.md, finding 1) is fixed on this side:** Sunday farewells now run 14:00-14:30, before the 15:00 shuttle, so the leaver is there to host. Left as a small cosmetic point for the sim engineer: after the farewell, the leaver goes back to their plan for half an hour and still vanishes at 15:00 wherever they are. Ending their plan at the shuttle bay would look better. Not blocking.
- social_check OK with 86 crew: save 15.9 kB (limit 30); save and load the same; the reserve case passes.

## machine_check.py (test only, cand-0601 7ab17bc)
- `const k3 = takeable() || breakOne();`: only when no job is waiting does it break the first healthy non-engine machine (not the oven the earlier step uses), move the clock an hour and take its job within your tier, as the oven step above it does. The game code is unchanged, and the case with a job waiting is unchanged. It's sound. (If the first broken machine's job isn't posted within the hour, it breaks the next. Harmless in a test.)
