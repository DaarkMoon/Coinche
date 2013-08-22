#!/usr/bin/env python
# -*- coding: utf8 -*-

#from global_values import *
import random
from card import Card

class Deck():
    """
    Classe représentant un jeu de 32 cartes avec les fonctions pour jeu de coinche.

    Attributs
        cardlist    tableau de cartes, limité à 32 cartes
    """
    
    def __init__(self):
        self.cardlist = [Card(value_index,color_index) for color_index in range(4) for value_index in range(8)]
        #create all cards
        #loop in value with 0,1,...,7
    
    def shuffle_deck(self):
        """
        Mélange le jeu
        """
        random.shuffle(self.cardlist)
    
    def cut_deck(self,mode="Auto",coupe=16,err=3):
        """
        Coupe le jeux suivant 3 méthodes
        - Auto : le bot choisit
        - Flou : le joueur choisit et le bot ajoute une marge d'erreurs
        - Fin  : le joueur choisit précisement
        """
        if mode == "Auto":
                coupe = random.randint(2,29)
        elif mode == "Flou":
                coupe += random.randint(-err,+err)
        elif mode != "Fin":
                raise ValueError("Invalid cut mode : %s"%(mode))

        self.cardlist = self.cardlist[coupe:]+self.cardlist[:coupe]
        
    def distribute_deck(self,two_cards=2):
        if two_cards not in range(1,4):
            raise ValueError("two_cards value must be 1, 2 or 3.")
        
        scheme = [3,3,3]
        distribution[two_cards-1] = 2
        lots = [[] for i in range(4)]

        for card_number in scheme:
            for lot_number in range(4):
                lots[lot_number].extend(self.cardlist[0:card_number])
                self.cardlist=self.cardlist[card_number:]
        return lots
    
    def __repr__(self):
        s = ""
        for card in self.cardlist:
                s += str(card) + "\n"
        return s
    
    def add_cards(self, card_list):
        self.cardlist.extend(card_list)
    
    