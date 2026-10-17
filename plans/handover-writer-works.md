# Handover: the Works writer (seat 12, Pillar 4)

**Role:** Writer for the Works department and the arrival. Plain text under `content/` only; never the game file,
`content_gen.py`, `lines_check.py` or another writer's files. **Report only to the head writer**
(session_016i7YYgZd6puKxfBSkLggRF) with send_message after each batch, never the lead or the user. The head writer
sets batches (~300 lines), reads them, and is the only one who merges.

**Branch:** `claude/writer-works` (push only there). Started from `claude/ship-integration` 0.60.0; merge
`origin/claude/content` before every batch. Writers have no build numbers; the head writer's builds are 0.48.x.

## What I own and built (all merged into claude/content unless noted)

| Batch | What | Files |
| --- | --- | --- |
| 0 | Voice cards for the 16 non-story Works crew (story cards are the head writer's) | `content/voices/{navarro-mateo,halloran-emeka,reyes-alejandro,silva-bea,teague-theo,rossi-femi,rahman-farah,eklund-leila,moreau-signe,soto-marta,volkov-maeve,quist-ilse,keane-davi,jovanovic-petra,amadi-asha,salo-saad}.voice` |
| 1 | Sampler lines for Torres (14), Calder (14), Kovac (10); Torres's Day 0 walking lines | `content/lines/torres-zeke.lines`, `calder.lines`, `kovac-zainab.lines` |
| 2 | ~15 everyday lines each for the 16 (240); the Works bank (37); Works overheard (12 conversations) | `content/lines/<the 16>.lines`, `content/banks/works.lines`, `content/overheard/works.lines` |
| arcs | Torres beats 1-6, Calder 1-5, Kovac 1-4 | `content/arcs/torres.arc`, `calder.arc`, `kovac.arc` |
| 3 | Torres and Calder to ~60 everyday lines each (invite, accept, decline, missed, hint, birthday, week1 Mon-Sun) | `torres-zeke.lines`, `calder.lines` |
| 4 | Keane's ladder-club lines; `introBriefing` (Mon 07:50) and `introSoloJob` (Tue 07:45); newcomer bank (16) | `keane-davi.lines`, `content/meetings/introBriefing.meet`, `introSoloJob.meet`, `content/banks/newcomer.lines` |
| 5 (last, sent with this note) | Torres's shadow-job talk-through (`flag:walk.job.<step>`: take, fetch, make, panel, done, turnin); Halloran's Friday-mug lines (week1 Thu/Fri, `flag:mug`) | `torres-zeke.lines`, `halloran-emeka.lines` |

Also: `content/facts.md` section **4a** (Works pronouns). Only that subsection is mine.

## Shared formats and gates to keep

- **Walking lines:** each Day 0 step is a block `? flag:walk.<step>` (hello, haulway, works, lift, wing, toMess,
  servery, free, call); the shadow job is `? flag:walk.job.<step>`. Bubbles, 60 characters or fewer. Onboarding's hook
  asks lineFor for them by step; nothing else sets those flags, so they never leak into week-1 chat.
- **Meetings:** cast slots `tech1`/`tech2` fill section 21's `'works:2'`. One choice, no wrong answer.
- **Arcs:** `needs` of each card gets the `+` warmer answer (Torres listen, Calder practical, Kovac listen).
  Flags: `torres.askCalder`, `torres.applied`, `kovac.liftjob` (with `favour:liftBrakes`, a placeholder job id the head
  writer is taking to the lead), `calder.welldone`.

## Canon rules that bit (read facts.md; these are the easy ones to break)

- **Calder never says "well done" before her beat 5.** No exclamation marks from her. Fenn is named only from
  `beat:calder.3`; the Halcyon junior only from `beat:calder.4`.
- **Torres:** nothing about his father before `beat:torres.4`, nor the Engine Specialist list before `beat:torres.2`.
  The scarf joke only after `mem:moment.torres.scarf`. Days off Thu-Fri.
- **Kovac** doesn't admit the lift until beat 2 ("exercise"). **Keane** never says "afraid"; the ladder club is Kovac,
  Cruz (they/them) and Keane.
- **Pronouns:** only those in facts.md section 4; otherwise the name or "they". The player is never gendered; my
  "share" replies give the player no backstory ("someone I love").
- **No romance read** (the lead's rule): every friend- or close-tier line and every moment. I reworded Reyes, Amadi,
  Keane and a Torres accept line for it.
- Gift tags (`loves`/`likes`): only `star music plant garden tea game book sweet card made`. Invites: only
  `quiz observatory film jam running tiles swap gym garden tasting roast works-tea patrol`.
- Card words have no end punctuation (the head writer's rule, in the voice bible).
- **On hold until the lead lifts it:** new `overheard`, `about`, `rumour`, `smalltalk` lines.
- `place:` takes single words / the aliases (mess, worksbay, teacorner, overlook...); I mostly used `act:` and `place:calm`.

## Approved new canon (facts.md section 11, the head writer's)

Reyes's neighbour minds his cat back home; Rossi calls home on Tuesdays; Keane's "cleanest engine room in the whole
Service"; Navarro's spanner owner (unnamed, they); the day-count breakfasts (Silva, Soto, Jovanovic); Amadi's best window
is in the shuttle bay; "Calder is the clock"; Teague's tidy-cloud comic of Calder ("Fair."); Soto's tin is the
everyone-knows joke (Torres can mention it).

## Loose ends (for the next Works writer)

- The 16 Works crew are at ~15 own lines; the brief's target is ~30 (60 for Works crew): invite, accept, decline,
  missed, birthday, callbacks, cues, visit, note, gift, rep are still to write.
- Kovac is at 10 everyday lines; Torres and Calder at ~60 of a 200 target.
- Newcomer reply sets wait for the guide script. Goodbyes and letters for Works crew are later batches.
- `lines/pell` had a 91-character week1 line (writer-commons's file; reported).

## How to test

```
S=<your scratchpad>; cp starship-cadet.html $S/game.html
python3 content_gen.py $S/game.html && python3 lines_check.py $S/game.html
```
Bake into a copy (the real game file is the head writer's to re-bake; against it lines_check reports only "baked blocks
out of date"). It must say PASS. Then commit, push to `claude/writer-works`, and send the head writer the commit,
the files, line counts and any canon questions.

## Open questions

None for the user. For the head writer: the job id behind `favour:liftBrakes`; whether newcomer reply sets should be a
`.meet`.
