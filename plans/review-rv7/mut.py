import sys, pathlib
src = pathlib.Path('tip.html').read_text()
M = {
 'm1_doable_old': ("(j.kind === 'chore' || typeof JOB_KINDS === 'object' && JOB_KINDS[j.kind] && !JOB_KINDS[j.kind].side) && typeof jobStepDone", "j.kind === 'chore' && typeof jobStepDone"),
 'm2_doable_side': ("JOB_KINDS[j.kind] && !JOB_KINDS[j.kind].side) && typeof jobStepDone", "JOB_KINDS[j.kind]) && typeof jobStepDone"),
 'm3_no_down': ("else if (GUIDE_SHIFT.band !== null && !up) toast(", "else if (false) toast("),
 'm4_no_meet_hold': ("|| (SHIP.occasions || []).some(r => r.status === 'asked' && now >= r.at - 5 && now < r.at + r.len)) return;\n  B.dry", ") return;\n  B.dry"),
 'm5_no_dialogue_hold': ("if (typeof DIALOGUE !== 'undefined' && DIALOGUE || c && (c.st", "if (c && (c.st"),
 'm6_no_train_hold': ("c && (c.st === 'watch' || c.st === 'do') || (SHIP.occ", "false || (SHIP.occ"),
 'm7_drill_trk': ("+ ', 15:00', drill: j.id });", "+ ', 15:00', drill: j.id, trk: 'career:drill', trkTo: j.until });"),
 'm8_seen_old': ("if (b !== 'new' && (up || GUIDE_SHIFT.band === null)) SHIP.guide.seen[k] = 1;", "if (b !== 'new') SHIP.guide.seen[k] = 1;"),
 'm9_takeable_old': ("L = L.filter(o => ixBoard.doable((SHIP.jobs || []).find(x => x.id === o.id)));", "L = L.filter(o => { const j = (SHIP.jobs || []).find(x => x.id === o.id); return !!j && (!!j.machine || j.kind === 'restock' || j.kind === 'chore' && typeof jobStepDone === 'function'); });"),
}
for k in sys.argv[1:]:
    a, b = M[k]; assert src.count(a) == 1, k
    pathlib.Path(f'mut_{k}.html').write_text(src.replace(a, b)); print('wrote', k)
