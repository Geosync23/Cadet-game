# Patch E probes (patch builder PE, 2026-10-20)

After-probes for batch E's first half, on PP1's harness (`plans/patch-plan-probes/pp.py`). Run from the repo with `CADET_WORK` set; the first argument is a folder for screenshots. Each turns its feature's switch on with its URL flag.

- `sign25.py OUT`: Deck 2's directory sign and text (#25).
- `c21after.py OUT`: the storekeeper's card with `?rankcard` (#21), and every distinct rank line.
- `e6.py OUT` with `Q='&clockundo'`: the time clock (#6): a double tap on Clock in, Undo, the 5 s window, a double tap on an early Clock out (Cancel where it was), Undo after 17:00, walking away, a save in the window, a Dev-style clock jump in the window.
- `e24.py OUT` with `Q='&shopmenu'`: the storekeeper at the counter at 15:00 (Orla), her card's Buy something, the menu with 5 credits (greyed lines), buying the dried apple through the counter's pay step, and no button on someone else's card (#24).
- `e5.py OUT` with `Q='&ladder'`: the spine ladder (#5): the hatch's tap on Decks 4, 5 and 1 (on Deck 1 the relay racks' tap box covers the hatch's foot, so it taps the middle), the panel, climbs 4→5, 5→1 with the lift held, 1→6 (time, energy, fitness, where you land), Engine control and the Sensor array reachable, the Reactor not, every deck's hatch and landing tile, and any tier wording left in door, room or item texts.
