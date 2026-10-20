# Talk a while: work pools (plan, decided 2026-10-20)

**TW1, for the user and lead 20; reviewed by TR1 (plans/work-pools-review.md on claude/talk-pack-review) and its fixes
folded in.** The full page with samples and the answer form is `plans/work-pools-plan.html`. The user's ask: a pool
of talks for each type of work, so crew can talk about something a little more personal, **in addition to** the pack
(the 160 talks, the shared pool, own talks, small talk and their rules stay as they are).

## The pools (from the game's roster: 86 crew, 74 aboard from Day 1, 12 arriving later)

| Pool | Who | Crew (Day 1 + later) | Odd cases |
| --- | --- | --- | --- |
| Works | Calder, techs, systems and engine officers, engine techs | 20 + 3 | your own department: talks treat you as a workmate; engine-room talks for the engine crew (6 at a time, 7 over the year) |
| Watch | Holt, Mensah, officers, ratings | 12 + 2 | five on nights |
| Survey | Sato, Mori, officers, assistants | 11 + 3 | |
| Bridge | helm (Raman...) and command (Captain, Vance, Kowalczyk, Zielinski) | 9 + 1 | helm talks `dept:helm`, command talks `dept:command`; command talks stay on plain work at acquaintance/colleague (all four have job-shaped stories) |
| Comms | Ferreira, officers, ratings | 5 + 1 | |
| Infirmary | Nandakumar, Yoon, aides, Oduya | 6 + 1 | Oduya (Counsellor) skips wound/bone talks; a few listening talks suit him, kept clear of grief |
| Galley | Brennan, hands, bartenders | 6 + 1 | bar talks for Madsen (and Haddad until day 203); bartenders skip dinner-rush talks |
| Garden | Cruz, O'Neill, Hart | 3 | |
| Store | Esposito, Ishikawa | 2 | could merge with Garden |

Guests and the roster's `civilian` group (empty today) have no work pool. Later arrivals draw their pool from day one;
leavers stop. Four arrivals are new cadets (days 35, 77, 161, 203): talks with a past in the job skip them.

## More personal, by tier (no stranger-tier work talks)

- **Acquaintance (~3 in 10):** the job up close: a day, a favourite corner, a small gripe, what it leaves on you.
- **Colleague (~4 in 10):** why they chose it, who taught them, the part nobody sees, a skill they're proud of.
- **Friend (~3 in 10):** what the job means to them, who they do it for, a proud moment, a habit it gave them, what
  they'd teach you. **Not** mistakes that haunt them, doubts, leaving or "can't say no": those are the crew's struggle
  themes (42 of 86 crew have one or an arc), so the pools stay off them.

Each keeps the question (their ask, your listen/share/cheer reply, their answer). Talks skip people whose story they'd
tell early (Torres's list, Pell's practical, Rina's and Tomas's exams, Brennan's offer, Calder's first chief).

## Picking order (recommended, after TR1)

own talks → **work and shared taking turns** (per person, preferring whichever wasn't had lately) → small talk. Own →
all work → shared would make Works crewmates talk only shop for weeks. Work talks start at acquaintance; one not ready
yet waits. Once per save (the user chose it for the shared pool on 20 October; question 2 asks whether work follows).
Run-out: roughly two months across the ship instead of one; sooner with your own department.

## Size and time (sized by who can tell them)

Works 36, Watch 20, Survey 20, Bridge 10 (6 helm, 4 command), Infirmary 8, Galley 8, Comms 8, Garden 6, Store 4:
**120 talks, 1,080 lines.** Two writer seats in parallel, about one session each, then TR1's review and fixes.

## For the engineer (TE1, told on 2026-10-20)

- Reader change: accept `@talks work:<pool>` (pool from the nine), files `content/talkpack/work-<pool>.talk`, topic
  always `work` (no `topic:` line), baked to `TALKS.work = { works: [...], ... }`.
- Ids `work.<pool>.<slug>`, hand-written and frozen, unique across pool, own and work; same fired record.
- One data table `TALK_WORK_POOLS` (helm and command → bridge; the rest to themselves; guests and civilians none),
  read at talk time.
- TE1's picker already takes an ordered source list; taking turns needs one small alternate-per-person rule.
- No new condition words: `dept:` splits helm from command; engine crew, bartenders and the Counsellor are `who:` lists.
  (`role:` was proposed and dropped.)

## Decided (the user, 2026-10-20): every recommendation, no comments

1. Order: own talks, then work and shared taking turns (preferring the one not had lately), then small talk.
2. Work talks follow the once-per-save rule.
3. The nine pools as listed.
4. About 120 talks (sizes above).
5. Friend tier: what the job means, who they do it for, a proud moment, a habit it gave them, ending warm.
6. Works talks treat you as a workmate.
