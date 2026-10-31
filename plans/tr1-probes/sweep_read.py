# TR1: one line per tradition from sweep.py's JSON lines. Usage: sweep_read.py FILE...
import sys, json
hh = lambda m: '%02d:%02d' % (int(m) % 1440 // 60, int(m) % 60)
for f in sys.argv[1:]:
    for l in open(f):
        r = json.loads(l)
        if r.get('crash'): print(r['id'], 'CRASH', r['crash'][:120]); continue
        t = r['tap'] if isinstance(r['tap'], dict) else {'who': 'NOT-ON:' + str(r['tap'])}
        a, at, ne, af = r['at12'], r.get('afterTap', {}), r.get('nearEnd', {}), r.get('after', {})
        at = at if isinstance(at, dict) else {}; ne = ne if isinstance(ne, dict) else {}; af = af if isinstance(af, dict) else {}
        flags = []
        if not r['firstTj']: flags.append('NO-JOIN-OFFER')
        if r['firstTj'] and r['firstMark'] is None: flags.append('no-marker-seen')
        if t.get('who') is None: flags.append('NOBODY-TO-TAP')
        elif not t.get('tapJoin'): flags.append('TAP-DOES-NOTHING')
        if r['peak']['atIts'] == 0: flags.append('NOBODY-AT-ITS-PLACES')
        if af.get('tagged', 0) > 2: flags.append('still-%d-after-end' % af['tagged'])
        if r['errors']: flags.append('ERRORS')
        print('%-24s D%-3s %s-%s %-10s peak %2d/%2d  tj %-14s +%s  tap %-14s %-5s act %-34s card %-18s said %3d by %s  end %s/%s  %s' % (
            r['id'], r['day'], hh(r['from']), hh(r['to']), r['where'], r['peak']['tagged'], r['peak']['atIts'],
            (r['firstTj'] or [None, '-'])[1], (r['firstTj'] or ['-'])[0], t.get('who'), t.get('tapJoin'), (t.get('act') or '-')[:34],
            ','.join(c[1] for c in r['cards'])[:18] or '-', r['said'], ','.join(r['saidBy'][:3]), ne.get('tagged'), af.get('tagged'), ' '.join(flags)))
        if r['errors']: print('     errors:', r['errors'])
