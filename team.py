#!/usr/bin/env python
# -*- coding: utf8 -*-

from player import *

class Team():
    """
    Une équipe est composé d'une liste de deux joueurs et d'un score.
    
    Attributs
        players     liste des joueurs dans l'équipe
        score       score de l'équipe
    """
    
    def __init__(self,playerA,playerB):
        """
        Ajoute les joueurs à la liste et met le score à 0.
        """
        if not (isinstance(playerA,Player) and isinstance(playerB, Player) ):
            raise ValueError("Invalid player in team : %s vs %s"%(playerA,playerB))
        self.players = [playerA, playerB]
        self.score = 0
            
    def add_points(self, points):
        """
        Ajoute les points à l'équipe.
        """
        assert isinstance(points,int), "points must be type of int."
        self.score += points