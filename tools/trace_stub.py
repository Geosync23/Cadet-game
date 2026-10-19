# TEST ONLY (M3, 0.53.0): stands in for seat S2's section-17 tracing pieces until they land. Usage: python3 tools/trace_stub.py GAME.html COPY.html, then mech_check.py COPY.html m9
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src).read()
def rep(old, new, n=1):
    global s
    assert s.count(old) == n, (s.count(old), old[:90]); s = s.replace(old, new)

STUB = r"""
// ---- S2 STAND-IN (test copy only): MACHINE_LINKS, linePath, lineOf, lineFlow ----
const MACHINE_LINKS = {
  water: ['3-recycler-1', '3-filter-1', '3-uv-1', '3-pump-1', ['5-pump-1', '5-pump-2'], { '5-valve-1': [1, 2, 3], '5-valve-2': [4, 5, 6] }],
  heat: ['4-heater-1', ['4-pump-1', '4-pump-2'], '5-manifold-1'],
  air: ['5-electrolyser-1', ['5-o2-1', '5-o2-2'], ['5-scrubber-1', '5-scrubber-2'], '5-fan-1', { '5-damper-1': [1, 2, 3], '5-damper-2': [4, 5, 6] }],
};
const LINE_ENDS = { air: { '5-damper-1': { 2: ['2-extractor-1'] }, '5-damper-2': { 4: [['4-scrubber-1', '4-scrubber-2']] } } };
function linePath(line, deck) {
  const L = MACHINE_LINKS[line]; if (!L) return null; const out = [];
  for (const x of L) {
    if (typeof x === 'string' || Array.isArray(x)) { out.push([].concat(x)); continue; }
    const b = Object.keys(x).find(id => x[id].includes(deck)); if (!b) return null; out.push([b]);
    const e = LINE_ENDS[line] && LINE_ENDS[line][b] && LINE_ENDS[line][b][deck]; if (e) for (const y of e) out.push([].concat(y));
  }
  const real = out.every(st => st.every(id => machineList().some(m => m.id === id && !m.stub)));
  return real ? out : null;
}
const lineOf = id => Object.keys(MACHINE_LINKS).filter(l => [1, 2, 3, 4, 5, 6].some(d => (linePath(l, d) || []).some(st => st.includes(id))));
const lineStep = c => c >= 50 ? 1 : c >= 25 ? .5 + .3 * (c - 25) / 25 : c / 50;
function lineFlow(line, id) {
  machinesNow(); let p = null;
  for (const d of [1, 2, 3, 4, 5, 6]) { const q = linePath(line, d); if (q && q.some(st => st.includes(id))) { p = q; break; } }
  if (!p) return 1; let v = 1;
  for (const st of p) { v *= Math.min(...st.map(x => lineStep(machEff(SHIP.machines[x])))); if (st.includes(id)) break; }
  return v;
}
"""
rep("const JOB_FOR = { worn: 'service', faulty: 'repair', failing: 'repair', broken: 'overhaul' };",
    STUB + "const JOB_FOR = { worn: 'service', faulty: 'repair', failing: 'repair', broken: 'overhaul' };")
rep("        if (j.cause && kind === 'repair' && typeof caseOffer === 'function') caseOffer(j, h);   // 24k (0.33.47)",
    "        if (j.cause && kind === 'repair' && typeof caseOffer === 'function') caseOffer(j, h);   // 24k (0.33.47)\n        if (kind === 'repair' && typeof traceOffer === 'function') traceOffer(j, h);")
rep("    if (cause && typeof caseOffer === 'function') caseOffer(jobs[jobs.length - 1], h);   // 24k's case engine may make it a head-scratcher (0.33.47)",
    "    if (cause && typeof caseOffer === 'function') caseOffer(jobs[jobs.length - 1], h);   // 24k's case engine may make it a head-scratcher (0.33.47)\n    if (typeof traceOffer === 'function') traceOffer(jobs[jobs.length - 1], h);")
rep("  const m = machineById(j.machine), room = (DECKS[m.deck].rooms[m.room] || {}).name;\n  const state = j.status === 'waiting'",
    "  if (typeof traceHidden === 'function' && traceHidden(j)) return traceCard(j, who);\n  const m = machineById(j.machine), room = (DECKS[m.deck].rooms[m.room] || {}).name;\n  const state = j.status === 'waiting'")
rep("  const m = machineById(j.machine); if (!m) return [];\n  const pp = panelPlace(m.id);",
    "  if (typeof traceHidden === 'function' && traceHidden(j)) return traceStops(j, known);\n  const m = machineById(j.machine); if (!m) return [];\n  const pp = panelPlace(m.id);")
rep("    const [title, where, state] = jobCard(j), m = j.machine && machineById(j.machine);\n    const stops = jobStops(j)",
    "    const [title, where, state] = jobCard(j), m = j.machine && !(typeof traceHidden === 'function' && traceHidden(j)) && machineById(j.machine);\n    const stops = jobStops(j)")
if "  damper:" not in s:   # S2's kind (0.33.55, e82abed) when the copy doesn't have it yet
    rep("  fan:         { name: 'Main fan',", "  damper:      { name: 'Duct dampers',      sys: 'air',        life: 30, time: 1,                 scope: 'ship', w: 1, tier: 2, part: 'relay' },\n  fan:         { name: 'Main fan',")
open(dst, 'w').write(s)
print('stub applied')
