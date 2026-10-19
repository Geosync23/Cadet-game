# Starship Cadet: start here (handover to a new account, 2026-10-19)

Work is paused. Everything is saved on GitHub; nothing is running.

## Read first
1. `CLAUDE.md` (how we work), `DEV_NOTES.md`, `design-doc.md`.
2. `plans/handover-lead.md` — read the last section, "HANDOVER TO LEAD 20": the formal handover for the next lead (fresh seats, who to start, what each reads).
3. `plans/start-prompts-lead20.md` — ready-made start messages for each new worker.
4. `plans/roadmap-after-recdeck.md` — what comes after the rec deck, in order, and the approved ways of working for a big codebase (set up with the split).
3. `plans/overnight-decisions.md` — every call made on the user's behalf; the user's own answers are at the end.

## Latest versions
| What | Branch / commit | Link (owner's account) |
|---|---|---|
| 0.63.5 Playtest Update (newest finished build) | `claude/p5-cand-s5` 38dcac4 | https://claude.ai/artifact/JMX6JPU4wTz3SaejZ2WxVU |
| 0.63.4 Step 4 | `claude/p5-cand-s4` aa4f42c | https://claude.ai/artifact/8Uo2bYs4FaUjXLYGueqw4G |
| 0.64.0 Rec Deck (NOT finished) | `claude/rec-cand-s1` cf55b35 | not published yet |
| Kayak / wall / pool prototypes | `claude/kayak-proto` | waiting for the user to test |

`main` and the main game link have not been touched; merging into main needs the user's go.

## Finishing the rec deck (0.64.0), in order
1. Read `plans/handover-build-master-9.md` (on `claude/rec-cand-s1`): the state of every check.
2. Read `plans/handover-rec-rc.md` (on `claude/rc-wip`, WIP 1030f4d): the determinism fix is done (machine_check OK on and off). Left: day_check days 3-8; (A) Maeve's rec round lift rides count as on-shift (day_check 476/480); (B) career pace — if a busy player still reaches "Relied on" before Day 5, rec machine jobs give half career xp (one named constant; the check's band unchanged). Then rebase onto `claude/rec-cand-s1`.
3. Rerun machine, day 0-8 + 14/21/28, events, deck, career, cadet (REC_DECK=false must equal the 0.63.5 game), then the rest of the round (list in `plans/brief-recdeck.md` "B").
4. Review the fix, read the whole file for outside links/personal data, publish as a new page titled "Starship Cadet Rec Deck".

Other notes per role: `plans/handover-*.md` (rec-ra on `claude/rec-crew`, rec-rb2 on `claude/rec-works`, writer-w3 on `claude/writer-rec`, build-master-8, reviewer-r7 on `claude/reviews-r7`, crew-sim X3 on `claude/crew-pt1`).

## Things for the user to look at later
- Tracked panel fills almost the whole screen on a small (320 px) phone.
- Two wall faults at once can leave you queued for a climb that never comes.
- Rec talent night only moves for the yearly talent night (day 152), not other busy days.
- Two small old bugs: an unclosed CSS comment (~line 181) and a hidden door gear (~line 1724).
