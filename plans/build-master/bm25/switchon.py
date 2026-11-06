#!/usr/bin/env python3
# switchon.py IN OUT [--off PIECE,...] : every 0.99.7 switch on (by piece), except the pieces named after --off
import re, sys
P = {
 'CH1': [r'const (CH_SOLE_ON|CH_POSE_ON|CH_RELAY_ON|CH_HAIR_ON|CH_SEAT_ON) = false;'],
 'TP1': [r"var TP997_ON = false \|\| URL_FLAGS"],
 'SC1': [r'var P997_SOCIAL_ON = false;'],
 'AV1': [r'const (REC_FILM|SND_DISC|SND_LIVE) = false;'],
 'JB3': [r'var JB3_SHELF_ON = false, JB3_SCI_ON = false, JB3_REC_ON = false, JB3_TEA_ON = false(, JB3_FOOD_ON = false)?;'],
 'TB6': [r"const TRAD997_ON = false \|\| URL_FLAGS"],
 'GM1': [r"const GAMES997_ON = false \|\| URL_FLAGS"],
 'MV1': [r'var MV_BRIEF_ON = false, MV_WASD_ON = false, MV_FIT_ON = false, MV_RIG_ON = false, MV_RECWC_ON = false, MV_SOFA_ON = false;'],
 'CR1': [r'var CR_DAY8_ON = false, INC_REDO_ON = false;', r'var CART_FIRST_ON = false;', r'var BOARD_NEW_ON = false;'],
 'EV1': [r'const (EV997_LIGHT_ON|EV997_SAT_ON|EV997_READ_ON) = false;'],
 'CL1': [r"const CAL997_ON = URL_FLAGS"],
}
src, out = sys.argv[1], sys.argv[2]; off = set(sys.argv[4].split(',')) if len(sys.argv) > 4 and sys.argv[3] == '--off' else set()
s = open(src).read()
for k, pats in P.items():
    if k in off: continue
    n = 0
    for p in pats:
        def on(m): g = m.group(0); return g.replace('= URL_FLAGS', '= true || URL_FLAGS') if 'CAL997' in g else g.replace('= false', '= true')
        s, c = re.subn('^' + p, on, s, flags=re.M); n += c
    print(k, n, file=sys.stderr)
open(out, 'w').write(s)
