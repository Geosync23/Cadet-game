# Handover: social engineer B (Pillar 4, seat 4, "social stories")

Written by session_019aEJaAGyZir9oq47CBRfA3 at 0.39.6, ahead of the memory rule, so a fresh session can take over.
Read CLAUDE.md, DEV_NOTES.md ("Social stories (20c, social engineer B, 0.39.x)" has every detail and the hook register),
plans/social-deep-plan.md (the design; Parts 1, 3, 6, 8b, 9, 12) and TEAM.md first.

## Next job: B8, calls home (approved by the lead, 2026-10-17)
The user's ask: people back home (Mum, Gran, Jo, Sam) the player calls, with whole arcs; the shapes agreed with head
writer 2 (session_01HNrh3xCtczeZM5NVFrE6pa) are under "Loose ends" below. **The lead's one change: calls any day, once
per contact per day; Letters evening (Sunday, the booths) is the best relay window, where the big live beats land.**
**Revised by head writer 2 after the lead's approval (2026-10-17 04:30):** home stays unnamed ("home"); at the booths
you can call each person once a day, any day: a live call scene (everyday talk from HOME_REPLY, or a beat if due).
`via: reply` / any-day beats play on an ordinary call (a little lag); `via: live` beats wait for Letters evening (a
clear line, no lag or drops; crew gather at the booths for their overheard calls). Recorded messages with Mail replies
are an optional extra (the device engineer retired; the Mail `play:` field is optional). Pacing as agreed: 7+ days,
a call since the last beat, one home beat a day. Head writer 2 writes content/home/mum.arc as the model.
Build it in 20c on the moments engine; ask the player engineer (booth -> `homeCall()`), the device engineer (Mail
`play: '<momentId>'`) and the traditions engineer (Letters evening) for their one-line hooks through the lead.

## Role, branch and builds
- Branch `claude/social-stories`, builds 0.39.x. Last: **0.39.6** (B4 first part). 0.39.0-0.39.3 passed reviewer 1
  (31f8aea); 0.39.4-0.39.5 sent for review (368ae8a); 0.39.6 in its check run when this was written.
- I own only the marked sub-block **`// 20c. SOCIAL STORIES`** at the end of section 20 (before `// 6. CAMERA`), ending at
  `// ---- end of 20c ----`. Section 20 itself is social engineer A's (session_012pK2XVi5UhqEd28fakYk68, `claude/social`).
- I merge `origin/claude/social` into my branch now and then, so the lead's merge of B after A is clean. The only
  conflicts so far: the HUD build line and `GAME_BUILD` (keep mine) and lines A changed next to my hooks (take A's).
- schedU keys 672-699 (A has 644-671). Used: 672 thread guess, 673-678 voice words, 681 introductions.
- Report every push to the lead (now session_01PJtmxWgAPLebXSZKP6ZRpG) with send_message; reviewer 1
  (session_01HK4m33sUiLuVim8VWaCPMs) reviews my branch: tell it when a set of builds is final. Only the lead talks to
  the user.

## What's built (all in 20c)
- 0.39.0 B1: `voiceOf(id)` (writers' VOICE > roster fields > template > a guess from traits/habits), `voiceWord`,
  `voiceFill` (hands off to section 22's `linesFill`), openness via `relGain` (only when written, never guessed),
  `STEP_GATES` / `stepGate` / `metDays`, "What you know" by section (`knowSections`, `knowBlocks`).
- 0.39.1 B2: bonds in `SHIP.social.bonds` (friends, best, rivals, drifting, mentor; `storyHour`), `socBondOf`,
  introductions (`introOptions`, `introDo`), the weekly snapshot for `affinityPlan` (`affPlanWeek`), `friendCap`.
- 0.39.3 B3: moments (`momentReady`, `momentShow`, `momentDone`, `momentDef`, `MOMENTS_BUILTIN` for Tomas/Pell/Rina
  beats 2-4), state in `SHIP.social.stories`; sparse snapshot (pairs at |aff| >= 30, the lead's OK).
- 0.39.4 B5: goodbye moments (`goodbyeMoment`, `goodbyeDef`, `goodbyeDone`).
- 0.39.5 B6: couples from the roster's `partner`; the engine reads the dialogue engineer's baked `MOMENTS` /
  `MOMENT_THEMES` shapes (gaps, `when` via `linesOk`, `where` calm/visit/appt/meal/any/room, `duty`, `them`, `needs`,
  `mem`/`flag`/`favour`, `warm`).
- 0.39.6 B4 (first part): `arcCrew`, `where: meal`, `STORY_FAVOURS` (favours that matter on A's favour API).

## Shared formats others rely on
- Section 20 calls (typeof-guarded): `relGain`, `knowBlocks`, `storyHour(h, pairs)`, `affPlanWeek(i, j, d)`,
  `momentOwnsBeat`, `momentReady`, `momentShow`, `momentHint`, `goodbyeMoment`, `socBondOf`, `introOptions`, `introDo`,
  `friendCap`, `arcCrew`. Section 18 calls a script's `onPick` / `onEnd` (MEETING_SCRIPTS['moment:<id>']).
- Saved by section 20: `SHIP.social.bonds`, `SHIP.social.affWeek`, `SHIP.social.stories`. I never touch socSave.
- Posted on the bus: `simNote('bond', { a, b, kind, was })`, `simNote('moment', { id, who, beat, flavour, tone, fit })`,
  `simNote('introduced', { a, b, you })`.
- Frozen spellings: bond kinds (A's `SOC_BOND_KINDS`), thread themes (homesick, exams, family, stuck, notgood, lonely,
  loss, talent, burnout, leaving, rivalry, startover) and `arc:<arcId>`.

## Loose ends
- B4 goes on as the writers deliver: head writer 2 (session_01HNrh3xCtczeZM5NVFrE6pa; the first head writer retired)
  has my notes on Calder (rep), Holt 1 (`where: meal`), Marrow 1 (`mem:readyroom`), Pell 7 (`duty: true`).
- The dialogue engineer made `rep:` / `ship.*:` mean "this band or better" (claude/dialogue 0.43.9) and `deck:` the
  player's deck (pass ctx.deck or leave it out), so Calder's and Holt's beats work as the writers meant.
- New ask from the user via the lead: calls home (Mum, Gran, Jo, Sam) with whole arcs. Agreed shape with head writer 2
  (they send the lead the proposal): HOME_CONTACTS, HOME_MOMENTS['<contact>:<n>'] (MOMENTS shape + `via: reply|live`),
  HOME_SEND, HOME_REPLY baked by the dialogue engineer from content/home/; state in SHIP.social.stories.home; pacing:
  a message since the last beat + 7 days; flags (home.gran.hip) and simNote('homeCall') for crew to ask after them.
  Hooks to ask for: section 15's "Calling home" activity calls `homeCall()`; the device engineer plays a Mail with
  `play: '<momentId>'` through `momentShow`; Letters evening (section 18) for live calls. Not built yet (B8, once the
  lead OKs it). Non-crew speakers work in section 18's panel (an unknown `who` shows as its name).
- Theme moments (MOMENT_THEMES) are baked but empty until the writers write them; the engine is tested with stand-ins.
- The sim engineer (session_01R6RBwwBM9aorpsqDCrztDU) passes the day to `affinityPlan` from 0.26.26: seating follows
  the weekly snapshot from week 2 once combined (an explained day_check/cadet_test difference past day 14).
- No drifting bond appears naturally in 42 days (friends meet daily); the designer accepted it (it'll come with
  shift changes and transfers); the forced test (a pair kept apart 3 weeks drifts on day 19) is the check.

## Gotchas
- 20c sits after section 20 but before ROSTER (section 9): everything lazy; `socInit()` first.
- Never declare `MOMENTS`, `MOMENT_THEMES`, `VOICE`, `VOICE_TEMPLATES`: section 22's generated block does. Read them
  through `momentBaked()` / `voiceData()` (try/catch for not-yet-declared consts).
- `affinityPlan` must stay pure per day: only the weekly snapshot, never live affinity.
- `pkill -f "_check.py"` from a Bash call can kill the call itself; stop a check run by its own task instead.
- Edits to DEV_NOTES' build table: keep one row per line (a slip once joined two rows).

## How to test
- Scratch folder with `new.html` (my build) and `old.html` (A's latest `claude/social`), then the full set one at a
  time (my `all.sh` in the scratchpad did: social, deck, day 1, player, events, interactions, food, machine, device,
  then cadet_test old vs new). device_check fails "Needs: the bar pulses while it has just risen" on plain 0.41.10 too:
  not ours.
- Feature tests used small scripts on cadet_test's `Game` class: a moment end to end (`momentShow` then `dialogueStep`),
  goodbyes (set `p.aboard = [null, day + 2]`), couples (set `partner`), bonds over 14-42 days, and the writers' 45
  moments on a scratch merge with `origin/claude/content` (a git worktree, so my branch isn't touched).

## Open questions for the user (through the lead)
- None open on my side. Numbers (moment points, gates, friend caps) are starting values to tune in play (A12/B7).
