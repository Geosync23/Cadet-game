# Handover: SW3, story writer (Salo, Raman, Kowalczyk)

**Role:** story writer under LEAD 32; story lead and editor CS1 (session_01QcPAXHjQZ2HfZKMCTbaW9v). Session
session_01MRMAfR4taMKEXeR5qa4Wpq. **Branch:** `claude/stories-sw3`, from `claude/integration` 364c80cb (game 0.92.2).
**State:** all three stories PASS from CS1 at 77b956ed. Content only: nothing baked, the game file untouched.

## What I own and wrote

| File | Story | Beats |
| --- | --- | --- |
| `content/arcs/salo.arc` | Saad Salo, "Twice" | 1 serial and Hala's news; 2 the checking card; 3 the Pallas (heartfelt); 4 crescendo in the ion storm, Deck 6, Day 13 (Torres, Calder on the comm); 5 afterglow, the card to Hala, keepsake "a checking card he made for you, with your name at the top"; 6 quiet ending for 4 |
| `content/arcs/raman.arc` | Dev Raman, "The same comet" | 1 soup and the Day 0 landing; 2 the model's empty shuttle bay (favour `ramanPin`); 3 Lisk and Asel (heartfelt); 4 trusting someone new (heartfelt); 5 crescendo at the observatory back window, comet night Day 16 22:10 (Bakshi on the speaker, Sato); 6 quiet ending, same keepsake (a tiny carved Tern) |
| `content/arcs/kowalczyk.arc` | Anja Kowalczyk, "The beacon" | 1 endings first, bow lounge; 2-3 your first night shift, Day 22 (before midnight); 4 crescendo on the bridge, Day 24 05:50, her rest night (Takahashi, Mensah); 5 afterglow, the annotated novel; 6 quiet ending for 4 |

No `.meet` files: every crescendo is a beat inside the arc, as CS1's outline asks.

## Conventions used (CS1's outline, content/arcs/outlines.md on claude/crew-stories-pitch)

- Beat numbers only go up: crescendo, quiet ending and afterglow are plain numbers. In Salo and Kowalczyk the
  afterglow (5) uses `when: beat:<arc>.4` (four beats told), so it follows either the crescendo (4) or the quiet
  ending (6). The crescendo sets a flag (`salo.signed`, `raman.comet`, `kowalczyk.lit`); the quiet ending has `!flag:`.
- Builders' notes are comments under the header: `// DAY: ...`, `// CRESCENDO rides on: ...`, `// QUIET ENDING for
  beat N ...`, `// IF <conditions>: <speaker>: <text>` (one, in Kowalczyk beat 4, on `flag:kowalczyk.signal`).
- Kowalczyk's beats 3-4 carry `tier: acquaintance` and `gapDays: 0` so they fit the night-shift window.

## Gotchas

- **lines_check on a content-only branch** always errors "baked blocks out of date". Check against a scratch copy:
  `cp starship-cadet.html $SCRATCH/baked.html && python3 content_gen.py $SCRATCH/baked.html && python3 lines_check.py $SCRATCH/baked.html`.
  Never commit the game file. The bar: PASS, and no "same line is also in" warning from your files.
- The new names Hala, Pallas and Asel warn until CS1's facts.md (claude/crew-stories-pitch 70ee2243) is merged.
- Words to avoid in these three (already said all over the ship): "check it twice"/"check twice", "best seat on the
  ship", "hold the rail" (the lift club), "Lovely work" (Halloran's), "Four, please" (Kovac's), "Back to it" (Calder's).
- No pictures or cameras: Kowalczyk's Mail says someone on Marra *wrote* to her father.

## Loose ends for the builders (not mine to do)

- Day gates, the crescendo hook, Calendar and Mail before a crescendo, the quiet-ending rule, and the new favour
  `ramanPin` (a stop at the machine shop bench).
- Kowalczyk's crescendo night (Day 23 into 24) is her rest night; she comes in on purpose (it's in her lines), so
  her rota needn't move. Confirm Takahashi and Mensah are on that night.
- The comet event is still a draft (`event:comet`); Raman's beats 4-6 rely on it.

## Open questions for the user

None from me. Anything the user changes after reading goes through CS1.
