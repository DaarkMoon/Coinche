#!/var/bin python
import unittest
from card import Card
from deck import Deck

class TestCard(unittest.TestCase):

    def setUp(self):
        #initialise test
        pass
           
    def test_create_card(self):
        """ TEST Card WHEN create card with correct value SHOULD create"""
        cardtest = Card(4, "carreau")
        self.assertEqual(cardtest.value, 4)
        self.assertEqual(cardtest.color, "carreau")


    def test_create_card_wrong_color_value(self):
        """ TEST Card WHEN create card with incorrect color value SHOULD return an error"""
        self.assertRaises(ValueError, Card, 4, "plop")
        

    def test_create_card_wrong_value_value(self):
        """ TEST Card WHEN create card with incorrect color value SHOULD return an error"""
        self.assertRaises(ValueError, Card, 10, "carreau")
        
    def test_create_card_wrong_value_type(self):
        """ TEST Card WHEN create card with incorrect color value SHOULD return an error"""
        self.assertRaises(AssertionError, Card, "plop", "carreau")
        
    def test_create_card_wrong_color_type(self):
        """ TEST Card WHEN create card with incorrect color value SHOULD return an error"""
        self.assertRaises(AssertionError, Card, 10, 10)


class TestDeck(unittest.TestCase):

    def setUp(self):
        #initialise test
        pass
           
    def test_create_deck(self):
        """ TEST Card WHEN create deck with correct value SHOULD create"""
        decktest = Deck()
        self.assertEqual(decktest.cardlist[0].color, "carreau")
        self.assertEqual(decktest.cardlist[0].value, 0)


    def test_set_trump(self):
        """ TEST Card WHEN set trump with correct value SHOULD set"""
        decktest = Deck()
        decktest.set_trump("carreau")
        self.assertEqual(decktest.trump, "carreau")

    def test_set_unvalid_trump(self):
        """ TEST Card WHEN set trump with uncorrect value SHOULD return an error"""
        decktest = Deck()
        self.assertRaises(ValueError, decktest.set_trump, "plop")
		
if __name__ == '__main__':
    unittest.main()
