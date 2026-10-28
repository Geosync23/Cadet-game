// shared.js: which top-level functions and tables are used outside the section that makes them (the owners map's lists).
//   node tools/shared.js [GAME.html] [--min N] [--md]     (acorn from $CADET_WORK/acorn/package, as names_check.js)
// For each top-level function, and each top-level UPPER_CASE const/let, in the game's script: the section it is made in
// (names_check.js's and tools/section.py's headings), its exact signature (functions), its shape (tables: object keys,
// array, Map, ...) and the other sections that read or call it. Lists those used by at least N other sections
// (default 3). --md prints rows for plans/owners.md. Changes nothing.
const fs = require('fs'), path = require('path');
const ROOT = path.join(__dirname, '..');
const args = process.argv.slice(2), md = args.includes('--md');
const mi = args.indexOf('--min'), MIN = mi >= 0 ? +args[mi + 1] : 3;
const GAME = args.find((a, i) => !a.startsWith('--') && args[i - 1] !== '--min') || path.join(ROOT, 'starship-cadet.html');
const acorn = require(path.join(process.env.ACORN_DIR || path.join(process.env.CADET_WORK || '/tmp/cadet-work', 'acorn/package'), 'dist/acorn.js'));
const html = fs.readFileSync(GAME, 'utf8');
const a = html.indexOf('<script>\n') + 9, src = html.slice(a, html.lastIndexOf('</script>'));
const L = html.split('\n'), SEC = [];
for (let i = 0; i < L.length; i++) { const m = /^\/\/ (\d+[a-z]?)\.? ([A-Z][A-Z&'()-]+\b.*)$/.exec(L[i]); if (m) SEC.push({ line: i + 1, id: m[1] }); }
const NL = []; for (let i = html.indexOf('\n'); i >= 0; i = html.indexOf('\n', i + 1)) NL.push(i);
const lineOf = i => { let lo = 0, hi = NL.length; while (lo < hi) { const m = (lo + hi) >> 1; if (NL[m] < a + i) lo = m + 1; else hi = m; } return lo + 1; };
const secOf = i => { const n = lineOf(i); let s = 'page'; for (const x of SEC) if (x.line <= n) s = x.id; return s; };
const ast = acorn.parse(src, { ecmaVersion: 2022, sourceType: 'script' });
const iife = ast.body.find(s => s.type === 'ExpressionStatement' && s.expression.type === 'CallExpression' && s.expression.callee.type === 'ArrowFunctionExpression');
const body = iife.expression.callee.body.body;
const defs = new Map();   // name -> { kind, sec, line, sig }
const sig = f => src.slice(f.start, f.body.start).replace(/\s+/g, ' ').replace(/^async /, 'async ').trim();
const shape = init => {
  if (!init) return 'let, set later';
  if (init.type === 'ObjectExpression') { const k = init.properties.filter(p => p.type === 'Property').map(p => p.key.name ?? p.key.value); return `{ ${k.slice(0, 6).join(', ')}${k.length > 6 ? `, ... (${k.length} keys)` : ''} }`; }
  if (init.type === 'ArrayExpression') return `[ ${init.elements.length} entries ]`;
  if (init.type === 'NewExpression') return `new ${init.callee.name}(...)`;
  if (init.type === 'Literal') return JSON.stringify(init.value);
  return src.slice(init.start, Math.min(init.end, init.start + 50)).replace(/\s+/g, ' ') + (init.end - init.start > 50 ? '...' : '');
};
for (const s of body) {
  if (s.type === 'FunctionDeclaration') defs.set(s.id.name, { kind: 'function', sec: secOf(s.start), line: lineOf(s.start), sig: sig(s) });
  if (s.type === 'VariableDeclaration') for (const d of s.declarations) if (d.id.type === 'Identifier') {
    const n = d.id.name;
    if (d.init && /Function/.test(d.init.type)) defs.set(n, { kind: 'function', sec: secOf(d.start), line: lineOf(d.start), sig: s.kind + ' ' + n + ' = ' + sig(d.init) });
    else if (/^[A-Z][A-Z0-9_]+$/.test(n)) defs.set(n, { kind: d.init && /^(Object|Array|New)Expression$/.test(d.init.type) ? 'table' : 'state', sec: secOf(d.start), line: lineOf(d.start), sig: `${s.kind} ${n} = ${shape(d.init)}` });
  }
}
const users = new Map();
const visit = n => {   // every identifier read in the script (a.b's b and an object's plain keys are only names, skipped)
  if (Array.isArray(n)) { for (const x of n) visit(x); return; }
  if (!n || typeof n.type !== 'string') return;
  if (n.type === 'MemberExpression' && !n.computed) { visit(n.object); return; }
  if ((n.type === 'Property' || n.type === 'MethodDefinition' || n.type === 'PropertyDefinition') && !n.computed && !n.shorthand) { visit(n.value); return; }
  if (n.type === 'Identifier' && defs.has(n.name)) { const s = secOf(n.start); if (s !== defs.get(n.name).sec) { if (!users.has(n.name)) users.set(n.name, new Set()); users.get(n.name).add(s); } }
  for (const k in n) if (k !== 'type' && n[k] && typeof n[k] === 'object') visit(n[k]);
};
visit(ast);
const rows = [...defs].map(([n, d]) => ({ n, ...d, u: [...(users.get(n) || [])] })).filter(r => r.u.length >= MIN).sort((x, y) => y.u.length - x.u.length || x.n.localeCompare(y.n));
if (md) { const at = id => { const i = SEC.findIndex(x => x.id === id); return i < 0 ? -1 : SEC[i].line; }; rows.sort((x, y) => at(x.sec) - at(y.sec) || x.line - y.line); }   // --md: by section, in file order
for (const r of rows) {
  if (md) console.log(`| \`${r.sig.replace(/\|/g, '\\|')}\` | ${r.kind} | ${r.sec} | ${r.line} | ${r.u.length}: ${r.u.join(', ')} |`);
  else console.log(`${r.kind.padEnd(8)} ${r.n.padEnd(24)} section ${r.sec.padEnd(4)} line ${String(r.line).padEnd(6)} used by ${r.u.length}: ${r.u.join(' ')}\n         ${r.sig}`);
}
console.log(`${md ? '<!-- ' : ''}shared.js: ${rows.length} of ${defs.size} top-level functions and tables are used by ${MIN}+ other sections${md ? ' -->' : ''}`);
