from freecell.deck import Deck, Card, Symbol, Value
from operator import itemgetter
from itertools import zip_longest, chain, count, cycle
from io import StringIO


class BlankCard:
    name = ""
    value = 0

    def __str__(self):
        return "   "

    def __hash__(self):
        return 1


class Placeholder:
    name = ""
    value = 0

    def __str__(self):
        return " _ "

    def __hash__(self):
        return 1


blank_card = BlankCard()
placeholder = Placeholder()


class Foundation:
    def __init__(self):
        self.slots = {
            Symbol.HEART: [placeholder],
            Symbol.SPADE: [placeholder],
            Symbol.DIAMOND: [placeholder],
            Symbol.CLUB: [placeholder],
        }

    def __iter__(self):
        return iter(map(itemgetter(-1), self.slots.values()))

    def can_add(self, card):
        top_card = self.slots[card.symbol][-1]
        if top_card is placeholder:
            return card.value == 1
        else:
            return top_card.value == card.value - 1

    def add(self, card):
        if self.can_add(card):
            self.slots[card.symbol].append(card)
        else:
            raise ValueError("Invalid Operation")

    def min_red_value(self):
        return min(
            self.slots[Symbol.HEART][-1].value, self.slots[Symbol.DIAMOND][-1].value
        )

    def min_black_value(self):
        return min(
            self.slots[Symbol.SPADE][-1].value, self.slots[Symbol.CLUB][-1].value
        )

    def __getitem__(self, i):
        return self.slots[list(self.slots.keys())[i]][-1]

    def index(self, symbol):
        return list(self.slots.keys()).index(symbol)


class Freecell:
    def __init__(self):
        self.slots = [placeholder] * 4

    def __iter__(self):
        return iter(self.slots)

    def __len__(self):
        return len([s for s in self.slots if s is not placeholder])

    def __bool__(self):
        return bool(len(self))

    def empty_cnt(self):
        return 4 - len(self)

    def add(self, card):
        for slot_no, slot in enumerate(self.slots):
            if slot is placeholder:
                self.slots[slot_no] = card
                return slot_no
        raise ValueError("No free cell")

    def pop(self, slot):
        card = self.slots[slot]
        self.slots[slot] = placeholder
        return card


class Game:
    def __init__(self):
        self.foundations = Foundation()
        self.freecells = Freecell()
        self.columns = Deck.create_full().shuffle().deal(8)
        self.undos = []

    def freeze(self):
        hashes = []
        def digest(iterable):
            hash_ = 0
            for card in iterable:
                hash_ = (hash_ << 8) + hash(card)
            return hash_

        def len_digest(iterable):
            return (len(iterable), digest(iterable))

        def hold(hash_):
            for i in range(hash_.bit_length() // 8, -1, -1):
                hashes.append((hash_ & (255 << 8 * i)) >> (8 * i))

        
        hold(digest(sorted(self.freecells, key=hash)))
        hold(digest(self.foundations))
        for line in zip_longest(*sorted(self.columns, key=len_digest), fillvalue=blank_card):
            hold(digest(line))
        return bytes(hashes)

    @classmethod
    def restore(cls, frozen_game):

        hashes = iter(frozen_game)
        game = cls()
        game.columns = [Deck() for _ in range(8)]

        for h, _ in zip(hashes, range(3)):
            if h != 1:
                game.freecells.add(Card.from_hash(h))

        for h, _ in zip(hashes, range(3)):
            if h != 1:
                card = Card.from_hash(h)
                if card:
                    game.foundations.slots[card.symbol] = [card]

        for h, col in zip(hashes, cycle(game.columns)):
            if h != 1:
                col.append(Card.from_hash(h))

        return game

    def pop_from_col(self, column):
        card = self.columns[column].pop()
        self.events.append((column, len(self.columns[column]) + 2))
        self.undos.append((self.undo_pop_from_col, column, card))
        return card

    def undo_pop_from_col(self, column, card):
        self.columns[column].append(card)
        self.events.append((column, len(self.columns[column]) + 1))

    def pop_from_free(self, slot):
        card = self.freecells.pop(slot)
        self.events.append((slot, 0))
        self.undos.append((self.undo_pop_from_free, slot, card))
        return card

    def undo_pop_from_free(self, slot, card):
        self.freecells.slots[slot] = card
        self.events.append((slot, 0))

    def add_to_col(self, column, card):
        if self.columns[column].cards:
            bottom_card = self.columns[column].cards[-1]
        if (not self.columns[column].cards) or (
            bottom_card.color != card.color and bottom_card.value == card.value + 1
        ):
            self.columns[column].append(card)
            self.events.append((column, len(self.columns[column]) + 1))
            self.undos.append((self.undo_add_to_col, column))
        else:
            self.undo()

    def undo_add_to_col(self, column):
        self.columns[column].pop()
        self.events.append((column, len(self.columns[column]) + 2))

    def add_to_free(self, card):
        if self.freecells.empty_cnt():
            slot = self.freecells.add(card)
            self.events.append((slot, 0))
            self.undos.append((self.undo_add_to_free, slot))
        else:
            self.undo()

    def undo_add_to_free(self, slot):
        self.freecells.pop(slot)
        self.events.append((slot, 0))

    def add_to_found(self, card):
        if self.foundations.can_add(card):
            self.foundations.add(card)
            self.events.append((4 + self.foundations.index(card.symbol), 0))
            self.undos.append((self.undo_add_to_found, card.symbol))
        else:
            self.undo()

    def undo_add_to_found(self, symbol):
        self.foundations.slots[symbol].pop()
        self.events.append((4 + self.foundations.index(symbol), 0))

    def undo(self):
        if self.undos:
            func, *args = self.undos.pop()
            func(*args)

    @property
    def won(self):
        return all(
            cards[-1].name == Value.KING.name
            for cards in self.foundations.slots.values()
        )

    def __str__(self):
        def align(c):
            return format(str(c), ">3")

        with StringIO() as stream:
            stream.write("{freecells} | {foundations}\n".format(
                freecells = " ".join(map(align, self.freecells)),
                foundations = " ".join(map(align, self.foundations)),
            ))
            stream.write(" %s\n" % ("-" * 33))
            for row in zip_longest(*self.columns, fillvalue=blank_card):
                stream.write("%s\n" % " ".join(map(align, row)))

            return stream.getvalue()
