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

- **30 own talks** in all: their 4 existing ones kept unchanged, plus **26 new**, laddered by tier. Because a player
  stays a stranger or acquaintance with some people for a long while, most talks open early:
  - **the Captain:** about 22 at any tier or acquaintance (of the 30), 5 from colleague, 3 from friend or close;
  - **everyone else:** about 16 at any tier or acquaintance, 7 from colleague, 4 from friend, 3 from close.
- Varied by topic (the ten topics: hobby, home, their day, work, food, news, a tradition, crew, the ship, plans), and
  some by time or mood (`time:`, `mood:`, `weekday:`), so the same week doesn't feel samey.
- **When they run out** (FX13's engine, agreed 2026-10-24): they **repeat their own talks**, the least lately heard
  first and none heard in the last 20 days if possible. No small-talk blocks are needed, and the general pool and
  shared small talk are never used for them (`only: own`).
- **The Captain's welcome:** her first talk ever is `== welcome` with `first: yes`: she introduces herself properly
  (name, rank, the ship) and welcomes you aboard; up to **4** `them:` lines (90 characters each), one `ask:` and the
  three replies. It counts as used only once you've answered; the generic hello isn't put in front of it.

## The format (agreed with FX13, 2026-10-24)

The existing `.talk` grammar, in the person's own file `content/talkpack/<crewId>.talk`:

- New talks: ordinary `== <talk-id>` blocks (`topic:`, `when:`, `them:` x1-3, `ask:`, `listen:`/`share:`/`cheer:` with
  the indented answer), appended after the existing four. Ids unique across that person's files, never reused.
- `only: own` on its own line before the first `==` (once per person): own pool only.
- `first: yes` straight under `== welcome` (Marrow only; one per person at most).
- A person may have more than one file (`marrow-2.talk`, all `@talks marrow`), baked in filename order, if a pool is
  split between writers. Not needed this round.

## Rules (as for the crew stories)

The person's voice card and roster entry (`content/voices/<id>.voice`, `plans/crew-roster.html`); every `avoid`
respected (story secrets only behind their beats); no line that's already anywhere in content/ (CS1 checks every push
with the duplicate checker, exact and near); no talk that retells a story beat; the tone rules (lighter; nobody ill or
in trouble now; Zeke's dad well and retiring; Halloran's dad long gone, gently). Lines under 90 characters on the card
(`them:`), the README's limits for the rest. lines_check PASS on a scratch bake.

## Assignment (first round)

- **SW3:** Marrow (welcome + 26 talks).
- **SW1:** Pell, Zeke, Calder.
- **SW2:** waits for the list; then the next three.
- After the list is confirmed: the remaining six shared out, three each to whoever finishes first.

## ETA

Marrow, Pell, Zeke and Calder: about 2 hours from the format being agreed, reviews rolling. All eleven: about 4-5
hours of writer time in parallel, plus review.
