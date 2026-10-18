# The user's play-test notes on 0.60.5b, for 0.60.7 (2026-10-17 ~23:40 UTC, verbatim)

> I have notes from playtesting. I think we will need one more pass before going to pillar 5. Take a look :
>
> Need some more instersting traditions to start the first week. Also we are upping to 2-3 a day. We will make many more in Pillar 7
>
> I dont see other works members doing the jobs im doing early on. We dont want ton but some should be repairing and delivering
>
> There shoudnt be a bench in the bathroom on deck.3
>
> Bathroom need builds to quickly
>
> Calendar should only show 7 days ahead.
>
> I want multiple tradition happening a day. 2-3. They can overlap too. Cant see them all.
>
> I want a "met" section in the roster. Then an acquaintance, then friend
>
> Running club ahould be called gym club
>
> Gym club left no room for me, no machines to use
>
> Need more conversation options. They shouldn't walk away when talking. Also have an option to "talk a while" to keep social going. Its a meter like when eating. It builds friendship..Just because you can only talk to someone once a day doesnt mean convos cant be more intersting. Current talk becomes say hello. Once a day too. But way less friendship bump then talking using convo options or the talk a while function. We will write more later in another pillar but do write some new lines ro accommodate this.
>
> Somehow we should give player tips on how to spend free time in the early game. Call home, traditions, social, and the newest addition to the game: hobbies. We shoild make a list of them. Simple things: Reading. Writng. Drawing. Stuff thsts easy to animate and can be done lots of places. Hobbies and doing traditions incrases the newest need: leisure. It goes down very slow.
>
> Lounge needs a bar tender and you should be able to grt s drink
>
> Bathroom need icon should be a toilet icon
>
> Not every bathrooms need showers. Just on command deck and quarters
>
> Need tiles table in  jr common room
>
> Need to change clothes every day by clicking a wardrobe. Will stop working after 5 days, need to do laundry to get it to go again. Juat click wardrobe when out of clean clothes to get a hamped. Take it to washing machine ..take it back to wardrobe to finish. This must be done day w so player sees it early. Zeke warns you.
>
> No weekly laundry duty. You do your own until you move upstairs.
>
> Get .6 out. In the meantime hire a .7 planner for all these features and fixes. Show me the plan when ready.

## Survey answers (2026-10-18 ~00:01, db survey/s0607)
Q1, Q4, Q5, Q8, Q9 (today+6), Q10, Q11 (Deck 2 suite), Q12 as suggested. Q2: add "Play games" on your personal device ("like Sims where it's a meter"). Q3: as suggested + reading and writing on your personal device; a tooltip explains hobbies and where to buy more. Q6: the full roster stays as the main view; another tab for Met / Acquaintances / Friends. Q7: allow all 6 on Saturday.

## More notes (2026-10-18 ~00:02, verbatim)
> You need to grab the right part from the right shelf. Inventory simulated. Shipments come in, must be unloaded. Not too tedious. Hover cart to pull in boxes then click shelves to auto unload . This is a tier 1 and 2 job.
>
> If arrow is presenr then iniactor whixh floor its on when slecting floor panel on elevator.
>
> Two elevator panels, one on each aide to serve any perspectivr

> Oh one last thing the shuttle is good but needs just a little more sleek-ness. Its very boxy.

## Stores answers (2026-10-18 ~00:10, db survey/s0607b)
Q13 weekly Wednesday 10:00; Q14 no penalty, note: "indicator shows you" (a visual pointer to the right shelf); Q15 held till 14:00 then crew where you can see; Q16 crates appear in the hold.

## Carried into 0.60.7 from 0.60.6 reviews (lead)
- Shuffle "Sorry" bubble can evict an overheard line or the arrival escort's line (BUBBLE_MAX 2): only bubble when a slot is free (1g LOW, one line).
- Crew lines in section 22 still lower-case tradition names (ctx.trad ~29190) (PE8).
- Pillar 5 later tidy: option B (shorter seat ray for all chairs) parked by DA3.
- Dinner a little heavier in 0.60.6 vs 0.60.5b (4.0 vs 3.6 ms avg; 13-14 vs 3-5 slow frames/h on phone.py): profile in 0.60.7 (DA3).

## The user's notes after playing 0.60.6 (2026-10-18, verbatim in substance)
For 0.60.6a (quick fix, PE6 on claude/fix-0606a, BM3 checks):
- Clock is cut off in the upper-right corner of the UI.
- The word "Needs" should be by the needs meters.
- The Relationships app label on the device is far too large and overlaps other apps; use a different word if it won't scale and stay readable.
For 0.60.7:
- Zeke is already in the mess hall when you take the lift up to dinner on arrival night (he should arrive with you / not be there ahead of you).
- Get rid of the tray return in the mess hall.
