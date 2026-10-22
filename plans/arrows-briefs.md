# Builder briefs: the arrow queue (piece B) and the panel pointer (piece C)

Written by AR1, 2026-10-22, for the arrows plan (`plans/arrows-pillar5-plan.html`, section "How it could be built"),
against claude/integration 2b4a05db (0.64.15). Line numbers are from that build; search for the names if they have moved.
Read first: CLAUDE.md, DEV_NOTES "Rules that keep it working", `plans/owners.md`, the plan page, and
`plans/arrows-pillar5-notes.md` ("How the game guides the player today" and "Step 1: the tracked shift").

**Decisions (the plan's five questions, answered "go with the recommendations", 2026-10-22, as passed on by lead 27):**
fixes first; the shift's arrows every shift while the shift is tracked, panel pointers the first three times
(`once: 3`); a training meeting may take the arrow from 15 minutes before, the job's arrow back straight after (level 2
over level 4); a Settings switch for teaching arrows, all / first time only / off, default first time only (C builds
it, B reads it: see "The Settings switch"); the burst pipe's job taken at the pipe (F4).
Two more (AR2's questions, as passed on by lead 27): scan first, every faulty-machine job starts with "Look it over"
once you have the scanner (FX2 builds it; F3's arrows assume it); the inspection, Tomas warns you in Bunk 1 on the first
Wednesday evening, then F2's Thursday 06:00 arrows.

**Both pieces start switched off** (`GUIDE_ON = false`, `POINT_ON = false`): with the switch off the game is identical
(cadet_test ALL IDENTICAL, no new save keys written). Nothing here calls `R()`. Neither adds anything to the 3D scene:
both are page elements (no draw calls).

**Relation to FX1.** FX1 is fixing the arrow lifecycle now (career arrows that never clear, the stale
`SHIP.player.track` check, "On shift", Dev mode's tracking switch, clock out). B does not undo FX1's fixes: it gives
them one home. Where FX1 added a clear-when rule to a caller, B's migration turns that rule into the entry's `done`.
Start B from integration once FX1 is merged, and read FX1's diff first.

---

## Piece B: the arrow queue ("guide")

**Seat and slot.** The interactions engineer's section 15b, in its slot
(`// ---- slot: Interactions engineer (section 15b)`, line 15943, above the end line). B owns `setGoal`, `clearGoal`,
`goalNow`, `ixFrame` and `ixJobStep` (all 15b), so no owner sign-off is needed for those. Callers in other sections move
to the queue in their own owners' sections, in pieces D-F, not in B (see "Migration").

### What it is
One table of things that want the world arrow, and one rule that picks which one shows. Today whoever calls
`setGoal` last wins, and nothing clears what it set unless its author wrote that code. After B, sections *ask*; the
queue picks the most important live entry, shows it through the existing `IX_GOAL`, and clears each entry when
its own `done` says so.

### API (new, in the 15b slot)
```js
// guideAsk(entry) -> true if added or refreshed (same id replaces). Pure data plus small functions; no side effects.
guideAsk({
  id: 'train:m4:meet',          // unique; also the "seen" key for once-only entries
  level: 2,                     // 1 now · 2 in the next 15 min · 3 learning · 4 your shift · 5 your body · 6 you chose
  goal: () => ({ deck: 5, crew: 'esposito-yara', room: 'r', label: 'Meet Yara: Main storage, 12:00' }),   // same shape as setGoal's
  from: absMin | null,          // not before (ship minutes, absolute); null = now
  until: absMin | null,         // gone after (the queue drops it)
  done: () => bool,             // checked once a ship minute and on events below; true = drop it for good
  once: true | number,          // show the first time (true) or the first n times, counted in SHIP.guide.seen[id]
  tip: { id, text } | null,     // optional: tipShow(id, text) when it first becomes the shown entry
  owner: '24 core',             // for the debug list and the arrows check
});
guideDrop(id)                   // the asker ends it early
guideNow()                      // -> the shown entry or null (for the Tracked panel and tests)
guideList()                     // -> all live entries, sorted (for Dev mode and the arrows check)
```

### The rule (`guidePick`, once a ship minute from `ixFrame`'s minute key, and at once after guideAsk/guideDrop)
1. Drop entries whose `until` has passed or whose `done()` is true. A `done` that throws counts as done (logged once).
2. Of the rest with `from` reached, pick the lowest `level`. Ties: the earliest `from`, then the earliest asked.
3. Tracking off (`SHIP.player.track === null`): only levels 1-2 show. The player chose quiet; urgent things still come.
4. Something the player tracked themselves (Tracked panel, Maps, Roster, a heads-up's Go: today's `IX_GOAL` with `trk`)
   is level 6, but **sticky**: only a level-1 entry may take the arrow from it, and when that entry is done the
   tracked goal comes back. (Today the Tracked panel's own `trkDone` does the clearing; keep it.)
5. Level 4 (your shift) has no entries of its own at first: it *is* today's fallback, `ixJobStep` then `ixWorkStep`.
   So with an empty queue the game behaves exactly as now. Piece D adds the clock-out and empty-board moments as
   level-4 entries.
6. The shown entry is written to `IX_GOAL` with `guide: id` on it, so code that reads `IX_GOAL` still works. Any
   direct `setGoal` call not yet migrated keeps working as before. While such a goal is up, the queue holds back,
   except for level 1, which may replace it (and puts it back after, as rule 4).
7. `once` entries count a "show" when they first become the shown entry; at the limit they are dropped before
   showing. The count is saved (`SHIP.guide.seen`, a small object of id: count, read back defensively like
   `tipsSeen`; cap 300 ids, oldest dropped).

### Done-when rules (the library: small helpers, so callers don't each write their own)
- `guideAt(deck, room)`: you are in that room on that deck (today's `trkDoneCheck` logic).
- `guideNear(goal, m)`: within m metres of the goal's world spot.
- `guideMet(occKey)`: the occasion is met, kept or missed (`SHIP.occasions`, status not 'asked').
- `guideTaken(jobId)`: the job is claimed by you, done or gone.
- `guideClocked('in' | 'out')`: `careerClockedIn(day)` or out.
- `guideTrained(id)`: `SHIP.works.tr[id] !== undefined`.
- `guideStage(id, st)`: `SHIP.works.cur` is no longer at that stage (for meet/watch/do).
- Every entry also needs a time limit (`until`); the queue warns in the console if one is asked without it.

### Words
Labels stay under about 30 characters, from the writer's keys via the asker's own text function (`worksText`,
`careerText`), stand-ins until written. The queue itself has no words.

### Migration (each in its owner's section, done by pieces D-F, not by B)
The 31 `setGoal` calls at 2b4a05db, by section, with what each becomes:
- 24 core 45268 (training meeting): level 2, `from` = 15 min before, `done` = `guideStage(id, 'meet')`. Piece E.
- 24c 45906 (drill): level 1, `until` 15:15, `done` = drill job closed. F2.
- 24f 48376 (burst pipe call): level 1, `done` = `guideMet('works.m6@d')`. F4.
- 24h 48535 (team turn): level 1, `done` = the step done. Later (Step 3).
- 24p 49306, 49409, 49468, 49569 (test job, summons, cabin, ceremony): level 1 or 2 with a met or arrived `done`. Later (Step 3).
- 24k 47635-47641 (clue arrows): level 3, `done` = the clue collected; they must stop setting `track = null`. F3.
- 15 14600, 14649, 15139 (needs, tea, clock): level 5 (1 when urgent), the tea arrow level 2, the clock level 4.
  Their own "never over someone else's" checks become the queue's job. D.
- 15b 15757 (round guide): level 3. F1.
- 21, 21b, 18, 20 (intro, clothes, events, sick): unchanged in B. They keep working as direct goals (rule 6);
  move them later only if a clash shows up.
- 19 (device "go" buttons, Maps, Roster, Settling in): these are the player's own choice, so they become the sticky
  level 6 (rule 4). Fix their `track = null` (FX1 is on it): choosing a place must not switch the job arrow off for good.

### Pop-ups: a short queue (added to B, 2026-10-22, the lead's placement)
Today `toast(t, x)` (section 11, line 52957, the HUD seat's) has one slot: each call replaces the text at once, so on
Day 2 at 10:00 Torres's invitation was replaced within the same ship minute by three other pop-ups. Add, behind
`GUIDE_ON`:
- `toast` keeps its signature. While a toast has been up for less than about 2.5 real seconds, a new one waits in a
  queue of at most 3 (older ones beyond that drop, never the one on screen); each queued one then shows for at least
  2.5 seconds, the last for the usual 5.6.
- Same title and text as the one on screen or queued: merged, not repeated.
- A toast marked urgent (an optional third argument `{ now: true }`, for the burst pipe call, the summons, the drill,
  "Bursting") jumps the queue.
- Real-time timers as today (toasts already run on real time, not the ship clock); the queue empties on a deck change.
- Section 11 is the HUD seat's: the edit is small but goes to that owner for sign-off. If the HUD seat prefers, the
  queue can live in the 15b slot with `toast` wrapped there.
Tests (arrows_check part "queue"): five toasts in one frame show in order, none for under 2.5 s, at most 3 waiting;
an urgent one shows at once; GUIDE_ON false is identical.

### The Settings switch (decision 4; agreed 2026-10-22 between AR1 and AC1, the lead's call: AC1 owns it)
Builder C (AC1, the device seat) adds the row to section 19's Settings app: `SHIP.device.settings.teach`, 'all' | 'first'
(default) | 'off', kept by 19's settings reader, read through `teachMode()` in 19's slot, shown only while
`GUIDE_ON || POINT_ON`. B reads it through `guideMode()` (teachMode() if present, else 'first'), so neither branch
needs the other. Meaning, for B's entries and C's pointers alike:
- 'first': `once` entries and pointers show their set number of times, as planned.
- 'all': `once` is ignored for teaching entries (level 3 and pointers): they show every time they apply.
- 'off': no level-3 entries and no pointers. Levels 1, 2, 4, 5 and 6 are unchanged: the shift's arrows, meetings and
  emergencies are not teaching.

### Tests for B (a new check, `arrows_check.py`, part "queue"; it can be built with B and grown by D-F)
- Off: `GUIDE_ON = false` gives cadet_test ALL IDENTICAL and no `guide` key in the save.
- Order: ask a level-4, a level-2 and a level-1 at once: the 1 shows, then the 2, then the 4 as each is done.
- Done and until: an entry past `until`, or with `done` true, never shows; one whose `done` throws is dropped.
- Once: a `once: 2` entry shows twice across a reload and never a third time.
- Tracking off: only levels 1-2 show.
- Sticky: a tracked place stays up through a level-2 ask; a level-1 borrows it and gives it back.
- Never stuck: over a played Day 2-8 (the honest shift player from `plans/arrows-tools/shift.py`), no entry is shown
  for more than its `until`, and the arrow is never empty while the player has a job and tracking is on.
- Save size: `SHIP.guide` under 4 KB after Day 26 (Dev mode's Set career).

**Size: M** (about one turn), plus the check's first part.

---

## Piece C: the panel and device pointer

**Seat and slot.** The device engineer's section 19, in its slot (`// ---- slot: Device engineer (section 19)`,
line 12566). The pointer lives with the device because most targets are device screens, and DEVICE_SKIN draws them.
Two small hooks outside 19 (owner sign-off, listed below) let it find the job board's rows and the clock screen's
buttons.

### What it is
A second marker, the same gold ring as the world arrow (`#ixGoal .ixarr` styles), that sits on one button inside an
open panel, with a short label. One at a time. When the button's panel isn't open, it points at what opens it
instead (the Device button, then the app tile, then the tab). It never pauses or blocks anything; a tap on the
button works as normal and ends the pointer.

### API (new, in the 19 slot)
```js
// pointAsk(p) -> true if added. One pointer shows at a time; the rest wait (a small queue like TIP_Q's).
pointAsk({
  id: 'p:works:training',          // unique; also the once-key (SHIP.device.pointsSeen, saved like tipsSeen)
  path: [                          // where to point, outermost first: the first step whose panel is closed is shown
    { open: () => DEV.open, el: () => document.getElementById('devBtn'), label: 'Open your device' },
    { open: () => DEV.app === 'works', el: () => tileFor('works'), label: 'Works: your training' },
    { open: () => WORKS_TAB === 'training', el: () => buttonFor({ app: 'works', do: 'tab', arg: 'training' }), label: 'Training' },
  ],
  done: () => bool,                // e.g. the tab has been opened once
  until: absMin | null,
  once: true | number,
});
pointDrop(id); pointNow();
```
- `tileFor(appId)`: the home grid's `button.app[data-app="<id>"]` (line 11763).
- `buttonFor(action)`: a device view button by its action ({ app, do, arg }). The skin's `act(el, action)` must leave the
  action readable on the element (a `data-act` JSON or a WeakMap): a small change inside 19's own skin.
- `deviceChoose` cards (marks card, tuning's minus/plus, the bunk card, the valve card): `chooseButton(k)`, the k-th
  choice button of the open card.
- Job board rows (15b, owner: interactions engineer): each row gets `data-job="<job id>"` on its button (the `row()`
  helper, line 15590). Then `boardButton(jobId)` and `boardTurnIn()`.
- The time clock screen (section 20, owner: the career engineer): its Clock in / Clock out buttons get
  `data-clock="in|out"`. Then `clockButton(want)`.
- The meeting panel's "Go on" button: `#devDlg .next`, if a lesson ever needs it.

### Drawing
- One `div#ptr` (fixed, `pointer-events:none`, z-index above the device sheet and the board panel, below the dialogue),
  holding the gold ring and the label pill (reuse `#ixGoal`'s CSS values; one shared CSS variable for the gold).
- Placed each animation frame from the target element's `getBoundingClientRect()`: the ring around the button's
  near corner, the label above or below to stay on screen (the same edge rules as the world arrow's label).
- Hidden while the element is missing, off screen, or covered by a dialogue; never shown during a meeting
  (`body.dlgon`) or a tip on the same spot.
- Reduced motion: no bob (as `#ixGoal`).
- Draw-call cost nil. Layout cost: one `getBoundingClientRect` a frame while a pointer is up; nothing when none is.

### Rules shared with B
- Pointers are teaching only: every one is `once` (true or a small number), saved in `SHIP.device.pointsSeen`
  (cap 200), and obeys the Settings switch the user is asked about (question 4: all / first time only / off).
- A pointer and the world arrow may show together (the world arrow on the job board, the pointer on its row once the
  board is open). Never two pointers.
- `done` is checked once a ship minute and on every device draw and board draw.

### Tests for C (`arrows_check.py`, part "pointer")
- Off: `POINT_ON = false` is identical; no `pointsSeen` written.
- Path: with the device shut, a Works pointer sits on the Device button; open the device, it moves to the Works tile;
  open Works, to the Training tab; open it, gone, and never again after a reload.
- Board: a pointer for a held job sits on that row's Take it at 390x844 and 844x390, and goes when the job is taken.
- Clock: on the clock screen's Clock in; gone once clocked in.
- Cards: on the k-th choice of an open `deviceChoose` card; gone when picked.
- Never off screen: the ring and the label are inside the viewport at 360x640, 390x844 and 844x390 for every target
  above (screenshots kept).
- No draw calls added (`renderer.info.render.calls` the same with a pointer up as without).

**Size: M** (about one turn), plus the check's part.

---

## The arrows check (`arrows_check.py`), in full once D-F land

Built from AR1's play tools (`plans/arrows-tools/`): it plays as a player who **only follows the arrow and the
pointer**: walk to the arrow (a teleport stands in for the walk, as Dev mode's Take me to does), tap the thing it points
at (`playerTap` on the nearest item, or a real click at the pin), press the button the pointer is on, read meetings
through. It fails if:
1. the arrow points nowhere while the player has a job (tracking on), or at a spot with nothing to tap after 3 tries;
2. an entry stays shown past its `until`, or a career entry is still up after its `done` should be true;
3. a lesson isn't trained by the end of its day when the player only followed arrows (Days 2-8: m1, m4, m3d, m5, m3i,
   m7, p3, m6, m2);
4. the player misses a clock-in, a meeting or the inspection while following the arrows;
5. a pointer is off screen or on a hidden element.
Runs from Dev mode's Set career to Day 1 with tracking set as in a real game (a job taken yesterday), about 10-15
minutes for Days 2-8. In check_fast? No: in the full round, with the career and machine checks.

## Order
B and C can be built at the same time (different seats, no shared lines). D (the shift chain) needs both. E (the four
training arrows, 24 core) needs B, and C for its last two steps. F1-F4 need B and C and can run side by side.
