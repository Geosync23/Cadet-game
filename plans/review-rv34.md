# RV34 review notes

RV34, reviewer, session session_01GKuymjMD8QCJBVidEVLFpP, hired by lead 51 (session_01GKuymjp49y3M5hgRLecobm).
Build master BM27 (session_01GKuymjy5t3QwM8whGj2QFE). Branch claude/review-rv34 (from claude/review-rv33).

## EV1: pale blink as the Last Light beacon passes (EV999_BLINK_ON)
- Builder EV1, session_01GKuymkhvqRE7N1Rj4VMtWD. Branch claude/ev999-blink from main 33c737b (0.99.8).
- OLD = main 33c737b, game 13681748513f9b7cb51fc299c4789085d0636829d8297b9f0d29d00683259fd3.
- Plan: Day 4 14:08, every deck's hemisphere/sun light washes pale blue-white, two soft ~0.8 s pulses (~2 s), feel kind
  'beacon' in 8b's shipFeelFrame, one-line notice, reduced motion one gentle swell; no meshes, no draw calls, col(), no R().
- Kit set up 2026-11-07 (/tmp/cadet-work, /tmp/rv34/old.html). Waiting for EV1's commit.
- Commit 5378fa0 (game), tip e3202a0 (perf_check scene 6140e27, shots; game unchanged), game sha256
  592cd2d80959ae9b2b2cbf63b9e73aeb0ee7a57a5a82af47ac206e85fe28bb71. On copy (sed the line to true): b657bf7b...7e60cf.

### Results
- Switch off: cadet_test vs 0.99.8 ALL IDENTICAL. check_fast off: QUICK CHECK OK (485 s). check_fast on: OK (497 s).
- events_check on: see below; off: see below.
- blink_trace.py (every deck 1-7, fresh page each, Day 4 14:07 -> 14:09:30, every frame), analysed by blink_analyse.py
  against the off build frame for frame:
  - on: fires at 14:08 on all 7 decks; only 47 frames differ (se 0.03-1.77 s); 2 pulses (peaks 0.4 s and 1.4 s, about
    1 a second, far under 3 a second); hemi intensity up to x1.7; draw calls identical to off on every deck (126, 152/153,
    197, 171, 162, 106, 149); the last 60 frames identical to off (the light back exactly).
  - reduced motion (matchMedia stubbed): one swell, intensity unchanged (x1.0), colour only; back exactly; draw calls same.
  - Deck 6 (warm, dim) swings most: blue channel +0.5 (others +0.09). Seen on the phone shot: brown to cool grey-blue for
    under a second a pulse. Taste note, not a fix.
- blink_more.py: only lastLight.lastLightBlink carries `notice` (no existing moment toasts). Deck change mid-blink: the
  pulse finishes on the new deck and its light comes back to the reference values. skipTo 14:00 -> 14:30: no blink;
  14:07 -> 14:12: none; 14:07 -> 14:09: fires (the 3-minute window, as the horn); Dev mode's +3 hours from 12:08
  (30-minute skipTo steps, one landing on 14:08): no blink, no notice.
- blink_save.py (real saving): saved mid-blink and reloaded: no second blink, light 0.85 (normal), felt kept. Saved at
  14:07:52 and reloaded: fires once after the reload.
- Notice: one line, fits at 390 px (box 366 x 68). It goes through the guide toast queue, so when another toast is fresh
  it shows about 3 s after the blink (seen behind "Your device: 2 new messages"). Not a fix; a note.
- Seen by chance: at 14:07 a crew bubble "The light's fixed. No more blinking. Lovely." (a machine-repair chatter line)
  just before the blink. Coincidence, for the lead's eye only.
