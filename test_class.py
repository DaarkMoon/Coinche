#!/var/bin python
import unittest
from coinche import *

class TestCard(unittest.TestCase):

    def setUp(self):
        #initialise test
        pass
           
    def test_create_card(self):
        """ TEST Card WHEN create card with correct value SHOULD create"""
        for value in range(8):
			for color in range(4):
				cardtest = Card(value, color)
				self.assertEqual(cardtest.value, value)
				self.assertEqual(cardtest.color, color)


    def test_create_card_wrong_color_value(self):
        """ TEST Card WHEN create card with incorrect color value SHOULD return an error"""
        self.assertRaises(CoincheError, Card, 2, 10)
        

    def test_create_card_wrong_value_value(self):
        """ TEST Card WHEN create card with incorrect color value SHOULD return an error"""
        self.assertRaises(CoincheError, Card, 10, 2)
        
    def test_create_card_wrong_value_type(self):
        """ TEST Card WHEN create card with incorrect color value SHOULD return an error"""
        self.assertRaises(CoincheError, Card, "plop", 2)
        
    def test_create_card_wrong_color_type(self):
        """ TEST Card WHEN create card with incorrect color value SHOULD return an error"""
        self.assertRaises(CoincheError, Card, 2, "plop")


class TestDeck(unittest.TestCase):

    def setUp(self):
        #initialise test
        pass
           
	def test_create_deck(self):
		""" TEST Card WHEN create deck with correct value SHOULD create"""
		decktest = Deck()
		for value in range(8):
			for color in range(4):
				self.assertEqual(decktest.cardlist[value+color*8].color, color)
				self.assertEqual(decktest.cardlist[value+color*8].value, value)

if __name__ == '__main__':
    unittest.main()
