from pp import *
g = start('?nosave&debug'); g.step(5)
print(g.ev("""(() => ({ on: EV_GUARD_ON,
  ready: Array.from({length: 30}, (_, i) => i + 1).map(d => [d, occReadyDay(d) ? hhmm(occReadyAt(d)) : null]).filter(x => x[1] && x[1] !== '11:00' || [9,10,11,14,15,16,17,18,19,20,26].includes(x[0])),
  table: [6, 13, 17, 19, 20, 21, 27, 48].map(d => [d, occTableSlot(d) && hhmm(occTableSlot(d).at) + '+' + occTableSlot(d).len]),
  fri: [5, 12].map(d => [d, guardFree(d, 960, 1000, 'beat'), guardFree(d, 1020, 1050, 'beat')]),
  night20morning: [guardFree(21, 300, 330, 'beat'), guardFree(21, 400, 430, 'beat')],
  errs: 0 }))()"""))
print(g.errors[:3]); g.close()
