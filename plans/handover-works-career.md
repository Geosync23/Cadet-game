# Handover: the Works career engineer (seat C2, after C)

Written 2026-10-19 ~03:55 UTC by C2 (session_014yREkgPvuwMyxBtoqB1P14, ~63% memory) for the next Works career seat. C's note for Steps 1-2 follows below; read both. Then CLAUDE.md, DEV_NOTES.md (the 0.44.14-0.44.26 rows; "Testing"), plans/brief-p5s3.md on claude/lead-pillar1, and the page `plans/mechanics/promotion-officer.html` on claude/p5-design.

## Branch, builds, people
- **Branch:** `claude/works-career`, head **f3b744c = 0.44.26** (on 0.63.2r 898d58d + DA5's claude/deck-p5s3 e58c9b1 merged in). Builds used: 0.44.14-0.44.26. Next: 0.44.27.
- **Hash keys:** 850 (training meeting time), 851 (What's next line), **852 (the ceremony's friend tie, promoGuests)**; 853-854 spare.
- People (2026-10-19): lead 16 session_01UMyfd16GqSdgNyz5PE8qSv; BM6 session_01F8k6hqdBRoxDJMzqAuiHqR; R3 session_01AR6tGFiSZF7hL1LfVpWgng; X crew sim session_01SNaWA6X5E9i2ZKfMnPTHJf; W2 writer session_01866TWKzGRgZmFcxiYRi4db; U HUD session_01FcMPTX7mMTHkyr4pxDfNcS; S2 systems session_01Wiqm2pAvvyJYGQyUgbsfXY; M2 session_016kzZEwTjU6H1miJmA13TRh; M3 session_01WJczDg7E7y1jR96aCMbNew; H2 session_01SixL3TcPYoHEP1DPv8cBRZ. DA5 and P have handed over.

## What C2 built
- **Playtest 1 (0.44.14-0.44.16):** the day shift 09:00-17:00 (`DAY_SHIFT` [540,1020], `DEV_SHIFT`, `shiftTick`, time clock opens 08:00 = `CAREER.clockIn`, leave bookable to 08:30, Day 1-3 times +1 h); the morning round still held to 11:00 (`ROUND_HELD` 120); more board jobs (CHORES per up ~1/day, `HOLD_MAX` 4). Breakfast 06:00-09:00 is X's.
- **The bridge by invitation (0.44.17, 0.44.22):** section 20 after the career occasions: `SHIP.bridgeInvited` (saved), `bridgeBarred(edge)` (asked by DA5's `YOU_LOCKS[1]` in section 4: edges v,10,5 / v,10,6 / h,14,10; exempt: already inside, doorOpenFor on B or R), `bridgeDoorTap`, `bridgeTick` (toast near the doors), `bridgeInviteReady(d)` (Vance's invite after the first ship-wide event; day 22 in a new game). S2 keeps bridge-room jobs off your board until invited.
- **24p THE FIRST PROMOTION (0.44.18-0.44.26)**, end of section 24: part 1 the test job (`promoAnnounce` Day 8, `WORK_MECH.t2.offer`: jobReserve(scrubber, d, 540, slot 20, { tier 2, train t2, until 15:00, cause filter, drift 2 }), `promoPassed` via worksDone, `promoDelay` +2 workdays, tuneSet at the repair stop); part 2 the summons (`OCCASIONS.promoSummons` 11:00 Calder's office, 10:30 urgent notice, 11:15 Calder follows you via `promoEscort`, scene `promo.officer` with onPick/onEnd hooks, `promoPromote` by 12:00 at the latest; friends' Mail; `promoPlan()` for X); Brennan's cake 16:30-17:00 (`promoCakeTick`, X's crewScene); part 3 the move (`promoMoveTick` 17:00 or up to 30 min later, `promoMoveEscort` lead to 4/W, `promoMoved` by 17:30, `worksHome()`, `worksHomeOpen` in doorOpenFor, simNote moveStart/moved); part 4 the ceremony (`OCCASIONS.promoCeremony` Day+1 17:15 1/O, `promoGuests` with key 852, X sets the appointment's `places`, `promoCommission` (keepsake from marrow, ms commissioned), `promoPip` (rank pips 0->1, rebuilt like playerKit), Calder leads you at 17:30, Mail by 19:00).
- **Shared bits:** ladder rows m8, m9, p1, p2 in 24 core's table (M2, M3, H2 sub-blocks); `SHIP.works.said`; `careerJobIn` fills `j.gains` for U's turn-in card (rep in words only, S2's j.meters as meters).
- **Line keys:** W2's final set (both name sets read; see DEV_NOTES 0.44.24/25).

## Loose ends (for Step 4 / the next seat)
- **`WORK_BANDS[2]` is provisional** [0,12,28,45,60]: Step 4's page should set the officer bands.
- **Section 15's locker and hobby texts that name Bunk 1 directly** are not switched to 4-23 after the move (P's note, plans/handover-player.md on claude/player-p5); the kit bag's bagLockerTap only runs on arrival day.
- Keepsakes aren't drawn anywhere yet; `DECKS[4].homeKeepsakes['4-23']` + `worksHome()` are ready.
- machine_check on this branch alone fails on DA5's dampers (S2's 'damper' kind): fine in BM6's merge order.
- H2 is switching p1Stage to `WORK_MECH.m9` (the P1-first puzzle_check clash in BM6's trial) — check it landed.
- `SHIP.works.mv` / `W.cake` are not kept by worksClean (a reload mid-walk restarts the walk; the cake toast may repeat once). Harmless.

## Gotchas
- **Never `pkill -f` a pattern in your own command line** (kills your shell); use `pgrep -f "[x]yz"`.
- The `simNotes` ring drops old notes after about a day: in long paper runs, record notes with `onSim` as they happen (career_check (j) does).
- `openJobs('you')` returns summaries, not job objects: look up `SHIP.jobs` by id for fields like `reserved`.
- Don't put a `//` comment in the middle of a one-line object entry (it ate `slot:` once); `node --check` the extracted script before a run.
- Check renames with W2 before switching: messages cross; I now read both sets.

## How to test
DEV_NOTES "Testing" setup (pip playwright; three r128 in /tmp/cadet-work/three; `CADET_CHROME=/opt/pw-browsers/chromium`). Per push: `career_check.py` (sections (h) bridge, (i) test job, (j) summons/move/ceremony/save/twice, (k) turn-in gains), `mech_check.py`, `leave_check.py`, `puzzle_check.py`, `deck_check.py`, `interactions_check.py`, `events_check.py`, `player_check.py`, `intro_check.py BUILD --week`, `cadet_test.py OLD NEW`. Run them one at a time from a script that logs each result (TEAM.md "Long check runs").

## Open questions for the user
- None from this seat; design calls (Tier 2 bands, dropping the work-40 need from t2, the cake's 16:30 slot) are with lead 16.

---

# Handover: the Works career engineer (Pillar 5, seat C)

Written 2026-10-18 ~14:50 UTC by session_01LgTgzjeqLNrjeCa2iRzbYx (about 58% memory) for a fresh session taking the seat for Step 3 (Officer, Days 9-15). Read CLAUDE.md, DEV_NOTES.md ("Pillar 5: your Works career, section 24 core", the 0.44.x build rows, the hook register), `plans/pillar5-plan.md` (Part 1, Part 3, Part 6 seat C) and `plans/mechanics/foundation.html` + the Step 3 pages on `claude/p5-design` first.

## Role, branches, builds
- **Seat C, the Works career engineer** (not the 0.61.x career engineer of leave and the time clock: that's `SHIP.career`, section 20). You own **section 24 core** and its checks: `career_check.py`, the frame of `mech_check.py` (and of `puzzle_check.py`, which H filled in).
- **Branch:** `claude/works-career` (head 8cc07a5 = 0.44.13). It already contains S 96cf5cb and P cfce34e (merged in for the join).
- **Join branch:** `claude/p5-join` (head 3f1ce38) = ce26fb2 (0.60.7 candidate) + S 78bf1c2 → 01a3a3b + P cfce34e + C (to 8cc07a5) + H 5a4d362. Build number 0.63.0 in that file. Green: career, mech, machine, puzzle checks, NAMES OK, cadet_test ALL IDENTICAL. Reviewers R and R2 passed it.
- **Builds:** 0.44.x (0.44.0-0.44.13 used). Hash keys: 850 (a training meeting's time), 851 (which What's next line today); 852-854 spare; Pillar 5's second range 1000-1049 is shared (ask before taking keys).
- People (2026-10-18): lead 12 session_01GjWhU9Z9V8RNoR8yyELA9V; build master BM4 session_013h22isZZqmJJSEKSbrwabf (BM5 also mentioned); reviewer R session_01MSLjUdmeVJetxFhh9PqzLt, R2 session_01DZoxp9pxhp63Wye1Kr2MsZ; designer session_01VXENaUt4vdyYtr3KjVZk9z; S session_01KxfsfBWkCGcncuuH2n1hFB; P session_0153WUGRakJnNzUCNNHf1E8X; H session_013nqpqRFX4hh3cLPhhpZirJ; M1 session_01PkbdtgrbpHymsmu5Pgazm7; M2 session_016kzZEwTjU6H1miJmA13TRh; writer W session_013DdpJv4AKFJcvuBBqjSXms. Report to the lead only finished pieces (hash, build, checks), blockers and design calls; hook names go seat to seat.

## What 24 core is (where: `// 24. WORK`, after 23 TILES, before 24g/24k and `// 6. CAMERA`)
- **State:** `SHIP.works` (saved `ship.works`), lazy: `worksInit()` makes it from Day 1 17:00 (`WORKS_START`), never at load. `worksClean` keeps only 24 core's fields: v, tier, rank, xp, tr, use, op, tools, sk, log, test, home, done, ms, cur. Sub-blocks keep their own data under their own key (24k `cases`, 24f `inc`) and read it back from `SAVED` themselves; the save writes SHIP.works whole so their keys survive.
- **cur** (the training under way): `{ id, st: ask|meet|watch|do|again|held, d, by, occ, j, w, hold?, told?, mail? }`.
- **The ladder:** `CAREER_LADDER` rows (m1, m4, m3d, m5, m3i, m7, p3, m6, m2, t2) with `size`, `day`, `needs`, `by` (teacher list, first on shift wins), `where`, `job`, `tool`, `stages`, `fixed`, `xp`. A row opens only if its sub-block registered `WORK_MECH[id]`. `ladderTick(h)` (from `worksCareerTick` each ship hour, and from S's `jobsHour`, idempotent): workdays only, big rows 06:00-10:30, small 06:00-16:00, one big and one small a day (`op[day]`), never for a day already past (0.44.13).
- **Training (big rows):** `trainOffer` (occasion `works.<id>` + Mail + toast + goal; `WORK_MECH.offer` replaces it; `WORK_MECH.at(day)` = earliest meeting minute) → meeting `MEETING_SCRIPTS['train.<id>.<teacher>']` (stand-in made if missing) → `trainWatch` (teacher's job via `M.reserve` or `jobReserve(row.job)` only if `row.job` is a machine kind; else trained at the meeting) → `trainDo` (your job, same slot 10+n; `M.hold` / `worksEscortHold` keeps the teacher until 24k's case on that job closes or `simNote('caseCalled', { train: true })`) → `worksTrained` (tr, tool, `simNote('trained')`). Missed → offered again next workday. `trainTick` waits while a dialogue is on screen.
- **Other APIs:** `worksUse(id)` (uses, tool wear, row xp; a small row's first use trains it once opened), `worksStage`, `worksIsOpen`, `worksTeach(mech, who, key, fallback)`, `WORK_TICKS.push(f)`, `worksTabAdd({ id, title, order, view, act, badge, verbs })`, `worksTabShow(id)`, `worksEscort(p, t)`, `worksRecordHead()`, `worksLockerText()`, `skillWord`, `worksBand` (null before SHIP.works), `worksNext`, `worksXp`, `worksNoticed`.
- **Reputation:** `WORK_BANDS[1] = [0, 8, 18, 30, 40]` (the page's; with S's real faults a steady player has 45-48 by the end of Day 8, a very busy one 35 at the end of Day 4). Later tiers need their numbers (Step 3 page).
- **Words:** everything through `worksText(key, standIn, vars)` on the writer's keys (claude/writer-p5 content/works/keys-p5.md).
- **Hooks into others' sections (made by me with the lead's OK):** section 12 main loop `worksCareerTick()`; section 14 `escortPlanOf` → `worksEscort`; section 19 Record first line → `worksRecordHead()`; Kit lockers via `PLAYER_TAPS` (from 24, no edit to 15b; Bunk 1's wardrobe stays clothes-only: the lead).

## Lessons from the join (read before Step 3)
- **Grep for name clashes before each push** (`name_check.py` on claude/reviews). My first clock was `worksTick`, which silently replaced section 17's job-board `worksTick`. Function declarations override quietly.
- **Tests that stub `window.x` don't reach in-scope functions.** The game runs inside an IIFE; stub through `window.__sc("x = ...")` and restore.
- **Run the checks on a combine, not only your branch:** real sub-blocks (24k's Day 5 case, the writer's meetings) changed the paths. The scripted players in career/mech_check now: call an open 24k case first (`caseCall(id, cause)`), read meetings through (`dialogueEnd`), count Mail from `cur.mail`.
- **Section 17's load catch-up runs `jobsHour` for every hour since the save** (and so `ladderTick`): anything hourly must ignore past days.
- **intro_check takes over 2 hours here;** BM runs it per candidate. Don't block a hand-off on it. Never `pkill -f` a pattern that's also in your own command line (it kills your shell).
- Merging S/P into your branch in merge order makes BM's merge clean (only build lines conflict; `plans/build-master/resolve.py` handles those).

## Step 3 for seat C (plan Part 3 and Part 6): the test job and the first promotion
- The Tier 2 test job: row `t2` (needs relied + m6 trained + Pillar 4 work 40) exists; it has no sub-block yet, so it never opens. Slots 20-23 are for test jobs; `jobReserve(..., { tier: 2, train: 't2' })` (S's 17.6 makes a held tier-2 job claimable).
- `SHIP.works.test` (`{ tier, day, tries, passed }`), `home`, `done`, `ms` are reserved in the save for the promotion page; `worksBandWord` already says "New officer" after a rank change; `simNote('promoted', { tier, rank })` is the planned note. `RANK_TITLE`/`works.rank.*` and `works.title.t*` exist.
- career_check must grow: test job pass/delay/pass, the promotion end to end (summons, Calder, the move to 4-23, the ceremony once), junior jobs no longer held after promotion but still on the board (S's 17.2: `j.junior`, `rankOk`). The rank-reserved-jobs test (never taken below rank, crew or you) was left for when S's 17.2 landed: it has (S 96cf5cb+) — add it.

## Loose ends
- `works.tool.<id>.about` (writer's key) isn't shown anywhere yet (Tools tab could use it).
- "Who noticed" in the Work log needs a caller (`worksNoticed(jobId, who)`; section 20 could call it on a repair reaction).
- design-doc.md has nothing on Pillar 5's foundation decisions yet (the designer's pages hold them); ask the lead whether to add a short section.

## How to test
Setup as DEV_NOTES "Testing" (playwright, three r128 in /tmp/cadet-work/three, `CADET_CHROME=/opt/pw-browsers/chromium`). Per push: `career_check.py BUILD`, `mech_check.py BUILD` (rows stubbed if no sub-blocks: inject `WORK_MECH[r.id] = { reserve: (d, at, slot, o) => jobReserve('washer', d, at, slot, o) }`, t2 `{ noJob: true }`), `cadet_test.py OLD NEW` (ALL IDENTICAL expected; Step 1 draws nothing), and on a join also `machine_check.py` (S's latest) and `puzzle_check.py`. About 3, 3, 4, 10 and 10 minutes.
