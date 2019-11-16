import collections
import enum
import itertools
import random


class Value(enum.IntEnum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    HEIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13


class Symbol(enum.Enum):
    SPADE = "\u2660"
    HEART = "\u2661"
    DIAMOND = "\u2662"
    CLUB = "\u2663"


class Color(enum.Enum):
    RED = "red"
    BLACK = "black"


class Card:
    def __init__(self, name, symbol):
        self.name = name.name
        self.value = name.value
        self.symbol = symbol

    def __str__(self):
        if self.name in {"ACE", "JACK", "QUEEN", "KING"}:
            name = self.name[0]
        else:
            name = str(self.value)
        return name + self.symbol.value

    def __hash__(self):
        return (self.value - 1) + len(Name) * list(Symbol).index(self.symbol)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __lt__(self, other):
        assert self.symbol == other.symbol
        return self.value < other.value

    @property
    def color(self):
        return Color.BLACK if self.symbol in (Symbol.SPADE, Symbol.CLUB) else Color.RED


class Deck:
    def __init__(self, cards=None):
        self.cards = collections.deque(cards or [])  # top deque = last card

    def draw(self, card_count):
        return Deck([self.cards.pop() for _ in range(card_count)])

    def deal(self, player_count):
        players = [Deck() for _ in range(player_count)]
        c_players = itertools.cycle(players)
        while self.cards:
            next(c_players).give(self.draw(1))
        return players

    def shuffle(self):
        random.shuffle(self.cards)
        return self

    def give(self, cards):
        self.cards.extend(cards)

    def __iter__(self):
        return iter(self.cards)

    def __len__(self):
        return len(self.cards)

    @classmethod
    def create_full(cls):
        return cls([Card(v, s) for v in Value for s in Symbol])

    def sort(self):
        cards = list(self.cards)
        cards.sort(key=hash)
        self.cards = collections.deque(cards)

    def pop(self):
        return self.cards.pop()

    def append(self, card):
        return self.cards.append(card)
