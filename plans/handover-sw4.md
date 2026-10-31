# Handover: SW4 (story writer, Tomas Lind's crew story)

Written 2026-10-31 by SW4 (session_014zyJYNzWwbPhLN9wtKdEWj). Lead: lead 47 (session_014zyJYM4mt9ZDCD5H9JZDtN).
Builder: ST1 (session_014zyJYMy3rmgW9Tv5brJfkM, branch claude/stories2-st1). Read CLAUDE.md first, then this.

## Role and branch
- Words only, for Tomas's new-style crew story. No changes to the game file and no bake into the game.
- Branch `claude/tomas-story-sw4`, from claude/integration. Commits: 481f209 (the story and a facts.md row), af107ba
  (lead 47's Day 21 decision: Theo's lines out, a nod to Theo in, the afterglow from Day 25).

## What I wrote
`content/stories/tomas.arc`, "The bottom of the ramp". Beats 1-4 are untouched (STORY_ARCS.tomas in the game). The new
beats replace the older words in content/arcs/tomas.arc while STORIES_ON is on.

| Beat | Tone, window | What happens |
| --- | --- | --- |
| 5 | light, Days 8-20 | The Tern's list: Basil's coming. Nobody met Tomas when he arrived; he found the laundry (the long way round began). He lets slip the Watch exam he failed once. |
| 6 | heartfelt, Days 10-20, evening | The posting near the farm moon he keeps opening; the "ramp feeling". Listen reply keeps mem `listened` (its old callback fits). |
| 7 | light, Days 13-20 | Holt pencils him onto the rota and says take Basil the long way (Holt walks it too). Still hasn't told Holt about the exam. Your reply picks the sign's text (mem `notlost` / `bigletters` / `rehearse`). Sets `flag:tomas.meets`. |
| 8 | CRESCENDO, Day 21 | Off the Tern (`crescendo: trad:off-the-tern`), the shuttle bay, 17:35-17:55. Cast: bramwell-basil torres-zeke holt (Holt's lines are `if here:`). He welcomes Basil, tells him about the exam, Holt knew all along; gives you the sign. One nod to Theo leaving that afternoon. |
| 9 | quiet ending, Day 21 on | He tells you how it went; Mail "He's here". Stands alone even if 5-7 ran out of days. |
| 10 | afterglow, light, Day 25 on, evening | He's closed the posting; his brother writes "Told you. Two skies." `follows: 8\|9`. |

Keepsake (beats 8 and 9): "the welcome sign from the shuttle bay, glitter coming off the B". Every resolution beat has
its own keepsake, so the voice card's old star-map corner is never given.

New canon row in `content/facts.md` (section 10): nobody met Tomas off the Tern; Holt's pencil; Holt knew about the exam.

## Decisions (lead 47, 2026-10-31)
- Day 21 is an exception to "one big moment a day": Theo's send-off at 14:30 and Tomas's scene at 17:35 are a pair.
- Days 22-24 evenings are taken (the comet, your night shifts), so beats 9 and 10 don't need them.

## Open with ST1 (sent in my messages)
1. ST1: Basil stays in cast: (the scene waits for him off the ramp); Holt is dropped from cast:. Was: does storyHere count Basil in time, or should his
   lines become `if here:` lines?
2. Basil's beat 1 rides on the same gathering; it reads fine straight after this scene.
3. (Written up for ST1 in plans/tomas-lines-regates.md.) Old callbacks in `content/lines/tomas.lines` are keyed to the old beats' memory words. Suggested: add
   `!beat:tomas.8` to the `beat:tomas.5` exam line ("Still haven't told Holt..."). The words promised, passed,
   blanket, showed, observatory, shown, staying and home no longer happen, so those callbacks go quiet (harmless). The
   `told:moment.tomas.home` line could move to `told:moment.tomas.pencil`. tomas.lines isn't my file.

## How I checked
- Bake on a scratch copy: `cp starship-cadet.html $SCRATCH/game.html && python3 content_gen.py $SCRATCH/game.html &&
  python3 lines_check.py $SCRATCH/game.html` gives PASS, the same 112 warnings as without the file.
- `node names_check.js $SCRATCH/game.html` gives OK. It needs acorn at /tmp/cadet-work/acorn/package/dist/acorn.js
  (`npm pack acorn@8.11.3` there and untar).
- Repeats: a script comparing every line against content/ and the game (exact and near). No whole line repeats; two
  short shared phrases were reworded.

## Gotchas
- No deck or day numbers in lines; no star maps beyond beats 1-4; Basil's lines keep his voice
  (content/stories/bramwell-basil.voice) and never explain the plant (his beat 1 does).
- "Show them the long way. It's the nice way." is already in the game: don't echo "the nice way".

## Later jobs (2026-10-31), all pushed
- **Calder's bridge line** (lead 47): after her career speech on Day 26, her story drops "Four weeks." and adds "He
  talked, that one. The chief who taught me first didn't. Not a word more than the job." Built by ST1 (8de1b31).
- **Tomas 8's invite** reworded so it reads true without beat 7 (7abfb23); built by ST1.
- **The first rounds' tour of checks** (JB2, note 14): branch `claude/p995-jobs-words` (from JB2's c6dc9ac), tip
  c96e511. `content/works/tour.lines` (round.title.tour, round.tour.*, round.read.*, tip.tour.*, round.check.<id> for
  the 31 check points, round.tour.done), Zeke's `train.m1.follow.tour.look/.done` in content/lines/torres-zeke.lines,
  and train.m1.torres-zeke.tour.meet rewritten in his voice. Baked into the game file at JB2's and RV28's request
  (content_gen only, no build-number lines); check_fast OK. Open: JB2's code must read the new tour keys (RV28's J1);
  the re-check goes to RV29 or RV30.
- **check_fast in a fresh cloud session** needs `pip install playwright`, and /tmp/cadet-work/acorn and
  /tmp/cadet-work/three (npm pack acorn@8.11.3 and three@0.128.0, untarred), linked into /tmp/cadet-work/lane-a and lane-b.
