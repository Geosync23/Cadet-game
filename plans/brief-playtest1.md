# Playtest update 1 brief (0.63.2) — lead 13, session_015UkCGSS9FyGoBdkePhrKbC, 2026-10-18 ~17:00 UTC

The user played the Pillar 5 preview and sent 33 notes. The plan (8 packages) and the user's answers are in the survey https://claude.ai/artifact/XpPc16Z2mB2fVHsraR6STk; everything below is APPROVED by the user and is the spec. This update ships as combined build **0.63.2** on top of Step 2 (0.63.1), before Pillar 5 Step 3 (which becomes 0.63.3). Holidays are ON HOLD (the user, ~16:51): nobody builds or plans further on them.

**Every seat reads, in order:** CLAUDE.md; this brief (on `claude/lead-pillar1`: `git fetch origin claude/lead-pillar1 && git show origin/claude/lead-pillar1:plans/brief-playtest1.md`); DEV_NOTES.md ("Rules that keep it working", "Testing", the build table); plans/brief-p5.md (the Pillar 5 working rules, which still apply); your predecessor's handover note if you replace someone.

- **Base:** the 0.63.1 candidate, `claude/p5-cand-s2` (head cb7d30a or newer; the build master tells you the final hash; merge it when it does). Your own branch is named in your package.
- **Rules (unchanged):** small exact-string edits, never rewrite the file; determinism (no `R()` in shared kit at load; anything that must "feel random" is seeded from the save's seed, so it differs between new games and is the same for one save); phones first (`col()`, no coplanar faces, watch draw calls); every new saved field loads old saves (a default) and gets a round-trip test; bump the HUD build number in your seat's series and add a DEV_NOTES build-table row per turn; quick checks for what you touched; cadet_test differences explained.
- **Series (new seats):** traditions T = 0.70.x, crew sim X = 0.71.x, HUD U = 0.72.x. Existing seats keep theirs (O4 0.42.x, W 0.48.x, P 0.28.x, C 0.44.x, A 0.47.x).
- **Report to lead 13** (send_message to session_015UkCGSS9FyGoBdkePhrKbC): one line when you start; one per finished piece (hash, build number, what, checks); at once if blocked or a design call is needed. No narration. Send each finished piece's hash to the build master BM5 (session_01DbBJ7iK6TrrADyEw7qbCsQ) and the reviewer R2 (session_01DZoxp9pxhp63Wye1Kr2MsZ) too.
- **Coordinate sideways** directly with the seat that owns code you need (ids below). A design gap → lead 13.
- **Never** contact the user, start sessions, or push outside your branch.
- **Memory:** tell lead 13 at ~60%; at ~70% write `plans/handover-<seat>.md`, push, stop.

## The user's answers (binding)
- **Work starts 09:00** for the whole day shift: 09:00–17:00 (was 08:00–17:00). Breakfast, the time clock window and Day 1's briefing move to fit.
- **Tea:** the 13:00 tea and biscuits REPLACES the 10:30 Works tea (all lines and pages that say "half ten" change). Interactive: once tea is out, when you finish a job the arrow points to tea and biscuits; you can drink and eat (slight hunger help), or dismiss the arrow and keep working. Many Works crew go, staggered, not all at once. On Day 1 Zeke explains it, then leads you there after your job (tracked + arrow), then work goes on with Zeke following and chatting.
- **Zeke "still walks and talks":** he may walk and talk on the tour (the user, ~17:12, no clock pause), but stops and faces you for the greeting and the cabin hand-over, keeps you beside him. Each line stays up long enough to read, and his first lines wait until you've reached him.
- **Bunk:** the game already gives the right bed (upper, middle of three = 2nd from left); only Zeke's words are wrong ("top bunk at the back").
- **Cabin talk:** Zeke hands you the device ("This is yours…") and says a few lines; the rest becomes Mail from Zeke, which he tells you to open. Every "locker" in his talk/Mail becomes "wardrobe".
- **Name on the Beam:** for you on arrival and for each new Works member who joins later (rotation arrivals).
- **Gym club vs Lap of the Wren:** Lap of the Wren moves to a quieter evening (not Monday).
- **Sunrise stretch** moves to the garden.
- **Evening light:** the dimming and the night a little brighter (not before 20:30).
- **Seated arm-waving:** seen everywhere except the mess hall.
- **Spice shelf supper:** keep 18:15; make the crew finish work on time.
- **Talk while eating:** sitting down near people gives a slight social bump; you may also "Talk a while" while eating, with ONE tidy combined meter (no stacked meters).
- **Tracked button:** in this update.
- **Tap to join:** for every tradition where there's something to do together (not all): tap the leader or any participant to join; you then do the activity with them automatically. Clear signs: on arrival the tracking arrow points at the leader, the leader has a marker over their head, and a tip says e.g. "Tap Tomas to join the lap". Traditions where you just turn up (a toast, the quiet watch) stay as they are.

## Packages (seat → items; note numbers from the survey)
**O4 onboarding (session_01MeEsh5sp4RyuD7KwdQEbLC, branch claude/arrival-0607b → push to claude/onboard-pt1), with W for lines:** Zeke: a plain first greeting; "Works Department" in his first tour lines; stop-and-talk, readable pacing, lines wait until you reach him (`INTRO_TOUR`, `introTourTick`, `INTRO_TOUR_GAP`); Day 1 training-day opener ("training day… I'm with you all day to help"); "Don't worry, jobs will get better as you go"; "you can't do every tradition in a day, you choose" (Zeke, replacing/alongside tip `t:eve-trad`). Cabin: hand over the device, the rest as Mail from Zeke he tells you to open; show the wardrobe ("this is where you get clean clothes"); Day 1 tip: fresh clothes from the wardrobe + do laundry when you can; bunk wording. Day 1 arrows: to the time clock when told to clock in; to the job board the moment you've clocked in; to the food / queue the first time the chief tells you to eat. Zeke's Day 1 tea explanation and walk to tea (with X's tea schedule and P's tea activity).
**W head writer (session_013DdpJv4AKFJcvuBBqjSXms, claude/writer-p5):** all new and changed lines: Zeke's above (incl. his device Mail), "locker" → "wardrobe" everywhere in Zeke's content, 08:00/"eight till five" → 09:00/"nine till five", "half ten" tea → 13:00 tea and biscuits; NEW unique crew lines for crew coming up to start a conversation with you (several per friendship level, clearly addressed to you); tap-to-join tips and join notices for each tradition T lists; Name on the Beam lines (tell you to tap the beam; everyone congratulates you).
**P player (session_0153WUGRakJnNzUCNNHf1E8X, claude/player-p5):** toilet lowers hygiene a little + tip to wash hands + a new wash-hands activity at the basins; talk while eating (one combined meter) + slight social bump when you sit near people; need very low → arrow (and tip) to the nearest place that fixes it; push against someone 2 s → you pass through briefly (Zeke included, escorts too); taking a job tracks it (`take()` must clear an older `IX_GOAL`); the tea and biscuits activity (drink/eat, small hunger help) and its after-job arrow with a dismiss.
**U HUD engineer (NEW):** the "Tracked" button and panel: everything on or coming up (traditions, appointments, your jobs) + fixed places (job board, your bed, the call room); tap to track (the goal arrow), tap again to stop; device app labels (Schedule, Calendar, Settings, Settling) a little smaller so none wrap. Branch claude/hud-pt1.
**T traditions engineer (NEW):** the tap-to-join mechanic (shared, so holidays can use it later): go through every tradition, decide which have an activity to do together, and add join + automatic activity (Lap of the Wren: everyone walks the lap in one line with you; Sunrise stretch; Gym club; Cook-along; Lantern walk; …), the leader marker, arrow to the leader, the tip; a clear join notice (what it is, what to do, what it gives: social / leisure); the tracking arrow clears once you've joined (`eventsPlayer` → `clearGoal()`); Lap of the Wren off Monday to a quieter evening; Sunrise stretch to the garden; Sunday dinner's extra tables go away afterwards (`DECK_DRESS.longTables`/`messExtra`, `tradDecor`); Name on the Beam: told to tap the beam, name goes up on tap, all names first names, congratulations then disband, held only when a new Works member joins (you on arrival, later rotation arrivals), room left on the beam but readable (beam model with A5). Branch claude/traditions-pt1.
**X crew sim + social engineer (NEW):** crew "calling out" become crew who walk up, stay beside you and start a conversation (`socialSeek`/`seekShow`), timing seeded per save; crew stuck on you while you sit in the mess hall (`occupiedBy` / the block check); the crew's day shift 09:00–17:00 (with C2) and crew finishing work on time (Spice supper); the 13:00 tea and biscuits in the Works room for Works crew, staggered, replacing the 10:00–14:00 random tea breaks for Works. Branch claude/crew-pt1.
**C2 works career (NEW, replaces C at 63%; reads claude/works-career 90f0916 plans/handover-works-career.md and S's plans/handover-systems.md):** the shift move to 09:00 in the career/clock code (`DAY_SHIFT`, `shiftStart`, the literal 480s, the time clock window, `INTRO_WEEK` briefing time) — coordinate the crew side with X and lines with W; a few more jobs on the board now that crew take jobs too (you still get about 3–6 a day). Branch claude/works-career.
**A5 deck architect (session_01CHRbUTZc18m7eBck8eWhXj, claude/deck-tern2 → push playtest work to claude/deck-pt1 based on 0.63.1 + Tern pass 2):** poses: exercise bike pedals the right way (`ACTS.cycle`); bench press gets its own animation (grab the big bar, press) instead of 'lie:lift'; find and fix the seated arm-waving pose (everywhere but the mess hall; likely 'sit:talk'/'sit:drink'); evening dimming + night a little brighter (`nightAt`, `NIGHT`); the beam's room for names (with T); Sunrise stretch's garden spot (with T). Tern pass 2 (484f160) rides in 0.63.2.
**BM5 build master:** after 0.63.1 is published, combine 0.63.2 on claude/p5-cand-pt1 in merge order: C2, X, P, O4, T, U, A5, W. Full check set incl. intro_check --week and day_check (09:00 shift).
**R2 reviewer:** reviews every piece (behaviour and saves in depth; lines and tests skimmed).

## New seats (started by lead 13 ~16:53, depth 4)
| Seat | Session | Branch | Series |
|---|---|---|---|
| T traditions | session_01X4SZJFeHprDF21NZqU5fGi | claude/traditions-pt1 | 0.70.x |
| X crew sim + social | session_01SNaWA6X5E9i2ZKfMnPTHJf | claude/crew-pt1 | 0.71.x |
| U HUD | session_01FcMPTX7mMTHkyr4pxDfNcS | claude/hud-pt1 | 0.72.x |
| C2 works career | session_014yREkgPvuwMyxBtoqB1P14 | claude/works-career | 0.44.x |
| O5 onboarding 2 (Day 1 arrows + tea walk; O4 keeps pacing/greeting/cabin, pushes to claude/arrival-0607b) | session_014y2M5qmkjuLdHK6K1JsqKD | claude/onboard-pt1 | 0.42.x after O4 |

## Added by the user ~17:00
- **Call home tip, first night (O5 + W):** Day 0, after meeting the chief: a tip to call home with a "Track it" option; once you reach the booth the tracker goes away and the default goes back to pointing at your bed.
- **Lap of the Wren (T):** Sunday 20:30, but not on the Sunday you arrive (Day 0); the first is Day 7.
| BM6 build master (0.63.2 combine + full run; BM5 at 60% handing over) | session_01F8k6hqdBRoxDJMzqAuiHqR | claude/p5-cand-pt1 | 0.63.2 |
| R3 reviewer (R2 retired at 70%) | session_01AR6tGFiSZF7hL1LfVpWgng | claude/reviews-p5-step2 | — |
- **Watch a film hobby (the user ~18:33, U + W):** a new hobby on the personal device, same as reading (same pose), new button and text. Rides in 0.63.2 if ready before the final run.
- **Flickering speech bubbles (the user ~18:36, seen on 0.63.1):** DA5 investigates and fixes at the root (with X / O4 / O5 if theirs). In 0.63.2.
- **Film hobby:** confirmed by the user for 0.63.2 (BM6 waits for it).
- **Bubble flicker** happens all over the ship (the user).
- **Day 0 auto-sit at the Chief's table** stopped happening on 0.63.1 (the user, ~18:38): O5 restores it + an intro_check assertion. In 0.63.2.
