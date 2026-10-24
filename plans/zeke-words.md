# Zeke's Day 0 device hand-over: the words (ZW1, 2026-10-23)

## FINAL (the user's pick, 2026-10-23, through lead 30): the mix

The user chose a mix: the bubble order below (DS1's and ZW1's lines, words unchanged; any line over 60 characters
split at a full stop) and DS1's Mail, word for word. The lines are in `content/lines/torres-zeke.lines` (the last
block): `flag:walk.hand` in file order before the Mail, `flag:walk.hand.after` once you close it. The device is
handed over on line 3 (`INTRO_HAND.give = 3`). The Mail goes in as `== mail.zeke.land`.

Before the Mail (`walk.hand`):

1. Oh, hold on. Nearly forgot the important bit.
2. Hands out. Careful, it's still warm from my pocket.
3. And this is yours. Your device. (kept from the green text; the hand-over)
4. There. Officially handed over. I'm a witness.
5. Most important thing you'll own aboard.
6. More than your boots. Slightly less than your mug.
7. Mail, Schedule, the Map, your Needs. The lot. Don't lose it. (kept)
8. It knows where you're meant to be before you do.
9. Annoying, but useful.
10. Needs tells you you're hungry. Before your tummy does.
11. Lose it and you'll spend a week asking strangers what day it is. (64 characters, one sentence with no full stop to split at: kept whole)
12. There. Officially crew.
13. I left you a note in there. Have a look.

The device opens on the Mail. After you close it (`walk.hand.after`):

14. Right, onward. The mess is on Deck 3. (kept)
15. And Brennan doesn't hold plates for anyone. (kept)

The Mail (DS1's, word for word): from Zeke Torres, written that Sunday morning before you landed. In the content
file as `== mail.zeke.land`, one line (`Subject | body`), like his other Mail (`mail.zeke.cabin`): the device shows a
Mail body as plain text, so his Mails have no paragraph breaks in the game. Laid out here for reading only:

Subject: **Before you land**

> New hand, I'm writing this before the Tern docks, so by the time you read it I'll have handed you this in person and said most of it already. Here's the rest.
>
> What do you do first? Dinner. Always dinner first. Then everything else.
>
> Is it always this much? First night, yes. By Thursday it's just home with a lift in it.
>
> And if you're the quiet sort, good. The quiet ones last longest.
>
> Tomorrow, ten to nine, the Works bay. I'll be the one with the tea.
>
> Zeke

### Final map: every green-text line, and where it lives now

| Green-text line (introDevice.meet) | Where it lives now |
|---|---|
| Zeke: "And this is yours. Your device." | Bubble 3, word for word (the hand-over). |
| Zeke: "Mail, Schedule, the Map, your Needs. The lot. Don't lose it." | Bubble 7, word for word. |
| Your choice: "What do I do first?" | Dropped as a choice (it was the question to you); asked by Zeke himself in the Mail. |
| Zeke's reply: "Dinner. Always dinner first. Then everything else." | The Mail, word for word. |
| Your choice: "Is it always this much?" | Dropped as a choice; asked by Zeke himself in the Mail. |
| Zeke's reply: "First night, yes. By Thursday it's just home with a lift in it." | The Mail, word for word. |
| Your choice: "(Just nod)" | Dropped (the question). |
| Zeke's reply: "Good. The quiet ones last longest." | The Mail ("And if you're the quiet sort, good. The quiet ones last longest."). |
| Zeke: "Right, onward. The mess is on Deck 3, and Brennan doesn't hold plates for anyone." | Bubbles 14 and 15, after you close the Mail (split in two, same words). |

Nothing from the green text is lost. The Mail also adds tomorrow's start (ten to nine, the Works bay), which matches
Calder's briefing time in the game.

---

## The first draft (ZW1, kept for the record)

For DS1 to wire in on `claude/zeke-tour`. Words only. Source of the old words: `content/meetings/introDevice.meet`
(the green text box, the dialogue strip) and its stand-in in section 21 (`INTRO_STUB_SCRIPTS.introDevice`).

The user's brief: no green text box and no question to you. Zeke walks up, faces you and, in speech bubbles, hands
you your device, very clearly, with a short overview in his voice. Then the device opens straight onto a Mail he
wrote before you arrived, carrying everything worth keeping from the green text. Every existing Zeke line stays.

Bubble limit: 60 characters or fewer (the limit on all his tour lines, `content/lines/torres-zeke.lines`).
`{me}` is your name, as in his other lines. Tags in brackets are poses or tones, the same marks his lines already use.

## (a) The bubble lines, in order

| # | Line | Chars | Note |
|---|------|-------|------|
| 1 | Oh, hold on. Nearly forgot the important bit. | 45 | He walks up and faces you. |
| 2 | Hands out, {me}. Both of them. Properly. | 40 | [gesture] |
| 3 | And this is yours. Your device. | 31 | KEPT, the green text's first line. [gesture] The hand-over happens on this line (introDeviceGive). |
| 4 | There. Officially handed over. I'm a witness. | 45 | #funny |
| 5 | Honestly? Most important thing you'll own here. | 47 | |
| 6 | More than your boots. Possibly more than me. | 44 | #funny |
| 7 | Mail, Schedule, the Map, your Needs. The lot. Don't lose it. | 60 | KEPT, the green text's second line, word for word. |
| 8 | Schedule says where you should be. Map says how. | 48 | |
| 9 | Needs tells you you're hungry. Before your tummy does. | 54 | #funny |
| 10 | Jobs, Calendar, people. It's all in there. | 42 | |
| 11 | Tap it any time. It never sulks. Unlike coil three. | 51 | #funny (his running joke) |
| 12 | Oh, and there's Mail waiting. From me. Wrote it last week. | 58 | Then the device opens on his Mail. |
| 13 | Read it now. I'm better on paper. Fewer tangents. | 49 | #funny |

After you close the Mail (or straight after line 13, if that's simpler to wire):

| # | Line | Chars | Note |
|---|------|-------|------|
| 14 | Right, onward. The mess is on Deck 3. | 37 | KEPT, the green text's last line, first half. [gesture] |
| 15 | And Brennan doesn't hold plates for anyone. | 43 | KEPT, its second half (the old line was 80 characters, too long for one bubble, so it's split, no words changed). |

## (b) The Mail

From: Zeke Torres

Subject: **Before you get here**

Body:

> Hello, {me}. I'm writing this a week before you land, so if anything's changed, blame the future.
>
> By now I've handed you this device and probably talked too much. Sorry. That's me.
>
> The one thing to know about tonight: dinner. Always dinner first. Then everything else. The mess is on Deck 3, dinner's till half eight, and Brennan doesn't hold plates for anyone. Not even for new hands. I've asked.
>
> It'll feel like a lot tonight. First night, it is. By Thursday it's just home with a lift in it.
>
> If you're the quiet sort, good. The quiet ones last longest. If you're not, also good. I'm not.
>
> See you at dinner. I'll save you a seat. Brennan won't.
>
> Z.

In the game's one-string form (as `clothesText` mails use, `Subject | body`; DS1 to say if another form is wanted):

```
Before you get here | Hello, {me}. I'm writing this a week before you land, so if anything's changed, blame the future. By now I've handed you this device and probably talked too much. Sorry. That's me. The one thing to know about tonight: dinner. Always dinner first. Then everything else. The mess is on Deck 3, dinner's till half eight, and Brennan doesn't hold plates for anyone. Not even for new hands. I've asked. It'll feel like a lot tonight. First night, it is. By Thursday it's just home with a lift in it. If you're the quiet sort, good. The quiet ones last longest. If you're not, also good. I'm not. See you at dinner. I'll save you a seat. Brennan won't. Z.
```

Facts checked against the game: the mess is on Deck 3; dinner runs till half eight (his goodnight line, walk.goodnight.2);
"Brennan doesn't hold plates" is his own line. Nothing new is promised.

## (c) Every green-text line, and where it lives now

| Green-text line (introDevice.meet) | Where it lives now |
|---|---|
| Zeke: "And this is yours. Your device." | Bubble 3, word for word (the moment he hands it over). |
| Zeke: "Mail, Schedule, the Map, your Needs. The lot. Don't lose it." | Bubble 7, word for word. |
| Your choice: "What do I do first?" | Dropped: it was the question to you. |
| Zeke's reply: "Dinner. Always dinner first. Then everything else." | The Mail, word for word ("Always dinner first. Then everything else."). |
| Your choice: "Is it always this much?" | Dropped: it was the question to you. |
| Zeke's reply: "First night, yes. By Thursday it's just home with a lift in it." | The Mail ("First night, it is. By Thursday it's just home with a lift in it."). |
| Your choice: "(Just nod)" | Dropped: it was the question to you. |
| Zeke's reply: "Good. The quiet ones last longest." | The Mail ("If you're the quiet sort, good. The quiet ones last longest."). |
| Zeke: "Right, onward. The mess is on Deck 3, and Brennan doesn't hold plates for anyone." | Bubbles 14 and 15 (split in two, same words), and again in the Mail. |
| Meeting gist: "Torres handed you your device: Mail, your Schedule, the Map and your Needs." | Unchanged if the record of the meeting stays (DS1's call); its content is bubble 7. |

Not green text, but in the same moment: the toast "He hands you your device. It's yours now: tap it any time."
Its content is bubbles 3, 4 and 11; DS1 decides whether the toast stays.

The stand-in in section 21 (`INTRO_STUB_SCRIPTS.introDevice`: "And this is yours: your device. Schedule, the Map,
Mail, the lot. Don't lose it." / "Right. Dinner. Come on.") is only used when the meeting file is missing; its
content is covered by bubbles 3, 7 and 14.

## Questions for the user

1. Bubbles 14 and 15 (the walk to dinner): after you close the Mail, or straight away? (Suggested: after the Mail, so he sends you off.)
2. Is the Mail's length right? It's six short paragraphs; it could lose the "quiet sort" paragraph if you'd like it shorter, but then that line would be lost.

Your answers here:

---

## Replacement for walk.more.3 (lead 31, 2026-10-23)

The line `walk.more.3` in `content/lines/torres-zeke.lines` (one of his Day 0 linger extras) says "Ask me anything,
by the way. Tap me. Questions are the best bit." (64 characters). His question menu is parked for now: tapping him
on the tour shows only his card (name, role, a line about him), so the line promises something the game doesn't do.
Two options, both shorter. **Picked: option 1** (lead 31, 2026-10-23); DS1 wires it under the same flag walk.more.3.

1. **(ZW1's pick)** Forget my name? Tap me. I won't be offended. Much.   #funny  (50 characters: invites a tap to see his card, promises nothing more)
2. Questions? Hold them for dinner. I think better fed.   #funny  (52 characters: drops the tap; dinner with him, introDinner, does have a choice for you)

Your answer here:

---

## Two words-only fixes (the user via lead 31, 2026-10-23): agreed as proposed (lead 31: all three, the Roster option); DS1 wires them

Only these lines change; timing, order and who speaks stay exactly as they are. At the arrival dinner you sit with
Zeke first and only get food after Calder's "Eat something" (the servery arrow then), so no line before that may
assume you have food.

| Where (flag / meeting line) | Old line | New line |
|---|---|---|
| introDinner.meet, first line (Zeke, [gesture]) | Sit, sit. Eat while it's hot. Brennan notices. (47) | Sit, sit. Talk first. Then food. I'll be quick. (47)  #funny |
| walk.servery.1 (the servery stop, before the table) | Tray first, then the servery. Take what smells best. (52) | The servery. Trays here. Food after a sit-down. (47) |
| walk.hand, 10th line (the hand-over) | Needs tells you you're hungry. Before your tummy does. (54) | The Roster's in there. Every name aboard. Mine's best. (54)  #funny |

Second option for the hand-over line only: "Calendar's in there too. Every tea, quiz and party." (51)

Checked and kept: the rest of the servery stop (Brennan, the table, her book of favourite dishes, bread day, the
grab shelf), walk.toMess and walk.deck3, the rest of introDinner, introChief (Calder's "Eat something" is what sends
you for food), and his goodnight. Line ids are made from the text when the words are baked, so the two bubble
lines get new ids; their flags stay the same.

---

## Backlog LEAD31-6 (lead 32, 2026-10-23): closed, the line is correct as is

walk.goodnight.1 stays: "Right, that's me. Breakfast from seven, shift at nine, tea at one." The game's breakfast is
07:00 to 09:00: `const MEALS = { breakfast: [420, 540], dinner: [1020, 1230] };   // breakfast 07:00-09:00 (the user's
playtest notes, patch 1: was from 06:00)` (starship-cadet.html line 9383 on claude/integration). ZW1's proposed change
to "from six" came from a stale read of the old 06:00 value and is cancelled; nothing was changed in the content files.

---

## Patch 0.92.3 item 26: crew comment on dirty clothes (ZW1, for AC3's hook)

Content only (not baked into the game file; AC3 or the build master bakes). Two kinds, both bubbles of 60 characters
or fewer, kind and never mean:
- `clothes.remark`: you're in yesterday's clothes (`flag:clothes.stale`, set by section 21b today).
- `clothes.grubby`: your uniform is grubby (`flag:clothes.grubby`; AC3 to set it while `uniformState() === 'grubby'`).

Where: the ten voice templates (new files `content/templates/<tpl>.lines`: 2 plain lines + 1 `tier>=friend` line per
kind, so every crew member without their own lines speaks in their template's voice), and own lines for Zeke, Brennan,
Pell, Rina, Tomas and Holt (both kinds) and Calder (`clothes.remark`; her `clothes.grubby` was already there). The shared
banks stay (`content/banks/clothes.lines`, `content/works/remarks.lines`). The hook proposed to AC3: pick the line with
`socLine(p, kind, { t, tier, bubble: true })` (own, then template, then bank), falling back to the bank as now.

Facts used, quoted from the game: the laundry is on Deck 4 ("Carry the hamper to the laundry on Deck 4, past the
washrooms in the junior wing", `tip.laundry` in content/banks/clothes.lines); you change at your wardrobe ("Change at
your wardrobe in Bunk 1", starship-cadet.html, the yesterday's-clothes toast, about line 44611 on claude/integration).
