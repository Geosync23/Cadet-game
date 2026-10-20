# First Light Cocoa: the draft words (PP1, for the writers)

The user's pick for #26 (2026-10-20): "Mix 1 and 3. Mostly just the tips from 3. I like 1. Also need a cocoa at the bar and you can see the mug in your hands." Lead 20's brief:
- The base is idea 1. The lounge dims, someone from the bridge points out where the Wren has been and where she's heading, and mugs of cocoa go round.
- Everyone who arrived this season says one thing they've noticed about the ship. You pick yours from three replies, Talk a while style.
- From idea 3, only the tips: a few long-serving crew each share the one thing they wish they'd known on their first day.
- No pin gift.

This is a **draft** in the writers' formats (`plans/trad-format.md`, `content/README.md`). When the patch is built, the head writer checks the tone, and the files go into `content/traditions/first-light-cocoa.trad` and `content/meetings/firstLightCocoa.meet` through `content_gen.py`, never by hand. The plan's item #26 (`plans/patch-plan.html`) has the design and the build; #29 covers cocoa at the bar and #30 the mug in your hands.

**Who.**
- **Dev Raman**, Senior Helm Officer, hosts. He's the pilot who flew you in on the Tern, so he's the one who knows where she's been.
- **Tomas Lind** speaks for this season's arrivals. He's been aboard one week ("since: one week" in the roster).
- The tips come from long-serving crew: Chief Holt (eight years), Anja Kowalczyk (nine), Chef Brennan (five), Emeka Halloran (five) and Dr. Imra Sato (seven). Three of the five speak, picked per save. Holt's is the user's own example, for fun. The other four are true in the game: Tracked's arrow, breakfast and the grab shelf, the Works log making a job quicker, and the windows' stargazing.

## The tradition (`first-light-cocoa.trad`)

```
@tradition first-light-cocoa
// First Light Cocoa (the user's pick, 2026-10-20; patch plan #26): once, on your first Monday, after Gym club. The bow
// lounge dims; Dev Raman (who flew you in) shows the crew through the big windows where the Wren has been and where
// she's heading; cocoa goes round (you hold a mug: #30); three long-serving crew each give the tip they wish they'd had
// on their first day; then this season's arrivals say one thing they've noticed, and you pick yours (the meeting
// firstLightCocoa). A one-off, so it never clashes with a weekly Monday (Book circle, the Department cup, the Wren talk).
k: <an unused key, picked by the traditions engineer; not 1039 (backlog #10)>
title: First Light Cocoa
when: arrival monday
at: 20:00-20:45
min: 15
where: 3 room Bow lounge: lounge-seat
who: raman always, tomas always, holt always, kowalczyk always, brennan 80%, halloran-emeka 70%, sato 70%, stargazer 60%, window-seat 50%, juniors 35%, everyone 12%
anim: cocoa
host: raman
from: raman
ties: decor firstLightCocoa
ties: meeting firstLightCocoa
invite: host=torres-zeke odds=100% line="Cocoa in the bow lounge at eight. First Light. It's for you, really. Come."

== mail
- First Light Cocoa tomorrow at {time}, the bow lounge. Cocoa, the big windows, and where we're going next. New faces especially welcome. Dev Raman

== ask
- First Light tonight. Raman's doing the windows. I'm doing the cocoa.
- Cocoa at eight, bow lounge. Bring yourself. Mugs provided.
- First Light Cocoa tonight. It's for the new ones. Which is you.   #funny

== here
- Mind the mug, it's hot. Window's that way.
- He tells it better every year. Don't tell him I said so.   #funny
- Look at that. Never gets old.   #warm

== thanks
- The lounge lights go down and someone puts a warm mug in your hands. Out of the big windows, the stars.   #warm

== chatter
- First Light's tonight. I still remember mine.   #warm
- Raman always points at the wrong star first. On purpose, he says.   #funny
- Best cocoa of the season. Brennan won't say what she puts in it.
```

New keys the build needs (the traditions engineer's, ask first):
- `ties: meeting <id>`: play a meeting when you join.
- `anim: cocoa`: the drink pose with the mug prop (#30).
- `invite` from someone who isn't the host: today it's `host=`; here the invite is Zeke's at your Day 1 dinner.
- The lounge dimming. Whether this is `ties: decor` (a few warm lamps, at most 6 draw calls) or a new light tie is for the traditions engineer and the performance engineer (section 5's mood light is set per deck today).

## The moment (`firstLightCocoa.meet`)

It plays in the panel like a Talk a while, because of the three replies.

```
@meeting firstLightCocoa
// First Light Cocoa (patch plan #26): the windows, three tips, then the season's arrivals and you. No wrong answer.
// Holt's tip is the user's own example (for fun); the others are true in the game. Three of the five play, picked per save (? pick 3).
title: First Light Cocoa
from: Dev Raman
gist: First Light Cocoa: Dev Raman showed everyone where the Wren has been and where she's heading, the old hands gave their first-day tips, and you said what you've noticed.
== lines
raman: Lights down, please. Thank you. Right. Mugs up, everyone got one?   [gesture]
raman: Out there, port side. That smudge is the Hollis Reach. We left it six weeks ago.
raman: Dead ahead, too faint to see yet: the Corvane Drift. We'll be there before the season turns.   [point]
raman > you: And somewhere behind us, the little shuttle that brought you. I flew it. Gently.   [laugh]
raman: Old hands. One thing you wish you'd known on your first day. Go on.
? pick 3
holt: Never sit in my chair. Bridge lobby, by the door. That's the whole tip.   [nod]
kowalczyk: Track what matters. Tap it on your device and an arrow takes you there. Saved me years.
brennan: Breakfast is six till nine. Miss it and the grab shelf's always open. Nobody goes hungry on my ship.
halloran-emeka: Write your jobs up in the Works log. You're quicker at them next time. Ask me how I know.
sato: The big windows on the promenade. Five minutes there and the day sits better.   [warm]
? end
raman: Now the new faces. One thing you've noticed about her. Tomas?   [listen]
tomas: The lift hums a different note on every deck. Deck 4's is the friendliest.   [laugh]
raman > you: {me}. Your turn. What have you noticed?   [listen]
? choice
* She never stops. Even at night you can feel her going.   rel:raman+1 flavour:share mem:firstlight.going
  raman: That's the drive. Zeke'll tell you it's coil three. It's always coil three.   [laugh]
* Everyone says hello. Even the ones who look busy.   rel:raman+1 rel:tomas+1 flavour:warm mem:firstlight.hello
  raman: That's the Wren. Small ship, long way from anywhere. We look after each other.   [warm]
* The cocoa's better than the coffee.   rel:raman+1 flavour:funny mem:firstlight.cocoa
  raman: Don't let Brennan hear you. Actually, do. She'll be thrilled.   [laugh]
raman: Right. To the next season, and the new faces in it. Drink up, it's going cold.   [gesture]
```

**Notes for the writers:**
- **Place names.** "Hollis Reach" and "Corvane Drift" are placeholders. Use the Wren's real route from the design doc, or ask the user.
- **`? pick 3` … `? end` is new.** It plays three lines of the block, picked per save. Ask the dialogue engineer. Until it exists, write three fixed tips.
- **Bubble length.** Each line is under 90 characters, so the panel's lines could also be said as bubbles.
- **`mem:` keys.** The `mem:firstlight.*` keys let crew mention your answer later. Tell the social engineer.

## Cocoa at the bar (#29) and the mug (#30)

These need only one new line each from the writers:
- `bar.serve.cocoa`: "One cocoa. Careful, it's hot."
- The finish line: "You finish your cocoa. Warm all the way down."

Ivo Madsen's other bar lines are unchanged.
