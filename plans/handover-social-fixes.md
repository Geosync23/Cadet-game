# Handover: social & traditions engineer (the user's social fixes, 0.62.x)

Written by session_01RvxnkWWPF4SF5ygWT4CvQE at 0.62.6. Read CLAUDE.md, DEV_NOTES.md (rows 0.62.0-0.62.6; "Social stories
(20c)"; "Social life", Save bounds), design-doc.md ("Ship traditions", "Calling home") and plans/handover-social-stories.md
(20c's owner before me) first.

## Role, branch and builds
- Branch `claude/social-fixes`, builds 0.62.x. Lead: session_01KPJMYjXAPkNUcrQ8VRkhLE. Reviewers: 1c
  session_01YcSJkhhJ2MnCjsJs7QV8ud (passed 0.62.0-0.62.4), 1e (passed 0.62.5, reviews on claude/reviews-4).
  Head writer 4 (calls home content): session_01MWyyMaXv6D7yKtDNy9VbCA.
- History: 0.62.0-0.62.4 started from 0.60.4 (d449914) and were merged into 0.60.5. On the lead's ask the branch was then
  reset onto 348b1d8 (0.60.5a) for 0.62.5 (shipped as the 0.60.5b hotfix) and 0.62.6 (for 0.60.6).

## What I built (the user's notes on 0.60.4 and 0.60.5a)
- 0.62.0: no promenade trestle (Sunday long table, harvest and farewell suppers): only the 4 end chairs in the mess
  (`MESS_EXTRA.heads`, places `3-longtable-1..4`); overflow eats an ordinary dinner. Letters evening deleted
  (content/traditions/letters.trad, re-baked). One call home a day in total (`home.call`, `homeCalledToday`).
  Beats play on ordinary calls when due (7+ days after the last; `homeLive` and the Letters wait are gone).
- 0.62.1-0.62.3: calls are one-sided (only they speak, no choices). `homeChatPick` chooses the scene: news reactions
  once (`c.news`), then a scene about someone else's story, then staged (`when:`) ones, then fresh, else the one heard
  longest ago (`c.h`, the last 16). Head writer 4's content/home/*.call: 6 beats + about 35 scenes a person, 5-7 lines.
- 0.62.4: the booth lists only people with something to play; `HOME_NEWS_MAX` 8.
- 0.62.5: **the "menu disappears" bug.** Section 18's `meetingsTick` closes a dialogue whose `m.where` you're not in, once a
  ship minute. 20c's dialogues had no where, so they closed within a second. Fix: `HOME_WHERE` (the booths) for the booth
  and calls, `hereWhere()` for moments. The postbox is gone too (kit and place).
- 0.62.6: recorded messages use `where: { any: true }`; section 18's `inMeeting` returns true for `any` (one line).

## Shared formats
- `.call` files: see content/README "Calls home" (rewritten by me). The bake already accepts one-sided calls.
  lines_check now warns when a chat HAS a `? send`.
- `stories.home` save shape and its worst case: the 20c header comment and "Social life", Save bounds.

## How to test
- `arc_check.py BUILD 70` (arcs), `... calls` (each person called daily for 70 days: all beats, no repeats in 30, every
  scene heard, no more news scenes than HOME_NEWS_MAX), `... booth` (the real game loop with real taps, click and touch:
  the picker stays and a call plays; a recorded message survives a lift ride). Plus social, events, food, deck,
  interactions and cadet_test against the previous build.
- Setup in a fresh container: `pip install playwright`, three.js r128 into /tmp/cadet-work/three (DEV_NOTES "Testing").

## Gotchas
- **On-paper checks miss game-loop closures.** Anything shown with `dialogueShow` needs an `m.where`; test it with
  frames stepping (`g.step`), not just `g.ev`.
- `pkill -f "_check.py"` from a Bash call kills the call itself.
- With `tail` and several files, use `tail -n N`.

## Loose ends and open questions
- None open. Greyed contacts after the day's call were skipped (the lead: the booth's message is enough).
- Moments keep `hereWhere()` (any room on this deck): a moment started in a doorway would close. Reviewer 1e judged it fine
  (moments start at a crew member's place).
