# Past check failures for validating tools/affected.py (TS2, from a search of the notes; 40 found, these 17 have their causing commit)

| Causing commit | Check(s) that failed | Note |
| --- | --- | --- |
| 955b16e | bigevents, social | events base F0b, calledIn cue |
| 1c4bc67 | mech, events, join | First Light Cocoa (FLC_ON gate, evTagId) |
| 155f0d4 | intro (--evening) | patch-a #17 escort |
| ee48072 | intro (--evening) | patch-a #17 floor tap. **Inherited from 155f0d4** (TS3, proven 20:25 UTC): its parent 5cb3aad already held 155f0d4's escort stop; ee48072 with 155f0d4 reverted: intro_check --evening OK (283 s); ee48072 as it was: FAILED (the evening walk stuck, 264 s); intro_check never taps the floor (the only line ee48072 changes). The replay checks this row against 155f0d4. |
| 1f91e90 | interactions | patch-a #11 trkDoneCheck |
| 2e46584 | career | rec deck machines |
| 32f7710 | career | rec deck switched on |
| 22ff1bb | machine (fast), disc | recVisit |
| 3a1cc57 | machine (fast) | recShutAt reads MACH_HIST |
| 9abd51f | day1, events | Maeve's rec lift rides as commute |
| 693e4f4 | leave (fast), mech, interactions, machine (fast) | X2 0.71.5 varied mornings |
| ec0cbc3 | player, machine (fast) | X2 0.71.4 queues |
| 0f34cfb | interactions | U2 0.73.2 devHeadsTick |
| 1d602ff | leave (fast) | turn-in chip text |
