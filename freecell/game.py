from freecell.deck import Deck, Card, Symbol, Value
from operator import itemgetter

class BlankCard:
    name = ""
    value = 0
    def __str__(self):
        return "   "
class Placeholder:
    name = ""
    value = 0
    def __str__(self):
        return " _ "
blank_card = BlankCard()
placeholder = Placeholder()

class Foundation:
    def __init__(self):
        self.slots = {
            Symbol.HEART: [placeholder],
            Symbol.SPADE: [placeholder],
            Symbol.DIAMOND: [placeholder],
            Symbol.CLUB: [placeholder]
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
            self.slots[Symbol.HEART][-1].value,
            self.slots[Symbol.DIAMOND][-1].value
        )
    
    def min_black_value(self):
        return min(
            self.slots[Symbol.SPADE][-1].value,
            self.slots[Symbol.CLUB][-1].value
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

    def empty_cnt(self):
        return 4 - len(self)

    def add(self, card):
        for slot_no, slot in enumerate(self.slots):
            if slot is placeholder:
                self.slots[slot_no] = card
                return slot_no
        raise ValueError('No free cell')

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
        self.events.append((len(self.freecells), 0))
        self.undos.append((self.undo_pop_from_free, slot, card))
        return card

    def undo_pop_from_free(self, slot, card):
        self.freecells.slots[slot] = card
        self.events.append((slot, 0))

    def add_to_col(self, column, card):
        if self.columns[column].cards:
            bottom_card = self.columns[column].cards[-1]
            allowed = (
            )
        else:
            allowed = True
        if ((not self.columns[column].cards)
            or (
                bottom_card.color != card.color
                and bottom_card.value == card.value + 1
            )
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
            print(args, file=open('log', 'a'))
            func(*args)

    @property
    def won(self):
        return all(
            cards[-1].name == Value.KING.name
            for cards in self.foundations.slots.values()
        )
    
