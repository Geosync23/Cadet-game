#!/usr/bin/env python3
"""Reference parser for .trad files (the traditions engineer's; the grammar is plans/trad-format.md).

content_gen.py (the dialogue engineer's) bakes content/traditions/*.trad into the game's TRADITIONS block. It reads
the file's frame itself (the @tradition header, // comments, == sections, ? conditions and - lines, as for .lines
files) and hands each "key: value" field line to parse_field() here, then calls finish() once per file. So the field
grammar lives in one place, this file, owned by the traditions engineer.

    python3 plans/trad_parse.py [content/traditions]           checks the files; prints the traditions as JSON
    python3 plans/trad_parse.py --standin [content/traditions]  prints section 18's stand-in block (TRAD_STANDIN)

Output is byte-identical on re-runs: files are read in name order and keys are written in a fixed order.
"""
import json, os, re, sys

WEEKDAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
TONES = ('light', 'funny', 'warm', 'serious')
TEXT_KINDS = ('mail', 'ask', 'here', 'thanks', 'chatter')
KEY_ORDER = ('id', 'k', 'name', 'when', 'at', 'min', 'prio', 'jitter', 'early', 'where', 'hold', 'who', 'anim', 'host',
             'from', 'cake', 'decor', 'ties', 'invite', 'trace', 'meal', 'text')


class TradError(Exception):
    pass


def _wd(word, where):
    w = word.lower()
    if w not in WEEKDAYS:
        raise TradError(f'{where}: "{word}" is not a weekday')
    return WEEKDAYS.index(w)


def _hhmm(s, where):
    m = re.fullmatch(r'(\d{1,2}):(\d{2})', s.strip())
    if not m or int(m.group(1)) > 23 or int(m.group(2)) > 59:
        raise TradError(f'{where}: "{s}" is not a time like 19:30')
    return int(m.group(1)) * 60 + int(m.group(2))


def _pct(s, where):
    s = s.strip().lower()
    if s == 'always':
        return 1
    if s == 'never':
        return 0
    m = re.fullmatch(r'(\d{1,3})%', s)
    if not m or int(m.group(1)) > 100:
        raise TradError(f'{where}: "{s}" should be a percentage like 40%, or always / never')
    return int(m.group(1)) / 100


def _int(s, where, lo, hi, what):
    if not re.fullmatch(r'\d+', str(s)) or not lo <= int(s) <= hi:
        raise TradError(f'{where}: {what} should be a whole number from {lo} to {hi}, not "{s}"')
    return int(s)


def parse_when(v, where):
    t = v.split()
    low = [x.lower() for x in t]
    w, i = {}, 0
    if low[:1] == ['weekly'] and len(t) >= 2:
        w, i = {'weekday': _wd(t[1], where)}, 2
    elif low[:1] == ['every'] and len(t) >= 4 and low[2] == 'weeks' and t[1] in ('2', '4'):
        w, i = {'every': t[1] + 'weeks', 'weekday': _wd(t[3], where)}, 4
        if low[4:5] == ['week']:
            if len(t) < 6:
                raise TradError(f'{where}: "week" needs a number')
            w['week'], i = _int(t[5], where, 1, int(t[1]), f'the week of every {t[1]} weeks'), 6
    elif low[:1] == ['quarter'] and len(t) >= 3:
        if low[1] == 'day':
            w, i = {'every': 'quarter', 'quarterDay': _int(t[2], where, 1, 91, 'a day of the season')}, 3
        elif low[1] == 'week' and len(t) >= 4:
            w, i = {'every': 'quarter', 'week': _int(t[2], where, 1, 13, 'a week of the season'), 'weekday': _wd(t[3], where)}, 4
    elif low[:1] == ['year'] and len(t) >= 3:
        if low[1] == 'day':
            w, i = {'every': 'year', 'dayOfYear': _int(t[2], where, 1, 364, 'a day of the year')}, 3
        elif low[1] == 'week' and len(t) >= 4:
            w, i = {'every': 'year', 'week': _int(t[2], where, 1, 52, 'a week of the year'), 'weekday': _wd(t[3], where)}, 4
    elif low[:1] == ['arrival'] and len(t) >= 2:
        if re.fullmatch(r'\+\d+', t[1]):
            w, i = {'after': 'arrival', 'days': _int(t[1][1:], where, 0, 364, 'days after arrival')}, 2
        else:
            w, i = {'after': 'arrival', 'weekday': _wd(t[1], where)}, 2
            if len(t) > 2 and t[2].isdigit():
                w['nth'], i = _int(t[2], where, 1, 52, 'which one after arrival'), 3
    elif low[:1] == ['birthday']:
        w, i = {'birthday': True}, 1
    if not w:
        raise TradError(f'{where}: can\'t read when "{v}" (see plans/trad-format.md)')
    while i < len(t):                                      # optional: season <name>[,<name>], from day N, until day N
        if low[i] == 'season' and i + 1 < len(t):
            s = [x for x in low[i + 1].split(',') if x]
            bad = [x for x in s if x not in ('sowing', 'greening', 'harvest', 'lanterns')]
            if bad:
                raise TradError(f'{where}: unknown season {bad}')
            w['season'], i = s[0] if len(s) == 1 else s, i + 2
        elif low[i] in ('from', 'until') and low[i + 1:i + 2] == ['day'] and i + 2 < len(t):
            w[low[i]], i = _int(t[i + 2], where, 0, 100000, 'a day'), i + 3
        else:
            raise TradError(f'{where}: can\'t read "{" ".join(t[i:])}" in when')
    return w


def parse_where(v, where):
    m = re.fullmatch(r'(\d)\s+pool\s+([\w-]+)', v.strip())
    if m:
        return {'deck': int(m.group(1)), 'pool': m.group(2)}
    m = re.fullmatch(r'(\d)\s+room\s+([^:]+):\s*(.+)', v.strip())
    if not m:
        raise TradError(f'{where}: can\'t read where "{v}" (try "3 pool garden" or "3 room Bow lounge: lounge-seat")')
    out = {'deck': int(m.group(1)), 'room': '^' + re.escape(m.group(2).strip()).replace('\\ ', ' ') + '$', 'types': []}
    words = [x.strip() for x in m.group(3).split(',') if x.strip()]
    for x in words:
        if x == 'free':
            out['free'] = True
        elif x == 'officers':
            out['who'] = 'officer'
        elif x.startswith('ids '):
            out['ids'] = x[4:].strip()
        else:
            out['types'].append(x)
    if not out['types']:
        raise TradError(f'{where}: where "{v}" names no place types')
    return out


def parse_rules(v, where, value):
    rules = []
    for part in [x.strip() for x in v.split(',') if x.strip()]:
        bits = part.rsplit(None, 1)
        if len(bits) != 2:
            raise TradError(f'{where}: "{part}" needs who and how much (e.g. "gardener 90%")')
        rules.append([bits[0].lower(), value(bits[1], where)])
    return rules


def parse_ties(v, where, ties):
    t = v.split()
    kind = t[0].lower() if t else ''
    if kind == 'garden' and len(t) == 2 and t[1] in ('sow', 'tend', 'harvest'):
        ties['garden'] = t[1]
    elif kind == 'decor' and len(t) == 2:
        ties['decor'] = t[1]
    elif kind in ('galley', 'tally') and len(t) >= 2:
        o = {}
        for x in t[1:]:
            if '=' not in x:
                if kind == 'tally' and 'kind' not in o:
                    o['kind'] = x
                    continue
                raise TradError(f'{where}: "{x}" in ties {kind} should be key=value')
            a, b = x.split('=', 1)
            o[a] = int(b) if b.isdigit() else b.split('|') if a == 'choices' else b
        ties[kind] = o
    else:
        raise TradError(f'{where}: can\'t read ties "{v}" (galley / garden / decor / tally)')


def parse_invite(v, where):
    o = {}
    for m in re.finditer(r'(\w+)=("[^"]*"|\S+)', v):
        a, b = m.group(1), m.group(2).strip('"')
        o[a] = _pct(b, where) if a == 'odds' else b
    if 'line' not in o:
        raise TradError(f'{where}: invite needs line="..."')
    return o


def parse_field(tr, key, v, where):
    """One "key: value" line of a .trad file into tr (a dict being built), in the baked shape. Raises TradError."""
    key, v = key.strip().lower(), v.strip()
    if key == 'title':
        tr['name'] = v
    elif key in ('k', 'min', 'prio', 'jitter', 'early'):
        if not v.isdigit():
            raise TradError(f'{where}: {key} is a whole number')
        tr[key] = int(v)
    elif key == 'when':
        tr['when'] = parse_when(v, where)
    elif key == 'at':
        a, _, b = v.partition('-')
        tr['at'] = [_hhmm(a, where), _hhmm(b, where)]
        if tr['at'][1] <= tr['at'][0]:
            raise TradError(f'{where}: ends before it starts')
    elif key == 'where':
        tr.setdefault('where', []).append(parse_where(v, where))
    elif key == 'hold':
        tr['hold'] = [] if v.lower() == 'none' else [_int(x.strip(), where, 1, 9, 'a where line (1 = the first)') - 1 for x in v.split(',')]
    elif key == 'who':
        tr['who'] = parse_rules(v, where, _pct)
    elif key == 'anim':
        tr['anim'] = v.lower() if ' ' not in v else parse_rules(v, where, lambda s, w: None if s.lower() == 'none' else s.lower())
    elif key in ('host', 'from', 'decor', 'trace'):
        tr[key] = v
    elif key == 'meal':
        if v.lower() not in ('dinner', 'breakfast'):
            raise TradError(f'{where}: meal is dinner or breakfast (going to it IS that meal)')
        tr['meal'] = v.lower()
    elif key == 'cake':
        tr['cake'] = v.lower() in ('yes', 'true')
    elif key == 'ties':
        parse_ties(v, where, tr.setdefault('ties', {}))
    elif key == 'invite':
        tr['invite'] = parse_invite(v, where)
    elif key in TEXT_KINDS:
        raise TradError(f'{where}: texts go in a section: "== {key}" and then "- ..." lines')
    else:
        raise TradError(f'{where}: unknown field "{key}" (see plans/trad-format.md)')


def finish(tr, tid, where):
    """After the last line of a tradition: the checks, and the keys in their fixed order (tr['text'] as built by the
    generator: { section: [ line entries ] })."""
    for need in ('k', 'name', 'when', 'at', 'where', 'who'):
        if need not in tr:
            raise TradError(f'{where}: tradition {tid} has no {need}' + (' (ask the traditions engineer for one)' if need == 'k' else ''))
    if not 434 <= tr['k'] <= 499:
        raise TradError(f'{where}: k {tr["k"]} is outside 434-499')
    if any(h >= len(tr['where']) for h in tr.get('hold', [])):
        raise TradError(f'{where}: hold names a where line that is not there')
    bad = [x for x in tr.get('text', {}) if x not in TEXT_KINDS]
    if bad:
        raise TradError(f'{where}: unknown section(s) {bad} ({", ".join(TEXT_KINDS)})')
    out = {'id': tid}
    out.update({k: tr[k] for k in KEY_ORDER if k in tr and k != 'id'})
    return out


def check_all(trads):
    """Across every tradition: ids and hash keys used once."""
    ids, ks = set(), set()
    for t in trads:
        if t['id'] in ids:
            raise TradError(f'tradition id {t["id"]} used twice')
        if t['k'] in ks:
            raise TradError(f'tradition {t["id"]}: k {t["k"]} is taken')
        ids.add(t['id'])
        ks.add(t['k'])


def parse_trad(src, name='?'):
    """One .trad file (one tradition) -> [tradition] in the baked shape (a list, so callers can add lists together).
    Comments start with // or #. Conditions on lines (? ...) are skipped here."""
    tr, tid, sect = {}, None, None
    for n, raw in enumerate(src.splitlines(), 1):
        where = f'{name}:{n}'
        line = raw.strip()
        if not line or line.startswith('//') or line.startswith('#') or line.startswith('?'):
            continue
        if tid is None:
            bits = line.split()
            if bits[0] != '@tradition' or len(bits) != 2 or not re.fullmatch(r'[a-z][a-z0-9-]*', bits[1]):
                raise TradError(f'{where}: a .trad file starts with "@tradition <id>" (lower-case letters, digits, dashes)')
            tid = bits[1]
            continue
        if line.startswith('=='):
            sect = line[2:].strip()
            tr.setdefault('text', {}).setdefault(sect, [])
            continue
        if sect is not None:
            if not line.startswith('- '):
                raise TradError(f'{where}: lines under "== {sect}" start with "- "')
            tone, text = 'light', line[2:].strip()
            m = re.search(r'\s#(\w+)\s*$', text)
            if m:
                tone, text = m.group(1), text[:m.start()].rstrip()
                if tone not in TONES:
                    raise TradError(f'{where}: unknown tone #{tone}')
            tr['text'][sect].append({'t': text, 'tone': tone})
            continue
        if ':' not in line:
            raise TradError(f'{where}: tradition fields are "key: value"')
        k, v = line.split(':', 1)
        parse_field(tr, k, v, where)
    if tid is None:
        raise TradError(f'{name}: empty file')
    return [finish(tr, tid, name)]


def read_all(folder):
    trads = [t for f in sorted(os.listdir(folder)) if f.endswith('.trad') for t in parse_trad(open(os.path.join(folder, f), encoding='utf-8').read(), f)]
    check_all(trads)
    return trads


def standin(trads):
    body = ''.join(f'  {json.dumps(t["id"])}: {json.dumps(t, ensure_ascii=False, separators=(", ", ": "))},\n' for t in sorted(trads, key=lambda t: t['id']))
    return ('// ---- the stand-in (plans/trad_parse.py --standin): until content_gen.py\'s TRADITIONS block is merged; then delete it\n'
            'var TRAD_STANDIN = {\n' + body + '};\n')


def bake_traditions(folder):
    """Every .trad file in the folder (name order) -> the baked block, markers included, byte-identical on re-runs:
    content_gen.py puts its const TRADITIONS = [ ... ]; (one tradition a line) in section 22's markers."""
    trads = read_all(folder)
    body = ''.join('  ' + json.dumps(t, ensure_ascii=False, separators=(', ', ': ')) + ',\n' for t in trads)
    return ('// ---- BEGIN TRADITIONS (generated from content/traditions/*.trad: never edit by hand; plans/trad-format.md) ----\n'
            'const TRADITIONS = [\n' + body + '];\n// ---- END TRADITIONS ----\n')


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    try:
        trads = read_all(args[0] if args else 'content/traditions')
    except TradError as e:
        print('TRAD ERROR', e, file=sys.stderr)
        sys.exit(1)
    if '--standin' in sys.argv:
        sys.stdout.write(standin(trads))
    else:
        for t in trads:
            print(json.dumps(t, ensure_ascii=False))
        print(f'{len(trads)} tradition(s) OK', file=sys.stderr)
