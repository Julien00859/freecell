import random
import sys
from argparse import ArgumentParser
from curses import wrapper
from freecell.tui import main
from freecell.game import Game
from time import time

parser = ArgumentParser()
parser.add_argument("--debug", action="store_true", default=False)
parser.add_argument("--seed", action="store", type=int, default=None)
options = parser.parse_args()
seed = options.seed or int(time())
random.seed(seed)
print("Game seed:", seed)

wrapper(main, Game(), debug=options.debug)
