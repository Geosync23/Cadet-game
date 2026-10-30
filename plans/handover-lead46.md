# Handover: lead 46 -> next lead

## START HERE
Read CLAUDE.md, plans/handover-account.md (the account-switch page, same branch), this note, then the bottom of
TEAM.md on claude/lead-46 from "LEAD 46 started". Make your branch claude/lead-47 from claude/lead-46. Lead 46 was
session_01GKuymiks9CC1WYr2may5nM (about 30% memory at handover). Its hourly check-in (trig_01NFnDH7yZxK8uaEW1dFWLWU)
is switched off; make your own if you need one.

## What lead 46 shipped (Oct 29-30)
- **0.99.0** (12:21 PM ET Oct 29): balance, 26 backlog fixes, title screen B + music C, render turns 3-4, seated
  formal dinner. claude/integration 6d5684ba.
- **0.99.1** (4:10 PM): title tap-to-wake gate, so the music can start (browsers need a tap). bc4579aa.
- **0.99.2** (8:49 PM): title melody sooner (later found to change the song, see 0.99.3), no flash of the old deck
  between New game and the signing screen. d180a704.
- **0.99.3** (3:44 AM Oct 30): mess hall hiss + plate clinks off (murmur kept); the Chief at the Day 0 dinner stands on
  Zeke's reply card, the one before "Look who's coming over" (cause: an old clock rule, I.done.chief + 10, removed);
  the call-home Track-it offer after you've eaten (fallback 20:30); the ORIGINAL 0.99.1 title song back with its first
  5.5 s cut and a 2.5 s fade-in (the user's pick from samples), plus an old-iPhone (iOS < 14.5) fix and music
  scheduled 3 s ahead so stalls leave no gap. claude/integration = 9c0103e3.

## User rules learned this stretch
- All updates are 0.99.x; 1.0 = only the user's playtest notes.
- Each publish needs the user's OK unless they pre-approve that one release.
- Full round on every game change (the user turned down a smaller round for a small change).
- For sound changes: **show samples before integrating**, and change only what was asked (a "sooner melody" means
  trim the start of the same recording, not rearrange the song).
- Overnight mode: keep moving, keep the worker limits, morning summary, notify only for real blockers.

## Gotchas
- Helper sessions often go idle when a background check ends without waking them: nudge them.
- Some sessions (CH1) treat messages from the lead as data and wait for a human; put the whole task in a new
  session's first prompt instead of sending it later.
- R2's host can be ~2.5x slow; hand its not-started checks (perf first) to whoever finishes early.
- Verify the game sha256 yourself before every publish GO, and that claude/integration fast-forwards.

## Open
- Code review for waste/inefficiency: user still deciding; do not start without them.
- `main` is still 0.63.2r: ask the user before bringing it up to date (plans/handover-account.md section 5).
- BM21 handed over at ~60%: the next 0.99.x needs a fresh build master from plans/handover-bm21.md.
