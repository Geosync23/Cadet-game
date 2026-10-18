# Handover: head writer, seat W (0.60.7, Pillar 5 Steps 1-2, playtest 1)

**Session:** session_013DdpJv4AKFJcvuBBqjSXms (stood down on call at ~65% memory, 2026-10-18 ~17:55 UTC).
**Lead:** lead 13, session_015UkCGSS9FyGoBdkePhrKbC (leads changed often: 10 → 11 → 12 → 13; check TEAM.md / the latest brief).
**Branches:** `claude/writer-0607` (0.60.7 content, done, final 0cc4cdf), `claude/writer-p5` (Pillar 5 + playtest 1, final
6a00d9c). Text only: content/, DEV_NOTES rows, lines_check.py, facts.md. **Writers never bake**; the build master runs
content_gen.py in the combine. Build series 0.48.x: last used **0.48.91**; next is 0.48.92.

Read first: CLAUDE.md, the current brief on claude/lead-pillar1 (plans/brief-*.md), content/README.md (the format),
content/voice-bible.md, content/facts.md, and the key lists below. The older head writers' note is
plans/handover-head-writer.md on claude/content (still accurate on tone, the no-romance read and gotchas).

## What I built (all reviewed PASS)

- **0.60.7** (`content/keys-0607.md`): talk.lines (Say hello / Talk a while, 10 topics), hobby, needs pop-ups
  (`need.low.<need>`), clock screen, bar (Ivo Madsen, Tamsin Haddad), clothes and laundry, stores, crew at work,
  calendar, quiz (`quiz.q<n>.text/.a1-a4`, a1 always right; Tomas's `quiz.right/wrong/done`), gardening hobby,
  12 traditions' words (content/trad-words/*.words: pasted by the traditions engineer into their .trad files),
  Zeke the Day 1 trainer (`walk.train.<job>.<step>`, `walk.follow.1-29`), Running club → Gym club everywhere.
- **Pillar 5 Steps 1-2** (`content/works/keys-p5.md`): training meetings `train.<id>.<teacherId>` (m1 m4 m3d m3i m5 m6 m2
  m7 p3; Day 5's teacher is Emeka Halloran, Torres and Calder versions kept; train.m5.brennan fallback), teachers' step
  words (kind `work`, `flag:train.<id>.lead|follow.<step>`; the panel step is `hold`), content/works/*.lines (Works app,
  Record, What's next, Tier 1 fault words `fault.name/shows/sign/still/tried.<kind>.<cause>`, cases, scanner, Step 2
  texts, round signs, inspection remarks, remarks), incident reactions.
- **Playtest 1 / 0.63.2** (keys-p5.md "Playtest 1"): 09:00 shift (briefing ten to nine; Day 2 office quarter to nine;
  leave until 08:30), 13:00 tea and biscuits (was half ten), breakfast **06:00-09:00**, in every line and facts.md.
  Zeke (O4/O5's keys): plain greeting "Works Department", `walk.train.open.1-3`, `walk.train.better.1`,
  `walk.cabin.wardrobe.1-2`, `walk.eve.choose.1-2`, `walk.tea.explain/go/at/back`, `mail.zeke.cabin`, introBunk
  reworded (middle top bunk, wardrobe, device, "open my Mail"), no "locker". `tip.clothes`, `tip.callhome` (+.button,
  .goal). Crew walk-up kind **`seek`** (seat X). Tap-to-join `join.<id>.tip/.notice` (+.done/.left for the two walks)
  for 21 traditions, `join.name-on-the-beam.*`, crew `beam.congrats`. Zeke's `trad.beam.1-4` restored (I cut them by
  mistake in 0.48.82).

## Gotchas

- **Agree key names with the seat that wires them, and adopt theirs** when messages cross (it happened four times).
  Keep a key list file current (keys-0607.md, works/keys-p5.md) and say renames in DEV_NOTES.
- **Check what a rewrite cuts:** a Python slice "from marker to end" dropped Zeke's beam lines in 0.48.82. Diff the
  removed lines (`git show <hash> -- file | grep '^-'`) after any block replacement.
- **Times:** the shift is 09:00-17:00 now; never write "half ten" or "eight" for work; breakfast 06:00-09:00.
- lines_check: placeholders added for 0.60.7/P5 (`{time} {hours} {n} {max} {part} {shelf} {drink} {answer} {mech}
  {job} {tools} {skill} {title} {rank} {band} {next} {shows} {drill} {host}`); tip.* and join.* up to 200, mail.* 400,
  works.ask / inspect.mail 140. The only expected lines_check error on a writer branch is "baked blocks out of date".
- Bubbles 60 characters; X's `seek` 70; card lines 90. Training meetings may have a second speaker (C confirmed it
  never holds a training; the career_check hold was its scripted player, fixed in C's 56d15b4).
- Mails are unsigned (the game adds the sender).

## How to test

`python3 lines_check.py` (expect only the baked-blocks error); a scratch bake: copy starship-cadet.html to the
scratchpad, `python3 content_gen.py <copy>` then `--check`. Send each hash to the build master and reviewer directly;
the lead only when a package is done or blocked.

## Loose ends

- `beam.cheer` (crew lines for a later Works hand's beam) is unused: T has no crew-line spot for it yet.
- `works.tool.<id>.about` written but not yet read by C.
- Step 2 seats M1/M2 never confirmed their keys (the lines follow keys-p5.md "Step 2"); check on their branches.
- Two code strings with "ten to eight" were O4's (fixed by O4); X owns the code-side breakfast texts.
