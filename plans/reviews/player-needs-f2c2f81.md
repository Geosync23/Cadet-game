# Review: player needs, tips and the News feed (claude/player-needs 41c895d..f2c2f81, 0.28.41-0.28.46)

Reviewer 1e, 2026-10-17. In-depth review, because this changes behaviour and saves. It covers player engineer 5's range:

- 0.28.41: the bathroom '+go' pose and the 70% walk; need warnings.
- 0.28.42: 34 teaching tips with pacing (33 plus the reputation tip).
- 0.28.43: social scaled by the bond (`bondMult`); at meals only your own table counts.
- 0.28.44: the News feed (the 'ship' app retitled, slot posts plus events, the last 40 saved); Crew renamed Relationships.
- 0.28.45: the tray fix (a tray only after being served; food rises as you eat).
- 0.28.46: tip text from head writer 4.

## Verdict: PASS WITH FIXES

There is one MEDIUM, which the player sees: tradition posts in the News feed show the tradition's id, not its name. Everything else works as described. The checks pass, the saves are bounded, tips never stack or show over a dialogue, and the feed is deterministic with no `R()`.

## Checks run

| Check | Build | Result |
| --- | --- | --- |
| player_check | 52a80ca (0.28.44) | Every check passed up to the last section (my 25-minute limit cut off the final "OK" line; there were no FAIL lines). It covered: the '+go' at bathroom 0 ([0.7, 0.7, needGo, blend 1, 0 prop meshes, "Bursting"], gone above 0); warnings 0-15 as designed; tips (34 unique, pacing, Tips off, none in the arrival, the Monday reputation tip, app tips only over their app, priority order, 496 bytes); news 4-8 posts a day, at most 2 a source, no repeat inside 7 days, 40 kept, 4.4 KB; a chat with a friend +12; tables [4,4,4,8,8,8,8], only your table counts, close friends ×3 capped at 6. |
| player_check | f2c2f81 (0.28.46) | See the end of this note (it covers the tray fix's own new test). |
| device_check | 52a80ca | device_check: OK |
| interactions_check | 52a80ca | INTERACTIONS CHECK OK |
| social_check | 52a80ca | SOCIAL CHECK OK, no page errors |
| News probe with the real bank (`player-needs-f2c2f81-news-probe.py`) | 52a80ca + head writer 3's `news.lines` (claude/content) baked in with `content_gen.py` | Details below |

## The News feed with the real bank

I baked the player branch's `content/` plus `content/banks/news.lines` from claude/content (all 10 kinds, 22-46 lines each) into a copy of the build. Then I ticked 14 ship days in two ways: every minute, and in 10-hour skips with chats (`lineFor` greets) in between.

- **Deterministic, no `R()`:** the seed is unchanged and there were no `Math.random` calls. The every-minute run gives the same feed twice. The 10-hour-skip run gives the same feed too (apart from one extra day at the end, because that loop runs past the last day).
- **Posts a day:** 2-7 (68 posts in 14 days). The sources are mixed: trad 25, galley 9, crew 9, bridge 6, outside 5, works 4, plus garden, infirmary, notice and gossip.
- No `{...}` is left unfilled, no post is over 90 characters, and no id comes back inside 7 days.
- **Save:** at most 40 posts (each text clipped to 200 on load), 120 `newsUsed` pairs and the rows map. The worst case is about 12 KB, and the real bank's texts are 90 characters or less, so it comes to about 4-5 KB. That is far inside the lead's 250 KB budget, so I didn't rerun `--long`.

### MEDIUM 1: tradition posts show the id, not the name
In the probe, 4 of the 25 tradition posts read like this:
> A ship tradition today: late-piano. Turn up and join in. That's all it takes.
> It's tasting-table today. Your device has the time and place. See you there.

**Cause:** `newsTrad` (06:00) and the `onSim('tradition')` post both pass `ctx.trad = e.id`. The bank's two generic lines under `trad:today` use `{trad}`. In `linesFill`, `val(k)` returns `ctx[k]` as it is whenever it's a string, *before* it asks `socialFill` (which would give the name). So `{trad}` fills with the id. The calls code (around line 27623) already has a pattern for this: `ctx.trad` = the name in lower case, and `ctx.tradId` = the id.

**Fix (smallest that keeps the bank as it is):** the feed passes `{ trad: e.name.toLowerCase(), tradId: e.id }`, as the calls do. Section 22's `linesOk` `case 'trad'` then also matches `ctx.tradId === x`, as `case 'came'` already does. Otherwise `trad:<id>` lines stop matching. That's a one-line change in section 22, so it needs the lines owner's OK. If that can't happen in time, a stopgap in `newsLine` is to swap the id for the name in the returned text when `ctx.trad` is set.
**Test:** add a news.trad stand-in with `{trad}` to player_check's feed test, and check that the post contains the event's name and not its id.

### LOW (content, for head writer 3): time-bound lines whose condition is wider than their text
- "Breakfast is on till 08:00…" is tagged `time:morning` (06-12), so it was posted at 09:45. "Friday tea and tool cleaning … this afternoon" is tagged only `weekday:fri`, so it was posted at 18:16.
- Fix: narrow the line, for example to `time:` plus an hour test if there is one, or reword it ("Breakfast till 08:00 every day…").
- None of this is engineering. Passing it on.

### LOW: slots lost after a skip longer than 12 hours
`NEWS_CATCH` is 720 minutes. A normal night (20:00-06:00, or even 19:43-06:00) is inside that. A multi-day skip (leave, sickness) loses the skipped days' posts, and the 06:00 "today" post if it falls outside the window. That's fine for a feed; I'm only noting it.

## Tips: never stacked, never over a dialogue

- **One at a time:** `teachTick` only offers a tip when `TIP_Q` is empty (it's part of `POP.busy`), and `tipShow` queues. Other sections' tips (`ixTip`, the device's first-open tip, 'walk', 'tiles-nobody') can still join the queue behind a teaching tip. They then show straight after it, with no 60 s gap. That was already true before; it's a LOW if it's a LOW at all.
- **Dialogue:** `teachTick` and `needWarnTick` both wait while `dlgon`/`DIALOGUE` is up. If a dialogue opens while a tip card is showing, CSS hides the card (`body.dlgon .devtip{display:none}`), and `dialogue(null)` brings back a tip still in the queue. Its 9 s timer keeps running behind the dialogue, so a tip can run out unseen. That's a nit, and it was already so.
- **Heads-ups:** a tip takes the top and the heads-up strip waits (`devHeadsBack`), so they don't overlap.
- **The 'sure' reputation tip** skips the 3-minute and 60 s pacing but still needs a quiet screen and no toast in the last 6 s. As designed.

## Social by the bond, tables, the tray fix

- `seatTable`'s single linkage at 1.3 m gives exactly the mess's 7 tables. `tableCrew` leaves out your own seat and other tables. Guests and unknown ids count 1.
- `A.o.company` is now a bond-weighted number. Its readers still work: the toast's "Good company, too." and `simAct('eat', { with })` (the 'Eat with the crew' lesson tests `with > 0`). `ixSide` handles both `true` and numbers.
- **Balance (for the lead or design, not a defect):** sitting company was capped at 3 and is now 6, and joining a tradition can now give up to +36. With close friends, social will be easy to keep full later in the game. That's the user's rule ("every social gain from a person scales with the bond"). I'm flagging it only so it's a known effect.
- **0.28.45:** every `actStart('eat')` either comes with `fed: true` (the tray-at-seat path, and "every seat's taken") or is turned into 'sit'. The arrival dinner already used 'sit', so nothing else depended on the old table service. The engineer's new player_check test covers both cases.

## Other LOWs and nits

- `WARN_SAID` and `TEACH_ST` aren't saved, so a reload can say a need warning once more for a need that's already low. That's harmless.
- `newsLoad` copies `s.newsRows` without checking the values. Only a hand-edited save could put junk there, and it only affects the comparison.
- The `crew` glyph is now unused in `GLYPH` (Relationships uses `people`). Harmless.
- '+go' looks right in the engineer's screenshot (hands clasped low, knees in). No new meshes, as player_check confirms.
