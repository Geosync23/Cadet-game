# RV27: CH1's intro_check part 20 (a real save + page reload mid-dinner) with the reload on card N (RV_CARDS, default 3), and the
# per-frame tracker of ch_dinner.py running after the reload. Usage: RV_CARDS=6 CADET_WORK=... python3 ch_reload.py WORKTREE
import sys, os, pathlib
WT = pathlib.Path(sys.argv[1]).resolve(); N = int(os.environ.get('RV_CARDS', '3'))
src = (WT / 'intro_check.py').read_text().replace("__file__.replace('intro_check.py', 'cadet_test.py')", repr(str(WT / 'cadet_test.py')))
TRACK = (pathlib.Path(__file__).parent / 'ch_dinner.py').read_text().split("TRACK = r'''")[1].split("'''")[0]
a = "    for _ in range(3):   # three cards at a player's pace (5 s a card), then save\n"; assert a in src
src = src.replace(a, f"    for _ in range({N}):   # RV27: N cards, then save\n", 1)
b = "    up, welcome, end = None, None, None\n"; assert b in src
src = src.replace(b, b + "    g.ev(" + repr(TRACK) + ")\n", 1)
c = "    print(f\"  before the save at {saved}"; assert c in src
src = src.replace(c, "    print('RV27 TRACK after the reload'); [print('  ', x) for x in g.ev('window.__ct || []')]\n" + c, 1)
sys.argv = [str(WT / 'intro_check.py'), str(WT / 'starship-cadet.html'), '--dinner']
os.chdir(WT); exec(compile(src, str(WT / 'intro_check.py'), 'exec'))
