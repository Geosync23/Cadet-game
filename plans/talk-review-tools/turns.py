import sys, os
os.chdir(sys.argv[1])
exec(open('cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
JS = r"""(() => {
  socInit(); SHIP.talks = { fired: {}, small: {} }; const out = {};
  for (const id of ['volkov-maeve', 'shah-dara', 'janssen-hugo', 'esposito-yara', 'pell', 'saruth']) {
    const p = SOC.crew[SOC.idx.get(id)] || ROSTER_GUESTS.find(g => g.id === id); if (!p) continue; relGet(p.id).tier = 3; const seq = [];
    for (let d = 2; d < 22; d++) { const t = d * 1440 + 720, pk = talkPackPick(p, t); if (!pk) { seq.push('none'); continue; } talkPackFire(p, pk, t); seq.push(pk.small ? 'small' : pk.talk.id.split('.').slice(0, 2).join('.')); }
    out[id] = seq.join(' ');
  }
  return out;
})()"""
with sync_playwright() as pw:
    g = Game(pw, 'starship-cadet.html', w=390, h=844, errors=[]); g.step(3); r = g.ev(JS)
    for k, v in r.items(): print(k, ':', v)
    g.close()
