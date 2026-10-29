# 0.98.0 round, share R5 (BM20)

Candidate claude/staging-pad 7a2ae7d2, game sha256 22f8939dbfea2dcf4b994dd8bfd7c8868f9d5450dd73c680c1dfd3c19d11918f (matched). OLD 0.97.0 610ad7f1. 2026-10-29 07:39-08:50 UTC; two lanes, join alone at the end.

Quick gates before the GO: names_check OK; check_fast OK in 265 s; cadet vs 610ad7f1: only mem/calls differ (calls 173 -> 142), renderer noise <= 1 level (lead 45's OK); join_check (120 s reload) OK.

```
machine1 exit 0 64s | MACHINE CHECK OK
machine2 exit 0 59s | MACHINE CHECK OK
day_12 exit 0 350s | DAY CHECK OK
day_13 exit 0 357s | DAY CHECK OK
day_16 exit 0 345s | DAY CHECK OK
mech exit 0 962s | MECH CHECK OK
bigevents exit 0 278s | BIGEVENTS CHECK OK
day_17 exit 0 351s | DAY CHECK OK
day_18 exit 0 353s | DAY CHECK OK
day_19 exit 0 378s | DAY CHECK OK
day_27 exit 0 356s | DAY CHECK OK
events exit 0 1422s | EVENTS CHECK OK
disc exit 0 456s | ALL OK
tiles exit 0 162s | ALL OK
food_1_7 exit 0 93s | FOOD CHECK OK
food_11_4 exit 0 87s | FOOD CHECK OK
fridays exit 0 1319s | FRIDAYS CHECK OK
clothes exit 0 69s | ALL OK
stories exit 0 38s | STORIES CHECK OK
promo_beats exit 0 82s | PROMO BEATS CHECK OK
join exit 0 257s | JOIN CHECK OK
done 08:50
```

All OK. events_check now fully OK: FX24-2 is fixed (OP1's walk-time fix).
