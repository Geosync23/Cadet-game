# Builds the publishable look-test pages: each page source with its exported room data put inside it.
#   python3 plans/look-test/build.py          -> bunk-room-look-test.html (the published page) and tea-corner-look-test.html
import pathlib
here = pathlib.Path(__file__).parent
for src, data, mark, out in [('bunk-room.src.html', 'bunk1.json', '/*ROOM_DATA*/', 'bunk-room-look-test.html'),
                             ('tea-corner.src.html', 'tea-corner.json', '/*TEA_DATA*/', 'tea-corner-look-test.html')]:
    s = (here / src).read_text(); d = (here / data).read_text().replace('</', '<\\/')
    (here / out).write_text(s.replace(mark, d))
    print('built', out, round(len(s) / 1024), 'KB of page +', round(len(d) / 1024), 'KB of room data')
