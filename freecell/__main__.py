import random
import sys
from argparse import ArgumentParser
from curses import wrapper
from freecell.tui import main
from freecell.game import Game

parser = ArgumentParser()
parser.add_argument("--debug", action="store_true", default=False)
parser.add_argument("--seed", action="store", type=int, default=None)
options = parser.parse_args()
if options.seed is not None:
    random.seed(options.seed)

wrapper(main, Game(), debug=options.debug)
