# Starship Cadet: record the Dev page's "Start at a day, as played" saves (section 25's devmodeDaysData; DS1, 2026-10-22).
# A player who only follows the arrow (arrows_check.py's follower: FOLLOW, Follower, Page; imported, not copied) plays
# a new Dev game from the shuttle (Day 0, 16:30) to Day 8. Each evening at 21:30 it stops, is washed and fed as after a
# normal evening (needs to 85 at least, as arrows_check's night does), stands by its bed and sleeps the game's own way
# (sleepGo, the alarm at 06:00). At each 06:00 (Days 1-8) it marks the Mail so far read (a player who followed saw the
# toasts), saves, and keeps the Dev save (save.dev dropped, job tracking on) deflated and base64'd, with the "arrived"
# key and a summary (section 25's devmodeDaySum, which the check compares after loading).
# A day is "played" while the follower keeps up: clocked in every workday so far and each lesson learned on its day
# (arrows_check's WEEK). From the first day it doesn't, the rest are recorded through Set career (devmodeSetCareerTo(d) by the end of
# the day before, then 06:00 in bed) and marked played: false (the Dev page says so: for testing only).
# The career's seed is DM_SEED (no sick day), as Set career's.
# Run:   python3 tools/day_saves.py BUILD.html [--write] [--twice] [--last N]
#   --write  writes devmodeDaysData into BUILD.html between the "day saves" lines (else prints the sizes only)
#   --twice  records Days 1-2 twice and checks the saves are byte-identical (the recorder's self-test)
#   --last N stop after Day N's morning (default 8)
# Needs arrows_check.py: the repo's root, or ARROWS_CHECK=path. Setup as cadet_test.py. About 15-20 minutes.
import sys, os, json, zlib, base64, pathlib, re, subprocess
ROOT = pathlib.Path(__file__).resolve().parent.parent
AC = pathlib.Path(os.environ.get('ARROWS_CHECK') or ROOT / 'arrows_check.py')
if not AC.exists(): sys.exit('day_saves: needs arrows_check.py (the repo root, or ARROWS_CHECK=path)')
exec(AC.read_text().split('PARTS = set(')[0])      # Page, Follower, FOLLOW, STATE, WEEK; nothing runs

args = [a for a in sys.argv[1:] if not a.startswith('--')]
PATH = args[0]; WRITE = '--write' in sys.argv; TWICE = '--twice' in sys.argv
LAST = int(sys.argv[sys.argv.index('--last') + 1]) if '--last' in sys.argv else 8
if '--last' in sys.argv: args = [a for a in args if a != str(LAST)]

SEED = "if (SHIP.career && SHIP.career.gs !== DM_SEED) SHIP.career.gs = DM_SEED"
BED = r"""(() => {                                          // beside your bed, as the walk there would leave you
  const id = playerBed(), n = deckOf(id), bed = (DECKS[n].places || []).find(p => p.id === id); if (!bed) return 'no bed';
  if (deckDef.num !== n) goToDeck(n);
  const w = cellPos(...bed.at), c = nearestOpen(w.x, w.z, player); player.obj.position.copy(cellPos(...c)); player.stop(); return 'bed ' + id; })()"""
TAKE = r"""(() => { for (const m of SHIP.mail || []) m.read = true;
  if (SHIP.player.track === null) SHIP.player.track = undefined;   // job tracking on, as a fresh game has it
  saveGame(); const s = JSON.parse(localStorage.getItem(SAVE_KEY)); delete s.dev;
  return { save: JSON.stringify(s), arrived: localStorage.getItem(INTRO_KEY) || '1', sum: devmodeDaySum() }; })()"""

class Rec(Follower):                                    # the follower, keeping the seed
    def run(self, until, every=6):
        pg = self.pg
        while pg.ev('shipNow()') < until:
            pg.ev(SEED); super().run(min(until, pg.ev('shipNow()') + 60), every)

def evening(pg, f, d):                                  # Day d's evening: to bed at 21:30, up at 06:00 on Day d+1
    f.run((d - 1) * 1440 + 21 * 60 + 30)
    pg.ev("devmodeSettle(); for (const k of NEED_KEYS) SHIP.player.needs[k] = Math.max(SHIP.player.needs[k], 85)")
    pg.ev(BED); pg.ev("sleepGo(360)")
    for _ in range(100):                                # the fade's timers are real time; no frames meanwhile, so it wakes at 06:00 exactly
        pg.page.wait_for_timeout(50)
        if not pg.ev('sleeping') and pg.ev('SHIP.time.day') == d + 1: break
    s = pg.ev('[SHIP.time.day, SHIP.time.min]')
    if s != [d + 1, 360]: raise RuntimeError(f'Day {d}: woke at Day {s[0]} {s[1]} min, not Day {d + 1} 06:00')

def kept_up(pg, d):                                     # did the follower do Day d as a player should?
    s = pg.ev(STATE); why = []
    if d >= 1 and pg.ev(f'playerShiftOn({d})') and not pg.ev(f'(SHIP.player.clockLog || {{}})[{d}] || 0'): why.append('never clocked in')
    for x, ms in WEEK:
        if x <= d: why += [f'"{m}" not learned' for m in ms if s['tr'].get(m) is None]
    return why

def pack(t): return base64.b64encode(zlib.compress(t['save'].encode(), 9)).decode()

def record(ctx, last):
    out, played = {}, True
    pg = Page(ctx, PATH); f = Rec(pg); pg.ev(SEED)
    log = []
    for d in range(0, last):
        try:
            if played:
                evening(pg, f, d)
                why = kept_up(pg, d)
                if why: played = False; log.append(f'Day {d}: the follower fell behind ({", ".join(why)}); Day {d + 1} on: through Set career')
        except Exception as e:
            played = False; log.append(f'Day {d}: the follower stopped ({str(e)[:200]}); Day {d + 1} on: through Set career')
        if not played:
            pg2 = Page(ctx, PATH)
            if d == 0: pg2.ev("devmodeRun('Set career', () => devmodeSetCareerTo(1))")   # Day 1 06:00 (nothing is taught before Day 2)
            else: pg2.ev(f"devmodeRun('Set career', () => {{ devmodeSetCareerTo({d}); devmodeSkipTo({d * 1440 + 360}); devmodeWake(); }})")   # the career by the end of Day d, then Day d+1 06:00 in bed (RV6: not d+1's, a day ahead)
            pg2.step(10)
            t = pg2.ev(TAKE); pg2.page.close()
        else:
            t = pg.ev(TAKE)
        t['played'] = played; t['z'] = pack(t); out[d + 1] = t
        print(f'  Day {d + 1}: {"played" if played else "Set career"}, save {len(t["save"])} chars, packed {len(t["z"])}; trained {t["sum"]["tr"]}, band {t["sum"]["band"]}, jobs {t["sum"]["jobs"]}', flush=True)
    for l in log: print('  ' + l)
    if pg.errors: print('  page errors:', pg.errors[:3])
    pg.page.close()
    return out

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    if TWICE:
        a = record(ctx, 2); ctx2 = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1); c = record(ctx2, 2)
        same = all(a[d]['save'] == c[d]['save'] for d in a)
        def where(x, y, path=''):                       # the paths that differ (the first 12)
            if type(x) != type(y): return [path or '/']
            if isinstance(x, dict): return [p for k in sorted(set(x) | set(y)) for p in where(x.get(k), y.get(k), path + '/' + k)]
            if isinstance(x, list): return [p for i in range(max(len(x), len(y))) for p in where(x[i] if i < len(x) else None, y[i] if i < len(y) else None, f'{path}[{i}]')]
            return [] if x == y else [f'{path}: {str(x)[:60]} / {str(y)[:60]}']
        for d in a:
            if a[d]['save'] != c[d]['save']: print(f'  Day {d} differs at:', where(json.loads(a[d]['save']), json.loads(c[d]['save']))[:12])
        print('DAY SAVES TWICE OK' if same else 'DAY SAVES TWICE FAILED: the two recordings differ'); b.close(); sys.exit(0 if same else 1)
    days = record(ctx, LAST)
    b.close()

html = pathlib.Path(PATH).read_text()
build = re.search(r"const GAME_BUILD = '([^']+)'", html).group(1)
try: rec = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], cwd=ROOT, capture_output=True, text=True).stdout.strip()
except Exception: rec = ''
block = {'build': build, 'rec': rec, 'days': {str(d): {'played': t['played'], 'sum': t['sum'], 'arrived': t['arrived'], 'z': t['z']} for d, t in days.items()}}
total = sum(len(t['z']) for t in days.values())
print(f'day saves: {len(days)} days, {total} chars packed')
if WRITE:
    a, z = '// ---- day saves: start', '// ---- day saves: end ----'
    i = html.index(a); i = html.index('\n', i) + 1; j = html.index(z)
    html = html[:i] + 'function devmodeDaysData() { return ' + json.dumps(block, separators=(',', ':')) + '; }\n' + html[j:]
    pathlib.Path(PATH).write_text(html); print(f'day saves: written into {PATH}')
