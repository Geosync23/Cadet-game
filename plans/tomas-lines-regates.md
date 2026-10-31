# Tomas's everyday lines: re-gates for his new crew story (SW4, for ST1)

For `content/lines/tomas.lines`, applied behind STORIES_ON in the same build as `content/stories/tomas.arc`
(claude/tomas-story-sw4). Only the gate (`?` line) above each line changes. No line's words change.

`beat:tomas.N` means at least N beats told. The crescendo (8) and its quiet ending (9) both count as past 8, because
the told count is the highest beat number told. So `beat:tomas.8` means "after he met Basil, whichever way you heard it".

## Change these

| Line (now) | The line | Old gate | New gate | Why |
| --- | --- | --- | --- | --- |
| 94 | Still haven't told Holt about the exam. Don't remind me. Do remind me. Soon. | `beat:tomas.5 tier>=friend` | `beat:tomas.5 !beat:tomas.8 tier>=friend` | New beat 5 is where he tells you about the exam. At the Tern (8, or 9 if you missed it) Holt turns out to know, so the line stops there. |
| 175 | Thanks for listening. About the list. I only read it twice a day now. Progress. | `told:moment.tomas.listened` | `told:moment.tomas.listened !beat:tomas.10` | New beat 6's listen reply keeps the word `listened` (the posting). In the afterglow (10) he has closed the posting for good. |
| 185 | Holt's put me down to meet the next shuttle. Me! I've been practising "This way."   #funny | `told:moment.tomas.home` | `told:moment.tomas.pencil !beat:tomas.8` | New beat 7 (mem `pencil`) is Holt putting him on the rota; it's said once, before the Tern. |
| 530 | The next new cadet's yours to meet now. Show them the long way. It's the nice way.   #warm | `leaving:you tier>=close beat:tomas.7` | `leaving:you tier>=close beat:tomas.8` | His goodbye if you leave: after he's met Basil. |

## Leave these (they go quiet by themselves)

These are keyed to memory words from the old beats 5-7, which the new story never sets, so they never play while
STORIES_ON is on. Nothing in them contradicts the new story. They come back unchanged if the switch is off.

| Line | Gate | The line (start) |
| --- | --- | --- |
| 169 | `told:moment.tomas.promised` | You never told anyone. About the exam... |
| 171 | `told:moment.tomas.passed` | "That's the one that counts." I wrote it inside my locker... |
| 173 | `told:moment.tomas.blanket` | The blanket held! Holt stared at it... |
| 177 | `told:moment.tomas.showed` | I did show you round, didn't I?... |
| 179 | `told:moment.tomas.observatory !beat:tomas.7` | Observatory night's coming. The star map's rolled up... |
| 181 | `told:moment.tomas.shown` | Just left of the bright one. My left... |
| 183 | `mem:moment.tomas.staying` | Still here. Still staying... |

## Checked, no change needed
- `content/overheard/booths.lines` 301 (`beat:tomas.4`, his brother's map): beats 1-4 are unchanged.
- `content/lines/pell.lines` 215 and `content/lines/rina.lines` 219 (`told:heard.moment.tomas`): about you as a
  bunkmate. Not tied to any beat.
- The comments in tomas.lines (lines 52, 166, 377-378, 514) describe the old beats. If you want them current, they
  could say: the exam from beat 5, the posting from beat 6, meeting the next new cadet from beat 8.
