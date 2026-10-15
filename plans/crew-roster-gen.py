# Starship Cadet: crew roster generator (the crew designer's tool, not part of the game)
#
# Writes the 75-person crew roster in two forms:
#   1. the ROSTER data block for section 9 of starship-cadet.html (fixed data: the game never runs this script)
#   2. plans/crew-roster.html, the readable roster page
#
# Run it only when you mean to change the crew:
#   python3 plans/crew-roster-gen.py
# It rewrites the ROSTER block in section 9 of starship-cadet.html (between the BEGIN/END ROSTER markers)
# and plans/crew-roster.html.
# The same seed always gives the same crew, so re-running without edits changes nothing.
#
# Story crew and provisional names are written out by hand below; only the other crew are generated.

import json, random, hashlib, html, os

R = random.Random(20261015)
DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
UNIFORM = {'command': 'command', 'helm': 'command', 'comms': 'command', 'works': 'works', 'galley': 'works',
           'watch': 'watch', 'survey': 'survey', 'infirmary': 'infirmary'}
RANK_NUM = {'junior': 0, 'officer': 1, 'senior': 1, 'chief': 2, 'xo': 3, 'captain': 4}

def seed_of(pid):
    return int(hashlib.sha256(pid.encode()).hexdigest()[:8], 16) % 1000000

# ---------------------------------------------------------------- habits (the shared vocabulary)
HABITS = {
    'early-riser': 'Wakes 30-45 minutes before their shift\'s usual time; first in the breakfast window.',
    'late-sleeper': 'Wakes late; breakfast near the end of the window, or grab-and-go.',
    'early-to-bed': 'Goes to bed 30-60 minutes before the usual time.',
    'night-owl': 'Stays up 30-60 minutes later, in leisure.',
    'skips-breakfast': 'Most days (about 70%) no breakfast: a grab-shelf stop on the way to work instead.',
    'late-diner': 'Dinner in the last hour of the dinner window.',
    'lingers-at-meals': 'Meals last 15-25 minutes longer.',
    'window-seat': 'Prefers a seat by a window (mess, lounge, common room) when one is free.',
    'workaholic': 'At work 15-30 minutes early and leaves 15-30 minutes late.',
    'tea-break': 'One mid-shift break of about 15 minutes at a tea or break spot.',
    'gym-regular': 'Gym after shift on most work days.',
    'garden-lover': 'Leisure in the garden.',
    'lounge-regular': 'Evenings in the bow lounge.',
    'quiet-corner': 'Leisure somewhere quiet: the lounge\'s window end, the chart room, the observatory.',
    'common-room': 'Evenings in the Deck 4 junior common room (juniors only).',
    'music': 'Evenings in the Deck 4 music room.',
    'calls-home': 'A call-home booth on rest days, and sometimes after dinner.',
    'evening-shower': 'Washes before bed instead of in the morning.',
}

# ---------------------------------------------------------------- workplaces
WORK = {   # where each kind of job is done: deck and place type
    'command': (1, 'work:command'), 'helm': (1, 'work:helm'), 'ops': (1, 'work:ops'), 'comms-bridge': (1, 'work:comms'),
    'comms': (2, 'work:comms'), 'watch': (2, 'work:watch'), 'survey': (2, 'work:survey'),
    'galley': (3, 'work:galley'), 'infirmary': (3, 'work:infirmary'),
    'works': (5, 'work:works'), 'engine': (6, 'work:engine'),
}
WORK_WORDS = {
    'work:command': 'the bridge', 'work:helm': 'the helm, on the bridge', 'work:ops': 'the ops console, on the bridge',
    'work:comms': 'comms', 'work:watch': 'the Watch office', 'work:survey': 'the Survey labs',
    'work:galley': 'the galley', 'work:infirmary': 'the infirmary', 'work:works': 'the Works bay', 'work:engine': 'the engine room',
}

# ---------------------------------------------------------------- story crew and provisional names (by hand)
# looks and bios of the existing crew are copied exactly from CREW in section 9
STORY = [
    dict(id='marrow', name='Captain Odile Marrow', story=True, rank='captain', dept='command', role='Captain', shift='day', bed='2-C', job='command',
         looks=dict(skin=4, hair='bun', hairColor='grey', height=1.03, build='slim', acc=['earrings']),
         bio='Calm, fair, and always testing you with questions.',
         habits=['early-riser', 'music'], traits=['patient', 'curious', 'quietly funny'],
         life=['Plays the grand piano in the music room late on Thursdays.', 'Has commanded the Wren for six years and knows every captain in her portrait gallery by name.']),
    dict(id='vance', name='Commander Teo Vance', story=True, rank='xo', dept='command', role='Executive Officer', shift='day', bed='2-X', job='command',
         looks=dict(skin=1, hair='short', hairColor='black', height=1.08, build='average', acc=[]),
         bio='By the book. Every page of it.',
         habits=['workaholic', 'gym-regular'], traits=['precise', 'competitive', 'loyal'],
         life=['Top of the rowing leaderboard in the gym, and taped the leaderboard there himself.', 'Keeps the waiting list for the good records.', 'Has two messages from home waiting.']),
    dict(id='sato', name='Dr. Imra Sato', story=True, rank='chief', dept='survey', role='Head of Survey', shift='day', bed='2-V', job='survey',
         looks=dict(skin=0, hair='long', hairColor='grey', height=.94, build='slim', acc=['glasses']),
         bio='Head of Survey. Her lab, her rules, her terrible tea.',
         habits=['workaholic', 'quiet-corner', 'tea-break'], traits=['brilliant', 'absent-minded', 'stubborn'],
         life=['Brews a tea nobody else will drink.', 'Labels every sample in the specimen store in her own handwriting.']),
    dict(id='holt', name='Chief Bram Holt', story=True, rank='chief', dept='watch', role='Head of Watch', shift='day', bed='2-T', job='watch',
         looks=dict(skin=2, hair='bald', hairColor='grey', height=1.05, build='broad', acc=['moustache']),
         bio='Head of Watch. Does not trust the Veyli, and says so.',
         habits=['early-riser', 'late-diner'], traits=['suspicious', 'dependable', 'gruff'],
         life=['Asked for the cabin next door to the Envoy\'s.', 'Only his deputy can make him laugh.']),
    dict(id='calder', name='Chief Ines Calder', story=True, provisional=True, rank='chief', dept='works', role='Head of Works', shift='day', bed='2-O', job='works',
         looks=dict(skin=3, hair='short', hairColor='grey', height=1.02, build='average', acc=['glasses']),
         bio='Head of Works. Remembers every repair you got wrong, and every one you got right.',
         habits=['early-riser', 'workaholic', 'tea-break'], traits=['exacting', 'fair', 'dry'],
         life=['Runs the job board from the glass office on Deck 5, and certifies every Works tech aboard.', 'Keeps a battered toolbox that belonged to her first chief.']),
    dict(id='pell', name='Pell Okafor', story=True, rank='junior', dept='works', role='Works technician', shift='day', bed='4-B2-2', job='works',
         looks=dict(skin=5, hair='buzz', hairColor='black', height=1.1, build='broad', acc=['beard']),
         bio='Works, like you, and two years ahead. Can fix anything except his sleep schedule.',
         habits=['late-sleeper', 'tea-break', 'gym-regular'], traits=['easygoing', 'handy', 'chatty'],
         life=['Talks in his sleep, mostly about engines.', 'Has three messages from his mum waiting.']),
    dict(id='rina', name='Rina Deshi', story=True, rank='junior', dept='infirmary', role='Infirmary aide', shift='day', bed='4-B2-3', job='infirmary',
         looks=dict(skin=3, hair='curls', hairColor='black', height=.95, build='average', acc=['earrings', 'headband']),
         bio='Dry humour, steady hands, undefeated at Tiles.',
         habits=['common-room', 'calls-home'], traits=['dry humour', 'steady', 'competitive'],
         life=['Uses a stack of medical journals as a pillow.', 'Has a message from her sister waiting.', 'Undefeated at Tiles in the junior common room.']),
    dict(id='brennan', name='Chef Auda Brennan', story=True, rank='officer', dept='galley', role='Chef, galley and mess hall', shift='day', bed='4-05', job='galley',
         looks=dict(skin=1, hair='bun', hairColor='auburn', height=.92, build='broad', acc=['apron', 'glasses']),
         bio='Runs the galley and mess hall. Cooks by ear, and sends biscuits down for the juniors.',
         habits=['early-riser', 'early-to-bed'], traits=['warm', 'fierce in her kitchen', 'generous'],
         life=['Furious whenever the cold store runs warm.', 'Sends biscuits down to the junior wing.']),
    dict(id='tomas', name='Tomas Lind', story=True, rank='junior', dept='watch', role='Watch rating', shift='day', bed='4-B1-1', job='watch',
         looks=dict(skin=0, hair='ponytail', hairColor='blonde', height=1.0, build='slim', acc=[]),
         bio='New to Watch, and your bunkmate. Still learning where everything is.',
         habits=['common-room', 'window-seat'], traits=['earnest', 'curious', 'a little lost'],
         life=['Taped a star map to the underside of the top bunk.', 'Joined the Wren a week before you did.']),
    # provisional: the Infirmary Chief and the six senior officers (placeholders by role until now)
    dict(id='nandakumar', name='Dr. Priya Nandakumar', provisional=True, rank='chief', dept='infirmary', role='Head of Infirmary', shift='day', bed='2-I', job='infirmary',
         looks=dict(skin=4, hair='long', hairColor='black', height=.97, build='slim', acc=['glasses', 'earrings']),
         bio='Head of Infirmary. Says "drink some water" in a way that ends the argument.',
         habits=['early-riser', 'garden-lover'], traits=['calm', 'brisk', 'kind'],
         life=['Puts a sign on her door: IF YOU ARE BLEEDING, DECK 3.', 'Grows chillies in a corner of the garden.']),
    dict(id='kowalczyk', name='Anja Kowalczyk', provisional=True, rank='senior', dept='command', role='Second Officer', shift='night', bed='2-S', job='command',
         looks=dict(skin=0, hair='ponytail', hairColor='brown', height=1.04, build='average', acc=[]),
         bio='Second Officer. Runs the bridge at night, when the ship is hers.',
         habits=['night-owl', 'quiet-corner'], traits=['steady', 'private', 'wry'],
         life=['Third in command, and first to be woken.', 'Reads old paper novels on the bridge during quiet nights.']),
    dict(id='raman', name='Dev Raman', provisional=True, rank='senior', dept='helm', role='Senior Helm Officer', shift='day', bed='2-H', job='helm',
         looks=dict(skin=3, hair='short', hairColor='black', height=1.06, build='slim', acc=['moustache']),
         bio='Senior Helm Officer. Flies the Wren like it might spill.',
         habits=['early-riser', 'window-seat'], traits=['careful', 'proud', 'gentle'],
         life=['Keeps a model of the Wren on the shelf by his door.', 'Has flown survey ships for twenty years.']),
    dict(id='ferreira', name='Lucia Ferreira', provisional=True, rank='senior', dept='comms', role='Comms Chief', shift='day', bed='2-R', job='comms',
         looks=dict(skin=2, hair='curls', hairColor='dark', height=.98, build='average', acc=['earrings']),
         bio='Comms Chief. Every message home passes through her hands, and she never reads them.',
         habits=['lounge-regular', 'calls-home'], traits=['sociable', 'discreet', 'quick'],
         life=['Hangs a headset on her door handle, just in case.', 'Speaks four languages and some Veyli.']),
    dict(id='oduya', name='Matthias Oduya', provisional=True, rank='senior', dept='infirmary', role='Ship\'s Counsellor', shift='day', bed='2-N', job='infirmary',
         looks=dict(skin=5, hair='short', hairColor='grey', height=1.07, build='broad', acc=['glasses', 'beard']),
         bio='Ship\'s Counsellor. Seventy-five people a long way from home keep him busy.',
         habits=['garden-lover', 'lingers-at-meals'], traits=['warm', 'perceptive', 'unhurried'],
         life=['Keeps office hours on Deck 3 and a bowl of sweets on his desk.', 'Knows everyone\'s birthday.']),
    dict(id='mensah', name='Kofi Mensah', provisional=True, rank='senior', dept='watch', role='Senior Watch Officer', shift='night', bed='2-G', job='watch',
         looks=dict(skin=5, hair='buzz', hairColor='black', height=1.1, build='broad', acc=[]),
         bio='Senior Watch Officer. Holt\'s deputy, in charge of the Watch at night.',
         habits=['night-owl', 'gym-regular'], traits=['easy laugh', 'watchful', 'patient'],
         life=['The only one who can make Holt laugh.', 'Walks the whole ship once a night, deck by deck.']),
    dict(id='mori', name='Hana Mori', provisional=True, rank='senior', dept='survey', role='Deputy Survey Chief', shift='day', bed='2-D', job='survey',
         looks=dict(skin=0, hair='bun', hairColor='black', height=.93, build='slim', acc=['glasses']),
         bio='Deputy Survey Chief. Runs the labs while Sato runs everyone.',
         habits=['workaholic', 'quiet-corner'], traits=['organised', 'shy', 'meticulous'],
         life=['Tapes a star chart over her nameplate.', 'Maps the frontier one survey at a time, in the chart room.']),
]

# the player: one of the 75 (a Works junior), kept apart from ROSTER because the player isn't scheduled
PLAYER = dict(id='you', name='You', player=True, rank='junior', dept='works', role='Works technician (you)', shift='day', bed='4-B1-4', job='works',
              rota={'offDays': [5, 6]}, looks=dict(skin=2, hair='short', hairColor='dark', height=1.05, build='average', acc=[]),
              bio='New aboard, a junior technician in Works. Your bunk is in Bunk 1, with Tomas.', habits=[], traits=[], life=[])

GUESTS = [
    dict(id='saruth', name='Envoy Saruth', story=True, rank='guest', dept='guest', role='Veyli Envoy (guest)', shift='day', bed='2-E', job=None,
         looks=dict(skin=2, hair='long', hairColor='white', height=1.09, build='slim', acc=['headband']),
         bio='The Veyli Envoy, guest of the Concord. Courteous, ritual-minded, and hard to read.',
         habits=['quiet-corner', 'garden-lover'], traits=['formal', 'observant', 'patient'],
         life=['Keeps a knot of Veyli cord on the door handle: visitors by invitation only.', 'Takes tea at a low table, kneeling, at the same hour every day.']),
]

# ---------------------------------------------------------------- the generated crew: who's needed
# (dept, rank, role, job, count, night count)
NEED = [
    ('helm', 'officer', 'Helm officer', 'helm', 2, 1),
    ('command', 'officer', 'Operations officer', 'ops', 1, 0),
    ('comms', 'officer', 'Comms officer', 'comms-bridge', 1, 1),
    ('comms', 'officer', 'Comms officer', 'comms', 1, 0),
    ('works', 'officer', 'Works systems officer', 'works', 2, 1),
    ('works', 'officer', 'Engine officer', 'engine', 2, 1),
    ('watch', 'officer', 'Watch officer', 'watch', 2, 1),
    ('survey', 'officer', 'Survey officer', 'survey', 3, 1),
    ('infirmary', 'officer', 'Doctor', 'infirmary', 1, 1),
    ('helm', 'junior', 'Helm rating', 'helm', 2, 1),
    ('comms', 'junior', 'Comms rating', 'comms', 2, 0),
    ('works', 'junior', 'Works technician', 'works', 15, 0),
    ('works', 'junior', 'Engine technician', 'engine', 4, 2),
    ('watch', 'junior', 'Watch rating', 'watch', 7, 1),
    ('survey', 'junior', 'Survey assistant', 'survey', 7, 1),
    ('infirmary', 'junior', 'Infirmary aide', 'infirmary', 2, 0),
    ('galley', 'junior', 'Galley hand', 'galley', 5, 0),
]
# night juniors: helm 1, engine 2, watch 1, survey 1 = 5, plus one more below (infirmary has Rina on days, so
# the sixth night junior is a second watch rating); officers on nights: helm, comms, works, engine, watch, survey, doctor = 7
NEED = [(d, r, ro, j, n, (nt + 1 if (r == 'junior' and d == 'watch') else nt)) for d, r, ro, j, n, nt in NEED]

FIRST = ['Ada', 'Aiko', 'Alejandro', 'Amara', 'Ana', 'Anders', 'Arjun', 'Asha', 'Bea', 'Benedikt', 'Bilal', 'Bo', 'Carmen', 'Chidi', 'Chloe',
         'Dara', 'Davi', 'Elif', 'Emeka', 'Erik', 'Esme', 'Farah', 'Felix', 'Femi', 'Gabriel', 'Greta', 'Hamid', 'Hugo', 'Ilse', 'Imani',
         'Isak', 'Ivo', 'Jae', 'Jalen', 'Jun', 'Kai', 'Kalani', 'Karin', 'Kemal', 'Lars', 'Leila', 'Lena', 'Luca', 'Lukas', 'Maeve',
         'Malik', 'Marta', 'Mateo', 'Mei', 'Mira', 'Nadia', 'Nils', 'Noor', 'Oisin', 'Olu', 'Omar', 'Oona', 'Orla', 'Pavel', 'Petra',
         'Quinn', 'Rafael', 'Ravi', 'Rosa', 'Ruth', 'Saad', 'Sana', 'Sefa', 'Signe', 'Sol', 'Sven', 'Tamsin', 'Tariq', 'Thea', 'Theo',
         'Tove', 'Uma', 'Vera', 'Wen', 'Xavi', 'Yara', 'Yusuf', 'Zainab', 'Zeke', 'Zofia']
LAST = ['Abara', 'Achterberg', 'Alvarez', 'Amadi', 'Bakshi', 'Barros', 'Bergstrom', 'Bianchi', 'Castell', 'Chen', 'Cruz', 'Dahl', 'Dlamini',
        'Eklund', 'Esposito', 'Farouk', 'Fonseca', 'Garcia', 'Grieve', 'Haddad', 'Halloran', 'Hart', 'Holloway', 'Ibarra', 'Ishikawa',
        'Janssen', 'Jovanovic', 'Kaur', 'Keane', 'Kim', 'Kovac', 'Lachance', 'Larsen', 'Lemaire', 'Lindqvist', 'Mabaso', 'Madsen', 'Marsh',
        'Mbeki', 'Moreau', 'Nakamura', 'Navarro', 'Nyberg', 'Obi', "O'Neill", 'Ortiz', 'Park', 'Petrov', 'Quist', 'Rahman', 'Reyes', 'Rossi',
        'Salo', 'Santos', 'Shah', 'Silva', 'Soto', 'Strand', 'Takahashi', 'Teague', 'Torres', 'Tran', 'Ueda', 'Vasquez', 'Varga', 'Volkov',
        'Wainwright', 'Walsh', 'Yilmaz', 'Yoon', 'Zamora', 'Zielinski']
TRAITS = ['cheerful', 'quiet', 'meticulous', 'restless', 'dry humour', 'shy', 'chatty', 'stubborn', 'thoughtful', 'easygoing', 'ambitious',
          'kind', 'nervous', 'proud', 'curious', 'practical', 'dreamy', 'blunt', 'patient', 'competitive', 'gentle', 'sharp-eyed',
          'forgetful', 'reliable', 'sarcastic', 'optimistic', 'homesick', 'tidy', 'messy', 'loyal', 'playful', 'serious']
PLACES = ['Kesh', 'Port Halloran', 'the Tevan belt', 'Marra Station', 'Lisk', 'New Aberdeen', 'Coriel', 'Hesper Dock', 'the Ostrander colonies', 'Valo']
LIFE = [
    'A sister on {p} who sends recipes.', 'Grew up on {p}, and misses the rain.', 'Writes letters home to {p} every rest day, on paper.',
    'Keeps a cactus called Gerald on the windowsill.', 'Is learning the guitar, badly.', 'Knits scarves for anyone who stands still long enough.',
    'Collects pressed flowers from the garden.', 'Has a cat back home on {p}, and talks about it a lot.', 'Is saving up for a boat on {p}.',
    'Bakes on rest days, if Brennan allows it.', 'Paints tiny portraits of the crew.', 'Keeps a journal of every star they have seen.',
    'Is training for the gym\'s rowing leaderboard.', 'Plays Tiles, and loses gracefully.', 'Sings in the shower; the whole washroom knows.',
    'Has a twin on another survey ship.', 'Reads mystery novels and guesses the ending too early.', 'Grows herbs for the galley.',
    'Is quietly in charge of the lost-property box.', 'Fixes everyone\'s broken headphones.', 'Collects old maps of {p}.',
    'Is learning Veyli from a phrasebook.', 'Has a parent who served on the Wren years ago.', 'Tells terrible jokes at breakfast.',
    'Makes a playlist for every week of the tour.', 'Keeps a tin of good biscuits and tells no one.', 'Writes poetry and shows nobody.',
    'Is the best at fixing the coffee machine.', 'Wants to be a Works chief one day.', 'Sends voice messages to a grandmother on {p}.',
    'Climbs the garden\'s big tree when nobody is looking.', 'Keeps fish back home on {p}.', 'Ran a market stall on {p} before joining up.',
    'Got married just before the tour and counts the days.', 'Draws comics about life aboard and pins them in the common room.',
    'Is secretly afraid of the lift.', 'Knows the lyrics to every song in the record cabinet.', 'Brought a telescope from home.',
]
BIOS = {
    'Helm officer': ['Flies the night watch with one hand on the helm and one on a cup of tea.', 'Can feel a drift in the Wren\'s course before the console shows it.', 'Learned to fly in shuttles and never quite got over the size of the Wren.'],
    'Operations officer': ['Keeps the bridge\'s boards honest, one status light at a time.'],
    'Comms officer': ['Hears every voice on the ship\'s channels, and remembers most of them.', 'Can tune a signal out of static like picking a lock.'],
    'Works systems officer': ['Keeps the Works bay\'s day running, and the job board tidy.', 'Traces faults through three decks before breakfast.'],
    'Engine officer': ['Happiest in the engine room, where the coils hum.', 'Knows the drive coils\' moods better than anyone\'s.'],
    'Watch officer': ['Runs the Watch rota, and knows who is where.', 'Calm in a crisis, fussy about paperwork.'],
    'Survey officer': ['Lives for the next sensor sweep.', 'Can name every star in the chart room, and argues about the rest.', 'Runs the sample lab like a kitchen.'],
    'Doctor': ['Night doctor. Steady hands and a soft voice at three in the morning.'],
    'Helm rating': ['Learning the helm one watch at a time.', 'Plots courses for fun on rest days.'],
    'Comms rating': ['Sorts the ship\'s messages, and sneaks a look at the gossip.', 'Young, quick and always wearing a headset.'],
    'Works technician': ['Fixes lamps, ovens and washers, and grumbles about all three.', 'New to Works, eager, and already covered in grease.', 'A steady pair of hands on the job board.', 'Good with filters, bad with mornings.', 'Can strip a scrubber in ten minutes flat.'],
    'Engine technician': ['Keeps the engine room clean enough to eat in.', 'Tends the coils on the long engine watch.'],
    'Watch rating': ['Walks the decks and knows every door.', 'Learning the Watch from Holt, one lecture at a time.', 'Friendly on patrol, firm at the airlock.'],
    'Survey assistant': ['Carries samples and dreams of naming a star.', 'Runs the lab scanners and labels everything twice.'],
    'Infirmary aide': ['Changes the infirmary beds and knows everyone\'s blood type.', 'Gentle, efficient and never out of plasters.'],
    'Galley hand': ['Chops, stirs and washes up under Brennan\'s eye.', 'Runs the serving line at breakfast with a grin.', 'Can carry six trays at once.'],
}
JUNIOR_HABITS = list(HABITS)
OTHER_HABITS = [h for h in HABITS if h != 'common-room']

def looks():
    return dict(skin=R.randrange(6), hair=R.choice(['ponytail', 'short', 'bun', 'curls', 'buzz', 'long', 'bald', 'short', 'short']),
                hairColor=R.choice(['black', 'dark', 'brown', 'brown', 'auburn', 'blonde', 'grey', 'black', 'dark', 'teal'] if R.random() < .5 else ['black', 'dark', 'brown', 'auburn', 'blonde']),
                height=round(R.uniform(.9, 1.1), 2), build=R.choice(['slim', 'average', 'average', 'broad']),
                acc=sorted(R.sample(['glasses', 'beard', 'moustache', 'earrings', 'headband'], R.choice([0, 0, 1, 1, 2]))))

DROPPED = []

def main():
    used_names = {p['name'].split()[-1] for p in STORY + GUESTS}
    used_first = {p['name'].split()[-2] if len(p['name'].split()) > 1 else '' for p in STORY}
    crew = [dict(p) for p in STORY]
    for d, r, ro, j, n, nt in NEED:
        for k in range(n):
            while True:
                f, l = R.choice(FIRST), R.choice(LAST)
                if l not in used_names and f not in used_first: break
            used_names.add(l); used_first.add(f)
            lk = looks()
            if lk['hair'] == 'bald' and R.random() < .5: lk['hair'] = 'buzz'
            pool = JUNIOR_HABITS if r == 'junior' else OTHER_HABITS
            hab = R.sample(pool, R.choice([1, 2, 2, 3]))
            if 'early-riser' in hab and 'late-sleeper' in hab: hab.remove('late-sleeper')
            if 'early-to-bed' in hab and 'night-owl' in hab: hab.remove('night-owl')
            pid = (l.lower().replace("'", '') + '-' + f.lower())
            crew.append(dict(id=pid, name=f + ' ' + l, rank=r, dept=d, role=ro, shift='night' if k < nt else 'day', job=j, looks=lk,
                             bio=R.choice(BIOS[ro]), habits=hab, traits=R.sample(TRAITS, 2),
                             life=[s.replace('{p}', R.choice(PLACES)) for s in R.sample(LIFE, 2)]))
    # ---- beds
    officers = [p for p in crew if p['rank'] == 'officer' and not p.get('bed')]
    window = ['4-06', '4-09', '4-10', '4-13', '4-14', '4-17', '4-18', '4-21', '4-22']        # 4-05 is Brennan's
    inner = ['4-11', '4-12', '4-15', '4-16', '4-19', '4-20']
    for p in sorted(officers, key=lambda p: p['shift'] == 'night'):                             # night officers take the quiet inner cabins
        p['bed'] = (window if (p['shift'] == 'day' and window) or not inner else inner).pop(0)
    juniors = [p for p in crew if p['rank'] == 'junior' and not p.get('bed')]
    night = [p for p in juniors if p['shift'] == 'night']
    day = [p for p in juniors if p['shift'] == 'day']
    assert len(night) == 6, len(night)
    for k, p in enumerate(night): p['bed'] = f'4-B8-{k + 1}'
    berths = [f'4-B1-{b}' for b in (3, 4, 5, 6)] + [f'4-B2-{b}' for b in (1, 4, 5, 6)] + [f'4-B{r}-{b}' for r in range(3, 8) for b in range(1, 7)]
    day.sort(key=lambda p: (p['dept'], p['id']))                                                 # bunk with your own department, roughly
    assert len(day) == len(berths), (len(day), len(berths))
    for p, b in zip(day, berths): p['bed'] = b
    # ---- days off: two in a row, staggered round the week, and within each department so it's never empty
    pairs = [[d, (d + 1) % 7] for d in range(7)]
    k = 0
    for dept in ['command', 'helm', 'comms', 'works', 'galley', 'watch', 'survey', 'infirmary']:
        for p in [p for p in crew if p['dept'] == dept]:
            p['rota'] = {'offDays': pairs[k % 7]}; k += 1
    for p in GUESTS: p['rota'] = {'offDays': []}
    # ---- the player is one of the 47 juniors, so the last generated Works technician makes way. Beds and days off were
    # given out first, so nobody else's change; whoever had 4-B1-6 takes the freed berth, leaving 4-B1-6 empty in your room
    drop = [p for p in crew if p['role'] == 'Works technician' and not p.get('story')][-1]
    crew.remove(drop); DROPPED.append(drop['name'])
    for p in crew:
        if p['bed'] == '4-B1-6': p['bed'] = drop['bed']
    # Bunk 1's furniture text puts you in the top berth of the second bunk (4-B1-4: you lost the coin toss), so whoever
    # was given that berth moves to 4-B1-2, the top berth of the first bunk, above Tomas and under his star map
    for p in crew:
        if p['bed'] == '4-B1-4': p['bed'] = '4-B1-2'
    # ---- work places, seeds, uniform
    out = []
    for p in crew + GUESTS + [PLAYER]:
        deck, place = WORK[p['job']] if p['job'] else (None, None)
        e = dict(id=p['id'], name=p['name'])
        if p.get('story'): e['story'] = True
        if p.get('provisional'): e['provisional'] = True
        if p.get('player'): e['player'] = True
        e.update(rank=p['rank'], dept=p['dept'], uniform=UNIFORM.get(p['dept']), role=p['role'], shift=p['shift'], rota=p['rota'], bed=p['bed'],
                 work=dict(deck=deck, place=place) if deck else None, habits=p['habits'], traits=p['traits'], looks=p['looks'],
                 bio=p['bio'], life=p['life'], seed=seed_of(p['id']))
        out.append(e)
    ids = [p['id'] for p in out]
    assert len(ids) == len(set(ids)), 'duplicate ids'
    beds = [p['bed'] for p in out]
    assert len(beds) == len(set(beds)), 'two people in one bed'
    return out

def js(entries):
    return '\n'.join('  ' + json.dumps(e, ensure_ascii=False, separators=(', ', ': ')) + ',' for e in entries)

# ---------------------------------------------------------------- the readable page
GROUPS = [('command', 'Command', 'The bridge: the Captain, the Executive Officer and the officers who run the ship.'),
          ('helm', 'Helm', 'They fly the Wren, from the helm on the bridge.'),
          ('comms', 'Comms', 'Every message in and out of the ship, from the comms room on Deck 2 and the bridge.'),
          ('works', 'Works', 'Your department: they keep every machine running, from the Works bay on Deck 5 and the engine room on Deck 6.'),
          ('watch', 'Watch', 'Safety, patrols, docking and keeping the peace, from the Watch office on Deck 2.'),
          ('survey', 'Survey', 'Sensors, labs, samples and charting, in the Survey labs on Deck 2.'),
          ('infirmary', 'Infirmary', 'Crew health and rest, in the infirmary on Deck 3.'),
          ('galley', 'Galley', 'Two meals a day for seventy-five people, in the galley and mess hall on Deck 3.'),
          ('guest', 'Guests', 'Not crew: visitors who live aboard.')]
RANK_ORDER = ['captain', 'xo', 'chief', 'senior', 'officer', 'junior', 'guest']
RANK_WORDS = {'captain': 'Captain', 'xo': 'Executive Officer', 'chief': 'Department Chief', 'senior': 'Senior Officer', 'officer': 'Officer', 'junior': 'Junior Officer', 'guest': 'Guest'}
UNI_COL = {'command': '#b4453f', 'works': '#d6a53a', 'watch': '#d6a53a', 'survey': '#3f9a92', 'infirmary': '#3f9a92', None: '#8a8f9a'}
DECK2_ROOM = {'C': "the Captain's quarters", 'E': "the Envoy's guest cabin"}

def bed_words(b):
    if b.startswith('4-B'):
        room, berth = b[3:].split('-')
        return f'Deck 4, Bunk {room}, berth {berth}' + (' (the night-shift room)' if room == '8' else '')
    if b.startswith('4-'): return f'Deck 4, officer cabin {b}'
    if b.startswith('2-'): return 'Deck 2, ' + DECK2_ROOM.get(b[2:], 'senior quarters, room ' + b[2:])
    return b

PAGE_HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Starship Cadet: the crew</title>
<style>
:root{--ink:#e8eef0;--muted:#93a6ae;--teal:#4cc3b5;--glass:rgba(13,21,33,.78);--line:rgba(150,200,196,.22)}
*{box-sizing:border-box}
html,body{margin:0;background:#121a27;color:var(--ink);font-family:"Avenir Next","Segoe UI",system-ui,sans-serif}
body{background:radial-gradient(ellipse at 50% 20%,#22304a 0%,#141c2b 60%,#0c111b 100%) fixed}
header,main,.bar{max-width:1100px;margin:0 auto;padding:0 16px}
header{padding-top:16px}
h1{font-size:20px;font-weight:600;margin:0}
.sub{font-size:13.5px;color:var(--muted);margin:6px 0 0;line-height:1.5}
.summary{background:var(--glass);border:1px solid var(--line);border-radius:14px;padding:12px 16px;margin:12px 0;font-size:13.5px;line-height:1.55;color:#cfd9dc}
.bar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:8px}
.bar a{color:#bdeee6;font-size:13px;text-decoration:none;border:1px solid var(--line);border-radius:999px;padding:5px 11px;background:var(--glass)}
.bar input[type=search]{flex:1 1 180px;min-width:0;font:inherit;font-size:13.5px;color:var(--ink);background:var(--glass);border:1px solid var(--line);border-radius:999px;padding:7px 12px}
.bar label{font-size:13px;color:var(--muted)}
h2{font-size:17px;font-weight:600;margin:22px 0 2px}
h2 .n{font-size:12.5px;color:var(--muted);font-weight:400;margin-left:6px}
.blurb{font-size:13px;color:var(--muted);margin:0 0 10px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:10px}
.p{position:relative;background:var(--glass);border:1px solid var(--line);border-radius:12px;padding:10px 12px 10px 26px;font-size:13px;line-height:1.45}
.dot{position:absolute;left:10px;top:15px;width:9px;height:9px;border-radius:50%}
.who b{font-size:14.5px;color:#eef3f1}
.role{display:block;color:var(--muted);font-size:12.5px}
.b{display:inline-block;font-size:11px;border-radius:999px;padding:1px 7px;margin-left:5px;vertical-align:1px;white-space:nowrap}
.b.story{background:rgba(76,195,181,.18);color:#bdeee6;border:1px solid rgba(76,195,181,.5)}
.b.prov{background:rgba(233,196,106,.14);color:#f0d88e;border:1px dashed rgba(233,196,106,.7)}
.b.night{background:rgba(122,143,208,.18);color:#c3cff2;border:1px solid rgba(122,143,208,.5)}
.b.you{background:rgba(214,165,58,.2);color:#f3d58f;border:1px solid rgba(214,165,58,.6)}
.bio{margin:6px 0;color:#dfe7e9}
dl{display:grid;grid-template-columns:1fr 1fr;gap:4px 10px;margin:0}
dt{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}
dd{margin:0;color:#cfd9dc}
.more{margin:7px 0 0;color:var(--muted);font-size:12.5px}
.tr{font-style:italic}
.hide{display:none}
footer{max-width:1100px;margin:24px auto;padding:0 16px;font-size:12px;color:var(--muted)}
</style>
</head>
<body>
<header>
  <h1>The crew of the CSV Wren</h1>
  <p class="sub">Everyone aboard, for Pillar 1 of the Living Ship. Grouped by department, most senior first. Each card shows when they work, their days off, where they sleep and where they work. Names marked <span class="b prov">Provisional name</span> are first ideas and can still change. <span class="b story">Story crew</span> are the hand-written characters. The coloured dot is their uniform: red for command, gold for operations, blue-green for sciences.</p>
'''
PAGE_TAIL = '''<footer>Made by the crew designer from the roster in the game file (section 9). The other crew come from plans/crew-roster-gen.py and are stored in the game as fixed data, so they only change when someone means them to.</footer>
<script>
const q = document.getElementById('q'), nights = document.getElementById('nights');
function filt() {
  const t = q.value.trim().toLowerCase();
  for (const a of document.querySelectorAll('.p')) a.classList.toggle('hide', (t && !a.dataset.text.includes(t)) || (nights.checked && a.dataset.shift !== 'night'));
  for (const s of document.querySelectorAll('.dept')) s.classList.toggle('hide', !s.querySelector('.p:not(.hide)'));
}
q.addEventListener('input', filt); nights.addEventListener('change', filt);
</script>
</body>
</html>
'''

def page(entries):
    e = lambda s: html.escape(str(s))
    from collections import Counter
    crew = [x for x in entries if x['rank'] != 'guest']
    out = [PAGE_HEAD]
    rc = Counter(x['rank'] for x in crew); sc = Counter(x['shift'] for x in crew)
    beds = Counter('d2' if x['bed'].startswith('2-') else 'cab' if not x['bed'].startswith('4-B') else 'bunk' for x in crew)
    out.append('  <div class="summary"><b>%d crew</b>, you included, plus Envoy Saruth as a guest. %d Captain, %d Executive Officer, %d Department Chiefs, %d Senior Officers, %d Officers and %d Junior Officers. '
               '%d work days and %d work nights. Everyone has two days off in a row, staggered round the week so every department always has people on. '
               'Beds: %d in the senior quarters on Deck 2, %d in officers\' cabins on Deck 4 and %d in the junior bunk rooms on Deck 4 (eight rooms of six berths, with one spare berth in Bunk 1).</div>\n</header>\n'
               % (len(crew), rc['captain'], rc['xo'], rc['chief'], rc['senior'], rc['officer'], rc['junior'], sc['day'], sc['night'], beds['d2'], beds['cab'], beds['bunk']))
    out.append('<div class="bar">' + ' '.join('<a href="#%s">%s</a>' % (k, e(t)) for k, t, _ in GROUPS) + '</div>\n')
    out.append('<div class="bar"><input id="q" type="search" placeholder="Find someone: a name, a job, a word" aria-label="Find someone"><label><input id="nights" type="checkbox"> Night shift only</label></div>\n<main>\n')
    for key, title, blurb in GROUPS:
        ppl = sorted([x for x in entries if x['dept'] == key], key=lambda x: (RANK_ORDER.index(x['rank']), not x.get('player'), x['name'].split()[-1]))
        if not ppl: continue
        out.append('<section class="dept" id="%s"><h2>%s <span class="n">%d %s</span></h2><p class="blurb">%s</p><div class="grid">\n' % (key, e(title), len(ppl), 'person' if len(ppl) == 1 else 'people', e(blurb)))
        for x in ppl:
            badges = (' <span class="b you">You</span>' if x.get('player') else '') + (' <span class="b story">Story crew</span>' if x.get('story') else '') + (' <span class="b prov">Provisional name</span>' if x.get('provisional') else '') + \
                     (' <span class="b night">Night shift</span>' if x['shift'] == 'night' else '')
            off = ' and '.join(DAYS[d] for d in x['rota']['offDays']) or 'none'
            work = (WORK_WORDS[x['work']['place']] + ' (Deck %d)' % x['work']['deck']) if x['work'] else 'no ship duties'
            shift = 'Days, 08:00 to 17:00' if x['shift'] == 'day' else 'Nights, 21:00 to 06:00'
            out.append('<article class="p" data-text="%s" data-shift="%s"><i class="dot" style="background:%s"></i>\n'
                       '  <div class="who"><b>%s</b>%s<span class="role">%s%s</span></div>\n'
                       '  <p class="bio">%s</p>\n'
                       '  <dl><div><dt>Shift</dt><dd>%s</dd></div><div><dt>Days off</dt><dd>%s</dd></div><div><dt>Sleeps</dt><dd>%s</dd></div><div><dt>Works</dt><dd>%s</dd></div></dl>\n'
                       '  <p class="more">%s <span class="tr">%s</span></p></article>\n'
                       % (e((x['name'] + ' ' + x['role'] + ' ' + x['bio']).lower()), x['shift'], UNI_COL[x['uniform']], e(x['name']), badges,
                          e(x['role']), (', ' + e(RANK_WORDS[x['rank']])) if RANK_WORDS[x['rank']].lower() not in x['role'].lower() else '', e(x['bio']), shift, off, e(bed_words(x['bed'])), e(work),
                          e(' '.join(x['life'])), e((', '.join(x['traits']).capitalize() + '.') if x['traits'] else '')))
        out.append('</div></section>\n')
    out.append('</main>\n' + PAGE_TAIL)
    return ''.join(out)

if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    entries = main()
    crew = [x for x in entries if x['rank'] != 'guest' and not x.get('player')]; guests = [x for x in entries if x['rank'] == 'guest']
    you = [x for x in entries if x.get('player')][0]
    from collections import Counter
    rc = Counter(x['rank'] for x in crew + [you]); sc = Counter(x['shift'] for x in crew + [you])
    assert len(crew) == 74 and rc == {'captain': 1, 'xo': 1, 'chief': 4, 'senior': 6, 'officer': 16, 'junior': 47}, rc
    assert sc == {'day': 60, 'night': 15}, sc
    block = ('// ---- BEGIN ROSTER (generated by plans/crew-roster-gen.py: fixed data; to change the crew, edit the generator and re-run it) ----\n'
             'const HABITS = ' + json.dumps(HABITS, ensure_ascii=False, indent=2) + ';\n'
             'const ROSTER = [\n' + js(crew) + '\n];\n'
             'const ROSTER_GUESTS = [\n' + js(guests) + '\n];\n'
             'const ROSTER_PLAYER = ' + json.dumps(you, ensure_ascii=False, separators=(', ', ': ')) + ';\n'
             '// ---- END ROSTER ----\n')
    game = os.path.join(here, '..', 'starship-cadet.html'); g = open(game).read()
    a = g.index('// ---- BEGIN ROSTER'); b = g.index('// ---- END ROSTER ----\n') + len('// ---- END ROSTER ----\n')
    open(game, 'w').write(g[:a] + block + g[b:])
    open(os.path.join(here, 'crew-roster.html'), 'w').write(page(entries))
    print('74 crew + you = 75, + %d guest; ranks %s; shifts %s; made way for you: %s. Wrote section 9 of starship-cadet.html and plans/crew-roster.html' % (len(guests), dict(rc), dict(sc), DROPPED))
