# Handover: FX25 (session_01V8edQWJxn9jX4Ddn19Jprf)

Role: builder under lead 38 (session_01G2y9crUv6vDiiEB2q6Yo9W; lead 37 session_019GcNZ4GGEqfiuYDYnue7nX before), the comet viewing for 0.93.2, switched ON (the user's decision).
Reviewer: RV18 (session_01PMfvrCN6StPzwVSPGX7ijH). Build master: BM18 (session_01A3S2VBMYmTt2wCZa8ej7XR): send shas to lead 38, RV18 and BM18 directly. Design: EP1's plans/events-plan-2.html Part A on claude/events-plan-2 (EP1: session_01LjeoeX6qpCuwTV5UNVNwV5).

## Branch and builds: claude/comet (from claude/event-swap 9ab920c)
- 0.93.2-c.1 2f5bf64: the event and its four hosted gatherings (keys 354-357), calendar Day 22 (with or without the swap), rooms closed 21:15-22:45, birthday an hour clear, hosts up late (schedFrame -> cometLate), jobs, Mail, news, status; Pell's practical `!event:comet.warning`; Raman's waiting story's DAY notes.
- 0.93.2-c.2 db72b2a: tap-to-join hosts (TRAD_JOIN), the naming card, Saruth's knot, a Cadet turned from the Captain's tea, the rooms' lines, the Record line, content/banks/event-comet.lines.
- 0.93.2-c.3: the sky comet (COMET_SKY, 1 draw call), the star turn, the dimming, ACTS.look/point (8b's slot), the dressing (basket, cord for good, blankets, teapot, Ravi's sketch 7 days), the keepsake knot, the sound hooks (sndFx('cometTurn'), cometMusicOn()).
- 0c5497f merges SD1's claude/sound-comet-c ff8f141d (the comet track, FX.cometTurn). 0.93.2-c.4: merges claude/event-swap 05a9e7d; RV18's c.2 fixes C1-C4 (cometTalk by distance, no catch-up, cycling; chatter hushed); the Friday address condition `comet` (Day 19 no Tuesday comet, Day 26 looks back); fridays_check excuse.
- Everything is in DEV_NOTES "The comet" and in the build-table rows 0.93.2-c.1 to c.3.

## Switch
`const EV_COMET_ON = true;` (section 13, under EV_SWAP_ON). The data needs EVENTS_ON too. Off: `sed 's/^const EV_COMET_ON = true; /const EV_COMET_ON = false;/'` -> cadet_test vs integration b957b92d ALL IDENTICAL (checked on each turn).

## Loose ends
- The sound is in (SD1's, merged). SD1's sound_check has check_comet_sound.
- The words: SW2 (session_017dLaLFBnRUQin3PQEQq6so) was sent content/banks/event-comet.lines to polish (lead 38's yes); take their commit when it comes, re-bake, check_fast.
- RV18's verdict on c.3 and c.4 is pending; the full round on the runners comes after.
- Numbers on Day 22 of a new game: 32 at the glass, 6 at the scope, 8 under blankets, 5 at the tea (EP1 hoped for about 45 at the glass; many are on nights or have early beds). Raise the hash split in cometData().split if wanted.
- In the stern rooms the sky comet shows only as a faint glow at the top-left of a portrait view; the bow lounge shows it clearly past the glass.
- Raman's story is still "waiting" (not built): its big moment (22:10 at the observatory's back window) needs the story built; Raman is one of the late people.
- join_check timed out at its real-reload step in my container only; CR6 ran it OK on db72b2a and b957b92d.

## Gotchas
- `pkill -f name` kills your own shell; use pids.
- Five checks at once on 4 cores push interactions_check past 50 minutes; run at most three at once.
- The slot's data must be functions or vars: the data block runs at load before the slot's consts exist (TDZ).
- Probes: put screenshots in the scratchpad, never in the repo folder.
