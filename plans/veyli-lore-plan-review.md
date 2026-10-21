# Who the Veyli are: adversarial review of the lore plan

Reviewer ER2 (session_01S8pboNujAzZgMSWFK84CxD), 2026-10-21. Branch `claude/event-plan-review-2`.
Plan reviewed: `claude/veyli-lore` 6c1c861, `plans/veyli-lore-plan.md` (LW1, v1). Reports to lead 22.

## Round 1 (6c1c861): PASS WITH FIXES

**How I checked:** I grepped the branch's game file and the whole of `content/` and `plans/events-ready/` for
"human(s)", "alien", "species", "their kind" and "creature". I also searched for every Veyli name (Saruth, Teshavi,
Kesrin, Moleth, Ithra, Taavek, "the Envoy", "the Speaker") within a few words of he, she, her or his. Then I read
Saruth's roster tiers, Holt's arc lines, the Line and storm plans, and facts.md.

### What holds
- **History A fits everything already written.** That's the cord, the tea hour, quiet, warmth, "do not bow", single
  names, Taavek's "no common words", rare Veyli ships, the "shared" frontier, "the Veyli homeworld", Tavessa, and the
  Line's "guests in someone else's sky" with the charts thin past it. About eighty years of contact sits fine with
  the Wren's run two years ago and Holt's "years ago". No war, and nothing links the contact to Holt's patrol day.
  It's the right recommendation, and it answers the user's "reaching into the distance" best.
- **The "human" lines: the audit is complete in the game.** Every game line with "human(s)" is in the audit: 23365,
  23374, 23377, 25147, 25154, 25156, 33838, 33839, 36691, 48852 and 48860. So are their source files.
- **The secrets table is right.** Saruth's tier-4 secret really is "Was sent to the Wren because no one at home
  expected the posting to work". Holt's beat 3 holds the six hours and the mourning rite. Nothing in the new lines
  touches either, previews the visit, or hints at the déjà vu day.
- **The learning steps sit where the player already goes.** Day 1, the booths, Saruth on Deck 2, Ferreira and Rossi,
  the Friday addresses, the Line, the comet, the visit. The basic fact is plain from week one, with no twist, which
  is the right call (vl-q2 a).

### Fixes
1. **The audit misses facts.md:19.** It reads "**The Concord:** the human union that runs the Survey Service". With
   the Veyli human, "the human union" says either that they aren't human or that they belong to it. Change it to,
   for example, "the union of the near stars' worlds that runs the Survey Service".
2. **There are three "she" slips in the game, not two.** Game line 6495 (the Captain's table, a tap text the player
   reads on screen) says "...and the Envoy when she accepts." That's Saruth, so it becomes "when they accept". The
   code comment at 5601 ("a quilt in her own colours") should be tidied too. Add both to the audit; the first is the
   owner of that deck's dressing. Section 4's "two slips in the game" becomes three.
3. **The storm step can't happen in a new game.** "Once, during the blackout, Deck 2 or the mess". EP3 measured the
   storm left alone: blackouts on Deck 1 (Saturday) and Deck 6 (Sunday), none on Deck 3 and none on Deck 2. Tie the
   line to the lantern supper instead: the mess is dimmed to lamp light on purpose, 18:00-19:30 Saturday, and
   Saruth goes (the storm plan says so). "When the lights were low, we read the cord by touch" fits it better
   anyway. Or tie it to "any blackout on the deck you're on".
4. **The line count (nit):** the table's new lines add up to 23, not "about 24". Fine as "about", but make the
   summary and the table agree.

### The recommendations
- **vl-q1 a** (the ones who went on): safe, and the best fit.
- **vl-q2 a** (plain fact in week one): safe.
- **vl-q3 a** (they/them as a Veyli custom): safe, and honest. It keeps every line already written, needs one
  Ferreira line at most, and with fix 2 the on-screen slips become three.
- **vl-q4 a, vl-q5 a, vl-q6 a:** safe. Option (c) of q4 ("humans" as a Veyli joke) would break the plan's own
  description rule, so it's rightly not recommended.

**Verdict: PASS WITH FIXES** (fixes 1-3; 4 is a nit). All six recommendations are safe to take once the audit gains
fixes 1-2.

## Round 2 (9fa7521): PASS
All four are in:
- facts.md:19 is now "the union of the near stars' worlds" (audit row 19).
- The "she" at game 6495 is now "they", and the 5601 comment is tidied (rows 20-21). Section 4 now says there are
  three slips.
- The cord-by-touch step sits at the lantern supper.
- The count reads about 23 new and 15 changed.

**Verdict on claude/veyli-lore 9fa7521: PASS.** vl-q1 to vl-q6 (a) are all safe to take.
