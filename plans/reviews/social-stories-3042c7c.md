# Re-review: claude/social-stories 6ec7522..3042c7c (0.39.7-0.39.10)

Reviewer 1, 2026-10-17. **Verdict: PASS WITH FIXES** (one medium contract fix in `homeOk`; the rest low or for other seats).

Range: 52561f6 and 31e2960 (merges of social A 0.36.58 and 0.36.59: build lines only), 8892ac9 (0.39.7, B8 calls home), bf240b7 (0.39.8, one live beat per contact on Letters evening, recorded messages), 2212052 (0.39.9, recorded messages known by sender and subject), 3042c7c (0.39.10, read-only queries), then notes and a screenshot (4222804 is notes only). All game lines are in 20c except the build line. New `schedU` keys: 682, 683, 684, 685, 686 (calls home), each used once, inside B's 672-699.

## Findings

### 1. Medium: with a section 22 older than dialogue 0.43.11, nothing you can tell home ever passes, so calls have no replies and recorded messages can't be answered
Path: `homeSends` -> `homeOk(sendLine, hp, ctx)` -> `linesOk(o, ...)` with the whole send line (`text`, `id`, `flavour`, `reply`, `sets`, `memo`). Only `beat` is taken out. Dialogue 0.43.11's `LINE_META` skips those keys, but the section 22 the sim-engineer branch carries (and so the build master's full merge, which has no claude/dialogue) is `new Set(['text','id','tone','w','odds','not','old','lines'])`: `lineCond('reply', ...)` returns false and every send line is rejected.
Evidence (probe p7 block 3, the same steps on two builds with content's HOME_* baked in: four first calls, then `homeMsgHour` at noon until a message comes, `socialMail`, `mailPlay(m)`, pick the first reply, `dialogueEnd(true)`):
- social-stories + claude/dialogue: `"shown": true, "after": false, "reply": [["Gran", 7921]]` (answered; Gran's answer queued for the next day).
- full merge (no claude/dialogue): `"shown": true, "after": true, "reply": []`: the message plays with no choice line, so nothing is picked, it stays unanswered and Play stays on. Everyday calls on that build get no "things to tell them" choice either (the `{ send: true }` line drops out).
`grep '^const LINE_META'`: full merge line 13966 has the short list; dialogue's has `'flavour', 'reply', 'sets', 'memo'`.
Fix (one line, makes 20c independent of which section 22 is in): in `homeOk`, delete the data keys before asking section 22, e.g. `for (const k of ['text', 'id', 'flavour', 'reply', 'sets', 'memo', 'lines', 'warm']) delete o[k];` next to `delete o.beat`. Until then, ship calls home only in a build that also has claude/dialogue 0.43.11 or later, and say so in the hook register.

### 2. Low: a recorded message with no reply lines can never be answered from Mail
Path: `homeMessage` adds a choice only when `homeSends` gives something; with none (every news told and no anytime lines whose conditions hold, or finding 1), `picked` stays null, `homeMsgDone` never runs, `c.msg.done` stays false, Play stays on and `homeMsgHour` posts no further message from that person until you call them. Fix: when `ch` is empty, mark the message heard in `onEnd` (`c.msg.done = true`, no reply Mail).

### For other seats (seen on the full merge; not caused by this range)
- **The jump test fails on the full merge with today's tips**, and it fails the same with social B at 0.39.6 (worktree rv-socB-full2b: arrival 8c28e91, sim 5687bec, deck-plans 4613d43, social dc80136, social-stories 6ec7522, player-needs 7e4cb98, galley 3721d34), while the 0.39.6 full merge with the earlier tips passed. Diffing the two saves (`jumpdiff.py`, the social_check RUN with jump false/true): the only difference is `cues`: the jump has `{"key": "repair.recycler", "at": 937, "who": "eklund-leila", "dept": "works", "room": "R"}`, the hour-by-hour run doesn't. So section 17's crew repairs (or the bus timing of their notes) differ between a jump and hourly. For the sim engineer and social A.
- The booth hook (player engineer 3's 8abc711) isn't on player-needs 7e4cb98, so in my full merge nothing calls `homeBooth` yet; the device's Play button (device engineer 3's 0.35.27) isn't in it either. Both are in the hook register; check them on the next combine.

## Checked and fine
- **The purity fix (0.39.10):** on a fresh game (content's HOME_* baked in, with and without claude/dialogue), `beatOf('home.mum')`, `homeBeatOf`, `homeFlags`, `homeKnown`, `homeCallable`, `mailPlayable`, `mailPlay` of a non-message, 46 hours of `homeMsgHour` outside noon, 200 `lineFor(..., { peek: true })` calls (121 lines) and `linesOk({ beat: 'home.mum.1' })`: `JSON.stringify(SHIP.social.stories)` and `socSave()` unchanged (`storiesSame: true, saveSame: true`, stories `{}`). The first real call creates only that contact's record.
- **Missing dialogue data:** on the bare tip (no HOME_* blocks, no `linesOk`) the page loads with no errors, `homeCallable` is `[]`, `homeBooth()` opens the panel with "the relay's busy". No TDZ: the HOME_* blocks are read through `typeof` inside try, and 20c's own consts are only read by functions called after load. `HOME_MSG_SUBJECT` is declared after `homeMsgHour` but only read when it runs.
- **Pacing over 100 days** (claude/dialogue merge, Mum called daily, the others every third day, at 20:30): all four arcs reach beat 6, live beats land on Letters evenings (days 21, 28, 35, 42, 63, 84, several contacts the same evening, as 0.39.8 intends), six recorded messages, the home state 1584 bytes, social save 13.2 kB. The same run twice: identical. Day 0: calls on the arrival Sunday at 20:00 work (a clear line, beat 1, `day: 0`); `weekday(0) === 6`.
- **Recorded messages (0.39.9):** Mail keeps only id/at/from/subject/body/read, and the message is found by sender and subject: `mailPlayable` true, `mailPlay` shows `home:msg:gran`, the reply is queued (claude/dialogue merge). (On 0.39.8 the `play` field was dropped and Play did nothing; 0.39.9 fixed it.)
- **Save:** a real `saveGame()` + reload (`?debug`) gives the same `stories.home` and `homeBeatOf('home.mum') === 1`. Social part on the full merge 22201 bytes with the reserve (86 crew), limit 30000; calls home add about 1.6 kB after 100 days and every list in it is bounded (sent and mem by the writers' ids, learn by the beats, keepsakes 8).
- **New game:** `socReset` sets `stories: {}` (probe p2: after `newGameStart(false)` stories is `{}`), and the home flags go with `SHIP.flags`.
- **Merges:** 31e2960 already merges social A's tip (dc80136); social-stories + claude/dialogue (4cbf62c) conflicts only on the build line and DEV_NOTES; name_check OK on both and on the full merge.

## Tests
- `name_check.py --branches 6ec7522 origin/claude/social-stories`: NAMES OK; `--branches f6c2a74 origin/claude/social-stories`: OK. `name_check.py` on the full merge and on social-stories + dialogue: OK.
- social_check (B's copy, unchanged since 0.39.8, same as social A's): bare tip 0.39.8 OK (save 15127). Full merge with 3042c7c: everything OK except "two days in one jump" (above; not this range).
- Browser probes p3, p4, p6, p7 (`?nosave&debug`; `?debug` for the save), no page errors.
