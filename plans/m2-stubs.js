// TEST STUBS for section 17's Step 2 API (seat S's 0.33.48-49), only in test copies
var STUB_LIFT = false;
function machineDrift(id) { const s = SHIP.machines[id]; return s && s.drift || 0; }
function tuneSet(id, v) { const s = SHIP.machines[id]; if (!s) return false; s.drift = Math.max(-3, Math.min(3, v)); MACH_REV++; if (!s.drift) simNote('tuned', { machine: id }); return true; }
function machineFault(id, c = 40) { machinesNow(); const s = SHIP.machines[id]; if (!s) return false; s.cond = Math.min(s.cond, c); s.state = machineState(s.cond); MACH_REV++; return true; }
function liftStuck(on) { STUB_LIFT = !!on; }
jobKindAdd('joint', { tier: 1, work: 20, parts: ['seal'], text: 'Fit a joint', stops: j => [{ deck: j.deck, placeId: j.at, mins: 20, tag: 'job' }], done() {}, crew: { can: p => !!p.work && p.work.place === 'work:works', mins: 20 } });
function jointJobPost(o) { const j = jobMake('joint', { id: 'joint:' + o.placeId + '@' + Math.floor(shipNow() / 60), deck: o.deck, at: o.placeId, h: Math.floor(shipNow() / 60), title: 'Fit a joint' }); SHIP.jobs.push(j); return j.id; }
