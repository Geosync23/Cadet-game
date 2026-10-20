// SR1 sketch: parse the glued game's script as a browser would (script goal), then list
// (1) names declared twice in the game's top-level scope (functions too: a second function silently wins),
// (2) keys added twice to one shared table by Object.assign(TABLE, {...}) / const TABLE = {...}.
// node names_check.js GAME.html [ACORN_DIR]
const fs = require('fs'), path = require('path');
const acorn = require(path.join(process.argv[3] || (process.env.CADET_WORK || '/tmp/cadet-work') + '/acorn/package', 'dist/acorn.js'));
const html = fs.readFileSync(process.argv[2], 'utf8');
const a = html.indexOf('<script>\n') + 9, b = html.lastIndexOf('</script>');
const src = html.slice(a, b), NL = [];
for (let i = html.indexOf('\n'); i >= 0; i = html.indexOf('\n', i + 1)) NL.push(i);
const lineOf = i => { let lo = 0, hi = NL.length; while (lo < hi) { const m = (lo + hi) >> 1; if (NL[m] < a + i) lo = m + 1; else hi = m; } return lo + 1; };
let ast;
try { ast = acorn.parse(src, { ecmaVersion: 2022, sourceType: 'script', locations: false }); }
catch (e) { console.log('FAIL the game does not parse: ' + e.message + ' (game line ' + lineOf(e.pos) + ')'); process.exit(1); }
const iife = ast.body.find(s => s.type === 'ExpressionStatement' && s.expression.type === 'CallExpression' && s.expression.callee.type === 'ArrowFunctionExpression');
const body = iife.expression.callee.body.body, seen = new Map(), bad = [];
const add = (n, at) => { if (seen.has(n)) bad.push(`name ${n}: game lines ${seen.get(n)} and ${lineOf(at)}`); else seen.set(n, lineOf(at)); };
const ids = p => p.type === 'Identifier' ? [p] : p.type === 'ObjectPattern' ? p.properties.flatMap(q => ids(q.value || q.argument)) : p.type === 'ArrayPattern' ? p.elements.filter(Boolean).flatMap(ids) : p.type === 'AssignmentPattern' ? ids(p.left) : p.type === 'RestElement' ? ids(p.argument) : [];
const keys = new Map();
const addKeys = (t, obj) => { for (const p of obj.properties) if (p.type === 'Property' && !p.computed) { const k = t + '.' + (p.key.name ?? p.key.value); if (keys.has(k)) bad.push(`key ${k}: game lines ${keys.get(k)} and ${lineOf(p.start)}`); else keys.set(k, lineOf(p.start)); } };
for (const s of body) {
  if (s.type === 'FunctionDeclaration' || s.type === 'ClassDeclaration') add(s.id.name, s.start);
  if (s.type === 'VariableDeclaration') for (const d of s.declarations) { for (const i of ids(d.id)) add(i.name, i.start); if (d.id.type === 'Identifier' && d.init && d.init.type === 'ObjectExpression' && /^[A-Z][A-Z0-9_]*$/.test(d.id.name)) addKeys(d.id.name, d.init); }
  const e = s.type === 'ExpressionStatement' && s.expression;
  if (e && e.type === 'CallExpression' && e.callee.type === 'MemberExpression' && e.callee.object.name === 'Object' && e.callee.property.name === 'assign' && e.arguments[0] && e.arguments[0].type === 'Identifier')
    for (const o of e.arguments.slice(1)) if (o.type === 'ObjectExpression') addKeys(e.arguments[0].name, o);
}
console.log(`${seen.size} top-level names, ${keys.size} shared-table keys`);
for (const x of bad) console.log('FAIL ' + x);
process.exit(bad.length ? 1 : 0);
