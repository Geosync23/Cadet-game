# CR6 check results

## 0.64.15 full round (2026-10-22): FAIL (1 new)

- **Build:** `claude/integration-next` c5c43293 ("0.64.15: playtest patch 1 ..."), `starship-cadet.html` sha256
  `e955d667fe946b3e1e0a21c0b1f3049694460096f675dad5019c328e5d7d4a25` (matches the lead's).
- **OLD:** `claude/integration` 32b699a6 (0.64.14), sha256 `94f32868dbe7f27fc744eb834bb6b5f7c335bc15ac1bca86563d8ca4652881e9`.
- **Setup:** CADET_WORK=/tmp/work-cr6, CADET_CHROME=/opt/pw-browsers/chromium; one check at a time; tiles alone.

| Check | Result | Key lines |
|---|---|---|
| check_fast.sh | OK (exit 0, 251 s) | `QUICK CHECK OK in 251 s` (words, names, deck, machine, leave, device) |
| mech_check | OK (exit 0, 204 s) | `MECH CHECK OK` |
| bigevents_check | OK (exit 0, 166 s) | `BIGEVENTS CHECK OK` |
| fridays_check | OK (exit 0, **1197 s**) | `FRIDAYS CHECK OK` (the guide says ~4 min; see note) |
| disc_check | OK (exit 0, 89 s) | `ALL OK` |
| tiles_check | OK (exit 0, 106 s, alone) | `ALL OK` |
| join_check | OK (exit 0, 137 s) | `JOIN CHECK OK` |
| food_check 1 7 | OK (exit 0, 58 s) | `FOOD CHECK OK` |
| food_check 11 4 | OK (exit 0, 79 s) | `FOOD CHECK OK` |
| clothes_check | **FAIL** (exit 1, 87 s; same on a re-run) | `FAIL a busy washer sends you to a free one`, `1 FAILED` |

### clothes_check: NEW

```
     toast: "Time clock\nStill not clocked in. The time clock's in the Works bay, Deck 5. Late is better than missed."
FAIL a busy washer sends you to a free one
```

- The step (clothes_check.py line 86-89) taps a busy washer and reads the toast for "is free". On 0.64.15 the toast
  showing is the **new** time-clock nag (`later:` text, starship-cadet.html line 15176; the string isn't in 0.64.14),
  so the washer's answer is covered or replaced.
- Proof it's new: the re-run on 0.64.15 fails the same way (deterministic). On OLD (0.64.14) with the same
  clothes_check.py, this step is `ok`; OLD fails only the two steps the check added for patch 1 #8
  (`changing ticks hygiene up ... (CLOTHES_FRESH 0)`, `no clothesDirtyTick`), as expected for a build without the patch.
- Not on the known-old list (backlog 14, 23). Whether it's the check's timing (the cadet is late for shift during the
  laundry part) or a real clash (a nag toast hiding the answer to the player's tap) is for the owner of the time-clock
  nag / clothes to judge.

### Note: fridays_check took 1197 s

It passed, but took about 20 minutes alone (the guide's table says ~4). Not a FAIL; the machine wasn't shared
(load ~4, only this check's browser). Worth timing on OLD if the slowdown matters.
