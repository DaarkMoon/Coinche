#!/usr/bin/env python
# -*- coding: utf8 -*-

from global_values import *

class Card():
    """
    Classe Carte qui représente une Carte par 
    - Sa valeur ("7","8","9","10","Valet","Dame","Roi","As") 
    - Sa couleur ("carreau", "pique", "trefle", "coeur")

    Attributs
        Valeur	    Valeur de la carte représenté par un int dans l'intervale [0,7] mappé sur VALUE_LIST
        Couleur     Couleur de la carte représenté par un int dans l'intervale [0,3] mappé sur COLOR_LIST
    """
    
    def __init__(self, value, color):
        if value not in range(8):
            raise ValueError("value value must be between 0 and 7.")
        if color not in range(4):
            raise ValueError("color value must be between 0 and 4.")
        self.value = value
        self.color = color
    
    def __repr__(self):
        return "card.Card(%s,%s)"%(self.value,self.color)
    
    def __str__(self):
        return "%s de %s"%(VALUE_LIST[self.value],COLOR_LIST[self.color])
        
    def __str__(self):
        return "%s\n%s"%(VALUE_LIST[self.value],COLOR_LIST[self.color])
    
    def __eq__(self, card_):
        assert isinstance(card_, Card), "card_ must be a type of Card class"
        return (self.color == card_.color) and (self.value == card_.value)
    
    def __ne__(self, card_):
        assert isinstance(card_, Card), "card_ must be a type of Card class"
        return (self.color != card_.color) or (self.value != card_.value)
    
    
