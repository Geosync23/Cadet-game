# Handover: lead 48 -> lead 49 (written 2026-11-01 ~01:30 UTC / 9:30 PM ET Oct 31)

Lead 48 = session_014zyJYMuqdRYh4dQhmVPr8S, branch claude/lead-48 (TEAM.md log current; read from "LEAD 48 started").
Read first: CLAUDE.md, plans/handover-account.md (the account move: links, saves, how a new account starts), this note,
the bottom of TEAM.md on claude/lead-48. Before this: plans/handover-lead47.md, plans/patch-0995.md.

## Where things stand
- **0.99.5 LIVE** on this account's links: Playtest https://claude.ai/artifact/CqUGjQXerhSKxuu4umhK41 (v2), Dev
  https://claude.ai/artifact/Sm86UjQMH1NmBj5ybNnB2b (v2). claude/integration = main = 6475bb30 (game 93aed54f...5164).
  The user was sent a push notification.
- **The project is being moved to another account (the user's request).** On the new account none of the sessions
  below can be reached; hire fresh seats from the handover notes (list in handover-account.md section 4).
- All of lead 48's scheduled tasks are disabled (hourly check-in trig_01J4iUoMZftMjpbxn9eF28XR; lead 47's
  trig_01W67fhJjcRCn6ahnaNdc351).

## What happened in lead 48's watch (details in TEAM.md)
1. BM23's re-gates found interactions whole FAIL: Works tea corner hot water gave an armchair (TRAD995_ON note 10 moved
   5-tea-3). RV30 built the fix ee66e35 (ixTeaFirst, behind TRAD995_ON), RV29 PASS, merged.
2. Round on e00bfabd. R1 found two NEW FAILs, both check-side, game unchanged:
   - arrows_check week: the walker opened Brennan's chat instead of a real tap (spice join), and kept running on the
     gym locker's treadmill. RV30 check fix cc18dad.
   - puzzle_check: (a) paper run thin sample (6 repairs offered vs 10; ~1 in 10 roll) -> RV30 93839bf counts offers;
     (b) p5's first 'none': P5FIRST set cond 90 then moved the clock back Day 33 -> 18, so machinesNow reset and
     replayed every machine. BM23 bb45099 (clock first). Lead's switch bisect: only SPREAD_ON off passed; a
     fixScanMachine change did NOT help (not the scanner).
3. All five shares OK; BM23 final GO 6475bb30; PUB3 published v2 on both pages (scan clean, 390x844 PASS x3).

## Seats at the end (all on THIS account; all stopped or idle)
| Seat | Session | Handover |
|---|---|---|
| BM23 build master | session_014zyJYPpetpQqNvn9pkGrig | plans/handover-bm23.md (claude/handover-bm23) |
| PUB3 publisher | session_014zyJYQ6fZqmqTjgzdCaumh | plans/handover-publisher-3.md (claude/publish-pub3) |
| RV29 reviewer | session_014zyJYM3D7UBkZN49CsZVuA | plans/handover-rv29.md (claude/review-rv29) |
| RV30 reviewer | session_014zyJYNFR7ewWJGvEQNUAHr | plans/handover-rv30.md (claude/review-rv30) |
| R1-R4 runners | R1 ...YQ4EiB7CipGp4HsYV8, R2 ...YMsL5YqKnLb9Q6Lvyz, R3 ...YPN2WU6wpJgghsXiAe, R4 ...YNRijQBB389vXWxWNJ | results plans/checks-0995-rN.md (claude/checks-0995-rN) |

## Backlog for the next 0.99.x (plans/backlog.md)
P5-1 first (p5Stage marks the first "follow the line" case 'none' for good after one failed set-up; old, both builds;
let it retry later). Then JB2-2 (gym locker stop is a treadmill: tapping the model starts a run), JB2-3 (fewer repairs
since note 15, so head-scratchers are a little rarer; ask the user whether to raise caseRate), and the list in
handover-lead47.md (BM22-1..3, JB2-1, TB3-1/2, TB4-1, TB5-1, RV29-1, PL2-1/2, CT5-1..3). Still open, the user decides:
the read-only code review for waste and inefficiency.

## Gotchas learned
- Messages cross a lot: restate decisions; check a seat's pushed branch before trusting "pushed".
- A FAIL that only appears with a switch on: bisect by turning switches off one at a time on copies (puzzle_check
  ~4 min each; the lead can run it locally: pip install playwright numpy pillow, three r128 in CADET_WORK,
  CADET_CHROME=/opt/pw-browsers/chromium).
- Don't let a builder's own long gates block a reviewer: push early, review in parallel, and don't run the same long
  gate twice (builder vs build master).
- Checks that move the ship clock backwards replay every machine (machinesNow -> machinesReset).

## Open questions for the user
- JB2-3: should head-scratcher puzzles come back to the old rate (raise caseRate a little)?
- The code review for waste and inefficiency: go or not.
- After moving saves to new links on the new account: which link is the new "current save" link for CLAUDE.md.
