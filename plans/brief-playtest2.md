# Playtest update 2 brief, lead 16, 2026-10-19 ~05:15 UTC (overnight)

The user's playtest notes (~05:12). Goal: fold into Step 4 (0.63.4) if ready when BM7 builds the final; otherwise its own build 0.63.5 right after Step 4, before the rec deck activation (the user: "totally fine"). Base: the 0.63.3 final (claude/p5-cand-pt1 7a6e137 + its last fix; the lead confirms). Same rules as `plans/brief-p5s4.md` (small edits, determinism, phones first, old saves load, one owner per function, HUD build number + DEV_NOTES row, checks for what you touched, cadet_test explained). Report to lead 16 (session_01UMyfd16GqSdgNyz5PE8qSv); hashes to BM7 (session_01QbuzvT3TwzMwSWRmakzX8Z) and R4 (session_01UGQxniXCxT5TLEE4tgRLfJ). New lines → W2 (session_01866TWKzGRgZmFcxiYRi4db), who bakes them.

## Items and owners
| # | The user's note | What to build | Owner |
|---|---|---|---|
| 1 | "This training is bugged" (Day 2 rounds with Torres) | Replace the walk-along: Torres **explains** rounds (a short talk), then the first round is **a new job on the job board**; taking it, the **goal arrow and green tips walk you through** each stop (look, mark). Same rounds code after that. | E1 (owns rounds, 24a) with U for the arrow/tips |
| 2 | The Chief isn't at the Day 1 dinner with Zeke | Calder (the Chief) sits at that dinner as written | X |
| 3 | Call-home marker doesn't appear after meeting the Chief | The call-home goal/marker shows right after the Chief's table visit (0.42.62 flow) | U |
| 4 | Toilet use should drop hygiene | Using a toilet lowers hygiene a little, shown with the usual pop-up "−N Hygiene" numbers | U |
| 5 | Energy: burns faster; alarm clock to manage bed time; extra sleep if needed; the alarm shows how much energy you'll recover | Energy drains faster awake (lead's tuning: a normal 16 h day ends near 20-25%); an **alarm clock** when you go to bed: pick the wake time (default as now), it shows the energy you'll wake with; sleeping longer gives more; never miss a shift silently (a warning if the alarm is after your shift starts) | U (with X if crew wake logic is touched) |
| 6 | Auto-track the time clock at 08:50 on your first shift | When it's 08:50+ before your first shift and you're in the Works bay, the time clock is tracked automatically (arrow + highlight) | U |
| 7 | Then highlight the job board | After clocking in, highlight the job board to take a job, the same way the turn-in is highlighted | U |
| 8 | Cargo loaders' hands are empty while loading | Hold a crate/weight prop in their hands during the loading animation | X |
| 9 | Green tip on training day | "Working is a good chance to check out your device" (once, on the training day) | U + W2 |
| 10 | Tea break on the Schedule like meals; only a tiny bit of food | Tea breaks listed in the Schedule; tea adds only a small amount to the food need | U |
| 11 | Wednesday delivery on the Schedule | List it | U |
| 12 | Appointment notifications | Appointments (summons, training, ceremony, talks) get the same 15-minute + start notifications as Schedule items | U |
| 13 | Couldn't tap the Name Beam | Tapping the beam during the tradition lets you add your name | X |
| 14 | Everyone should say welcoming things once you do | After you add your name, nearby crew say welcoming lines | X + W2 |
| 15 | Call booth queue, with a message saying your place in line | A queue at the booths; a small message "You're 2nd in line" | X (queue) + U (message) |
| 16 | Rower: the bar doesn't move | The modelled handle moves with the rowing animation | X |
| 17 | Green tips shouldn't repeat | Each green tip shows once per save (saved; old saves: none seen) | U |
| 18 | Lift panel floor 2 label | Deck 2 reads "Officers' quarters and science" (keep the change tiny: the lift panel is where the rec deck merged) | U |
| 19 | Day 2 laundry tip at the top of the day | The laundry green tip appears at the start of Day 2 | U + W2 |
| 20 | Shower queue | A visible queue at the showers with the same place-in-line message as the booths | X (queue) + U (message) |
| 21 | Crew wake up earlier | Shift wake times earlier (lead's tuning: about 30 min earlier) | X |
| 22 | Too many crew wake and go to breakfast at once | Stagger wake and breakfast times across the crew (deterministic, seeded) | X |

U's list is long: do 3, 6, 7, 17, 9, 19 (onboarding and tips) first, then 10-12, 18, then 4-5 (needs and the alarm clock; the biggest). Tell the lead at ~60% memory; unfinished items move to a fresh seat.
