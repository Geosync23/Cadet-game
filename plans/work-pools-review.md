# Review of the work-pools plan (TR1)

**Reviewer:** TR1, for TW1 and lead 20. **Reviewed:** `claude/talk-pack` at 6de6a87: `plans/work-pools-plan.html`
(every line, the samples and the form) and `plans/work-pools-plan.md`. Checked against the game's `ROSTER` and
`ROSTER_ROTATIONS` (in the build on that branch), the theme threads, `plans/talk-pack-plan.md` (with the user's
2026-10-20 decision), TE1's reader on `claude/talk-wire` (cc04ef8), and the page at 390 px in Chromium.

## The plain summary

The plan is sound and the pools are right: every headcount matches the game's crew list exactly (86 crew; 74 from
Day 1 and 12 arriving through `ROSTER_ROTATIONS`), the odd cases are real (Madsen's role is "Bartender", Haddad's
"Galley hand, relief bartender", Oduya is in the infirmary department, and the Captain, Vance, Kowalczyk and Zielinski
are department `command`), the sizes add up (138 talks × 9 = 1,242 lines), the form has exactly the markup asked for,
and the page has no sideways scroll at 390 px.

Four things to fix before it goes to the lead and the user:

1. **The friend tier collides with the struggle themes.** "A mistake that stuck, doubts, would you choose it again,
   what's next" *are* the themes `notgood`, `burnout`, `leaving` and `stuck`. 42 of the 86 crew have one of those, an
   exams theme or a story arc. If the friend talks skip them all (as the plan says), the Galley has 2 people left to
   tell its friend talks, the Store 1, the Infirmary 3, Comms 3, the Bridge 4. Choose friend-tier subjects the themes
   don't own instead (what the job means to them, who they do it for, a proud moment, a teacher, a habit it gave them).
2. **The picking order would make your own department talk shop for weeks.** Own → work → shared means every Works
   crewmate tells only work talks until the Works pool (36) is used up, and Works is who you see most. The pack's own
   "vary the topic" rule can't help, because the order puts all work first. Recommend: work and shared take turns
   (prefer whichever topic you haven't had with this person lately), and make that option 1.
3. **Question 2 asks again what the user has already decided** (2026-10-20: strict once per save, for the shared pool).
   Say so on the page, and only ask whether work pools follow the same rule.
4. **Four sample opener lines are over the 90-character limit**, and a few samples need conditions (who has bunkmates,
   who works the engine room, who isn't Brennan).

The engineer hooks are close: TE1's reader takes `pool`, `smalltalk` or a crew id after `@talks`, so `work:<pool>`
needs a small change there (and a `work` key in `TALKS`). The new `role:` word isn't needed: `dept:` already splits
helm from command, and the bartenders, engine crew and Counsellor are short `who:` lists.

Counts: **0 blockers, 13 should-fix (S1-S13) plus fixes to the samples (section 7: four over-long lines and some
missing conditions), 12 nits.**

---

## 1. Pools and headcounts against the roster: correct

| Pool | Plan | Roster (Day 1 + later) | Notes |
| --- | --- | --- | --- |
| Works | 20 + 3 | 20 + 3 (Bramwell 35, Mwangi 77, Kowal 161) ✓ | engine crew: Torres, Reyes, Keane, Jovanovic, Amadi, Salo, + Kowal on 161 (Keane leaves 161): **6 at a time**, 7 over the year |
| Watch | 12 + 2 | 12 + 2 (Dufresne 161, Castellano 245) ✓ | 5 on nights from Day 1 |
| Survey | 11 + 3 | 11 + 3 (Achebe 77, Tavares 161, Juarez 245) ✓ | |
| Bridge | 9 + 1 | helm 5 + command 4, + Haverford 119 ✓ | Zielinski works at `work:ops` and Kowalczyk on nights, both Deck 1 |
| Comms | 5 + 1 | 5 + 1 (Quaye 119) ✓ | Ferreira, Farouk, Santos, Tran work on Deck 2; Takahashi on Deck 1 |
| Infirmary | 6 + 1 | 6 + 1 (Nordqvist 203) ✓ | Oduya is `dept: infirmary` |
| Galley | 6 + 1 | 6 + 1 (Sorensen 203) ✓ | Madsen "Bartender"; Haddad "relief bartender", leaves 203 |
| Garden | 3 | 3 ✓ | |
| Store | 2 | 2 ✓ | |

- **S1. "Bar talks for Madsen and Haddad":** Haddad leaves on day 203 and nobody replaces her at the bar (Sorensen is a
  "Galley cadet"). After 203 Madsen is the only bartender, so three bar talks once per save are fine, but say on the page
  that it's one person for most of the year. (`work-pools-plan.html:89`)
- **S2. Cadets arrive brand new** (Works, Survey, Watch and Galley cadets on days 35, 77, 161, 203). Talks with a past in
  the job ("my first month", "who taught me", "a mistake that stuck") don't fit someone who arrived last week, and
  `!newhere` only covers 7 days. Add a line to the plan: history talks skip roles with "cadet" (`who:` lists, or `rank`
  plus the arrival day if the engine adds `aboard`). (`:93`)

## 2. The odd cases

- **S3. Bridge: helm talks are wrong for all four command crew, not just the Captain and Vance.** Kowalczyk (Second
  Officer) and Zielinski (Operations) aren't helm either; "People think helm is steering" from Zielinski is wrong. Use the
  existing condition: helm talks `dept:helm`, command talks `dept:command`. (`:86`, `.md` table row "Bridge")
- **S4. Command talks are the riskiest in the plan.** The Captain's arc is the loneliness of the chair, her daughter and
  retiring; Vance's is the rule he broke and the messages from home; Kowalczyk's thread is `lonely`; Zielinski's is
  `notgood`. Four command talks for four people, three of whom have a story that's "about the job", leaves almost no safe
  ground. Either keep the four command talks at acquaintance and colleague only, on the plain work (the watch rota, the
  log, the long night shift), or fold them into the shared pool as two or three talks. (`:130`)
- **S5. Oduya:** his thread is `loss` (his late wife). The "listening" talks suit him; keep them clear of grief and of
  "who listens to you" (the loss theme's beat 2 opens that door). (`:88`)
- **N1.** Comms isn't "on the bridge" and the page doesn't say it is; fine. But "Comms joins Bridge" in question 3's
  second option would put Deck 2 workers in a Deck 1 pool: say "Comms joins Bridge (both command-side)".

## 3. Picking order and once per save

- **S6. Own → work → shared runs each person's work pool dry before they ever talk about anything else.** The variety
  rule in `talk-pack-plan.md` ("prefer a topic you haven't talked about with this person lately") only works *within* a
  source. Your Works crewmates are the people you see most, and the Works pool is 36 talks shared by 23 people, so for
  the first weeks at acquaintance and up, nearly every talk with a Works crewmate would be shop talk. Recommend making
  "mixed" the first, recommended option: own talks first; then work and shared alternate per person (or the picker
  treats the work pool as one more topic in the variety rule). Rewrite option 1's text and the "Picking order" section
  (`:113-119`, `:251-253`):
  `<label><input type="radio" name="wp-q1" value="mixed">Their own talks first, then work and shared talks take turns, so nobody talks shop all week <span class="rec">recommended</span></label>`
- **S7. Question 2 asks again what the user has already decided** (CLAUDE.md: don't re-ask a decided question). The
  pack plan records: "the user's decision, 2026-10-20: keep strict once-per-save, no repeats". Say so and narrow the
  question (`:257-261`):
  `<p><b>2. You chose "once per save" for the shared pool (20 October). Do work talks follow the same rule?</b></p>`
  with options "Yes, the same rule" (recommended) / "No: once per person, so each crewmate can tell their version".
- **S8. The run-out estimate needs a footnote.** "Roughly two months instead of one" (`:118`) assumes the player spreads
  talks across all pools. A player who mostly talks to Works crew uses up the Works pool in about 36 talks (eight or nine
  days at four a day) and the smaller pools are never reached. Fine, but say "about two months across the whole ship;
  sooner with your own department". Also note the pack plan's "more pool talks when the game grows past Day 30".
- **N2.** "Work talks start at acquaintance, so strangers go straight to the shared pool" (`:116`): true, and good. Add
  that a work talk that fails its tier waits, like own talks do, so it isn't skipped for good.

## 4. Size and seats

- The arithmetic is right: 36+20+20+14+12+12+10+8+6 = 138; ×9 = 1,242 lines; about 1.6-3 talks per person.
- **S9. Size them by who can actually tell them, not by headcount.** After the skips the plan itself asks for (stories
  told early, work themes), the speakers are: Works 13 of 23, Watch 8 of 14, Survey 8 of 14, Bridge 4 of 10, Infirmary 3
  of 7, Galley 2 of 7, Comms 3 of 6, Garden 2 of 3, Store 1 of 2. Twelve galley talks for two speakers, or six store talks
  for Ishikawa alone, will each read as one person's monologue. Either fix S10 (fewer skips), or shrink the small pools:
  Galley 8, Store 4, Infirmary 8, Bridge 10 (then about 120 in all).
- Seats: the first pack (160 talks) was one writer in three chunks; two seats at ~70 each for one session each is
  realistic, plus my review and one round of fixes. Fine as written.

## 5. The friend tier and the themes (the main design point)

- **S10. The friend-tier subjects are the struggle themes' own material.** Plan `:102` and `.md` "Friend (~3 in 10): a
  mistake that stuck, how it follows them home, doubts, what's next, would they choose it again". Compare the theme
  outlines (`content/arcs/outlines.md`): `notgood` beat 2 "a mistake they still think about"; `burnout` "can't say no";
  `leaving` "unsure whether to stay"; `stuck` "wants to try another department". The pack review already asked for
  `!thread:` skips for these; here they'd remove half of every pool. Proposed friend-tier list instead (none of them a
  theme's beat):
  - what the job means to them, put plainly ("someone sleeps safe because of the night round");
  - who they do it for (a teacher, someone back home, the crew);
  - a moment they're proud of, small and specific;
  - a habit the job gave them that they can't switch off (sample `watch.switch-off` is exactly this, and good);
  - what they'd teach you if you had a week.
  Keep "a mistake that stuck" and "would you choose it again" out of the pools: they belong to the themes. Change `:102`
  to: `<b>Friend: what it means</b>What the job means to them, who they do it for, a moment they're proud of, a habit it gave them, what they'd teach you.`
  and question 5's first option to match.

## 6. Engineer hooks (checked against TE1's reader, `claude/talk-wire` cc04ef8)

- **S11. The reader rejects `@talks work:<pool>` today:** `parse_talk_file` takes "pool, smalltalk or a crew id"
  (`[a-z][a-z0-9-]*`), and `TALKS` has only `pool`, `own` and `small`. The plan should name the change: accept
  `@talks work:<pool>` with `<pool>` from the fixed list of nine; build ids `work.<pool>.<slug>`; set `topic: work` (so
  no `topic:` line in work files, and one is an error, as in pool files); add `TALKS.work = { works: [...], ... }`; and
  check ids unique across pool, own and work together (the reader already checks pool + own).
- **S12. Drop the new `role:` word.** `dept:` (existing) splits helm from command; engine crew is
  `who:torres-zeke|reyes-alejandro|keane-davi|jovanovic-petra|amadi-asha|salo-saad|kowal-priya`; bartenders
  `who:madsen-ivo|haddad-tamsin`; the Counsellor `who:oduya` / `!who:oduya`. Seven, two and one names, all stable ids.
  One less word for lines_check and the engine. (`:151`, `.md` "For the engineer")
- **S13. The dept→pool table should be data, not code,** and live in one place (`TALK_WORK_POOLS = { works: 'works',
  watch: 'watch', survey: 'survey', helm: 'bridge', command: 'bridge', comms: 'comms', infirmary: 'infirmary',
  galley: 'galley', garden: 'garden', store: 'store' }`), so question 3's "fewer" or "more" answer is a table edit. Say
  which department the roster's guests and `civilian` map to: none.
- **N3.** "Fired in the same save record" and "work talks count as topic work": both right, and they match the pack
  plan. Add "the picker reads the speaker's pool from the table at talk time, so a crewmate who arrives later draws it
  from their first day" (it does that already; say it).

## 7. The ten samples

All ten keep the question (their ask, three replies, an answer each), have no lunch, nothing romantic, no tokens or
placeholders in the replies, and replies within 44. Notes:

- **S-lengths (should fix): four openers are over 90 characters.**
  - `:194` (95) → `I chose this because of one nurse. I was nine, my arm was broken. She explained it all.` (87)
  - `:202` (99) → `Dinner rush: seventy-five people in three hours. You stop being a person. You're hands.` (87)
  - `:226` (102) → `On the Watch you think about what could go wrong, all shift. Then you take it to dinner.` (88)
  - `:234` (93) → `A long turn takes four hours. You hardly touch anything. You watch, wait, stay ready.` (85)
- **`work.works.hands` (`:169-175`):** "Coil oil" is the engine room; "my bunkmates" is a junior. Give it
  `when: tier>=acquaintance rank:junior who:keane-davi|jovanovic-petra|amadi-asha|salo-saad|kowal-priya`, or make it
  everyone's: `them: Machine oil. Two washes, and my hands still smell of it at dinner.` with `rank:junior`.
- **`work.works.first-fault` (`:161-167`):** from Calder ("I was shaking") it fits her history (swarf, the shipyard)
  only loosely; from Torres it's fine. Add `!who:calder` (her first-chief story is her arc). Also skip `notgood`
  (Salo): "Then I sat on the floor for ten minutes" is that theme's beat 2.
- **`work.works.choose-again` (`:177-183`):** the clearest theme clash (S10): it's `leaving`/`stuck` (Rahman wants
  another department; Teague is on the transfer list). Replace it as a sample with a friend talk from the new list, e.g.
  `them: Know what I think about on a long shift? Who's asleep upstairs because the air's right.` /
  `them: Seventy-odd people. Not one of them knows my name was on that job. I like that.` /
  `ask: Who do you do the job for, really?` ... "I mean that" (L182) is also the pack's most-repeated sign-off (N29 last time).
- **`work.infirmary.waiting-room` (`:185-191`):** the infirmary has no waiting room in the game (the "Waiting sofa" is
  the call-home booths'). → `It's the bench by the door.` / `Someone sits on the bench pretending they're fine.` This
  one suits Oduya best: mark it as one of his "listening" three.
- **`work.infirmary.one-nurse` (`:193-199`):** gives Rina a reason for medicine her arc doesn't have (her story is the
  hard year at home and the exam she won't sit): `!who:rina|oduya` (Oduya isn't medicine), and skip the `exams` theme
  (Grieve).
- **`work.galley.rush` (`:201-207`):** good. Bartenders don't do the dinner rush: `!who:madsen-ivo`. "Cold dinner,
  standing up, half eight" fits the 17:00-20:30 dinner. Fine.
- **`work.galley.again` (`:209-215`):** needs `!who:brennan`, and it's a `notgood` beat in miniature ("a mistake you're
  glad you made"): skip Walsh and Dlamini. Brennan saying "Again." and staying till midnight is lovely and in her voice.
- **`work.watch.door-sounds` (`:217-223`):** good, and "someone from Works turns up with a spanner" is a nice nod to you.
  Holt's own talk now counts doors too ("two hundred and six", which the page quotes at `:117`): keep the numbers
  consistent, or let only Holt count them. Nit: the mess bell exists only as a Pell joke; "The kettle at the tea
  corner. I'm well trained." avoids inventing it.
- **`work.watch.switch-off` (`:225-231`):** "my bunk ladder... my bunkmates" needs `rank:junior` (officers have cabins).
  The best sample on the page; it's the model for the friend tier (S10).
- **`work.bridge.long-turn` (`:233-239`):** `dept:helm` (S3). The cheer "Waiting for dinner. Every evening." is a
  food joke, and the pack is already heavy with them (45 of 160) → `cheer: Waiting for the lift on a Monday.` /
  `them: The longest wait aboard. Even the helm can't hurry it.   #funny`

## 8. The answer form (`:244-301`)

Markup is exactly as specified: `form#answers`; `div.q` with `data-qid` `wp-q1`...`wp-q6` and `wp-general`; radios
`name="wp-qN"`, recommended option first and marked; `textarea name="wp-qN-comment"`, and `wp-general-comment`. No
option is pre-ticked (good: the user chooses).

- **N4.** The page has no script and no capability, so nothing is kept until the publisher wires `form#answers` to the
  artifact's store (CLAUDE.md: "a page that keeps what the user writes"). Say in the hand-off who does that.
- **N5.** Each question's options are in a `div` with a `<p>`; a `<fieldset>` with a `<legend>` would let a screen
  reader say the question before each option. Optional.
- **N6.** If S6 and S7 are taken, question 1's recommended option changes and question 2's wording changes; keep the
  `value`s stable (`own-work-shared`, `mixed`...) so anything reading the answers still works.

## 9. Phone at 390 px

Checked in Chromium at 390 × 844: `scrollWidth` 390, no sideways scroll. The nav chips and the two tables scroll
inside their own boxes, as designed.

- **N7.** The pools table has four columns; at 390 px "Odd cases" is off to the side and easy to miss. Consider stacking
  it (cards, as the "More personal" grid does) or dropping the "Who's in it" column on narrow screens.
- **N8.** The page is dark only. The artifact rules ask for colour tokens on `:root` with a light and dark version;
  fine for a plan page in this repo, but if it's published as an artifact, the publisher should add the light set.

## Small wording nits

- **N9.** `:61` "Nothing is written or built yet beyond the samples here" → also say the 160 talks already got the
  user's decision and TR1's fixes (so the reader knows what "unchanged" means).
- **N10.** `:117` "two hundred and six doors" is Holt's own talk; the example reads as if a Watch rating says it. Use a
  sample's own line: "if a Watch rating has told you how a tired door sounds, no other Watch rating tells it again".
- **N11.** `:124` "at least six a pool": the Store has 6 for 2 people (1 after skips): see S9.
- **N12.** `.md` "Odd cases" for Works says "engine-room talks for the 7 engine crew": 6 at any one time (Keane leaves
  on 161 as Kowal arrives).
