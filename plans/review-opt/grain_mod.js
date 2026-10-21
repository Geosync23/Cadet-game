// exhaustive-ish: random seeds in [1, m-1] plus edges, one step each; then long chains
const m = 2147483647;
const f = s => { const x = s * 16807, hi = Math.floor(x / 2147483648); s = x - hi * 2147483648 + hi; if (s >= m) s -= m; return s; };
const g = s => (s * 16807) % m;
let bad = 0; const edge = [1, 2, m - 1, m - 2, 127773, 127774, 2147483648 / 16807 | 0, 1 << 30, (1 << 30) + 1];
for (const s of edge) if (f(s) !== g(s)) bad++;
for (let k = 0; k < 3e7; k++) { const s = 1 + Math.floor(Math.random() * (m - 1)); if (f(s) !== g(s)) { bad++; if (bad < 5) console.log('bad', s); } }
for (const s0 of [11, 48211, 0]) { let a = s0, b = s0; for (let k = 0; k < 2e7; k++) { a = f(a); b = g(b); if (a !== b) { bad++; break; } } }
console.log('bad', bad);
