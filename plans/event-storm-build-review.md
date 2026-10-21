# The ion storm update: adversarial build review (before S10)

Reviewer ER2 (session_01S8pboNujAzZgMSWFK84CxD), 2026-10-21. Branch `claude/event-plan-review-2`.
Build reviewed: `claude/storm-update` 347c573 (S1-S9; f32d901 plus EV4's handover note), builder EV4. Reports to lead 23.

## Round 1: PASS WITH FIXES

**How I tested:** headless Chromium at 390x844, which draws every frame like the checks do. I used a copy with
`EVENTS_ON = true` (so `EV_STORM_ON` is on) and a new game, played as a player would: I skipped to each beat, went
to the deck, stood beside the person and stepped real frames. Probes are in my scratchpad, not pushed.

### Off: identical
cadet_test, with the merge base 394182b6 as old and 347c573 as new: **ALL IDENTICAL**, with no errors on either side.

### The story plays end to end (story A, "Sixty by lamplight")
- **Friday 17:40:** in the galley beside Lukas, `moment:stormLukasFri` opens. His first line follows your cabin ("hi.bunk"
  or "hi.moved"). Reply 0 sets `wants:stormLanterns` ("Lanterns are in Deck 5 storage. Bring all of them."). His fallback
  Mail is marked but not sent, because you met him (`unless: 'story:fri'`). When you don't meet him, "Sixty" arrives by
  Mail as planned.
- **Saturday 15:05, reply 1 (the errand):**
  - Brennan is found on Deck 4 at leisure, and `stormBrennanErrand` plays, ending "it's his galley tonight" (the guard
    rail is kept);
  - back in the galley, Lukas's bubble plays, and `story:errand` reaches 3;
  - at the supper (18:25, in the mess), `stormLanternBrennan.asked` plays: "Low and slow, lid on. He listened. Nobody
    listens, love."
- **Saturday, reply 0 (fix it):** `storm.lukas.fixed` is set, and `stormRange` is posted and claimed by you.
- **Left alone:** the crew do all the prep jobs, and the storm ends **bumpy**, as planned. The Monday debrief "Ion storm:
  how it went" arrives, and so do the gists of missed meetings (the briefing notes, the all-clear notes).

### Crowds and draw calls (390x844)
| Moment | Crowd | Draw calls |
| --- | --- | --- |
| Lantern supper, Sat 18:25, the mess | 54 planned (22 of them standing at crowd spots), within the 60 cap | 272 |
| Party, Sun 19:40, bow lounge | 25 there at once (34 seats; the rest drop in), within lead 22's call | 344 |

Both are under 450.

### Calendar
- Day 14: the party at 19:00; talent night is gone, and the Lap of the Wren is dropped.
- Day 15: the Lap of the Wren at 20:30 with Tomas, alongside running and book circle.
- The event ends with Day 15. `SHIP.event` is empty on Day 16, and the log reads `["ionStorm", "bumpy"]`.

### Fixes
1. **The S10 gate: bigevents_check must pass first.** EV4's note says it still FAILs on the party ("53 people for 34
   places", counted over the whole evening). EC1 must count the people there at once for a gathering with `stay`. My
   own count is 25 at once, so the build is right and the check is behind. **S10 waits for a clean bigevents_check.**
2. **S2 isn't built, so S10's order needs saying.** S2 takes the Captain and Vance off the double shift for Day 12's
   address. It waits for claude/fridays to reach claude/integration.
   - If the storm is switched on before Fridays lands: no address, as today, and that's fine.
   - If Fridays lands first: both speakers are stuck on the bridge at 16:00.

   Put the rule in DEV_NOTES and the S10 brief: Fridays and S2 together, or S2 before Fridays is switched on. Use
   FR2's minutes (Marrow off from 15:30, Vance from 15:45, through 16:50).
3. **Lukas's moments need you within 4 m of him, and from the mess that's rarely true.** The galley's line spots are at
   columns 37-39, and the mess side of the pass is column 34-35. So a player standing at the servery, where the plan
   says the moment opens, is within 4 m only while he's at `3-galley-5` (37,5), and maybe `-4`. He moves spots about
   every 25 minutes. The player can walk into the galley through its door (v,35,8), but nothing tells them to. My probe
   teleported beside him, so it didn't test this. Either:
   - widen the reach to about 6 m when you're in the mess or the galley; or
   - make the servery tiles count;

   and add a probe that **walks** to the servery and waits, on Friday and Saturday.
4. **A reload in the middle of a moment loses the thread.** `story:fri` (and `story:sat`) is set when the panel opens,
   not when you reply. A reload mid-panel therefore:
   - loses the reply, so no lanterns are held;
   - suppresses Lukas's fallback Mail (`unless: 'story:fri'`);
   - and never offers the moment again.

   Set the key when the moment ends (`onEnd`) or on its reply, so a reload offers it again or sends the Mail.

### Nits (no turn needed)
- **Commendation timing:** "There's a commendation in your Mail" is said at 10:00, and the letter comes at 10:12
  (EV4's known item).
- **Mail order after a long skip:** the gist notes of missed meetings land after the Monday debrief in the inbox, so the
  order reads wrong after a skip. If the Mail list is sorted by arrival, stamp gists with their meeting's minute.

### Not tested here
- Leave and sick days during Days 12-13: the story only needs you on Deck 3, so being away just skips it.
- Dev mode's phase jumps: devmode_check and bigevents_check's live part cover them.

I'll check those in the fix round if lead 23 wants.

**Verdict: PASS WITH FIXES** (fixes 1-4). After them, and with a clean bigevents_check, S10 can go to the user's review.

## Round 2 (5f3fc3f): PASS
- **Fix 1:** bigevents_check from EC1's 037a149, which judges a gathering with `stay` by the most there at once, is OK
  on 5f3fc3f (EV4's run).
- **Fix 2:** DEV_NOTES now says "Fridays and S2 together, or S2 first", with FR2's minutes. EV4 builds S2 next, with
  claude/fridays merged in (lead 23's call).
- **Fix 3:** Lukas's reach is now 6.5 m, for the moments and for his bubbles. EV4's walking probe
  (`plans/storm-probes/walk_servery.py`) has the player walk to the servery and queue with a real tap. It now opens at
  17:10 in the queue, 5.5 m from him; before the fix it never opened all evening.
- **Fix 4:** `story:fri` and `story:sat` are now set on the reply, or through the moment's new `onEnd` when the panel
  closes, not when it opens. A reload mid-panel offers the moment again. While the panel is open, `DIALOGUE` stops it
  opening twice. Walking away still closes it for good.
- **My re-run on a switched-on copy of 5f3fc3f:** Friday, the Saturday errand and Brennan's "asked" line at supper all
  play as before. The supper has 51 at once (22 standing) at 272 calls. No errors.

The nits (commendation timing, gist order after a long skip) stay noted. Neither blocks S10.

**Verdict on claude/storm-update 5f3fc3f: PASS.** S10 can go to the user's review once S2 is in with the Fridays, as
DEV_NOTES now says.
