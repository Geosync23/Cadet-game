# Early review: claude/social-stories 8d6e932 (0.39.0 WIP, voice cards and steps in 20c)

Reviewer 1, 2026-10-17. Branch marked WIP ("checks still running"). Diff: `git diff origin/claude/ship-integration...origin/claude/social-stories`. New sub-block 20c plus two hook lines in social A's section 20 (both typeof-guarded, both in its hook register): in seat.

**Verdict (preliminary): PASS WITH FIXES.** Nothing blocking; three contract points to settle before 0.60.0.

## 1. SHOULD FIX: openness changes everyone's friendship speed now, before any voice card is written
- `relGain` multiplies every positive point (chat, meals, work, favours, appointments, news) by 0.8 for anyone whose traits guess "guarded" and 1.2 for "open". The guess is live today from the roster's traits, so the time to reach each tier shifts for most of the crew as soon as this merges. That's a game change, not an inert step. DEV_NOTES says only Tomas (normal) and Pell (open) were checked.
- Ask: either keep it inert until the crew designer's `openness` field lands (only scale when `p.openness` or `VOICE[id].openness` is set), or say plainly in the build row that this changes progression, and list social_check's before and after for the main crew.

## 2. SHOULD FIX: `knowSections` drops anything whose topic isn't in its list
- An `about` entry whose `topic` isn't one of work, home, hobby, past, secret, story, loves goes into `by[topic]`, which `KNOW_SECTIONS` never reads, so it vanishes from the Crew app. The crew designer is writing six or more `about` details per person now; agree the topic list with them (or put unknown topics under Home).

## 3. Note: `voiceOf` caches the first card it builds, forever
- Cards are cached per person (`VOICE_CARD`). If anything calls `voiceOf` before the writers' `VOICE` block or the crew designer's fields exist (a load-order slip, or a test that installs `VOICE` later), that person keeps the guessed card for the whole session. And as with social A, `typeof VOICE` throws if `VOICE` is a `const` declared later in the file and `voiceOf` runs at load. Agree with the dialogue engineer on where the baked blocks sit and that they're `var`, or clear `VOICE_CARD` when they load.

## Also checked
- Hash keys 672-678 used, inside the agreed 672-699; nothing draws; no `R()`. `relGain` leaves `intro:` and `moment` points alone, so onboarding's arrival totals hold.
- The bond names: see the social A review, finding 1 (`{friend}` vs `friends`). B2 should use the same frozen list.
- Merge note for the lead: 20c and the arrival's section 21 are both inserted after `chatTick`, before `// 6. CAMERA`.
