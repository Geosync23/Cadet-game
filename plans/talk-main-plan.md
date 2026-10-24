# Talk a while: the Captain and the main characters (patch 0.92.3, item 15)

**Words lead:** CS1 (claude/crew-stories-pitch). **Writers:** SW1, SW2, SW3. **Engine:** FX13. **Code review:** RV13.

The user: "The captain and 10 main characters should have their own large pool of original things to say when using
talk a while. The captain should introduce herself properly and welcome you aboard first time you talk with her. These
main characters should never pull from the general pool of talk a while lines."

## Who (the lead is confirming with the user)

The Captain, plus ten. Two readings:

- **A (recommended): the roster's ten story crew** (`story: true` in ROSTER, besides the Captain): Vance, Sato, Holt,
  Calder, Pell, Rina, Brennan, Tomas, Nandakumar, Zeke. Exactly "the Captain and 10"; all already have their own talks.
- **B: the ten crew-story people**: Pell, Zeke, Calder, Kovac, Theo, Basil, Halloran, Salo, Raman, Kowalczyk.

In both: **Marrow, Pell, Zeke, Calder**. Writing starts with them.

## What each main character gets

- **30 own talks** in all: their 4 existing ones kept unchanged, plus **26 new**. Laddered by tier so a player who
  talks to them every day has something new each day: about 8 at any tier or acquaintance, 8 from colleague, 6 from
  friend, 4 from close friend (`when: tier>=...`). A game of about 30 days uses at most about 30.
- Varied by topic (the ten topics: hobby, home, their day, work, food, news, a tradition, crew, the ship, plans), and
  some by time or mood (`time:`, `mood:`, `weekday:`), so the same week doesn't feel samey.
- **Their own small talk** for when every talk they can give today is used: `== small.<id>` (15 lines, no question,
  may repeat, in their voice) and `== done.<id>` (3 lines, "we've talked about everything"). The pattern Saruth
  already has (`small.saruth`, `done.saruth`).
- **Never the general pool:** no `pool-*`, `work-*` or generic `smalltalk` lines for them (FX13's engine side).
- **The Captain's welcome:** her first talk ever is `== welcome`: she introduces herself properly (name, that she
  commands the Wren) and welcomes you aboard. One question and three replies, like any talk. FX13 makes it play first.

## The format (FX13 to confirm)

The existing `.talk` grammar, in each person's own file `content/talkpack/<crewId>.talk` (one writer per file):

- New talks: ordinary `== <talk-id>` blocks (`topic:`, `when:`, `them:`, `ask:`, `listen:`/`share:`/`cheer:` with the
  indented answer), appended after the existing four. Ids unique within the file.
- `== welcome` (Marrow only): plays as her first talk.
- `== small.<crewId>` and `== done.<crewId>`: `- ` lines, as in smalltalk.talk, placed at the end of the person's file.

## Rules (as for the crew stories)

The person's voice card and roster entry (`content/voices/<id>.voice`, `plans/crew-roster.html`); every `avoid`
respected (story secrets only behind their beats); no line that's already anywhere in content/ (CS1 checks every push
with the duplicate checker, exact and near); no talk that retells a story beat; the tone rules (lighter; nobody ill or
in trouble now; Zeke's dad well and retiring; Halloran's dad long gone, gently). Lines under 90 characters on the card
(`them:`), the README's limits for the rest. lines_check PASS on a scratch bake.

## Assignment (first round)

- **SW3:** Marrow (welcome + 26 talks + small).
- **SW1:** Pell, Zeke, Calder.
- **SW2:** waits for the list; then the next three.
- After the list is confirmed: the remaining six shared out, three each to whoever finishes first.

## ETA

Marrow, Pell, Zeke and Calder: about 2 hours from the format being agreed, reviews rolling. All eleven: about 4-5
hours of writer time in parallel, plus review.
