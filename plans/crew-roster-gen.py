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
# Story crew and the senior names (approved by the user) are written out by hand below; only the other crew are generated.

import json, random, hashlib, html, os

R = random.Random(20261015)
DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
UNIFORM = {'command': 'command', 'helm': 'command', 'comms': 'command', 'works': 'works', 'galley': 'works', 'store': 'works', 'garden': 'survey',
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
    'works': (5, 'work:works'), 'engine': (6, 'work:engine'), 'store': (3, 'work:store'), 'garden': (3, 'work:garden'),
}
WORK_WORDS = {
    'work:command': 'the bridge', 'work:helm': 'the helm, on the bridge', 'work:ops': 'the ops console, on the bridge',
    'work:comms': 'comms', 'work:watch': 'the Watch office', 'work:survey': 'the Survey labs',
    'work:galley': 'the galley', 'work:infirmary': 'the infirmary', 'work:works': 'the Works bay', 'work:engine': 'the engine room',
    'work:store': 'the crew store',
    'work:garden': 'the hydroponics garden',
}

# ---------------------------------------------------------------- story crew and senior names (by hand)
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
    dict(id='calder', name='Chief Ines Calder', story=True, rank='chief', dept='works', role='Head of Works', shift='day', bed='2-O', job='works',
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
    # the Infirmary Chief and the six senior officers (names approved by the user, 2026-10-16)
    dict(id='nandakumar', name='Dr. Priya Nandakumar', rank='chief', dept='infirmary', role='Head of Infirmary', shift='day', bed='2-I', job='infirmary',
         looks=dict(skin=4, hair='long', hairColor='black', height=.97, build='slim', acc=['glasses', 'earrings']),
         bio='Head of Infirmary. Says "drink some water" in a way that ends the argument.',
         habits=['early-riser', 'garden-lover'], traits=['calm', 'brisk', 'kind'],
         life=['Puts a sign on her door: IF YOU ARE BLEEDING, DECK 3.', 'Grows chillies in a corner of the garden.']),
    dict(id='kowalczyk', name='Anja Kowalczyk', rank='senior', dept='command', role='Second Officer', shift='night', bed='2-S', job='command',
         looks=dict(skin=0, hair='ponytail', hairColor='brown', height=1.04, build='average', acc=[]),
         bio='Second Officer. Runs the bridge at night, when the ship is hers.',
         habits=['night-owl', 'quiet-corner'], traits=['steady', 'private', 'wry'],
         life=['Third in command, and first to be woken.', 'Reads old paper novels on the bridge during quiet nights.']),
    dict(id='raman', name='Dev Raman', rank='senior', dept='helm', role='Senior Helm Officer', shift='day', bed='2-H', job='helm',
         looks=dict(skin=3, hair='short', hairColor='black', height=1.06, build='slim', acc=['moustache']),
         bio='Senior Helm Officer. Flies the Wren like it might spill.',
         habits=['early-riser', 'window-seat'], traits=['careful', 'proud', 'gentle'],
         life=['Keeps a model of the Wren on the shelf by his door.', 'Has flown survey ships for twenty years.']),
    dict(id='ferreira', name='Lucia Ferreira', rank='senior', dept='comms', role='Comms Chief', shift='day', bed='2-R', job='comms',
         looks=dict(skin=2, hair='curls', hairColor='dark', height=.98, build='average', acc=['earrings']),
         bio='Comms Chief. Every message home passes through her hands, and she never reads them.',
         habits=['lounge-regular', 'calls-home'], traits=['sociable', 'discreet', 'quick'],
         life=['Hangs a headset on her door handle, just in case.', 'Speaks four languages and some Veyli.']),
    dict(id='oduya', name='Matthias Oduya', rank='senior', dept='infirmary', role='Ship\'s Counsellor', shift='day', bed='2-N', job='infirmary',
         looks=dict(skin=5, hair='short', hairColor='grey', height=1.07, build='broad', acc=['glasses', 'beard']),
         bio='Ship\'s Counsellor. Seventy-five people a long way from home keep him busy.',
         habits=['garden-lover', 'lingers-at-meals'], traits=['warm', 'perceptive', 'unhurried'],
         life=['Keeps office hours on Deck 3 and a bowl of sweets on his desk.', 'Knows everyone\'s birthday.']),
    dict(id='mensah', name='Kofi Mensah', rank='senior', dept='watch', role='Senior Watch Officer', shift='night', bed='2-G', job='watch',
         looks=dict(skin=5, hair='buzz', hairColor='black', height=1.1, build='broad', acc=[]),
         bio='Senior Watch Officer. Holt\'s deputy, in charge of the Watch at night.',
         habits=['night-owl', 'gym-regular'], traits=['easy laugh', 'watchful', 'patient'],
         life=['The only one who can make Holt laugh.', 'Walks the whole ship once a night, deck by deck.']),
    dict(id='mori', name='Hana Mori', rank='senior', dept='survey', role='Deputy Survey Chief', shift='day', bed='2-D', job='survey',
         looks=dict(skin=0, hair='bun', hairColor='black', height=.93, build='slim', acc=['glasses']),
         bio='Deputy Survey Chief. Runs the labs while Sato runs everyone.',
         habits=['workaholic', 'quiet-corner'], traits=['organised', 'shy', 'meticulous'],
         life=['Tapes a star chart over her nameplate.', 'Maps the frontier one survey at a time, in the chart room.']),
]

# the player: one of the 75 (a Works junior), kept apart from ROSTER because the player isn't scheduled
PLAYER = dict(id='you', name='You', player=True, rank='junior', dept='works', role='Works technician (you)', shift='day', bed='4-B1-4', job='works',
              rota={'offDays': [5, 6]}, looks=dict(skin=2, hair='short', hairColor='dark', height=1.05, build='average', acc=[]),
              bio='New aboard, a junior technician in Works. Your bunk is in Bunk 1, with Tomas.', habits=[], traits=[], life=[])

HAND = {p['id'] for p in STORY}   # written by hand: the habit and birthday streams skip or treat them apart
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
# Pillar 2 (0.16.4): habits for the new activities, one room's regulars each. Added after the two pools above
# and handed out with their own random stream (NEW_R, below), so everything generated before is unchanged
HABITS_P2 = {
    'runner': 'Runs on the gym treadmills on Deck 3, before breakfast or after shift, on most work days.',
    'shopper': 'Browses the crew store on Deck 3 a few times a week, after shift or on rest days, and pays at the till.',
    'musician': 'Plays an instrument in the Deck 4 music room some evenings (`music` is listening; this is playing).',
    'gardener': 'Tends the Deck 3 garden in free time: waters, trims and picks (`garden-lover` sits there; this works it).',
    'bar-regular': 'A drink at the bow lounge bar on Deck 3 most evenings, after dinner.',
    'stargazer': 'Evenings in the Deck 2 observatory at the bow windows, on the observatory-night list.',
}
HABITS.update(HABITS_P2)
# story crew whose life lines already say it; the rest are spread by NEW_R
STORY_P2 = {'marrow': 'musician', 'tomas': 'stargazer', 'mori': 'stargazer', 'nandakumar': 'gardener', 'ferreira': 'bar-regular'}
P2_COUNT = {'runner': 10, 'shopper': 10, 'bar-regular': 8, 'gardener': 5, 'musician': 5, 'stargazer': 4}   # generated crew each
P2_LIKES = {'runner': ['gym-regular', 'early-riser'], 'shopper': ['calls-home', 'common-room'], 'bar-regular': ['lounge-regular', 'night-owl'],
            'gardener': ['garden-lover', 'early-riser'], 'musician': ['music', 'night-owl'], 'stargazer': ['quiet-corner', 'window-seat']}
P2_DISLIKES = {'bar-regular': ['early-to-bed'], 'stargazer': ['early-to-bed'], 'runner': ['late-sleeper']}
NEW_R = random.Random(20261016)
BDAY_R = random.Random(20261017)   # birthdays (0.16.6)
# ---------------------------------------------------------------- habits that change (0.16.7, answers pass row 18)
# A short list per person of plausible habit changes. The sim engineer (section 14, habitWeek) picks who changes
# and when (a few a month), applies one item and logs it in SHIP.habitLog; `why` is shown as it is (the log, Mail,
# the tap line), so it's a whole sentence that names the person. Every item is valid against the person's habits
# here: it adds only what they don't have and drops only what they do, and never makes a clashing pair.
SHIFT_R = random.Random(20261018)
CLASH = [('early-riser', 'late-sleeper'), ('early-to-bed', 'night-owl')]
# the hand-written crew: what their life lines suggest
SHIFTS_HAND = {
    'marrow': [{'add': 'stargazer', 'why': 'Captain Marrow has started coming to observatory night, to see what the juniors see.'}],
    'vance': [{'add': 'runner', 'drop': 'gym-regular', 'why': 'Commander Vance has moved from the rowing machine to the treadmills, to start a new leaderboard.'},
              {'drop': 'workaholic', 'why': 'Commander Vance has started leaving the bridge on time, on the Counsellor\'s advice.'}],
    'sato': [{'add': 'gardener', 'why': 'Dr. Sato has started growing sample plants in the garden, and tends them every evening.'}],
    'holt': [{'add': 'gym-regular', 'why': 'Chief Holt has started training in the gym after shift.'}],
    'calder': [{'drop': 'tea-break', 'why': 'Chief Calder has given up her tea break: there\'s always one more job on the board.'}],
    'pell': [{'add': 'calls-home', 'why': 'Pell has started calling his mum back on rest days.'},
             {'drop': 'late-sleeper', 'why': 'Pell is trying to get up on time, after one too many late starts in the Works bay.'}],
    'rina': [{'add': 'stargazer', 'why': 'Rina has started going up to observatory night with Tomas.'}],
    'brennan': [{'add': 'gardener', 'why': 'Chef Brennan has started picking her own herbs in the garden.'}],
    'tomas': [{'add': 'runner', 'why': 'Tomas has taken up running: Vance talked him into the treadmill.'}],
    'nandakumar': [{'add': 'runner', 'why': 'Dr. Nandakumar has started running before breakfast, and recommends it to everyone.'}],
    'kowalczyk': [{'add': 'stargazer', 'why': 'Anja Kowalczyk has started spending evenings off in the observatory.'}],
    'raman': [{'add': 'musician', 'why': 'Dev Raman has started playing an old guitar in the music room.'}],
    'ferreira': [{'drop': 'bar-regular', 'why': 'Lucia Ferreira is cutting back on the bar, and spending evenings on her Veyli.'}],
    'oduya': [{'add': 'bar-regular', 'why': 'Matthias Oduya has started dropping by the lounge bar, where people talk more freely.'}],
    'mensah': [{'add': 'runner', 'drop': 'gym-regular', 'why': 'Kofi Mensah has swapped the weights for the treadmill.'}],
    'mori': [{'drop': 'workaholic', 'why': 'Hana Mori has stopped working late, now the charts are up to date.'}],
    'saruth': [{'add': 'gardener', 'why': 'Envoy Saruth has asked for a corner of the garden, and tends Veyli seedlings there.'}],
}
# everyone else: swaps (one habit for another), new habits and dropped ones, each a sentence with {f} for the first name
SHIFT_SWAPS = [
    ('gym-regular', 'runner', '{f} has swapped the weights for the treadmill.'),
    ('music', 'musician', '{f} has gone from listening in the music room to playing.'),
    ('garden-lover', 'gardener', '{f} has gone from sitting in the garden to tending it.'),
    ('common-room', 'stargazer', '{f} has swapped Tiles nights for the observatory.'),
    ('bar-regular', 'runner', '{f} has swapped the bar for the treadmill.'),
    ('late-sleeper', 'early-riser', '{f} has turned into an early riser.'),
    ('lounge-regular', 'bar-regular', '{f} has moved from the lounge sofas to the bar.'),
    ('night-owl', 'early-to-bed', '{f} has started going to bed early.'),
    ('skips-breakfast', 'lingers-at-meals', '{f} has started taking time over meals.'),
]
SHIFT_ADDS = {
    'runner': '{f} has taken up running on the treadmills.', 'gym-regular': '{f} has joined the after-shift gym crowd.',
    'shopper': '{f} has started browsing the crew store after shift.', 'musician': '{f} has dusted off an old instrument and plays in the music room now.',
    'gardener': '{f} has started helping out in the garden.', 'bar-regular': '{f} has become a regular at the lounge bar.',
    'stargazer': '{f}\'s name is on the observatory-night list now.', 'early-riser': '{f} has started getting up early.',
    'tea-break': '{f} has started taking a mid-shift tea break.', 'calls-home': '{f} has started calling home more often.',
    'garden-lover': '{f} has found a favourite bench in the garden.', 'lounge-regular': '{f} spends evenings in the bow lounge now.',
    'quiet-corner': '{f} has been looking for quiet corners lately.', 'window-seat': '{f} always heads for a window seat now.',
    'evening-shower': '{f} has switched to showering at night.', 'music': '{f} has started listening in the music room in the evenings.',
    'common-room': '{f} has joined the Tiles nights in the common room.',
}
SHIFT_DROPS = {
    'bar-regular': '{f} is cutting back on the bar.', 'runner': '{f} has given up running for now.',
    'gym-regular': '{f} has stopped going to the gym after shift.', 'late-sleeper': '{f} is trying to get up on time.',
    'night-owl': '{f} has started going to bed on time.', 'skips-breakfast': '{f} has started eating breakfast again.',
    'workaholic': '{f} has stopped staying late at work.', 'common-room': '{f} has drifted away from the common-room crowd.',
    'shopper': '{f} is saving up, and has stopped browsing the store.', 'lounge-regular': '{f} rarely goes to the lounge now.',
    'tea-break': '{f} has stopped taking a tea break.', 'lingers-at-meals': '{f} eats and goes these days.',
}
# the rank line on a door plate (the ranks of design-doc "The crew", as the game's RANK_NAME says them)
PLATE_RANK = {'captain': 'Captain', 'xo': 'Executive Officer', 'chief': 'Department Chief', 'senior': 'Senior Officer',
              'officer': 'Officer', 'guest': 'Veyli Envoy'}
# the gardeners (0.16.11): role, team, days off, hours, hours on other days ([{ days, hours }]: they replace hours
# on those days), bio
GARDENERS = {
    'cruz-tove': ('Senior gardener', 'senior', [5, 6], [[480, 1020]],
                  [{'days': [0, 1], 'hours': [[360, 840]]}, {'days': [2, 3], 'hours': [[780, 1260]]}],
                  'Runs the hydroponics garden, and knows every plant by the week it was sown.'),
    'hart-ravi': ('Gardener', 'early', [0, 1], [[360, 840]], None, 'Waters the garden at first light, before anyone else is up.'),
    "oneill-imani": ('Gardener', 'late', [2, 3], [[780, 1260]], None, 'Tends the garden into the evening, and picks the galley\'s herbs for the next day.'),
}
# the galley staff: team and days off (0 = Monday)
GALLEY_TEAMS = {'brennan': ('chef', [4, 5]), 'varga-tariq': ('early', [0, 1]), 'haddad-tamsin': ('early', [2, 3]),
                'dlamini-lukas': ('early', [1, 2]), 'walsh-esme': ('late', [5, 6]), 'madsen-ivo': ('late', [0, 1])}
# the storekeepers: work hours ([start, end] in ship minutes; they replace the shift's), days off, bio
STOREKEEPERS = [([[480, 870]], [0, 1], 'Opens the crew store in the morning and knows who has run out of what.'),
                ([[870, 1260]], [3, 4], 'Keeps the crew store open into the evening, and the ledger in perfect order.')]

def looks():
    return dict(skin=R.randrange(6), hair=R.choice(['ponytail', 'short', 'bun', 'curls', 'buzz', 'long', 'bald', 'short', 'short']),
                hairColor=R.choice(['black', 'dark', 'brown', 'brown', 'auburn', 'blonde', 'grey', 'black', 'dark', 'teal'] if R.random() < .5 else ['black', 'dark', 'brown', 'auburn', 'blonde']),
                height=round(R.uniform(.9, 1.1), 2), build=R.choice(['slim', 'average', 'average', 'broad']),
                acc=sorted(R.sample(['glasses', 'beard', 'moustache', 'earrings', 'headband'], R.choice([0, 0, 1, 1, 2]))))

# ---------------------------------------------------------------- what the story crew tell you (0.16.8-0.16.9, Pillar 3)
# about: [{ tier, topic, text }]: things a story crew member tells you as you get to know them, for the social engineer's
# chat lines ("Ask about...") and the Crew app's "what you know". tier is section 20's relationship tier (0 stranger,
# 1 acquaintance, 2 colleague, 3 friend, 4 close friend, kept for a real confidence); topic is home, work, hobby, past or
# secret. Third person, one sentence each; they add to the bio and life lines and never contradict them
ABOUT = {
    'tomas': [(0, 'work', 'Joined the Wren a week before you did, and still takes the long way round Deck 2.'),
              (0, 'work', 'Thinks the Watch office has the best view of the lift, and therefore of everyone.'),
              (1, 'home', 'Grew up on a farm moon where the sky was always the same grey.'),
              (1, 'hobby', 'Taped the star map up so the first thing he sees each morning is somewhere he has never been.'),
              (2, 'work', 'Failed the Watch exam once before passing, and hasn\'t told Chief Holt.'),
              (3, 'home', 'Writes to his little brother every week and pretends the job is more exciting than it is.'),
              (4, 'secret', 'Signed up because he was afraid of staying home for the rest of his life.')],
    'pell': [(0, 'work', 'Has been in Works two years, and knows which panel on Deck 5 sticks.'),
             (0, 'hobby', 'Can sleep anywhere, any time, except at night.'),
             (1, 'hobby', 'Keeps a tin of spare screws from every ship he has fixed something on.'),
             (1, 'home', 'His mum sends the same three messages every week: eat, sleep, call.'),
             (2, 'work', 'Wants Chief Calder\'s certification more than anything, and is scared of the practical.'),
             (3, 'past', 'Taught himself engines from an old manual he found in a scrapyard.'),
             (4, 'secret', 'Nearly left the Wren in his first month, and is glad every day that he didn\'t.')],
    'rina': [(0, 'work', 'Works in the infirmary, and will tell you to drink some water.'),
             (0, 'hobby', 'Has never lost a game of Tiles in the junior common room, and keeps count.'),
             (1, 'work', 'Studies for her medical exams in the evenings, with the journals she uses as a pillow.'),
             (1, 'home', 'Her sister is a doctor on a station, and they argue about everything by message.'),
             (2, 'work', 'Wants to be a ship\'s doctor one day, and quietly thinks she\'d be good at it.'),
             (3, 'past', 'Learnt to play Tiles from her grandmother, who cheated.'),
             (4, 'secret', 'Joined the Wren after a hard year at home, and the routine helped more than she expected.')],
    'marrow': [(0, 'work', 'Asks every new junior one question about the ship, and remembers the answer.'),
               (1, 'hobby', 'Learnt the piano as a girl and took it up again on her first command.'),
               (3, 'home', 'Has a daughter at the Concord academy who doesn\'t write often enough.'),
               (4, 'secret', 'Thinks about retiring, and can\'t imagine anyone else in the ready room.')],
    'vance': [(0, 'work', 'Has read the ship\'s regulations cover to cover, twice.'),
              (1, 'hobby', 'Rowed for his academy, and still checks the gym leaderboard every morning.'),
              (2, 'work', 'Keeps a list of every junior he has recommended for promotion.'),
              (4, 'past', 'Was a junior who broke every rule once, which is why he knows them all.')],
    'sato': [(0, 'hobby', 'Will explain the tea to anyone, at length.'),
             (1, 'work', 'Named three comets, and pretends not to care about the third.'),
             (2, 'past', 'Turned down a university post to stay on the frontier.'),
             (4, 'secret', 'Worries the survey she is proudest of was mostly luck.')],
    'holt': [(0, 'work', 'Walks every deck before breakfast, the long way.'),
             (1, 'past', 'Served on a border patrol before the Wren, and doesn\'t talk about it much.'),
             (3, 'past', 'Distrusts the Veyli because of one bad day years ago, and knows it isn\'t fair.'),
             (4, 'secret', 'Asked for the cabin next to the Envoy\'s so he could keep an eye out, and has started to like the Envoy.')],
    'calder': [(0, 'work', 'Can tell you what\'s wrong with a fan by the sound.'),
               (1, 'past', 'Started as a junior in a shipyard, sweeping up swarf.'),
               (2, 'work', 'Keeps a list of every Works tech she has certified, with a note on each.'),
               (4, 'past', 'The toolbox was her first chief\'s, who taught her everything and never said well done.')],
    'brennan': [(0, 'work', 'Cooks by ear: she listens to the pans.'),
                (1, 'past', 'Ran a restaurant on Port Halloran before the Wren.'),
                (2, 'work', 'Keeps a book of every crew member\'s favourite dish.'),
                (4, 'secret', 'Left the restaurant after a fire, and finds the galley\'s order comforting.')],
    'saruth': [(0, 'home', 'Takes tea at the same hour every day, and will sometimes invite you.'),
               (1, 'home', 'Ties a new knot in the cord on the cabin door for every month aboard.'),
               (3, 'work', 'Finds humans exhausting and very kind, often at once.'),
               (4, 'secret', 'Was sent to the Wren because no one at home expected the posting to work.')],
}

def looks_with(rng):                               # looks() from another random stream (visitors)
    return dict(skin=rng.randrange(6), hair=rng.choice(['ponytail', 'short', 'bun', 'curls', 'buzz', 'long', 'short']),
                hairColor=rng.choice(['black', 'dark', 'brown', 'brown', 'auburn', 'blonde', 'grey', 'teal']),
                height=round(rng.uniform(.9, 1.1), 2), build=rng.choice(['slim', 'average', 'average', 'broad']),
                acc=sorted(rng.sample(['glasses', 'beard', 'moustache', 'earrings', 'headband'], rng.choice([0, 0, 1, 1, 2]))))

# ---------------------------------------------------------------- visitors (0.16.8, Pillar 3 C8)
# GUESTS: people who stay a while and leave. Inert data: the sim engineer schedules them from GUEST_TEMPLATES
# (section 14), the events engineer sets the day an event guest arrives. Same shape as roster entries (rank 'guest',
# habits, bio, life, seed) plus template, cabin, arrive and leave (ship days of the year, 1-364, like birthdays),
# and spec, ready for crowd.add / makeCharacter. Their own random stream (VIS_R), after everything else.
VIS_R = random.Random(20261019)
# what each kind of visitor does with a day: [deck, place type, weight] as in LEISURE (types with no places are
# skipped); 'cabin' is their own cabin; 'work' is their entry's work place. The sim engineer turns these into days
GUEST_TEMPLATES = {
    'scientist': {'label': 'A visiting scientist or specialist: works by day, the observatory or the lounge in the evening',
                  'day': [['work', 6], [2, 'work:survey', 2]], 'evening': [[2, 'observatory', 3], [3, 'lounge-seat', 2], [3, 'bar', 1], ['cabin', 2]],
                  'meals': 'mess', 'wake': 390, 'bed': 1350},
    'delegate': {'label': 'A member of a delegation: tours, formal dinners (the event decides), the observation room, their cabin',
                 'day': [['cabin', 3], [1, 'common-room', 2], [3, 'garden', 2], [2, 'observatory', 1]], 'evening': [['cabin', 3], [3, 'lounge-seat', 1]],
                 'meals': 'mess', 'formal': True, 'wake': 360, 'bed': 1320},
    'passenger': {'label': 'A passenger or a transfer waiting for their ship: the lounge, the mess, the garden, the store',
                  'day': [[3, 'lounge-seat', 3], [3, 'garden', 2], [3, 'shop', 1], [3, 'bench', 1], ['cabin', 1]],
                  'evening': [[3, 'lounge-seat', 3], [3, 'bar', 2], [2, 'observatory', 1], ['cabin', 1]], 'meals': 'mess', 'wake': 450, 'bed': 1380},
    'survivor': {'label': 'Rescued: the infirmary for the first days, then rest, the garden and the mess',
                 'first': 2, 'firstDay': [[3, 'work:infirmary', 1]], 'day': [['cabin', 3], [3, 'garden', 2], [3, 'lounge-seat', 1]],
                 'evening': [['cabin', 3], [3, 'lounge-seat', 1]], 'meals': 'mess', 'wake': 480, 'bed': 1260},
}
# the guest cabins: Deck 2's visitors' suite (2-B) and second visitors' cabin (2-U, for event visitors); Deck 4's
# six guest cabins. Event guests use 2-U and 4-01..4-04 (one event at a time), everyday visitors 4-07 and 4-08 by turns,
# so the two never meet
EVERYDAY_CABINS = ['4-07', '4-08']
# clothes: specialists wear their service's uniform (spec.dept a DEPT key); everyone else is spec.dept 'civilian' with
# spec.outfit, the colour a civilian outfit should be. makeCharacter has no civilian outfit yet (unknown depts fall back to
# the survey colour), so that's for whoever draws them
VEYLI_LOOKS = lambda: dict(skin=VIS_R.choice([1, 2, 3]), hair=VIS_R.choice(['long', 'bun', 'ponytail']), hairColor=VIS_R.choice(['white', 'teal', 'grey']),
                           height=round(VIS_R.uniform(1.04, 1.12), 2), build='slim', acc=['headband'])
EVENT_GUESTS = [
    # the diplomatic visit: a Veyli delegation of four; the leader on Deck 2, the others on Deck 4
    dict(id='teshavi', name='Speaker Teshavi', role='Leader of the Veyli delegation', template='delegate', cabin='2-U', event='diplomatic', stay=5,
         outfit='#6b4a8a', bio='Speaks for the Veyli council. Patient, precise, and fond of long silences.',
         life=['Has known Envoy Saruth since they were both students of the cord.', 'Brought a gift for the Captain wrapped in seven knots.'],
         habits=['quiet-corner', 'early-riser']),
    dict(id='kesrin', name='Kesrin', role='Aide to the Speaker', template='delegate', cabin='4-01', event='diplomatic', stay=5,
         outfit='#6b4a8a', bio='Carries the Speaker\'s schedule in their head and their tea set in a satchel.',
         life=['Is secretly delighted by the vending machine on Deck 3.', 'Writes everything down, including the jokes.'],
         habits=['window-seat']),
    dict(id='moleth', name='Moleth', role='Veyli scholar', template='delegate', cabin='4-02', event='diplomatic', stay=5,
         outfit='#7a5a3a', bio='Studies human ships, and asks the crew questions nobody has asked before.',
         life=['Wants to see the engine room more than anything.', 'Has a list of forty questions for Chief Calder.'],
         habits=['garden-lover', 'stargazer']),
    dict(id='ithra', name='Ithra', role='Veyli pilot and guard', template='delegate', cabin='4-03', event='diplomatic', stay=5,
         outfit='#3a4a5a', bio='Flies the delegation\'s shuttle and watches every door. Says very little.',
         life=['Has asked Chief Holt about the Watch rota, twice.', 'Runs laps of the plaza at dawn.'],
         habits=['early-riser', 'runner']),
    # nebula drift: the visiting scientist who books the observatory
    dict(id='lindgren', name='Dr. Soraya Lindgren', role='Visiting astrophysicist', template='scientist', cabin='4-04', event='nebula', stay=6,
         outfit=None, dept='survey', work=dict(deck=2, place='work:survey'),
         bio='Chases nebulae across the frontier, and has finally caught one.', life=['Gives a talk in the observation room before she leaves.', 'Lives on tea and star charts.'],
         habits=['stargazer', 'night-owl']),
    # a Veyli vessel needs help: one of their engineers comes aboard
    dict(id='taavek', name='Taavek', role='Veyli engineer', template='scientist', cabin='4-04', event='veyliVessel', stay=3,
         outfit='#3a4a5a', work=dict(deck=5, place='work:works'),
         bio='Came aboard with a crate of parts and no common words for most of them.', life=['Sketches every machine in the Works bay.', 'Trades Veyli sweets for coffee.'],
         habits=['workaholic']),
    # salvage: two survivors from the derelict
    dict(id='quill', name='Mara Quill', role='Survivor from the derelict', template='survivor', cabin='4-01', event='salvage', stay=7,
         outfit='#8a8f9a', bio='Was the derelict\'s cook. Has not stopped thanking people.', life=['Wants to help in the galley as soon as Dr. Nandakumar lets her.', 'Lost everything but a photo of a dog.'],
         habits=['early-riser']),
    dict(id='petrie', name='Jonah Petrie', role='Survivor from the derelict', template='survivor', cabin='4-02', event='salvage', stay=7,
         outfit='#8a8f9a', bio='Was the derelict\'s navigator. Quiet, and watches the stars from any window.', life=['Keeps asking what day it is.', 'Is good at cards, and better at losing on purpose.'],
         habits=['window-seat', 'night-owl']),
]
# everyday visitors: [role, template, uniform or None (civilian), work (deck, place) or None, stay range, bios, life lines]
EVERYDAY = [
    ('Visiting astronomer', 'scientist', 'survey', (2, 'work:survey'), (5, 9), ['Here to borrow the observatory for a week of measurements.', 'Brought a telescope lens the size of a dinner plate.'], ['Asks everyone what they have seen out of the windows.', 'Has a habit of naming stars after cafes.']),
    ('Concord hull inspector', 'scientist', 'works', (5, 'work:works'), (4, 7), ['Inspects survey ships for the Concord, clipboard first.', 'Knocks on bulkheads and listens.'], ['Says the Wren is the tidiest ship this quarter, and means it.', 'Collects mission patches.']),
    ('Relief doctor', 'scientist', 'infirmary', (3, 'work:infirmary'), (6, 9), ['Covers the infirmary on rotation between ships.', 'A doctor on rotation, here to give Dr. Nandakumar a few days off.'], ['Has worked on eleven ships and remembers every galley.', 'Knits during quiet shifts.']),
    ('Visiting botanist', 'scientist', 'survey', (2, 'work:survey'), (5, 8), ['Studies plants grown in space, and has opinions about the garden.', 'Here to test new seeds in the garden.'], ['Talks to the tomatoes.', 'Brought cuttings from a Kesh orchard.']),
    ('Survey cartographer', 'scientist', 'survey', (2, 'work:survey'), (5, 8), ['Draws the charts other ships fly by.', 'On loan from the Concord charts office.'], ['Carries a pencil behind each ear.', 'Is trying to map the Wren\'s corridors by memory.']),
    ('Transfer to Marra Station', 'passenger', 'works', None, (2, 5), ['A Works technician waiting for a ship to Marra Station.', 'Between postings, and itching for something to fix.'], ['Offers to help in the Works bay every morning.', 'Has never seen a nebula.']),
    ('Retired captain', 'passenger', None, None, (3, 6), ['Commanded a freighter for thirty years, and is on the way home.', 'A retired captain hitching a ride to see family.'], ['Gives Captain Marrow advice she never asked for.', 'Tells stories in the lounge until late.']),
    ('Trader\'s apprentice', 'passenger', None, None, (2, 4), ['Learning the trade, and trying to sell everyone a better kettle.', 'Travels with a case of samples and a big smile.'], ['Has already sold two kettles.', 'Misses home and calls every night.']),
    ('Concord courier', 'passenger', None, None, (2, 3), ['Carries sealed pouches between ships, and says nothing about them.', 'A courier with a locked case and a tired face.'], ['Sleeps with the case.', 'Plays chess with anyone who asks.']),
    ('Musician on tour', 'passenger', None, None, (3, 5), ['Plays the stations of the frontier, one lounge at a time.', 'A travelling musician on the way to the next station.'], ['Plays in the music room every evening.', 'Can play anything you hum.']),
    ('Student on placement', 'passenger', 'survey', None, (4, 7), ['A student on a short placement, following the Survey team around.', 'Here to learn how a survey ship works.'], ['Asks the juniors for advice.', 'Keeps a notebook of everyone\'s names.']),
    ('Chef on exchange', 'passenger', 'works', None, (3, 6), ['A chef from Port Halloran, here to trade recipes with Brennan.', 'Swapping recipes with the galley for a few days.'], ['Brennan let them near the ovens once.', 'Brought spices nobody can pronounce.']),
]
# visitors' names: their own pools, so they never run short and never share a surname with the crew
VIS_FIRST = ['Adaeze', 'Alba', 'Aleksi', 'Amir', 'Anouk', 'Ari', 'Ayla', 'Bastian', 'Bryn', 'Cato', 'Celeste', 'Dario', 'Dilan', 'Edda', 'Elio', 'Esra',
             'Fen', 'Florin', 'Gael', 'Hale', 'Idris', 'Ilka', 'Ines', 'Iver', 'Jora', 'Juno', 'Kaito', 'Keira', 'Lark', 'Lio', 'Mads', 'Maren',
             'Milo', 'Nell', 'Nico', 'Nyla', 'Odo', 'Petra', 'Pim', 'Rhea', 'Ronan', 'Saoirse', 'Silas', 'Talia', 'Teo', 'Ulla', 'Vesna', 'Wilf', 'Yuki', 'Zora']
VIS_LAST = ['Aalto', 'Abbas', 'Arden', 'Baptiste', 'Bjork', 'Calloway', 'Castro', 'Danek', 'Delacroix', 'Ekwueme', 'Fairweather', 'Ferro', 'Galloway',
            'Grimaldi', 'Hadley', 'Hovland', 'Iwasaki', 'Jaramillo', 'Kalnins', 'Kessler', 'Laurent', 'Lindahl', 'Marsh', 'Mbatha', 'Novak', 'Oyelaran',
            'Pacheco', 'Quinlan', 'Rasmussen', 'Rocha', 'Saarinen', 'Sandoval', 'Szabo', 'Tamura', 'Thorne', 'Upton', 'Valdez', 'Varela', 'Wexley', 'Whitlock',
            'Adeyemi', 'Xu', 'Yarrow', 'Zaid', 'Zeller', 'Ashby', 'Brandt', 'Corwin', 'Dunmore', 'Ellery', 'Faraday', 'Gunn', 'Holm', 'Ingram', 'Royce',
            'Kirby', 'Lowe', 'Mercer', 'Nash', 'Orme']
CIVVIES = ['#7a6a5a', '#5a6a7a', '#6a7a5a', '#7a5a6a', '#5a5a5a', '#8a7a5a']

def visitors(out):
    used = {p['name'].split()[-1] for p in out} | {p['name'].split()[-1] for p in EVENT_GUESTS}
    used_first = {p['name'].split()[0] for p in out}
    res = []
    for g in EVENT_GUESTS:
        e = dict(id=g['id'], name=g['name'], rank='guest', dept='guest', uniform=g.get('dept'), role=g['role'], template=g['template'],
                 cabin=g['cabin'], event=g['event'], stay=g['stay'], arrive=None, leave=None,
                 work=g.get('work'), habits=g['habits'], bio=g['bio'], life=g['life'], seed=seed_of(g['id']))
        lk = VEYLI_LOOKS() if g['outfit'] in ('#6b4a8a', '#7a5a3a', '#3a4a5a') else looks_with(VIS_R)
        e['spec'] = dict(name=g['name'], dept=g.get('dept') or 'civilian', rank=0, bio=g['bio'], outfit=g['outfit'], **lk)
        res.append(e)
    free = {c: 0 for c in EVERYDAY_CABINS}             # the day each everyday cabin is free from
    for w in range(52):
        role, tpl, uni, work, (lo, hi), bios, lifes = VIS_R.choice(EVERYDAY)
        f = VIS_R.choice([x for x in VIS_FIRST if x not in used_first])
        l = VIS_R.choice([x for x in VIS_LAST if x not in used])
        used.add(l)
        arrive = w * 7 + VIS_R.randrange(7) + 1
        cabin = min(EVERYDAY_CABINS, key=lambda c: (free[c], c))
        arrive = max(arrive, free[cabin])
        leave = min(364, arrive + VIS_R.randint(lo, hi))
        free[cabin] = leave + 1
        pid = 'v-' + l.lower().replace("'", '') + '-' + f.lower()
        lk = looks_with(VIS_R)
        bio = VIS_R.choice(bios)
        e = dict(id=pid, name=f + ' ' + l, rank='guest', dept='guest', uniform=uni, role=role, template=tpl, cabin=cabin,
                 arrive=arrive, leave=leave, work=dict(deck=work[0], place=work[1]) if work else None,
                 habits=VIS_R.sample(['window-seat', 'lounge-regular', 'garden-lover', 'stargazer', 'bar-regular', 'shopper', 'early-riser', 'night-owl', 'calls-home'], 2),
                 bio=bio, life=[VIS_R.choice(lifes)], seed=seed_of(pid))
        e['spec'] = dict(name=e['name'], dept=uni or 'civilian', rank=0, bio=bio, outfit=None if uni else VIS_R.choice(CIVVIES), **lk)
        res.append(e)
    # checks: one guest per cabin at a time, every week has an everyday arrival, ids unique
    every = [e for e in res if e['arrive']]
    for c in EVERYDAY_CABINS:
        st = sorted((e['arrive'], e['leave']) for e in every if e['cabin'] == c)
        assert all(a[1] < b[0] for a, b in zip(st, st[1:])), c
    assert len({(e['arrive'] - 1) // 7 for e in every}) >= 50
    assert len({e['id'] for e in res}) == len(res) and not {e['id'] for e in res} & {p['id'] for p in out}
    assert not {e['cabin'] for e in res} & {p['bed'] for p in out}, 'a guest in a crew bed'
    for e in res:
        if any(a in e['habits'] and b in e['habits'] for a, b in CLASH): e['habits'] = e['habits'][:1]
    return res

# ---------------------------------------------------------------- Pillar 4 (0.16.12): days off, the social fields, couples
# and the reserve pool. All of it runs after everything above, from plain rules and its own random stream (P4_R), so
# nobody's name, looks, bed, habits or birthday moves
P4_R = random.Random(20261020)
# ---- varied days off: two days in a row; about 40% of the day shift at the weekend, the rest spread across the week; the
# night shift its own pattern; every department staffed every day. Fixed: these people, the galley, store and garden rotas
DAYS_FIXED = {'torres-zeke': [3, 4], 'halloran-emeka': [5, 6], 'calder': [5, 6]}
WEEKDAY_PAIRS = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [6, 0]]
NIGHT_PAIRS = [[1, 2], [3, 4], [5, 6], [0, 1], [2, 3], [4, 5], [6, 0]]
def stable(s): return int(hashlib.md5(s.encode()).hexdigest()[:8], 16)
def days_off(crew):
    fixed = lambda p: p['id'] in DAYS_FIXED or p['dept'] in ('galley', 'store', 'garden')
    for p in crew:
        if p['id'] in DAYS_FIXED: p['rota'] = dict(p['rota'], offDays=DAYS_FIXED[p['id']])
    day = [p for p in crew if p['shift'] == 'day']
    for dept in sorted({p['dept'] for p in day}):
        free = sorted([p for p in day if p['dept'] == dept and not fixed(p)], key=lambda p: stable(p['id']))
        allin = [p for p in day if p['dept'] == dept]
        wk = round(len(free) * .45)
        if wk and wk + sum(1 for p in allin if fixed(p) and p['rota']['offDays'] == [5, 6]) >= len(allin): wk -= 1   # someone works weekends
        off = stable(dept) % 6
        for k, p in enumerate(free):
            p['rota'] = dict(p['rota'], offDays=[5, 6] if k < wk else WEEKDAY_PAIRS[(off + k) % 6])
    night = sorted([p for p in crew if p['shift'] == 'night'], key=lambda p: (p['dept'], p['id']))
    for k, p in enumerate(night): p['rota'] = dict(p['rota'], offDays=NIGHT_PAIRS[k % 7])
    # every department, on each shift, has someone on every day (where it has two or more on that shift); fix any gap by moving a free member's pair
    for _ in range(50):
        gaps = [(dept, sh, d) for sh in ('day', 'night') for dept in sorted({p['dept'] for p in crew if p['shift'] == sh})
                if sum(1 for p in crew if p['dept'] == dept and p['shift'] == sh) > 1      # a lone night officer has days off like anyone
                for d in range(7) if all(d in p['rota']['offDays'] for p in crew if p['dept'] == dept and p['shift'] == sh)]
        if not gaps: break
        dept, sh, d = gaps[0]
        p = next(p for p in sorted(crew, key=lambda p: p['id']) if p['dept'] == dept and p['shift'] == sh and not fixed(p) and d in p['rota']['offDays'])
        p['rota'] = dict(p['rota'], offDays=next(q for q in WEEKDAY_PAIRS + [[5, 6]] if d not in q and q != p['rota']['offDays']))
    assert not gaps, gaps
    for p in crew: o = p['rota']['offDays']; assert len(o) == 2 and o[1] == (o[0] + 1) % 7, p['id']
# ---- voice templates, gifts, joys, threads (the social plan, Part 9)
TPL_OF = [('warm', ['kind', 'warm', 'gentle', 'generous', 'sociable']), ('dry', ['dry humour', 'sarcastic', 'wry', 'dry', 'quietly funny']),
          ('shy', ['shy', 'quiet', 'nervous', 'homesick', 'private']), ('brisk', ['practical', 'precise', 'organised', 'exacting', 'brisk', 'serious', 'tidy']),
          ('chatty', ['chatty', 'cheerful', 'easy laugh']), ('earnest', ['earnest', 'ambitious', 'reliable', 'dependable', 'loyal', 'a little lost']),
          ('gruff', ['blunt', 'stubborn', 'gruff', 'suspicious', 'proud']), ('dreamy', ['dreamy', 'absent-minded', 'forgetful', 'curious', 'thoughtful', 'messy']),
          ('steady', ['steady', 'patient', 'calm', 'meticulous', 'careful', 'unhurried', 'watchful', 'handy']), ('playful', ['playful', 'competitive', 'restless', 'optimistic', 'quick', 'sharp-eyed'])]
TPLS = [t for t, _ in TPL_OF]
OPEN_OF = {'shy': 'guarded', 'gruff': 'guarded', 'chatty': 'open', 'warm': 'open', 'playful': 'open'}
NEEDS_OF = {'warm': 'share', 'dry': 'cheer', 'shy': 'listen', 'brisk': 'practical', 'chatty': 'share', 'earnest': 'practical',
            'gruff': 'practical', 'dreamy': 'share', 'steady': 'listen', 'playful': 'cheer'}
GIFT_TAGS = ['tea', 'sweet', 'plant', 'garden', 'made', 'book', 'music', 'star', 'game']
TAGS_OF_HABIT = {'gardener': ['garden', 'plant'], 'garden-lover': ['plant', 'garden'], 'musician': ['music'], 'music': ['music'], 'stargazer': ['star'],
                 'window-seat': ['star'], 'tea-break': ['tea'], 'lounge-regular': ['tea'], 'early-riser': ['tea'], 'shopper': ['sweet'], 'lingers-at-meals': ['sweet'],
                 'late-sleeper': ['sweet'], 'quiet-corner': ['book'], 'common-room': ['game'], 'bar-regular': ['game'], 'workaholic': ['made'], 'calls-home': ['made'],
                 'runner': ['sweet'], 'gym-regular': ['game']}
LIFE_CLUES = [('guitar', 'music', 'learning the guitar, badly'), ('knit', 'made', 'knitting scarves'), ('cactus', 'plant', 'looking after a cactus called Gerald'),
              ('flowers', 'plant', 'pressing flowers from the garden'), ('bake', 'sweet', 'baking on rest days'), ('paint', 'made', 'painting tiny portraits of the crew'),
              ('journal', 'book', 'keeping a journal'), ('novel', 'book', 'mystery novels'), ('herbs', 'garden', 'growing herbs'), ('recipe', 'sweet', 'trying recipes from home'),
              ('song', 'music', 'knowing every song in the record cabinet'), ('jokes', 'game', 'telling terrible jokes'), ('star', 'star', 'watching the stars'),
              ('letters', 'made', 'writing letters home'), ('cat', 'made', 'talking about their cat'), ('chess', 'game', 'chess')]
JOY_OF_HABIT = {'runner': 'running on the treadmill', 'gym-regular': 'the gym after shift', 'musician': 'playing in the music room', 'music': 'evenings in the music room',
                'gardener': 'tending the garden', 'garden-lover': 'the garden benches', 'stargazer': 'observatory nights', 'bar-regular': 'a drink at the lounge bar',
                'shopper': 'browsing the crew store', 'common-room': 'Tiles nights', 'calls-home': 'calls home', 'quiet-corner': 'a good book in a quiet corner',
                'window-seat': 'a seat by the window', 'lounge-regular': 'evenings in the bow lounge', 'tea-break': 'a proper tea break'}
THEMES = ['homesick', 'exams', 'family', 'stuck', 'notgood', 'lonely', 'loss', 'talent', 'burnout', 'leaving', 'rivalry', 'startover']
THEME_OF_TRAIT = {'homesick': 'homesick', 'nervous': 'exams', 'ambitious': 'stuck', 'meticulous': 'notgood', 'shy': 'lonely', 'quiet': 'lonely',
                  'restless': 'leaving', 'competitive': 'rivalry', 'blunt': 'rivalry', 'reliable': 'burnout', 'dreamy': 'talent', 'thoughtful': 'loss',
                  'curious': 'startover', 'loyal': 'family', 'kind': 'family', 'stubborn': 'rivalry', 'gentle': 'loss', 'serious': 'notgood'}
KEEPSAKE_OF = {'tea': 'a little tin of their own tea blend', 'sweet': 'a recipe card in their handwriting', 'plant': 'a cutting in a jar', 'garden': 'a packet of seeds from the garden',
               'made': 'something they made: a little gear on a chain', 'book': 'a battered paperback with notes in the margins', 'music': 'a guitar pick, worn smooth',
               'star': 'a hand-drawn star chart', 'game': 'a Tiles piece, chipped at one corner'}
FAMILY = ['a younger brother', 'two older sisters', 'parents who run a repair shop', 'a grandmother who raised them', 'a big, noisy family', 'a twin',
          'a mother who writes every week', 'a father who grows apples', 'three cousins they grew up with', 'an aunt who was a pilot', 'a little sister who wants to join up',
          'parents on a mining station']
SHIPS = ['the Kestrel', 'the Halcyon', 'the Osprey', 'the Meridian', 'the Calypso', 'the Heron', 'the Lark', 'the Corvid']
# the about details for everyone without hand-written ones: { tier, topic, text }, text a sentence with {home}, {family}, {joy}, {work}
ABOUT_WORK0 = ['Knows {work} better than anyone gives them credit for.', 'Will tell you which corner of {work} is the warmest.', 'Has opinions about how {work} should be run.',
               'Is usually the first in {work} and the last out.', 'Keeps a mug at {work} that nobody else is allowed to use.']
ABOUT_CADET0 = ['Is still learning where everything is in {work}, and asks a lot of questions.', 'Got lost on the way to {work} on the first morning, and laughs about it now.']
ABOUT_HOBBY1 = ['Spends free evenings {joy}.', 'Lights up when anyone mentions {joy}.', 'Will talk about {joy} for as long as you let them.']
ABOUT_HOME1 = ['Grew up on {home}.', 'Comes from {home}, and says it like a boast.', 'Still calls {home} home.']
ABOUT_FAMILY2 = ['Has {family}, and keeps a photo of them by the bunk.', 'Writes to {family} more often than they write back.', 'Has {family}, and misses them more than they let on.']
ABOUT_WORK2 = ['Thinks the Wren is the best-run ship they\'ve served on, and would never say so to Calder.', 'Thinks the coffee on Deck 5 is the best on the ship, and says so loudly.',
               'Has a running bet with someone in another department that nobody else knows about.', 'Thinks the lift on Deck 5 has a personality.']
ABOUT_THEME = {   # tier 3 (past or work, opens up) and tier 4 (secret) per struggle theme
    'homesick': ('home', 'Misses the food on {home} more than the people, and feels bad about it.', 'secret', 'Has a ticket home saved up, just in case, and has never told anyone.'),
    'exams': ('work', 'Is studying for a certification and is quietly terrified of the practical.', 'secret', 'Failed it once already, before the Wren.'),
    'family': ('home', 'Someone in the family has been unwell, and the news comes slowly.', 'secret', 'Thinks about going home for good, and hasn\'t decided.'),
    'stuck': ('work', 'Has done the same job for five years and wonders about another department.', 'secret', 'Has filled in a transfer request three times and never sent it.'),
    'notgood': ('past', 'Still thinks about a mistake on an old ship, though nobody else remembers it.', 'secret', 'Checks their own work twice because once, years ago, they didn\'t.'),
    'lonely': ('past', 'Has never been good at joining in, and eats alone more than they\'d like.', 'secret', 'Would love to be asked to a Tiles night, and would never ask.'),
    'loss': ('past', 'Goes quiet on one day each year, and doesn\'t say why.', 'secret', 'Lost someone close a few years ago, and keeps something of theirs in the bunk.'),
    'talent': ('hobby', 'Hums, sketches, or scribbles when they think nobody\'s watching.', 'secret', 'Is good at it, really good, and too shy to show anyone.'),
    'burnout': ('work', 'Is always the last to leave, and can\'t say no to anyone.', 'secret', 'Is more tired than they let anyone see.'),
    'leaving': ('work', 'Reads the transfer lists every week.', 'secret', 'Isn\'t sure whether to stay on the Wren, and changes their mind daily.'),
    'rivalry': ('past', 'Has an old rivalry with someone aboard that goes back years.', 'secret', 'Can\'t remember how it started, and would quite like it to end.'),
    'startover': ('past', 'Is vague about what they did before the Wren.', 'secret', 'Came aboard to start over after something went wrong at home, and is glad they did.'),
}
# hand-written for the hand-written crew: social fields, and about details added to theirs (to six or more each)
SOCIAL_HAND = {
    'marrow': dict(tpl='steady', openness='guarded', needs='listen', loves=['music'], likes=['tea', 'book'], joy='the piano on Thursday nights', thread='arc:marrow', keepsake='a page of sheet music she wrote', home='Port Halloran', family='a daughter at the Concord academy'),
    'vance': dict(tpl='brisk', openness='guarded', needs='practical', loves=['game'], likes=['made', 'tea'], joy='the rowing leaderboard', thread='arc:vance', keepsake='his old academy rowing medal', home='New Aberdeen', family='a brother in the Concord navy'),
    'sato': dict(tpl='dreamy', openness='normal', needs='share', loves=['tea', 'star'], likes=['book', 'plant'], joy='her terrible tea', thread='arc:sato', keepsake='a tin of the terrible tea', home='Lisk', family='a partner on a research station'),
    'holt': dict(tpl='gruff', openness='guarded', needs='practical', loves=['made'], likes=['tea', 'game'], joy='walking the decks before breakfast', thread='arc:holt', keepsake='his first Watch badge', home='Marra Station', family='an old border-patrol crew he still writes to'),
    'calder': dict(tpl='brisk', openness='guarded', needs='practical', loves=['made'], likes=['tea', 'book'], joy='a fan that runs sweetly', thread='arc:calder', keepsake='a spanner from the battered toolbox', home='the Tevan belt shipyards', family='her first chief, as near to family as she had'),
    'pell': dict(tpl='chatty', openness='open', needs='cheer', loves=['music', 'sweet'], likes=['made', 'game'], joy='his tin of screws from every ship', thread='arc:pell', keepsake='his smallest music box', home='Coriel', family='his mum, who messages every week'),
    'rina': dict(tpl='dry', openness='guarded', needs='cheer', loves=['game', 'sweet'], likes=['tea', 'garden'], joy='Tiles', thread='arc:rina', keepsake='a Tiles piece, the cheating one', home='Kesh', family='a sister who is a station doctor, and her gran'),
    'brennan': dict(tpl='warm', openness='normal', needs='share', loves=['garden', 'sweet'], likes=['tea', 'plant'], joy='a full mess hall', thread='arc:brennan', keepsake='a biscuit tin with a recipe taped inside', home='Port Halloran', family='the old restaurant crew'),
    'tomas': dict(tpl='earnest', openness='open', needs='listen', loves=['star'], likes=['book', 'sweet'], joy='his taped-up star map', thread='arc:tomas', keepsake='his spare star map', home='a farm moon with a grey sky', family='a little brother he writes to every week'),
    'nandakumar': dict(tpl='brisk', openness='normal', needs='practical', loves=['garden', 'plant'], likes=['tea', 'book'], joy='her chillies in the garden', thread='burnout', keepsake='a dried chilli on a string', home='New Aberdeen', family='two grown sons'),
    'kowalczyk': dict(tpl='dry', openness='guarded', needs='listen', loves=['book'], likes=['tea', 'star'], joy='old paper novels', thread='lonely', keepsake='a paper novel with her notes in it', home='Marra Station', family='a father who ran a lighthouse beacon'),
    'raman': dict(tpl='steady', openness='normal', needs='share', loves=['made'], likes=['music', 'star'], joy='his model of the Wren', thread='leaving', keepsake='a tiny model shuttle he carved', home='Lisk', family='a wife and two daughters on Lisk'),
    'ferreira': dict(tpl='chatty', openness='open', needs='share', loves=['music'], likes=['tea', 'book'], joy='languages, Veyli most of all', thread='family', keepsake='a phrasebook in four languages', home='Coriel', family='a big family who all talk at once'),
    'oduya': dict(tpl='warm', openness='open', needs='listen', loves=['sweet'], likes=['plant', 'book'], joy='a bowl of sweets on his desk', thread='loss', keepsake='a sweet from the bowl, the last of a kind', home='Kesh', family='a late wife he still talks about'),
    'mensah': dict(tpl='playful', openness='normal', needs='cheer', loves=['game'], likes=['sweet', 'music'], joy='making Holt laugh', thread='startover', keepsake='a lucky coin from his first patrol', home='Port Halloran', family='a twin brother'),
    'mori': dict(tpl='shy', openness='guarded', needs='listen', loves=['star'], likes=['book', 'tea'], joy='charting', thread='notgood', keepsake='a corner of her first chart', home='the Tevan belt', family='parents who wanted her to stay home'),
    'torres-zeke': dict(tpl='warm', openness='open', needs='share', loves=['music', 'made'], likes=['tea', 'sweet'], joy='knitting scarves and every song in the record cabinet', thread='arc:torres', keepsake='a scarf he knitted for you', home='Hesper Dock', family='a grandmother who taught him to knit'),
    'saruth': dict(tpl='steady', openness='guarded', needs='listen', loves=['tea'], likes=['plant', 'made'], joy='the daily tea', thread='lonely', keepsake='a knot of Veyli cord', home='the Veyli homeworld', family='a teacher of the cord, far away'),
}
ABOUT_HAND_MORE = {
    'marrow': [(2, 'past', 'Commanded a freighter before the Wren, and hated every day of it.'), (3, 'hobby', 'Plays the piano best when she thinks the music room is empty.')],
    'vance': [(1, 'home', 'Grew up in New Aberdeen, where his brother still teases him about the rules.'), (3, 'hobby', 'Rows at 05:00 so nobody sees him lose to the machine.')],
    'sato': [(2, 'home', 'Has a partner on a research station, and they send each other comet photographs.'), (3, 'hobby', 'Grows a single tea plant in the garden, badly.')],
    'holt': [(2, 'home', 'Writes to his old patrol crew every month, by hand.'), (3, 'work', 'Respects Kofi Mensah more than he has ever told him.')],
    'calder': [(2, 'home', 'Grew up in the Tevan belt shipyards, with no family to speak of.'), (3, 'hobby', 'Fixes broken things nobody asked her to, late at night, to think.')],
    'brennan': [(2, 'home', 'Still gets letters from the old restaurant crew on Port Halloran.'), (3, 'hobby', 'Grows her own herbs, and won\'t let anyone else pick them.')],
    'saruth': [(2, 'past', 'Studied the cord for twenty years before the posting.'), (3, 'work', 'Finds Chief Holt\'s suspicion almost restful: at least it is honest.')],
}
ABOUT_HAND_NEW = {
    'nandakumar': [(0, 'work', 'Runs the infirmary like a clock, and will tell you to drink some water.'), (1, 'hobby', 'Grows chillies in the garden that nobody else can eat.'),
                   (1, 'home', 'Comes from New Aberdeen, and has two grown sons there.'), (2, 'work', 'Thinks Rina will make a fine doctor, and hasn\'t told her yet.'),
                   (3, 'past', 'Worked in a big city hospital for years before choosing the frontier.'), (4, 'secret', 'Is more tired than she lets anyone see, and keeps saying yes.')],
    'kowalczyk': [(0, 'work', 'Runs the bridge at night, and likes it quiet.'), (1, 'hobby', 'Reads old paper novels on quiet nights, and sniffs the pages.'),
                  (1, 'home', 'Grew up on Marra Station, where her father kept a beacon.'), (2, 'work', 'Thinks the night shift is the real ship, and the day shift is visitors.'),
                  (3, 'past', 'Has been on night shift so long she has forgotten what lunch is like.'), (4, 'secret', 'Sometimes goes a whole week without a real conversation, and minds more than she says.')],
    'raman': [(0, 'work', 'Flies the Wren like it might spill.'), (1, 'hobby', 'Keeps a model of the Wren by his door, and adds a detail every month.'),
              (1, 'home', 'Has a wife and two daughters on Lisk.'), (2, 'work', 'Has flown survey ships for twenty years, and still gets nervous docking.'),
              (3, 'home', 'Misses his daughters growing up, one call at a time.'), (4, 'secret', 'Has been offered a desk job near home, and hasn\'t answered.')],
    'ferreira': [(0, 'work', 'Every message home passes through her hands, and she never reads them.'), (1, 'hobby', 'Speaks four languages and some Veyli, and wants more.'),
                 (1, 'home', 'Comes from a big family on Coriel who all talk at once.'), (2, 'work', 'Is learning Veyli from the Envoy, one word a day.'),
                 (3, 'home', 'Her mother has been ill, and the news comes slowly.'), (4, 'secret', 'Reads the messages from home three times before she can answer.')],
    'oduya': [(0, 'work', 'Keeps office hours on Deck 3 and a bowl of sweets on his desk.'), (1, 'hobby', 'Knows everyone\'s birthday, and their favourite sweet.'),
              (1, 'home', 'Comes from Kesh, and still cooks its food badly.'), (2, 'work', 'Thinks most problems aboard are about sleep, and is usually right.'),
              (3, 'past', 'Lost his wife some years ago, and talks about her easily now.'), (4, 'secret', 'Took the posting because their house was too quiet without her.')],
    'mensah': [(0, 'work', 'Walks the whole ship once a night, deck by deck.'), (1, 'hobby', 'Is the only one who can make Chief Holt laugh, and works at it.'),
               (1, 'home', 'Has a twin brother on Port Halloran.'), (2, 'work', 'Thinks the Watch is about kindness more than rules, and Holt half agrees.'),
               (3, 'past', 'Was a very different man before he joined the Watch.'), (4, 'secret', 'Came aboard to start over, and the Wren worked.')],
    'mori': [(0, 'work', 'Runs the labs while Sato runs everyone.'), (1, 'hobby', 'Maps the frontier one survey at a time, in the chart room.'),
             (1, 'home', 'Comes from the Tevan belt, where her parents wanted her to stay.'), (2, 'work', 'Thinks Sato is a genius and a menace, in equal parts.'),
             (3, 'past', 'Made a charting mistake years ago that nobody else remembers.'), (4, 'secret', 'Checks every chart three times because of it.')],
    'torres-zeke': [(0, 'work', 'Knows every engine on the Wren by its sound.'), (1, 'hobby', 'Knits scarves for anyone who stands still long enough.'),
                    (1, 'home', 'Grew up on Hesper Dock, where his grandmother taught him to knit.'), (2, 'work', 'Remembers his own first week aboard, and was terrible at it.'),
                    (3, 'past', 'Nearly washed out of training, and someone gave him a second chance.'), (4, 'secret', 'Asked to be the one who meets the new cadets, because nobody met him.')],
}
# couples: established crew couples (never the player, never story crew), partner both ways
COUPLES = 4
def social_fields(out):
    hand = set(SOCIAL_HAND)
    for e in out:
        if e.get('player') or e['rank'] == 'guest' and e['id'] not in hand: continue
        if e['id'] in hand:
            e.update(SOCIAL_HAND[e['id']])
        else:
            tr = e.get('traits', [])
            e['tpl'] = next((t for t, words in TPL_OF if any(w in tr for w in words)), TPLS[stable(e['id']) % 10])
            e['openness'] = OPEN_OF.get(e['tpl'], 'normal'); e['needs'] = NEEDS_OF[e['tpl']]
            life = ' '.join(e.get('life', [])).lower()
            clue = next(((tag, joy) for k, tag, joy in LIFE_CLUES if k in life), None)
            tags = ([clue[0]] if clue else []) + [t for h in e['habits'] for t in TAGS_OF_HABIT.get(h, [])]
            tags = list(dict.fromkeys(tags)) or [P4_R.choice(GIFT_TAGS)]
            e['loves'] = tags[:1 + (len(tags) > 2)]
            rest = [t for t in tags if t not in e['loves']] + P4_R.sample([t for t in GIFT_TAGS if t not in tags], 2)
            e['likes'] = rest[:2]
            e['joy'] = clue[1] if clue else next((JOY_OF_HABIT[h] for h in e['habits'] if h in JOY_OF_HABIT), 'a good cup of tea')
            cand = [THEME_OF_TRAIT[t] for t in tr if t in THEME_OF_TRAIT] + (['burnout'] if 'workaholic' in e['habits'] else [])
            e['thread'] = P4_R.choice(cand) if cand and P4_R.random() < .7 else P4_R.choice(THEMES)
            e['keepsake'] = KEEPSAKE_OF[e['loves'][0]]
            hm = next((pl for pl in PLACES if pl.lower() in life), None)
            e['home'] = hm or P4_R.choice(PLACES); e['family'] = P4_R.choice(FAMILY)
        # about: hand-written where there are some; everyone ends with six or more, tiers 0-4, one tier-4 secret
        if e['id'] in ABOUT_HAND_NEW: e['about'] = [dict(tier=t, topic=k, text=x) for t, k, x in ABOUT_HAND_NEW[e['id']]]
        elif e['id'] in ABOUT_HAND_MORE: e['about'] = e['about'] + [dict(tier=t, topic=k, text=x) for t, k, x in ABOUT_HAND_MORE[e['id']]]
        elif not e.get('about'):
            work = WORK_WORDS[e['work']['place']] if e.get('work') else 'the ship'
            f = lambda s: s.format(home=e['home'], family=e['family'], joy=e['joy'], work=work)
            t3k, t3, t4k, t4 = ABOUT_THEME[e['thread']]
            e['about'] = [dict(tier=0, topic='work', text=f(P4_R.choice(ABOUT_CADET0 if e.get('cadet') else ABOUT_WORK0))), dict(tier=1, topic='hobby', text=f(P4_R.choice(ABOUT_HOBBY1))),
                          dict(tier=1, topic='home', text=f(P4_R.choice(ABOUT_HOME1))), dict(tier=2, topic='home', text=f(P4_R.choice(ABOUT_FAMILY2))),
                          dict(tier=2, topic='work', text=f(P4_R.choice(ABOUT_WORK2))), dict(tier=3, topic=t3k, text=f(t3)), dict(tier=4, topic=t4k, text=f(t4))]
        a = e['about']
        assert len(a) >= 6 and sum(x['tier'] == 4 for x in a) >= 1 and all(x['tier'] in range(5) and x['topic'] in ('home', 'work', 'hobby', 'past', 'secret') for x in a), e['id']
        for k in ('tpl', 'loves', 'likes', 'joy', 'thread', 'needs', 'openness', 'keepsake', 'home', 'family'): assert e.get(k), (e['id'], k)
# ---- who may be transferred (the social plan, Part 8b): never the Captain, the Chiefs, the escort, the story crew, Saruth
STAYS = {'marrow', 'vance', 'sato', 'holt', 'calder', 'nandakumar', 'torres-zeke', 'tomas', 'pell', 'rina', 'brennan', 'saruth'}
def couples_and_moves(out):
    crew = [e for e in out if e['rank'] != 'guest' and not e.get('player')]
    for e in crew:
        if e['id'] in STAYS: e['stays'] = True
        else: e['transferTo'] = SHIPS[stable(e['id']) % len(SHIPS)]
        e['aboard'] = None
    pool = sorted([e for e in crew if e['id'] not in HAND and e['id'] not in STAYS], key=lambda e: e['id'])
    made = []
    while len(made) < COUPLES:
        a = P4_R.choice(pool)
        cand = [b for b in pool if b is not a and b['shift'] == a['shift'] and b['dept'] != a['dept'] and abs(RANK_ORDER.index(a['rank']) - RANK_ORDER.index(b['rank'])) <= 1]
        if not cand: continue
        b = P4_R.choice(cand)
        a['partner'], b['partner'] = b['id'], a['id']
        if a['thread'] == 'lonely': a['thread'] = 'family'
        if b['thread'] == 'lonely': b['thread'] = 'family'
        b['transferTo'] = a['transferTo']             # a couple transfers together
        made.append((a['id'], b['id'])); pool = [e for e in pool if e not in (a, b)]
    return made
# ---- the reserve pool: about 12 future crew, a third of them new cadets; and the rotation calendar
RES_LAST = ['Achebe', 'Bramwell', 'Castellano', 'Dufresne', 'Eriksen', 'Fontaine', 'Gallagher', 'Haverford', 'Ishikawa-Lund', 'Juarez', 'Kowal', 'Lindgren-Bay',
            'Mwangi', 'Nordqvist', 'Okonkwo', 'Pellegrini', 'Quaye', 'Rourke', 'Sorensen', 'Tavares']
RES_FIRST = ['Agnes', 'Basil', 'Cora', 'Dmitri', 'Effie', 'Femi', 'Gwen', 'Hiro', 'Iona', 'Jem', 'Kofi', 'Lumi', 'Mara', 'Nell', 'Otto', 'Priya', 'Rafe', 'Sunny', 'Tam', 'Vida']
RESERVE = [   # dept, rank, role, job, shift, cadet
    ('works', 'junior', 'Works cadet', 'works', 'day', True), ('survey', 'junior', 'Survey cadet', 'survey', 'day', True),
    ('watch', 'junior', 'Watch cadet', 'watch', 'day', True), ('galley', 'junior', 'Galley cadet', 'galley', 'day', True),
    ('works', 'junior', 'Works technician', 'works', 'day', False), ('works', 'junior', 'Engine technician', 'engine', 'night', False),
    ('helm', 'officer', 'Helm officer', 'helm', 'day', False), ('survey', 'officer', 'Survey officer', 'survey', 'day', False),
    ('infirmary', 'junior', 'Infirmary aide', 'infirmary', 'day', False), ('comms', 'junior', 'Comms rating', 'comms', 'day', False),
    ('watch', 'officer', 'Watch officer', 'watch', 'night', False), ('survey', 'junior', 'Survey assistant', 'survey', 'day', False),
]
RES_BIOS = {'cadet': ['Brand new, and trying very hard not to look it.', 'Fresh from the academy, with a kitbag that\'s far too heavy.', 'New aboard, and already lost twice.'],
            'other': ['Transferred in from another survey ship, with stories.', 'Has served on three ships and likes this one already.', 'Arrives with a good reputation and a bad haircut.']}
RES_LIFE = ['Has never seen a nebula.', 'Brought a plant from home that is not doing well.', 'Writes letters home every week.', 'Plays the harmonica, quietly.',
            'Is trying to learn everyone\'s name in a week.', 'Has a cat back home, and talks about it a lot.', 'Collects mission patches.', 'Bakes on rest days.']
ROTATION_DAYS = [35, 77, 119, 161, 203, 245]      # Sundays, every six ship weeks from week 5
ROTATION_IN = [1, 2, 2, 3, 2, 2]                  # arrivals each time (the same number leave); the first brings a new cadet
def reserve(out):
    used_last = {e['name'].split()[-1] for e in out}; used_first = {e['name'].split()[0] for e in out}
    taken = {e['birthday'] for e in out if e.get('birthday')}
    res = []
    order = [0, 4, 1, 6, 9, 2, 5, 7, 3, 8, 11, 10]  # arrival order: a new cadet first
    for k in order:
        dept, rank, role, job, shift, cadet = RESERVE[k]
        f = P4_R.choice([x for x in RES_FIRST if x not in used_first]); l = P4_R.choice([x for x in RES_LAST if x not in used_last])
        used_first.add(f); used_last.add(l)
        pid = l.lower().replace("'", '') + '-' + f.lower()
        deck, place = WORK[job]
        bday = P4_R.choice([d for d in range(1, 365) if d not in taken]); taken.add(bday)
        e = dict(id=pid, name=f + ' ' + l, reserve=True, cadet=cadet, rank=rank, dept=dept, uniform=UNIFORM[dept], role=role, shift=shift,
                 rota={'offDays': ([[5, 6]] + WEEKDAY_PAIRS)[stable(pid) % 7] if shift == 'day' else NIGHT_PAIRS[stable(pid) % 7]}, bed=None,
                 work=dict(deck=deck, place=place), habits=P4_R.sample(list(HABITS)[:18], 2), traits=P4_R.sample(TRAITS, 2), looks=looks_with(P4_R),
                 bio=P4_R.choice(RES_BIOS['cadet' if cadet else 'other']), life=P4_R.sample(RES_LIFE, 2), seed=seed_of(pid), birthday=bday)
        if any(a in e['habits'] and b in e['habits'] for a, b in CLASH): e['habits'] = e['habits'][:1]
        if rank != 'junior': e['plate'] = {'rank': PLATE_RANK[rank], 'name': e['name']}
        e['transferTo'] = None
        res.append(e)
    social_fields(res)
    k = 0; rot = []
    for day, n in zip(ROTATION_DAYS, ROTATION_IN):
        arr = res[k:k + n]; k += n
        for e in arr: e['aboard'] = [day, None]
        rot.append(dict(day=day, out=n, **{'in': [e['id'] for e in arr]}))
    assert k == len(res) and res[0]['cadet'] and all(d % 7 == 0 for d in ROTATION_DAYS)
    return res, rot

DROPPED = []
COUPLED = []

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
    # ---- Pillar 2 habits: at most one new habit each. Each habit picks its regulars one at a time, weighted towards
    # people whose habits go with it and away from departments it already has, so every room gets a mix
    for p in crew:
        if p['id'] in STORY_P2: p['habits'] = p['habits'] + [STORY_P2[p['id']]]
    gen = [p for p in crew if p['id'] not in HAND]
    for h, n in P2_COUNT.items():
        depts = {}
        for _ in range(n):
            pool = [p for p in gen if not set(p['habits']) & set(HABITS_P2)]
            w = [(4 if set(p['habits']) & set(P2_LIKES[h]) else 1) * (.1 if set(p['habits']) & set(P2_DISLIKES.get(h, [])) else 1)
                 / (1 + 2 * depts.get(p['dept'], 0)) for p in pool]
            p = NEW_R.choices(pool, w)[0]
            p['habits'] = p['habits'] + [h]; depts[p['dept']] = depts.get(p['dept'], 0) + 1
    # ---- the crew store (0.16.5): two Works technicians, from the biggest department, become the storekeepers
    # (after the habits, so those don't move).
    # They stay day-shift juniors; their hours hand over at the one till, and their days off never meet
    for p, (hours, off, bio) in zip([p for p in crew if p['role'] == 'Works technician' and not p.get('story')][-2:], STOREKEEPERS):
        p.update(dept='store', role='Storekeeper', job='store', bio=bio)
        p['rota'] = {'offDays': off, 'hours': hours}
    # ---- the garden (0.16.11): the three day crew with the gardener habit tend the working garden. Ravi Hart works
    # early, Imani O'Neill late; Tove Cruz, the senior gardener, works days, and on their days off takes their hours
    # (rota.hoursOn), so the garden has early and late cover every day. Their beds and habits stay; they work at the
    # garden's work:garden stations (the deck architect's 0.38.6)
    for p in crew:
        if p['id'] in GARDENERS:
            role, team, off, hours, on, bio = GARDENERS[p['id']]
            p.update(dept='garden', role=role, job='garden', bio=bio)
            p['rota'] = {'offDays': off, 'hours': hours, 'team': team}
            if on: p['rota']['hoursOn'] = on
    for d in range(7):
        hrs = [h for p in crew if p['dept'] == 'garden' and d not in p['rota']['offDays']
               for h in next((o['hours'] for o in p['rota'].get('hoursOn', []) if d in o['days']), p['rota']['hours'])]
        assert any(a <= 360 for a, b in hrs) and any(b >= 1260 for a, b in hrs), ('garden cover', d)
    # ---- the galley staff's teams, agreed with the galley engineer (section 16 owns their hours, in GALLEY_SHIFTS; shift
    # stays 'day'). Days off give a chef and at least one early and one late hand every day; Lukas Dlamini, an early
    # hand, works the chef's shift on Brennan's days off (Fri and Sat)
    for p in crew:
        if p['dept'] == 'galley':
            team, off = GALLEY_TEAMS[p['id']]
            p['rota'] = dict(p['rota'], offDays=off, team=team)
            if p['id'] == 'dlamini-lukas': p['rota']['cover'] = {'for': 'brennan', 'days': [4, 5]}
    for d in range(7):
        on = [p['rota']['team'] for p in crew if p['dept'] == 'galley' and d not in p['rota']['offDays'] and d not in p['rota'].get('cover', {}).get('days', [])]
        assert 'early' in on and 'late' in on, d
    days_off(crew)                                      # Pillar 4: varied days off (after every rota above)
    # ---- work places, seeds, uniform
    out = []
    for p in crew + GUESTS + [PLAYER]:
        deck, place = WORK[p['job']] if p['job'] else (None, None)
        e = dict(id=p['id'], name=p['name'])
        if p.get('story'): e['story'] = True
        if p.get('player'): e['player'] = True
        e.update(rank=p['rank'], dept=p['dept'], uniform=UNIFORM.get(p['dept']), role=p['role'], shift=p['shift'], rota=p['rota'], bed=p['bed'],
                 work=dict(deck=deck, place=place) if deck else None, habits=p['habits'], traits=p['traits'], looks=p['looks'],
                 bio=p['bio'], life=p['life'], seed=seed_of(p['id']))
        out.append(e)
    # ---- birthdays (0.16.6): a ship day of the year, 1-364 (52 weeks of 7 days; day 1 is the game's Day 1, a Monday).
    # Everyone gets one, you and the Envoy included: every week has at least one, 24 weeks have two (on different
    # days), so about one a week. Their own random stream, so nothing above moves
    weeks = list(range(52)) + BDAY_R.sample(range(52), len(out) - 52)
    BDAY_R.shuffle(weeks)
    taken = set()
    for e, w in zip(out, weeks):
        d = BDAY_R.randrange(7)
        while w * 7 + d in taken: d = (d + 1) % 7
        taken.add(w * 7 + d); e['birthday'] = w * 7 + d + 1
    # ---- door plates (0.16.6): everyone with a cabin of their own (officers and up, and guests) gets
    # plate: { rank, name }, the two lines the architects print on the door; titles that are ranks move to the rank line
    for e in out:
        if e['rank'] != 'junior':
            name = e['name']
            for t in ('Captain ', 'Commander ', 'Chief ', 'Envoy '):
                if name.startswith(t): name = name[len(t):]
            e['plate'] = {'rank': PLATE_RANK[e['rank']], 'name': name}
    # ---- habits that change (0.16.7): hand-written for the hand-written crew and the Envoy; for everyone else one or
    # two items drawn (SHIFT_R, after everything else) from the swaps, adds and drops that are valid for them
    def ok(e, it):
        hab = set(e['habits'])
        if it.get('drop') and it['drop'] not in hab: return False
        if it.get('add'):
            if it['add'] in hab: return False
            after = (hab - {it.get('drop')}) | {it['add']}
            if any(a in after and b in after for a, b in CLASH): return False
            if it['add'] == 'common-room' and e['rank'] != 'junior': return False
        return True
    for e in out:
        if e.get('player'): continue
        if e['id'] in SHIFTS_HAND:
            e['habitShifts'] = SHIFTS_HAND[e['id']]
        else:
            f = e['name'].split()[0]
            opts = [dict(drop=a, add=b, why=w.format(f=f)) for a, b, w in SHIFT_SWAPS] * 2 + \
                   [dict(add=h, why=w.format(f=f)) for h, w in SHIFT_ADDS.items()] + [dict(drop=h, why=w.format(f=f)) for h, w in SHIFT_DROPS.items()]
            opts = [o for o in opts if ok(e, o)]
            pick = []
            for _ in range(SHIFT_R.choice([1, 2, 2])):
                o = SHIFT_R.choice(opts)
                if all(o.get('add') != q.get('add') and o.get('drop') != q.get('drop') for q in pick): pick.append(o)
            e['habitShifts'] = [{k: o[k] for k in ('add', 'drop', 'why') if o.get(k)} for o in pick]
        assert e['habitShifts'] and all(ok(e, it) for it in e['habitShifts']), e['id']
        for it in e['habitShifts']: assert e['name'].split()[0] in it['why'] or e['name'] in it['why'] or e['id'] in it['why'].lower(), (e['id'], it['why'])
    for e in out:
        if e['id'] in ABOUT: e['about'] = [dict(tier=t, topic=k, text=x) for t, k, x in ABOUT[e['id']]]
    assert all(a['tier'] in range(5) and a['topic'] in ('home', 'work', 'hobby', 'past', 'secret') for e in out for a in e.get('about', []))
    social_fields(out); COUPLED.extend(couples_and_moves(out))   # Pillar 4: the social fields, couples, who may transfer
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
          ('store', 'Crew store', 'The crew store on Deck 3: snacks, soap, socks and the odd luxury, from the counter by the till.'),
          ('garden', 'Garden', 'The hydroponics garden on Deck 3: herbs and greens for the galley, from first light to late evening.'),
          ('guest', 'Guests', 'Not crew: visitors who live aboard.')]
RANK_ORDER = ['captain', 'xo', 'chief', 'senior', 'officer', 'junior', 'guest']
RANK_WORDS = {'captain': 'Captain', 'xo': 'Executive Officer', 'chief': 'Department Chief', 'senior': 'Senior Officer', 'officer': 'Officer', 'junior': 'Junior Officer', 'guest': 'Guest'}
UNI_COL = {'command': '#b4453f', 'works': '#d6a53a', 'watch': '#d6a53a', 'survey': '#3f9a92', 'infirmary': '#3f9a92', None: '#8a8f9a'}
DECK2_ROOM = {'C': "the Captain's quarters", 'E': "the Envoy's guest cabin", 'B': "the visitors' suite", 'U': "the second visitors' cabin"}

def bed_words(b):
    if b.startswith('4-B'):
        room, berth = b[3:].split('-')
        return f'Deck 4, Bunk {room}, berth {berth}' + (' (the night-shift room)' if room == '8' else '')
    if b in ('4-01', '4-02', '4-03', '4-04', '4-07', '4-08'): return f'Deck 4, guest cabin {b}'
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
.b.night{background:rgba(122,143,208,.18);color:#c3cff2;border:1px solid rgba(122,143,208,.5)}
.b.you{background:rgba(214,165,58,.2);color:#f3d58f;border:1px solid rgba(214,165,58,.6)}
.bio{margin:6px 0;color:#dfe7e9}
dl{display:grid;grid-template-columns:1fr 1fr;gap:4px 10px;margin:0}
dt{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}
dd{margin:0;color:#cfd9dc}
.more{margin:7px 0 0;color:var(--muted);font-size:12.5px}
.tr{font-style:italic}
dl .wide{grid-column:1/-1}
.vis{width:100%;border-collapse:collapse;margin-top:12px;font-size:13px}.vis td,.vis th{border-top:1px solid var(--line);padding:5px 6px;text-align:left;vertical-align:top}.vis th{color:var(--muted);font-weight:500}
.hide{display:none}
footer{max-width:1100px;margin:24px auto;padding:0 16px;font-size:12px;color:var(--muted)}
</style>
</head>
<body>
<header>
  <h1>The crew of the CSV Wren</h1>
  <p class="sub">Everyone aboard, for Pillar 1 of the Living Ship. Grouped by department, most senior first. Each card shows when they work, their days off, where they sleep and where they work. <span class="b story">Story crew</span> are the hand-written characters. The coloured dot is their uniform: red for command, gold for operations, blue-green for sciences.</p>
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

# the galley teams in words; their hours are the galley engineer's (GALLEY_SHIFTS, section 16), so none are copied here
GALLEY_WORDS = {'chef': 'Galley chef: cooks before breakfast and again before dinner', 'early': 'Galley, early team: before breakfast to early afternoon',
                'late': 'Galley, late team: early afternoon through dinner'}
# habits in plain words, for the page
HABIT_WORDS = {'early-riser': 'early riser', 'late-sleeper': 'late sleeper', 'early-to-bed': 'early to bed', 'night-owl': 'night owl',
               'skips-breakfast': 'skips breakfast', 'late-diner': 'late diner', 'lingers-at-meals': 'lingers at meals',
               'window-seat': 'likes a window seat', 'workaholic': 'workaholic', 'tea-break': 'takes a tea break', 'gym-regular': 'gym regular',
               'garden-lover': 'sits in the garden', 'lounge-regular': 'lounge regular', 'quiet-corner': 'finds a quiet corner',
               'common-room': 'common-room regular', 'music': 'music-room evenings', 'calls-home': 'calls home',
               'evening-shower': 'showers at night', 'runner': 'runs on the treadmill', 'shopper': 'shops at the store',
               'musician': 'plays in the music room', 'gardener': 'tends the garden', 'bar-regular': 'drinks at the lounge bar',
               'stargazer': 'stargazes in the observatory'}
assert set(HABIT_WORDS) == set(HABITS)

def bday_words(d):
    return 'Day %d: the %s of week %d' % (d, ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][(d - 1) % 7], (d - 1) // 7 + 1)

THEME_WORDS = {'homesick': 'homesick', 'exams': 'exam nerves', 'family': 'family worry', 'stuck': 'feeling stuck', 'notgood': 'not good enough',
               'lonely': 'lonely in a crowd', 'loss': 'an old loss', 'talent': 'a secret talent', 'burnout': 'burning out', 'leaving': 'leaving soon?',
               'rivalry': 'an old rivalry', 'startover': 'starting over'}
def social_words(x, entries):
    if not x.get('tpl'): return 'you'
    th = x['thread']; th = 'their own story' if th.startswith('arc:') else THEME_WORDS[th]
    w = '%s voice, %s; loves %s, likes %s; joy: %s; from %s, with %s; struggle: %s; keepsake: %s' % (
        x['tpl'], x['openness'], ' and '.join(x['loves']), ' and '.join(x['likes']), x['joy'], x['home'], x['family'], th, x['keepsake'])
    if x.get('partner'): w += '. Partner: ' + next(y['name'] for y in entries if y['id'] == x['partner'])
    return w + ('. Stays aboard.' if x.get('stays') else '. Could be posted to %s.' % x['transferTo'] if x.get('transferTo') else '.')

def page(entries, visits=None, reserve=None, rotations=None):
    e = lambda s: html.escape(str(s))
    from collections import Counter
    crew = [x for x in entries if x['rank'] != 'guest']
    out = [PAGE_HEAD]
    rc = Counter(x['rank'] for x in crew); sc = Counter(x['shift'] for x in crew)
    beds = Counter('d2' if x['bed'].startswith('2-') else 'cab' if not x['bed'].startswith('4-B') else 'bunk' for x in crew)
    out.append('  <div class="summary"><b>%d crew</b>, you included, plus Envoy Saruth as a guest. %d Captain, %d Executive Officer, %d Department Chiefs, %d Senior Officers, %d Officers and %d Junior Officers. '
               '%d work days and %d work nights. Everyone has two days off in a row, staggered round the week so every department always has people on, and a birthday: about one falls each week. '
               'Beds: %d in the senior quarters on Deck 2, %d in officers\' cabins on Deck 4 and %d in the junior bunk rooms on Deck 4 (eight rooms of six berths, with one spare berth in Bunk 1).</div>\n</header>\n'
               % (len(crew), rc['captain'], rc['xo'], rc['chief'], rc['senior'], rc['officer'], rc['junior'], sc['day'], sc['night'], beds['d2'], beds['cab'], beds['bunk']))
    out.append('<div class="bar">' + ' '.join('<a href="#%s">%s</a>' % (k, e(t)) for k, t, _ in GROUPS) + '</div>\n')
    out.append('<div class="bar"><input id="q" type="search" placeholder="Find someone: a name, a job, a word" aria-label="Find someone"><label><input id="nights" type="checkbox"> Night shift only</label></div>\n<main>\n')
    for key, title, blurb in GROUPS:
        ppl = sorted([x for x in entries if x['dept'] == key], key=lambda x: (RANK_ORDER.index(x['rank']), not x.get('player'), x['name'].split()[-1]))
        if not ppl: continue
        out.append('<section class="dept" id="%s"><h2>%s <span class="n">%d %s</span></h2><p class="blurb">%s</p><div class="grid">\n' % (key, e(title), len(ppl), 'person' if len(ppl) == 1 else 'people', e(blurb)))
        for x in ppl:
            badges = (' <span class="b you">You</span>' if x.get('player') else '') + (' <span class="b story">Story crew</span>' if x.get('story') else '') + \
                     (' <span class="b night">Night shift</span>' if x['shift'] == 'night' else '')
            off = ' and '.join(DAYS[d] for d in x['rota']['offDays']) or 'none'
            work = (WORK_WORDS[x['work']['place']] + ' (Deck %d)' % x['work']['deck']) if x['work'] else 'no ship duties'
            shift = GALLEY_WORDS[x['rota']['team']] if x['dept'] == 'galley' else \
                    ('Days, 08:00 to 17:00' if x['shift'] == 'day' else 'Nights, 21:00 to 06:00') if not x['rota'].get('hours') else \
                    ' and '.join('%02d:%02d to %02d:%02d' % (a // 60, a % 60, b // 60 % 24, b % 60) for a, b in x['rota']['hours'])
            for o in x['rota'].get('hoursOn', []):
                shift += '; %s: %s' % (' and '.join(DAYS[d] for d in o['days']), ' and '.join('%02d:%02d to %02d:%02d' % (a // 60, a % 60, b // 60 % 24, b % 60) for a, b in o['hours']))
            out.append('<article class="p" data-text="%s" data-shift="%s"><i class="dot" style="background:%s"></i>\n'
                       '  <div class="who"><b>%s</b>%s<span class="role">%s%s</span></div>\n'
                       '  <p class="bio">%s</p>\n'
                       '  <dl><div><dt>Shift</dt><dd>%s</dd></div><div><dt>Days off</dt><dd>%s</dd></div><div><dt>Sleeps</dt><dd>%s</dd></div><div><dt>Works</dt><dd>%s</dd></div><div><dt>Birthday</dt><dd>%s</dd></div><div class="wide"><dt>Habits</dt><dd>%s</dd></div><div class="wide"><dt>Might change</dt><dd>%s</dd></div><div class="wide"><dt>Social</dt><dd>%s</dd></div>%s</dl>\n'
                       '  <p class="more">%s <span class="tr">%s</span></p></article>\n'
                       % (e((x['name'] + ' ' + x['role'] + ' ' + x['bio'] + ' ' + ' '.join(x['habits'])).lower()), x['shift'], UNI_COL[x['uniform']], e(x['name']), badges,
                          e(x['role'] + (', and cook on the chef\'s days off' if x['rota'].get('cover') else '')), (', ' + e(RANK_WORDS[x['rank']])) if RANK_WORDS[x['rank']].lower() not in x['role'].lower() else '', e(x['bio']), shift, off, e(bed_words(x['bed'])), e(work), e(bday_words(x['birthday'])), e(', '.join(HABIT_WORDS[h] for h in x['habits']).capitalize() or 'none yet'), e(' '.join(i['why'] for i in x.get('habitShifts', [])) or 'you decide'), e(social_words(x, entries)),
                          ''.join('<div class="wide"><dt>Tells %s</dt><dd>%s</dd></div>' % (['anyone', 'an acquaintance', 'a colleague', 'a friend', 'a close friend'][t], e(' '.join(a['text'] for a in x['about'] if a['tier'] == t))) for t in sorted({a['tier'] for a in x.get('about', [])})),
                          e(' '.join(x['life'])), e((', '.join(x['traits']).capitalize() + '.') if x['traits'] else '')))
        out.append('</div></section>\n')
    if reserve:
        out.append('<section class="dept" id="reserve"><h2>The reserve pool <span class="n">%d future crew</span></h2>'
                   '<p class="blurb">Crew who will join the Wren on rotation days (a Sunday shuttle about every six ship weeks, from week 5); the same number leave. A third of them are new cadets, like you.</p><div class="grid">\n' % len(reserve))
        for x in reserve:
            out.append('<article class="p" data-text="%s" data-shift="%s"><i class="dot" style="background:%s"></i>\n'
                       '  <div class="who"><b>%s</b>%s<span class="role">%s</span></div>\n  <p class="bio">%s</p>\n'
                       '  <dl><div><dt>Arrives</dt><dd>Day %d</dd></div><div><dt>Birthday</dt><dd>%s</dd></div><div class="wide"><dt>Social</dt><dd>%s</dd></div>%s</dl>\n'
                       '  <p class="more">%s</p></article>\n'
                       % (e((x['name'] + ' ' + x['role']).lower()), x['shift'], UNI_COL[x['uniform']], e(x['name']), ' <span class="b you">New cadet</span>' if x['cadet'] else '',
                          e(x['role']), e(x['bio']), x['aboard'][0], e(bday_words(x['birthday'])), e(social_words(x, entries + reserve)),
                          ''.join('<div class="wide"><dt>Tells %s</dt><dd>%s</dd></div>' % (['anyone', 'an acquaintance', 'a colleague', 'a friend', 'a close friend'][t], e(' '.join(a['text'] for a in x['about'] if a['tier'] == t))) for t in sorted({a['tier'] for a in x['about']})),
                          e(' '.join(x['life']))))
        out.append('</div></section>\n')
    if visits:
        ev = [v for v in visits if v.get('event')]; every = [v for v in visits if not v.get('event')]
        out.append('<section class="dept" id="visitors"><h2>Visitors <span class="n">%d event guests, %d everyday visitors a year</span></h2>'
                   '<p class="blurb">Guests who stay a while and leave. Event guests come with a ship-wide event (the day is the event\'s); everyday visitors arrive about once a week. '
                   'Deck 2\'s second visitors\' cabin is kept for event visitors; on Deck 4, event guests use cabins 4-01 to 4-04 and everyday visitors 4-07 and 4-08.</p><div class="grid">\n' % (len(ev), len(every)))
        EVW = {'diplomatic': 'The diplomatic visit', 'nebula': 'Nebula drift', 'veyliVessel': 'A Veyli vessel needs help', 'salvage': 'Salvage'}
        for x in ev:
            out.append('<article class="p" data-text="%s" data-shift="day"><i class="dot" style="background:%s"></i>\n'
                       '  <div class="who"><b>%s</b> <span class="b story">%s</span><span class="role">%s</span></div>\n  <p class="bio">%s</p>\n'
                       '  <dl><div><dt>Stays</dt><dd>%d days, in %s</dd></div><div><dt>Kind</dt><dd>%s</dd></div><div class="wide"><dt>Habits</dt><dd>%s</dd></div></dl>\n'
                       '  <p class="more">%s</p></article>\n'
                       % (e((x['name'] + ' ' + x['role'] + ' ' + x['bio']).lower()), x['spec'].get('outfit') or UNI_COL[x['uniform']], e(x['name']), e(EVW[x['event']]), e(x['role']),
                          e(x['bio']), x['stay'], e(bed_words(x['cabin'])), e(x['template']), e(', '.join(HABIT_WORDS[h] for h in x['habits']).capitalize()), e(' '.join(x['life']))))
        out.append('</div><table class="vis"><tr><th>Arrives</th><th>Leaves</th><th>Who</th><th>Cabin</th></tr>\n' + ''.join(
            '<tr><td>Day %d</td><td>Day %d</td><td><b>%s</b>, %s. %s</td><td>%s</td></tr>\n' % (x['arrive'], x['leave'], e(x['name']), e(x['role'].lower()), e(x['bio']), x['cabin'])
            for x in every) + '</table></section>\n')
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
    visits = visitors(entries)
    reserve_pool, rotations = reserve(entries + visits)
    block = ('// ---- BEGIN ROSTER (generated by plans/crew-roster-gen.py: fixed data; to change the crew, edit the generator and re-run it) ----\n'
             'const HABITS = ' + json.dumps(HABITS, ensure_ascii=False, indent=2) + ';\n'
             'const ROSTER = [\n' + js(crew) + '\n];\n'
             'const ROSTER_GUESTS = [\n' + js(guests) + '\n];\n'
             'const ROSTER_PLAYER = ' + json.dumps(you, ensure_ascii=False, separators=(', ', ': ')) + ';\n'
             '// visitors (Pillar 3, C8): inert data; the sim engineer schedules them, the events engineer sets event guests\' days\n'
             'const GUEST_TEMPLATES = ' + json.dumps(GUEST_TEMPLATES, ensure_ascii=False, separators=(', ', ': ')) + ';\n'
             'const GUESTS = [\n' + js(visits) + '\n];\n'
             '// the reserve pool (Pillar 4): future crew, off the ship until their rotation day; aboard: [fromDay, toDay]\n'
             'const ROSTER_RESERVE = [\n' + js(reserve_pool) + '\n];\n'
             '// crew rotation days (Sundays): `out` crew leave (the sim picks who, 10 days ahead) and the reserve ids in `in` arrive\n'
             'const ROSTER_ROTATIONS = ' + json.dumps(rotations, ensure_ascii=False, separators=(', ', ': ')) + ';\n'
             '// ---- END ROSTER ----\n')
    game = os.path.join(here, '..', 'starship-cadet.html'); g = open(game).read()
    a = g.index('// ---- BEGIN ROSTER'); b = g.index('// ---- END ROSTER ----\n') + len('// ---- END ROSTER ----\n')
    open(game, 'w').write(g[:a] + block + g[b:])
    open(os.path.join(here, 'crew-roster.html'), 'w').write(page(entries, visits, reserve_pool, rotations))
    print('74 crew + you = 75, + %d guest; ranks %s; shifts %s; made way for you: %s. Wrote section 9 of starship-cadet.html and plans/crew-roster.html' % (len(guests), dict(rc), dict(sc), DROPPED))
