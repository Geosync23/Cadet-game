# Talk a while: work pools (plan, for review)

**TW1, for the user and lead 20.** The full page with samples and the answer form is `plans/work-pools-plan.html`.
The user's ask: a pool of talks for each type of work, so crew can talk about something a little more personal,
**in addition to** the pack (the 160 talks, the shared pool, own talks, small talk and their rules stay as they are).

## The pools (from the game's roster: 86 crew, 74 aboard from Day 1, 12 arriving later)

| Pool | Who | Crew (Day 1 + later) | Odd cases |
| --- | --- | --- | --- |
| Works | Calder, techs, systems and engine officers, engine techs | 20 + 3 | your own department: talks treat you as a workmate; engine-room talks for the 7 engine crew |
| Watch | Holt, Mensah, officers, ratings | 12 + 2 | half on nights |
| Survey | Sato, Mori, officers, assistants | 11 + 3 | |
| Bridge | helm (Raman...) and command (Captain, Vance, Kowalczyk, Zielinski) | 9 + 1 | Captain and Vance only draw talks marked for command |
| Comms | Ferreira, officers, ratings | 5 + 1 | |
| Infirmary | Nandakumar, Yoon, aides, Oduya | 6 + 1 | Oduya (Counsellor) skips wound/bone talks; a few listening talks suit him |
| Galley | Brennan, hands, bartenders | 6 + 1 | bar talks for Madsen and Haddad |
| Garden | Cruz, O'Neill, Hart | 3 | |
| Store | Esposito, Ishikawa | 2 | could merge with Garden |

Guests have no work pool. Crew who arrive later draw their pool from their first day; crew who leave stop.

## More personal, by tier (no stranger-tier work talks)

- **Acquaintance (~3 in 10):** the job up close: a day, a favourite corner, a small gripe, what it leaves on you.
- **Colleague (~4 in 10):** why they chose it, who taught them, the part nobody sees, what they'd change.
- **Friend (~3 in 10):** a mistake that stuck, how it follows them home, doubts, what's next, would they choose it again.

Each keeps the question (their ask, your listen/share/cheer reply, their answer). Cozy; nobody is bad at their job;
serious lines rare and behind friendship. Talks skip people whose story they'd tell early (Torres's list, Pell's
practical, Rina's and Tomas's exams, Brennan's offer, Calder's "well done") and people whose struggle theme is about work.

## Picking order (recommended)

own talks → **work pool** → shared pool → small talk. Work talks start at acquaintance, so strangers get the shared
pool first. Once per save, like the shared pool. The run-out comes about twice as late (roughly two months for a keen
player instead of one).

## Size and time

Works 36, Watch 20, Survey 20, Bridge 14, Infirmary 12, Galley 12, Comms 10, Garden 8, Store 6: **138 talks, 1,242
lines.** Two writer seats in parallel, about one session each, then TR1's review and fixes (one seat: two sessions).

## For the engineer (TE1, told on 2026-10-20)

- Files `content/talkpack/work-<pool>.talk`, header `@talks work:<pool>`, same talk grammar.
- Ids `work.<pool>.<slug>`, hand-written and frozen; fired in the same `{ id: [day, crewId] }` record.
- Pool from the roster dept by a table: works, watch, survey, helm+command → bridge, comms, infirmary, galley, garden,
  store; guests none.
- TE1's picker already takes an ordered source list (`TALK_SOURCES`, claude/talk-wire aeef392): a work pool is one more
  entry; "mixed" (taking turns) needs one small extra rule.
- Same condition words plus `role:engine|bar|counsel` (a fixed list, mapped by a table from the roster's role text:
  Engine officer/technician → engine; Bartender, relief bartender → bar; Ship's Counsellor → counsel). Command vs helm
  in Bridge uses the existing `dept:`. The roster's `civilian` dept has nobody today: no pool.
- Work talks count as topic `work` for the shared pool's variety rule.

## Questions for the user (answer on the page)

1. Order: own → work → shared (recommended) / mixed / shared first.
2. No repeats: once per save (recommended) / once per person.
3. Pools: nine as listed (recommended) / fewer, bigger / more (split Works).
4. Size: about 140 (recommended) / about 90 / about 200.
5. Friend tier: ordinary mistakes and doubts, ending warm (recommended) / all light / deeper.
6. Works treats you as a workmate (recommended) / same as other pools.
