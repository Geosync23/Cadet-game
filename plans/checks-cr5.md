# CR5 check results

Check runner 5. Share (plans/testing-guide.md, six-way split): `day_check` Days 21 and 27, interactions, events,
career. Own `CADET_WORK=/tmp/work-cr5`, `CADET_CHROME=/opt/pw-browsers/chromium`, one browser check at a time, each
on a copy of the game in `/tmp/work-cr5/new.html` (sha256 checked after copying).

## 0.64.15 full round (2026-10-22, started 06:43 UTC, for lead 26 and BM13)

- Candidate: `claude/integration-next` c5c43293 ("0.64.15: playtest patch 1 ... the Line merged switched off;
  breakfast (F) not in it").
- `starship-cadet.html` sha256 `e955d667fe946b3e1e0a21c0b1f3049694460096f675dad5019c328e5d7d4a25`: matches the
  lead's.
- OLD (for any FAIL): `claude/integration` 32b699a6 (0.64.14), sha256
  `94f32868dbe7f27fc744eb834bb6b5f7c335bc15ac1bca86563d8ca4652881e9`: matches. Not needed: nothing failed.

| Check | Result | Exit | Time | Key lines |
|---|---|---|---|---|
| `day_check.py BUILD 21` | OK | 0 | 271 s | `DAY CHECK OK`; draw calls peak 220 / 207 / 258 / 233 on Decks 1-4 (budget 450); worst stuck 0.0 ship min |
| `day_check.py BUILD 27` | OK | 0 | 266 s | `DAY CHECK OK` |
| `interactions_check.py BUILD` | OK | 0 | 425 s | `INTERACTIONS CHECK OK` |
| `events_check.py BUILD` | OK | 0 | 247 s | `EVENTS CHECK OK` |
| `career_check.py BUILD` | OK | 0 | 43 s | `CAREER CHECK OK` (backlog 12's `busy: "Relied on" before Day 5` doesn't show) |

No FAIL lines in any log. The one warning is Python's `SyntaxWarning: invalid escape sequence '\|'` at
interactions_check.py:498 (the check's own source, not the game; harmless).

**CR5: OK** (5 of 5).
