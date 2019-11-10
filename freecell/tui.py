from freecell.game import Game, blank_card, placeholder
from functools import partial
from itertools import zip_longest
import curses
import curses.ascii

def refresh_all(stdscr, game):
    # Freecells and foundation
    fc = " ".join(map(lambda c: format(c, '>3'), map(str, game.freecells)))
    fu = " ".join(map(lambda c: format(c, '>3'), map(str, game.foundations)))

    stdscr.addstr(0, 0, fc)
    stdscr.addstr(0, 16, "|")
    stdscr.addstr(0, 18, fu)
    stdscr.addstr(1, 0, "-" * 33)

    # Cascades
    rows = zip_longest(*game.columns, fillvalue=blank_card)
    for row_no, row in enumerate(rows):
        line = " ".join(map(lambda c: format(c, '>3'), map(str, row)))
        stdscr.addstr(2 + row_no, 0, line)

def refresh(stdscr, game, updates):
    for x, y in updates:
        mod = 0
        if y == 0 and x < 4:
            card = game.freecells.slots[x]
        elif y == 0 and x >= 4:
            card = game.foundations[x - 4]
            mod = 2
        elif y - 2 < len(game.columns[x]):
            card = game.columns[x].cards[y - 2]
        else:
            card = blank_card
        stdscr.addstr(y, x * 4 + mod, format(str(card), '>3'), curses.A_NORMAL)

def highlight(stdscr, game, state):
    def _highlight(tpl, attr):
        if tpl:
            x, y = tpl
            if y == 0 and x < 4:
                stdscr.chgat(0, x * 4, 3, attr)
            elif y == 0 and x >= 4:
                stdscr.chgat(0, 2 + x * 4, 3, attr)
            else:
                y = len(game.columns[x]) or 1
                stdscr.chgat(1 + y, x * 4, 3, attr)

    _highlight(state['old'], curses.A_NORMAL)
    _highlight((state['x'], state['y']), curses.A_STANDOUT)
    _highlight(state['from'], curses.A_STANDOUT)
    _highlight(state['to'], curses.A_NORMAL)

def log(stdscr, *log, sep=" "):
    stdscr.addstr(17, 0, format(sep.join(map(str, log)), '<79'))

def main(stdscr, game, debug):
    stdscr.clear()
    refresh_all(stdscr, game)

    turn = 0
    state = {
        'x': 0,
        'y': 0,
        'old': None,
        'from': None,
        'to': None,
        'undo': False,
    }
    while not game.won:
        stdscr.refresh()
        key = stdscr.getch()
        if key == curses.ascii.ESC:
            break
        state = dispatch_key(key, state, game)
        highlight(stdscr, game, state)
        updates = play(game, state)
        if debug:
            log(stdscr, updates)
        refresh(stdscr, game, updates)


def key_up(state, game):
    state['old'] = state['x'], state['y']
    state['y'] = max(0, state['y'] - 1)

def key_down(state, game):
    state['old'] = state['x'], state['y']
    state['y'] = min(1, state['y'] + 1)

def key_left(state, game):
    state['old'] = state['x'], state['y']
    state['x'] = max(0, state['x'] - 1)

def key_right(state, game):
    state['old'] = state['x'], state['y']
    state['x'] = min(7, state['x'] + 1)

def key_space(state, game):
    if not state['from']:
        if ((state['y'] == 1
             and game.columns[state['x']].cards)
            or (state['y'] == 0
                and state['x'] < 4
                and game.freecells.slots[state['x']] is not placeholder)
        ):  
            state['from'] = (state['x'], state['y'])
    elif state['from'] == (state['x'], state['y']):
        state['from'] = None
    elif not state['to']:
        state['to'] = (state['x'], state['y'])
    else:
        assert False

def key_backspace(state, game):
    state['undo'] = True

key_dispatcher = {
    curses.KEY_LEFT: key_left,
    curses.KEY_RIGHT: key_right,
    curses.KEY_UP: key_up,
    curses.KEY_DOWN: key_down,
    ord(' '): key_space,
    curses.KEY_BACKSPACE: key_backspace,
}
def dispatch_key(key, state, game):
    func = key_dispatcher.get(key)
    if func:
        func(state, game)
    return state

def play(game, state):
    game.events = []
    if state['undo']:
        state['undo'] = False
        game.undo()  # undo place
        game.undo()  # undo take

    elif state['from'] and state['to']:
        fx, fy = state['from']
        tx, ty = state['to']

        card = game.pop_from_col(fx) if fy == 1 else game.pop_from_free(fx)
        if ty == 1:
            game.add_to_col(tx, card)
        elif tx < 4:
            game.add_to_free(card)
        else:
            game.add_to_found(card)

        state['from'] = None
        state['to'] = None

    return game.events

"""
 _   _   _   _  |  _   _   _   _
---------------------------------
10♢  7♠  7♡  8♢  3♠  4♢  Q♡  5♢
 Q♣  2♢  5♠  J♡  2♡  6♡  6♣ 10♠
 6♢  9♢ 10♣  K♠  J♢  4♠  3♡  K♢
 7♣  9♠  3♣  7♢  4♣  J♠  9♡  4♡
 A♣  K♡  A♢  5♣  K♣  5♡  2♠  8♠
 Q♢  8♣  Q♠  6♠  A♠  2♣  3♢  8♡
 A♡  9♣  J♣ 10♡

"""