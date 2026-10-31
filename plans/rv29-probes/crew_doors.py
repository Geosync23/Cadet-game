# RV29: PL2 note 13: the crew's cabin comings and goings. Dev jump to Day D (default 3) at AT (default 06:40) on Deck 4,
# you stand in the officers' corridor ('-'), run N ship minutes at frame pace; every ship minute: each crew member's room
# and which closed doors are drawn open. Prints a hash and the trace, to compare two builds. usage: crew_doors.py WT BUILD
import sys, os, json, hashlib
WT, BUILD = sys.argv[1], sys.argv[2]
sys.argv = [sys.argv[0], BUILD]
src = open(WT + '/devmode_check.py').read().split("\ndef part_off")[0].replace("__file__.replace('devmode_check.py', 'cadet_test.py')", repr(WT + '/cadet_test.py'))
exec(src)
D, AT, N, DK, RM = int(os.environ.get('CD_DAY', '3')), int(os.environ.get('CD_AT', '400')), int(os.environ.get('CD_N', '45')), int(os.environ.get('CD_DECK', '4')), os.environ.get('CD_ROOM', '-')
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get('CADET_CHROME'), args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    pg = Page(ctx, '#dev'); pg.sign(); pg.step(20)
    print('jump', pg.ev(f"devmodeRun('Jump', () => devmodeSetCareerTo({D}, {{ id: 'rv29c', label: 'c', day: {D}, by: {D - 1}, at: {AT}, where: {{ deck: {DK}, room: '{RM}' }} }}))")); pg.step(20)
    print('where', pg.ev("[deckDef.num, roomAt(...player.here()), hhmm(SHIP.time.min)]"))
    trace = []; last = None
    for i in range(N * 6):
        pg.step(5)
        m = pg.ev("SHIP.time.min")
        if m == last: continue
        last = m
        s = pg.ev("""(() => ({ t: hhmm(SHIP.time.min), crew: DECK_CREW.filter(a => a.p).map(a => a.p.id + '@' + roomAt(...cellAt(a.x, a.z))).sort().join(' '),
          open: DOOR_OBJS.filter(o => o.e.type === 'closed' && o.open > .5).map(o => o.e.key).sort().join(' '), me: roomAt(...player.here()) }))()""")
        trace.append(s)
    h = hashlib.sha256(json.dumps([x['crew'] for x in trace]).encode()).hexdigest()[:16]
    print('crew hash', h, 'minutes', len(trace))
    for s in trace: print(s['t'], 'me', s['me'], '| open', s['open'] or '-', '|', s['crew'][:300])
    print('errors', pg.errors[:5]); b.close()
