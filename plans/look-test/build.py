# Builds tea-corner-look-test.html: the page source with the exported room data put inside it.
#   python3 plans/look-test/build.py
import pathlib
here = pathlib.Path(__file__).parent
src = (here / 'look-test.src.html').read_text()
data = (here / 'tea-corner.json').read_text().replace('</', '<\\/')
(here / 'tea-corner-look-test.html').write_text(src.replace('/*TEA_DATA*/', data))
print('built', round(len(src) / 1024), 'KB of page +', round(len(data) / 1024), 'KB of room data')
