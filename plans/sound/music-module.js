/* =====================================================================
   WREN MUSIC: the ship's music by time of day (sound designer SD1, 2026-10-25)
   Approved by the user on 2026-10-25. Ready to paste into the game's sound
   block (SND) or load as is. NOT in starship-cadet.html yet.

   Everything is made live with Web Audio, with no files. 14 tracks of about
   ten minutes each. Each one is built from sections (intro, tune, fuller
   part, a B part, a quiet bridge, outro) with a new tune and lead instrument
   on every pass, so nothing loops audibly.

   Rules it keeps (CLAUDE.md, integration-plan.md):
   - Math.random only for the schedule; tunes come from each track's own
     seeded numbers. It never calls the game's R().
   - It draws nothing and changes nothing in the ship. It only reads the ship
     clock through the shipTime() you pass in.
   - It plays under the hum: at volume 1 every track's loudest moment is about
     4 to 6 dB under the Quarters hum.

   Use:
     const music = createWrenMusic({ ctx, dest, shipTime });
       ctx: an AudioContext (or OfflineAudioContext for tests)
       dest: where the music goes (the SND music bus, or ctx.destination)
       shipTime: () => ({ day, min: minutes since midnight 0-1439, onShift: bool })
     music.update()            call often (each frame, or every 100-250 ms)
     music.setEnabled(on)      Settings: Music on/off (off stops after a fade)
     music.setVolume(v)        Settings: 0..1 (Low 0.45, Medium 0.7, High 1)
     music.pause() / resume()  with the game's pause
     music.setMode(m)          'schedule' (the default: by time of day, work on
                               shift) or a track key to play that track
     music.next()              schedule: the next track from the set now;
                               chosen track: the next track in the list
     music.state()             what's playing, for the Music app or a check
     music.LIST                the tracks grouped for the Music app
   Rules from the user: music is on by default, in Ship schedule mode; there
   is no music on arrival night (Day 0). It starts on Day 1. Sound effects and
   the hum still play on Day 0; that is the SND block's business.
   Options: gapMin/gapMax (seconds of quiet between tracks, default 60-180),
   xfade (seconds, default 6), sectionWait (max seconds to wait for a section
   end before changing on a new time of day, default 30), random (default
   Math.random), onEvent(text) for a log, firstDay (default 1), mode, volume,
   enabled, heard (the saved choices and rotation from the sound key).
   ===================================================================== */
function createWrenMusic(opts) {
  const ctx = opts.ctx, rnd = opts.random || Math.random, log = opts.onEvent || (() => {});
  const cfg = { gapMin: 60, gapMax: 180, xfade: 6, sectionWait: 30, firstDay: 1, ...opts };
  // ---- the module's own small mixer: music bus -> volume -> dest, and a soft room echo
  const main = ctx.createGain(); main.gain.value = 0; main.connect(opts.dest);
  const sr = ctx.sampleRate;
  const WHITE = ctx.createBuffer(1, sr * 2, sr), wd = WHITE.getChannelData(0); for (let i = 0; i < wd.length; i++) wd[i] = Math.random() * 2 - 1;
  const BROWN = ctx.createBuffer(1, sr * 2, sr), bd = BROWN.getChannelData(0); let last = 0; for (let i = 0; i < bd.length; i++) { last = (last + 0.02 * (Math.random() * 2 - 1)) / 1.02; bd[i] = last * 3.5; }
  const ir = ctx.createBuffer(2, sr * 1.8, sr);
  for (let ch = 0; ch < 2; ch++) { const d = ir.getChannelData(ch); let lp = 0; for (let i = 0; i < d.length; i++) { const t = i / sr; lp = lp * 0.6 + (Math.random() * 2 - 1) * 0.4; d[i] = lp * Math.exp(-t * 3.2) * (t < 0.012 ? t / 0.012 : 1); } }
  const verb = ctx.createConvolver(); verb.buffer = ir; const verbOut = ctx.createGain(); verbOut.gain.value = 0.9; verb.connect(verbOut); verbOut.connect(main);
  const LEVEL = 0.55;   // the trim that puts volume 1 under the hum (measured in the Sound Lab)
  // ---- sound helpers (the same as the soundscape's)
  function conn(node, bus, pan, wet) { node.connect(bus); if (wet) { const s = ctx.createGain(); s.gain.value = wet; node.connect(s); s.connect(verb); } }
  function env(g, t, peak, a, d) { g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(peak, t + a); g.gain.exponentialRampToValueAtTime(0.0001, t + a + d); }
  function tone(t, f, d, o = {}) {
    const osc = ctx.createOscillator(), g = ctx.createGain(), a = o.a ?? 0.006;
    osc.type = o.type || 'sine'; osc.frequency.setValueAtTime(f, t);
    if (o.to) osc.frequency.exponentialRampToValueAtTime(o.to, t + (o.toT ?? d * 0.7));
    env(g, t, o.gain ?? 0.2, a, d);
    if (o.lp) { const f2 = ctx.createBiquadFilter(); f2.type = 'lowpass'; f2.frequency.value = o.lp; osc.connect(f2); f2.connect(g); } else osc.connect(g);
    conn(g, o.bus, 0, o.wet); osc.start(t); osc.stop(t + a + d + 0.05);
  }
  function noise(t, d, o = {}) {
    const src = ctx.createBufferSource(); src.buffer = o.brown ? BROWN : WHITE;
    const f = ctx.createBiquadFilter(); f.type = o.ft || 'bandpass'; f.frequency.setValueAtTime(o.f || 1000, t); f.Q.value = o.q ?? 1;
    const g = ctx.createGain(); env(g, t, o.gain ?? 0.1, o.a ?? 0.003, d);
    src.connect(f); f.connect(g); conn(g, o.bus, 0, o.wet); src.start(t, Math.random() * (src.buffer.duration - d - 0.2)); src.stop(t + d + 0.1);
  }
  function fmBell(t, f, d, gain, ratio, index, trem, b) {
    const car = ctx.createOscillator(), mod = ctx.createOscillator(), mg = ctx.createGain(), g = ctx.createGain();
    car.frequency.value = f; mod.frequency.value = f * ratio;
    mg.gain.setValueAtTime(f * index, t); mg.gain.exponentialRampToValueAtTime(f * 0.05, t + d * 0.5);
    mod.connect(mg); mg.connect(car.frequency); env(g, t, gain, 0.002, d); car.connect(g); conn(g, b, 0, 0.35);
    car.start(t); mod.start(t); car.stop(t + d + 0.1); mod.stop(t + d + 0.1);
  }
  const mtof = m => 440 * Math.pow(2, (m - 69) / 12);
  function seeded(a) { return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  const MI = {
    pad(t, notes, d, g, out, att = 0.8) {
      notes.forEach(m => [-6, 6].forEach(c => {
        const o = ctx.createOscillator(), lp = ctx.createBiquadFilter(), e = ctx.createGain();
        o.type = 'triangle'; o.frequency.value = mtof(m); o.detune.value = c; lp.type = 'lowpass'; lp.frequency.value = 900;
        e.gain.setValueAtTime(0, t); e.gain.linearRampToValueAtTime(g, t + att); e.gain.setValueAtTime(g, t + Math.max(att, d - 0.6)); e.gain.linearRampToValueAtTime(0, t + d + 0.4);
        o.connect(lp); lp.connect(e); e.connect(out); o.start(t); o.stop(t + d + 0.5);
      }));
    },
    keys(t, m, d, g, out) {   // electric piano
      const f = mtof(m), car = ctx.createOscillator(), mod = ctx.createOscillator(), mg = ctx.createGain(), e = ctx.createGain();
      car.frequency.value = f; mod.frequency.value = f; mg.gain.setValueAtTime(f * 1.1, t); mg.gain.exponentialRampToValueAtTime(f * 0.02, t + 0.4);
      mod.connect(mg); mg.connect(car.frequency); env(e, t, g, 0.006, d); car.connect(e); e.connect(out);
      car.start(t); mod.start(t); car.stop(t + d + 0.1); mod.stop(t + d + 0.1);
    },
    pluck(t, m, d, g, out) { const f = mtof(m); tone(t, f, 0.5, { gain: g, a: 0.003, bus: out }); tone(t, f * 4, 0.06, { gain: g * 0.15, a: 0.002, bus: out }); },
    box(t, m, d, g, out) { const f = mtof(m); tone(t, f, 1.1, { gain: g, a: 0.002, bus: out }); tone(t, f * 2, 0.4, { gain: g * 0.22, a: 0.002, bus: out }); tone(t, f * 5.4, 0.07, { gain: g * 0.08, a: 0.001, bus: out }); },
    glass(t, m, d, g, out) { fmBell(t, mtof(m), 2.6, g, 2, 0.6, 0, out); },
    flute(t, m, d, g, out) {
      const o = ctx.createOscillator(), v = ctx.createOscillator(), vg = ctx.createGain(), e = ctx.createGain(); d = Math.max(0.15, d);
      o.frequency.value = mtof(m); v.frequency.value = 5; vg.gain.value = mtof(m) * 0.004; v.connect(vg); vg.connect(o.frequency);
      e.gain.setValueAtTime(0, t); e.gain.linearRampToValueAtTime(g, t + 0.07); e.gain.setValueAtTime(g, t + d * 0.8); e.gain.linearRampToValueAtTime(0, t + d);
      o.connect(e); e.connect(out); o.start(t); v.start(t); o.stop(t + d + 0.05); v.stop(t + d + 0.05);
      noise(t, 0.08, { f: mtof(m) * 2, q: 2, gain: g * 0.3, a: 0.02, bus: out });
    },
    chip(t, m, d, g, out) {   // a soft, cute square lead, rounded off
      const o = ctx.createOscillator(), lp = ctx.createBiquadFilter(), e = ctx.createGain(); d = Math.max(0.12, d);
      o.type = 'square'; o.frequency.value = mtof(m); lp.type = 'lowpass'; lp.frequency.value = 1700;
      e.gain.setValueAtTime(0, t); e.gain.linearRampToValueAtTime(g, t + 0.012); e.gain.setValueAtTime(g * 0.8, t + d * 0.7); e.gain.linearRampToValueAtTime(0, t + d);
      o.connect(lp); lp.connect(e); e.connect(out); o.start(t); o.stop(t + d + 0.05);
    },
    bass(t, m, d, g, out) { tone(t, mtof(m), d, { gain: g, a: 0.02, bus: out }); tone(t, mtof(m + 12), d * 0.6, { gain: g * 0.3, type: 'triangle', lp: 600, a: 0.02, bus: out }); },
    kick(t, g, out) { tone(t, 95, 0.22, { gain: g, to: 45, toT: 0.1, a: 0.002, bus: out }); },
    snare(t, g, out) { noise(t, 0.16, { f: 1900, q: 0.6, gain: g, a: 0.003, bus: out }); noise(t, 0.05, { brown: true, ft: 'lowpass', f: 300, gain: g * 1.5, a: 0.002, bus: out }); },
    hat(t, g, out) { noise(t, 0.035, { f: 8000, q: 0.7, gain: g, a: 0.002, bus: out }); },
    shaker(t, g, out) { noise(t, 0.05, { f: 7000, q: 0.7, gain: g, a: 0.006, bus: out }); },
  };
  // a tune walking a scale: per bar, a few notes on the beat grid; returns [[beat, note, length], ...] for each bar
  function walkMelody(rng, bars, scale, lo, hi, grid, count, rests = []) {
    const pool = scale.filter(m => m >= lo && m <= hi); let k = (pool.length / 2) | 0;
    return Array.from({ length: bars }, (_, b) => {
      if (rests.includes(b % 4)) return [];
      const n = count[0] + ((rng() * (count[1] - count[0] + 1)) | 0);
      const pos = [...new Set(Array.from({ length: n }, () => grid[(rng() * grid.length) | 0]))].sort((x, y) => x - y);
      return pos.map((p, i) => { k = Math.max(0, Math.min(pool.length - 1, k + [-2, -1, -1, 1, 1, 2][(rng() * 6) | 0])); return [p, pool[k], ((pos[i + 1] ?? grid[grid.length - 1] + 1) - p)]; });
    });
  }
  const PENTA = r => [0, 2, 4, 7, 9].flatMap(d => [36, 48, 60, 72, 84, 96].map(o => o + r + d)).sort((a, b) => a - b);
  // The parts. c: { t, s (seconds a beat), beats, ch (chord notes), root, out, rng, e (how busy, 1-3), sw (swing, seconds), mel (this bar's tune), lead, lg }
  const PARTS = {
    pad: c => MI.pad(c.t, c.ch.map(m => m + 12), c.s * c.beats, 0.011, c.out),
    padLow: c => MI.pad(c.t, c.ch, c.s * c.beats, 0.011, c.out, 1.6),
    keys: c => { c.ch.forEach(m => MI.keys(c.t, m, c.s * (c.beats - 0.4), 0.017, c.out)); if (c.beats === 4) c.ch.slice(-2).forEach(m => MI.keys(c.t + c.s * 2.5 + c.sw, m, c.s * 1.4, 0.01, c.out)); },
    keysLofi: c => { (c.beats === 4 ? [0, 1.5, 2.5] : [0, 1, 2]).forEach((b, i) => c.ch.slice(i ? 1 : 0).forEach(m => MI.keys(c.t + b * c.s + (b % 1 ? c.sw : 0), m, c.s * (i ? 0.8 : 1.3), i ? 0.011 : 0.016, c.out))); },
    waltz: c => { MI.bass(c.t, c.root, c.s * 0.9, 0.07, c.out); [1, 2].forEach(b => c.ch.forEach(m => MI.keys(c.t + b * c.s, m, c.s * 0.6, 0.011, c.out))); },
    bass: c => { const long = c.e < 2 || c.beats === 3; MI.bass(c.t, c.root, c.s * (long ? c.beats - 0.3 : 1.8), 0.075, c.out); if (!long) MI.bass(c.t + 2 * c.s + c.sw * 0, c.root + (c.bar % 2 ? 7 : 12), c.s * 1.6, 0.05, c.out); },
    arp: c => { const up = c.ch.map(m => m + 12), seq = [...up, up[2], up[1]]; for (let k = 0; k < c.beats * 2; k++) MI.pluck(c.t + k * c.s / 2 + (k % 2 ? c.sw : 0), seq[k % seq.length], 0, k % 2 ? 0.026 : 0.036, c.out); },
    boxArp: c => { const up = c.ch.map(m => m + 24); for (let k = 0; k < c.beats; k++) MI.box(c.t + k * c.s, up[k % up.length], 0, 0.026, c.out); },
    pulse: c => { for (let k = 0; k < c.beats * 2; k++) MI.pluck(c.t + k * c.s / 2, c.ch[k % 2 ? 2 : 1] + 12, 0, 0.018, c.out); },
    bells: c => { const n = 1 + ((c.rng() * 2) | 0); for (let k = 0; k < n; k++) MI.glass(c.t + ((c.rng() * c.beats * 2) | 0) * c.s / 2, c.ch[(c.rng() * c.ch.length) | 0] + 24, 0, 0.022, c.out); },
    mel: c => c.mel.forEach(([b, m, d]) => MI[c.lead](c.t + b * c.s + (b % 1 ? c.sw : 0), m, Math.min(d, 2) * c.s * 0.9, c.lg, c.out)),
    drums: c => {   // soft lo-fi kit; quieter when the section is calm
      const v = c.e >= 3 ? 1 : c.e === 2 ? 0.75 : 0.45, sw = c.sw;
      if (c.beats === 4) {
        MI.kick(c.t, 0.11 * v, c.out); MI.kick(c.t + 2.5 * c.s + sw, 0.07 * v, c.out);
        if (c.e >= 2) { MI.snare(c.t + c.s, 0.035 * v, c.out); MI.snare(c.t + 3 * c.s, 0.035 * v, c.out); }
        for (let k = 0; k < 8; k++) MI.hat(c.t + k * c.s / 2 + (k % 2 ? sw : 0), (k % 2 ? 0.012 : 0.02) * v, c.out);
      } else { MI.kick(c.t, 0.09 * v, c.out); [1, 2].forEach(b => MI.hat(c.t + b * c.s, 0.014 * v, c.out)); }
    },
    brushes: c => { for (let k = 0; k < c.beats * 2; k++) MI.shaker(c.t + k * c.s / 2 + (k % 2 ? c.sw : 0), k % 2 ? 0.014 : 0.008, c.out); },
    shaker: c => { for (let k = 0; k < c.beats * 2; k++) MI.shaker(c.t + k * c.s / 2 + (k % 2 ? c.sw : 0), k % 2 ? 0.025 : 0.013, c.out); },
  };
  // sec(label, chords key, bars, parts, how busy, lead instrument)
  const sec = (label, prog, bars, parts, e = 2, lead) => ({ label, prog, bars, parts, e, lead });
  // A long track: an intro, then the cycle of sections again and again (a new tune and lead each pass) until about ten minutes, then an outro.
  function longForm(intro, cycle, outro, bpm, beats, minutes, leads) {
    const barSec = 60 / bpm * beats, target = minutes * 60 / barSec, out = [...intro], tail = outro.reduce((a, x) => a + x.bars, 0);
    let n = intro.reduce((a, x) => a + x.bars, 0), k = 0;
    while (n + tail < target - 4) {   // section by section, so it ends close to the target
      const pass = Math.floor(k / cycle.length), x = cycle[k % cycle.length];
      out.push({ ...x, pass, lead: x.lead === '*' ? leads[pass % leads.length] : x.lead }); n += x.bars; k++;
    }
    return [...out, ...outro];
  }
  const CH = s => s.map(c => ({ notes: c.slice(0, -1), root: c[c.length - 1] }));
  const TRACKS = {
    // ---- full tracks, about ten minutes, by time of day
    morning: { name: 'Morning', time: 'Morning', full: true, bpm: 92, beats: 4, swing: 0, wet: 0.25, seed: 23, scale: PENTA(7), range: [74, 88], lg: 0.032,
      note: 'Bright marimba patterns, a whistled flute and a light shaker. It builds through the morning and drops back to a quiet bridge now and then.',
      prog: { A: CH([[55, 59, 62, 67, 43], [54, 57, 62, 66, 42], [52, 55, 59, 64, 40], [48, 55, 60, 64, 36]]), B: CH([[57, 60, 64, 67, 45], [54, 57, 62, 66, 38], [55, 59, 62, 67, 43], [52, 55, 59, 62, 40]]), C: CH([[48, 52, 55, 59, 36], [47, 50, 54, 57, 35], [45, 48, 52, 55, 33], [50, 54, 57, 62, 38]]) },
      form: () => longForm([sec('Intro', 'A', 4, ['pad', 'arp'], 1)],
        [sec('A', 'A', 8, ['pad', 'arp', 'bass', 'shaker'], 2), sec('A with tune', 'A', 8, ['arp', 'bass', 'shaker', 'mel'], 3, '*'), sec('B', 'B', 8, ['keys', 'bass', 'mel', 'shaker'], 2, 'pluck'),
         sec('B, full', 'B', 8, ['keys', 'arp', 'bass', 'mel', 'shaker'], 3, '*'), sec('Bridge', 'C', 8, ['pad', 'bells'], 1), sec('A again', 'A', 8, ['pad', 'arp', 'bass', 'mel', 'shaker'], 3, 'flute')],
        [sec('Outro', 'A', 4, ['pad', 'arp'], 1)], 92, 4, 10, ['flute', 'pluck', 'chip', 'box']) },
    evening: { name: 'Evening', time: 'Evening', full: true, bpm: 66, beats: 4, swing: 0.06, wet: 0.35, seed: 11, scale: PENTA(0), range: [72, 86], lg: 0.04,
      note: 'Slow electric piano, a soft pad and plucked notes, with soft brushes later on. Winding down after the shift.',
      prog: { A: CH([[53, 57, 60, 64, 41], [52, 55, 59, 62, 40], [50, 53, 57, 60, 38], [48, 52, 55, 59, 36]]), B: CH([[46, 50, 53, 57, 34], [45, 48, 52, 55, 33], [43, 46, 50, 53, 31], [48, 52, 55, 60, 36]]), C: CH([[50, 53, 57, 60, 64, 38], [46, 50, 53, 57, 34], [53, 57, 60, 64, 41], [48, 52, 55, 57, 36]]) },
      form: () => longForm([sec('Intro', 'A', 4, ['pad'], 1)],
        [sec('A', 'A', 8, ['keys', 'pad', 'bass'], 1), sec('A with tune', 'A', 8, ['keys', 'bass', 'mel'], 2, '*'), sec('B', 'B', 8, ['keys', 'bass', 'mel', 'brushes'], 2, 'pluck'),
         sec('Bridge', 'C', 8, ['pad', 'bells', 'bass'], 1), sec('B, lo-fi', 'B', 8, ['keysLofi', 'bass', 'drums', 'mel'], 2, '*')],
        [sec('Outro', 'A', 4, ['keys', 'pad'], 1)], 66, 4, 10, ['pluck', 'glass', 'box', 'flute']) },
    latenight: { name: 'Late night', time: 'Late night', full: true, bpm: 56, beats: 4, swing: 0, wet: 0.55, seed: 37, scale: PENTA(2), range: [78, 93], lg: 0.026,
      note: 'Long, slow pad swells and glassy bells, no beat at all. For the quiet hours, stargazing and the night watch.',
      prog: { A: CH([[50, 57, 61, 64, 66, 38], [47, 54, 57, 61, 62, 35], [43, 50, 54, 59, 61, 31], [45, 52, 57, 59, 62, 33]]), B: CH([[52, 55, 59, 62, 66, 40], [43, 50, 54, 59, 31], [50, 54, 57, 61, 38], [45, 52, 57, 61, 33]]), C: CH([[47, 50, 54, 57, 35], [43, 47, 50, 54, 57, 31], [52, 55, 59, 62, 40], [45, 50, 52, 57, 33]]) },
      form: () => longForm([sec('Intro', 'A', 4, ['padLow'], 1)],
        [sec('A', 'A', 8, ['padLow', 'bass'], 1), sec('A with bells', 'A', 8, ['padLow', 'bass', 'bells'], 1), sec('B', 'B', 8, ['padLow', 'mel'], 1, '*'),
         sec('C, music box', 'C', 8, ['padLow', 'boxArp', 'bass'], 1), sec('B again', 'B', 8, ['padLow', 'bass', 'mel'], 1, 'glass')],
        [sec('Outro', 'A', 4, ['padLow'], 1)], 56, 4, 10, ['glass', 'box', 'flute']) },

    // ---- samples, 30 to 90 seconds
    shift: { name: 'Shift start', time: 'Work', bpm: 100, beats: 4, swing: 0.05, wet: 0.2, seed: 101, scale: PENTA(0), range: [72, 86], lg: 0.022, lead: 'chip',
      note: 'A cheerful little beat with a cute square-wave tune. Clocking on.',
      prog: { A: CH([[48, 52, 55, 60, 36], [45, 48, 52, 57, 33], [53, 57, 60, 65, 41], [55, 59, 62, 67, 43]]) },
      form: () => [sec('Beat', 'A', 4, ['keysLofi', 'bass', 'drums'], 2), sec('Tune', 'A', 8, ['keysLofi', 'bass', 'drums', 'mel'], 3), sec('Tune and arp', 'A', 4, ['arp', 'bass', 'drums', 'mel'], 3)] },
    steady: { name: 'Steady work', time: 'Work', bpm: 88, beats: 4, swing: 0.12, wet: 0.25, seed: 113, scale: PENTA(5), range: [72, 86], lg: 0.04, lead: 'pluck', vinyl: true,
      note: 'Chill lo-fi: swung electric piano, a soft kit, plucked notes and a little vinyl crackle. For heads-down jobs.',
      prog: { A: CH([[53, 57, 60, 64, 41], [55, 59, 62, 64, 43], [52, 55, 59, 62, 40], [57, 60, 64, 67, 45]]) },
      form: () => [sec('Beat', 'A', 4, ['keysLofi', 'drums', 'bass'], 2), sec('Tune', 'A', 8, ['keysLofi', 'drums', 'bass', 'mel'], 2), sec('Music box', 'A', 8, ['keysLofi', 'drums', 'bass', 'pad', 'mel'], 2, 'box')] },
    rounds: { name: 'On your rounds', time: 'Work', bpm: 112, beats: 4, swing: 0, wet: 0.2, seed: 127, scale: PENTA(2), range: [74, 90], lg: 0.032, lead: 'flute',
      note: 'Bouncy marimba and shaker with a soft kick. Walking the ship with your job list.',
      prog: { A: CH([[50, 54, 57, 62, 38], [55, 59, 62, 67, 43], [47, 50, 54, 59, 35], [45, 49, 52, 57, 33]]) },
      form: () => [sec('Marimba', 'A', 4, ['arp', 'bass', 'shaker'], 2), sec('Flute', 'A', 8, ['arp', 'bass', 'drums', 'mel'], 3), sec('Cute lead', 'A', 8, ['arp', 'bass', 'drums', 'mel'], 3, 'chip')] },
    firstlight: { name: 'First light', time: 'Early morning', bpm: 70, beats: 4, swing: 0, wet: 0.45, seed: 131, scale: PENTA(9), range: [76, 90], lg: 0.03, lead: 'box',
      note: 'A music box and soft pad, waking up slowly before the day starts.',
      prog: { A: CH([[57, 59, 61, 64, 45], [56, 59, 64, 44], [54, 57, 61, 64, 42], [50, 54, 57, 61, 38]]) },
      form: () => [sec('Waking', 'A', 4, ['pad', 'boxArp'], 1), sec('Tune', 'A', 8, ['pad', 'boxArp', 'bass', 'mel'], 1)] },
    midday: { name: 'Midday', time: 'Midday', bpm: 96, beats: 4, swing: 0.05, wet: 0.2, seed: 137, scale: PENTA(10), range: [72, 86], lg: 0.022, lead: 'chip',
      note: 'Happy and bright: lo-fi keys and beat with a cute lead. The busy middle of the day.',
      prog: { A: CH([[46, 50, 53, 58, 34], [55, 58, 62, 65, 43], [51, 55, 58, 63, 39], [53, 57, 60, 65, 41]]) },
      form: () => [sec('Beat', 'A', 4, ['keysLofi', 'bass', 'drums'], 2), sec('Tune', 'A', 8, ['keysLofi', 'bass', 'drums', 'mel'], 3), sec('Tune and arp', 'A', 8, ['arp', 'keysLofi', 'bass', 'drums', 'mel'], 3)] },
    lunch: { name: 'Lunch break', time: 'Midday', bpm: 84, beats: 4, swing: 0.15, wet: 0.25, seed: 139, scale: PENTA(0), range: [72, 86], lg: 0.04, lead: 'pluck', vinyl: true,
      note: 'Swung, jazzy lo-fi with a little crackle. Feet up for half an hour.',
      prog: { A: CH([[48, 52, 55, 59, 36], [45, 48, 52, 55, 33], [50, 53, 57, 60, 38], [43, 47, 50, 53, 31]]) },
      form: () => [sec('Beat', 'A', 4, ['keysLofi', 'drums', 'bass'], 2), sec('Tune', 'A', 12, ['keysLofi', 'drums', 'bass', 'mel'], 2)] },
    afternoon: { name: 'Afternoon', time: 'Afternoon', bpm: 80, beats: 4, swing: 0.12, wet: 0.3, seed: 149, scale: PENTA(3), range: [75, 89], lg: 0.022, lead: 'glass', vinyl: true,
      note: 'Lazy lo-fi with glassy bells on top. The long, easy stretch of the afternoon shift.',
      prog: { A: CH([[51, 55, 58, 62, 39], [48, 51, 55, 58, 36], [56, 60, 63, 67, 44], [46, 50, 53, 55, 34]]) },
      form: () => [sec('Beat', 'A', 4, ['keysLofi', 'drums', 'bass'], 2), sec('Bells', 'A', 12, ['keysLofi', 'drums', 'bass', 'mel'], 2)] },
    tea: { name: 'Tea break', time: 'Afternoon', bpm: 76, beats: 4, swing: 0.08, wet: 0.3, seed: 151, scale: PENTA(7), range: [74, 88], lg: 0.03, lead: 'flute',
      note: 'A music box, soft brushes and a flute. Tea and a biscuit by the Works kettle.',
      prog: { A: CH([[55, 59, 62, 66, 43], [48, 52, 55, 59, 36], [57, 60, 64, 67, 45], [50, 54, 57, 62, 38]]) },
      form: () => [sec('Music box', 'A', 4, ['boxArp', 'bass', 'brushes'], 1), sec('Flute', 'A', 12, ['boxArp', 'bass', 'brushes', 'mel'], 2)] },
    golden: { name: 'Golden hour', time: 'Evening', bpm: 72, beats: 4, swing: 0.1, wet: 0.3, seed: 157, scale: PENTA(4), range: [76, 88], lg: 0.04, lead: 'pluck', vinyl: true,
      note: 'Warm lo-fi electric piano and a soft beat, as the lights go amber.',
      prog: { A: CH([[52, 56, 59, 63, 40], [49, 52, 56, 59, 37], [57, 61, 64, 68, 45], [47, 51, 54, 56, 35]]) },
      form: () => [sec('Keys', 'A', 4, ['keysLofi', 'bass', 'pad'], 1), sec('Beat and tune', 'A', 12, ['keysLofi', 'bass', 'drums', 'mel'], 2)] },
    watch: { name: 'Night watch', time: 'Night', bpm: 60, beats: 4, swing: 0, wet: 0.5, seed: 163, scale: PENTA(0), range: [76, 91], lg: 0.024, lead: 'glass',
      note: 'A soft pulse under a pad and a few bells. Quietly keeping watch.',
      prog: { A: CH([[53, 57, 60, 64, 41], [48, 52, 55, 60, 36], [55, 59, 62, 64, 43], [57, 60, 64, 67, 45]]) },
      form: () => [sec('Pulse', 'A', 4, ['pad', 'pulse', 'bass'], 1), sec('Bells', 'A', 8, ['pad', 'pulse', 'bass', 'mel'], 1)] },
    lullaby: { name: 'Lights out', time: 'Night', bpm: 52, beats: 3, swing: 0, wet: 0.45, seed: 167, scale: PENTA(0), range: [72, 86], lg: 0.03, lead: 'box',
      note: 'A slow music-box lullaby in three. Lights out in the bunk room.',
      prog: { A: CH([[60, 64, 67, 48], [60, 65, 69, 41], [59, 62, 65, 67, 43], [60, 64, 67, 48]]) },
      form: () => [sec('Lullaby', 'A', 8, ['pad', 'bass', 'mel'], 1), sec('Again', 'A', 8, ['pad', 'bass', 'boxArp', 'mel'], 1)] },
  };
  // Lay the bars out once: each bar knows its section, chord, parts and tune. Tunes come in 4-bar phrases; the second half of
  // an 8-bar section repeats the phrase with its last bar changed.
  function layout(def) {
    const form = def.form(), bars = []; const grid = def.beats === 4 ? [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5] : [0, 1, 2];
    form.forEach((x, si) => {
      const rng = seeded(def.seed * 97 + si * 13 + (x.pass || 0) * 7), prog = def.prog[x.prog];
      const phrase = walkMelody(rng, 4, def.scale, def.range[0], def.range[1], grid, def.beats === 4 ? [2, 4] : [1, 3], [3]);
      const alt = walkMelody(rng, 4, def.scale, def.range[0], def.range[1], grid, def.beats === 4 ? [2, 4] : [1, 3], [3]);
      for (let b = 0; b < x.bars; b++) {
        const ph = b >= 4 && b % 4 === 2 ? alt[2] : phrase[b % 4];
        bars.push({ sec: x, si, b, chord: prog[b % prog.length], mel: ph });
      }
    });
    return bars;
  }
  // ---- ambient sci-fi synth (morning take 2, 2026-10-25): Systems online picked for mornings; Wake cycle and Station dawn for early morning
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
  // ---- four more tracks (2026-10-25) so every time of day has several to rotate through
  Object.assign(TRACKS, {
    promenade: { name: 'Promenade', time: 'Midday', full: true, bpm: 98, beats: 4, swing: 0.06, wet: 0.22, seed: 233, scale: PENTA(2), range: [74, 88], lg: 0.022, lead: 'chip', vinyl: true,
      note: 'Happy, bouncy lo-fi with a cute lead and little bells. A sunny walk down the promenade at lunchtime.',
      prog: { A: CH([[50, 54, 57, 61, 38], [47, 50, 54, 57, 35], [55, 59, 62, 66, 43], [45, 49, 52, 54, 33]]), B: CH([[55, 59, 62, 66, 43], [57, 61, 64, 67, 45], [54, 57, 61, 64, 42], [47, 50, 54, 59, 35]]), C: CH([[43, 47, 50, 54, 31], [45, 49, 52, 57, 33], [47, 50, 54, 57, 35], [45, 49, 52, 55, 33]]) },
      form: () => longForm([sec('Intro', 'A', 4, ['keysLofi', 'pad'], 1)],
        [sec('Beat', 'A', 8, ['keysLofi', 'drums', 'bass'], 2), sec('Tune', 'A', 8, ['keysLofi', 'drums', 'bass', 'mel'], 3, '*'), sec('B', 'B', 8, ['keys', 'arp', 'bass', 'drums', 'mel'], 3, 'box'),
         sec('Bridge', 'C', 8, ['pad', 'bells', 'bass'], 1), sec('A again', 'A', 8, ['keysLofi', 'drums', 'bass', 'mel'], 2, '*')],
        [sec('Outro', 'A', 4, ['keysLofi', 'pad'], 1)], 98, 4, 10, ['chip', 'box', 'pluck']) },
    circuits: { name: 'Warm circuits', time: 'Afternoon', full: true, bpm: 78, beats: 4, swing: 0.1, wet: 0.35, seed: 239, scale: PENTA(0), range: [74, 88], lg: 0.02, lead: 'synthLead', vinyl: true,
      note: 'Chill lo-fi keys and a soft beat with a gentle synth echo on top. A long, easy afternoon at the bench.',
      prog: { A: CH([[48, 52, 55, 59, 62, 36], [45, 48, 52, 55, 59, 33], [53, 57, 60, 64, 41], [55, 59, 62, 65, 43]]), B: CH([[52, 55, 59, 62, 40], [57, 60, 64, 67, 45], [50, 53, 57, 60, 38], [55, 59, 62, 64, 43]]), C: CH([[53, 57, 60, 64, 41], [52, 55, 59, 62, 40], [50, 53, 57, 62, 38], [43, 47, 50, 55, 31]]) },
      form: () => longForm([sec('Intro', 'A', 4, ['keysLofi', 'air'], 1)],
        [sec('Beat', 'A', 8, ['keysLofi', 'drums', 'bass'], 2), sec('Echoes', 'A', 8, ['keysLofi', 'drums', 'bass', 'echoArp'], 2), sec('B', 'B', 8, ['keysLofi', 'drums', 'bass', 'mel'], 2, '*'),
         sec('Bridge', 'C', 8, ['synthPad', 'bells', 'bass'], 1), sec('A again', 'A', 8, ['keysLofi', 'drums', 'bass', 'echoArp', 'mel'], 2, '*')],
        [sec('Outro', 'A', 4, ['keysLofi'], 1)], 78, 4, 10, ['synthLead', 'pluck', 'glass']) },
    porthole: { name: 'Porthole', time: 'Evening', full: true, bpm: 70, beats: 4, swing: 0.1, wet: 0.35, seed: 241, scale: PENTA(8), range: [75, 88], lg: 0.036, lead: 'pluck', vinyl: true,
      note: 'Warm electric piano and a soft brushed beat, watching the stars go by through a porthole after dinner.',
      prog: { A: CH([[56, 60, 63, 67, 44], [53, 56, 60, 63, 41], [49, 53, 56, 60, 37], [51, 55, 58, 60, 39]]), B: CH([[49, 53, 56, 60, 37], [51, 55, 58, 62, 39], [48, 51, 55, 58, 36], [53, 56, 60, 63, 41]]), C: CH([[46, 49, 53, 56, 34], [51, 55, 58, 61, 39], [44, 48, 51, 55, 32], [49, 53, 56, 58, 37]]) },
      form: () => longForm([sec('Intro', 'A', 4, ['keys', 'pad'], 1)],
        [sec('Keys', 'A', 8, ['keys', 'bass', 'brushes'], 1), sec('Tune', 'A', 8, ['keysLofi', 'bass', 'drums', 'mel'], 2, '*'), sec('B', 'B', 8, ['keysLofi', 'bass', 'drums', 'mel'], 2, '*'),
         sec('Bridge', 'C', 8, ['pad', 'bells', 'bass'], 1), sec('A again', 'A', 8, ['keys', 'bass', 'brushes', 'mel'], 2, 'glass')],
        [sec('Outro', 'A', 4, ['keys', 'pad'], 1)], 70, 4, 10, ['pluck', 'glass', 'box']) },
    deepspace: { name: 'Deep space', time: 'Late night', full: true, bpm: 52, beats: 4, swing: 0, wet: 0.6, seed: 251, scale: PENTA(9), range: [76, 91], lg: 0.022, lead: 'glass',
      note: 'Slow synth pads, drifting air and a few far-off bells, with a faint echo pattern later on. The ship gliding through the dark.',
      prog: { A: CH([[45, 52, 57, 59, 64, 33], [41, 48, 53, 57, 60, 29], [43, 50, 55, 59, 62, 31], [40, 47, 52, 55, 59, 28]]), B: CH([[38, 45, 50, 53, 57, 26], [41, 48, 52, 57, 29], [45, 52, 55, 60, 33], [43, 50, 55, 59, 31]]), C: CH([[41, 48, 53, 57, 29], [40, 47, 52, 56, 28], [45, 52, 57, 60, 33], [43, 47, 50, 55, 31]]) },
      form: () => longForm([sec('Intro', 'A', 4, ['synthPad', 'air'], 1)],
        [sec('Drift', 'A', 8, ['synthPad', 'air'], 1), sec('Bells', 'A', 8, ['synthPad', 'bells', 'bass'], 1), sec('B', 'B', 8, ['synthPad', 'synthPadHi', 'mel'], 1, '*'),
         sec('Echoes', 'C', 8, ['synthPad', 'echoArp', 'air'], 1), sec('B again', 'B', 8, ['synthPad', 'bass', 'mel'], 1, '*')],
        [sec('Outro', 'A', 4, ['synthPad', 'air'], 1)], 52, 4, 10, ['glass', 'synthLead', 'box']) },
  });
  // ---- every sample grows into a full ten-minute track: its own sections, a B part on the same chords moved round,
  // a quiet bridge, and its sections again with a new tune and lead each pass
  function grow(d) {
    const A = d.prog.A; d.prog.B = d.prog.B || [A[2], A[3], A[0], A[1]]; d.prog.C = d.prog.C || [A[3], A[1], A[2], A[0]];
    const base = d.form(), full = base[base.length - 1], soft = d.time === 'Night' || d.time === 'Early morning';
    const leads = [...new Set([d.lead, 'pluck', 'box', soft ? 'glass' : 'chip', 'flute'])].slice(0, 4);
    d.form = () => longForm([{ ...base[0], label: 'Intro', bars: 4 }],
      [...base.map(x => ({ ...x, lead: x.lead || '*' })), sec('B', 'B', 8, full.parts, full.e, '*'), sec('Bridge', 'C', 8, d.beats === 3 ? ['pad', 'bass'] : ['pad', 'bells', 'bass'], 1)],
      [sec('Outro', 'A', 4, ['pad'], 1)], d.bpm, d.beats, 10, leads);
  }
  for (const d of Object.values(TRACKS)) if (!d.full) { grow(d); d.full = true; }
  // levels per track (measured against the hum in the Sound Lab)
  const MLV = { wake: 1.65, systems: 1.75, dawn: 1.9, promenade: 1.19, circuits: 0.95, porthole: 0.85, deepspace: 1.75,  morning: 1.12, evening: 0.851, latenight: 0.661, shift: 1.047, steady: 1.12, rounds: 1.035, firstlight: 0.891, midday: 1.012, lunch: 1.12, afternoon: 1.12, tea: 0.923, golden: 1.023, watch: 0.785, lullaby: 0.841 };

  // ---- the schedule: ship time of day, and a working set while you're on shift
  const PERIODS = [   // [name, from minute]; each runs to the next one's start
    ['late night', 0 * 60 + 30], ['early morning', 5 * 60], ['morning', 7 * 60 + 30], ['midday', 11 * 60],
    ['afternoon', 14 * 60], ['evening', 17 * 60 + 30], ['night', 21 * 60],
  ];
  const SETS = {   // several tracks for each time of day (the user, 2026-10-25); the player rotates through them
    'early morning': ['dawn', 'wake', 'firstlight'],
    'morning': ['systems', 'morning', 'firstlight', 'tea'],
    'midday': ['midday', 'lunch', 'promenade'],
    'afternoon': ['afternoon', 'tea', 'circuits', 'golden'],
    'evening': ['evening', 'golden', 'porthole'],
    'night': ['watch', 'lullaby', 'porthole', 'evening'],
    'late night': ['latenight', 'deepspace', 'watch', 'dawn'],
    'working': ['shift', 'steady', 'rounds', 'circuits'],
  };
  // the Music app's list: every track, grouped by when it plays
  const TIMES = ['Work', 'Early morning', 'Morning', 'Midday', 'Afternoon', 'Evening', 'Night', 'Late night'];
  const LIST = TIMES.map(time => ({ time, tracks: Object.keys(TRACKS).filter(k => TRACKS[k].time === time).map(k => ({ key: k, name: TRACKS[k].name })) })).filter(g => g.tracks.length);
  const ORDER = LIST.flatMap(g => g.tracks.map(t => t.key));
  function periodAt(min) { let p = PERIODS[PERIODS.length - 1][0]; for (const [n, from] of PERIODS) if (min >= from) p = n; return p; }
  const setFor = st => st.onShift ? 'working' : periodAt(((st.min % 1440) + 1440) % 1440);

  // ---- one playing track
  function play(key, o = {}) {
    const def = TRACKS[key], bars = layout(def), s = 60 / def.bpm, len = s * def.beats, t0 = ctx.currentTime + 0.1;
    const out = ctx.createGain(), fin = o.fadeIn ?? cfg.xfade, lvl = MLV[key] ?? 1;
    out.gain.setValueAtTime(0, t0); out.gain.linearRampToValueAtTime(lvl, t0 + fin); out.connect(main);
    const send = ctx.createGain(); send.gain.value = def.wet; out.connect(send); send.connect(verb);
    const rng = seeded(def.seed), nodes = [];
    if (def.vinyl) { const v = ctx.createBufferSource(); v.buffer = WHITE; v.loop = true; const hp = ctx.createBiquadFilter(); hp.type = 'bandpass'; hp.frequency.value = 3000; hp.Q.value = 0.5; const vg = ctx.createGain(); vg.gain.value = 0.004; v.connect(hp); hp.connect(vg); vg.connect(out); v.start(t0); nodes.push(v); }
    let i = o.startBar || 0, next = t0, ending = null;
    const T = {
      key, def, out, len, total: bars.length * len, startAt: t0 - i * len, bars,
      tick(u) {   // schedule bars up to time u; the track plays once through, then ends
        while (next < u && i < bars.length && !ending) {
          const bar = bars[i], c = { t: next, s, beats: def.beats, ch: bar.chord.notes, root: bar.chord.root, out, rng, e: bar.sec.e, sw: def.swing * s, mel: bar.mel, lead: bar.sec.lead || def.lead || 'pluck', lg: def.lg, bar: bar.b };
          bar.sec.parts.forEach(p => PARTS[p](c));
          if (def.vinyl && rng() < 0.5) noise(next + rng() * len, 0.004, { f: 2500, q: 0.7, gain: 0.02, a: 0.001, bus: out });
          i++; next += len;
        }
      },
      endsAt() { return ending ?? (T.startAt + T.total); },
      sectionEnd() {   // when the current section ends (to change at a musical moment)
        const k = Math.max(0, Math.min(bars.length - 1, Math.floor((ctx.currentTime - T.startAt) / len))), si = bars[k].si;
        let j = k; while (j < bars.length && bars[j].si === si) j++; return T.startAt + j * len;
      },
      where() { const e = Math.max(0, ctx.currentTime - T.startAt), k = Math.min(bars.length - 1, Math.floor(e / len)); return { e, sec: bars[k].sec.label }; },
      fadeOut(at, f) {   // fade over f seconds starting at `at`, then stop
        if (ending) return; ending = at + f; out.gain.cancelScheduledValues(at); out.gain.setValueAtTime(lvl, at); out.gain.linearRampToValueAtTime(0, at + f);
        nodes.forEach(n => n.stop(at + f + 0.1)); setTimeout(() => { try { out.disconnect(); } catch (e) {} }, Math.max(0, (at + f - ctx.currentTime + 8) * 1000));
      },
    };
    T.tick(t0 + 0.4);
    // the natural end: fade the last few seconds of the outro
    const natural = T.startAt + T.total; out.gain.setValueAtTime(lvl, Math.max(t0 + fin, natural - 4)); out.gain.linearRampToValueAtTime(0, natural);
    return T;
  }

  // ---- the player
  let enabled = opts.enabled ?? true, volume = opts.volume ?? 0.7, paused = false, mode = opts.mode && TRACKS[opts.mode] ? opts.mode : 'schedule', resting = false;
  let cur = null, curSet = null, seenSet = null, nextAt = ctx.currentTime + (opts.firstGap ?? 3), lastKey = null, lastMin = null, pendingChange = null;
  const applyVol = (f = 1.5) => { const v = enabled && !paused ? LEVEL * volume : 0; main.gain.cancelScheduledValues(ctx.currentTime); main.gain.setValueAtTime(main.gain.value, ctx.currentTime); main.gain.linearRampToValueAtTime(v, ctx.currentTime + f); };
  applyVol(0.5);
  // rotation: never the one that just played, and of the rest, the one heard least recently (never heard comes first;
  // ties are broken at random). heard[key] counts up across the day and can be saved with the music settings.
  const heard = { ...(opts.heard || {}) }; let heardN = Math.max(0, ...Object.values(heard).filter(Number.isFinite));
  function pick(set) {
    if (set === 'chosen') return mode;
    const list = SETS[set].filter(k => k !== lastKey), best = Math.min(...list.map(k => heard[k] ?? -1));
    const pool = list.filter(k => (heard[k] ?? -1) === best); return pool[(rnd() * pool.length) | 0] || SETS[set][0];
  }
  function startNext(set, fadeIn) { const k = pick(set); cur = play(k, { fadeIn }); lastKey = k; heard[k] = ++heardN; curSet = set; log(`Playing ${TRACKS[k].name} (${set})`); }
  function update() {
    if (!enabled || paused) return;
    const now = ctx.currentTime, st = opts.shipTime();
    if ((st.day ?? cfg.firstDay) < cfg.firstDay) {   // arrival night: no music until Day 1 (the user's rule)
      if (!resting) { resting = true; log('Arrival night: no music until Day 1'); }
      if (cur) { cur.fadeOut(now, 3); cur = null; } pendingChange = null; nextAt = now + 2; lastMin = st.min; return;
    }
    if (resting) { resting = false; log('Day 1: music begins'); }
    const set = mode === 'schedule' ? setFor(st) : 'chosen';
    // a big jump in ship time (sleeping skips the night) changes over straight away
    const jumped = lastMin !== null && Math.abs(st.min - lastMin) > 30 && Math.abs(st.min - lastMin) < 1410; lastMin = st.min;
    if (set !== seenSet) { if (seenSet !== null && set !== 'chosen') log(`Time of day is now ${set}`); seenSet = set; }
    if (cur) {
      cur.tick(now + 0.5);
      if (set !== curSet) {   // time of day (or the shift) changed: cross-fade at the end of this section, or now after a jump
        if (!pendingChange) pendingChange = { at: jumped ? now : Math.min(cur.sectionEnd(), now + cfg.sectionWait) };
        else if (jumped) pendingChange.at = now;
      } else if (pendingChange) pendingChange = null;   // it changed back before we got there: carry on
      if (pendingChange && now >= pendingChange.at - 0.05) {
        cur.fadeOut(now, cfg.xfade); pendingChange = null; startNext(set, cfg.xfade);   // overlapping fades: a cross-fade, into what fits now
      } else if (now >= cur.endsAt()) {
        log(`${cur.def.name} ended; quiet for a while`); cur = null; nextAt = now + cfg.gapMin + rnd() * (cfg.gapMax - cfg.gapMin);
      }
    } else if (now >= nextAt) startNext(set, 4);
  }
  return {
    update,
    setEnabled(on) { enabled = !!on; if (!enabled && cur) { cur.fadeOut(ctx.currentTime, 2); cur = null; nextAt = ctx.currentTime + 3; } applyVol(); },
    setVolume(v) { volume = Math.max(0, Math.min(1, v)); applyVol(0.3); },
    pause() { paused = true; applyVol(0.3); },
    resume() { paused = false; applyVol(0.6); },
    setGaps(min, max) { cfg.gapMin = min; cfg.gapMax = Math.max(min, max); if (!cur) nextAt = Math.min(nextAt, ctx.currentTime + cfg.gapMax); },
    setMode(m) {   // 'schedule', or a track key to play that one; changes over with a short cross-fade
      const want = m === 'schedule' || !TRACKS[m] ? 'schedule' : m; if (want === mode) return; mode = want;
      log(mode === 'schedule' ? 'Ship schedule' : `Chosen: ${TRACKS[mode].name}`);
      if (cur && !resting) { cur.fadeOut(ctx.currentTime, 2); cur = null; pendingChange = null; nextAt = ctx.currentTime + 1; }
    },
    next() {
      if (mode !== 'schedule') return this.setMode(ORDER[(ORDER.indexOf(mode) + 1) % ORDER.length]);
      if (cur) { cur.fadeOut(ctx.currentTime, 2); cur = null; } pendingChange = null; nextAt = ctx.currentTime + 1;
    },
    skip() { return this.next(); },
    state() { return { enabled, paused, mode, resting, heard: { ...heard }, set: curSet, track: cur && cur.key, name: cur && cur.def.name, where: cur && cur.where(), total: cur && cur.total, quietFor: cur ? 0 : Math.max(0, nextAt - ctx.currentTime), pending: !!pendingChange }; },
    play,   // for tests and the harness: play(key, { startBar, fadeIn })
    TRACKS, SETS, PERIODS, LIST, periodAt,
  };
}
if (typeof module !== 'undefined') module.exports = { createWrenMusic };
