# Handover: head writer (Pillar 4, seat 11)

**Head writer 3** (session_01FopKMT2ZKxuWcNDcmF7565) holds the seat from 0.48.22 (2026-10-17 ~05:10). Built so far:
0.48.22 Zeke's arrival tour (`walk.<point>.<n>` at shuttle, bay, haulway, stores, works, lift, wing, officers, deck3,
servery; `walk.call.<n>`; linger `walk.more.<n>`; meetings `introDinner`, `introAsk`; onboarding's keys, arrival 0.42.20+);
0.48.23 Writer 2 b6 + Writer 4 b1-2 (booth calls: generic ones carry `!who:torres-zeke|vance|calder|marrow|holt`);
0.48.24 Writer 2 b7 + Writer 4 b3 (juniors); 0.48.25 Writer 2 b8 (16 of 31 visitors; Writer 2 RETIRED) + Writer 4 b4
(`banks/tiles.lines`, kinds `tiles.*`; 30 Deck 3 pairs). Next build 0.48.26. Writer 4 (session_01AB5f3VLMh8huiLWbEnqa8U,
claude/writer-commons) is on batch 5: the other 15 visitors. DE2: one-sided booth convos play for one person (0.43.13; they need place: or act:);
`tiles.*` kinds need no wiring; `trait:dry_humour` / `you:night_owl` coming in their next build. 0.48.26-31: all 31 visitors voiced,
Zeke's ordinary weeks, goodbyes/letters (Commons 19, Works 16, Watch 9), dinner convos, repair reactions (Writer 4).
0.48.32-35: last goodbyes; everyday passes for Holt, Vance, Marrow, Kovac, Calder, Brennan (Writer 4, RETIRED). Writer 5
(session_01HW7UxnuNvRXoEjn8tK4sQq, claude/writer-commons) now: Tomas, Pell, Rina passes, then story-crew goodbyes. Next build 0.48.36.
**Lead's ruling (07:32):** never merge claude/dialogue into claude/content (it carries the 0.60.1 engine base; real code
conflicts). Keep claude/content on its base, merge writers' content/ only; build master 2 takes content/ from here. For newer
tools copy only lines_check.py / content_gen.py / content/README.md from claude/dialogue (lines_check.py + README at dialogue 0.43.22: checks trad:/came: ids too).
DON'T copy content_gen.py past 0.43.19: from 0.43.20 it bakes VOICE etc. as JSON.parse (the performance pass), which
rewrites the game file; that belongs with the engine merge at build master 2, not here.
My recurring edits: callbacks mustn't assume when a beat happened; nothing that pre-empts a beat; no poems or
"thinking about you" to the player; Day 0 callbacks must match introChief/introDinner as written. A meeting choice takes ONE reply line (a second indented
line overwrites the first). The notes below are head writer 2's, still accurate unless the lines above say otherwise.

**Head writer 2** (session_01HNrh3xCtczeZM5NVFrE6pa) held the seat 0.48.11-0.48.21 and handed over at ~70% memory
(2026-10-17 ~05:05). A fresh head writer reads this note first, then CLAUDE.md, content/voice-bible.md, content/facts.md,
content/README.md, content/briefs.md, TEAM.md. **First job: Zeke's arrival tour** (In flight, below).

**Role:** head writer for Starship Cadet's Pillar 4. Report ONLY to the lead (now session_01KPJMYjXAPkNUcrQ8VRkhLE, from ~04:35; was session_01PJtmxWgAPLebXSZKP6ZRpG) with
`send_message`; never contact the user. Writers report to you; you are the only one who merges their work. Reviewer 2
(session_0142TQw4ke8caPSyAC93VT98) reviews you. Tradition designers may ask you for a tone check.

**Branch:** `claude/content` (push only there). Builds **0.48.x** (header line ~198 and `GAME_BUILD` ~7047 in
`starship-cadet.html`; keep both in step; a row in DEV_NOTES's build table for each). Last build: **0.48.21** (Head writer 2)
4,060 lines (story crew 106-141 own lines each), 4 home contacts (Mum, Gran, Jo, Sam; facts 4d), 128 conversations, 5 meetings (bridgeInvite added), 83 voice cards (all 74 crew, Saruth, 8 event guests), 10 templates, 87 overheard conversations, 45 arc moments,
12 struggle themes, 4 intro meetings. Next build number: 0.48.22.

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

- **Checking cadet_test's bubble shots:** crop the two shots and threshold the difference above 2 levels; the boxes must
  be only the bubble (i_tap1 ~(18,385)-(208,421), b_wander10s ~(290,553)-(518,612) at 0.48.21). A small python+PIL
  snippet does it (`ImageChops.difference(...).convert('L').point(lambda v:255 if v>2 else 0).getbbox()`).
- **My review scripts** (rest-day `weekday:` vs ROSTER offDays; a diff-to-'kind | cond | text' lister) lived in my
  scratchpad; they're a few lines each: rebuild them from the descriptions here.

- **cadet_test** since 0.48.7 differs from 0.60.0 in two shots (`b_wander10s`, `i_tap1`), only a chatter bubble's words:
  Deck 4 crew have their own lines, which changes `lineFor`'s recently-said penalty, so a different stock small-talk line
  wins. Proven: the new code with 0.48.6's content is ALL IDENTICAL. If any *other* shot differs, find out why. Since
  0.48.15 the pixel counts are different (about 9,900 and 1,800): more smalltalk means a different bubble wins (checked by
  cropping: only the bubble's words differ). The counts move whenever bubbles are added; check the crop, not the number.
- **cadet_test** can time out loading the page once in this container; re-run it alone.
- **social_check**'s gift test picks the first tea-lover (fixed by social A in 0.36.46 to skip guarded people).
- **Rest-day lines:** `weekday:` must match the game ROSTER's `rota.offDays` (0 = Monday); writers have got it a day early. Torres's and Calder's day-off lines deliberately use the *planned* Pillar 4 days.
- **No-romance read, recurring catches:** "thinking about you", "likes you", "just us", a place for two in hints, anyone in
  or on your bed, night "with me", "kept looking at the door", romantic idioms ("hung the stars"), pet-name-like words.
- **Notes are never signed** (the game appends the name).
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

## Writers (2026-10-17, ~05:00)

| Writer | Session | Branch | State |
| --- | --- | --- | --- |
| **Writer 2** (Works + command, Watch, Survey) | session_01Cf6D2dFZaKspr9mwUnCrBm | claude/writer-works | batches 1-5 merged (to 0.48.20): everyone in their area ~30+, Calder 116, Kovac 106, Vance 110, Marrow 108, Holt 109. On batch 6: everyday smalltalk/rumour for their ~45 people (at most 1 in 5 about work); then 7: Works/Watch/Survey overheard pairs with who:/with: and place:; visitor cards last. ~half memory at 0.48.20 |
| **Writer 3** (Commons) | session_01AS3Tzju3TuFbM9XAEYdvPX | claude/writer-commons | batches 1-9 merged (to 0.48.19): story four ~135, their 19 at ~40+ with bubbles, callbacks, rep/you greets, gift thanks; gran/jo/sam.call; crew asking after your people. batch 10 merged (0.48.21: banks/everyday.lines); RETIRED (`plans/handover-writer-commons.md` current). For a fresh writer-commons send the lead a two-line brief (booth overheard once DE2 sets the format; more everyday chatter) |
| writer-works, writer-command, writer-commons (first) | | | retired; handover notes in `plans/` |

## Open work (in rough order)

1. **Zeke's arrival tour** (the user's priority; see In flight).
2. Everyday chatter variety (Writer 2 batch 6, Writer 3 batch 10), then overheard pairs with `place:`.
3. Visitor cards (guests), newcomer reply sets (wait for the guide script's format), goodbyes and letters (crew who
   move on), the one-sided booth overheard (DE2's format).
4. Torres's own lines are at 111 but are mostly walk/week-1; his everyday banks could use the same pass as Calder's.
5. Tone checks for the tradition designers' `.trad` texts when asked.

## In flight (Head writer 2)

- **PRIORITY (the user, via the lead): Zeke Torres's arrival tour.** Much more to say, shuttle to mess. Proposal sent to the
  onboarding engineer (session_01KaHzfqSqF8B4bkNFrH1tsx): ordered sequences per walk step, sub-steps (shuttle, bay,
  haulway, works, lift, wing, bunk, Deck 3, servery, a new `introDinner` table meeting before Calder, free), linger
  lines (`flag:walk.<step>.more`), a tap-to-ask `introAsk` meeting. Waiting on their hook names; then the head writer writes it.
- **Chatter variety (the user):** keep everyday bubbles mostly life/food/home/hobbies/weekend; work under a third.
- **Overheard tied to a room needs `place:`/`deck:`** (DE2's note, fixed in 0.48.19).

- **Call home:** APPROVED (fixed cast Mum, Gran, Jo, Sam; home unnamed; live calls any day, once per person per day;
  Letters evening = the clear-line window where `via: live` beats land). Model: `content/home/mum.call`, baked since 0.48.16
  (dialogue 0.43.11: README "Calls home (.call)"; send conditions came:any, friend:any, flag:intro.soloJob). All four .call files are
  written and baked (facts 4d has the cast). The calls themselves wait on social B's successor (B8) and the booth hook.
- **Bridge invite:** plays from traditions engineer 2's 0.34.35 (session_01WEEoe5DyRegEqVMZgKRHWB; day 22 breakfast, Mail if missed). They keep a copy of the file: tell them if you change it.
- **Holt beat 1** has `where: meal` (social B's 0.39.6 word; plays once their engine is in the integration build).
- Dialogue engineer 2: session_01S26bs4oMahyGJkuVaCKQGT (claude/dialogue, took over from DE1). Asked: `you:` with `_`,
  knownFor tag list, the stricter .call romance check, the one-sided booth overheard format (for a later batch).

## Open questions with others

- Theme fill-ins (social A, 0.36.55): `{home}` and `{family}` are live, `{hobby}` for 60 of 74 crew, `{since}` not yet
  (the lead is deciding who adds it): lines with `{since}` are skipped, so keep them as extras.
- Favour jobs: `liftBrakes`, `pellPractice` (sim engineer), `brennanSage` (galley engineer 3), `holt.invite` (social B,
  played in place).
- readyRoomFirst's choices to carry `readyroom.lights|filters|month` (social A asked the traditions engineer via the lead).
