# Handover: FX17 (0.92.6 traditions builder; the reserved-job fix for 0.93.0), 2026-10-25

**Role:** builder under lead 35, then lead 36, now lead 37 (session_019GcNZ4GGEqfiuYDYnue7nX). Reviewers: RV14 (0.92.6 items),
RV17 (Line fix, m17), RV16 (session_01ELg87ZGa4f9GTgTJMx39W5: the reserved-job fix). Build master BM17 (session_01WxdNuUeTUoneMvqKiF6GQL).
Words: SW2 (session_01E4qPjPEbEsohiaqRLm3Nyb), voice CS1. FX22 (session_013hfW44u1PvirfEXtYYtwVF, item 9 appointments) builds on my work.

## Branches
| Branch | What | State |
|---|---|---|
| claude/p926-fx17 | 0.92.6 items 2, 3, 4, 5, 7 (a, b, c), 8, 13, 15 behind `P926_TRADS` (on in 0.92.6), the Line fix (27ad3cba), mech_check m17 (eba4d365) | RV14 PASS (fa4c1d38), RV17 PASS (3e8c78a6, eba4d365); in staging-0.92.6 / integration |
| claude/fix-reserved-job | from integration 5898c190: jobMakeWay (section 15) + evMeetClash reading only the calendar and the cast | ba6632b9 pushed, with RV16 for 0.93.0's round |

## What I built (all in section 18's Traditions engineer slot unless said; plans/build-table.md rows "p926-fx17 ...", "fix-reserved-job")
- **13 talks spoken:** talkTick (the speaker says talk.<speaker> from the stool/ring; the question card after: talkAskScript, talkLater). Full rota to Day 84 in REC_TALKS (SW2's speakers; Brennan's and Oduya's talks parked). A talk's speaker is planned as its host (eventPlan host flag).
- **8 join to the end:** host jitter 0 and leisure to the end (section 14), tradJoinMinute's fallback leader, the device lists traditions that are on (section 19, RV14 signed off).
- **5 One week aboard:** TRAD_JOIN + week1Card (week1Ctx: jobs, a tradition, the friend). **2 swap meet:** 3-swap-stall-1/2, 3-swap-browse-1..4, swapCard, swapSay. **15 spice:** 3-spice-host, crewHold on Brennan (looks only), spiceFrame/spiceCard, SPICE_JARS or LINES['spice.jars']. **4 reading corner:** Esme hosts, ids 3-lounge-25..29,31,33, readSay. **3 Winner stays on:** stay 150-270, stayMid (evStay, key 1041), odds +.3.
- **7:** eight new .trad (k 712-719, "every 8 weeks"), milestones (710, 711), window-sketch-2 (k 720, Lumi Achebe from Day 77), P926_NEW (loader skip; skip on days the host isn't aboard).
- **Shared helpers:** tradTalk(id, say), trLine, cardWhere(e) (a card's `where`: the tradition's rooms + the room you're in, else anywhere; FX22's apptScene uses it), p926Where(e), evMeetClash (nobody at a stay/new tradition over their ship-wide event meeting).
- **Checks:** p926_check.py (parts 13 8 5 2 15 4 3 7; on/off copies named by pid). events_check knows the rota, 8 weeks, a speaker's 5 early minutes. mech_check m17 compares rules, not crowd counts. lines_check knows {jobs} {spice}.

## Loose ends
- backlog FX17-1: talent night's card (recActCard) and the Wren talk cards with P926 off close at the next ship minute (no `where`).
- backlog FX17-2: cadet_test's a_start can flip run to run on a busy machine (rerun once first).
- jobMakeWay (section 15) wants its owner's glance (RV16 asked to note it).
- Plan changes ripple through machine wear: a change to who goes where on one day can change repair jobs days later (the Line fix moved Day 11's jobs). Run player_check, mech_check and bigevents_check after any planner-visible change.

## How to test
- Setup: pip install playwright numpy pillow; three r128 + acorn 8.12.1 in /tmp/cadet-work; CADET_CHROME=/opt/pw-browsers/chromium.
- `python3 p926_check.py starship-cadet.html [13 8 5 2 15 4 3 7]` (~5 min a part). Two browser checks at once at most.
- After .trad/.lines/.meet changes: `python3 content_gen.py starship-cadet.html`, `python3 lines_check.py starship-cadet.html`.
- Gotchas: never name a check global HOOK (cadet_test's page hook); a copied tradition's words are getters (defineProperty); `bubbleSay(a.h)` has no `.p`, use friSpeaker(a) in hooked checks; a `until pgrep -f X` loop matches itself.

## Open questions for the user
None.
