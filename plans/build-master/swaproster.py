import sys
def blk(s):
    a = s.index('// ---- BEGIN ROSTER'); b = s.index('// ---- END ROSTER ----'); return a, b
new = open(sys.argv[1]).read(); old = open(sys.argv[2]).read()
na, nb = blk(new); oa, ob = blk(old)
open(sys.argv[3], 'w').write(new[:na] + old[oa:ob] + new[nb:])
