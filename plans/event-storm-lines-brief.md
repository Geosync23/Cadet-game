# The ion storm, story A "Sixty by lamplight": the lines brief for the writer

Event planner EP3, 2026-10-21, for the events writer (EW1, or whoever holds the seat). Lead 22 assigns it. The plan is `plans/event-storm-plan.md` on `claude/event-plan-storm`; **the user chose story A and the plan's (a) answers (02:29 UTC).** Planning only: these lines go to `plans/events-ready/ionStorm/` first, like your other storm files, and the builder moves them into `content/` in turn S7.

## The story in four lines
Brennan is off on Friday Day 12 and Saturday Day 13 (her rota; facts.md: "Lukas Dlamini covers for Brennan Fri-Sat"), so Lukas runs her galley alone through the storm's two worst days, and Saturday's lantern supper (18:00-19:30, the mess by lamp light, about 55-60) is his. The 11:20 surge leaves his range with two rings of six. You choose: fix the range, carry his question to Brennan, or tell him two rings is plenty. Brennan comes to the supper to eat (she's off; her own day has her in the mess then), and says one line by your choice.

## Who they are (from their cards and facts.md)
- **Lukas Dlamini:** galley junior, eight months aboard, from Port Halloran, berth 5 in Bunk 1. Few words, all dry; says the true thing, then is kind about it; **says a number out of nowhere**; claims Brennan's galley "runs itself" on her days off while visibly running it. Cares that Brennan's galley doesn't slip on his watch. Tariq leads him at onions, 41 to 38. His aunt was a pilot. Words: hi "Hey / You again / Hm. Hello"; thanks "Ta / Appreciated"; yes "Fine / Suppose so / Go on then"; sigh "Typical".
- **Chef Auda Brennan:** calls everyone "love"; cooks by ear, listens to the pans; proud and warm; on her day off she can't keep out of the mess ("just watching Lukas cook. Closely.").

## Guard rails (check every line)
- **Lukas:** only tonight's supper, the range, the storm and Brennan's galley. **Never** his own worry theme (`notgood`: a mistake on an old ship, checking his work twice), the person he married (unnamed in facts.md), or his count of days until home.
- **Brennan:** **never** her own story: the restaurant, the fire, Port Halloran's past, her mother's soup, blue sage, Nell Arrowby or Hesper Dock, her book of favourite dishes, leaving. **And nothing that hints at handing the galley on**: no "he's ready", no "one day it'll be yours". "His galley" is for tonight only.
- **Your rank and cabin aren't assumed.** The promotion can run late, so you may still be his bunkmate in Bunk 1 on Day 12. Write the Friday lines in two versions where it shows: `? flag:cabin.moved` (you've moved to the officers' corridor: "since you moved") and `? !flag:cabin.moved` ("bunkmate"). The builder names the real flag; write it as `{moved}` versions if simpler. "I'm Works" works at any rank.
- **Calder** never says "well done" (her arc's payoff), if she appears at all.
- **Nothing about the Veyli** or the visit.
- **The dead rings are words only.** The galley's food still comes out on time, so nobody says the supper was late or short.

## What's needed (about 30-35 lines)
Lengths: bubbles 60 characters, cards 90, meeting lines 140, Mail 400 (the `event.*.mail.*` rule you asked lines_check for). Placeholder `{me}`. Replies carry `flavour:` and `flag:` as in `lineTomasSat`.

1. **`stormLukasFri.meet`** (a moment, section 20c; Friday Day 12, 17:00-20:30, at the servery or in the galley, when you're near Lukas). About 6 lines plus three replies:
   - his opener is a number: "Sixty." Then what it means: covers, tomorrow, the lantern supper by lamp light, on her day off, his galley;
   - replies: practical "I'll give you a hand tomorrow." (`flag:storm.lukas.promised`; he answers dry and pleased); cheer "She left you in charge for a reason." (he: she left him a list, eleven of the twelve lines say don't panic); listen "What's the worst that could happen?" (he just says the number again);
   - the bunkmate/moved versions where his greeting shows it.
2. **`event.ionStorm.mail.lukas`** (bank): his Mail at about 20:50 if you didn't meet him. One line, his voice, e.g. "Lantern supper tomorrow. If you've got hands, I've got onions." (Subject | body.)
3. **`stormLukasSat.meet`** (a moment; Saturday 14:30-17:00, the galley). About 6 lines plus three replies:
   - the situation: the surge took four rings; Works has a list and he's near the bottom; sixty bowls on two rings, or he goes and knocks on her door;
   - practical "I'm Works. Let me look at it." (`flag:storm.lukas.fixed job:stormRange`; he: "Six rings. Huh. Not bad." or his own words, said when the job's done, see 4);
   - share "Ask her. I'll go." (`flag:storm.lukas.asked`; he lets you, reluctantly);
   - cheer "Two rings is plenty. Stew's one pot." (`flag:storm.lukas.own`; he nearly laughs: his aunt cooked on two rings in a cockpit for twenty years; he'll make hers).
4. **The range fixed:** one bubble from Lukas when `stormRange` is done (`event.ionStorm.lukas.fixed`).
5. **The errand to Brennan** (`stormBrennanErrand.meet`, a short moment wherever her own plan has her on Deck 4): she won't come in ("It's his night."), and sends back: *"Tell him: one pot, low and slow, lid on. And tell him it's his galley tonight."* Then one bubble from Lukas when you bring it back (`event.ionStorm.lukas.asked`).
6. **The job titles** (bank): `event.ionStorm.job.stormRange` ("Storm: reset the galley range"), `event.ionStorm.job.stormLanterns` ("Lantern supper: carry the lanterns up from storage"). Cards, 90 characters.
7. **Brennan at the supper** (`stormLanternBrennan.meet`, a short moment at the supper, 18:05-18:32, when you're in the mess). Her three lines, by flag (the plan's drafts, yours to improve):
   - `fixed`: "Six rings on a storm night. Somebody's been in my galley with a spanner." then to Lukas: "Good."
   - `asked`: "Low and slow. He listened. Nobody listens."
   - `own` or none: "That's not my stew." A pause. "Make it again on Friday."
8. **Lukas at the end of the supper:** one bubble, a number: the covers (`event.ionStorm.lukas.covers`, e.g. "Sixty-one.").
9. **The crew retelling** (reactions, `event.ionStorm.afterglow` or the resolution file, from Sunday): 3-4 lines, e.g. "Lukas ran the lantern supper on two rings. Or six. Depends who you ask."; one from a galley hand (Tariq or Agnes, one week aboard); one from Brennan on Sunday, in her galley again, about her pans being where she left them (or not).
10. **The trace:** one tap line for the storm lantern left on the galley pass (`event.ionStorm.trace.lantern`), a card.
11. **Notices** (one line each): the lantern job posted at 14:00 Saturday ("held for you" version too).

## Hand-off
Push to `claude/events-lines` under `plans/events-ready/ionStorm/`, tell lead 22 and the builder the hash, and note any line that needs a flag or key the builder hasn't named. The head writer checks the guard rails before S7.
