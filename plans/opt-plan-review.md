# Optimization pass plan: adversarial review

Reviewer ER2 (session_01S8pboNujAzZgMSWFK84CxD), 2026-10-21. Branch `claude/event-plan-review-2`.
Plan reviewed: `claude/opt-plan` e9ecf81 (`plans/opt-plan.html`, `plans/opt-measure.md`, `plans/opt-probes/`), by
OP1, from 0.64.7. Reports to lead 23.

## Round 1 (e9ecf81): PASS WITH FIXES

**How I checked:** I read the page, the measurements and the probe list. I confirmed in the code:
- the perf_check room bug;
- the grain painter and the random-number function;
- the crowd's upload code.

I timed two page opens on e9ecf81 in this container. They took 12.8 s cold and 9.4 s warm, against OP1's 7.5 s.
That's a different box, so the size is plausible.

### What holds
- **Item 0 is real and rightly first.** perf_check.py:46 passes the room's middle tile (column, row) to
  `nearestOpen(x, z, who)`, which wants a world position. So every perf baseline so far was taken in whatever room
  is nearest that point. Fixing it and taking a new baseline before anything else is correct. So is the corrected
  headroom: the mess hall at 418 of 450.
- **The measurements are honest about this box.** The page plainly says SwiftShader's shader and draw times are not
  phone times, and the 4-5× rule applies only to game code. Every table names its probe in `plans/opt-probes/`.
- **The "not proposed" list follows the user's rules.** Nothing skips drawing, nothing changes what you see, and the
  shader-store idea was tried and dropped, with the numbers.
- **The ranking is mostly right.** Item 1 (affected checks) and item 2 (crowd uploads) give the biggest gain for
  the least risk. Item 7 (the cache) and item 10 (saved starting points) come last and wait on the user, which
  matches the user's "fixtures with caution, never the only check".
- **Determinism for the grain work (items 4 and 7) is feasible.** All 8 `grain()` calls run while the page opens,
  and `R()` is a single Lehmer step on one number (`seed`). So "the same numbers, a tighter loop" can be exact, and
  a cache can put the generator back exactly by saving that one number.

### Fixes
1. **Item 2's method doesn't fit three.js r128 as written, and its proof contradicts it.**
   - **Uploads:** today each chunk sets a single `updateRange` (offset and count) per attribute (section 8b, around
     line 48318). In r128 an attribute has only **one** update range per upload. If several people in a chunk change
     in one frame, which is the normal case after skipped frames, "only that person's piece" means either one range
     covering all of them (back to big uploads) or calling WebGL directly through three's internals
     (`renderer.attributes`).
   - **The proof:** "keep each person's shape in its own fixed place" changes the buffer's layout. So a probe that
     compares *what is sent* byte for byte with the old code can't pass by design.
   - **The fix:** say which way it's built:
     - (a) the same layout, with the dirty part tracked per frame and the upload split into several direct
       `bufferSubData` calls (an r128 internals hook: name it and how it's guarded);
     - (b) fixed slots, with the proof comparing the **final buffer contents and the picture** after each drawn
       frame, not the upload stream;
     - or (c) smaller chunks. That costs draw calls, which the mess hall can't afford at 418 of 450.

   Re-estimate the gain for whichever is chosen.
2. **Item 7 must never run inside the checks unseen.** Checks open with `?nosave`. Say that `?nosave` never reads or
   writes the texture cache, so every check still paints, and that one probe tests the cached open on purpose:
   - the same pixels;
   - the same `seed` after opening and after visiting every deck.

   Otherwise either the painting path or the cached path goes untested. Also say where the textures are stored
   (several MB means IndexedDB, not localStorage's ~5 MB), and that a full or blocked store falls back to painting.
3. **Item 5's caches are "records built while the game runs", which the planner rule forbids.** Remembering
   `whereIs`, `planWhere` or `walkGap` per person per ship minute is fine only if:
   - the cache is keyed by everything those functions read;
   - it's cleared on every event that can change a plan in the same minute: a skip or sleep, a reload, joining a
     tradition, a meeting, an event phase, a Dev-mode jump;
   - and it's never read by the planner itself, only by the frame code.

   Say so, and add a check that runs those cases: a jump, a skip and a join, each compared person by person with
   the old build. The HUD cache (`matchMedia`, button positions) must also clear when the HUD changes for reasons
   other than a resize (the needs strip, the device opening, orientation). Its proof is interactions_check and
   bubble_check at 390 and 360 wide, not cadet_test's pictures, which don't test where taps land.
4. **Item 1 needs a number before the user's question 3 is answered.** Function coverage in a game where every check
   runs the main loop may pick "nearly everything" for most sections. Content and data-only changes, such as
   section 22's baked lines and the tradition tables, don't show up as functions at all. Put two measured numbers on
   the page:
   - how many checks it would pick, on average, for the last 10-20 merges in the build table;
   - whether every check that really failed on those merges was among them.

   Also say how data sections map: by their readers, through `tools/section.py`. Without these, "a turn would
   usually need 3-6 checks" is a guess, and the recommendation to answer question 3 with "quick plus affected"
   rests on it.
5. **The biggest single check has no item.** player_check is 36 min 39 s, a third of the round. "Where its time goes
   is the test-speed seat's first look after item 1" should be its own item, ranked: profile it in turn 0 or 1, with
   the same proof rules as the others. It probably gains the most check time of anything here.
6. **The seat count against the user's limit.** The page asks for five sessions overnight plus the build master
   already on duty, which makes six. The user's standing rule in TEAM.md (lead 21, 18:20) is "3-4 helpers steady",
   and lead 23 says "within 5 seats". Make question 8's recommendation fit the limit:
   - recommend 4 (test-speed, render, one load-and-frame seat, the reviewer), or say plainly that the build master
     counts outside it;
   - and keep "fewer" as the slower option.
7. **(Missing, small)** Warm the shaders after a deck change. On a phone the first frame after a deck change still
   compiles every new kind of material. `renderer.compile(scene, camera)` right after `buildDeck` moves that work
   off the first drawn frame without changing a pixel. Add it as a measured candidate on the render seat, or say why
   not.

### Smaller points
- **What "headless" means.** The user's rule says "NEVER headless/no-drawing runs". Our checks run Chromium without a
  window but draw every frame they draw today. Say that in one plain sentence on the page, so "headless" isn't read
  as breaking the rule.
- **Gain estimates are marked "aim".** Good. Item 4's "about half" is optimistic: the loop is already tight (one
  `R()` and three adds a pixel). Treat it as an upper bound.

### The questions
Q1, Q2, Q4, Q5, Q6 and Q7 are clear for a non-coder and have honest recommendations. Q3 needs fix 4's numbers first.
Q8 needs fix 6.

**Verdict: PASS WITH FIXES** (fixes 1-7). Items 0, 4, 6 and 11 are ready to build as written. Items 1, 2, 5 and 7
need their fixes in the plan first.

## Round 2 (d1a6516): PASS
All seven fixes are folded in, and the items are renumbered 0-13:
- **Crowd (#3):** fixed slots with one `updateRange` from the first changed slot to the last, which fits r128 with
  no internals hook. The proof reads back the triangles each chunk draws, skips the empty ones and compares the rest
  with the old build, then the pictures. Smaller chunks are ruled out. The gain is re-estimated honestly: the real
  check gain is probably the double-send found in turn 1.
- **Texture cache (#9):** never under `?nosave`, kept in IndexedDB, and falls back to painting. One probe compares a
  cached and a painted open: the same pixels and the same seed.
- **Frame caches (#7):** frame code only, keyed by everything they read, cleared on every plan-changing case, with a
  probe for each. The HUD cache is proven by interactions_check and bubble_check at 390 and 360.
- **Affected checks (#1):** a measured lower bound. Over the last 20 turns it picks 4.2 checks (28 min) against
  22 (106 min). Q3's answer applies only after the replay of caught failures passes.
- **player_check (#2):** turn 0.
- **Seats:** four, with the build master outside.
- **The warm-up:** measured. It only moves the wait, so OP1 found a better change instead: #4 keeps compiled shaders
  across deck changes. A second lap's first frames take 6.3 s instead of 9.2 s. It's one named internals hook in
  three r128, which is pinned. The probe checks that the shader count stops growing. One condition for its build
  review: decks with different lights or fog make more shader variants, so the count must be measured after every
  deck at both phone sizes, and the flat memory over round trips must hold.

**Verdict on claude/opt-plan d1a6516: PASS.** All recommendations are safe to take.
