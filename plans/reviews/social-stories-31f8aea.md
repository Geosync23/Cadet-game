# Re-review: claude/social-stories 192e9c8..31f8aea (0.39.3: moments, the sparse weekly snapshot; social A 0.36.44 merged)

Reviewer 1, 2026-10-17. 20c, plus two one-line, guarded hooks in section 18 (`dialogueStep` → `sc.onPick`, `dialogueEnd` → `sc.onEnd`), both in the hook register with the traditions engineer as owner. Social A's merged 0.36.42-0.36.44 is reviewed separately (0.36.44 only adds seams for 20c). name_check OK against 192e9c8 and on a merge with crew 0.16.13.

**Verdict: PASS.**

## My 192e9c8 points: fixed (checked)
- **Save size** (the lead's decision, threshold 30): `affWeek` keeps only pairs at |aff| ≥ 30, as `[i, j, v]` bytes with the crew count in the header (a snapshot for another crew size is dropped). On a merge with crew 0.16.13 (86 crew), social_check: social save **19,440 bytes** (limit 30,000), OK.
- **Seating unchanged:** the only reader of `affinityPlan`, section 14's seating, compares against ±30 only (`a >= 30` friends, `a <= -30` avoid), so reading 0 for a pair between the lines can't change any seat. Crew indexes are stored as single bytes, fine below 256 crew (86 now).
- Day 0's week (-1) is read back (`/^(-?\d+):(\d+):/`). The "planned more than a week ahead" edge is in DEV_NOTES.

## Moments (smoke run in the browser)
- With Tomas as a friend (tier 3), met 20 days ago and his arc's first card beat told, `momentReady` finds `tomas:2` at 17:00 on the first evening, and `momentShow` opens it in the dialogue panel. It closes again when you're not in the room with them (section 18's rule); nothing is recorded then, so the moment can come back. Without the first card beat told, the arc waits, as designed.
- The gates check out in the code: tier and days known, one moment a day each, one serious moment a day for you, Pell's last beat waiting for his show, no moment at a crisis's onset, somewhere calm or a visit. The state is in `SHIP.social.stories` (saved). `onEnd` removes the script and counts the moment only if a reply was picked.
- social_check OK with 86 crew (bonds: 10 best friends, 9 mentors, 9 friends, 2 rivals; save and load the same; the reserve case passes).
