Freecell
========

Terminal (ncruses) implementation of the freecell solitaire game.

     5♡  3♠  _   2♠ |  2♡  A♠  3♢  2♣
    ---------------------------------
     K♠  K♣ 10♢      9♡  K♡  3♡  4♢
     Q♢  Q♡  9♣      4♡  Q♠  K♢  3♣
     J♠  J♣  8♢      Q♣  J♡  5♣  8♣
    10♡      7♣      J♢ 10♠  4♠  7♢
     9♠      6♡     10♣  9♢      6♠
     8♡                  8♠
     7♠                  7♡
     6♢                  6♣
     5♠                  5♢
                         4♣

Setup
-----

The package is available on my own repository. As it requires `ncurses` to run, it won't work on windows natively.

    $ pip3 -i https://pypi.drlazor.be/ freecell
    $ python3 -m freecell

How to play ?
-------------

* arrows: move cursor
* space: select/move card
* backspace: undo
* escape: quit
