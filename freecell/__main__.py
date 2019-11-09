from curses import wrapper
from freecell.tui import main
from freecell.game import Game
wrapper(main, Game())
