# Review: claude/social a033f17..752d964 (0.36.79-0.36.81: affWeek by crew list, NEWS_MAX 16, the packed save)

Reviewer 1c, 2026-10-17 (reviewer 1 passed up to a033f17). Diff: `git diff a033f17 752d964` (section 20, social_check, DEV_NOTES, the handover note).

**Verdict: PASS** (one low worth a line).

## Checked
- **social_check on 752d964: SOCIAL CHECK OK.** Packed vs raw at 14 days: 4,134 vs 4,873 bytes. News and cue rows round-trip, and the older object forms load.
- **My own round trip** (400 pairs moved off their start, -100..99): `socLoad(socSave())` gives every pair back exactly. A garbage `aff` (`'d:!!notbase64'`) is refused (`false`).
- **`affPack` / `affVals`:**
  - The zigzag never makes 0, so 0 always starts a run. Runs are varint lengths, so a 74-person list (2,701 pairs) fits.
  - Values are the start plus the change, so they come back exact.
  - With a different crew list, the starts are rebuilt from the saved `idl` against today's roster objects, and pairs with someone gone become NaN and are skipped.
- **`rel` rows:** saved as `[SOC.idx.get(id), ...]` against the save's own crew list, and loaded through `idl` when the list changed (the by-id object still loads). Ids outside `SOC` were dropped on load before as well, so nothing new is lost.
- **News and cue rows:**
  - `rowOf` trims trailing nulls only when there's no extra object; with one it pads, then appends. `newsRow` and `cueObj` read them back.
  - Cues always have `at` and `until`, and the old `cueSaved` also left empty fields off, so a short row reads the same as before.
- **`affWeek`** only loads when the saved `idl` matches today's; older saves without `idl` keep it, as before.
- **`affStart`** reads dept, bunk room, shift, habits, traits, partners and clashes, not thread or home. So the roster's recent edits (Kovac's thread and home, Sato's thread) don't shift loaded affinity. A rotation that moves someone's bunk or shift would, by the delta design. That's fine, but worth a sentence in DEV_NOTES' Save bounds: "a roster change to dept/bunk/shift/habits/traits shifts saved affinity by the change in the start".

## Low: a truncated affinity string now loads instead of being refused
- I cut the packed `aff` to half its length (on a 4-character boundary): `socLoad` returned **true**, and 1,733 of 3,655 pairs changed.
- With the same crew list, `affVals` fills the missing pairs with NaN, and the `Int8Array` turns them into 0. Before 0.36.81, a raw string of the wrong length was refused.
- Truncation is unlikely (localStorage writes whole strings), but the guard costs one condition:
  - in `socLoad`'s same-list branch: `if (!vals || vals.length !== a.length || vals.some(v => !Number.isFinite(v))) return false;`
  - or have `affVals` return null when the data runs out before the last pair.
