# Re-review: claude/deck-plans-1-2-6 d53cf40..cadfbdd (0.16.16-0.16.20: Sato and Kovac's threads, Kovac's canon details and home, collecting nouns, talent crafts)

Reviewer 1c, 2026-10-17. Diff: `git diff d53cf40 cadfbdd` (the generator, the generated block, the roster page, DEV_NOTES, the handover note). Follows roster-d53cf40.md.

**Verdict: PASS.** My medium from d53cf40 is fixed, and nothing moved that shouldn't.

## Checked
- **Regenerates byte-identical** at cadfbdd (`git status` clean after `python3 plans/crew-roster-gen.py`).
- **Every roster table compared field by field, d53cf40 vs cadfbdd.** Only these changed:
  - Sato's `thread`, arc:sato → notgood;
  - Kovac's `thread` (notgood → arc:kovac), `home` (Valo → Marra Station) and `about` (seven lines from canon);
  - `hobbyNoun` for pell, zielinski-oona, shah-dara (the collecting nouns);
  - `hobbyNoun` for the six talent-theme people.
  Everything else in `HABITS`, `ROSTER`, `ROSTER_PLAYER`, `GUEST_TEMPLATES`, `GUESTS`, `ROSTER_GUESTS`, `ROSTER_RESERVE` and `ROSTER_ROTATIONS` is unchanged.
- **The talent fix:** `TALENT_NOUN` gives crossword setting, tea blending, story writing, tile carving, star sketching and patch sewing. All six read right in head writer 3's talent beats ("I do a bit of tile carving when nobody's looking", "Me, teaching story writing", "I made it for you"). The generator stops if a talent person has no entry. Public `hobby` is unchanged. The duplicate `HOBBY_NOUN` keys are gone.
- **Agrees with the writers** (content fd3db63): `content/voices/kovac-zainab.voice` says `thread: arc:kovac`, and `content/arcs/kovac.arc` exists (the ladder, the scrubber, Marra Station in beat 3). There's no `sato.arc` and her voice card has no thread, so notgood from the roster is what plays. `arc_fixes` runs after `kin_lost`, so Kovac's kin ("my mum", from her big family) and lost ("") are unaffected.

## Low (for the lead: canon vs the sim, not this seat's to fix alone)
- Kovac's secret is "Is afraid of the lift", and her tier-3 line says she always takes the maintenance ladder, but section 10 sends every crew member between decks by the lift. A player may see her riding it. Either the sim walks her by a crawlway or ladder when there is one, or the writers soften the line to "avoids the lift when she can".
- "Skips breakfast for the garden" vs the schedule: day_check makes everyone eat twice, and her plan has breakfast. Harmless, but if the writers want it seen, sim engineer 4 could give her a garden slot in place of a breakfast on some days.
