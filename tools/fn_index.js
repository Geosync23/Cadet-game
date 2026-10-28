// fn_index.js: the game's top-level declarations by line, and who reads each (for tools/affected.py and check_cover maps).
//   node tools/fn_index.js [GAME.html]      prints JSON: { decls: [[first line, last line, name, kind, section]], refs: { name: [top-level names that use it] },
//                                            uses: { name: [game lines where another declaration mentions it] } }
// A declaration is a top-level statement inside the game's IIFE: a function, a const/let/var (each declarator), a class;
// any other top-level statement is named '<section: its first line>' (with ' #2'... if repeated).
// kind: 'function' (functions and arrow/function consts), 'class', 'table' (object/array/new ...), 'state' (anything else).
// refs: for each declared name, the other top-level declarations whose code mentions it (an Identifier, not a property key).
// Lines are the game file's (as tools/section.py). acorn from $CADET_WORK/acorn/package, as names_check.js. Changes nothing.
const fs = require('fs'), path = require('path');
const GAME = process.argv[2] || path.join(__dirname, '..', 'starship-cadet.html');
const acorn = require(path.join(process.env.ACORN_DIR || path.join(process.env.CADET_WORK || '/tmp/cadet-work', 'acorn/package'), 'dist/acorn.js'));
const html = fs.readFileSync(GAME, 'utf8');
const a = html.indexOf('<script>\n') + 9, src = html.slice(a, html.lastIndexOf('</script>'));
const L = html.split('\n'), SEC = [];
for (let i = 0; i < L.length; i++) { const m = /^\/\/ (\d+[a-z]?)\.? ([A-Z][A-Z&'()-]+\b.*)$/.exec(L[i]); if (m) SEC.push({ line: i + 1, id: m[1] }); }
const NL = []; for (let i = html.indexOf('\n'); i >= 0; i = html.indexOf('\n', i + 1)) NL.push(i);
const lineOf = i => { let lo = 0, hi = NL.length; while (lo < hi) { const m = (lo + hi) >> 1; if (NL[m] < a + i) lo = m + 1; else hi = m; } return lo + 1; };
const secOf = n => { let s = 'page'; for (const x of SEC) if (x.line <= n) s = x.id; return s; };
const ast = acorn.parse(src, { ecmaVersion: 2022, sourceType: 'script' });
const iife = ast.body.find(s => s.type === 'ExpressionStatement' && s.expression.type === 'CallExpression' && s.expression.callee.type === 'ArrowFunctionExpression');
const decls = [], owners = [];   // owners: [start, end, name] per top-level statement, for refs
const anon = {};
for (const s of iife.expression.callee.body.body) {
  const one = (node, name, kind) => { const f = lineOf(node.start), l = lineOf(node.end - 1); decls.push([f, l, name, kind, secOf(f)]); owners.push([node, name]); };
  if (s.type === 'FunctionDeclaration') one(s, s.id.name, 'function');
  else if (s.type === 'ClassDeclaration') one(s, s.id.name, 'class');
  else if (s.type === 'VariableDeclaration') {
    for (const d of s.declarations) {
      const names = []; (function pat(p) { if (!p) return; if (p.type === 'Identifier') names.push(p.name); else if (p.type === 'ObjectPattern') p.properties.forEach(q => pat(q.value || q.argument)); else if (p.type === 'ArrayPattern') p.elements.forEach(pat); else if (p.type === 'AssignmentPattern') pat(p.left); else if (p.type === 'RestElement') pat(p.argument); })(d.id);
      const kind = d.init && /Function/.test(d.init.type) ? 'function' : d.init && /^(Object|Array|New)Expression$/.test(d.init.type) ? 'table' : 'state';
      // a one-statement declaration of several names: each name gets the whole declarator's lines
      for (const n of names) one(s.declarations.length === 1 ? s : d, n, kind);
    }
  } else {                                        // top-level code that runs at load (a registration, an assignment): named by its section and first line,
    const f = lineOf(s.start), k = secOf(f) + ': ' + L[f - 1].trim().slice(0, 60);   // which stays the same while lines move
    anon[k] = (anon[k] || 0) + 1; one(s, '<' + k + (anon[k] > 1 ? ' #' + anon[k] : '') + '>', 'statement');
  }
}
const declared = new Set(decls.map(d => d[2])), refs = {}, uses = {};
const walk = (node, owner) => {
  if (!node || typeof node.type !== 'string') return;
  if (node.type === 'Identifier' && declared.has(node.name) && node.name !== owner) { (refs[node.name] = refs[node.name] || new Set()).add(owner); (uses[node.name] = uses[node.name] || new Set()).add(lineOf(node.start)); }
  for (const k in node) {
    if (k === 'type' || k === 'start' || k === 'end') continue;
    const v = node[k];
    if (node.type === 'MemberExpression' && k === 'property' && !node.computed) continue;   // obj.name: a property, not the declaration
    if (node.type === 'Property' && k === 'key' && !node.computed && !node.shorthand) continue;
    if (Array.isArray(v)) v.forEach(x => walk(x, owner)); else if (v && typeof v === 'object') walk(v, owner);
  }
};
for (const [node, name] of owners) walk(node, name);
const out = {}, at = {}; for (const k in refs) { out[k] = [...refs[k]].sort(); at[k] = [...uses[k]].sort((x, y) => x - y); }
process.stdout.write(JSON.stringify({ game: path.basename(GAME), decls, refs: out, uses: at }));
