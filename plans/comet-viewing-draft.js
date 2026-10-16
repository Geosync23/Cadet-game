// Comet viewing: drafted at 0.34.18 by the events engineer, NOT in the build (the user, 2026-10-16: "we will do the rest later").
// To build it: paste this block into section 18 just before "// the ship-wide events' gathering moments", add 'comet' to EVENT_ORDER
// between 'ionStorm' and 'diplomatic', and add the COMET check to events_check (see plans/handover-events.md).
// It was tested on paper: due day 21 in a new game, 18 crew at the bow lounge, 2 in the observatory, traditions paused.
// ---- comet viewing (a short event, between the storm and the visit; plans/pillar3-plan.md, "The shorter events"):
// one gentle evening. Sato's Mail in the morning, then from 21:00 the comet at the bow lounge windows (the deck
// architect's crowd spots) and in the observatory. No strain, no threads (it always goes smoothly); the traditions
// that evening give way to it. Day 1 is a little afterglow of chatter
SHIP_EVENTS.comet = {
  title: 'Comet viewing', days: 2, gap: 3, need: ['sato'], draft: true,   // on when the lead says (events_check runs it)
  phases: [{ id: 'warning', at: [0, 480] }, { id: 'onset', at: [0, 1230] }, { id: 'resolution', at: [0, 1350], clears: true },
    { id: 'afterglow', at: [1, 0], clears: true }],
  pause: ['onset'], keep: ['birthday'],
  systems: { onset: { effects: ['skyComet'] } },          // the performance engineer may light the windows (inert until then)
  routines: {}, galley: {}, jobs: {},
  news: [
    { id: 'comet-coming', from: 'sato', phase: 'warning', at: [0, 480], seed: ['dept:survey'], weight: 2,
      lines: ['There\'s a comet passing tonight. Sato says the tail will fill the bow windows.', 'Comet at nine. Get a window seat early.'] },
    { id: 'comet-told', phase: 'afterglow', at: [1, 420], seed: ['all'], weight: 1,
      lines: ['Did you see the tail last night? Green all the way along.', 'Half the ship was at the bow windows. Best seat on the ship.'] },
  ],
  moments: [
    { id: 'cometLounge', name: 'Comet viewing', phase: 'onset', at: [0, 1260], len: 75, where: { venue: 'bow-lounge', deck: 3, room: /^Bow lounge$/ }, gathering: true, who: .55, anim: null,
      ask: 'Comet tonight at nine. The bow windows are the place.', here: 'Look at the tail on it.', thanks: 'You find a spot at the bow windows as the comet slides past, its tail lit green.' },
    { id: 'cometObservatory', name: 'Comet viewing (observatory)', phase: 'onset', at: [0, 1260], len: 75, where: { deck: 2, room: /^Observatory$/ }, gathering: true, who: .3, anim: null,
      ask: 'Sato\'s opening the observatory for the comet tonight.', here: 'Through the scope you can see the ice boiling off it.', thanks: 'You take a turn at the observatory scope. The comet\'s head is a fizzing ball of ice.' },
  ],
  meetings: [],
  mail: { warning: { from: 'Dr. Imra Sato', subject: 'A comet tonight', body: 'A comet passes us tonight from about 21:00, close enough to see its tail from the bow lounge windows. The observatory will be open for anyone who wants a look through the scope. Wrap up warm.' } },
  threads: [], traces: { smooth: [], bumpy: [], rough: [] },
};

/* events_check.py parts (paste the JS before 'ok = True', the Python before the console check):
# comet viewing (the short event between the storm and the visit, 0.34.18) on paper: after the storm it's due 3+ days
# on, on a day Sato works; Sato's Mail; the evening's two gatherings (bow lounge, observatory) with people going; the
# traditions that evening paused; it ends smoothly with no threads
COMET = r"""(() => {
  const keep = { e: SHIP.event, log: SHIP.eventLog.slice(), tr: SHIP.traces.slice(), m: MEETINGS.splice(0), draft: SHIP_EVENTS.comet.draft };
  SHIP_EVENTS.comet.draft = false;
  SHIP.event = null; SHIP.eventLog.length = 0; SHIP.eventLog.push({ id: 'ionStorm', startDay: 10, endDay: 16, band: 'smooth', threads: {}, mine: {} }); EV_DAYS.clear();
  const due = eventDueDay(), sd = due.day, mails = [], send = mailSend; SHIP_DAYS.clear();   // plans made before it was on
  mailSend = m => { mails.push(Math.floor(m.at / 1440) + 1 - sd + ' ' + hhmm(m.at % 1440) + ' ' + m.subject); };
  const on = eventsOn(sd).map(e => e.id + ' ' + hhmm(e.from) + '-' + hhmm(e.to));
  const going = ['cometLounge', 'cometObservatory'].map(id => schedPeople().filter(p => planDay(p, sd).some(s => s.tag && s.tag.startsWith('ev-' + id))).length);
  eventStart('comet', sd); EV_DAYS.clear(); const steps = [];
  for (let t = (sd - 1) * 1440; t <= (sd + 2) * 1440; t += 15) { const o = eventAdvance(t, true); if (o.length) steps.push((Math.floor(t / 1440) + 1 - sd) + ' ' + hhmm(t % 1440) + ' ' + o.join(', ')); }
  mailSend = send;
  const R = { due, on, going, steps, mails, log: SHIP.eventLog.slice(1).map(l => l.band) };
  SHIP_EVENTS.comet.draft = keep.draft; SHIP.event = keep.e; SHIP.eventLog.length = 0; SHIP.eventLog.push(...keep.log); SHIP.traces.length = 0; SHIP.traces.push(...keep.tr);
  MEETINGS.length = 0; MEETINGS.push(...keep.m); EV_DAYS.clear(); SHIP_DAYS.clear();
  return R;
})()"""


    # 10. comet viewing on paper
    C = g.ev(COMET)
    print('Comet viewing: due', C['due'], '| that day', C['on'], '| going (lounge, observatory)', C['going'])
    print('  steps', C['steps'], '| Mail', C['mails'], '| result', C['log'])
    if not C['due'] or C['due']['id'] != 'comet' or C['due']['day'] < 19: fail(f"the comet's start: {C['due']}")
    if not any(x.startswith('cometLounge 21:00') for x in C['on']) or C['going'][0] < 8 or C['going'][1] < 2: fail(f"the comet's gatherings: {C['on']} {C['going']}")
    if any(x.split(' ')[0] in ('quiz', 'observatory-night', 'film', 'jam', 'hull-lights') for x in C['on']): fail(f"traditions not paused for the comet: {C['on']}")
    if C['log'] != ['smooth'] or not any('A comet tonight' in x for x in C['mails']): fail(f"the comet's end or Mail: {C['log']} {C['mails']}")

*/
