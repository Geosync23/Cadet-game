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
3. **Combine and test (BM3, `claude/cand-0607`):** merge order PE6, deck, sim, systems, social, traditions, onboarding 3, onboarding 4, writer. BM3 builds candidates on claude/cand-0606 (its only push branch); the lead starts check runners when the first candidate is ~30 min away. Every seat sends hashes and verdicts to BM3 directly too; check runners spread the full set.

## Seats and branches
| Seat | Session | Branch | Plan items + the user's 0.60.6 notes |
|---|---|---|---|
| Player engineer 6 | session_01AWgP6kgzpprnpA5pMAAiqq | claude/player-needs | Plan list, minus the lift goal mark (already shipped in 0.60.6a), minus the shelf taps (moved to systems). Plus: **low-need pop-ups** in plain words ("You need to pee", one per need, once as it crosses the low line, never stacked or over a card); **the time clock gets a pop-up screen in the device's art style** (clock in / clock out / your hours). |
| Social engineer (new) | session_01Q6zXcCnBpTeJQrUP8qPKUP | claude/social-0607 | Plan list. |
| Traditions engineer (new) | session_018vCE4Nv4tCR3YvNX7GTE3c | claude/trad-0607 | Plan list. |
| Deck architect 4 (new; DA3's note: `plans/handover-deck-architect.md` on claude/poses) | session_01P6DtVbtWZs9i82fJ4UzRuB | claude/deck-0607 | Plan list. Plus: **junior officers on Deck 4 lie crosswise in their beds** (fix the sleeping pose/orientation); **remove the tray return from the mess hall** (with the sim engineer, see below). |
| Sim engineer (new) | session_01F7zv2wjhyPPuoHxM8hFzzy | claude/sim-0607 | Plan list. Plus: **no tray return**: crew stop walking trays to it; the user decided: a tray simply goes away once the meal is completed (no clearing walk); keep the galley/dish pit flow working. Check food_check. |
| Systems engineer (new) | session_016Mv2wxrtkGgAwcst4GWADY | claude/systems-0607 | Plan list, plus the shelf taps (right part from the right shelf, the glow). |
| Onboarding engineer 3 | session_016TRcnsFqFB1q5zZp6vjGBn | claude/arrival | Plan list. Plus Zeke on Day 0/1: **not already in the mess hall** when you ride up to dinner on arrival night (he arrives with you); **always with you after the first lift ride down to Deck 4**; **the shuffle-aside (moving past people) works for him while he follows you**; **he stays with you between jobs** (doesn't stop when one ends and restart when the next is picked); **he acts as a trainer on Day 1**, saying more about each job (the head writer writes the lines; a sample is pitched to the user first). |
| Onboarding engineer 4 (new, split from onboarding 3) | session_01MeEsh5sp4RyuD7KwdQEbLC | claude/arrival-0607b | Clothes and laundry (Day 2, Zeke warns you; agree the hook with onboarding 3), your first delivery on Day 3. Builds 0.42.40+ (onboarding 3 keeps 0.42.31-0.42.39). |
| Head writer (new) | session_013DdpJv4AKFJcvuBBqjSXms | claude/writer-0607 | Plan list (~500 lines). Plus: Zeke's trainer lines (pitch ~10 first), the low-need pop-up texts, the time clock screen's words. |
| Build master 3 | session_01WrXgDfR5dzwktKJfYwVwsV | claude/cand-0607 | Combine, check runners, results to `plans/cand-0607-results.md`. |
| Reviewer 0607 (new) | session_01BusfBzBamabWrCsrwQeABh | claude/reviews-0607 | Reviews each piece as it lands. |
| DA3 | session_01NsysH87qqJnf1dBEVRz2fW | claude/poses | Stays idle as the expert on poses for questions; the dinner-profiling item goes to the sim engineer if time allows, else 0.60.8. |

## Handoffs (the user's request, 2026-10-18 ~04:10)
- The lead checks every helper's memory at each hourly check-in (get_session context_usage). At ~60% a helper is told to finish its piece and write its handover note; at ~70% it hands over at once.
- **Replacements are always started by the lead** (a depth-0 session), never by a helper, so each new session starts with a fresh lineage and can itself schedule and (if needed) start sessions. Older helpers (BM3, PE6, onboarding 3) were started by late leads and may be near the depth limit: they ask the lead to start any session (check runners included).
- A helper that sees its own memory near 60% tells the lead without waiting to be asked.

## Team trimmed (the user, ~04:10)
- The sim seat folds into systems (systems takes the bartender rota, shower queue, crew hobbies and trays); the sim engineer pushes its work and a note (`plans/handover-sim-0607.md` on claude/sim-0607) and is closed.
- Onboarding 3 does only Zeke's five fix notes, then hands over; onboarding 4 takes clothes/laundry, Zeke's Day 1/Day 2, then the Day 3 delivery.
- Check runners: 2 (INTRO alone; DAYS + PLAYER + PERF staggered on the second); BM3 runs the rest.
- Merge order: PE6, deck, systems (incl. sim), social, traditions, onboarding 3, onboarding 4, writer.

## Rebalance (lead, ~04:42)
Systems was the long pole. The old sim items move to the social engineer (finished and idle): trays, morning() slotting for the morning traditions, the day-100 seat share at 3-mess-12, bartender rota, shower queue, crew hobbies (in that order), on claude/social-0607 from 0.36.85. Systems keeps shelves (0.33.41), the Wednesday delivery (0.33.42) and moving Bea's Day 1 vent later.

## PE6's list split (lead, ~05:08)
PE6 keeps: Hobbies app, time clock pop-up, bathroom rate + toilet icon, tray text, player_check one-liner. Moved: Gym club member + Tiles table any time → traditions; the bar order → social; low-need pop-ups + first-evening tips + Ideas card + Settling-in items → onboarding 4. All build on PE6's hook 52839a6.
**Split cancelled (~05:10):** PE6 had already built every moved item locally (0.28.62-0.28.64, pushing ~05:30). All stay with PE6. Added for PE6 (the user, ~05:10): gardening counts as a hobby (leisure) with a tip; head writer writes the lines.

## Lead 11 (from ~05:35)
Report to lead 11, session_01YKC3CGA9VS4b7wuqLbPT7V (lead 10 is idle). ~06:01: **build master 4** session_013h22isZZqmJJSEKSbrwabf started (push branch claude/cand-0607) to take the 0.60.7 candidate from BM3 (~58% memory) at its next quiet point. DA4 bisects the day_check day 3 'kovac-zainab Deck 5 stuck' failure.
