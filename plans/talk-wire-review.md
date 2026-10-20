# Review of the Talk a while wiring (TR1)

**Reviewer:** TR1, standing in as owner of sections 20 and 22, for TE1 and lead 20. **Reviewed:** `claude/talk-wire`
at f053df0 (from integration 5dd740c + `claude/talk-pack`): cc04ef8 (T1 reader), 37fd3f8 + aeef392 (T2 picker,
`TALK_SOURCES`, `save.talks`, `talk_check.py`), 853dbec (section 20's hook), f053df0 (T3, `TALK_PACK_ON`, the phone
part of talk_check).

## Verdict: PASS WITH FIXES

One should-fix before the switch stays on for players (the "we've talked about everything" line can come too early),
and a few small notes. Everything the user's rules ask for holds, and every check passes.

## The plain summary

The wiring is careful and small. Section 20 gained four one-line hooks, each guarded so nothing changes without
section 22; section 22 holds the picker, the save and the card's words. With the switch off, the game is the same as
integration's, pixel for pixel and in what the crew say. With it on, a talk is chosen in the user's order (their own
talks, then the shared pool, then small talk), is used up the moment it starts, keeps its question and three reply
buttons, and is saved and loaded correctly. Every one of the pack's lines appears exactly as written in the `.talk`
files, and fits a 390-wide phone.

The one thing to fix: when someone has nothing *ready today* (say, a stranger once the few any-tier pool talks are
used), the picker falls to small talk and one time in four opens with "We've talked about everything, haven't we?",
though dozens of their talks are still waiting for a closer friendship. That line should only come when nothing at all
is left for them.

## What I ran (all on f053df0)

| Check | Result |
| --- | --- |
| `talk_check.py` (with `--shots`) | TALK CHECK OK: (a) 100 pool + 15×4 own + small baked; (b, c) 148 fired over 40 days, no repeats, run-out order held, Saruth never draws the pool; (d) tier, `!who:`, `!thread:`, `rank:` broken 0 at every tier, arc-gated own talks closed on a fresh save; (e) lately-had topics go behind; (f) save round trip, junk dropped, New game clears; (g) phone card flow |
| `social_check.py` | SOCIAL CHECK OK |
| `cadet_test.py` integration vs f053df0 (switch **on**) | ALL IDENTICAL |
| `cadet_test.py` integration vs f053df0 with `TALK_PACK_ON = false` | ALL IDENTICAL (apart from renderer noise: some pixels 1 level off) |
| `social_check.py` on the switch-off copy vs on integration | identical output, line for line (Talk a while uses the old `talk.<topic>` lines exactly as before) |
| `bash check_fast.sh` | QUICK CHECK OK in 413 s |
| `content_gen.py --check`, `lines_check.py` | up to date (160 talks); PASS, 0 errors, 6 warnings (none new that matter: "Prevention" read as a name) |
| Baked `TALKS` against the `.talk` files (my script) | 160 talks, every them/ask/reply/answer identical, none lost or doubled; small talk 36 lines = 36 in the file |
| Every line on the chat card at 390 × 844 (my script) | 1,440 card views (each them line and ask; the ask with its three buttons; each answer; every small-talk line): 0 off screen, 0 clipped buttons, tallest card 378 px. The longest greeting + opener (139 characters) fits too (card bottom 830 of 844) |

## Against the user's rules and the plan

- **No repeats:** `talkPackStart` fires the talk before the card shows it (`talkPackFire` → `save.talks.fired[id] =
  [day, crewId]`), so walking off or "got to go" still uses it up. A pool talk fired with one person is gone for all.
  Checked by (b) and by playing Tomas twice in (g). ✓
- **Run-out order own → pool → small talk:** `TALK_SOURCES` in that order; own in file order (the first whose `when:`
  holds), pool seeded by day and speaker with a lately-had topic last; guests never draw the pool. ✓ The list shape
  takes TW1's planned work pools as one more entry. ✓
- **Conditions honoured:** `linesOk` with the talk's own `t`; the new `thread:` reads the voice card's thread, else
  the roster's. A talk with a placeholder that can't be filled waits (checked: `{trad}` skips honoree days and rec-deck
  traditions while `REC_DECK` is off). ✓
- **The question with three replies:** the pack's ask at `TALK_ASK` (7 min), its three reply texts as the buttons, the
  chosen answer, and the +2 for the reply that suits them as before. More lines come every 2 minutes, so all of a
  talk's (at most 2) more lines are said before the question. Small talk has no question and no buttons but Stop. ✓
- **Save shape:** `save.talks = { fired: { id: [day, crewId] }, small: { crewId: [day, done] } }`, written only once
  something has happened (so a save from a game that never talked is unchanged), read back through `talksClean`, about
  7.4 KB with everything fired. ✓
- **Nothing changes with the switch off:** see the table. ✓
- **Section 20 (as owner):** the four hooks are one line each and `typeof`-guarded; `const open = pk || (C.talk.topic
  && ...)` and `memAdd` keep the old behaviour when `pk` is null. Fine to merge. ✓
- **Section 22 (as owner):** new code is inside the dialogue engineer's slot; `lineQ` gained `voiceOf`; `linesNew`
  clears `SHIP.talks`. No build-number lines touched. ✓

## Should fix

**W1. "We've talked about everything" comes while talks are still waiting.** `talkPackPick` falls to small talk when
nothing is *ready* today, then `done = dones.length > 0 && schedU(...) < TALK_DONE_ODDS && ...`. My check: Rosa Abara
as a stranger, with the 28 any-tier pool talks used up and 72 tier-gated pool talks unfired, had small talk on 58 of
58 days, and 12 of them opened with a "done" line. The plan's rule is "when both are used up". Fix: only allow `done`
when no source has an unfired talk for them at all, whatever its `when:`:
```js
const left = TALK_SOURCES.some(s => s.talks(p).some(tk => !T.fired[tk.id]));
const done = !left && dones.length > 0 && schedU(seed, d, 757) < TALK_DONE_ODDS && !(last && last[1] && last[0] < d);
```
(Then talk_check (c) should also check "no done line while a talk remains".)

## Nits

- **W2.** Four pool talks use `{friend}` (`pool.crew.friend-funny`, `get-on`, `friend-help`, `pool.hobby.teach-me`) and
  can't be said by anyone until the sim has formed bonds. That's by design (they wait), but talk_check (b) fired 94 of
  100 pool talks: print the ones that never fired and why, so a talk that can never come is visible.
- **W3.** The "done" share came out at 20% in (c), against `TALK_DONE_ODDS` 25%; that's the never-twice-running rule
  at work. Fine; maybe say so in the plan.
- **W4.** The screenshots named in f053df0's message (`plans/talk-wire-shots/`) aren't in the commit: `*.png` is in
  `.gitignore`. Send them with the hand-over, or say they're made by `talk_check.py --shots DIR`. (I made them; they
  look right: the question with three wrapped buttons, the answer, small talk with Stop.)
- **W5.** The switch is committed **on** (`TALK_PACK_ON = true`). CLAUDE.md: "new features stay switched off (identical
  game) until they're switched on". cadet_test is identical either way, but the lead should confirm it was switched on
  by decision (the lead's brief), not by default, and the build table row should say so.
- **W6.** After a pack talk's more lines, the old `talk.filler` lines fill the gap to the question and to the end
  (Tomas at 4 and 6 minutes: "I like a chat. People don't stop enough."). That's the plan's design ("then filler"), and
  the duplicate guard stops a filler line repeating a pack line. Fine; noted so nobody reads it as a bug.

## The old `talk.<topic>` lines: park them now?

**Yes, as a marking only, now; no deletion and no renaming.** They are unused while `TALK_PACK_ON` is true, but they are
still the switch-off path (and the fallback if the pack ever has nothing for someone), so the keys must stay and stay
working. TW1 should, in one small commit:
1. put a comment above the topic sections in `content/banks/talk.lines`: `// PARKED 2026-10-20 (cut while the Talk a
   while pack is on, TALK_PACK_ON): kept as the switch-off fallback; never reuse these keys`;
2. record it as cut in `design-doc.md` "Talking" (date, the user's reason: the pack replaces the topic lines) and in
   `plans/talk-pack-plan.md`.

Taking them out of the file is its own reviewed step later, once the switch itself is retired (CLAUDE.md, "Cut things
are parked, never deleted").
