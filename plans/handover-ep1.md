# Handover: EP1 (events and career planner)

Session: EP1, hired by lead 37, now reporting to lead 38 (session_01G2y9crUv6vDiiEB2q6Yo9W). Planning only: no game edits.
Branch: `claude/events-plan-2` (this session can push only there; leads cherry-pick onto other branches).

## What I wrote (all on claude/events-plan-2)

1. `plans/events-plan-2.html`: the next ship-wide events (lead 37 published it for the user).
   - Part A, the comet, Monday Day 22, 21:30-22:40: four windows with hosts (Sato at the bow lounge, Mori at the
     observatory scope, Tomas with blankets in the junior common room, the Captain's tea in the observation room for
     Officers and up), Saruth's comet knot 22:00, Raman's story 22:10. **Built and on in 0.93.2** (FX25, `EV_COMET_ON`);
     the user answered A1 (its own music track) and A2 (the knotted cord stays for good).
   - Part B, the short Veyli visit, Days 16-19, with a kept/cut/new table against the built `SHIP_EVENTS.diplomatic`
     (FX22b built the calendar swap behind `EV_SWAP_ON`, by link only in 0.93.2). Questions B1-B6 not answered as far
     as I know; B3 (summons Day 22) is superseded by the Pillar 5 plan (summons stays Day 18 16:00).
   - Part C, "A Veyli vessel needs help", Days 27-30 (Taavek, the parts chain, making the impeller, the engine lights).
     Questions C1-C2 open. Not built (a parked calendar row in the swap).
2. `plans/pillar5-steps56-plan.html` v3.1 (commits b98057c3, d186d56f, c827f392): Pillar 5 Steps 5-6 brought up to
   date for lead 38 (the user asked to modernise them).
   - The user's answers (26 Oct): night 1 at 22:45 after the comet; Navarro's leave is why you cover nights; the
     commendation summons stays Day 18 16:00 (the visit's dinner isn't your Captain's scene); Calder tells you the
     Tier 4 result at the comet; the toast kept; the Senior Officer's bar in the observation room; **the move to Deck 2
     comes with Engine Specialist** (Thursday Day 25 after dinner), Senior Officers stay in 4-23.
   - Both promotions follow FX28's promotion beats (`PROMO_BEATS_ON`); 17 switched pieces with their checks, including
     `controller_check` (section 13a lists the new buttons the pad must reach).
   - Design-doc follow-up (when Step 5 starts): the tier tables and the laundry line (section 12's last row).

## Gotchas

- Facts: every Veyli is they/them (the built visit's address said "she" for the Speaker); never "permission" or "leave"
  about the reach; the comet's Veyli name is unspoken (new canon).
- The player's Deck 2 quarters are room B (the visitors' suite); Teshavi lodges in 2-U.
- Day 18 is Calder's first chief's talk (19:00); Day 22 is Olu Farouk's birthday; Raman and Bakshi are off at weekends.
- With the swap, the build moves the `mondayBriefing` hold to Day 16 and `seniorBriefing` to Day 19 08:00; Pillar 5
  needs its own Day 22 briefing hold.

## How to check a page

Pages are plain HTML in the house style; the answers form saves to the page db at `answers/user` (needs the `db`
capability when published). Before pushing: the script parses (`node -e` new Function on the <script>), and a
390-px-wide Playwright load has `scrollWidth` 390.
