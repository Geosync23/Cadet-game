const fs = require('fs'); const s = fs.readFileSync(process.argv[2], 'utf8').split('\n');
for (const [name, line] of [['VOICE', 19595], ['LINES', 28251], ['TALKS', 33824]]) {
  // the block: JSON.parse([ '...', '...' ].join('')) ; find its end
  let i = line - 1, src = ''; while (!/^\]\.join\(|^\]\)/.test(s[i]) && i < line + 20000) { src += s[i] + '\n'; i++; } src += s[i];
  const expr = src.replace(/^const \w+ = /, '').replace(/;\s*$/, '');
  const t0 = process.hrtime.bigint(); const v = eval(expr); const t1 = process.hrtime.bigint();
  console.log(name, 'lines', i - line + 2, 'chars', src.length, 'parse+eval ms', Number(t1 - t0) / 1e6);
}
