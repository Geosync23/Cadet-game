# Handover: head writer (Pillar 4, seat 11)

**Now held by Head writer 2** (session_01HNrh3xCtczeZM5NVFrE6pa, from 0.48.11).

**Role:** head writer for Starship Cadet's Pillar 4. Report ONLY to the lead (session_01PJtmxWgAPLebXSZKP6ZRpG) with
`send_message`; never contact the user. Writers report to you; you are the only one who merges their work. Reviewer 2
(session_0142TQw4ke8caPSyAC93VT98) reviews you. Tradition designers may ask you for a tone check.

**Branch:** `claude/content` (push only there). Builds **0.48.x** (header line ~198 and `GAME_BUILD` ~7047 in
`starship-cadet.html`; keep both in step; a row in DEV_NOTES's build table for each). Last build: **0.48.11** (Head writer 2, b1e454b):
2,502 lines, 83 voice cards (all 74 crew, Saruth, 8 event guests), 10 templates, 87 overheard conversations, 45 arc moments,
12 struggle themes, 4 intro meetings. Next build number: 0.48.12.

## What you own

- `content/` as a whole (merging the writers): `facts.md` (the canon sheet), `voice-bible.md` (tone rules, checklist,
  batch notes), `briefs.md` (who writes whom), `arcs/outlines.md` (agreed with social B), the ten story crew's voice
  cards, the ten templates, the Day 0 meetings `introBunk` and `introChief`.
- `tools/voices_sampler.py` → `plans/voices-sampler.html` (the user APPROVED the sampler, 2026-10-17 ~03:37).
- The baked LINES and MEETINGS blocks (generated; never hand-edit; `python3 content_gen.py`).

## How a round goes

1. Writers push to their branch and message you. `git fetch origin <branch>`, read what's new (`git show
   origin/<branch>:<file>`), against the voice card, `facts.md`, already-told beats and the **no-romance read** (the
   lead's standing rule: every moment and every friend/close line said to the player).
2. Merge: `git merge --no-edit origin/<branch>`. Conflicts are usually `content/lines/pell.lines` (an old tip line:
   keep ours) and, from `claude/dialogue`, the header build line, `GAME_BUILD` and DEV_NOTES's "Current build" line:
   always keep HEAD's side (a small python re.sub keeps the `<<<<<<< HEAD` half).
3. Fix small things yourself; send notes for bigger ones. Approve new canon into `facts.md` section 11.
4. `python3 content_gen.py`, bump the build, add the DEV_NOTES row, `python3 tools/voices_sampler.py`.
5. Checks (scratch copy in the scratchpad): `content_gen.py --check`, `lines_check.py`, and with
   `CADET_CHROME=/opt/pw-browsers/chromium`: `cadet_test.py OLD NEW` (run from a scratch folder; OLD =
   `git show e3ee66b:starship-cadet.html`, the 0.60.0 base), `social_check.py`, `intro_check.py`, `events_check.py`.
   Setup in a fresh container: `pip install playwright`; three.js in `/tmp/cadet-work/three` (DEV_NOTES "Testing").
6. Commit (message ends with the Co-Authored-By line), push, report to the lead (commit, what's in, checks, memory).

## Known state and gotchas

- **cadet_test** since 0.48.7 differs from 0.60.0 in two shots (`b_wander10s`, `i_tap1`), only a chatter bubble's words:
  Deck 4 crew have their own lines, which changes `lineFor`'s recently-said penalty, so a different stock small-talk line
  wins. Proven: the new code with 0.48.6's content is ALL IDENTICAL. If any *other* shot differs, find out why.
- **cadet_test** can time out loading the page once in this container; re-run it alone.
- **social_check**'s gift test picks the first tea-lover (fixed by social A in 0.36.46 to skip guarded people).
- **Rest-day lines:** `weekday:` must match the game ROSTER's `rota.offDays` (0 = Monday); writers have got it a day early. Torres's and Calder's day-off lines deliberately use the *planned* Pillar 4 days.
- Card words (`hi`, `bye`...) carry no end punctuation; lines supply it.
- Day 0 walking lines: `== week1` under `? flag:walk.<step>`; shadow job: `flag:walk.job.<step>` (onboarding maps
  its keys: take, stop.fetch, stop.make, stop.job=panel, done, turnin).
- Rooms with spaces in `place:` use underscores or aliases (mess, commons, lounge, booths, overlook, teacorner,
  worksbay, chartroom, musicroom). `where:` in arcs: calm, visit, appt, any, or a room name (needs the person there off
  duty by their habits, or `duty: true`).
- Cues: `repair.<kind>`, `favour.<lamp|fetch|job>`, `gift.<tag>`, `tradition.<id>`, `event.<id>.<phase>`, `harvest`,
  `lateMeal`; `.you` when you did it; `@me` (about the speaker), `@dept` (in the speaker's department).
- Romance: lines_check bans romance said to the player; couple talk only under `pair:couple` / `bond:couple`, never
  near the player. False alarms: reword, or add the line id to `content/allow.list` (yours to approve).
- `lines_check` reads every capitalised word in `facts.md` as a known name: keep facts.md current.

## Writers (2026-10-17)

| Writer | Session | Branch | State |
| --- | --- | --- | --- |
| writer-works | session_01DbudMKaYgwjL8yDQpe3DFo | claude/writer-works | retired (`plans/handover-writer-works.md`) |
| **Writer 2** (Works + command) | session_01Cf6D2dFZaKspr9mwUnCrBm | claude/writer-works | batch 1 and 1b merged in 0.48.11; on batch 2 (command, Watch, Survey people to ~30 each) |
| writer-command | session_01HdsVyhcPUgWse8qpaYqKex | claude/writer-command | retired (`plans/handover-writer-command.md`) |
| writer-commons | session_01DfadYjSP8skcVF72f6JxBw | claude/writer-commons | handed over (`plans/handover-writer-commons.md`, 9eb51fa), idle: ask the lead to retire it and hire a fresh writer-commons when needed |

Writer 2 is on batch 1 (Works 1-8 and Kovac to ~30, Torres's job-2/job-3 bubbles under `flag:walk.job2.<step>` and
`flag:walk.job3.tea|turnin`, telling onboarding when they're in). Newcomer replies are on hold (they wait for the guide
script's format). `who:` / `with:` speaker conditions are in (dialogue 0.43.8): the newlyweds' and the knitting circle's
overheard can now be written.

## Open work (in rough order)

0. Hire a fresh writer-commons (from `plans/handover-writer-commons.md`). Its suggested next batches: callbacks
   (`mem:`/`told:`), visits and notes, `rep` and `knownFor`, rumour and smalltalk for their people, the story crew toward
   about 120 lines each, the newlyweds' overheard with `who:`, Pell's `mem:moment.pell.timed` callback.

1. Works crew to ~30 own lines each (now ~15); Kovac, command, Watch and Survey crew the same; visitor cards.
2. Torres's job-2 and job-3 bubbles (onboarding's INTRO_JOB_LINES); newcomer reply sets (a `.meet`?).
3. Goodbyes, letters (crew who move on), `about`, `rep`, `knownFor`, `visit`, `note`, `gift` lines.
4. Tone checks for the tradition designers' `.trad` texts when asked.

## Open questions with others

- Theme fill-ins (social A, 0.36.55): `{home}` and `{family}` are live, `{hobby}` for 60 of 74 crew, `{since}` not yet
  (the lead is deciding who adds it): lines with `{since}` are skipped, so keep them as extras.
- Favour jobs: `liftBrakes`, `pellPractice` (sim engineer), `brennanSage` (galley engineer 3), `holt.invite` (social B,
  played in place).
- readyRoomFirst's choices to carry `readyroom.lights|filters|month` (social A asked the traditions engineer via the lead).
