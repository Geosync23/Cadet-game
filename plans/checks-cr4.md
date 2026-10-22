# Check runner CR4: results

## 0.64.15 full re-run (2026-10-22)

- **Candidate:** `claude/integration-next` 31c44cb9 ("Merge claude/patch-play1-d 836db6c7 ... into claude/integration-next")
- **starship-cadet.html sha256:** `0c1f6fb487d6f7f7a47ab3f4f20a475f0ded2b53107030bdd4dbfb6ef8259d2e` (matches lead 26's)
- **OLD:** `claude/integration` 32b699a6 (0.64.14), sha256 `94f32868...881e9`; not needed, no FAIL
- **Share:** day_check Days 12, 13, 16, 19, one at a time, alone, checked out at 31c44cb9 (day_check.py unchanged since c5c43293), `CADET_WORK=/tmp/work-cr4`

| Check | Result | Key lines |
|---|---|---|
| day_check 12 | OK (exit 0, 261 s) | `DAY CHECK OK`; plans the same twice; rec deck shut for the storm (skipped, as designed); draw calls peak 250 / 450 |
| day_check 13 | OK (exit 0, 263 s) | `DAY CHECK OK`; plans the same twice; rec deck shut for the storm (skipped); draw calls peak 253 / 450 |
| day_check 16 | OK (exit 0, 264 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 246 / 450 |
| day_check 19 | OK (exit 0, 241 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 265 / 450 |

**CR4: OK.** No FAILs. Same peaks as the c5c43293 round below.

## 0.64.15 full round (2026-10-22)

- **Candidate:** `claude/integration-next` c5c43293 ("0.64.15: playtest patch 1 ... the Line merged switched off; breakfast (F) not in it")
- **starship-cadet.html sha256:** `e955d667fe946b3e1e0a21c0b1f3049694460096f675dad5019c328e5d7d4a25` (matches lead 26's)
- **OLD:** `claude/integration` 32b699a6 (0.64.14), sha256 `94f32868dbe7f27fc744eb834bb6b5f7c335bc15ac1bca86563d8ca4652881e9` (matches); not needed, no FAIL
- **Share:** day_check Days 12, 13, 16, 19 (testing-guide six-way split), one at a time, alone, `CADET_WORK=/tmp/work-cr4`, Chromium /opt/pw-browsers/chromium

| Check | Result | Key lines |
|---|---|---|
| day_check 12 | OK (exit 0, 263 s) | `DAY CHECK OK`; plans the same twice; rec deck shut for the storm (comparison skipped, as designed); draw calls peak 250 / 450; worst stuck 0.0 min |
| day_check 13 | OK (exit 0, 253 s) | `DAY CHECK OK`; plans the same twice; rec deck shut for the storm (skipped); draw calls peak 253 / 450; worst stuck 0.0 min |
| day_check 16 | OK (exit 0, 272 s) | `DAY CHECK OK`; plans the same twice; rec deck traditions rec-dawn-swim, rec-wall-night; draw calls peak 246 / 450 |
| day_check 19 | OK (exit 0, 268 s) | `DAY CHECK OK`; plans the same twice; rec deck mean 7.3 peak 17; draw calls peak 265 / 450 |

**CR4: OK.** No FAILs, so no OLD runs were needed.
