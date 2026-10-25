# Handover: lead 35 → lead 36

## START HERE (lead 36)
1. Read CLAUDE.md, this note, plans/patch-0.92.6.md, plans/patch-0.92.5.md, then the bottom of TEAM.md on claude/lead-35 (from "LEAD 35 took over").
2. Branch `claude/lead-36` from `claude/lead-35`; push only there. Read the game from origin/claude/staging-0.92.5 (or integration), never the lead branch's copy (stale).
3. Make your hourly check-in (create_trigger, cron `57 * * * *`, into your session), then disable lead 35's trig_01CCMLzJ1TikrbvoD9CLh8hG.
4. Message every working seat with your session id (priority "next", never "now"). Tell lead 35 (session_01VQkkt8RXcvvGs1Dmzn2emM) you've taken over.
5. The user is in US Eastern (EDT, UTC-4). Plain words, no emojis, few messages. Cap: at most 8 seats working at once. During a six-runner round (BM + 6) only 1 other seat works; pause builders.

## State at handover
- **0.92.5**: frozen candidate claude/staging-0.92.5 53c11f8 (same bytes as 19a7c30; game sha256 fddc0ef61c68ac012409a0f88e4ded2a62098b28377760461d99fb144b595559). Round started ~05:47 UTC by BM17 (session_01WxdNuUeTUoneMvqKiF6GQL), OLD = ba836359. Contents: patch-0.92.5 items 1-12, 14-22 (13 dropped), sim bay ON, weekend traditions ON (4-week rotation, the user's), item 8 Mum "chick", item 22 every lesson's job on the board (FX15). Known-old FAILs: backlog 12, 14; RV14-1 food_check 7 7 window; 7 expected weekend perf flags (CR2).
- **Next for 0.92.5**: BM17's go/no-go → show the user in the morning → ONLY on the user's say: PUB1 (session_01GnpjFR6oumvuvTrmcXSqeg) updates Playtest 3HqM5xiXaHXzgrpq7JbesJ + Dev 9ZWAgqiZCvkJvVjjhjVkEr (confirm with the user); NEVER the current-save page 6daNCLCJAcsLCZn27CEthq. Then ask the user's OK to fast-forward integration.
- **0.92.6** (plans/patch-0.92.6.md, the user's overnight notes + crew stories): builders branch from b0916bb1, merge 19a7c30 after the round. All behind switches, switched on after review.
  - FX17 session_01YKeSjUhEnJRbmjyHz2aa6u: traditions 2,3,4,5,7,8,13,15 on claude/p926-fx17 (P926_TRADS; p926_check.py). Words SW2 ac684e57 (FINAL PASS). Reviewer RV14 session_01RwUYVcYt2PP7B7g3ogduFZ (~30%).
  - FX18 session_01V2XNs79MARor5fuig48bVF: items 1 (auditorium 4 m open archway), 6 (bench bar), 12 ('→ Tracked'), 16 (Lift button, also in the car), 17 (outfit line) on claude/p926-fx18. Reviewer RV15: NOT HIRED YET.
  - FX19 session_01VCJjaLf6ZHwNM9YQ5GH9vf: promotion 14/18 + trained jobs 11 + quarters can't be missed, on claude/p926-fx19 (PROMO_SIGHT_ON, BOARD_TRADE_ON). USER DESIGN: test the next workday after **Reliable** + Making it safe + not before Day 9 (asked, answered). Calder walks you next day if the cabin walk was missed. Calder never says "well done" before her payoff (3 lines changed). Reviewer RV15.
  - FX21 session_01PK2uvMjSsonGWpsJpRymqs: crew stories stage 1 (Pell, Theo, Basil, Halloran, Kovac, Saad) on claude/p926-stories (STORIES_ON; STORY_MOMENTS; stories_check.py). S1-S5 built; S6 tuning with CS1; S7 switch-on needs the user's yes. Lead chose (A) planner hook: crescendo person + cast go to the gathering on the story's fixed days (switch on only, free only). Words CS1 session_01QcPAXHjQZ2HfZKMCTbaW9v. Reviewer RV16: NOT HIRED YET.
  - SW2 session_01E4qPjPEbEsohiaqRLm3Nyb (~17%): writing appointments (item 9) on claude/p926-appt-words. USER answered pitch CTLouY4DK2gFuWBF8YwS3L: yes to all but the helm chair; "appointments work like ship traditions but one on one or very small group". Builder FX22: NOT HIRED YET.
  - Item 10 (many more simple jobs around the ship, not the bridge): FX20 NOT HIRED YET (after FX19's board weighting).
- The 8 new traditions (told the user): Tool night D29 Kovac; Route night D38 Raman; Window sketching D48 Luca Alvarez; Open house D53 Ferreira + Holt; Garden walk D63 Tove Cruz; The spoon band D64 Femi Rossi; Card night D73 the Counsellor; Worst joke night D81 Holt (+ Halloran). Six weeks aboard D42 (Zeke), Twelve weeks aboard D84 (Calder toast).
- After the round: un-pause FX17/18/19/21 + CS1 (tell them "round done, merge 19a7c30"); hire RV15 (FX18 + FX19), RV16 (FX21), FX22 (appointments), FX20 (simple jobs) as the cap allows; a BM for claude/staging-0.92.6.

## Idle / retired (handover notes exist)
BM16, DS1, DV1 (plans/handover-dv1.md on claude/handover-dv1), FX9, FX12, FX13, FX14, FX15 (idle, low memory), FX16 (weekend; plans/handover-fx16.md), RV12, RV13, SW1, ZW1, PUB1 (idle), CR1-6 (in the round; CR2 needs a fresh replacement after this round).

## Gotchas
- Never priority "now". Check shas on origin before believing "pushed". Force-add PNGs.
- Sessions underestimate their memory: ask for real usage.
- Two builders on one branch collide: after a handover, tell the old one to stop pushing.
- The user played 0.92.2 (their save), not 0.92.4, for the overnight notes.
