# Playtest patch for 0.99.5 (the user, 2026-10-31 ~2:30 AM ET, before bed; start after 4 AM ET)

The user's notes, numbered, in their words (tidied spelling only), with the area each touches. Builds on 0.99.4
(claude/staging-0994 8976965e) once 0.99.4 is published (the user's OK still needed for 0.99.4 itself).

| # | Note | Area |
|---|---|---|
| 1 | The tip says Tuesday is laundry day. That's only true the first time; then you have 5 outfits and the day changes. Remove that tip; teach laundry in general. | tips / onboarding |
| 2 | With a controller it's too hard to talk to people while sitting next to them in the mess hall. | controller |
| 3 | Add the sit button to all chairs, not just the mess hall. | player / interactions |
| 4 | Mess hall murmur should scale with the number of people inside; empty = no murmur. | sound |
| 5 | With a controller you can't pick "Go there" when it pops up in the corner: needs a button prompt. | controller / heads-ups |
| 6 | Controller right stick: invert the horizontal axis for camera turning. | controller |
| 7 | Zeke stops following you briefly on training day near the end of the shift. He must stay with you to take you to Name on the beam. | onboarding / Day 1 |
| 8 | Name on the beam: nearly perfect, but where you stand to write isn't where the name goes. Scoot the player over (where it's written is nice). Crew speech buttons cover the name: slide those crew over. | traditions |
| 9 | In a browser on Android, switching to another window pauses the game but the audio keeps playing. | sound |
| 10 | Tea and biscuits: nobody sits down, they just walk up to it. And they trap you: you can't get round them to leave that small room. | crew sim / Works tea corner |
| 11 | Rina's Day 2 appointment no longer says "new crew check-up". Appointments must say what they are, not just who and where. | appointments / device |
| 12 | Talk a while counts down minutes left in the conversation and always ends early. | social |
| 13 | All the officers' quarters doors on Deck 4 open automatically even with the default door setting. Those are private doors and should be locked. | doors |
| 14 | "Your first rounds" makes no sense: it asks you to report a machine's status with no sign of how it's running. Make it a quick tour of checks, on different machines and items around the ship to keep it interesting. | jobs / career |
| 15 | Jobs keep sending you back to the exact same spots (so many washer visits). Vary job locations much more: there are many places on the ship to go and fix things. | jobs / machines |
| 16 | The new crew health check does nothing, doesn't trigger. Make it like a ship tradition: tap the doctor and a moment starts. | appointments / social |
| 17 | Long play sessions: audio glitches start; lots of popping and crackle after some play. | sound |
| 18 | No job or machine shop task should be more than 40 minutes, and that length shouldn't be common. | jobs / machine shop |
| 19 | Spice shelf supper does nothing, doesn't trigger, nobody to tap. **Hire a reviewer whose sole task is to analyse ship traditions, especially their starts and triggers.** | traditions |

Lead's plan (lead 47): step-1 reports first (cause and fix per note, by seat), then build, RV review, one 0.99.5
staging, full round, the user's OK. Seats: sound (4, 9, 17), controller (2, 5, 6), traditions reviewer TR1 (19 and
a sweep of every tradition's start and trigger; also 8, 10, 16 findings), onboarding/tips (1, 7, 11, 16), jobs (14,
15, 18), player/doors/social (3, 12, 13), traditions builder (8, 10, 19 fixes from TR1).

## Seats (lead 47, 2026-10-31 ~08:07 UTC / 4:07 AM ET), all from claude/staging-0994 8976965e
| Seat | Notes | Session | Branch |
|---|---|---|---|
| TR1 traditions reviewer (review only) | 19 + sweep of every tradition; findings for 8, 10, 16 | session_014zyJYMx26ZwoJgqt2dLUYL | claude/p995-tr1 |
| SD5 sound | 4, 9, 17 | session_014zyJYPA1T75TkyU4en5qbs | claude/p995-sound |
| CT5 controller | 2, 5, 6 | session_014zyJYR3AFNZzzKwMND31qr | claude/p995-controller |
| OB2 onboarding + appointments | 1, 7, 11, 16 | session_014zyJYNAM2DgZ8od9tmAhMb | claude/p995-onboarding |
| JB2 jobs | 14, 15, 18 | session_014zyJYMCGakWaNzvpk6S3h5 | claude/p995-jobs |
| PL2 seats, doors, talk | 3, 12, 13 | session_014zyJYMwNf9vLrMDd1uuPFU | claude/p995-player |
| TB3 traditions builder | 8, 10, 19 + TR1's broken list | session_014zyJYRP1bV78VRB3vsquNz | claude/p995-traditions |
Reviewer: RV28 session_014zyJYQKwGvytfCGdrWMoiZ (a second reviewer if the queue grows). Build master: BM22 (staging-0995).
Each builder: step-1 report (cause + fix) to the lead, lead GO, then build.
Reviewers split (~09:48 UTC): RV28 = OB2, SD5, TB3; **RV29** session_014zyJYM3D7UBkZN49CsZVuA (claude/review-rv29) = JB2, PL2, CT5. SW4 polishes JB2's stand-in words (claude/p995-jobs-words).
Reviewers, revised (~09:50 UTC): RV28 finishes JB2 then hands over; RV29 = PL2, CT5; **RV30** session_014zyJYNFR7ewWJGvEQNUAHr (claude/review-rv30) = SD5, OB2, TB3. All builders told.
