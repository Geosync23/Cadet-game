# Appointments (0.92.6 item 9): the words

SW2, 2026-10-25, from the appointments pitch (plans/appointments-pitch.html on claude/appointments-pitch; the user's
answers in its db at answers/user). The user said yes to the cheap fix and to nine appointments, no to the spare helm
chair, and: "Appointments work almost exactly the same as ship traditions but are usually one on one or very small
group." So each file here reads like a `.trad` file (fields, then `==` text sections), sized for one to four people.
The builder (FX22) owns the reader; these are proposals in a shape a reader can follow. Nothing here is baked yet.

## Files

| File | Appointment | Starts it | Host | Size |
| --- | --- | --- | --- | --- |
| `talk-fix.lines` | The cheap fix: a real talk at every appointment | (any) | whoever you meet | 1-1 |
| `brennan-book.appt` | A page in Brennan's book | invite | Brennan | 1-1 |
| `night-round.appt` | The night round | invite | Kofi Mensah | 1-1 |
| `shadow.appt` | An hour in another department | you ask | a colleague in another department (5 places) | 1-1 |
| `teach-me.appt` | Teach me your thing | you ask | someone whose hobby it is (4 people) | 1-1 |
| `show-tell.appt` | Show and tell | invite (the cabin visit) | an officer friend (4 people) | 1-1 |
| `scope.appt` | Your turn at the big scope | you ask | Dr. Sato | 1-1 |
| `garden-bed.appt` | A bed of your own | invite | Tove Cruz | 1-1, then short visits |
| `rehearse.appt` | Help me rehearse | invite | a friend before their big thing (3 people) | 1-1 |
| `midnight-feast.appt` | Midnight feast | you ask | your bunkmates | 3-5 |

## The fields (the `.trad` ones where they fit)

| Field | Means |
| --- | --- |
| `@appointment <id>` | first line |
| `title:` | what the Appointments app and the Calendar call it |
| `starts:` | `invite` (they ask you, once a gate is met) or `ask` (a line in the app's new "What for?" list) |
| `host:` | a crew id, or `per-host` when the file has one scene per person (`== scene <id>`) |
| `gate:` | when it's offered, in the lines' condition words (`tier>=friend`, `!flag:...`) |
| `when:` / `at:` | the day rule and the time window, as in `.trad` files (proposals; the builder may move them to fit the day) |
| `where:` | as in `.trad` files: `<deck> room <Room>: <place type>` or `<deck> pool <pool>` |
| `who:` | who comes (`host` and `you`; a group names its rule) |
| `once:` | `yes` (once a game), or how often it can be booked again |
| `mem:` / `flag:` | set when it's kept (memory `appt.<id>`; flags for what follows) |
| `record:` | the line for your Record (the device), if any |
| `where <id>:` / `at <id>:` | in a `per-host` file, that host's place and hour |

## The text sections

| Section | When | Cap |
| --- | --- | --- |
| `== invite` | the host's invitation (bubble or chat card), for `starts: invite` | 90 |
| `== ask` | the "What for?" entry (first line) and the host's yes (the rest), for `starts: ask` | 90 |
| `== busy` | the host can't this time (kind; "ask me Thursday") | 90 |
| `== mail` | the Calendar note the evening before or on booking | 200 |
| `== scene` | the scripted moment when you're both there, in the meeting format (`id: text   [pose]`, `? choice`, `* reply   flavour:... mem:...`, the answer indented); per-host files use `== scene <id>` | 140 a line, 4-10 lines |
| `== here` | bubbles while it's on, if it runs long (walks, visits) | 60 |
| `== thanks` | the toast when it's done | 140 |
| `== after` | what they say later, once (`told:`), about it; `== after <id>` per host | 90 |
| `== stops` / `== tend` / `== harvest` | lines said in order at each step of a longer one (the night round's decks; the garden bed's visits and its harvest), in the scene format | 140 |

Placeholders are only the ones lines_check already knows ({me}, {name}, {first}, {dish}, {thing}, {time}, {weekday},
{room}, {deck}, {hobby}...), plus voice tokens ({hi}, {bye}, {yes}, {thanks}, {nick}). Never "Deck 7" on screen.
