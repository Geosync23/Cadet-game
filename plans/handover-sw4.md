# Handover: SW4 (writer, "A Veyli vessel needs help")

**Role:** writer for the Veyli vessel (Days 27-30), hired by lead 39 (session_019V68fz33UFv4cK5Z4iCDvi). SW4 is
session_01DgMynb62u2rTUA9RocZi65. Took over from SW2 (session_017dLaLFBnRUQin3PQEQq6so; plans/handover-sw2.md on
claude/stories-sw2).
**Branch:** `claude/vessel-words`, from claude/staging-0.93.3 (d9c7e5f0). Content files only, baked into the game with
`content_gen.py` (the baked blocks are the only game change; nothing reads the new keys until VB1's code does).
**Sources:** plans/veyli-vessel-spec.html on claude/p5-specs (the beats table, section 8); plans/events-plan-2.html
Part C on claude/events-plan-2 (EP1's story and canon notes).
**Builders:** VB1 session_01UsjGN26E88zwrNPWwef4iT (events, key names), VB2 session_01KRBGtugjBpv5iGcV5WDvCP (props' tap
texts). Send each pushed sha to lead 39 and VB1.

## The user's answers (2026-10-26) the words follow

- C1 commendation: yes (`mail.commendation`, the storm's form).
- C2 the ship visible outside: yes (the view lines Saturday, the lights Monday).
- C3 missed at the ramp: Taavek and Calder WAIT at the ramp up to an hour (`vesselRamp.late`, `talk.rampWait`,
  `notice.rampWait*`); only after that Zeke stands in (`talk.rampZeke`, `notice.rampZeke`, `vesselRamp.bench`).
- Pronounced moments with dialogue: replies where they fit, others reacting, a clear close line.
- Not mine unless lead 39 sends it: the Day 30 ending ("Crossing back" + a transfer offer).

## What I wrote

| File | What |
| --- | --- |
| `content/banks/event-veyliVessel.lines` | every key `event.veyliVessel.*`: status by phase; the call (talk.call); breakfast news and Saruth's line; both addresses (address.sat/tue, as "marrow: ..." lists) and their Mails; Calder's parts list; Vance's "Tomorrow"; rings, notices, goals, Tracked and Schedule rows for each beat; the view, the Tern out, the ramp crowd, the wait, the swap meet, the chain (gather.*, chain.count, talk.chain, talk.chainEnd), Sunday evening, the helper card and picks, the five making steps (ring/tracked/taavek/help.<id>.step.N), pair exchanges (help.pair.<a>.<b>, ids alphabetical), lunch, test-fit reactions, going home, the lights (gather.*, talk.lights, lights.you), the turn back, commendation, Taavek's letter, the shelf, tap texts (tap.*, VB2), the afterglow (news.told.N), Record |
| `content/meetings/vesselSheet.meet` | Sat 10:00, Calder, two replies |
| `content/meetings/vesselRamp.meet`, `.late.meet`, `.bench.meet` | Sun 09:30 the ramp (three replies); late (they waited); Zeke stood in, met at the bench |
| `content/meetings/vesselRoundOne.meet` | Sun 10:00, the bench, one choice |
| `content/meetings/vesselJob.meet` | Mon 09:20, Calder; the helper card follows (bank keys) |
| `content/meetings/vesselTestFit.meet` | Mon 13:30, two replies |
| `content/meetings/vesselHome.meet` | Mon 15:00, the sketch, three replies |

Key names are my proposal (sent to VB1); rename to match VB1 if they differ.

## Gotchas

- Bank lines are 90 characters at most, the "speaker: " prefix included. Mail bodies can be longer.
- A bank kind can't contain `+` (hence `help.pair.<a>.<b>`).
- A .meet choice takes only one indented reply line; anything after the choice is heard by every choice.
- "handsome" is on the banned list (romance words).
- Taavek's long Veyli word is never spelled out; Veyli are not described in human terms (no family words for Taavek).
- Zeke did not give the player a pen on Day 0 (EP1's sample said so): he showed you your bunk.

## How to check

`python3 content_gen.py starship-cadet.html`, then `python3 lines_check.py` (PASS, 69 old warnings), names_check,
`bash check_fast.sh`. CS1's `tools/near_dupes.py` (claude/crew-stories-pitch): zero EXACT except the meetings'
`from:` field; the ramp versions are NEAR each other on purpose (the same moment, only one is ever heard).

## Open

- VB1's key names and any rank variants (myrank) they want.
- Lead 39's review of the words.
