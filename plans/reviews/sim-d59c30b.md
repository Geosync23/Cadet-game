# Review: sim 0.26.41 (claude/sim-engineer d59c30b), meal traditions through the line

Reviewer 1d, 2026-10-17. For 0.60.6. Sim engineer 5's change, plus plans/events_check-0.26.41.patch.

## Verdict: PASS

**The change:**
- A meal tradition's diners now set off 8-30 minutes early (seeded per person, `U(530)`).
- They queue at the servery and get a tray, then take their table seat. With no seat left, they eat where they stand.
- `lineCounter` serves two at once from 35 minutes before a meal tradition until its end. It's live state, read only by the line, not by the plans.
- No `R()`.

**Tested on a merge:** claude/social-fixes (afbb5c9, with the promenade trestle gone) plus d59c30b. Only the build-number lines and the docs conflicted; I kept social-fixes' versions. The events_check patch applied cleanly.

| Check | Result |
| --- | --- |
| day_check day 7 (Sunday, the long table) | OK. Servery line: 118 joined, 118 served, longest line 6, longest wait 3.5 ship min, trays 95 out and 95 back, nobody gave up. Deck 3 peak 75 crew and 278 draw calls; nobody stuck. |
| day_check day 1 | OK. 128 joined and served, longest wait 3.7 min, trays 125/125, nobody gave up. |
| food_check (days 1-7) | FOOD CHECK OK |
| events_check, patched | EVENTS CHECK OK |
| Table probe (sim-d59c30b-table-probe.py, from the plans) | **Day 7:** 46 at the Sunday table (18:00). Half seated by 18:02, 90% by 18:12, the last at 18:21. **Day 14:** 41 diners. The line opens 17:35; half by 17:59, 90% by 18:09, the last at 18:12. |

The table is full by about 18:20 and waits are short, as the lead asked.

**Low (worth a look by the sim engineer):** on day 7 at least one table diner has no tradition line visit before sitting. My probe found their nearest earlier queue was breakfast (07:27). That's probably the host, or someone the "held up" branch seats directly. If it's anyone else, they sit without a tray.
