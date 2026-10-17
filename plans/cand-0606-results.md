# 0.60.6 check results

One line per finished check (check, game commit, OK/FAIL, key numbers). A new build master reruns only what is missing here.

- c20e8cd name_check OK · content_gen --check up to date (7515 lines) · smoke OK · newgame OK (Day 0 Sun 17:30 deck 5 manifest) · machine OK
- c20e8cd food_check FAIL: day 7 (Sunday) breakfast, salo-saad gave up waiting (152 came, 151 fed); garden 'missed 1' follows from it. Bisecting.
- c20e8cd cadet_test vs 7b57bb6: DIFFERENCES (state items/spots/calls; taps 0-4 + steers; toast = 0.28.41 need warning 'Very hungry'). Explaining step by step.
- a6ad933 (c20e8cd + poses 0.27.44-45) food_check OK (the day-7 miss gone with the washrooms reverted)
- c20e8cd deck_check OK (Deck 4 memory steady 373 geo / 39 tex) · leave_check OK
