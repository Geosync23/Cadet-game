# Handover: B3, S5-5 (M20, the sensor array)

- **Role:** B3 (session_014FBmsiTsA9QymoN2qt4NyL), Step 5 builder; reports to lead 40 (session_01NXybH7NNqM8M4ngiyidq6m); reviewer RV20 (session_01PyJwfvfQVu4oXTYDMGkacw). My S5-4 shutdowns note is `plans/handover-b3.md` on `claude/p5s5-mech-b`.
- **Branch:** `claude/p5s5-m20`, from B2's `claude/p5s5-mech-a` c32aab5d (so M19 and the power line are in), with B1's `claude/p5s5-career` 51b1a9c6 merged (the ladder order; SW3's words come with it). Build-table rows `0.93.4-ar.1`, `ar.2`. Build-number lines untouched.
- **Built:** section 24x behind `P5_M20`; DEV_NOTES "The sensor array, M20" has the whole of it (the lesson, the `arraycal` job, the weeks and stages, the beats, the save, the words, the tests).

## Judgement calls (overrule any)
- Mori is off on Thursdays and Fridays, and crew keep their rest days (lead 40), so on Day 19 the ladder's teacher is Calder (the row's second `by`), with her own stand-in meeting `train.m20.calder`. `arrHost` books the teacher at the array's panel, and the other one at the first rack's only if they're on shift. Mori's word comes the first time you're near her after it (`m20.mori.later`).
- Every stop is at the array's panel. The spec's "replace a failing module" is the array's own module, not a rack's: one machine, so tap and pad play every stop.
- Any star is a right pick. Your last logged star (24t's "Wren {n}") is offered third.
- The save is `SHIP.works.side.ar`: the spec's SHIP.works.ar, under side so 24 core's worksClean keeps it.
- Job slot 34; schedU keys 1065-1069 (B2's reservation).

## Loose ends
- No Dev preset for Day 19 (that's the Dev mode seat's); the checks set the state up on paper.
- Words: SW3's m20 keys are used with stand-ins. My leftovers are in `content/works/array.lines`.

## How to test
- **Off:** `cadet_test.py` against mech-a's build: ALL IDENTICAL. Then `bash check_fast.sh`.
- **On (copy with `const P5_STEP5 = true;`):** `mech_check.py ON m20 wstap`; `CTL_P5S5=1 controller_check.py BUILD m20`.
