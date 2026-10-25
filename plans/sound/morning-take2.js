// Morning music take 2 (SD1, 2026-10-25): three ambient sci-fi synth candidates, Wake cycle, Systems online and Station dawn.
// Not in music-module.js yet. To use one, paste this block into createWrenMusic just before '// ---- every sample grows',
// add its level to MLV (wake 1.65, systems 1.75, dawn 1.9) and put its key in SETS.
  // ---- morning take 2: ambient sci-fi synth candidates (not on the schedule until the user picks)
  Object.assign(MI, {
    // a wide, slow synth pad: three detuned saws through a low filter that slowly opens and closes over the bar
    synthPad(t, notes, d, g, out, open = 1) {
      notes.forEach(m => [-9, 0, 9].forEach(c => {
        const o = ctx.createOscillator(), lp = ctx.createBiquadFilter(), e = ctx.createGain();
        o.type = 'sawtooth'; o.frequency.value = mtof(m); o.detune.value = c; lp.type = 'lowpass'; lp.Q.value = 0.7;
        lp.frequency.setValueAtTime(380, t); lp.frequency.linearRampToValueAtTime(380 + 900 * open, t + d * 0.55); lp.frequency.linearRampToValueAtTime(420, t + d);
        e.gain.setValueAtTime(0, t); e.gain.linearRampToValueAtTime(g, t + Math.min(2, d * 0.4)); e.gain.setValueAtTime(g, t + d - 0.8); e.gain.linearRampToValueAtTime(0, t + d + 0.8);
        o.connect(lp); lp.connect(e); e.connect(out); o.start(t); o.stop(t + d + 0.9);
      }));
    },
    // a soft synth pluck with an echo (the same note again, quieter, a dotted beat later)
    echoPluck(t, m, d, g, out, s = 0.6) {
      [[0, 1], [0.75, 0.4], [1.5, 0.16]].forEach(([dt, k]) => {
        const at = t + dt * s, o = ctx.createOscillator(), lp = ctx.createBiquadFilter(), e = ctx.createGain();
        o.type = 'triangle'; o.frequency.value = mtof(m); lp.type = 'lowpass'; lp.frequency.value = 1700 - dt * 500;
        env(e, at, g * k, 0.004, 0.45); o.connect(lp); lp.connect(e); e.connect(out); o.start(at); o.stop(at + 0.55);
      });
    },
    // a soft sci-fi lead: a gentle saw through a low filter, with slow vibrato
    synthLead(t, m, d, g, out) {
      const o = ctx.createOscillator(), v = ctx.createOscillator(), vg = ctx.createGain(), lp = ctx.createBiquadFilter(), e = ctx.createGain(); d = Math.max(0.3, d);
      o.type = 'sawtooth'; o.frequency.value = mtof(m); v.frequency.value = 4.5; vg.gain.value = mtof(m) * 0.006; v.connect(vg); vg.connect(o.frequency);
      lp.type = 'lowpass'; lp.frequency.value = 1100; lp.Q.value = 1;
      e.gain.setValueAtTime(0, t); e.gain.linearRampToValueAtTime(g, t + 0.25); e.gain.setValueAtTime(g, t + d * 0.75); e.gain.linearRampToValueAtTime(0, t + d + 0.3);
      o.connect(lp); lp.connect(e); e.connect(out); o.start(t); v.start(t); o.stop(t + d + 0.4); v.stop(t + d + 0.4);
    },
    // moving air: a slow swell of filtered noise, like the ship's air plant breathing in the morning
    air(t, d, g, out) {
      const src = ctx.createBufferSource(); src.buffer = WHITE; src.loop = true; const f = ctx.createBiquadFilter(), e = ctx.createGain();
      f.type = 'bandpass'; f.Q.value = 1.2; f.frequency.setValueAtTime(900, t); f.frequency.linearRampToValueAtTime(2600, t + d * 0.5); f.frequency.linearRampToValueAtTime(1200, t + d);
      e.gain.setValueAtTime(0, t); e.gain.linearRampToValueAtTime(g, t + d * 0.5); e.gain.linearRampToValueAtTime(0, t + d);
      src.connect(f); f.connect(e); e.connect(out); src.start(t, Math.random()); src.stop(t + d + 0.1);
    },
  });
  Object.assign(PARTS, {
    synthPad: c => MI.synthPad(c.t, c.ch, c.s * c.beats, 0.0055, c.out, c.e >= 2 ? 1 : 0.6),
    synthPadHi: c => MI.synthPad(c.t, c.ch.map(m => m + 12), c.s * c.beats, 0.004, c.out, 0.8),
    echoArp: c => { const up = c.ch.map(m => m + 12), seq = [up[0], up[2], up[1], up[3] ?? up[0] + 12]; for (let k = 0; k < c.beats; k++) MI.echoPluck(c.t + k * c.s, seq[(k + c.bar) % seq.length], 0, 0.022, c.out, c.s); },
    echoArp8: c => { const up = c.ch.map(m => m + 12), seq = [...up, up[1] + 12]; for (let k = 0; k < c.beats * 2; k++) MI.echoPluck(c.t + k * c.s / 2, seq[k % seq.length], 0, k % 2 ? 0.012 : 0.018, c.out, c.s); },
    pulse8: c => { for (let k = 0; k < c.beats * 2; k++) tone(c.t + k * c.s / 2, mtof(c.root + 12), c.s * 0.4, { gain: k % 2 ? 0.02 : 0.03, type: 'triangle', lp: 500, a: 0.01, bus: c.out }); },
    heart: c => { MI.bass(c.t, c.root, c.s * 1.2, 0.06, c.out); if (c.beats === 4) MI.bass(c.t + 2 * c.s, c.root, c.s * 1.2, 0.04, c.out); },
    air: c => MI.air(c.t, c.s * c.beats, 0.012, c.out),
  });
  Object.assign(TRACKS, {
    wake: { name: 'Wake cycle', time: 'Morning', full: true, bpm: 72, beats: 4, swing: 0, wet: 0.5, seed: 211, scale: PENTA(2), range: [74, 90], lg: 0.022, lead: 'synthLead',
      note: 'Slow, wide synth pads that open up like a dimmer coming on, a soft echoing arpeggio and a gentle heartbeat bass. The ship waking up.',
      prog: { A: CH([[50, 57, 62, 64, 38], [47, 54, 57, 62, 35], [43, 50, 55, 59, 31], [45, 52, 57, 61, 33]]), B: CH([[52, 57, 59, 64, 40], [43, 50, 54, 59, 31], [50, 54, 57, 62, 38], [45, 49, 52, 57, 33]]), C: CH([[47, 50, 54, 57, 35], [43, 47, 50, 55, 31], [52, 55, 59, 62, 40], [45, 50, 52, 57, 33]]) },
      form: () => longForm([sec('Intro', 'A', 4, ['synthPad', 'air'], 1)],
        [sec('Pads', 'A', 8, ['synthPad', 'air', 'heart'], 1), sec('Arpeggio', 'A', 8, ['synthPad', 'echoArp', 'heart'], 2), sec('B', 'B', 8, ['synthPad', 'echoArp', 'heart', 'mel'], 2, '*'),
         sec('Open', 'B', 8, ['synthPad', 'synthPadHi', 'echoArp8', 'heart', 'mel'], 3, '*'), sec('Bridge', 'C', 8, ['synthPad', 'air', 'bells'], 1)],
        [sec('Outro', 'A', 4, ['synthPad', 'air'], 1)], 72, 4, 10, ['synthLead', 'glass', 'synthLead', 'box']) },
    systems: { name: 'Systems online', time: 'Morning', full: true, bpm: 84, beats: 4, swing: 0, wet: 0.4, seed: 223, scale: PENTA(9), range: [76, 88], lg: 0.02, lead: 'echoPluck',
      note: 'A soft pulse ticking under the pads and a rising arpeggio, as the ship\'s systems come online one by one. The most motion of the three, but still calm.',
      prog: { A: CH([[57, 60, 64, 67, 45], [53, 57, 60, 64, 41], [48, 52, 55, 59, 36], [55, 59, 62, 64, 43]]), B: CH([[50, 53, 57, 60, 38], [53, 57, 60, 64, 41], [57, 60, 64, 67, 45], [52, 55, 59, 64, 40]]), C: CH([[48, 52, 55, 59, 36], [53, 57, 60, 62, 41], [50, 53, 57, 60, 38], [52, 56, 59, 62, 40]]) },
      form: () => longForm([sec('Intro', 'A', 4, ['synthPad', 'pulse8'], 1)],
        [sec('Pulse', 'A', 8, ['synthPad', 'pulse8', 'heart'], 2), sec('Arpeggio', 'A', 8, ['synthPad', 'pulse8', 'echoArp8'], 2), sec('B', 'B', 8, ['synthPad', 'pulse8', 'echoArp8', 'mel'], 3, '*'),
         sec('Bridge', 'C', 8, ['synthPadHi', 'air', 'bells'], 1), sec('A again', 'A', 8, ['synthPad', 'pulse8', 'echoArp', 'mel'], 2, '*')],
        [sec('Outro', 'A', 4, ['synthPad'], 1)], 84, 4, 10, ['echoPluck', 'synthLead', 'glass']) },
    dawn: { name: 'Station dawn', time: 'Early morning', full: true, bpm: 60, beats: 4, swing: 0, wet: 0.6, seed: 227, scale: PENTA(4), range: [76, 92], lg: 0.022, lead: 'glass',
      note: 'The most ambient: long pad swells, slow moving air and a few glassy bells, with a faint pulse arriving later. Before anyone else is up.',
      prog: { A: CH([[52, 59, 63, 66, 40], [49, 56, 59, 64, 37], [45, 52, 56, 59, 33], [47, 54, 59, 61, 35]]), B: CH([[44, 51, 56, 59, 32], [45, 52, 57, 61, 33], [52, 56, 59, 64, 40], [47, 51, 54, 59, 35]]), C: CH([[49, 52, 56, 59, 37], [45, 49, 52, 57, 33], [47, 50, 54, 59, 35], [52, 54, 59, 63, 40]]) },
      form: () => longForm([sec('Intro', 'A', 4, ['synthPad', 'air'], 1)],
        [sec('Swells', 'A', 8, ['synthPad', 'air'], 1), sec('Bells', 'A', 8, ['synthPad', 'air', 'bells'], 1), sec('B', 'B', 8, ['synthPad', 'synthPadHi', 'mel'], 1, '*'),
         sec('Pulse', 'B', 8, ['synthPad', 'echoArp', 'heart', 'mel'], 2, '*'), sec('Bridge', 'C', 8, ['synthPadHi', 'air'], 1)],
        [sec('Outro', 'A', 4, ['synthPad', 'air'], 1)], 60, 4, 10, ['glass', 'synthLead', 'echoPluck']) },
  });
