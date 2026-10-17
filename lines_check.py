#!/usr/bin/env python3
"""lines_check.py: checks the writers' files under content/ before they're baked (writers run it before every push).

    python3 lines_check.py [GAME.html] [--strict] [--quiet]

Errors (exit 1): a file content_gen.py can't read; an unknown {token} or condition value; a line too long; an
unknown crew id; the banned list (romance and flirting, swearing beyond the ship's mild "blast", real-world brands
and politics, things the game doesn't have); #serious lines not behind tier>=friend or an arc beat; the baked
blocks in the game file out of date (re-run content_gen.py).
Warnings: names that aren't crew, guests or ship words; the same line in two places; American spellings; a habit:
condition in someone's own file for a habit they don't have; hard-to-read files (reading ease under 60).
Reports: coverage per person and kind against the targets in the plan (story crew about 200 lines, Works crew and your
bunkmates about 60, everyone else about 30 of their own); --strict turns missing coverage into errors (wave 2 on),
and the voice budget's numbers for a ship day (the rules section 22 enforces, and what the banks can supply).
The vocabulary it checks against is content_gen.py's COND_KEYS and content/README.md.
"""
import json, os, re, sys
import content_gen as cg

ROOT = os.path.dirname(os.path.abspath(__file__))

TOKENS = {'hi', 'bye', 'yes', 'thanks', 'wow', 'sigh', 'nick'}
PLACEHOLDERS = {'me', 'name', 'first', 'friend', 'best', 'rival', 'partner', 'mentor', 'mentee', 'boss', 'thing', 'trad',
                'machine', 'room', 'deck', 'dish', 'weekday', 'home', 'family', 'hobby', 'since', 'other'}
TRAD_PLACEHOLDERS = {'trad', 'host', 'names', 'first', 'season', 'weekday', 'time'}   # tradition texts: only these (plans/trad-format.md, tradFill)
VALUES = {
    'warmth': {'cold', 'warm'},
    'bond': {'best', 'friends', 'friend', 'rivals', 'rival', 'mentor', 'mentee', 'drifting', 'couple', 'partner'},   # section 20's BOND_KINDS and bondOf's aliases 'mood': {'low', 'ok', 'high'},
    'rep': {'new', 'known', 'well', 'theirs'}, 'ship.work': {'low', 'ok', 'high'}, 'ship.kindness': {'low', 'ok', 'high'},
    'ship.spirit': {'low', 'ok', 'high'}, 'week1': {'true', 'false'}, 'leaving': {'soon', 'you'}, 'newhere': {'true', 'false'},
    'guide': {'true', 'false'},
    'time': {'morning', 'afternoon', 'evening', 'night'}, 'weekday': {'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'},
    'season': {'sowing', 'greening', 'harvest', 'lanterns'}, 'birthday': {'me', 'you'},
    'dept': {'command', 'helm', 'comms', 'works', 'watch', 'survey', 'infirmary', 'galley', 'garden', 'store', 'civilian', 'guest'},
    'rank': {'junior', 'officer', 'senior', 'chief', 'xo', 'captain', 'guest'},
    'act': {'work', 'breakfast', 'dinner', 'meal', 'gym', 'wash', 'sleep', 'leisure', 'off', 'free', 'event', 'shop', 'call'},
}
BUBBLE_KINDS = {'smalltalk', 'rumour', 'overheard'}        # spoken over heads: 60 characters (90 at most)
LONG_KINDS = ('story', 'arc', 'moment', 'note', 'trad')    # chat lines, moments, Mail: 140
CARD = 90
NAME_W = 9                                                 # a filled-in name counts as this many characters

BANNED = [
    # romance and flirting with anyone (the user: no romance with the player; couples live quietly in the background)
    r'\bkiss\w*', r'\bflirt\w*', r'\bdarling\b', r'\bsweetheart\b', r'\bbabe\b', r'\bsexy\b', r'\bgorgeous\b', r'\bcrush\b',
    r'\bromanc\w*', r'\bdate night\b', r'\bon a date\b', r'\blove you\b', r'\bhandsome\b', r'\bcutie\b', r'\bsnog\w*',
    # swearing (the ship's "blast" is fine)
    r'\bdamn\w*', r'\bhell\b', r'\bbloody\b', r'\bcrap\w*', r'\bshit\w*', r'\bfuck\w*', r'\bbastard\w*', r'\bpiss\w*',
    r'\barse\w*', r'\bass\b', r'\bbollocks\b', r'\bgod\b', r'\bjesus\b', r'\bchrist\b',
    # real-world brands and politics
    r'\bcoca[- ]?cola\b', r'\bpepsi\b', r'\biphone\b', r'\bgoogle\b', r'\bfacebook\b', r'\bapple\b(?! pie)', r'\bnike\b',
    r'\bstarbucks\b', r'\bamazon\b', r'\bnetflix\b', r'\bdisney\b', r'\bmcdonald\w*', r'\bdemocrat\w*', r'\brepublican\w*',
    r'\bbrexit\b', r'\btory\b', r'\btories\b', r'\bparliament\b', r'\bpresident\b', r'\belection\w*',
    # things the game doesn't have (the social plan's writers' rules)
    r'\bphotos?\b', r'\bphotograph\w*', r'\bcamera\b', r'\bselfie\w*', r'\bguns?\b', r'\bweapons?\b', r'\bblaster\w*',
    r'\bphone\b', r'\binternet\b',
]
US = {'color': 'colour', 'favorite': 'favourite', 'favor': 'favour', 'center': 'centre', 'realize': 'realise',
      'organize': 'organise', 'gray': 'grey', 'mom': 'mum', 'honor': 'honour', 'neighbor': 'neighbour', 'theater': 'theatre',
      'apologize': 'apologise', 'recognize': 'recognise', 'traveled': 'travelled', 'cozy': 'cosy', 'defense': 'defence',
      'labor': 'labour', 'humor': 'humour', 'flavor': 'flavour', 'meter': 'metre', 'pajamas': 'pyjamas', 'cookie': 'biscuit'}
# capitalised words that aren't people (ship words, places, days, the Veyli...): names checks skip them
SHIP_WORDS = set('''I I'm I'll I've I'd OK Wren CSV Works Watch Survey Comms Helm Command Galley Infirmary Store Garden Deck Decks
Bridge Captain Commander Chief Chef Doctor Dr Envoy Cadet Officer Lieutenant Ensign Veyli Tiles Hesper Dock Mail Monday Tuesday
Wednesday Thursday Friday Saturday Sunday Sowing Greening Harvest Lanterns Board Mess Lounge Gym Shuttle Tern Coil Oi Ta
Mum Dad Gran Grandad Grandma Grandpa Nan Uncle Auntie Aunt Morning Evening Afternoon Night Hey Hi Hello Good Right Well'''.split())


def roster(game):
    with open(game, encoding='utf-8') as f:
        html = f.read()
    people = {}
    for name in ('ROSTER', 'ROSTER_GUESTS', 'GUESTS'):     # crew, guests living aboard, and event guests and visitors
        m = re.search(r'^const ' + name + r' = \[\n(.*?)^\];', html, re.M | re.S)
        for l in (m.group(1).split('\n') if m else []):
            l = l.strip().rstrip(',')
            if l.startswith('{"id"'):
                p = json.loads(l)
                people[p['id']] = p
    return people, html


def flesch(text):
    words = re.findall(r"[A-Za-z']+", text)
    if not words:
        return 100.0
    sents = max(1, len(re.findall(r'[.!?]+', text)))
    syl = 0
    for w in words:
        w = w.lower().strip("'")
        groups = re.findall(r'[aeiouy]+', w)
        n = len(groups) - (1 if w.endswith('e') and len(groups) > 1 and not w.endswith('le') else 0)
        syl += max(1, n)
    return 206.835 - 1.015 * len(words) / sents - 84.6 * syl / len(words)


def main(argv):
    strict, quiet = '--strict' in argv, '--quiet' in argv
    args = [a for a in argv if not a.startswith('--')]
    game = args[0] if args else os.path.join(ROOT, 'starship-cadet.html')
    errors, warns = [], []
    try:
        out = cg.bake()
    except cg.GenError as e:
        print('ERROR ' + str(e))
        print('lines_check: FAIL (content_gen.py can\'t read content/)')
        return 1
    people, html = roster(game)
    names = set()
    for p in people.values():
        names.update(w.strip('.') for w in p['name'].split())
    known_words = SHIP_WORDS | names

    # every line, with where it came from: (where, kind, entry, speaker id or None, source)
    allx = []
    for cid, card in out['VOICE'].items():
        if cid not in people:
            errors.append(f'VOICE "{cid}": no such crew member or guest')
        for kind, es in card.get('lines', {}).items():
            allx += [(f'lines/{cid}', kind, e, cid, 'own') for e in es]
    for tpl, card in out['VOICE_TEMPLATES'].items():
        for kind, es in card.get('lines', {}).items():
            allx += [(f'template {tpl}', kind, e, None, 'tpl') for e in es]
    for kind, es in out['LINES'].items():
        allx += [('bank', kind, e, None, 'bank') for e in es]
    for c in out['CONVOS']:
        for l in c['lines']:
            allx.append((f'overheard {c["topic"]}', 'overheard', dict(c, text=l['text']), None, 'convo'))
    for tr in out['TRADITIONS']:                           # the traditions engineer's shape: text: { kind: [{ t, tone }] }
        for sec, es in tr.get('text', {}).items():
            allx += [(f'tradition {tr["id"]}', 'trad.' + sec, {'text': e.get('text', e.get('t')), 'tone': e.get('tone', 'light'), 'id': tr['id']}, None, 'trad') for e in es]
    for mid, sc in out['MEETINGS_BAKED'].items():
        for l in sc['lines']:
            for x in ([l] if 'text' in l else [c for c in l['choice']] + [c['reply'] for c in l['choice'] if 'reply' in c]):
                allx.append((f'meeting {mid}', 'moment', {'text': x['text'], 'id': mid}, None, 'meet'))

    seen = {}
    for where, kind, e, cid, src in allx:
        t, tag = e['text'], f'{where} [{kind}] "{e["text"][:50]}"'
        for tok in re.findall(r'\{([^}]*)\}', t):
            if (tok not in TRAD_PLACEHOLDERS) if kind.startswith('trad.') else (tok not in TOKENS | PLACEHOLDERS):
                errors.append(f'{tag}: unknown token {{{tok}}}')
        if t.count('{') != t.count('}'):
            errors.append(f'{tag}: unbalanced braces')
        # conditions' values
        for scope in (e, e.get('not', {})):
            for k, v in scope.items():
                if k in VALUES:
                    for x in (v if isinstance(v, list) else [v]):
                        for alt in str(x).split('|'):
                            if alt not in VALUES[k]:
                                errors.append(f'{tag}: {k}:{alt} is not one of {", ".join(sorted(VALUES[k]))}')
                if k == 'aff':
                    for x in (v if isinstance(v, list) else [v]):
                        for alt in str(x).split('|'):
                            band = alt.rsplit(':', 1)
                            if band[-1] not in {'rival', 'neutral', 'friend'} or (len(band) == 2 and band[0] not in people):
                                errors.append(f'{tag}: aff is aff:rival|neutral|friend or aff:<crewId>:<band>')
                if k == 'moved':
                    for x in (v if isinstance(v, list) else [v]):
                        if x not in people:
                            errors.append(f'{tag}: moved:{x} is not a crew id')
                if k in ('beat', 'beatIs'):
                    for x in (v if isinstance(v, list) else [v]):
                        if not re.fullmatch(r'[\w-]+\.\d+', x):
                            errors.append(f'{tag}: beat is like beat:tomas.3 (arc id, a dot, beats told)')
        # length, with names filled in
        n = len(re.sub(r'\{[^}]*\}', 'x' * NAME_W, t))
        lim = 90 if kind in ('trad.chatter', 'trad.ask', 'trad.here') else 200 if kind in ('trad.mail', 'trad.thanks') else 400 if kind == 'letter' else 60 if kind in BUBBLE_KINDS else 140 if kind.startswith(LONG_KINDS) else CARD
        if not e.get('old'):
            if n > (90 if kind in BUBBLE_KINDS else lim):
                errors.append(f'{tag}: {n} characters (at most {lim})')
            elif n > lim:
                warns.append(f'{tag}: {n} characters (a bubble wants {lim} or fewer)')
        low = t.lower()
        for b in BANNED:
            m = re.search(b, low)
            if m:
                errors.append(f'{tag}: "{m.group(0)}" is on the banned list')
        for us, uk in US.items():
            if re.search(r'\b' + us + r's?\b', low):
                warns.append(f'{tag}: American spelling "{us}" (British: "{uk}")')
        mems = [str(x) for x in (e.get('mem') if isinstance(e.get('mem'), list) else [e.get('mem')]) if x]
        if e.get('tone') == 'serious' and not ((e.get('tier') and e['tier'][0] >= 3) or e.get('beat') or e.get('beatIs') or any(m.startswith('moment') for m in mems)
                                               or 'soon' in str(e.get('leaving', '')) or kind.startswith(('story', 'arc', 'moment'))):
            errors.append(f'{tag}: #serious needs tier>=friend, a beat:, mem:moment or leaving:soon (serious moments are earned)')
        if cid and e.get('habit'):
            have = set(people.get(cid, {}).get('habits', [])) | {h['add'] for h in people.get(cid, {}).get('habitShifts', [])}
            for h in (e['habit'] if isinstance(e['habit'], list) else [e['habit']]):
                if not set(h.split('|')) & have:
                    warns.append(f'{tag}: {cid} doesn\'t have the habit "{h}"')
        # names: capitalised words mid-sentence that aren't crew, guests or ship words
        for m in re.finditer(r'(?<![.!?]\s)(?<!^)(?<!["(])\b([A-Z][a-z]+)\b', t):
            w = m.group(1)
            if w not in known_words and m.start() > 0 and not re.search(r'[.!?:]\s*$', t[:m.start()]):
                warns.append(f'{tag}: "{w}" isn\'t a crew member, guest or ship word (a name only from the roster)')
        for m in re.finditer(r"\b([A-Z][a-z]+)(?:'s\b| says\b| said\b| told\b| thinks\b| wants\b| is\b| was\b| and I\b)", t):
            if m.group(1) not in known_words and m.group(1) not in ('It', 'That', 'This', 'There', 'What', 'Who', 'Everyone', 'Nobody', 'Someone', 'Here', 'He', 'She', 'Today', 'Tomorrow', 'Dinner', 'Breakfast', 'Lunch', 'Food', 'Nothing', 'Something', 'Life', 'Home', 'Work',
                                                                       'Or', 'How', 'Why', 'When', 'Where', 'Which', 'Everything', 'Anyone', 'Anything', 'Mine', 'Yours',
                                                                       'His', 'Her', 'Their', 'Our', 'Your', 'My', 'One', 'Each', 'Now', 'Then', 'So', 'Yes', 'No', 'Yesterday'):
                warns.append(f'{tag}: "{m.group(1)}" looks like a name that isn\'t crew or a guest')
        key = (kind, t)
        if key in seen and src != 'convo':
            warns.append(f'{tag}: the same line is also in {seen[key]}')
        seen.setdefault(key, where)

    # reading ease per file
    byfile = {}
    for where, kind, e, cid, src in allx:
        byfile.setdefault(where, []).append(e['text'])
    ease = {w: flesch(' '.join(ts)) for w, ts in byfile.items()}
    for w, s in sorted(ease.items()):
        if s < 60:
            warns.append(f'{w}: reading ease {s:.0f} (aim for 60 or more: short words, short sentences)')

    # the baked blocks are up to date
    new = html
    for name, body in cg.blocks(out).items():
        try:
            new = cg.splice(new, name, body)
        except cg.GenError as e:
            errors.append(str(e))
    if new != html:
        errors.append('the baked blocks in the game file are out of date: run python3 content_gen.py')

    # coverage per person (their own lines) against the plan's targets
    crew = [p for p in people.values() if p.get('rank') != 'guest']
    story = {p['id'] for p in crew if p.get('story')} | {'torres-zeke', 'calder', 'brennan', 'kovac-zainab'}
    def target(p):
        if p['id'] in story:
            return 200
        if p.get('dept') == 'works' or (p.get('bed') or '').startswith('4-B1'):
            return 60
        return 30
    cov, kinds_seen = [], set()
    for p in crew:
        card = out['VOICE'].get(p['id'], {})
        n = sum(len(v) for v in card.get('lines', {}).values())
        kinds_seen.update(card.get('lines', {}).keys())
        cov.append((p['id'], n, target(p), 'words' in card, sorted(card.get('lines', {}).keys())))
    with_card = sum(1 for c in cov if c[3])
    short = [c for c in cov if c[1] < c[2]]
    if strict:
        for c in short:
            errors.append(f'{c[0]}: {c[1]} lines of their own (target {c[2]})')
        for c in cov:
            if not c[3]:
                errors.append(f'{c[0]}: no voice card')

    # the voice budget for a ship day: the rules (section 22 and 20 enforce them) and what the banks can supply
    serious = sum(1 for x in allx if x[2].get('tone') == 'serious')
    budget = [
        'one bubble or one overheard conversation on screen at a time; none while a chat card or meeting is open',
        'at most one #serious line a day (ship-wide); reactions once per person per kind per day',
        'overheard conversations and reactions never repeat to you within 7 ship days (the saved ring)',
        f'supply: {len(out["CONVOS"])} overheard conversations (a week of evenings wants about 30), '
        f'{len(out["LINES"].get("cue", []))} reaction lines, {serious} #serious lines',
    ]

    print(f'lines_check: {len(allx)} lines in {len(byfile)} places; {len(out["VOICE"])} voice cards '
          f'({with_card} with words) for {len(crew)} crew; {len(out["CONVOS"])} conversations; '
          f'{len(out["MEETINGS_BAKED"])} meetings; {len(out["TRADITIONS"])} traditions')
    if not quiet:
        print('coverage (own lines / target), people with any:')
        for c in cov:
            if c[1] or c[3]:
                print(f'  {c[0]:<18} {c[1]:>4} / {c[2]:<4} card: {"yes" if c[3] else "no "}  kinds: {", ".join(c[4])}')
        print(f'  {len(short)} of {len(crew)} crew below their target (expected until the writers start)')
        print('voice budget (a ship day):')
        for b in budget:
            print('  ' + b)
        print('reading ease: ' + ', '.join(f'{w} {s:.0f}' for w, s in sorted(ease.items())))
    for w in warns:
        print('warn  ' + w)
    for e in errors:
        print('ERROR ' + e)
    print(f'lines_check: {"FAIL" if errors else "PASS"} ({len(errors)} errors, {len(warns)} warnings)')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
