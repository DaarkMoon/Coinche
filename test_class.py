#!/var/bin python
# -*- coding: utf8 -*-

import unittest
from card import Card
from deck import Deck
from player import Player

class TestPlayer(unittest.TestCase):

    def setUp(self):
        #initialise test
        pass
    
    def test_create_player(self):
        """ TEST Player WHEN create player with correct value SHOULD create"""
        playertest = Player("carreau")
        self.assertEqual(playertest.name, "carreau")
    
    def test_create_player_wrong_name_type(self):
        """ TEST Player WHEN create player with incorrect name value SHOULD return an error"""
        self.assertRaises(AssertionError, Player, 10)

class TestCard(unittest.TestCase):

    def setUp(self):
        #initialise test
        pass
           
    def test_create_card(self):
        """ TEST Card WHEN create card with correct value SHOULD create"""
        cardtest = Card(4, 0)
        self.assertEqual(cardtest.value, 4)
        self.assertEqual(cardtest.color, 0)


    def test_create_card_wrong_color_value(self):
        """ TEST Card WHEN create card with incorrect color value SHOULD return an error"""
        self.assertRaises(ValueError, Card, 4, 4)
        

    def test_create_card_wrong_value_value(self):
        """ TEST Card WHEN create card with incorrect color value SHOULD return an error"""
        self.assertRaises(ValueError, Card, 10, 0)
        
    def test_create_card_wrong_value_type(self):
        """ TEST Card WHEN create card with incorrect color value SHOULD return an error"""
        self.assertRaises(AssertionError, Card, "plop", 0)
        
    def test_create_card_wrong_color_type(self):
        """ TEST Card WHEN create card with incorrect color value SHOULD return an error"""
        self.assertRaises(AssertionError, Card, 4, "plop")
    
    def test_same_cards(self):
        """ TEST Card WHEN compare 2 same cards SHOULD be the same"""
        card1 = Card(5,0)
        card2 = Card(5,0)
        self.assertEqual(card1, card2)
    
    def test_different_cards(self):
        """ TEST Card WHEN compare 2 different cards SHOULD be the different"""
        card1 = Card(5,0)
        card2 = Card(6,0)
        card3 = Card(6,1)
        self.assertNotEqual(card1, card2)
        self.assertNotEqual(card2, card3)
        self.assertNotEqual(card3, card1)
    

class TestDeck(unittest.TestCase):

    def setUp(self):
        #initialise test
        pass
           
    def test_create_deck(self):
        """ TEST Card WHEN create deck with correct value SHOULD create"""
        decktest = Deck()
        self.assertEqual(decktest.cardlist[0].color, 0)
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
        
    def test_shuffle_deck(self):
        pass

    
if __name__ == '__main__':
    unittest.main()
