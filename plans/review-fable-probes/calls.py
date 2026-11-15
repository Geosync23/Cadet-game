# how many times a frame the planner-ish functions are called in a busy scene (counts are exact, not timing)
import sys; sys.path.insert(0, '' + __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + ''); from g import *
FN = ['whereIs', 'planWhere', 'shipDay', 'eventsOn', 'worksEscort', 'p5Escort', 'p5TeacherWait', 'promoEscort', 'crewWayOn', 'placeSpot', 'schedPeople', 'findPath', 'crewPath', 'apptList', 'shipNow', 'seekWho', 'heldPose', 'crewPose', 'parsePose', 'evChanged', 'evSig', 'evArrival', 'flag', 'machinesNow', 'galleyAdvance', 'galleyShow', 'playerHolds', 'introOn', 'roomAt', 'crewNearDoor', 'youLock', 'tradJoinFrame', 'chatTick', 'linesTick', 'nightAt', 'applyLight', 'updateClock', 'stripTick', 'popupWatch', 'bubbleSay', 'toast', 'drawScreen', 'occupiedBy', 'nearestOpen', 'free', 'schedData', 'crewMood', 'crewNeeds', 'shipEffectsAt', 'relTier', 'socP', 'lineFor']
with sync_playwright() as pw:
    for day, tm, deck in [(1, '18:30', 3), (2, '10:00', 5)]:
        g = Game(pw, sys.argv[1]); h, m = map(int, tm.split(':')); g.ev(f"skipTo({(day - 1) * 1440 + h * 60 + m}); if (deckDef.num !== {deck}) goToDeck({deck})"); g.step(150)
        ok = g.ev("(() => { window.__n = {}; const ok = []; for (const f of " + json.dumps(FN) + ") { try { const o = eval(f); if (typeof o !== 'function') continue; window.__n[f] = 0; eval(f + ' = function (...a) { window.__n[\"' + f + '\"]++; return o.apply(this, a); }'); ok.push(f); } catch (e) {} } return ok; })()")
        g.ev("for (const k in window.__n) window.__n[k] = 0"); g.step(300)
        n = g.page.evaluate('window.__n'); people = g.ev('crowd.stats().people')
        print(f"\nDay {day} {tm} deck {deck}, {people} people; calls per frame over 300 frames (wrapped {len(ok)} of {len(FN)}):")
        print('  ' + '  '.join(f"{k} {v / 300:.1f}" for k, v in sorted(n.items(), key=lambda x: -x[1]) if v))
        g.close()
