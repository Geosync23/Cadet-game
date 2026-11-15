# Pay and things to buy: the plan (piece E, R2_PAY_ON)

W3 for lead 52, 2026-11-15. Plan only: nothing in the game has changed. Base: claude/staging-fable-review (0.99.92-review).
The user's decision: "Pay by the job's length and parts, and add more to buy."
Also decided the same day, and counted in below: no paid board jobs before clocking in at 09:00; no daily stopping point;
reputation's pace and the Day 9 promotion stay as they are.

For the user: the five questions are at the end. Each has my recommendation; a yes or no to each is enough.

## 1. How pay works today (read from the code)

**Money in.** You start with 40 credits. After that the only income is 15 credits for a finished job (`JOB_PAY = 15`,
one number in section 15). There is no wage, and nothing else gives credits.

**The 15 is paid in three separate places, and some jobs miss all three:**

| Job | Minutes of work | Parts | Paid today |
|---|---|---|---|
| Repair on a machine | 22 to 24 (about 29 at the next rank) | 2 fetched from storage, sometimes 1 made at the lathe | 15, at the machine |
| Service on a machine | 12 to 13 | 1 | 15, at the machine |
| Overhaul (a broken machine) | up to 40 (the game's cap) | 3 | 15, at the machine |
| Calibrate, small fault, filters, pressure seal | 10 to 20 | 0 or 1 | 15, at the machine |
| Small repair from Chief Calder ("fix") | 10 to 20 | 0 or 1 | 15, at the board |
| Lamp, vent, delivery, burst joint, inspection round | 10 to 20 | 0 or 1 | 15, at the board |
| Cart run (restock) | 33 | none | 15, when the cart is docked |
| Tuning a machine | a minute or two of your own turning | none | **nothing** |
| Morning rounds, manifest run, stocktake, incident, leak, rewire, nozzles and the later trained jobs | 4 to 13 | none | **nothing** |

So "every job pays 15" is nearly true but not quite: the newer kinds of job (the ones added with the career) were never
connected to pay. On the board about one job in four is one of those. The review's own totals agree: 203 jobs turned in,
but 1,485 credits earned, which is 99 payments.

Rank does not change pay. A higher-rank job only takes longer (a quarter longer per rank). Training makes you quicker
at a job, and today that makes no difference to pay.

**Money out.** Meals in the mess are free. The only things that cost credits:

| Where | What | Price |
|---|---|---|
| Crew store, snack shelf | dried apple, chocolate, spiced nuts, flapjack, biscuits (a little food) | 2 to 3 |
| Crew store, fridge | fizzy lime, cold tea, oat milk, a tin of tea | 2 to 4 |
| Crew store, window display | novel, socks, postcard, little plant, cards, candle, puzzle book, music chip, pocket puzzle, tiles set (a little social; several are gifts for crew; three can sit in your cabin) | 3 to 10 |
| Crew store, window display | the three hobby kits: sketchpad 15, needles and wool 12, puzzle book 10 (once each) | 10 to 15 |
| The bar, evenings | tea, juice, fizz or cocoa | 2 |

Everything in the game can be bought once for about 110 credits. After that the only spending is 2 or 3 credits at a time.

## 2. The proposed pay rule

One rule for every kind of job, shown on the job's card on the board ("Pays 16") and paid when you turn it in:

> **4 credits for the job, plus 2 for every five minutes of work, plus 2 for each part you fetch, plus 6 if you have to make a part at the lathe.**

- "Minutes of work" is the job's standard time at the job itself. Walking does not count
  (it would pay you for dawdling), and being trained and quicker does not cut your pay.
- No rank bonus. Higher-rank jobs are already longer, so they already pay more under the rule.
- Every kind is paid, including the ones that pay nothing today.

What that comes to, from the jobs the game actually posted over three weeks:

| Job | Today | Proposed |
|---|---|---|
| Tuning | 0 | 4 |
| Incident, leak | 0 | 6 |
| Morning rounds, stocktake, inspection round, small fault | 0 or 15 | 8 |
| Manifest run, calibrate, pressure seal, delivery | 0 or 15 | 10 |
| Service (1 part) | 15 | 10 to 12 |
| Small repair from Calder | 15 | 8 to 14 |
| Lamp (1 part), vent | 15 | 12 |
| Filters, burst joint (1 part) | 15 | 14 |
| Repair (2 parts) | 15 | 16 to 18; 22 to 24 with a part made |
| Cart run | 15 | 18 |
| Overhaul (3 parts) | 15 | about 26 |

The average job comes out at 11 to 12 credits, a little under today's 15, but a long repair with parts now pays four
times what a quick tune pays.

Not paid, as now: the Wednesday drill (a duty), favours for crew (a kindness; they pay in friendship), and training
lessons. The team job is paid like any other. This is question 2.

## 3. What a player earns

Two players, both taking jobs only after clocking in. You work five days in seven.

- **The steady player** (measured: the game's own job list run on paper for 21 days; one job an hour at most, about six
  a working day).
- **The arrow-follower** (estimated from the review's automatic player, who did 203 jobs in nine days starting at 06:00;
  starting at 09:00 that is about 18 jobs a working day).

| Credits per week | Today's flat 15 | Proposed rule |
|---|---|---|
| Steady player, week 1 | 390 | 342 |
| Steady player, week 2 | 405 | 390 |
| Steady player, week 3 | 315 | 320 |
| Steady player, a working day | about 75 | about 70 |
| Arrow-follower, a week (estimate) | about 800 | about 1,000 |
| Arrow-follower, a working day (estimate) | about 160 | about 200 |

In plain words: the new rule makes jobs feel different from each other, but it does not make the player poorer. The
arrow-follower earns slightly more, because the unpaid jobs become paid. Over three weeks that is about 1,050 credits
for a steady player and about 3,000 for someone who follows the arrow all day, against 110 credits of things to buy.
**The rule alone does not fix the review's finding. The things to buy do.** That is why the list below is priced in
tens and hundreds, not ones.

(The arrow-follower's figures are an estimate, not a measurement. When the build is made I would run the automatic
player again to confirm them.)

## 4. More to buy

Chosen to reuse what the game already has: the store's shelves and till, gifts and crew tastes, the cabin's four display
spots, the hobby meter, the bar, Mail from home. Build size: cheap = a few table rows and words; medium = a new small
behaviour or a new shape to draw; big = a new system.

| # | Thing | Price | What it does, where it shows | Build |
|---|---|---|---|---|
| 1 | Better gifts at the store: a boxed tea set, a star atlas, a tin of good chocolates, a record of old songs, a board game, a potted fern | 20 to 35 each | Given to crew like today's gifts, to the tastes they already have; a loved one counts for more than a postcard does. Repeatable, so it never runs out | cheap |
| 2 | Buy a round at the bar | 8 | Everyone at the bar with you gets a drink; a little friendship with each. Repeatable | cheap to medium |
| 3 | A tin of biscuits for the Works tea corner | 15 | Put on the tea table before 13:00; the Works crew at tea warm to you that day. Repeatable, once a day | medium |
| 4 | Better hobby kits: a box of paints, fine wool, a thousand-piece jigsaw | 40 each | Each makes that hobby give more leisure per sitting. Needs the first kit | cheap |
| 5 | Store-bought cabin things: a framed photo of home, a reading lamp, a striped rug, a model of the Wren, a bigger plant | 40 to 90 each | Shown in your cabin on the four spots that exist (floor, desk, shelf, ledge), beside the things you can already make in the workshop | medium (each needs a small shape) |
| 6 | A sixth set of clothes | 60 | One more clean day between laundry trips | cheap |
| 7 | A parcel home | 50 | Sent from the store counter; a few days later Mail from home thanks you for it. A few times, different replies | medium (needs the writer) |
| 8 | A second cabin shelf | 120 | Two more places to show things in your cabin | medium |
| 9 | A ukulele | 250 | A new hobby, played in the music room or your cabin; sits on the cabin shelf when not in use. The thing to save up for | medium to big |
| 10 | An off-duty jumper, in a colour you choose | 80 | Worn after clocking out instead of the uniform | big (the player's look changes) |

One of everything that is bought once comes to about 1,050 credits, which is three weeks of a steady player's pay, plus
the repeatable things (gifts, rounds, biscuits) for the player who earns more. So a steady player always has something
ahead to save for through week 3, and the arrow-follower runs out of one-off things around the end of week 2 but still
has people to treat.

The Wallet app would also list "Saving for" (the thing you picked) so the money has a visible aim. Cheap.

## 5. What I recommend building first

**First build (one update, behind the switch R2_PAY_ON; with it off the game is exactly as now):**

1. The pay rule, paid at the board on turn-in for every kind, with the amount on the job card and in the turn-in message.
   About one function and three small edits where 15 is paid today. Works with W2's clock-in piece: a job you cannot
   take, you cannot be paid for.
2. Items 1, 4 and 6 (better gifts, better hobby kits, the extra set of clothes): all cheap, all on existing shelves.
3. Item 5 with three cabin things to start, and item 2 (a round at the bar).
4. "Saving for" in the Wallet.

That gives about 350 credits of one-off things and two repeatable ones. Checks: player_check, interactions_check,
clothes_check and saves_check extended for the new pay and purchases, a re-run of the automatic player for the income
table, then the full round of six.

**Second build, if the user likes the first:** the parcel home (needs the writer), the tea-corner biscuits, the second
shelf, the ukulele. **Later or never:** the off-duty jumper, which is the only big one.

The design document's money paragraphs are updated in the same commit as the build, as the rules say.

## Questions for the user

1. **How much should jobs pay overall?** The rule above keeps a job at about today's level (average 11 to 12 credits,
   from 4 for a tune to about 26 for an overhaul). The other way is to halve everything and keep prices low.
   Recommended: keep it at today's level and price the new things in tens and hundreds, so today's snacks and drinks
   stay pocket money.
2. **Should every kind of job pay?** Today tuning, morning rounds, manifest runs, incidents and the later trained jobs
   pay nothing (an oversight, not a decision). Recommended: yes, all paid by the same rule, except the Wednesday drill,
   favours for crew and training lessons.
3. **Should all pay arrive when you turn the job in at the board?** Today machine jobs pay at the machine and the rest
   at the board. Recommended: yes, all at the board, with the amount shown on the job's card beforehand.
4. **Is the first set of things to buy the right one?** Better gifts, better hobby kits, a sixth set of clothes, three
   cabin things, a round at the bar. Recommended: yes. Tell me anything on the list of ten you would rather have first,
   or do not want at all.
5. **Should there be one big thing to save up for?** Recommended: yes, the ukulele at 250 credits, in the second build.
   If you would prefer a different big thing (something for the cabin, something to wear), say which.
