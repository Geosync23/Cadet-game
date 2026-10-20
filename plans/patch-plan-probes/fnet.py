# F batch, the net Tier 1 repair time (PP1 revision, the reviewer's point 3): a steady player's week on paper with the
# game's own needsDrain / needEffects, today vs the user's chosen numbers; at every 15 minutes of each shift (Mon-Fri
# 09:00-17:00) the task speed, so the repair hold = 45 x factor / task. Same day shape as dpaper4.py.
from pp import *
import json
SIM = r"""(({ drain, taper, workHunger, company, chats, bed, gym }) => {
  const n = SHIP.player.needs; Object.assign(n, NEEDS_FRESH); const D0 = JSON.parse(JSON.stringify(NEED_DRAIN));
  if (drain) for (const k in drain) NEED_DRAIN[k] = drain[k];
  const samples = [], soc = [], wakeE = [], hiE = [], hiS = [];
  const tick = (mins, f) => { for (let m = 0; m < mins; m++) { needsDrain(1, false); if (f) f(m); } };
  const workTick = mins => tick(mins, m => { if (workHunger) n.hunger = needClamp(n.hunger - (workHunger - 1) * NEED_DRAIN.hunger[0] / 60); n.leisure = needClamp(n.leisure - WORK_LEISURE / 60);
      if (m % 15 === 0) { const e = needEffects(n); samples.push(e.task); hiE.push(n.energy >= 75 ? 1 : 0); hiS.push(n.social >= 75 ? 1 : 0); } });
  const act = (kind, extra) => { const d = PLAYER_ACTS[kind]; for (let m = 0; m < d.mins; m++) { needsDrain(1, false, null, d.need);
    if (d.need) n[d.need] = needClamp(n[d.need] + d.gain / d.mins); if (d.cost) for (const k in d.cost) n[k] = needClamp(n[k] - d.cost[k] / d.mins); if (extra) extra(); } };
  const meal = () => act('eat', () => { n.social = needClamp(n.social + COMPANY_GAIN * company * needEffects(n).socialGain); });
  const sleep = mins => { for (let m = 0; m < mins; m++) { for (const k of NEED_KEYS) if (k !== 'energy') n[k] = needClamp(n[k] - NEED_DRAIN[k][1] / 60);
      const g = taper && n.energy >= taper[0] ? SLEEP_GAIN * taper[1] : SLEEP_GAIN; n.energy = needClamp(n.energy + g / 60); } };
  for (let day = 1; day <= 7; day++) {
    const work = day <= 5; wakeE.push(Math.round(n.energy));
    act('toilet'); tick(57); act('shower'); tick(5); meal(); tick(25);
    for (let c = 0; c < chats; c++) n.social = needClamp(n.social + CHAT_GAIN * needEffects(n).socialGain);
    tick(60); (work ? workTick : tick)(180); act('toilet'); (work ? workTick : tick)(297);
    tick(30); meal(); act('toilet'); tick(37);
    if (gym) { if (day % 2) act('gym'); else act('call'); } else tick(day % 2 ? 60 : 45); act('hobby');
    const tb = bed; tick(tb - (18 * 60 + 30) - (day % 2 ? 60 : 45) - 3); act('toilet');
    soc.push(Math.round(n.social)); sleep(1440 + 360 - tb);
  }
  for (const k in D0) NEED_DRAIN[k] = D0[k]; Object.assign(n, NEEDS_FRESH);
  const avg = a => a.reduce((x, y) => x + y, 0) / a.length;
  return { task: Math.round(avg(samples) * 1000) / 1000, inv: Math.round(avg(samples.map(t => 1 / t)) * 1000) / 1000, min: Math.min(...samples), max: Math.max(...samples), wakeE, soc,
           rested: Math.round(avg(hiE) * 100), spirits: Math.round(avg(hiS) * 100) };
})"""
g = start('?nosave&debug'); g.step(5)
TODAY_SOC = g.ev('NEED_DRAIN.social')
def run(label, **o):
    base = dict(drain=None, taper=None, workHunger=None, company=3, chats=2, bed=22*60, gym=True); base.update(o)
    r = g.ev(f"({SIM})({json.dumps(base)})")
    print(label, json.dumps(r), '| repair 45 min x factor:', {f: round(45 * f * r['inv'], 1) for f in (1, .67, .6, .55, .5)})
    return r
for bed in (22*60, 23*60):
    print('--- bed', bed // 60)
    run('today          ', bed=bed)
    run('user: all four ', bed=bed, drain={'social': [3, .25]}, taper=[90, 1/3], workHunger=1.75)
    run('  social only  ', bed=bed, drain={'social': [3, .25]})
    run('  energy only  ', bed=bed, taper=[90, 1/3])
    run('  quiet player ', bed=bed, drain={'social': [3, .25]}, taper=[90, 1/3], workHunger=1.75, chats=0, company=1)
g.close()
