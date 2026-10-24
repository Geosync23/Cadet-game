# Small repairs: line keys (FX10, patch 0.92.3 items 21 and 24)

The small repairs Calder puts on the job board (section 17, `FIX_ROWS` and `fixPost`). Each is a real fitting, not a
machine: a stand spot, a part (or none), a tool and three lines. The game works with the plain titles below until the
words land. The title is read when the job is posted; the sign and done lines when you get to them.

File: `content/works/fixes.lines` (header `@bank all`, texts said by nobody, like faults.lines).

| Key | What | Notes |
| --- | --- | --- |
| `fix.<id>.title` | the job board card and the job's name everywhere (Tracked, toasts) | an order, short: about 40 characters at most (the board on the wall squeezes longer ones). Name the room only when the same thing is in several rooms on one deck; the card adds the deck and room itself. No deck numbers |
| `fix.<id>.sign` | what you see or hear when you get there, shown as you start the work | one sentence, only what's there to notice ("The tap drips into the sink, slow and steady.") |
| `fix.<id>.done` | one short line when it's done, before "Turn it in at the job board" | what's different now, plain ("Not a drop.") |

Parked (in the table and the words, never posted: the machine shop's and main storage's spots are those rooms' own taps): sh-lamp, sh-press, sh-grinder, st-ladder, st-light, st-scanner.

One line per key is enough; a key with several lines uses the first (no rotation). Tools are said by the game ("with a
hex key"); don't repeat the tool in the title. Science rows (Deck 2) come up most often: write those first.

| id | deck | room | part | tool | plain title |
| --- | --- | --- | --- | --- | --- |
| wo-screen | 2 | Watch office | - | a pin driver | Reseat a flickering watch screen |
| wo-chair | 2 | Watch office | - | a hex key | Tighten a wobbly watch chair |
| wo-blind | 2 | Watch office | - | a screwdriver | Free a stuck glass blind |
| wo-lamp | 2 | Watch office | lamp | a step stool | Replace a desk lamp in the Watch office |
| wo-jack | 2 | Watch office | cable | a crimper | Rewire a crackling headset jack |
| wo-vent | 2 | Watch office | - | a vent brush | Clear a rattling ceiling vent |
| wo-clock | 2 | Watch office | - | a pin driver | Reset the drifting watch clock |
| cr-table | 2 | Chart room | lamp | a step stool | Replace the chart table backlight |
| cr-drawer | 2 | Chart room | - | a hex key | Free a jammed chart drawer |
| cr-plotter | 2 | Chart room | bearing | a pin driver | Fit a new bearing in the plotter arm |
| cr-projector | 2 | Chart room | - | a lens cloth and a hex key | Realign the star projector |
| cr-shelf | 2 | Chart room | - | a hex key | Fix a sagging chart shelf |
| cr-seat | 2 | Chart room | - | a screwdriver | Fix a loose window-seat hinge |
| cr-reading | 2 | Chart room | lamp | a step stool | Replace a reading lamp in the chart room |
| cr-hum | 2 | Chart room | - | a multimeter | Find the hum in the chart room sockets |
| sl-fume | 2 | Survey lab | fan belt | a spanner | Fit a new belt on a fume hood fan |
| sl-spectro | 2 | Survey lab | - | a lens cloth and a hex key | Realign a spectrometer mount |
| sl-tap | 2 | Survey lab | seal | a basin wrench | Fix a dripping lab tap |
| sl-socket | 2 | Survey lab | - | a multimeter | Reset a tripped bench socket |
| sl-stool | 2 | Survey lab | - | a hex key | Tighten a wobbly lab stool |
| sl-lamp | 2 | Survey lab | lamp | a step stool | Replace a bench lamp in the Survey lab |
| sl-screen | 2 | Survey lab | cable | a crimper | Replace a frayed screen cable |
| sl-eyewash | 2 | Survey lab | valve | a spanner | Fix the eyewash station valve |
| sl-cabinet | 2 | Survey lab | - | a screwdriver | Adjust a sticking cabinet door |
| sl-centrifuge | 2 | Survey lab | bearing | a pin driver | Fit a bearing in a whining centrifuge |
| sl-gastap | 2 | Survey lab | seal | a leak spray | Reseal a hissing gas tap |
| sl-hoodlamp | 2 | Survey lab | lamp | a step stool | Replace a fume hood lamp |
| sl-balance | 2 | Survey lab | - | a test weight | Level and zero a lab balance |
| sm-fridge | 2 | Sample lab | seal | a screwdriver | Replace a sample fridge door seal |
| sm-freezer | 2 | Sample lab | - | a multimeter | Fix a freezer alarm that goes off for nothing |
| sm-glovebox | 2 | Sample lab | seal | a glove-port ring tool | Change a split glove on the glove box |
| sm-scope | 2 | Sample lab | lamp | a small screwdriver | Replace a microscope lamp |
| sm-sink | 2 | Sample lab | - | a drain rod | Clear a slow lab sink |
| sm-rack | 2 | Sample lab | - | a hex key | Fix a rattling sample rack |
| sm-printer | 2 | Sample lab | cable | a crimper | Repair a label printer cable |
| sm-cleanbench | 2 | Sample lab | fan belt | a spanner | Fit a new belt on the clean bench fan |
| sm-panel | 2 | Sample lab | lamp | a step stool | Replace a flickering ceiling panel in the sample lab |
| sm-incubator | 2 | Sample lab | - | a multimeter | Recalibrate a drifting incubator |
| cm-card | 2 | Comms room | - | a pin driver | Reseat a loose console card |
| cm-lead | 2 | Comms room | cable | a crimper | Rewire a headset lead |
| cm-chair | 2 | Comms room | - | a hex key | Fix a comms chair that sinks |
| cm-patch | 2 | Comms room | cable | a cable tester | Replace a patch panel lead |
| cm-fan | 2 | Comms room | bearing | a pin driver | Quiet a buzzing rack fan |
| cm-booth | 2 | Comms room | seal | a screwdriver | Reseal the quiet booth door |
| cm-lamp | 2 | Comms room | lamp | a step stool | Replace a desk lamp in the comms room |
| cm-screen | 2 | Comms room | - | a lens cloth and a hex key | Realign a call-home screen |
| cm-mic | 2 | Comms room | - | a small screwdriver | Fix a crackling microphone arm |
| cm-clocks | 2 | Comms room | - | a pin driver | Set the wall clocks to ship time |
| ob-mount | 2 | Observatory | bearing | a pin driver | Fit a bearing in the telescope mount |
| ob-dimmer | 2 | Observatory | - | a multimeter | Fix the dimmer for star nights |
| ob-shutter | 2 | Observatory | - | a hex key | Free a sticky window shutter |
| ob-cushion | 2 | Observatory | - | a screwdriver | Fix a loose window-seat clip |
| ob-floor | 2 | Observatory | - | a multimeter | Reset a cold floor heater |
| ob-redlamp | 2 | Observatory | lamp | a step stool | Replace a red night lamp |
| ob-eyepiece | 2 | Observatory | - | a lens cloth | Clean and refit the eyepiece rack |
| sc-door | 2 | Science corridor | - | a screwdriver | Adjust a slow lab door |
| sc-sign | 2 | Science corridor | lamp | a step stool | Replace a lamp in the lab sign |
| sc-panel | 2 | Science corridor | - | a hex key | Refit a loose wall panel |
| sc-vent | 2 | Science corridor | - | a vent brush | Clear a whistling vent |
| sc-notice | 2 | Science corridor | cable | a crimper | Fix the notice screen by the labs |
| sc-light | 2 | Science corridor | lamp | a step stool | Replace a science corridor light |
| l2-call | 2 | Lift lobby | - | a pin driver | Fix a sticky lift call button |
| l2-bench | 2 | Lift lobby | - | a hex key | Tighten a loose bench by the lift |
| l2-planter | 2 | Lift lobby | - | a drain rod | Clear the planter's drip tray |
| w2-tap | 2 | Washroom | seal | a basin wrench | Fix a dripping tap in the science washroom |
| w2-cistern | 2 | Washroom | valve | a spanner | Fix a running cistern in the science washroom |
| d1-blind | 1 | Observation room | - | a hex key | Free a sticky blind in the observation room |
| d1-urn | 1 | Observation room | - | a descaler | Descale the observation room urn |
| d1-screen | 1 | Observation room | cable | a crimper | Fix the conference screen lead |
| d1-chair | 1 | Observation room | - | a hex key | Fix a creaky conference chair |
| d1-lamp | 1 | Observation room | lamp | a step stool | Replace a window lamp |
| d1-call | 1 | Bridge lobby | - | a pin driver | Fix a sticky lift call button |
| d1-ready | 1 | Ready room | lamp | a step stool | Replace the ready room desk lamp |
| d1-tap | 1 | Bridge washroom | seal | a basin wrench | Fix a dripping tap in the bridge washroom |
| d1-helm | 1 | Bridge | - | a pin driver | Reseat a loose helm screen |
| d1-swivel | 1 | Bridge | - | a hex key | Fix a stiff bridge chair swivel |
| d1-ops | 1 | Bridge | cable | a crimper | Replace a frayed console lead |
| p3-call | 3 | Lift plaza | - | a pin driver | Fix a sticky lift call button |
| p3-bench | 3 | Lift plaza | - | a hex key | Tighten a loose plaza bench |
| p3-down | 3 | Lift plaza | lamp | a step stool | Replace a plaza downlight |
| pr-bench | 3 | Promenade | - | a hex key | Fix a wobbly promenade bench |
| pr-lamp | 3 | Promenade | lamp | a step stool | Replace a promenade lamp |
| pr-blind | 3 | Promenade | - | a screwdriver | Free a jammed window blind |
| pr-drip | 3 | Promenade | - | a drain rod | Clear a blocked planter drip line |
| pr-vent | 3 | Promenade | - | a vent brush | Clear a rattling vent |
| pr-rail | 3 | Promenade | - | a spanner | Tighten a loose hand rail |
| ms-table | 3 | Mess hall | - | a hex key | Level a wobbly mess table |
| ms-chair | 3 | Mess hall | - | a hex key | Fix a squeaky mess chair |
| ms-grab | 3 | Mess hall | lamp | a step stool | Replace the grab shelf light |
| ms-menu | 3 | Mess hall | cable | a crimper | Fix the menu screen's lead |
| ms-trayrack | 3 | Mess hall | - | a spanner | Straighten a bent tray rack |
| ga-sink | 3 | Galley | seal | a basin wrench | Fix a dripping prep sink |
| ga-fridge | 3 | Galley | seal | a screwdriver | Replace a worn fridge door seal |
| ga-drawer | 3 | Galley | bearing | a hex key | Fix a stiff drawer runner |
| ga-heatlamp | 3 | Galley | lamp | a step stool | Replace a heat lamp at the pass |
| ga-shelf | 3 | Galley | - | a spanner | Fix a loose shelf bracket |
| bl-tap | 3 | Bow lounge | seal | a basin wrench | Fix the bar's sticky drinks tap |
| bl-sofa | 3 | Bow lounge | - | a hex key | Fix a sagging sofa |
| bl-lamp | 3 | Bow lounge | lamp | a step stool | Replace a table lamp in the bow lounge |
| bl-reader | 3 | Bow lounge | cable | a crimper | Fix the card reader at the bar |
| bl-blind | 3 | Bow lounge | - | a screwdriver | Free a jammed window blind |
| bl-speaker | 3 | Bow lounge | cable | a crimper | Fix a crackling lounge speaker |
| gd-hose | 3 | Hydroponics garden | seal | a spanner | Fix a dripping hose reel |
| gd-trolley | 3 | Hydroponics garden | bearing | a hex key | Fix a sticky trolley wheel |
| gd-mister | 3 | Hydroponics garden | - | a pin driver | Clear a blocked misting nozzle |
| gd-lamp | 3 | Hydroponics garden | lamp | a step stool | Replace a potting bench lamp |
| gd-bench | 3 | Hydroponics garden | - | a spanner | Tighten a loose potting bench |
| in-rail | 3 | Infirmary | - | a hex key | Fix a stiff bed side rail |
| in-light | 3 | Infirmary | lamp | a step stool | Replace a reading light over a bed |
| in-call | 3 | Infirmary | cable | a crimper | Fix a call button by a bed |
| in-chair | 3 | Infirmary | - | a hex key | Fix a wobbly visitor chair |
| ex-lamp | 3 | Exam room | lamp | a step stool | Replace an exam lamp |
| ex-couch | 3 | Exam room | - | a spanner | Fix the exam couch lever |
| w3-tap | 3 | Washrooms | seal | a basin wrench | Fix a dripping tap in the washrooms |
| w3-cistern | 3 | Washrooms | valve | a spanner | Fix a running cistern in the washrooms |
| w3-dryer | 3 | Washrooms | - | a multimeter | Reset a hand dryer |
| gy-rower | 3 | Gym | bearing | a pin driver | Fix a squeaking rowing machine |
| gy-bench | 3 | Gym | - | a hex key | Tighten a weight bench |
| gy-tread | 3 | Gym | - | a hex key | Adjust a slipping treadmill belt |
| gy-lamp | 3 | Gym | lamp | a step stool | Replace a gym light |
| gy-fountain | 3 | Gym | valve | a spanner | Fix the gym water fountain |
| cs-till | 3 | Crew store | - | a screwdriver | Fix a sticky till drawer |
| cs-shelf | 3 | Crew store | lamp | a step stool | Replace a shelf light in the crew store |
| cs-reader | 3 | Crew store | cable | a crimper | Fix the crew store's card reader |
| cb-headset | 3 | Call-home booths | cable | a crimper | Fix a call-home booth headset |
| cb-door | 3 | Call-home booths | seal | a screwdriver | Reseal a call-home booth door |
| cb-light | 3 | Call-home booths | lamp | a step stool | Replace a light by the call-home booths |
| co-curtain | 3 | Cold store | - | a spanner | Rehang the cold store strip curtain |
| l4-call | 4 | Lift lobby | - | a pin driver | Fix a sticky lift call button |
| l4-bench | 4 | Lift lobby | - | a hex key | Tighten a loose bench by the lift |
| l4-lamp | 4 | Lift lobby | lamp | a step stool | Replace a lift lobby downlight |
| jc-kettle | 4 | Junior common room | - | a descaler | Descale the common room kettle |
| jc-sofa | 4 | Junior common room | - | a hex key | Fix a sagging common room sofa |
| jc-lamp | 4 | Junior common room | lamp | a step stool | Replace a common room lamp |
| jc-table | 4 | Junior common room | - | a spanner | Fix the games table leg |
| jc-screen | 4 | Junior common room | cable | a crimper | Fix the screen's loose lead |
| jc-blind | 4 | Junior common room | - | a screwdriver | Free a sticky window blind |
| mu-stand | 4 | Music room | - | a hex key | Tighten a loose music stand |
| mu-player | 4 | Music room | bearing | a small screwdriver | Fix the record player's tone arm |
| mu-lamp | 4 | Music room | lamp | a step stool | Replace a music room lamp |
| mu-amp | 4 | Music room | cable | a crimper | Fix a buzzing amp lead |
| la-catch | 4 | Laundry | - | a screwdriver | Fix a sticky dryer door catch |
| la-lamp | 4 | Laundry | lamp | a step stool | Replace a laundry room lamp |
| la-table | 4 | Laundry | - | a spanner | Fix a folding table leg |
| la-lint | 4 | Laundry | - | a vent brush | Clear a clogged lint trap |
| wp-shower | 4 | Port washroom | seal | a spanner | Fix a dripping shower head |
| wp-tap | 4 | Port washroom | seal | a basin wrench | Fix a loose basin tap |
| wp-rail | 4 | Port washroom | - | a multimeter | Fix a cold towel rail |
| wq-cold | 4 | Starboard washroom | valve | a spanner | Fix a shower that runs cold |
| wq-cistern | 4 | Starboard washroom | valve | a spanner | Fix a running cistern |
| wq-mirror | 4 | Starboard washroom | lamp | a step stool | Replace a mirror light |
| wb-vice | 5 | Works bay | - | a spanner | Fix a vice that won't grip |
| wb-lamp | 5 | Works bay | lamp | a step stool | Replace a bench lamp in the Works bay |
| wb-rail | 5 | Works bay | - | a spanner | Rehang the tool wall rail |
| wb-stool | 5 | Works bay | - | a hex key | Fix a wobbly stool |
| wb-socket | 5 | Works bay | - | a multimeter | Reset a tripped bench socket |
| wo-closer | 5 | Works Chief's office | - | a screwdriver | Adjust the office door closer |
| tc-urn | 5 | Tea corner | - | a descaler | Descale the tea urn |
| tc-table | 5 | Tea corner | - | a hex key | Fix a wobbly tea table |
| w5-tap | 5 | Works washroom | seal | a basin wrench | Fix a dripping tap in the Works washroom |
| w5-cistern | 5 | Works washroom | valve | a spanner | Fix a running cistern in the Works washroom |
| st-ladder | 5 | Main storage | bearing | a hex key | Fix a sticky shelf ladder wheel |
| st-light | 5 | Main storage | lamp | a step stool | Replace an aisle light |
| st-scanner | 5 | Main storage | cable | a crimper | Fix the parts scanner's lead |
| sh-press | 5 | Machine shop | - | a spanner | Free a sticking drill press lever |
| sh-lamp | 5 | Machine shop | lamp | a step stool | Replace the lathe lamp |
| sh-hose | 5 | Machine shop | - | a screwdriver | Fix an extractor hose clamp |
| sh-grinder | 5 | Machine shop | fan belt | a spanner | Fit a new belt on the bench grinder |
| sb-floor | 5 | Shuttle bay | lamp | a step stool | Replace a bay floor light |
| sb-ring | 5 | Shuttle bay | - | a spanner | Free a stiff tie-down ring |
| sb-beacon | 5 | Shuttle bay | relay | a pin driver | Fix a bay warning beacon |
| bc-screen | 5 | Bay control booth | - | a pin driver | Reseat a flickering booth screen |
| l5-call | 5 | Lift lobby | - | a pin driver | Fix a sticky lift call button |
| l5-lamp | 5 | Lift lobby | lamp | a step stool | Replace a lift lobby downlight |
| l6-call | 6 | Lift lobby | - | a pin driver | Fix a sticky lift call button |
| l6-bench | 6 | Lift lobby | - | a hex key | Tighten a loose bench by the lift |
| l6-lamp | 6 | Lift lobby | lamp | a step stool | Replace a lift lobby downlight |
| eo-rail | 6 | Engine overlook | - | a spanner | Tighten the overlook hand rail |
| eo-lamp | 6 | Engine overlook | lamp | a step stool | Replace an overlook lamp |
| ec-chair | 6 | Engine control | - | a hex key | Fix a stiff control room chair |
| ew-lamp | 6 | Engine watch room | lamp | a step stool | Replace a desk lamp in the watch room |
| ew-jack | 6 | Engine watch room | cable | a crimper | Fix a loose headset jack |
| rc-lamp | 7 | Concourse | lamp | a step stool | Replace a concourse lamp |
| rc-call | 7 | Lift lobby | - | a pin driver | Fix a sticky lift call button |
| au-stool | 7 | Auditorium | - | a hex key | Fix a wobbly stage stool |
| au-lectern | 7 | Auditorium | lamp | a small screwdriver | Fix the lectern's reading light |
| au-board | 7 | Auditorium | - | a spanner | Tighten a loose stage board |
| po-lounger | 7 | Pool | - | a hex key | Fix a stiff lounger hinge |
| po-lamp | 7 | Pool | lamp | a step stool | Replace a poolside lamp |
| rv-shower | 7 | River hall | seal | a spanner | Fix the beach shower tap |
| rv-cleat | 7 | River hall | - | a spanner | Tighten a loose kayak cleat |
| ch-locker | 7 | Changing rooms | - | a screwdriver | Free a jammed locker |
| ch-shower | 7 | Changing rooms | seal | a spanner | Fix a dripping shower head in the changing rooms |
| ch-lamp | 7 | Changing rooms | lamp | a step stool | Replace a changing room light |
