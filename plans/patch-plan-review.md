# Review of the playtest patch plan (PR1, 2026-10-20)

Reviewed: `claude/patch-plan` 2f8976c by PP1 (`plans/patch-plan.html`, `.md`, 26 shots, 43 probes), against the user's 28 notes in `plans/roadmap-after-recdeck.md` (origin/claude/start-here-review-3qoht9). The game at 2f8976c is unchanged from 5dd740c, so every line number in the plan still holds. Reviewer PR1, for lead 20.

## In plain words

The plan is careful and mostly right. I re-ran a sample of PP1's probes and wrote two of my own. The main findings reproduced: Day 2's meeting starts at 08:56 with no Chief; Zeke counts as "talking" and so never steps aside; about 130 toilet visits a day; the Captain spends about 11-12 hours a week on Deck 4. All 28 notes are covered, none were dropped, and the owners are right except one.

Things to fix before the plan goes to the user:

1. **Blocker, #1: the fix as written would still start the meeting without the Chief.** On PP1's own scratch copy she walked in at 08:54. The new rule ("fallback 3 minutes after you arrive") would fire at 08:48 for a player who comes at the advertised quarter to nine. She has to be sent about 20 minutes early, or the fallback has to wait longer than her walk.
2. **Should fix, #7: the .55 → .15 change would hit every musician on the ship, not just the Captain.** I measured it. On its own it barely moves the Captain (9.2 → 8.6 h a week in the music room, because her "music" habit is what pulls her there). It halves five other people's evenings, for example Mbeki 9.3 → 4.0 h and Ueda 5.8 → 2.4 h. Limit it to the Captain.
3. **Should fix, the tuning items (#16, #20, #22, #27) are planned one at a time, but they push on each other.** You get +15% task speed while energy is 75 or more and +10% while social is 75 or more (`NEED_FX`, line 12176). So #27 (less energy) and #22 (lower social) make every job slower, which partly undoes #16 (shorter repairs). The user should see the overall result (how long a Tier 1 repair really takes on a normal day, before and after), and questions pp-q9 and pp-q10 should say that jobs get slower.
4. **Should fix, #16: making Tier 1 two-thirds as long leaves a big jump at the first promotion.** A Tier 2 job would take 1.87× as long as a Tier 1 job, not today's 1.25×.
5. **Should fix, #26: a weekly Monday 19:30-20:15 tradition clashes with things already on the calendar.** It overlaps Gym club (19:15) on the very first Monday, and later the Wren talk (Mondays 19:00-19:40 from day 25), Book circle (20:15) and the Department cup (20:15). It should be a one-off on your first Monday (`when: arrival monday`, as Name on the beam already is), or moved clear of those.
6. **Should fix, #6: the owner is wrong and the question asks again what the user already decided.** Section 20 is the Social engineer's (plans/owners.md), so the Works career engineer would be building inside someone else's section and changing the shared `careerClockedIn`. The user asked for undo in so many words, so pp-q3 shouldn't offer "Confirm" or "only the double-tap fix" as the recommendation's rivals. The open question is how long Undo stays up.
7. **Should fix, #10: the planned fix probably won't stop the overlap the user saw.** A body is 0.4 tiles wide (`BODY_R` .2). A lane of about ±0.2 tiles leaves two people a typical 0.13 tiles apart, still mostly inside each other. A ±6% speed spread takes about 9 seconds on average to separate a pair, and pairs with close speeds take far longer. The lift-exit stagger (marked optional) or a "keep a gap behind the person ahead" rule is needed, with a pass mark measured by PP1's c10 probe.
8. **Should fix, #1: the red-haired technician stays in the Chief's chair.** With the fix, Marta Soto still sits at `5-office-1` (Calder's own chair, per the comment at line 7301) while Calder stands and says "Come in. Don't sit." The user noticed exactly that person. The desk swap, marked optional, should be part of #1 or put to the user as a question.
9. **Should fix, #19: the recommended beam time changes the most.** 16:45 inside the shift moves the Works crew's Day 1 (after-shift semantics, day_check, events_check, food_check's dinner queue). Option 2 (keep 17:05; Zeke keeps you in the bay from 16:50 and the dinner nudges wait) meets the user's "so players don't miss it" without touching the crew. The question should say which option changes less, or recommend option 2.
10. **Should fix, the page can't keep the user's answers yet.** It has 18 text boxes and 53 radio buttons but no script, so nothing is saved. Per the user's rule it needs the artifact's answer capability before it's published.

Everything else is a nit (below). Sizes: about 19 turns is fair. C is closer to 3.5-4 turns, and #3 is smaller than planned because the walk-over code already exists (line 40040-40046).

## How I checked

- PP1's probes re-run on a scratch work dir (`CADET_WORK` in my scratchpad, three r128, Chromium at 390×844): `b2_day2.py` (#1: the meeting opens at **08:56** with Calder absent, as reported), `c9.py` (#9: **130** toilet visits on Day 1, 116-152 a day over a week, every visit 3-6 min, as reported; Deck 4 has only two toilet places, `4-toilet-p1`/`q1`, which take 59 visits a day), `c7.py` (#7: Marrow on Deck 4 for 862 and 553 minutes in weeks 1 and 2, average **11.8 h** a week, matching PP1's 11.3; most of it on her days off, untagged leisure, which is the "music" habit), `b1_12.py` (#12: Zeke `esc: 'follow|19,4'`, `talking: 1`, `shuf: False` from 09:18 on, as reported).
- My own probe (`pr_music`, scratch only): every musician's music-room hours a week over Days 1-14, on the game as it is and on a copy with .55 → .15 at line 10185. The results are in #7 below.
- Code read for every item at the cited lines (all still correct at 2f8976c); owners checked against `plans/owners.md` and `tools/section.py --where`.

## Item by item

Ratings: **blocker** (the plan would ship a wrong fix), **should fix** (fix the plan before the user sees it, or the builder will trip on it), **nit**. "OK" means I agree with the cause, fix, owner and size.

### A. Day 2

**#1 (the Chief isn't in her office): cause right; fix has a blocker.**
- The cause is right. `introPlan` (line 10518) takes `cand` from `S.places`, and `schedData` (9222) puts `type: 'event'` places into `evPlaces`, not `places`. The office's other place, `5-office-1`, is a `work:works` desk, so `deskOf` skips it. That leaves no candidate, `placeId: null`, and she stays where she was. Reproduced: the meeting starts at 08:56 by the 10-minute fallback (`at + 10`, line 39873).
- **Blocker: the timing.** A named place makes `from = at - INTRO_EARLY` (5 min), so she leaves at 08:40 and, as PP1's scratch run shows, arrives at 08:54. The plan's new rule ("if she isn't there 3 minutes after you, the fallback runs") then fires at **08:48** for anyone who arrives on time at 08:45. That's the user's bug again. The fix needs a per-beat lead of about 20 minutes (her walk is 14), or a fallback longer than her worst walk. Note that `INTRO_EARLY` and `introPlan` are section 14 (the sim engineer's). A per-beat `early` field changes what `introBeats` hands section 14, which is a shared format, so it goes to the sim engineer first, not just "sim reviews".
- **Should fix: her block's length.** If the beat's `until` becomes 10:00 to match the new meeting window, Calder stands at `5-office-stand-1` from about 08:25 to 10:00 even when the meeting was over at 08:50. Either end the block when `d2-solo:met` is set (intro state, which introPlan may read, then re-planned through `introSig`), or say that standing for 80 minutes is intended.
- **Should fix: Marta in the Chief's chair.** The plan's own screenshot `01-probe-fixed-meeting.png` shows someone seated at the desk while Calder says "Come in. Don't sit." `5-office-1` is commented as "her chair" (line 7301). The user called out the red-haired person. Make the desk swap part of #1 (it's a crew change: day_check and cadet_test on Deck 5, so in batch D's style), or ask the user. Don't leave it optional and unasked.
- "Counted as work time": in the first week (`CAREER.grace` 7) being in a Works room already counts as at work (`careerAtWork`). Check that the Works Chief's office counts as one, and that clocking in after a 09:30 meeting doesn't trigger the late tip (`n.late >= 20`, `careerTip('late')`, line 37009). That's a nit if it holds.
- Standing, not auto-sitting: the user allowed "may auto-sit", and standing follows the line. OK, and the plan says so.
- Owner: onboarding (21), with the sim engineer as owner of the 14 part (see above). Size: 1 turn is fine.

**#2 (naming): OK.** My search found the same places. Also `content/home/jo.call:329` ("Your first job on your own") and `content/overheard/goodbyes.lines:48` already mean "solo", so they can stay. The plan is right that 39543's "Ten to eight" is wrong (the briefing is 08:50).

**#28 (laundry tip only 06:00-09:00): OK.** Line 12389 is exactly as described. The rest of the lesson (21b's `CLOTHES_BEATS`, `d2-laundry` 16:45-18:00) isn't tied to the morning, so the tip is the only gate. Nit: "awake and not clocked in" on a late wake (say 10:00) shows the tip straight away, before the player clocks in, while they're already late. The wording should not make them think laundry comes first. The second wording should cover that case too.

### B. The arrival evening

**#3 (Chief doesn't walk over): OK; smaller than planned.** The walk-over already exists: `calderGo` / `crewComeTo('calder', introSeat('calder'), …)` at lines 40040-40046 runs on "Look who's coming over". Since 0.71.3 she is already in that seat, so it does nothing. The change is mainly where she waits (a nearby, visible table instead of 0.42.64's far `away`), plus the existing `introCalderIn` start. Probably ½ turn. Keep the user's 0.71.3 point (she must be visibly at the dinner), as the plan does.

**#4 (green panel, not a bubble): OK.** The screenshot confirms it: "the green text at the bottom" is the dialogue panel (`04-evening-yours-in-panel.png`). `introSay` (39697) already says `walk.goodnight.n` as bubbles, up to 4 (39669), and `BUBBLE_MAX` is 2 (47596). Nit: hushing the crowd's chatter touches bubbles (8b, the performance engineer's). Name the section that emits overheard chatter so the right owner reviews it.

**#14 (device button): OK.** Nit: cadet_test hides `#devBtn`'s glow in shots. The new pointer element should be hidden the same way, or be absent at test URLs (the device is already booted there). Say which.

**#15 (laundry line): OK.**

### C. Training day

**#11 (tracked arrow blocks the intro arrows): OK.** `trkTap` (14919) never clears, and `introArrowTick` (39934) waits for any arrow that isn't its own. The fix is general and correct. Nit: list what "started with you there" means for each kind of tracked thing (meeting, tradition, appointment, job, place). A place has no start, so it should keep its arrow until you arrive.

**#12 (stuck on Zeke): OK.** `shuffleable` (13480) already lets a follow-mode escort shuffle; only `!(a.talking > 0)` stops it. Reproduced: `talking: 1, shuf: False` all morning. Nit: with `SHUFFLE_COOL` at 1.5 s and follow mode re-aiming at you, check that he doesn't step straight back into you (b1_12 with a hold-walk through him, 3 angles, should pass in under about 0.5 s).

**#17 (Zeke on your tile): OK**, with one note. `escortStep` (48728) in lead mode walks to `escortGoal`, the arrow's tile, and stops there. Follow mode already keeps `ESC_NEAR`. The tap-path part touches every tap; the plan gates it, which is right. Nit: if #10's speed spread lands first, keep the escort at his own pace (`e.pace`), not the spread, or the lead/follow distances shift.

**#13 (device tip wording): OK.** Nit: the tip is Day 1 only (`c.d === 1`). If you do no long hold on Day 1 it never shows. Let it wait for the first long hold on any day of the first week.

**#18 (end of training day): OK.** `? time:morning` is a supported condition.

**#19 (the beam): cause right; recommendation should change.** The arrow is `{ item: /^The beam$/ }` (34743), and `BEAM.slots[0]` is the right target. The .trad is already `when: arrival monday`, and its header says 17:05-17:40 was chosen so the crowd walks to dinner "inside the shift-change rush (food_check's queue, 0.34.54)". It also has `after-shift: yes`, so at 16:45 the crowd would only come as they clock off unless that rule changes too. PP1 notes this ("the Works crew come 15 minutes before clock-off"), but that's new behaviour, not just a time change. **Should fix:** pp-q15's recommendation has the biggest footprint (crew plans, day_check, events_check, food_check). Option 2 meets the user's aim with intro-only changes. Recommend option 2, or at least put the trade-off in the question. The arrow fix is needed either way.

### D. The crew's life

**#7 (Captain on Deck 4): cause right; the fix should be narrower.**
- My probe, hours a week in the music room (Days 1-14, average), today → with .55 → .15 for everyone: Marrow 9.2 → 8.6; Reyes 5.9 → 3.8; Dahl 4.3 → 3.5; Ueda 5.8 → 2.4; Mbeki 9.3 → 4.0; Larsen 5.3 → 3.4. The line is `H.has('musician') && U(102) < (thursday && captain ? 1 : .55)`, so it applies to every musician. **Should fix:** make it `captain ? (thu ? 1 : .15) : .55`.
- Dropping her "music" habit is what does the work. Her untagged Deck 4 leisure is mostly on her days off (Sunday Day 7: 467 min). Her habits are hand-set in `plans/crew-roster-gen.py` line 69 (the plan says "roster generator": right file, but it's a data edit). Regenerating must change only Marrow's row. Check the diff, since the generator also uses habits for gift tags (`TAGS_OF_HABIT`) and the habit-change stories (line 290).
- She will still pass through Deck 4 for laundry (Saturday 18:56-19:39) and its toilets. Count those in the "3-4 h" estimate.

**#9 (toilets): cause right; fix needs two details.**
- Confirmed: `take`'s `arrive` adds travel only for a deck change (`dk !== deck ? C : 0`), and `toilet()` asks 3-6 min. PP1's c9b uses a Manhattan distance on place tiles, which is a fair estimate.
- **Should fix (determinism): name the distance.** The planner plans every deck while only one deck's grid is loaded. So "fixed map distances" should be a pure function of the `DECKS` place data (Manhattan × a detour factor, or a table made at load with no `R()`), never `crewPath` on the live grid.
- **Should fix (capacity): hold the stall from arrival, not from leaving.** Deck 4 has two toilet places taking about 59 visits a day. If the hold includes the walk, each visit holds a stall about 13 min instead of 4.5. At the 06:00-07:00 and 22:00 peaks the `wait: 4` will fail more often and visits will be dropped, which works against the fix. Re-run c9 after the change, and count both reaching and taking place.
- If #10's speed spread is built, the lead should use the slowest speed.

**#10 (walking inside each other): cause right; fix likely too weak (should fix).** The arithmetic is in point 7 of the summary. Make the lift-exit stagger part of the fix (that's the user's exact case: "who leave the lift together"), or add a simple rule: a walker closing on a same-way walker ahead within 0.45 tiles matches their speed. Both are frame-only and deterministic under the test clock. Set a pass mark with c10, e.g. no pair within 0.3 tiles for more than 3 real s. More nits: the lane offset turns 90° at corners, so ease it or the drawn body jumps by about 0.28 tiles; check `bubble_check` (bubbles follow the drawn body). Keep the offset at doorways as well as walls. The player's bump test uses `a.x`/`a.z`, not the drawn offset, so up to 0.2 tiles of "invisible" body; that's fine, but say so.

**#8 (stall light): OK.** Nit: instead of a separate green and red piece per stall (an extra draw call each, always), leave the merged green as it is and add a red cap slightly proud of it, not coplanar, shown only while the stall is taken. That costs draw calls only for taken stalls in view.

### E. Small features

**#25 (lift label): OK.** Nit: the other names are in sentence case ("Officers' quarters and science", "Commons"), and the user wrote "Officer's Quarters - Science" in title case with a hyphen. pp-q1 asks about the apostrophe only. Add capitals and the dash to the same question, or say the label will match the others' style.

**#21 (rank on the card): OK.** `ROSTER_RANK` puts `senior` and `officer` at the same level. The words table keeps them apart, which is fine.

**#6 (clock): cause right; owner and question should fix.**
- Owner: section 20, lines 35934-38264 by `section.py`, is the **Social engineer's** (owners.md row `20`). The clock was written by the career engineer, but under the owners rule, a 1-2 turn feature in section 20 that changes `careerClock` and how the shared `careerClockedIn` (used by 14, 19, 15, 21) reads goes to the Social engineer first. Either the Social engineer builds it, or the lead assigns it to the Works career engineer with the Social engineer's sign-off on the design. The plan has the Social engineer only reviewing.
- Design: "nothing counts until it's gone" would leave `careerClockedIn` false for the Undo window, so the intro's job-board arrow, the Schedule and section 14's at-work all lag. Better: apply the punch at once, keep a snapshot (`ci`, `co`, `on`, `clockLog[d]`), and hold back only the side effects (`repAdd` −2, `careerRemark`, `simNote('clock')`) until Undo expires. Saving during the window must not lose the snapshot (or the window simply ends on save).
- **Should fix: pp-q3.** The user's note says "add a way to undo a clock-out (and clock-in) right after punching". Undo isn't in question. Ask how long it stays (a few seconds, or until you walk away from the clock), and keep the double-tap fix in every case.

**#24 (shop menu): OK.** Nit: four seats (15, 20, 19, HUD) for 1-1½ turns means a lot of hand-offs. Name one builder, with the others as reviewers.

**#5 (ladder): OK, one gap.** "Paths and crew routes don't change" is true for decks that already have a hatch. Deck 5 has none ("only glass"), so a new hatch there may take a walkable tile, and then Deck 5's paths, deck_check and the crew's routes change. Say whether it takes a free tile or a wall slot, and add deck_check and day_check for Deck 5. The pp-q5 framing ("the Reactor sealed for safety, not rank") is fair to the user's "no more tiered access".

**#26 (one more tradition on Day 1): should fix, see point 5 of the summary.** The clashes: Gym club 19:15 (Day 1 itself), `rec-wren-talk` Monday 19:00-19:40 from day 25, `book-circle` 20:15 every two weeks from day 8, `department-cup` 20:15 week 4, `lantern-walk` 20:30 in its season. A weekly new tradition also changes every Monday's crew plans for good. `when: arrival monday` keeps it to the player's first Monday, with no calendar clashes after week 1, and day_check only differs on Day 1. Put that choice in pp-q2. The plan doesn't say weekly or one-off.

### F. Tuning

**#16 (Tier 1 repairs): numbers right; should fix the tier jump and the interaction.**
- `jobMins` is only used for you (13980, 11498); the crew use `JOB_TYPES` directly (17397). So "you only" is right.
- A 0.67 factor on Tier 1 only makes Tier 2 (×1.25) about 1.87× Tier 1. The first promotion would suddenly almost double repair times. Either scale the base `work` for you, all tiers, or ask the user about the step.
- The job board's minutes (section 17, line 18300, `JOB_TYPES[...].work × tier`) are the systems engineer's. If they're shown to you anywhere, they need the same factor, so add the systems engineer as reviewer.
- Career pace: if jobs aren't limited by supply, shorter repairs mean more jobs a day, which means faster reputation, credits and `careerSpeed` skill. Dev mode's "Set career" table ("what a steady player has by that day") would then be out of date. Say whether jobs a day is limited by the board, and if not, tell the Dev mode owner.

**#20 (hunger): OK.** Nit: define "while working" (clocked in, or in a work step). A player who skips breakfast (starting at 60 in a fresh game) reaches "Hungry: tasks 15% slower" (<25) by about 13:30 at 7/h. That's probably intended (it pushes lunch), but the question should say so.

**#22 (social): should fix the question.** Today social sits at about 95, so most players always have "In good spirits: tasks go 10% faster". At about 12 a day falling, that bonus is gone from Day 1 evening on a quiet week. pp-q9 must say that jobs get about 10% slower when you keep to yourself.

**#27 (waking energy): should fix the question.** Energy drains 4.8 an hour, so waking at 90 instead of 100 ends "Well rested: tasks 15% faster" about 2 hours earlier (around 09:10 instead of about 11:15). That's most of the morning shift. pp-q10 should say so. Together with #22, a typical work day's task speed drops by roughly 10-20%. Show the user the net Tier 1 repair time after all four changes, not 30 min in isolation.

**#23 (large-group moments): OK** as a note for the events plan.

## The questions

- pp-q1: add capitals and the dash (nit).
- pp-q2: add "one-off on your first Monday vs weekly", and move off 19:15-20:15 or say how it fits with Gym club (should fix).
- pp-q3: re-asks a decided point. Ask how long Undo stays instead (should fix).
- pp-q5, q6, q11, q12, q13, q14, q16, q17: fair, and the recommendations are sound.
- pp-q7: add the Tier 2 step (should fix).
- pp-q8: fair (nit: mention the skipped-breakfast case).
- pp-q9, q10: must mention the task-speed side effects (should fix).
- pp-q15: recommend option 2, or show its smaller footprint (should fix).
- New question needed for #1: the office desk (Calder's chair), unless it's made part of the fix.

## Dropped or changed from the user's notes

Nothing is dropped. Where the plan changes something, it says so: standing instead of sitting (#1), the Reactor staying sealed (#5, put to the user), and #23 as a note, not a build item (as the roadmap says).

## Smaller things in the plan itself

- The HTML says "Five batches" while listing A-F (six). The `.md` says six.
- Batch C is about 3.5-4 turns by its own item sizes, not 3. #3 is likely ½ turn, not 1 (the code exists).
- The page has no script and no answer capability, so it needs one before publishing (the user's rule).
- Backlog #15 (lowercased name in the goal arrow): confirmed in `17-tour-overlap.png`'s label. Fine as a backlog row.
