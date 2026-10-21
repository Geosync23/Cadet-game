# ER3's probes for the Crossing the Line build review (plans/event-line-build-review.md)
Setup: three.js in /tmp/cadet-work/three (DEV_NOTES "Testing"); `pip install playwright`. Each probe takes a build:
a switched-on copy, `sed 's/^const EVENTS_ON = false;/const EVENTS_ON = true;/; s/^const EV_LINE_ON = false;/const EV_LINE_ON = true;/'`.
Edit the scratchpad path at the top of each .py (it reads common.py from there) or copy them next to common.py.
- `probe.py BUILD JS`: prints what a JS snippet returns (d7.js: Day 7 crowds, first-timers, Tomas, the supper; d7b/d7d: dinners;
  plans.js: a hash of every plan Days 1-30 to compare builds; reach.js: Brennan's distance from the servery line).
- `p1.py` Saturday with Tomas (walked); `p_reload.py` fix 1's repro; `p2.py` Sunday: offer, jobs, secret, horn, oath, dunking,
  mug at his post; `p3.py BUILD ANS mug|nomug|miss` the supper; `p3b.py` the same standing in the servery line; `p4.py` draw calls,
  the Lap, Monday; `p5.py` the certificate, Tuesday's Record.
- The plants (copies of a build with `const EV_LINE_ON = EVENTS_ON;` for bigevents_check): P1 `who: (p, d) => p.id === 'saruth' || cer.who`
  -> `who: (p, d) => cer.who`; P2 `stay: [45, 60], seated: true, pudding: true` -> `where: [[3, '@gather-mess']], pudding: true`;
  P3 drop `'dept:watch', ` from standEasy's `not`; P4 (off build) linePudding: `if (d === 7) { out.pudding = ...; return; }` before the switch test.
