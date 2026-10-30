from pp import *
import json
SIM = r"""(({ drain, sleepGain, taper, workHunger, company, chats, bed, wake }) => {
  const n = SHIP.player.needs; Object.assign(n, NEEDS_FRESH); const D0 = JSON.parse(JSON.stringify(NEED_DRAIN));
  if (drain) for (const k in drain) NEED_DRAIN[k] = drain[k];
  const log = { hunger: [], social: [], fitness: [], wakeE: [], bedE: [] }; let clock = 360;
  const tick = (mins, f) => { for (let m = 0; m < mins; m++) { needsDrain(1, false); if (f) f(); clock++; } };
  const workTick = mins => tick(mins, () => { if (workHunger) n.hunger = needClamp(n.hunger - (workHunger - 1) * NEED_DRAIN.hunger[0] / 60); if (typeof WORK_LEISURE !== 'undefined') n.leisure = needClamp(n.leisure - WORK_LEISURE / 60); });
  const act = (kind, extra) => { const d = PLAYER_ACTS[kind]; for (let m = 0; m < d.mins; m++) { needsDrain(1, false, null, d.need);
    if (d.need) n[d.need] = needClamp(n[d.need] + d.gain / d.mins); if (d.cost) for (const k in d.cost) n[k] = needClamp(n[k] - d.cost[k] / d.mins); if (extra) extra(); clock++; } };
  const meal = () => act('eat', () => { n.social = needClamp(n.social + COMPANY_GAIN * company * needEffects(n).socialGain); });
  const sleep = mins => { for (let m = 0; m < mins; m++) { for (const k of NEED_KEYS) if (k !== 'energy') n[k] = needClamp(n[k] - NEED_DRAIN[k][1] / 60);
      const g = taper && n.energy >= taper[0] ? sleepGain * taper[1] : sleepGain; n.energy = needClamp(n.energy + g / 60); } };
  const snap = () => { log.hunger.push(Math.round(n.hunger)); };
  for (let day = 1; day <= 7; day++) {
    const work = day <= 5; log.wakeE.push(Math.round(n.energy));
    // 06:00 wake (or `wake`), toilet, shower, breakfast ~07:00, shift 09:00-17:00 (noon toilet), dinner 17:30, gym or call, hobby, bed
    const w0 = wake || 360; if (w0 > 360) sleep(w0 - 360);
    act('toilet'); tick(60 - (w0 - 360) > 0 ? 57 - (w0 - 360) : 0); act('shower'); tick(5); const hb = Math.round(n.hunger); meal(); const ha = Math.round(n.hunger); tick(25);
    const s0 = n.social; for (let c = 0; c < chats; c++) n.social = needClamp(n.social + CHAT_GAIN * needEffects(n).socialGain);
    tick(60); const h9 = Math.round(n.hunger); (work ? workTick : tick)(180); const h12 = Math.round(n.hunger); act('toilet'); (work ? workTick : tick)(297); const h17 = Math.round(n.hunger);
    tick(30); meal(); act('toilet'); tick(37);
    if (day % 2) act('gym'); else act('call'); act('hobby');
    const tb = bed || 1320; tick(tb - (18 * 60 + 30) - (day % 2 ? 60 : 45) - 3); act('toilet');
    log.bedE.push(Math.round(n.energy)); if (day === 1) log.day1 = { beforeBreakfast: hb, afterBreakfast: ha, at0900: h9, at1200: h12, at1700: h17 };
    log.social.push(Math.round(n.social)); log.fitness.push(Math.round(n.fitness));
    sleep(1440 + 360 - tb);
  }
  for (const k in D0) NEED_DRAIN[k] = D0[k]; Object.assign(n, NEEDS_FRESH);
  return log;
})"""
g = start('?nosave&debug'); g.step(5)
def run(label, **o):
    base = dict(drain=None, sleepGain=12.5, taper=None, workHunger=None, company=3, chats=2, bed=None, wake=None); base.update(o)
    r = g.ev(f"({SIM})({json.dumps(base)})"); print(label, json.dumps(r)); return r
run('TODAY')
run('TODAY bed 23:00', bed=1380)
run('TODAY bed 00:00 (6h)', bed=1439)
run('TODAY alone at meals, no chats', company=0, chats=0)
run('HUNGER work x1.5', workHunger=1.5)
run('HUNGER awake 5', drain={'hunger':[5,2]})
run('SOCIAL 2.5/.5', drain={'social':[2.5,.5]})
run('SOCIAL 2.5/.5 + company .12', drain={'social':[2.5,.5]})
run('SLEEP 10 + half above 90', sleepGain=10, taper=[90,.5])
run('SLEEP 10 + half above 90, bed 23', sleepGain=10, taper=[90,.5], bed=1380)
run('SLEEP 10 flat', sleepGain=10)
run('SLEEP 9 flat', sleepGain=9)
print(g.ev("({COMPANY_GAIN, CHAT_GAIN, SLEEP_GAIN, NEED_DRAIN, WORK_LEISURE: typeof WORK_LEISURE!=='undefined'?WORK_LEISURE:null})"))
g.close()
