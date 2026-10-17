# Handover: head writer (Pillar 4, seat 11)

**Role:** head writer for Starship Cadet's Pillar 4. Report ONLY to the lead (session_01PJtmxWgAPLebXSZKP6ZRpG) with
`send_message`; never contact the user. Writers report to you; you are the only one who merges their work. Reviewer 2
(session_0142TQw4ke8caPSyAC93VT98) reviews you. Tradition designers may ask you for a tone check.

**Branch:** `claude/content` (push only there). Builds **0.48.x** (header line ~198 and `GAME_BUILD` ~7047 in
`starship-cadet.html`; keep both in step; a row in DEV_NOTES's build table for each). Last build: see the top of the
0.48.x rows in DEV_NOTES.

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
| **Writer 2** (Works + command) | session_01Cf6D2dFZaKspr9mwUnCrBm | claude/writer-works | new (2026-10-17 ~03:58); briefed with the batch order in "Open work" below |
| writer-command | session_01HdsVyhcPUgWse8qpaYqKex | claude/writer-command | retired (`plans/handover-writer-command.md`) |
| writer-commons | session_01DfadYjSP8skcVF72f6JxBw | claude/writer-commons | working (about 50%): their 19 crew toward 30 own lines (bunkmates toward 60) |

Asked of the dialogue engineer: a `who:` speaker condition for overheard (the newlyweds, the knitting circle).

## Open work (in rough order)

1. Works crew to ~30 own lines each (now ~15); Kovac, command, Watch and Survey crew the same; visitor cards.
2. Torres's job-2 and job-3 bubbles (onboarding's INTRO_JOB_LINES); newcomer reply sets (a `.meet`?).
3. Goodbyes, letters (crew who move on), `about`, `rep`, `knownFor`, `visit`, `note`, `gift` lines.
4. Tone checks for the tradition designers' `.trad` texts when asked.

## Open questions with others

- Roster fields `{home}`, `{family}`, `{hobby}`, `{since}` (who owns them now the crew designer has retired?). Theme
  beats needing them don't play until they exist.
- Social A is wiring `{home}`, `{family}`, `{hobby}`, `{since}` (the lead asked, 2026-10-17).
- Favour jobs: `liftBrakes`, `pellPractice` (sim engineer), `brennanSage` (galley engineer 3), `holt.invite` (social B,
  played in place).
- readyRoomFirst's choices to carry `readyroom.lights|filters|month` (social A asked the traditions engineer via the lead).
