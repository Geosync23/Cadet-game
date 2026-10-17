#!/usr/bin/env python3
"""Reference parser for .trad files (the traditions engineer's; the grammar is plans/trad-format.md).

content_gen.py (the dialogue engineer's) bakes content/traditions/*.trad into the game's TRADITIONS block. This file
is the reference for that step: content_gen.py may import parse_trad() and bake_traditions(), or copy them.

    python3 plans/trad_parse.py [content/traditions]      prints the baked block (stdout), or the errors (exit 1)

Output is byte-identical on re-runs: files are read in name order and keys are written in a fixed order.
"""
import json, os, re, sys

WEEKDAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
TONES = ('light', 'funny', 'warm', 'serious')
TEXT_KINDS = ('mail', 'ask', 'here', 'thanks', 'chatter')
KEY_ORDER = ('id', 'k', 'name', 'when', 'at', 'min', 'prio', 'jitter', 'early', 'where', 'hold', 'who', 'anim', 'host',
             'from', 'cake', 'decor', 'ties', 'invite', 'text')


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


def parse_when(v, where):
    t = v.split()
    low = [x.lower() for x in t]
    w, i = {}, 0
    if low[:1] == ['weekly'] and len(t) >= 2:
        w, i = {'weekday': _wd(t[1], where)}, 2
    elif low[:1] == ['every'] and len(t) >= 4 and low[2] == 'weeks' and t[1] in ('2', '4'):
        w, i = {'every': t[1] + 'weeks', 'weekday': _wd(t[3], where)}, 4
        if low[4:5] == ['week']:
            w['week'], i = int(t[5]), 6
            if not 1 <= w['week'] <= int(t[1]):
                raise TradError(f'{where}: week {w["week"]} of every {t[1]} weeks')
    elif low[:1] == ['quarter'] and len(t) >= 3:
        if low[1] == 'day':
            w, i = {'every': 'quarter', 'quarterDay': int(t[2])}, 3
        elif low[1] == 'week' and len(t) >= 4:
            w, i = {'every': 'quarter', 'week': int(t[2]), 'weekday': _wd(t[3], where)}, 4
    elif low[:1] == ['year'] and len(t) >= 3:
        if low[1] == 'day':
            w, i = {'every': 'year', 'dayOfYear': int(t[2])}, 3
        elif low[1] == 'week' and len(t) >= 4:
            w, i = {'every': 'year', 'week': int(t[2]), 'weekday': _wd(t[3], where)}, 4
    elif low[:1] == ['arrival'] and len(t) >= 2:
        if re.fullmatch(r'\+\d+', t[1]):
            w, i = {'after': 'arrival', 'days': int(t[1][1:])}, 2
        else:
            w, i = {'after': 'arrival', 'weekday': _wd(t[1], where)}, 2
            if len(t) > 2 and t[2].isdigit():
                w['nth'], i = int(t[2]), 3
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
            w[low[i]], i = int(t[i + 2]), i + 3
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


def _line(raw, where):
    tone, text = 'light', raw.strip()
    m = re.search(r'\s#(\w+)\s*$', text)
    if m:
        tone, text = m.group(1).lower(), text[:m.start()].rstrip()
        if tone not in TONES:
            raise TradError(f'{where}: unknown tone #{tone} ({", ".join(TONES)})')
    if not text:
        raise TradError(f'{where}: an empty line')
    return {'t': text, 'tone': tone}


def parse_trad(src, name='?'):
    """One .trad file's text -> a list of traditions (dicts in the baked shape)."""
    out, cur, sect = [], None, None
    for n, raw in enumerate(src.splitlines(), 1):
        where = f'{name}:{n}'
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        if line.startswith('@tradition'):
            bits = line.split()
            if len(bits) != 2 or not re.fullmatch(r'[a-z][a-zA-Z0-9-]*', bits[1]):
                raise TradError(f'{where}: "@tradition <id>" (lower-case letters, digits, dashes)')
            cur, sect = {'id': bits[1], 'where': [], 'text': {}}, None
            out.append(cur)
            continue
        if cur is None:
            raise TradError(f'{where}: text before "@tradition <id>"')
        if line.startswith('=='):
            sect = line[2:].strip().lower()
            if sect not in TEXT_KINDS:
                raise TradError(f'{where}: unknown section "== {sect}" ({", ".join(TEXT_KINDS)})')
            continue
        if sect:
            if not line.lstrip().startswith('- '):
                raise TradError(f'{where}: lines under "== {sect}" start with "- "')
            cur['text'].setdefault(sect, []).append(_line(line.lstrip()[2:], where))
            continue
        if ':' not in line:
            raise TradError(f'{where}: expected "key: value"')
        key, v = line.split(':', 1)
        key, v = key.strip().lower(), v.strip()
        if key == 'title':
            cur['name'] = v
        elif key in ('k', 'min', 'prio', 'jitter', 'early'):
            if not v.isdigit():
                raise TradError(f'{where}: {key} is a whole number')
            cur[key] = int(v)
        elif key == 'when':
            cur['when'] = parse_when(v, where)
        elif key == 'at':
            a, _, b = v.partition('-')
            cur['at'] = [_hhmm(a, where), _hhmm(b, where)]
            if cur['at'][1] <= cur['at'][0]:
                raise TradError(f'{where}: ends before it starts')
        elif key == 'where':
            cur['where'].append(parse_where(v, where))
        elif key == 'hold':
            cur['hold'] = [] if v.lower() == 'none' else [int(x) - 1 for x in v.split(',')]
        elif key == 'who':
            cur['who'] = parse_rules(v, where, _pct)
        elif key == 'anim':
            cur['anim'] = v.lower() if ' ' not in v.strip() else parse_rules(v, where, lambda s, w: None if s.lower() == 'none' else s.lower())
        elif key in ('host', 'from', 'decor'):
            cur[key] = v
        elif key == 'cake':
            cur['cake'] = v.lower() in ('yes', 'true')
        elif key == 'ties':
            parse_ties(v, where, cur.setdefault('ties', {}))
        elif key == 'invite':
            cur['invite'] = parse_invite(v, where)
        elif key in TEXT_KINDS:
            cur['text'].setdefault(key, []).append(_line(v, where))
        else:
            raise TradError(f'{where}: unknown key "{key}"')
    for t in out:
        for need in ('k', 'name', 'when', 'at'):
            if need not in t:
                raise TradError(f'{name}: tradition {t["id"]} has no {need}')
        if not t['where']:
            raise TradError(f'{name}: tradition {t["id"]} has no where')
        if 'who' not in t:
            raise TradError(f'{name}: tradition {t["id"]} has no who')
    return [{k: t[k] for k in KEY_ORDER if k in t} for t in out]


def bake_traditions(folder):
    """Every .trad file in the folder (name order) -> the text of the baked block, markers included."""
    trads, ids, ks = [], set(), set()
    for f in sorted(os.listdir(folder)):
        if f.endswith('.trad'):
            for t in parse_trad(open(os.path.join(folder, f), encoding='utf-8').read(), f):
                if t['id'] in ids:
                    raise TradError(f'{f}: id {t["id"]} used twice')
                if t['k'] in ks or not 434 <= t['k'] <= 499:
                    raise TradError(f'{f}: k {t["k"]} is taken or outside 434-499')
                ids.add(t['id'])
                ks.add(t['k'])
                trads.append(t)
    body = ',\n'.join('  ' + json.dumps(t, ensure_ascii=False, separators=(', ', ': ')) for t in trads)
    return ('// ---- BEGIN TRADITIONS (generated from content/traditions/*.trad: never edit by hand; plans/trad-format.md) ----\n'
            'const TRADITIONS = [\n' + body + (',\n' if body else '') + '];\n// ---- END TRADITIONS ----\n')


if __name__ == '__main__':
    try:
        sys.stdout.write(bake_traditions(sys.argv[1] if len(sys.argv) > 1 else 'content/traditions'))
    except TradError as e:
        print('TRAD ERROR', e, file=sys.stderr)
        sys.exit(1)
