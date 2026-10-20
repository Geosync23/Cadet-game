// names_check.js: read the game's script the way the browser does, and find what would break it quietly.
//   node names_check.js [GAME.html]          (acorn from $CADET_WORK/acorn/package: npm pack acorn@8.12.1)
// FAILs, each with the piece and line it's in:
//   the game's script doesn't parse (as a browser script: a stray top-level return fails here, unlike node --check);
//   a piece doesn't parse on its own (it only parses thanks to its neighbours: a brace or comment left open);
//   a name declared twice at the game's top level (a second function silently replaces the first);
//   a key added twice to one shared table (const TABLE = {...} / Object.assign(TABLE, {...}): the second quietly wins);
//   "Deck 7" in a string (the rec deck's name on screen comes from deckWord).
const fs = require('fs'), path = require('path');
const ROOT = __dirname, GAME = process.argv[2] || path.join(ROOT, 'starship-cadet.html');
const acorn = require(path.join(process.env.ACORN_DIR || path.join(process.env.CADET_WORK || '/tmp/cadet-work', 'acorn/package'), 'dist/acorn.js'));
const html = fs.readFileSync(GAME, 'utf8');
const a = html.indexOf('<script>\n') + 9, b = html.lastIndexOf('</script>');
const src = html.slice(a, b), NL = [];
for (let i = html.indexOf('\n'); i >= 0; i = html.indexOf('\n', i + 1)) NL.push(i);
const lineOfGame = i => { let lo = 0, hi = NL.length; while (lo < hi) { const m = (lo + hi) >> 1; if (NL[m] < i) lo = m + 1; else hi = m; } return lo + 1; };
// where each piece starts in the game file (by line), when the pieces are there and glue to this file
let PIECES = [];
try {
  const order = fs.readFileSync(path.join(ROOT, 'pieces/ORDER'), 'utf8').split('\n').filter(l => l.trim() && !l.startsWith('#')).map(l => l.split(/\s+/)[0]);
  let line = 1, glued = '';
  for (const n of order) { const t = fs.readFileSync(path.join(ROOT, 'pieces', n), 'utf8'); PIECES.push({ n, line, t }); line += t.split('\n').length - 1; glued += t; }
  if (glued !== html) PIECES = [];
} catch (e) { PIECES = []; }
// without pieces (the one-file game): name the section a line is in, from the file's own "// 19. DEVICE ..." headings
const SECTIONS = [];
{ const L = html.split('\n'); for (let i = 0; i < L.length; i++) { const m = /^\/\/ (\d+[a-z]?)\. (.{0,40})/.exec(L[i]); if (m) SECTIONS.push({ line: i + 1, name: 'section ' + m[1] + ' (' + (m[2].length < 40 ? m[2].trim() : m[2].replace(/\s+\S*$/, '').trim() + '...') + ')' }); } }
const where = gameLine => {
  if (!PIECES.length) { let s = null; for (const x of SECTIONS) if (x.line <= gameLine) s = x; return s ? `${s.name}, game line ${gameLine}` : `game line ${gameLine}`; }
  let p = PIECES[0]; for (const q of PIECES) if (q.line <= gameLine) p = q;
  return `${p.n} line ${gameLine - p.line + 1} (game line ${gameLine})`;
};
const at = i => where(lineOfGame(a + i));
const bad = [];
let ast;
try { ast = acorn.parse(src, { ecmaVersion: 2022, sourceType: 'script' }); }
catch (e) { console.log('FAIL the game\'s script does not parse: ' + e.message.replace(/ \(\d+:\d+\)$/, '') + ' at ' + at(e.pos)); process.exit(1); }
for (const p of PIECES) if (p.n.endsWith('.js')) {
  try { acorn.parse(p.t, { ecmaVersion: 2022, sourceType: 'script', allowReturnOutsideFunction: true }); }
  catch (e) { bad.push(`piece ${p.n} does not parse on its own: ${e.message} (it only works joined to its neighbours: a brace, bracket or comment left open?)`); }
}
const iife = ast.body.find(s => s.type === 'ExpressionStatement' && s.expression.type === 'CallExpression' && s.expression.callee.type === 'ArrowFunctionExpression');
const body = iife.expression.callee.body.body, seen = new Map();
const add = (n, i) => { if (seen.has(n)) bad.push(`name ${n} made twice: ${seen.get(n)} and ${at(i)}`); else seen.set(n, at(i)); };
const ids = p => p.type === 'Identifier' ? [p] : p.type === 'ObjectPattern' ? p.properties.flatMap(q => ids(q.value || q.argument)) : p.type === 'ArrayPattern' ? p.elements.filter(Boolean).flatMap(ids) : p.type === 'AssignmentPattern' ? ids(p.left) : p.type === 'RestElement' ? ids(p.argument) : [];
const keys = new Map();
const SLOTS = new Set();   // TABLE = { x: null }: a slot that its owner fills once, later, with TABLE.x = ...
const addKeys = (t, obj) => { for (const p of obj.properties) if (p.type === 'Property' && !p.computed) { const k = t + '.' + (p.key.name ?? p.key.value); if (p.value.type === 'Literal' && p.value.value === null) SLOTS.add(k); if (keys.has(k)) bad.push(`key ${k} added twice: ${keys.get(k)} and ${at(p.start)}`); else keys.set(k, at(p.start)); } };
// repeats that are meant (each with why): a second registration replaces a shell on purpose, a table entry reset on load
const MEANT = new Set([
  'deviceApp:crew',   // section 19's shell, replaced by section 20's real app (the comment above the shell says so)
  'SHIP.tiles',       // the empty record, then tilesLoad(SAVED) over it
]);
const cname = c => c.type === 'Identifier' ? c.name : c.type === 'MemberExpression' && !c.computed ? cname(c.object) + '.' + c.property.name : '?';
const regs = new Map();
const addReg = (k, i) => { if (MEANT.has(k)) return; if (regs.has(k)) bad.push(`${k.includes(':') ? 'registration' : 'key'} ${k} made twice: ${regs.get(k)} and ${at(i)}`); else regs.set(k, at(i)); };
function walk(stmts, gated) {
  for (const s of stmts) {
    if (s.type === 'IfStatement') { for (const br of [s.consequent, s.alternate]) if (br) walk(br.type === 'BlockStatement' ? br.body : [br], true); continue; }
    if (s.type === 'BlockStatement') { walk(s.body, true); continue; }
    if (!gated) {   // names in a gated block are that block's own; table keys and registrations there are shared
      if (s.type === 'FunctionDeclaration' || s.type === 'ClassDeclaration') add(s.id.name, s.start);
      if (s.type === 'VariableDeclaration') for (const d of s.declarations) { for (const i of ids(d.id)) add(i.name, i.start); if (d.id.type === 'Identifier' && d.init && d.init.type === 'ObjectExpression' && /^[A-Z][A-Z0-9_]*$/.test(d.id.name)) addKeys(d.id.name, d.init); }
    }
    const e = s.type === 'ExpressionStatement' && s.expression;
    if (!e) continue;
    if (e.type === 'CallExpression' && e.callee.type === 'MemberExpression' && e.callee.object.name === 'Object' && e.callee.property.name === 'assign' && e.arguments[0] && e.arguments[0].type === 'Identifier')
      for (const o of e.arguments.slice(1)) if (o.type === 'ObjectExpression') addKeys(e.arguments[0].name, o);
    // registrations by id: deviceApp({ id: 'x', ... }), LIST.push({ id: 'x', ... }), worksTabAdd({ id: ... }) and the like
    if (e.type === 'CallExpression' && e.arguments[0] && e.arguments[0].type === 'ObjectExpression') {
      const id = e.arguments[0].properties.find(p => p.type === 'Property' && !p.computed && (p.key.name || p.key.value) === 'id' && p.value.type === 'Literal');
      if (id) addReg(cname(e.callee) + ':' + id.value.value, s.start);
    }
    // TABLE.key = ... (a shared table's entry set by assignment; also clashes with a key from its literal)
    if (e.type === 'AssignmentExpression' && e.operator === '=' && e.left.type === 'MemberExpression' && !e.left.computed && e.left.object.type === 'Identifier' && /^[A-Z][A-Z0-9_]*$/.test(e.left.object.name)) {
      const k = e.left.object.name + '.' + e.left.property.name;
      if (MEANT.has(k)) continue;
      if (SLOTS.has(k)) { SLOTS.delete(k); continue; }   // filling its null slot, once
      if (keys.has(k)) bad.push(`key ${k} added twice: ${keys.get(k)} and ${at(s.start)}`); else keys.set(k, at(s.start));
    }
  }
}
walk(body, false);
let texts = 0;
for (const t of acorn.tokenizer(src, { ecmaVersion: 2022 })) {
  if (t.type.label !== 'string' && t.type.label !== 'template') continue;
  texts++;
  if (/\bDeck 7\b/.test(String(t.value))) bad.push(`"Deck 7" in text that can reach the screen: ${at(t.start)}`);
}
console.log(`names_check: ${seen.size} top-level names, ${keys.size} shared-table keys, ${regs.size} registrations, ${texts} strings` + (PIECES.length ? `, ${PIECES.length} pieces` : ' (no pieces in step: game lines only)'));
for (const x of bad) console.log('FAIL ' + x);
if (!bad.length) console.log('names_check: OK');
process.exit(bad.length ? 1 : 0);
