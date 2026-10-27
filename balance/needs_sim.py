# BAL1 balance research: the player's seven needs over 28 days for several play styles, on paper.
# A faithful copy of the game's arithmetic (section 15, build b18d2b64): NEED_DRAIN [awake, asleep] per ship hour,
# needsDrain's 30-minute steps with needEffects' energy-drain multiplier, SLEEP_GAIN 12.5 with the taper above 90,
# WORK_HUNGER 3 and WORK_LEISURE 3 an hour on shift, the gains of PLAYER_ACTS and the social/leisure adds
# (meal company 0.2/min per stranger at your table, cap 6; tradition +15 leisure, social min(20,12*bond); call home
# +40 social +5 leisure; Talk a while +30 social +5 leisure; hobby +25 leisure; tea +4 food; clothes +8 hygiene;
# toilet -3 hygiene, basin gives it back; yesterday's clothes from 10:00 x1.6 hygiene drain).
# Ship effects (a failing recycler etc.) are left at 1. Run: python3 balance/needs_sim.py -> balance/data/needs.json
import json, pathlib
K = ['hunger', 'energy', 'hygiene', 'fitness', 'social', 'bathroom', 'leisure']
DRAIN = dict(hunger=(4, 6), energy=(4.8, 0), hygiene=(2.5, 1), fitness=(1.4, .35), social=(4.5, .5), bathroom=(6, 1.5), leisure=(2.4, 0))
FRESH = dict(hunger=60, energy=100, hygiene=60, fitness=70, social=70, bathroom=60, leisure=70)
HI, LO = 75, 25
FX = dict(energy=({'task': 1.15}, {'walk': .8}), fitness=({'drain': .94, 'walk': 1.05}, {'walk': .8, 'drain': 1.06}),
          hunger=({'drain': .96}, {'task': .85}), hygiene=({'sg': 1.5}, {'sg': .5}), social=({'task': 1.1}, {'drain': 1.05}),
          bathroom=({'task': 1.05}, {'task': .9}), leisure=({'fg': 1.25}, {'task': .9}))
cl = lambda v: max(0.0, min(100.0, v))
def eff(n):
    e = dict(walk=1, task=1, drain=1, sg=1, fg=1)
    for k in K:
        side = 0 if n[k] >= HI else 1 if n[k] < LO else None
        if side is None: continue
        for f, v in FX[k][side].items(): e[f] *= v
    if n['bathroom'] <= 0: e['walk'] *= .7
    return e

class P:
    def __init__(s): s.n = dict(FRESH); s.t = 0; s.log = []; s.shower_at = -1e9; s.dirty_from = None; s.toilet_owed = 0
    def drain(s, mins, asleep=False, work=False, except_=None, dirty=False):
        left = mins
        while left > 0:
            step = min(left, 30); h = step / 60; ed = 1 if asleep else eff(s.n)['drain']; left -= step
            for k in K:
                if k == except_: continue
                r = DRAIN[k][1 if asleep else 0] * (ed if k == 'energy' else 1)
                if k == 'hygiene' and dirty and not asleep: r *= 1.6
                if work and k == 'hunger': r += 3
                if work and k == 'leisure': r += 3
                s.n[k] = cl(s.n[k] - r * h)
            if asleep:
                g = 12.5 * h; full = max(0, min(g, 90 - s.n['energy'])); s.n['energy'] = cl(s.n['energy'] + full + (g - full) / 3)
            s.t += step; s.snap(asleep, work)
    def snap(s, asleep, work): s.log.append((s.t, asleep, work, dict(s.n)))
    def gain(s, k, v): s.n[k] = cl(s.n[k] + v)

def day(p, d, style, workday):
    """one day from 06:00 (or the style's wake) to the next 06:00; returns minutes free (awake, off shift, not on needs)"""
    st = STYLES[style]; T = lambda hh, mm=0: (d * 1440) + hh * 60 + mm
    free = 0; busy = 0
    def until(t, work=False, dirty_ok=True):
        nonlocal free
        m = t - p.t
        if m <= 0: return
        dirty = p.dirty_from is not None and p.t >= p.dirty_from
        p.drain(m, work=work, dirty=dirty)
        if not work: free += m
    def act(mins, need=None, g=0, work=False, extra=None):
        nonlocal busy
        dirty = p.dirty_from is not None and p.t >= p.dirty_from
        p.drain(mins, work=work, except_=need, dirty=dirty)
        if need: p.gain(need, g)
        for k, v in (extra or {}).items(): p.gain(k, v)
        if not work: busy += mins
    def toilet():
        act(3, 'bathroom', 100, extra={'hygiene': -3}); act(1, extra={'hygiene': 3})   # wash hands
    wake = T(*st['wake'][1 if not workday else 0])
    # asleep until wake (the previous evening's bedtime handled at the end of the day)
    if p.t < wake: p.drain(wake - p.t, asleep=True)
    toilet()
    # clothes: change each morning if the style does, else yesterday's clothes from 10:00
    if st['clothes']: act(1, extra={'hygiene': 8}); p.dirty_from = None
    else: p.dirty_from = T(10)
    if st['shower_morning'] and p.t - p.shower_at >= 360: act(10, 'hygiene', 80); p.shower_at = p.t
    if st['breakfast'](d, workday):
        until(max(p.t, T(7, 30))); act(3); act(20, 'hunger', 55, extra={'social': 0.2 * st['table'] * 20 * eff(p.n)['sg']})
    elif st['grab'](d, workday): act(3, 'hunger', 25)
    if workday:
        until(T(9)); t_end = T(15, 30) if d % 7 == 4 else T(17)
        until(T(12), work=True); toilet()
        if st.get('lunch'): act(3, 'hunger', 25, work=True)
        until(T(13), work=True)
        if st['tea']: act(6, 'hunger', 4, work=True)
        until(T(15), work=True); toilet()
        until(t_end, work=True)
        if d % 7 == 4: until(T(16)); act(50, extra={'leisure': 15, 'social': 12})   # the Captain's address (a tradition's gain)
    else:
        until(T(11))
        if st['dayoff_hobby']: act(30, 'leisure', 25)
        until(T(13)); toilet()
        if st['grab'](d, False): act(3, 'hunger', 25)
        until(T(15))
    # evening
    until(max(p.t, T(17, 30))); toilet()
    if st['dinner'](d, workday): act(3); act(20, 'hunger', 55, extra={'social': 0.2 * st['table'] * 20 * eff(p.n)['sg']})
    if st['gym'](d, workday): act(30, 'fitness', 30, extra={'energy': -6})
    if st['shower_evening'](d) and p.t - p.shower_at >= 360: act(10, 'hygiene', 80); p.shower_at = p.t
    if st['call'](d): act(15, 'social', 40, extra={'leisure': 5})
    for _ in range(st['trads'](d, workday)): act(45, extra={'leisure': 15, 'social': min(20, 12 * st['bond'](d))})
    for _ in range(st['talks']): act(15, 'social', 30 * eff(p.n)['sg'] * st['bond'](d) / 1.0 if False else 30, extra={'leisure': 5})
    if st['hobby'](d, workday): act(30, 'leisure', 25)
    if st['bar'](d): act(15, extra={'hunger': 5, 'social': 5, 'leisure': 5})
    toilet()
    bed = T(*st['bed']); until(bed)
    return free, busy

STYLES = {
  # the diligent player: up at 06:00, everything every day, in bed 22:30
  'diligent': dict(wake=((6, 0), (7, 0)), bed=(22, 30), clothes=True, shower_morning=True, shower_evening=lambda d: False, table=3,
      breakfast=lambda d, w: True, grab=lambda d, w: True, dinner=lambda d, w: True, tea=True, gym=lambda d, w: True,
      call=lambda d: True, trads=lambda d, w: 1, talks=1, hobby=lambda d, w: True, bar=lambda d: False, dayoff_hobby=True, bond=lambda d: 1 + min(1, d / 28)),
  # a steady average player: gym every other day, call home every other day, a tradition most evenings, a talk a day
  'average': dict(wake=((7, 0), (8, 0)), bed=(23, 0), clothes=True, shower_morning=True, shower_evening=lambda d: False, table=3,
      breakfast=lambda d, w: True, grab=lambda d, w: False, dinner=lambda d, w: True, tea=True, gym=lambda d, w: d % 2 == 0,
      call=lambda d: d % 2 == 1, trads=lambda d, w: 1 if d % 3 else 0, talks=1, hobby=lambda d, w: not w, bar=lambda d: False, dayoff_hobby=True, bond=lambda d: 1 + min(.5, d / 28)),
  # the socialiser: two traditions and three talks every evening, the bar, never the gym
  'socialiser': dict(wake=((7, 15), (9, 0)), bed=(23, 30), clothes=True, shower_morning=True, shower_evening=lambda d: False, table=5,
      breakfast=lambda d, w: True, grab=lambda d, w: False, dinner=lambda d, w: True, tea=True, gym=lambda d, w: False,
      call=lambda d: d % 3 == 0, trads=lambda d, w: 2, talks=3, hobby=lambda d, w: False, bar=lambda d: True, dayoff_hobby=False, bond=lambda d: 1 + min(2, d / 10)),
  # the meal-skipper: up at 08:30, no breakfast (a grab now and then), dinner, otherwise average
  'skipper': dict(wake=((8, 30), (10, 0)), bed=(23, 30), clothes=True, shower_morning=True, shower_evening=lambda d: False, table=2,
      breakfast=lambda d, w: False, grab=lambda d, w: d % 2 == 0, dinner=lambda d, w: True, tea=False, gym=lambda d, w: d % 2 == 0,
      call=lambda d: d % 2 == 1, trads=lambda d, w: 1 if d % 3 else 0, talks=1, hobby=lambda d, w: not w, bar=lambda d: False, dayoff_hobby=True, bond=lambda d: 1.2),
  # the slacker: up late, no clean clothes, a shower every third evening, no gym, no calls, one meal, a hobby, late bed
  'slacker': dict(wake=((8, 45), (11, 0)), bed=(0, 30), clothes=False, shower_morning=False, shower_evening=lambda d: d % 3 == 0, table=0,
      breakfast=lambda d, w: False, grab=lambda d, w: True, dinner=lambda d, w: True, tea=False, gym=lambda d, w: False,
      call=lambda d: False, trads=lambda d, w: 0, talks=0, hobby=lambda d, w: True, bar=lambda d: False, dayoff_hobby=True, bond=lambda d: 1),
  # the diligent player plus a bite at lunch (the grab shelf at 12:00 on shift days)
  'diligent+lunch': dict(wake=((6, 0), (7, 0)), bed=(22, 30), clothes=True, shower_morning=True, shower_evening=lambda d: False, table=3,
      breakfast=lambda d, w: True, grab=lambda d, w: True, dinner=lambda d, w: True, tea=True, gym=lambda d, w: True, lunch=True,
      call=lambda d: True, trads=lambda d, w: 1, talks=1, hobby=lambda d, w: True, bar=lambda d: False, dayoff_hobby=True, bond=lambda d: 1 + min(1, d / 28)),
  # the workaholic who forgets to live: no traditions, no talks, no hobby, no calls (needs only)
  'grinder': dict(wake=((6, 0), (6, 0)), bed=(22, 0), clothes=True, shower_morning=True, shower_evening=lambda d: False, table=0,
      breakfast=lambda d, w: True, grab=lambda d, w: False, dinner=lambda d, w: True, tea=False, gym=lambda d, w: True,
      call=lambda d: False, trads=lambda d, w: 0, talks=0, hobby=lambda d, w: False, bar=lambda d: False, dayoff_hobby=False, bond=lambda d: 1),
}
def run(style, days=28):
    p = P(); p.t = 6 * 60   # Day 0 counted as day index 0 = the first Monday here (index 0..)
    p.t = 0; rows = []
    for d in range(days):
        wd = d % 7; work = wd < 5
        if st_bed_after_midnight(style) and d > 0: pass
        free, busy = day(p, d, style, work)
        rows.append(dict(d=d + 1, work=work, free=free, busy=busy))
    return p, rows
def st_bed_after_midnight(style): return STYLES[style]['bed'][0] < 6

if __name__ == '__main__':
    out = {}
    for s in [k for k in STYLES if not k.endswith('_')]:
        # the slacker's 00:30 bedtime: handle by shifting bed into the next morning
        p = P(); p.t = 0; rows = []
        for d in range(28):
            wd = d % 7; work = wd < 5
            st = STYLES[s]
            if st['bed'][0] < 6: st = dict(st, bed=(24 + st['bed'][0], st['bed'][1])); STYLES[s + '_'] = st
            free, busy = day(p, d, s + '_' if s + '_' in STYLES else s, work)
            rows.append(dict(d=d + 1, work=work, free=free, busy=busy))
        awake = [x for x in p.log if not x[1]]
        red = {k: sum(30 if False else 1 for x in awake if x[3][k] < LO) for k in K}
        mins = {k: 0 for k in K}; prev = None
        for x in p.log:
            if prev is not None and not x[1]:
                dt = x[0] - prev[0]
                for k in K:
                    if x[3][k] < LO: mins[k] += dt
            prev = x
        awake_total = sum(x[0] - y[0] for y, x in zip(p.log, p.log[1:]) if not x[1])
        lows = {k: round(min(x[3][k] for x in p.log[200:]), 1) for k in K}
        tired_walk = sum(x[0] - y[0] for y, x in zip(p.log, p.log[1:]) if not x[1] and eff(x[3])['walk'] < 1)
        slow_task = sum(x[0] - y[0] for y, x in zip(p.log, p.log[1:]) if x[2] and eff(x[3])['task'] < 1)
        fast_task = sum(x[0] - y[0] for y, x in zip(p.log, p.log[1:]) if x[2] and eff(x[3])['task'] > 1)
        worktotal = sum(x[0] - y[0] for y, x in zip(p.log, p.log[1:]) if x[2])
        curve = [(x[0], {k: round(v) for k, v in x[3].items()}) for x in p.log if x[0] % 60 == 0 and x[0] < 7 * 1440]
        out[s] = dict(red_share={k: round(mins[k] / awake_total * 100, 1) for k in K}, lows=lows,
                      walk_slowed_share=round(tired_walk / awake_total * 100, 1), work_slow_share=round(slow_task / max(1, worktotal) * 100, 1),
                      work_fast_share=round(fast_task / max(1, worktotal) * 100, 1),
                      free_workday=round(sum(r['free'] for r in rows if r['work']) / 20), free_dayoff=round(sum(r['free'] for r in rows if not r['work']) / 8),
                      end=dict((k, round(v)) for k, v in p.n.items()), curve=curve)
        o = out[s]
        print(f"{s:10} red% {o['red_share']}  lows {o['lows']}  walk-slowed {o['walk_slowed_share']}%  work slow {o['work_slow_share']}% fast {o['work_fast_share']}%  free min/workday {o['free_workday']} dayoff {o['free_dayoff']}")
    (pathlib.Path(__file__).parent / 'data' / 'needs.json').write_text(json.dumps(out))
