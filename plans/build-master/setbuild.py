# setbuild.py HTML BUILD: set the header build line and GAME_BUILD
import re, sys
p, b = sys.argv[1], sys.argv[2]; s = open(p).read()
s, n1 = re.subn(r"(STARSHIP CADET: CSV Wren\s+build )\S+", lambda m: m.group(1) + b, s, count=1)
s, n2 = re.subn(r"const GAME_BUILD = '[^']*';", f"const GAME_BUILD = '{b}';", s, count=1)
open(p, 'w').write(s); print('build', b, n1, n2)
