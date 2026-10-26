(() => { SHIP_EVENTS.veyliVessel = { title: 'A Veyli vessel needs help', days: 4, commend: false, threads: [], pause: [], keep: [], settle: 'resolution',
  phases: [{ id: 'warning', at: [0, 340] }, { id: 'onset', at: [1, 480] }, { id: 'escalation', at: [2, 0] }, { id: 'resolution', at: [3, 540], clears: true }, { id: 'afterglow', at: [3, 600], clears: true }],
  systems: {}, routines: {}, galley: {}, status: {}, news: [] };
  vesselLooksInit(); return !!SHIP_EVENTS.veyliVessel.dressing; })()