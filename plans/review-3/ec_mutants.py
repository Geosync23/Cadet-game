# PR3: break copies of the game and check bigevents_check.py fails on each (EC1 turn 1, bfb2b76).
# Run from a worktree of the branch:  python3 plans/review-3/ec_mutants.py starship-cadet.html
import sys, subprocess, pathlib
src = pathlib.Path(sys.argv[1]).read_text(); out = pathlib.Path('/tmp/rv/mut'); out.mkdir(parents=True, exist_ok=True)
M = {
 'm1_hold1500': ("id: 'fridayAddress', kind: 'held', weekday: 4, fromDay: 5, at: [930, 1020] }", "id: 'fridayAddress', kind: 'held', weekday: 4, fromDay: 5, at: [900, 1020] }"),
 'm2_party341': ("len: 120, k: 340, where:", "len: 120, k: 341, where:"),
 'm3_eventDayLive': ("function eventDay(d) {", "function eventDay(d) { if (SHIP.event) return true;"),
 'm4_onset1545': ("{ id: 'onset', at: [1, 840] }", "{ id: 'onset', at: [1, 945] }"),
 'm5_heldAlways': ("return EV_CAL_ON ? evHeldEnd(t) : t; }", "return evHeldEnd(t); }"),
 'm6_noSkip': ("filter(r => r.day < EV_LOAD_DAY &&", "filter(r => r.day < 0 &&"),
 'm9_guardOpen': ("if (on.some(b => b.kind !== 'test' && cross(b))) return false;", ""),
 'm10_captainTwice': ("if (kind === 'captain' && on.some(b => b.kind === 'test' || b.kind === 'captain')) return false;", ""),
 'm11_tableLate': ("? { at: 1140, len: 75 } : null;", "? { at: 1140, len: 95 } : null;"),
 'n1_notesWhileOff': ("if (EV_NOTES_ON && typeof simNote === 'function') simNote(", "if (true && typeof simNote === 'function') simNote("),
 'n2_noteTwice': ("simNote('eventPhase', { id: e.id, phase: ph, day: e.startDay, t: evBeatAt(e.startDay, def.phases[k].at) });", "simNote('eventPhase', { id: e.id, phase: ph, day: e.startDay, t: evBeatAt(e.startDay, def.phases[k].at) }); simNote('eventPhase', { id: e.id, phase: ph, day: e.startDay, t: evBeatAt(e.startDay, def.phases[k].at) });"),
 'n3_noteLate': ("simNote('eventPhase', { id: e.id, phase: ph, day: e.startDay, t: evBeatAt(e.startDay, def.phases[k].at) });", "simNote('eventPhase', { id: e.id, phase: ph, day: e.startDay, t: evBeatAt(e.startDay, def.phases[k].at) + 5 });"),
 'n4_noCue': ("eventPhase: [d => 'event.' + d.id + '.' + d.phase, 1]", "eventPhase: [d => 'evx.' + d.id + '.' + d.phase, 1]"),
 'm8_ladderSun': ('"id": "tiles-ladder", "k": 450, "name": "Tiles ladder", "when": {"weekday": 5}, "at": [900, 990]',
                  '"id": "tiles-ladder", "k": 450, "name": "Tiles ladder", "when": {"weekday": 6}, "at": [1150, 1200]'),
}
only = sys.argv[2:]
for k, (a, b) in M.items():
    if only and k not in only: continue
    if src.count(a) != 1: print(k, 'SKIP (text not found once)'); continue
    p = out / f'{k}.html'; p.write_text(src.replace(a, b))
    r = subprocess.run([sys.executable, 'bigevents_check.py', str(p)], capture_output=True, text=True)
    fails = [l for l in r.stdout.splitlines() if l.startswith('  FAIL')]
    print(k, 'caught' if r.returncode == 1 and fails else 'NOT CAUGHT', r.returncode, len(fails), (fails[:1] or [''])[0][:160])
