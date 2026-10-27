# Overnight decisions: lead 41 (night of Oct 26-27, 2026)

The user, ~03:35 UTC Oct 27 (11:35 PM Eastern): "Please only 5 workers going tonight. Going to bed. overnight mode. Finish all current work then make step 6. Then a controller update. Goodnight."

Overnight mode (as before, roadmap-after-recdeck.md): no messages to the user; the lead takes the recommended answer to every question and logs it here, so the user can change any of them in the morning.

## The order
1. Finish 0.94.0: reviews (RV23), merges + switch-on (BM19: P5_STEP5, EV_VESSEL_ON, EV_ENDING_ON on; older switches stay off), gate, full round, publish.
2. Step 6 (plans/p5-step6-spec.html on claude/p5-specs; the user's answers: all recommended, see handover-lead39.md).
3. The controller update: PAD_ON on (the user's rule: "until we update once content complete"), after Step 6.

## Decisions
| # | Question | Decision (recommended) | Why |
|---|---|---|---|
| 1 | Old links (owned by the old account) or new links? | **New links** published from this account (Playtest + Dev). The old links and the user's save link 6daN are untouched. | This account can't update the old ones and the user is asleep; new private links lose nothing. The user carries the save over with Download my save / Load a save file. Switch back to the old links if the user shares edit access. |
| 2 | Six runners for the full round with a 5-worker cap? | **Every check still runs (the full round); the six shares are spread over as many runners as the cap allows** (the build master runs one share itself). | The user's cap tonight beats the six-runner habit; the rule's point (every check, before publishing) still holds. |
| 3 | Start Step 6 while 0.94.0 finishes? | **Only its foundation turn** (the Works career engineer's first turn: switch lines, section 28, ladder rows, held hours; all OFF, cadet identical), on top of staging-0.94.0. Wave 1 starts once 0.94.0 is published. | Keeps "finish current work first" while using a free seat; the foundation touches only new lines. |
| 4 | Step 6 needs 5-6 builders + a writer + reviewers; the cap is 5. | **Smaller waves**: at most 5 seats at once in all (builders + reviewer + build master). Builders bake their own stand-in words (as Step 5). | The user's cap. |

## Clarified by the user (~03:40 UTC)
"When I say 5 workers I mean 5 active ones": the cap counts seats **working at the same time**. A seat that is idle (waiting for a verdict or its next wave) doesn't count, so idle seats can stay rather than being archived and re-hired. Decision 2 follows: the round can use up to 5 runners at once while the others wait.
