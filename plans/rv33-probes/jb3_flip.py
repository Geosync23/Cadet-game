import re, sys
src, out = sys.argv[1], sys.argv[2]; skip = set(sys.argv[3].split(',')) if len(sys.argv) > 3 and sys.argv[3] else set()
s = open(src).read()
NAMES = ['REC_FILM','TP997_ON','TRAD997_ON','GAMES997_ON','MV_BRIEF_ON','MV_WASD_ON','MV_FIT_ON','MV_RIG_ON','MV_RECWC_ON','MV_SOFA_ON','JB3_SHELF_ON','JB3_SCI_ON','JB3_REC_ON','JB3_TEA_ON','JB3_FOOD_ON','EV997_LIGHT_ON','EV997_SAT_ON','EV997_READ_ON','P997_SOCIAL_ON','CR_DAY8_ON','INC_REDO_ON','CART_FIRST_ON','BOARD_NEW_ON','CH_SOLE_ON','CH_POSE_ON','CH_RELAY_ON','CH_HAIR_ON','CH_SEAT_ON','SND_DISC','SND_LIVE']
done = []
for n in NAMES:
    if n in skip: continue
    s2, k = re.subn(r'(\b(?:const|var|let) [^;\n]*?\b' + n + r' = )false\b', r'\1true', s, count=1)
    if not k: s2, k = re.subn(r'(,\s*' + n + r' = )false\b', r'\1true', s, count=1)
    if k: done.append(n); s = s2
if 'CAL997_ON' not in skip:
    s2 = s.replace("const CAL997_ON = URL_FLAGS.has('cal997');", "const CAL997_ON = true || URL_FLAGS.has('cal997');")
    if s2 != s: done.append('CAL997_ON'); s = s2
open(out, 'w').write(s); print(len(done), 'on; missing:', [n for n in NAMES + ['CAL997_ON'] if n not in done and n not in skip])
