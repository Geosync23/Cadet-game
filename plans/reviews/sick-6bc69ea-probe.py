import sys
exec(open('cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1]); ev = g.ev
    print(ev("""(() => { SHIP.time.day = 51; SHIP.time.min = 600; SHIP.career = null; careerInit(); const c = SHIP.career; c.sd = 51; c.sh = 0;
      goToDeck(3); const b = ROOM_BOX.I || null; const ids = Object.keys(ROOMS).filter(k => /Infirmary|Exam room/.test(ROOMS[k].name));
      const pl = (DECKS[3].places || []).find(p => ids.includes(p.room) && free(...p.at)) ; if (pl) player.obj.position.copy(cellPos(...pl.at));
      sickExamTick(shipNow()); const id = DIALOGUE && DIALOGUE.id, n = id && MEETING_SCRIPTS[id] ? MEETING_SCRIPTS[id].lines.length : 0;
      return { rooms: ids, at: pl && pl.id, dialogue: id, lines: n, scripts: ['sickExam1','sickExam2','sickExam3','sickExamCover'].map(k => !!MEETING_SCRIPTS[k]) }; })()"""))
    for e in g.errors: print('page error', e)
    g.close()
