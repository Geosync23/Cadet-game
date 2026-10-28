# plant one failure into a copy of the game: plant.py KIND OUT
import sys
s = open('/home/user/Cadet-game/starship-cadet.html', encoding='utf-8').read()
anchor = '// 5. LIGHTING\n'
add = {
  'parse':  'function broken( {\n',
  'func':   'function lineFor(a) { return a; }\n',
  'app':    "deviceApp({ id: 'home', title: 'Home again', view: () => '' });\n",
  'tkey':   'M.planted = 1;\nM.planted = 2;\n',
  'gated':  "if (REC_DECK) { REC_SHOWS.planted = 1; }\nREC_SHOWS.planted = 2;\n",
  'push':   "const PLANT_LIST = [];\nPLANT_LIST.push({ id: 'x' });\nPLANT_LIST.push({ id: 'x' });\n",
  'let':    'let plantedTwice = 1;\nlet plantedTwice = 2;\n',
  'deck7':  "const PLANT_TEXT = 'Welcome to Deck 7';\n",
}[sys.argv[1]]
assert s.count(anchor) == 1
open(sys.argv[2], 'w', encoding='utf-8').write(s.replace(anchor, anchor + add))
