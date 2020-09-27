#!/usr/bin/env python3
import random
from argparse import ArgumentParser
from base64 import b64encode, b64decode
from functools import partial
from os import getenv
from time import time
from freecell.game import Game

parser = ArgumentParser()
parser.add_argument("display", choices=["TUI", "GUI"])
parser.add_argument("--debug", action="store_true", default=False)
parser.add_argument("--seed", action="store", type=int, default=None)
parser.add_argument("--restore", action="store")
options = parser.parse_args()

# Initialise backend
seed = options.seed or int(time())
random.seed(seed)
print("Game seed:", seed)
if options.restore:
    freeze = b64decode(options.restore.encode())
    game = Game.restore(freeze)
else:
    game = Game()

# Select frontend
if options.display == "GUI":
    from freecell.gui import main
else:
    from curses import wrapper
    from freecell.tui import main
    main = partial(wrapper, main)

# Start the game
main(game, debug=options.debug)
if not game.won:
    print("Freeze:", b64encode(game.freeze()).decode())
