# RV12 review notes

Reviewer RV12 (session_013JmdoWWEDQde8y1bwrMGnY), branch claude/review-rv12 (notes only), under lead 32.

## FX6 tray-seat arrow (LEAD31-14, 0.92.2), on claude/mess-taps (base FX7 980c2591)
- Status: waiting for FX6's sha (~21:45 UTC). Baseline interactions_check and arrows_check week running on 980c2591.
- Known so far: the hunger arrow comes from needGoal('hunger') (NEED_FIX hunger: servery-queue, grab-shelf); it is
  cleared only when an act with def.need hunger starts (eat) or Food is back over WARN_REARM, so after the queue hands
  you a tray it still points at the servery.
