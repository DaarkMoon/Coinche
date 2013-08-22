#!/usr/bin/env python
# -*- coding: utf8 -*-

class Player():
    """
    Un joueur est composé d'un nom et d'une liste de carte en main.
    
    Attributs
        name        nom du joueur
        cardlist    liste des cartes en main pour un joueur
    """
    def __init__(self, name):
        """
        Créé un joueur avec un nom et une main vide.
        """
        assert isinstance(name,str), "name must be type of str."
        self.name = name
        self.cardlist = []
    
    
    
