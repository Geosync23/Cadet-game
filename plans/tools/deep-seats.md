# The 44 deep seats (0.27.40 probe, seatprobe.py on 0.27.39): cushion under the knees

Measured with a seated stand-in: `kneeS` is the surface 0.3 m ahead under the knee. Some are false positives (a table the legs go under, e.g. the bow lounge booths at 0.42, the bridge window seats, 3-gym-4 the rower); give those no `cush`. Check each by eye.

| deck | place | type | seat y | surface under the knees |
| --- | --- | --- | --- | --- |
| 1 | 1-window-1 | lounge-seat | 0.52 | 0.42 |
| 1 | 1-window-4 | lounge-seat | 0.52 | 0.42 |
| 2 | 2-armchair-1 | lounge-seat | 0.44 | 0.44 |
| 2 | 2-armchair-10 | lounge-seat | 0.44 | 0.44 |
| 2 | 2-armchair-11 | lounge-seat | 0.44 | 0.3 |
| 2 | 2-armchair-12 | common-room | 0.44 | 0.44 |
| 2 | 2-armchair-2 | lounge-seat | 0.44 | 0.44 |
| 2 | 2-armchair-3 | lounge-seat | 0.44 | 0.44 |
| 2 | 2-armchair-4 | lounge-seat | 0.44 | 0.44 |
| 2 | 2-armchair-5 | lounge-seat | 0.44 | 0.3 |
| 2 | 2-armchair-6 | lounge-seat | 0.44 | 0.44 |
| 2 | 2-armchair-7 | lounge-seat | 0.44 | 0.44 |
| 2 | 2-armchair-8 | lounge-seat | 0.44 | 0.44 |
| 2 | 2-beanbag-1 | common-room | 0.39 | 0.399 |
| 2 | 2-captable-6 | lounge-seat | 0.5 | 0.445 |
| 3 | 3-bench-17 | bench | 0.48 | 0.44 |
| 3 | 3-bench-18 | bench | 0.48 | 0.44 |
| 3 | 3-gym-4 | gym | 0.43 | 0.43 |
| 3 | 3-lounge-13 | lounge-seat | 0.54 | 0.42 |
| 3 | 3-lounge-14 | lounge-seat | 0.54 | 0.42 |
| 3 | 3-lounge-15 | lounge-seat | 0.54 | 0.42 |
| 3 | 3-lounge-17 | lounge-seat | 0.54 | 0.42 |
| 3 | 3-lounge-18 | lounge-seat | 0.54 | 0.42 |
| 3 | 3-lounge-19 | lounge-seat | 0.54 | 0.42 |
| 3 | 3-lounge-20 | lounge-seat | 0.54 | 0.42 |
| 3 | 3-lounge-21 | lounge-seat | 0.54 | 0.42 |
| 3 | 3-lounge-22 | lounge-seat | 0.54 | 0.42 |
| 3 | 3-lounge-24 | lounge-seat | 0.54 | 0.42 |
| 3 | 3-lounge-25 | lounge-seat | 0.44 | 0.44 |
| 3 | 3-lounge-26 | lounge-seat | 0.44 | 0.44 |
| 3 | 3-lounge-27 | lounge-seat | 0.44 | 0.3 |
| 3 | 3-lounge-28 | lounge-seat | 0.44 | 0.3 |
| 3 | 3-lounge-29 | lounge-seat | 0.44 | 0.44 |
| 3 | 3-lounge-30 | lounge-seat | 0.44 | 0.3 |
| 3 | 3-lounge-31 | lounge-seat | 0.44 | 0.44 |
| 3 | 3-lounge-33 | lounge-seat | 0.44 | 0.44 |
| 4 | 4-common-4 | common-room | 0.44 | 0.44 |
| 4 | 4-common-5 | common-room | 0.44 | 0.44 |
| 4 | 4-common-7 | common-room | 0.44 | 0.44 |
| 4 | 4-music-2 | music | 0.42 | 0.356 |
| 4 | 4-music-4 | music | 0.42 | 0.356 |
| 4 | 4-music-5 | music | 0.42 | 0.347 |
| 5 | 5-tern-seat-1 | event | 0.5 | 0.42 |
| 6 | 6-watch-2 | work:engine | 0.44 | 0.44 |

Tools (performance engineer 3): `seatprobe.py BUILD.html out.json` puts a stand-in on every seat place on every deck and prints, per type, the thigh against the seat. Its JSON has kneeY/kneeS per seat. `raycount.py BUILD.html` reports seatCushion rays per frame and ms per ray at Sunday dinner. `phone.py` is the phone-like hour (4x CPU).
