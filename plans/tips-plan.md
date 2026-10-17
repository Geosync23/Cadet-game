# Teaching tips, need warnings and the "need to go" pose (player engineer 5, builds 0.28.41+)

The user's three asks after playing 0.60.3. All in section 15 (plus one no-prop pose row in 8b's `HOLDS`).

## 1. Bursting for the toilet (bathroom at 0)

- At bathroom 0 your figure walks in a new `'+go'` pose: hands clasped low in front, knees in, short quick steps, a little jiggle when standing. No prop, so no new draw calls; colours untouched.
- You walk at 70% (`GO_SPEED`, in `needEffects`, so the device's Needs page says "Walking at 70% speed" and "Bursting for the toilet").
- Both end the moment bathroom is above 0 (a toilet fills it in 3 minutes). Hands full (cart, tray, parts): the hold wins, the slow walk stays. Nothing saved.

## 2. Need warnings

- **Gentle** when a need first drops below 25 (the low line the device already shows in amber, where the penalties start). **Firmer** below 10.
- Each says what it means and what to do (draft text below). **Re-arms** only once the need is back to 40 or more.
- Shown as the normal toast, titled with the need ("Hungry", "Tired" ...). One at a time; never while a toast, tip card, dialogue, a panel (device, lift, job board, health board, chat, sleep prompt, queue prompt) is up, or while asleep or riding the lift. If two are due, the lowest need goes first, the other waits for the next quiet moment (8 s after the screen clears).
- They replace the two old "you walk slower" toasts for energy and fitness. Not switched off by the Tips setting (they're about you, not teaching), but the intro holds them until it's over.
- **What happens at 0 today:** there's no fail state. Below 25 the penalty applies and stays the same down to 0. Food: tasks 15% slower. Energy: walk at 80%. Hygiene: chatting does half the good. Fitness: walk at 80% and tire sooner. Social: tire a little sooner. Bathroom: tasks 10% slower, and now at 0 the pose and 70% walking.

| Need | Below 25 | Below 10 |
| --- | --- | --- |
| Food | You're getting hungry, and hungry work goes slowly. The mess on Deck 3 serves breakfast 06:00-08:00 and dinner 17:00-20:30; the grab-and-go shelf there is always open. | You're very hungry: tasks are going 15% slower. Get something to eat at the mess on Deck 3; grab-and-go is always open. |
| Energy | You're tired, so you walk slower. Sleep in your bunk (Bunk 1, Deck 4) from 20:00; by day, lying down or sitting rests you. | You're exhausted. Get to your bunk in Bunk 1, Deck 4, and sleep it off. |
| Hygiene | You could do with a wash: people enjoy your company less. The showers are in the washrooms at either end of the junior wing, Deck 4. | You really need a shower. Chatting does half the good until you've had one: washrooms at the ends of the junior wing, Deck 4. |
| Fitness | You're out of shape: you walk slower and tire sooner. A session on the treadmill or the weights in the gym on Deck 3 will help. | You're badly out of shape. The gym on Deck 3: even one workout makes a difference. |
| Social | You're feeling a bit lonely, and tire sooner for it. Chat with someone, eat with company, or call home from the booths on Deck 3. | You're really missing people. Call home from the booths on Deck 3, or find a friendly face and say hello. |
| Bathroom | You need the toilet. The public washrooms are on Deck 4 (the junior wing) and Deck 3. | You really need the toilet, now! Washrooms on Deck 4 and Deck 3. If it gets to nothing, you'll be hopping. |

## 3. Teaching tips

- About 30 tips, each shown **once ever**, each triggered by first-time context (list below; order = priority when several are due).
- Shown with the device's existing tip card (`tipShow`: "TIP", tap or 9 s to close). Seen flags are the device's existing `SHIP.device.tipsSeen` (saved); ids are short (`t:` plus a word), about 0.5 KB for all of them.
- **Pacing:** at most one teaching tip every 3 real minutes; none within 60 s of another tip card, need warning, dialogue or heads-up; none within 6 s of an ordinary toast (toasts come with nearly every tap, so 60 s after those would almost never let a tip through). None while a toast, card, panel, dialogue, sleep, lift ride or the intro is on. App tips may show over the device (they're about the app on screen); nothing else does.
- A tip whose moment passes (you left the queue) simply waits for the next time it fits.
- **Turning them off:** the device's Settings already has Tips on/off (`settings.tips`); off means none show and none are marked seen.

| Id | When | Draft text |
| --- | --- | --- |
| t:needs | A need first under 50 | Your needs are in the strip at the top: food, energy, hygiene, fitness, social and bathroom. Keep them up and things go better; let them drop and they slow you down. |
| t:queue | First time in the meal queue | The line moves on its own. When it's your turn you get a tray; tap anywhere if you'd rather leave. |
| t:tray | First tray in hand | Take your tray to any free seat and tap it to eat. Eating with company lifts your spirits too. |
| t:lift | First arrival on a new deck by lift | Six decks, one lift. Maps on your device shows where you are and what's on each deck. |
| t:deck3 | First time on Deck 3 | Deck 3 is the Commons: the mess, the gym, the crew store, the call-home booths and the promenade. |
| t:deck5 | First time on Deck 5 | Deck 5 is Operations: the Works bay with the job board, main storage and the machine shop. Your shift is here. |
| t:shift | A work day, 07:30-08:00, first time | Your shift runs 08:00 to 17:00 in the Works bay, Deck 5. Pick up a job from the board when you get there. |
| t:dayoff | First day off, after 07:00 | Day off! No shift today. The time's yours: the garden, a game of Tiles, a long call home, or nothing at all. |
| t:fault | First failing machine you can see | See that blinking light? A machine is struggling. Faults become jobs on the board in the Works bay, and the Ship app shows how everything's holding up. |
| t:pay | First credits from a job | Credits! Spend them at the crew store on Deck 3: snacks, and small comforts for your locker. Some make good gifts. |
| t:carry | First time carrying parts | Parts in hand. Fit them at the job's machine; anything you don't need goes back to main storage. |
| t:gift | First gift in hand | You're carrying a gift. Tap a crewmate to give it; everyone has their favourites. |
| t:chat | After your first chat | Chatting lifts your Social. The first chat with someone each day counts most, and it's how strangers become friends. |
| t:tier | First time you get on better with someone | You're getting to know someone. Chats, meals together and favours take you from stranger to acquaintance, colleague, friend and close friend. |
| t:friend | First friend | A friend! Friends save you a seat, invite you along to things and sometimes leave a note on your bunk. |
| t:mail | First Mail after the welcome | New mail. Read it in Mail on your device. Ship traditions are announced the evening before. |
| t:trad | First tradition on today, from an hour before | There's a ship tradition today. Turn up and join in: it's how the crew keeps the long voyage cozy. |
| t:hu | After the first heads-up | Heads-ups remind you what's coming up. Change how early, or turn them off, in your device's Settings. |
| t:sleep | After your first night's sleep | Your bunk sleeps you through to 06:00 from 20:00. By day you can lie down in it to rest, or sit anywhere to slow the tiredness. |
| t:late | Awake after 22:00, first time | It's getting late. Your bunk's in Bunk 1, Deck 4. Stay up if you like; you'll feel it tomorrow. |
| t:sit | Energy first under 50 | Tired? Sit down anywhere for a bit: it slows the tiredness. Lying on your bunk rests you properly. |
| t:food | Food first under 50, outside meal times | Missed a meal? The grab-and-go shelf in the mess on Deck 3 is always open. |
| t:loo | Bathroom first under 50 | Public washrooms are on Deck 4 (the junior wing) and Deck 3. Cabin bathrooms are private. |
| t:gym | Fitness first under 50 | The gym on Deck 3 has treadmills and weights. A workout every few days keeps you fit and quick on your feet. |
| t:call | Social first under 50 | Missing home? The call-home booths on Deck 3 put you through to family. |
| t:bonus | First time a need gives a bonus (75+) | Needs kept high give bonuses: well rested, tasks go faster. The Needs app on your device shows what's helping and what's holding you back. |
| t:view | About 5 minutes into play | Rotate turns the view and Walls lowers them so you can see into rooms. Pinch or scroll to zoom. |
| t:a-sched | Schedule app first opened | Your day at a glance: meals, your shift and anything booked. Tap an entry and the marker shows the way. |
| t:a-cal | Calendar app first opened | The Calendar has the weeks ahead: days off, traditions, birthdays and appointments. |
| t:a-maps | Maps first opened | Every deck, room by room. Tap a room to set the marker there. |
| t:a-jobs | Jobs app first opened | Your job and its steps. The board in the Works bay has the rest. |
| t:a-crew | Crew app first opened | Everyone you've met, and how well you know them. |
| t:a-needs | Needs app first opened | Your needs, and what each one is doing for you right now: ▲ helping, ▼ holding you back. |

The existing tips stay as they are (device, walk, board, taken, machine, turnin, tiles-nobody: shown at once, in context, by their owners); the pacing applies to the new ones only.
