# Handover: event reviewer 2 (ER2), the adversarial reviewer for ship-wide events

Written 2026-10-21 by ER2 (session_01S8pboNujAzZgMSWFK84CxD), at about 460k of memory, at lead 23's request.
The fresh reviewer (ER3) takes the Crossing the Line **build** review from L1 on.

## Role and people
- **Role:** adversarial review of every event plan and every event build, plus one-off reviews the lead hands out.
  Verdicts are PASS / PASS WITH FIXES (exact fixes) / FAIL. They go to the author and the lead, in plain words.
  Reviews live on branch `claude/event-plan-review-2`, one file each.
- **Lead:** lead 23, session_01XXiKm9iPgm565SZ4n1knmU. Report only there.
- **Authors you'll meet:**
  - EP2 (session_01GpiqZ9jCYbS9XTNPF8adHr): the Line plan
  - EP3 (session_01PC5DMnhFSWXqPZSk8wa779): the storm plan
  - EV4 (session_01MqpjPG6mDFe5avrDxcNWTU): the storm builder
  - LW1 (session_01FDk7X14eAEbCZtr59mLxPi): Veyli lore
  - OP1 (session_01RxxLLT9jpvagqJpCW99dop): the optimization pass
  - PR4: the turn reviewer
  - EC1: bigevents_check

## What I reviewed (all on `claude/event-plan-review-2`)
| File | Subject | Final verdict |
| --- | --- | --- |
| `plans/event-line-plan-review.md` | Crossing the Line plan (claude/event-plan-line, last 9ea6ec7) | PASS |
| `plans/event-storm-plan-review.md` | Ion storm plan (claude/event-plan-storm 06ce585) | PASS |
| `plans/veyli-lore-plan-review.md` | Who the Veyli are (claude/veyli-lore 9fa7521) | PASS |
| `plans/opt-plan-review.md` | Optimization pass plan (claude/opt-plan d1a6516) | PASS |
| `plans/event-storm-build-review.md` | Ion storm build (claude/storm-update 5f3fc3f) | PASS. S10 waits for S2 with the Fridays (DEV_NOTES) |

## Method (what found the real bugs)
1. **Never trust a number in a plan: measure it in a new game.** Each plan review found at least one wrong fact:
   - the Line's crew count (86, really 76) and its first-timers (13 and 17, really 1 and 4);
   - Tomas's whereabouts on Saturday, and his watch post;
   - the storm's lantern job, which didn't exist;
   - "the human union" in facts.md;
   - perf_check standing you in the wrong rooms.
2. **Play builds as a player:** a switched-on copy, phone size 390x844, skip to the beat, go to the deck, stand
   there, step real frames, then answer the panel. But teleporting next to someone hides reach bugs (the storm's
   4 m Lukas bug). For any "near someone" moment, make the author prove it with a **walking** probe, as EV4's
   `plans/storm-probes/walk_servery.py` on claude/storm-update does.
3. **Reloads:** check what a story flag is set on (open, reply, end). A flag set when the panel opens loses the
   moment on a reload.
4. **Off means identical:** cadet_test with the branch's merge base as old and the tip as new (`OLD.html NEW.html`).
5. **Spoilers and canon:** grep content/facts.md, the arcs (`"<id>:<n>"` beats with `mem` and `learn`), the roster
   tiers (`{"tier": 4, "topic": "secret"`) and the voices' `avoid`. Saruth's secret is "sent because no one at home
   expected the posting to work". Holt's is beat 3 (Hanne Rook, the six hours of silence). Brennan's beats 4-5 are
   about leaving (Nell Arrowby). Tomas's beats 5-7 are the exam, the list and staying. Veyli pronouns are they/them.

## Probes (copied to `plans/er2-probes/`; they need `/tmp/cadet-work/three`, see DEV_NOTES)
- `probe.py BUILD JS`: opens the game (cadet_test's Game) and prints the JSON a JS snippet returns. Useful globals:
  `schedPeople`, `aboard(p, d)`, `isWorkDay(p, d)`, `planDay(p, d)` (absolute minutes: day d starts at (d-1)*1440),
  `whereIs(p, t)`, `eventsOn(d)`, `galleyMenu(d)`, `gatherSpots(venue)`, `DECKS[n].places`, `BLOCKED` (only after
  `goToDeck(n)`), `EV_CALENDAR`, `SHIP_EVENTS`, `SHIP.event.mine`, `SHIP.mail` (newest first).
- `play.py` and `play2.py`: storm play-throughs (Friday moment, errand, supper, crowds, the party, Mails).
  `__near(id)` stands you beside someone; `__dlg(k)` plays a panel and picks reply k.
- `dc.py`: draw calls at 390x844 at a few spots.
- Make a switched-on copy with `sed 's/^const EVENTS_ON = false;/const EVENTS_ON = true;/'`. The Line has its own
  switch, `EV_LINE_ON`, so check what it follows. **Regenerate the copy after every new commit.**
- Give each run its own `CADET_WORK` (the probes use /tmp/cw-er2).

## What to watch in the Crossing the Line build (L1-L6, claude/event-plan-line's plan at 9ea6ec7 and later)
- **Decided by the user:**
  - story A, "The one on watch";
  - q1 b (Saturday talk from 08:00; Vance's Mail at a fixed 18:00, which needs EV1's fixed-minute Mail);
  - q2-q8 a;
  - line-q10 A, "guests in someone else's sky": "as guests", never "by the Veyli's leave", and "the charts are thin"
    past the Line.
- **The ceremony moved to the bow lounge**, in its own venue `bow-lounge-line`, switched on only with the event:
  - lead spots on open tiles 50,9-50,12 (the Captain at 50.5,10.5);
  - the bowl and ribbons only 14:30-15:15;
  - the reading corner there at 16:00.

  Check that the lead tiles are still open and hold no place. Check 49,10 and 49,11 are low furniture (the deck
  architect's call).
- **Numbers to re-measure on the build:**
  - 76 aboard on Day 7 (74 crew and 2 guests);
  - 25 at work at 14:30;
  - `standEasy` (not command, helm, watch or the galley line), so the crowd should reach 45 or more, capped about 60;
  - 21 first-timers under two years;
  - Saruth excluded (`not: saruth`);
  - Ulla goes like anyone off duty.
- **Tomas:** at his post `2-watch-6` (Deck 2's lift lobby) 08:51-17:00 and never pulled away. The mug stop finds him
  from his plan. He's on the Lap at 20:30 with `torres-zeke` and `pell` pulled to 1 (`EV_DAY_DRESS`, the Map keyed
  `trad@day`). The Captain walks the Lap with no line. The Saturday moment follows him (mess, garden, then climbing
  on the rec deck 22:08-22:40, in bed 22:46), with the Mail fallback at about 22:50.
- **The Sunday table re-dressed:** k 440, the crew's voted dish (fish and chips in a new game) plus a pudding,
  18:00-19:15, no Saturday Mail.
- **Off:** `EV_SHIPWIDE`, `eventsOn` and Deck 3's places must be byte-identical.
- **Two events in one calendar:** the storm's `EV_DAY_DRESS` rows (Days 14, 15, 21) and the Line's (Day 7) share one
  table. Check neither clobbers the other.
- **Draw calls:** about 240-300 in the lounge on Day 7. Re-measure with the bowl, ribbons and plaque at 390x844 and
  the widest zoom. The storm's party measured 343 at phone sizes and 416 at the widest.
- **Reloads and reach:** the same two traps as the storm: flags set on reply or end, and walk to the moment, never
  teleport.

## Loose ends
- **The storm:** S2 (Marrow and Vance off the double shift for Day 12's address) is being built by EV4 with
  claude/fridays merged in. Lead 23 may ask for a quick look before S10. The nits that stay:
  - the commendation is mentioned at 10:00 but its Mail comes at 10:12;
  - the gist notes land after the Monday debrief after a long skip.
- **The optimization pass:** item #4 (keep shaders across deck changes) must measure the shader count after every deck
  at both phone sizes. My note is in `plans/opt-plan-review.md`.
- **backlog 18b:** perf_check's tile-for-world bug, item 0 of the optimization pass.

## Gotchas
- `nearestOpen(x, z)` wants world coordinates: use `cellPos(i, j)` first.
- `DRESS.on` fills on `eventsTick`, not `goToDeck`.
- `BLOCKED` is for the current deck only.
- `eventStopOf({ machine })` matches a machine's kind, or `id.split('-')[1]`, never the whole id.
- `SHIP.mail` is newest first, and Mails sent during a skip land in a batch.
