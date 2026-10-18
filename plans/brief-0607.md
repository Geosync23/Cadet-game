# 0.60.7 brief (lead 10, session_014hkEBULoSV9EKZZSwMWyPd, 2026-10-18 ~04:05 UTC)

The user said go for 0.60.7. Every seat reads, in order: CLAUDE.md, this brief, the plan page, DEV_NOTES.md ("Rules that keep it working", "Testing", the build table), TEAM.md, and its predecessor's handover note.

- **The plan (approved by the user):** `plans/plan-0607.html` on `claude/plan-0607` (published at https://claude.ai/artifact/KMeosKAm5MkLNVDAfdChNS). The "Team and time" section says which seat builds what. Survey answers and the user's verbatim notes: `plans/notes-0607.md` on `claude/lead-pillar1`.
- **Base:** live 0.60.6a = `claude/ship-integration` c8685cf. Every new branch below starts there. Existing seats merge c8685cf into their branch first.
- **Report to the lead** with send_message to session_014hkEBULoSV9EKZZSwMWyPd: one line when you start, one per finished piece (hash, build number, what, checks run), and at once if blocked. Don't send narration.
- **Build numbers:** keep your seat's own series (look up your seat's last row in the DEV_NOTES build table and use the next free number). Never reuse a number another seat uses.
- **Checks:** run the quick checks for what you touched (the DEV_NOTES "Testing" section says which). cadet_test differences must be explained. The build master runs the full set on the combined build.
- **Review:** reviewer 0607 reviews behaviour, save and schedule changes in depth and skims content and test-only changes. Tell the reviewer (and the lead) the hash when a piece is ready.
- **Content rule (the user's):** new kinds of content are pitched first and written in only after the user approves (the lead relays). The plan already approved the new lines it lists; anything beyond the plan is pitched.
- **Phones first, determinism, small exact edits, never rewrite the file:** as in CLAUDE.md.
- **Memory:** hand over at about 70% (write `plans/handover-<role>.md`, push, tell the lead, stay idle).

## Phases
1. **Hooks (about 45 min):** the shared pieces first: PE6 the leisure need (the 7th need) and the Hobby button frame; the deck architect the new places' names (bar, gym machines, wardrobes, shelves, crates, Tiles table, second lift panel), pushed as one early commit so others can use them; the head writer the line-key names. Each pushes its hook early and tells the lead, who forwards to everyone.
2. **Everyone at once (2.5 to 3 h).**
3. **Combine and test (BM3, `claude/cand-0607`):** merge order PE6, deck, sim, systems, social, traditions, onboarding, writer; check runners spread the full set.

## Seats and branches
| Seat | Session | Branch | Plan items + the user's 0.60.6 notes |
|---|---|---|---|
| Player engineer 6 | session_01AWgP6kgzpprnpA5pMAAiqq | claude/player-needs | Plan list, minus the lift goal mark (already shipped in 0.60.6a), minus the shelf taps (moved to systems). Plus: **low-need pop-ups** in plain words ("You need to pee", one per need, once as it crosses the low line, never stacked or over a card); **the time clock gets a pop-up screen in the device's art style** (clock in / clock out / your hours). |
| Social engineer (new) | | claude/social-0607 | Plan list. |
| Traditions engineer (new) | | claude/trad-0607 | Plan list. |
| Deck architect 4 (new; DA3's note: `plans/handover-deck-architect.md` on claude/poses) | | claude/deck-0607 | Plan list. Plus: **junior officers on Deck 4 lie crosswise in their beds** (fix the sleeping pose/orientation); **remove the tray return from the mess hall** (with the sim engineer, see below). |
| Sim engineer (new) | | claude/sim-0607 | Plan list. Plus: **no tray return**: crew stop walking trays to it; the default (lead's call, the user can change it) is that diners leave trays on the table and the galley crew clear them, so nothing breaks in the galley/dish pit flow. Check food_check. |
| Systems engineer (new) | | claude/systems-0607 | Plan list, plus the shelf taps (right part from the right shelf, the glow). |
| Onboarding engineer 3 | session_016TRcnsFqFB1q5zZp6vjGBn | claude/arrival | Plan list. Plus Zeke on Day 0/1: **not already in the mess hall** when you ride up to dinner on arrival night (he arrives with you); **always with you after the first lift ride down to Deck 4**; **the shuffle-aside (moving past people) works for him while he follows you**; **he stays with you between jobs** (doesn't stop when one ends and restart when the next is picked); **he acts as a trainer on Day 1**, saying more about each job (the head writer writes the lines; a sample is pitched to the user first). |
| Head writer (new) | | claude/writer-0607 | Plan list (~500 lines). Plus: Zeke's trainer lines (pitch ~10 first), the low-need pop-up texts, the time clock screen's words. |
| Build master 3 | session_01WrXgDfR5dzwktKJfYwVwsV | claude/cand-0607 | Combine, check runners, results to `plans/cand-0607-results.md`. |
| Reviewer 0607 (new) | | claude/reviews-0607 | Reviews each piece as it lands. |
| DA3 | session_01NsysH87qqJnf1dBEVRz2fW | claude/poses | Stays idle as the expert on poses for questions; the dinner-profiling item goes to the sim engineer if time allows, else 0.60.8. |
