p = '/home/user/Cadet-game/starship-cadet.html'
s = open(p).read()
def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:90])
    s = s.replace(a, b)
rep("build 0.47.3", "build 0.47.4")
rep("const GAME_BUILD = '0.47.3';", "const GAME_BUILD = '0.47.4';")
anchor = "DECKS[4].keepsakes = { room: 'a', bed: '4-B1-4', place: '4-B1-4-keepsake',"
i = s.index(anchor); j = s.index("\n", i) + 1
block = r"""// 0.47.4 (Pillar 5 Step 3, seat A): the places the Step 3 pages ask for. All type `event` (inert: nobody's day plan uses them).
// Team jobs (m8-team-jobs): spots by each machine, `event: 'team-job'`, `works: true` (Works crew and you), `team: <machine id>`;
// spot 1 is the lead's (by the panel or between the machines), the others round the machine. DECKS[n].teamSpots[machine] lists them.
// The office meeting (promotion-officer, the summons): `5-office-visit-1` (you, beside Calder's desk) and `5-office-stand-1`
// (Calder, standing, to hand you the badge); her chair is `5-office-1`. The ceremony (Deck 1's observation room, by the stern
// windows): `1-ceremony-captain`, `1-ceremony-you`, `1-ceremony-guest-1..6` (Vance and Calder first, at your sides), `event: 'ceremony'`.
// Your cabin as an officer (4-23): `4-23-keepsake` and DECKS[4].homeKeepsakes['4-23'] (the shelf above its bed, the same shape as
// DECKS[4].keepsakes, for section 8b when your things move); its door plate shows your name once SHIP.works.home is '4-23'.
{
  const team = (n, room, machine, spots) => {
    (DECKS[n].teamSpots = DECKS[n].teamSpots || {})[machine] = spots.map((_, k) => `${machine.replace(/-\d+$/, '')}-team-${k + 1}`);
    spots.forEach(([c, r, face], k) => DECKS[n].places.push({ id: DECKS[n].teamSpots[machine][k], type: 'event', event: 'team-job', team: machine, works: true, at: [c, r], face, pose: 'stand', anim: 'work', room }));
  };
  team(3, 'R', '3-recycler-1', [[14, 15, 'w'], [14, 17, 'w'], [13, 14, 's'], [15, 15, 'w']]);
  team(4, 'l', '4-washer-1', [[14, 18, 'n'], [12, 18, 'n'], [11, 18, 'n']]);   // all four washers in a row
  team(5, 'n', '5-manifold-1', [[35, 14, 's'], [37, 14, 's'], [36, 13, 's']]);
  team(4, 't', '4-heater-1', [[21, 17, 'e'], [21, 19, 'e'], [20, 17, 'e']]);
  team(4, 's', '4-scrubber-1', [[22, 2, 'n'], [21, 3, 'n'], [23, 3, 'n']]);      // both stacks: spot 1 stands between them
}
DECKS[5].places.push(
  { id: '5-office-visit-1', type: 'event', event: 'office', at: [12, 1], xy: [12.4, 1.35], face: 'w', pose: 'stand', room: 'o' },
  { id: '5-office-stand-1', type: 'event', event: 'office', at: [10, 1], xy: [10.6, 1.35], face: 'e', pose: 'stand', room: 'o' },
);
{
  const fx = 2.95, fz = 2.5, at = (c, r, x, z) => ({ at: [c, r], xy: [x, z], face: Math.round(Math.atan2(fx - x, fz - z) * 180 / Math.PI) });
  DECKS[1].places.push(
    { id: '1-ceremony-captain', type: 'event', event: 'ceremony', at: [2, 2], xy: [2.45, 2.5], face: 'e', pose: 'stand', room: 'O' },
    { id: '1-ceremony-you', type: 'event', event: 'ceremony', at: [3, 2], xy: [3.4, 2.5], face: 'w', pose: 'stand', room: 'O' },
    ...[[3, 1, 3.45, 1.45], [3, 3, 3.45, 3.55], [4, 1, 4.4, 1.6], [4, 3, 4.4, 3.4], [4, 2, 4.5, 2.5], [5, 2, 5.4, 2.5]].map(([c, r, x, z], k) =>
      ({ id: '1-ceremony-guest-' + (k + 1), type: 'event', event: 'ceremony', ...at(c, r, x, z), pose: 'stand', room: 'O' })),
  );
}
DECKS[4].places.push({ id: '4-23-keepsake', type: 'event', at: [40, 10], xy: [40.1, 10.8], face: -139, pose: 'stand', room: 'W' });
DECKS[4].homeKeepsakes = { '4-23': { room: 'W', bed: '4-23', place: '4-23-keepsake', slots: [39.14, 39.28, 39.43, 39.57, 39.72, 39.86].map(x => [x, 2.17, 10.2]), trophy: [39.79, 2.17, 10.13] } };
"""
s = s[:j] + block + s[j:]
# the shelf in 4-23, last in Deck 4's dress
rep("    placeWall('a', 'keepsakeShelf', 'n', 2.5, { hitW: .9, it: IT('Your shelf', 'A plank above your bunk, just within reach from the top berth. Empty for now. People on the Wren tend to fill theirs.') });\n",
    "    placeWall('a', 'keepsakeShelf', 'n', 2.5, { hitW: .9, it: IT('Your shelf', 'A plank above your bunk, just within reach from the top berth. Empty for now. People on the Wren tend to fill theirs.') });\n"
    "    placeWall('W', 'keepsakeShelf', 'n', .5, { hitW: .9, it: IT('Shelf', 'A plank above the bed, waiting for whoever moves in.') });   // 0.47.4: 4-23, the officer's cabin you move to (Step 3)\n")
# the door plate: your name on 4-23 once it's your home
rep("    for (const [key, tw, text] of d.plates) { const who = d.officer(text); placeOnEdge(",
    "    let home = null; try { home = SHIP.works && SHIP.works.home; } catch (e) { home = null; }   // 0.47.4: your own cabin's plate (Step 3: 4-23 once you're an officer)\n"
    "    for (const [key, tw, text] of d.plates) { if (home && text === 'Spare ' + home) { let nm = 'Cadet'; try { nm = (SHIP.player && SHIP.player.name) || nm; } catch (e) {} placeOnEdge('namePlate', key, tw, { text: nm, sub: home + '  ·  Works Officer' }); continue; } const who = d.officer(text); placeOnEdge(")
open(p, 'w').write(s)
print('ok')
