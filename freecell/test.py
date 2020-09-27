#!/usr/bin/env python3

import textwrap
import unittest
import base64
from game import Game
from deck import Card, Symbol, Value


class NullList:
    def append(self, x):
        pass


class TestGame(unittest.TestCase):
    def setUp(self):
        self.freeze = base64.b64decode(
            b"AQEBAQEBAQEKFBscBxYYKyIyKA4pMy4kDyASHScMBjUmHy0x"
            b"EBkTLywaHgIVBSoECRELDTQDJRcBAQEBCCMwIQ=="
        )
        self.game = Game.restore(self.freeze)
        self.game.events = NullList()

    def test_str(self):
        self.assertEqual(str(self.game), textwrap.dedent("""
         _   _   _   _  |  _   _   _   _ 
        ---------------------------------
         9♠  6♡  K♡  A♢  6♠  8♡ 10♡  3♣
         7♢ 10♣  K♢  K♠  A♣  J♣  6♣  9♢
         A♡  5♢  4♡  2♢  Q♢  J♠  5♠  K♣
         J♢  4♢  5♣  9♣  2♡  J♡  5♡  7♣
         4♣  Q♡  3♢  A♠  7♡  4♠  2♣  3♠
         8♠  3♡ 10♠  Q♠  Q♣  2♠ 10♢  9♡
                         7♠  8♢  8♣  6♢
        """[1:]))

    def test_freeze(self):
        self.assertEqual(self.game.freeze(), self.freeze)

    def test_col_to_col(self):
        card = self.game.pop_from_col(7)
        self.assertEqual(card, Card(Value.SIX, Symbol.DIAMOND))
        self.game.add_to_col(4, card)
        self.assertEqual(self.game.columns[4].cards[-1], card)

    def test_col_to_fc(self):
        card = self.game.pop_from_col(3)
        self.assertEqual(card, Card(Value.QUEEN, Symbol.SPADE))
        self.game.add_to_free(card)
        self.assertEqual(self.game.freecells.slots[0], card)

    def test_col_to_found(self):
        # moving the queen to the freecells so the ace is available
        self.game.add_to_free(self.game.pop_from_col(3))

        card = self.game.pop_from_col(3)
        self.assertEqual(card, Card(Value.ACE, Symbol.SPADE))
        self.assertTrue(self.game.foundations.can_add(card))
        self.game.add_to_found(card)
        self.assertEqual(self.game.foundations.slots[hash(Symbol.SPADE)][-1], card)

    def test_fc_to_found(self):
        # moving both the queen and the ace to the freecells
        self.game.add_to_free(self.game.pop_from_col(3))
        self.game.add_to_free(self.game.pop_from_col(3))

        card = self.game.pop_from_free(1)
        self.assertEqual(card, Card(Value.ACE, Symbol.SPADE))
        self.assertTrue(self.game.foundations.can_add(card))
        self.game.add_to_found(card)
        self.assertEqual(self.game.foundations.slots[hash(Symbol.SPADE)][-1], card)


if __name__ == '__main__':
    unittest.main()
