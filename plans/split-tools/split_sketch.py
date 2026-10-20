# plans/split-tools/split_sketch.py: the split reviewer (SR1)'s reference cut for plans/split-plan.html, NOT the real split.py.
# Cuts by marker lines (never line numbers) into the 40 pieces of the plan; prints whether gluing them back is byte-identical.
#   python3 plans/split-tools/split_sketch.py GAME.html OUTDIR [-v]
# Byte-identical on 0.64.0 (e71388f, sha256 534ceeda...918aa) and 0.64.2 (1eeb99c, e4897023...27624).
import sys, re, hashlib, os
# (piece, regex of the line the piece starts at, back: lines to step back from the match (the ==== banner))
CUTS = [
 ('page/head.html', None, 0),
 ('page/css.css', r'^<style>$', -1),            # starts the line AFTER <style>
 ('page/body.html', r'^</style>$', 0),
 ('js/s01-setup-materials.js', r'^\(\(\) => \{$', -1),
 ('js/s04-deck-kit.js', r'^// 4\. DECK: ', 1),
 ('js/s04c-deck-build.js', r'^// 4c\. ', 1),
 ('js/s04d-utility-kit.js', r'^// 4d\. ', 1),
 ('js/s04d-deck4-quarters.js', r'^// DECK 4: QUARTERS', 1),
 ('js/s04d-deck5-operations.js', r'^// DECK 5: OPERATIONS', 1),
 ('js/s04d-deck3-commons.js', r'^// DECK 3: COMMONS', 1),
 ('js/s04d-deck2-command.js', r'^// DECK 2: COMMAND', 1),
 ('js/s04d-deck6-engineering.js', r'^// DECK 6: ENGINEERING', 1),
 ('js/s04d-deck1-bridge.js', r'^// DECK 1: BRIDGE', 1),
 ('js/s04d-places-all-decks.js', r'^// ---- Big gatherings ', 0),
 ('js/s04e-rec-deck.js', r'^// 4e\. ', 1),
 ('js/s05-lighting.js', r'^// 5\. LIGHTING', 1),
 ('js/s13-time-save.js', r'^// 13\. SHIP TIME', 1),
 ('js/s14-schedules.js', r'^// 14\. SCHEDULES', 1),
 ('js/s19-device.js', r'^// 19\. DEVICE', 1),
 ('js/s15-player-needs.js', r'^// 15\. PLAYER NEEDS', 1),
 ('js/s15b-interactions.js', r'^// 15b\. ', 1),
 ('js/s15r-rec-activities.js', r'^// 15r\. ', 1),
 ('js/s16-galley.js', r'^// 16\. GALLEY', 1),
 ('js/s17-machines-jobs.js', r'^// 17\. MACHINES', 1),
 ('js/s22-lines-engine-1.js', r'^// 22\. LINES', 1),
 ('content/s22-words.gen.js', r'^// ---- BEGIN LINES ', 0),
 ('js/s22-lines-engine-2.js', r'^// ---- END TRADITIONS ----$', -1),
 ('js/s18-events.js', r'^// 18\. SHIP EVENTS', 1),
 ('js/s20-social.js', r'^// 20\. SOCIAL', 1),
 ('js/s21-arrival-clothes.js', r'^// 21\. ARRIVAL', 1),
 ('js/s23-tiles-lightdisc.js', r'^// 23\. TILES', 1),
 ('js/s24-work.js', r'^// 24\. WORK', 1),
 ('js/s24k-cases.js', r'^// 24k\. ', 1),
 ('js/s06-camera-grid.js', r'^// 6\. CAMERA', 1),
 ('js/s08-characters-crowd.js', r'^// 8\. CHARACTER KIT', 1),
 ('js/s09-crew-data.js', r'^// 9\. CREW DATA', 1),
 ('js/s10-walkers.js', r'^// 10\. WALKERS', 1),
 ('js/s08c-rec-moves.js', r'^// 8c\. ', 1),
 ('js/s11-ui-main-loop.js', r'^// 11\. INTERACTION', 1),
 ('page/tail.html', r'^\}\)\(\);$', 0),
]
def split(data, merge10=False):
    L = data.split(b'\n')  # last element '' if trailing newline
    starts = [0]; pos = 0
    for name, rx, back in CUTS[1:]:
        hits = [i for i in range(len(L)) if re.match(rx.encode(), L[i])]
        if name == 'page/tail.html': hits = hits[-1:]   # the last })(); closes the IIFE
        if name == 'js/s01-setup-materials.js': hits = hits[:1]   # the first (() => { opens it (4 more inner IIFEs at column 0)
        if len(hits) != 1: raise SystemExit(f'{name}: marker {rx} found {len(hits)} times')
        s = hits[0] - back
        if s <= starts[-1]: raise SystemExit(f'{name}: out of order')
        starts.append(s)
    out = []
    for k, (name, _, _) in enumerate(CUTS):
        a = starts[k]; b = starts[k+1] if k + 1 < len(starts) else len(L)
        chunk = b'\n'.join(L[a:b]) + (b'\n' if k + 1 < len(starts) else b'')
        out.append((name, chunk))
    return out
if __name__ == '__main__':
    data = open(sys.argv[1], 'rb').read(); outdir = sys.argv[2]
    ps = split(data)
    for name, c in ps:
        p = os.path.join(outdir, name); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, 'wb').write(c)
    open(os.path.join(outdir, 'ORDER'), 'w').write(''.join(n + '\n' for n, _ in ps))
    joined = b''.join(c for _, c in ps)
    print('identical' if joined == data else 'DIFFERENT', hashlib.sha256(joined).hexdigest(), len(ps), 'pieces')
    if '-v' in sys.argv:
        for n, c in ps: print(f'{c.count(b"\n"):6d} {n}')
