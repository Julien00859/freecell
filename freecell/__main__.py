import random
import sys
from argparse import ArgumentParser
from base64 import b64encode, b64decode
from curses import wrapper
from freecell.tui import main
from freecell.game import Game
from time import time

parser = ArgumentParser()
parser.add_argument("--debug", action="store_true", default=False)
parser.add_argument("--seed", action="store", type=int, default=None)
parser.add_argument("--restore", action="store")
options = parser.parse_args()
seed = options.seed or int(time())
random.seed(seed)
print("Game seed:", seed)
if options.restore:
    freeze = b64decode(options.restore.encode())
    game = Game.restore(freeze)
else:
    game = Game()

wrapper(main, game, debug=options.debug)
if not game.won:
    print("Freeze:", b64encode(game.freeze()).decode())
