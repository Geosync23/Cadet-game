# Review of the Dev mode jumps plan v4 (DM1)

CA1 for lead 43, 2026-10-28. An adversarial technical review of `plans/devmode-plan.html` / `.md` on
**claude/devmode-plan-2 cd43ba6** (page version 2, https://claude.ai/artifact/X2GVBU4c5hZdt1R3dNxqy4), built on the user's
v2.1 and v3 answers. (An earlier pass read fa0c1fa by mistake; everything measured there holds for cd43ba6, which keeps
the same runner and jumps and adds the agreed Stop 3 tools: threads − and +, End and undo, End and keep. F8 and F9 are
about those.) Read and run only: no game or check change.
Game read: 0.95.0 (the plan's base, claude/staging-pad, has the same game file). Runs: headless Chromium, 4 cores, the
real Set career code (`devmodeSetCareerTo`) under `devmodeRun`, `#dev` with the arrival marked done; probe scripts in
CA1's scratchpad (not kept).

## Verdict: FIXES

The idea holds up: a jump built as Set career plus a landing does reach the late game, every ship-wide event happens on
its own calendar day, the ending can be driven through the game's own functions, the real save is never touched, and two
runs give the same save byte for byte. But four things must change before building (F1-F3, F8), and five should (F4-F7, F9).

## What I measured

| Run | Result |
|---|---|
| Set career to Day 26, twice | 12.1 s and 11.7 s; the same save both times (sha256 cb73608609a7…, 113 KB); Engine Specialist, Calder's question settled for Day 26, nights 22-24 counted; events run: Line (Day 6), ion storm (Day 11, bumpy), comet (Day 22); no page errors |
| Set career to Day 36, twice | 15.4 s and 15.3 s; the same save both times (eecb36c5e6ea…, 116 KB); events also: the vessel (Day 27), the crossing back (Day 31); no errors |
| Day 36, CPU slowed 4 times (a phone stand-in) | **65.5 s** |
| The ending path, run as the plan's runner would (Day 26; `cqAnswer` at 19:10; on to Day 32 16:40; `endOfferDone('room')`, `endSay('go')`; on to Day 36 06:00) | 13.1 s; the offer met, Go said Day 32, **settled Go on Day 35** at the address; no errors |
| Plain Set career to Day 36 (no answers) | the offer booked for Day 32 but **never met, nothing said, nothing settled** |
| `W.ms` (your milestones) across that run | after `cqAnswer` on Day 26: `mentor, nights, question` added; **gone again on Day 32** (the next morning's career re-set) |

## Must fix

**F1. The runner wipes what the game wrote on the way.** `devmodeCareerSet` runs every morning and does
`Object.assign(W, devmodeCareerFor(n))`, which replaces `W.ms`, `W.tr`, `W.pu`, `W.done`, `W.tools`, `W.op`, `W.use`,
`W.home` and `W.test` with the table's. Today that's harmless because Set career stops at Day 30 and nothing plays on
the way. A jump past Day 26 does play on the way. Confirmed: the `mentor`, `nights` and `question` milestones that the
mentoring and Calder's question write on Day 26 are gone by Day 32. The Works app's career page reads them (24 core,
line ~58078) and so does Calder's question page (`cqPage`, ~67285), so a landing at the offer or the goodbye shows a
career with no nights, no mentoring and no question. Fix in J0: after the table's last row day (today Day 26), stop
re-setting the career; or keep the game's own entries (merge `ms` and `done`, keep any `tr`/`pu` key the table doesn't
name). Add a check line: a Day 36 jump still has `nights`, `mentor`, `question` in `W.ms`.

**F2. The answers must be put in by the runner, at their minute, and J0 must own that.** Calder's question is asked at
the tea (about 19:05-19:30 on Day 26); the offer is from Day 32 16:00; the answer is said by Saturday 20:00; it settles at
the Captain's address on Day 35. Set career skips a whole day at a time (to 05:00, then the career re-set), so a call made
after the run is too late (the address has already passed with nothing said). The plan's `devmodeJump({ ..., answers })`
names the field but not the mechanism, and gives the answers row to J3 while J1's Calder's question landing and J3's
ending rows both need it. Fix: in J0 the runner takes a list of `{ at, fn }` stops (absolute ship minutes) and pauses
its day loop there (`devmodeSkipTo(at)`, then `fn`, then on); the answers live in J0's state with their defaults
(`DM_UI.ans = { cq: 'engines', offer: ... }`); J3 only draws the row and adds rows that read it. Then J1 and J3 never
edit the runner. My run above is that mechanism by hand, and it reaches a settled Go on Day 35.

**F3. Plain Set career past Day 32 lands in a state no player can reach.** Measured: with no answers the offer is booked
for Day 32 but never met (in play Calder comes to find you and it is "never missed"), so Days 33-40 have an open offer
nobody heard. With the plan's default answer Go, a Set career to Day 37-40 would be past the end of the game (the Tern
leaves on Day 36). Fix: plain Set career beyond Day 32 uses the same runner stops with **Stay** (or the answers row, with
Stay for Set career and Go only for the ending's Go jumps), and the panel says which answers were used. Set career's new
range (to Day 40) then means "the endgame, staying on".

**F8. End and undo has nothing to go back to, and the event starts again.** In 3.1 the event was started by Dev
mode, so "undo" was the Undo copy taken just before that start. In v4 the event starts on its own inside the jump's run,
so there is no saved moment "before it started"; Undo my last Dev action goes back to the Dev game before the jump. And
ending a run without logging it doesn't stop it: the calendar's next event is the first one not in `SHIP.eventLog`
(`evCalDue`, ~47775), so on the next tick `eventAdvance` starts the same event again. `EV_SKIPPED` is rebuilt at load from
the log and the start day (~47748; the vessel adds to it at run time, but that isn't saved), so a skip added by Dev mode
would be lost on the next reload. Fix, pick one before J2: (a) End and undo = the Dev save from the morning of the
event's first day, kept by the runner when the jump passes it (one more record of about 116 KB, inside `DM_ROOM`), with
the event then running again as the calendar says, and the panel saying so; or (b) a saved "skipped by Dev" mark that
`evSkippedFor` reads, which is a change in section 18 (the events base's owner, EC1) and breaks v4's "no hooks in other
sections"; or (c) drop End and undo and keep End and keep, Next phase and the threads. I recommend (c), or (a) if the user
still wants it: (b) touches the calendar every later event depends on.

## Should fix

**F4. Long jumps are about a minute on a phone. The user already answered this.** A Day 36 jump is 15 s here and 65 s
with the CPU slowed 4 times (the factor the parked replay measured for phones). That's over the plan's 30 s line, so
question 6's fallback (start from an earlier Mark) would come into play. But the user answered this kind of question on
the v2.1 page (question 13, "Is a first long jump of a few minutes on a phone acceptable?": **ok**, with a progress bar),
and on v3.1 chose the lean Dev mode and parked the replay's kept days. Recommendation: drop question 6's Mark
fallback (it brings back the parked kept days' complexity, and a reloaded save then run on is not proven byte-identical
to a fresh run). Keep the progress line Set career already has, add a Stop, and tell the user "about a minute on a phone
for the ending's jumps".

**F5. Check time.** Each jump is a whole fresh run: about 12-15 s each here, plus about 10 s to load the page. `beats` has
about 16 jumps, `events` about 18 (each also run twice for one jump and Undo), `ending` 6 jumps times the answer
combinations (3 offer answers and 4 Calder answers). That's about 4-6 minutes per part on a runner, more on a slow one.
Fix: J0 measures a whole part, not just one jump, and lays down the stubs as halves (`events1`, `events2`; `ending1`,
`ending2`) so a part can split without editing the shared part list later. Run the answer combinations from the Day 26
landing (one fresh run, then the four Calder answers each from an Undo or a Mark taken there), not as 12 fresh runs.

**F6. Missing jumps.** Not in the list but in the game and worth a tester's time:
- the power and relays lesson (M19, Day 17, 11:00);
- the sensor array's training (M20, Day 19);
- the old mysteries board (Day 21);
- the first crew rotation (Day 21);
- a Short Friday's 15:30 clock-out and the Captain's Friday address (18f, every Friday from Day 5; not a tradition, so the Traditions tab can't reach it);
- the slower career's ending (Calder's question on a later Friday, so the offer comes a week on). The plan rules it out, but it's a real branch with its own lines (`endSlow`, `endingAsk.slow`). Suggest one jump that sets the career a week slow.

**F7. Fit with the user's earlier answers.** (cd43ba6 already lists the 20 October answers as decided and keeps them; this point is only about size.)
- On v2.1 the user wrote "I'm questioning the need for this much complexity. I want to be able to test the traditions and career progression" and "Would it be easier to select a day and just add tradition testing?". v3.1 then went lean.
- v4 is 40 jumps and about 20 hours. It is built on the lean Set career, not the parked replay, which fits. But the page should say plainly that it is the larger option.
- Offer a smaller first cut: the Career and Nights groups, the ending's three landings, and one jump per ship event (about 12 hours). The rest can follow.
- Don't reuse the parked names (`DEV_PLAYER`, "kept days"), as the user's rule says.

**F9. The running-event tools need two guards.**
- **The threads' − and + stop counting at the storm's all-clear.** They go through `eventScore`, which ignores changes once `e.mine.settled` is set (~47092). So the buttons must grey out after that, or the band won't move and the check's "threads − and + change the band" fails late in the storm.
- **After End and keep, the crew's plans for the rest of the day still have the event in them.** Today's plans were made with the event running. Make that day's plans again and refill the deck, the way the Traditions tab already does (`devmodeTradsAgain`), and check that nobody heads for an event meeting that's gone.

## Checked and fine

- **No R().** Section 25 and the functions a jump calls (`newGameStart`, `introSkip`, `skipTo`, `devmodeCareerSet`, `cqAnswer`, `endOfferDone`, `endSay`) don't call it. The career seed is fixed (`DM_SEED`, no sick day before Day 46, so Day 40 is safe).
- **Save-safe.**
  - Everything goes to the Dev keys. The ending's kept copy is `SAVE_KEY + '-before-end'`, which carries `-dev` in Dev mode.
  - The end page's Start a new game opens the Dev slots.
  - A Day 36 Dev save is 116 KB, so Undo, Mark and the save fit easily inside `DM_ROOM`.
- **Events on their own days.** The run log shows the Line (Day 6), the storm (Day 11), the comet (Day 22), the vessel (Day 27) and the crossing back (Day 31), each played without you and finished. So jumps into them are the real events. `eventFinish` is ready for End it now.
- **Shared lines between J1-J4.**
  - Separate blocks, with J0 owning `DM_TABS`, `DM_LATER`, `devmodeDraw`, `devmodeSet` and `DM_CAREER`. That holds, once F1 and F2 are also J0's (both are in `devmodeCareerSteps`, which no later turn should touch).
  - J3's one line in `devmodeTrad` touches no other turn's lines.
  - J4's DV block (the career arrow, ~72100-72180) is apart from J1-J3.
- **The controller waves (plans/controller-audit.md).**
  - No clash. Wave A adds the Dev card (`.hud`) to section 26's screen-edge list. The new rows and tabs are plain buttons in `#dmSheet`, which the pad already reaches.
  - Go's two taps (`devmodeTwice`, 4 s) work with A pressed twice.
  - Small point: the rows say "Tap Go twice"; with a pad in use that could read "Press Go twice" (Wave C's words pass can take it).
- **The planner rule.** The runner's stops call the game's own functions. The records they write (`W.end`, `SHIP.end`) are the ending's own design, read the way they are in play. The existing mentoring shortcut's `SHIP_DAYS.delete` is the pattern for any landing that settles a day's record.

## Answers I'd give to the plan's questions

| Question (cd43ba6) | Answer |
|---|---|
| 1. Events: jump to their day, plus the running tools | Yes; but End and undo as F8 says |
| 2. Diplomatic visit | Not yet |
| 3. Answers row | Yes, but Stay for plain Set career (F3), and the row's state is J0's (F2) |
| 4. First week in J0 | Try it, but expect the arrival's records to need the play-once recipe (v2.1's reviewers found the Day 2 meeting needs the arrival played) |
| 5. Arrow at event meetings | Yes |
| 6. Slow jumps | Already answered by the user (F4): progress and Stop, no Mark fallback |
| 7. Builders | Three side by side after J0, with F1, F2 and F5's stubs in J0 |

Rank by hand for Senior Officer and Engine Specialist (J0, following the user's 20 October answer): fine as long as it
stays marked approximate. A rank set by hand skips the records later pieces read (the Tier 3 and 4 test records in
`W.pu`, the Deck 2 move), so the panel should point to the rank buttons for anything past Day 16.
