#!/usr/bin/env python
# -*- coding: utf8 -*-

from global_values import *

class Round_coinche():
    """
    Un round est une manche en 8 tour.
    Un round possÃ¨de tous les attributs et fonctions valables pendant un round.
    
    Attributs
        trump       entier faisant rÃ©fÃ©rence Ã  la couleur atout pour le round
        contract    valeur du contrat, compris dans CONTRACT_VALUES
        master      joueur maÃ®tre et prochain joueur Ã  joueur Ã  jouer le pli
        belotte     indicateur de belotte: 0 si pas de belotte, 0.5 si belotte ou rebelotte, 1 si belotte et rebelotte
        pli         pli en cours
    
    """
    def __init__(self, trump, contract, players):
        if (trump not in range(4)) or (contract not in CONTRACT_VALUES):
            raise ValueError("invalid annouce for the round")
        self.trump = self.set_trump(trump)
        self.contract = contract
        self.master = players[0]
        self.masters = []
        self.belotte = 0
    
    def play_pli(self):
        self.pli = []
        for i in range(4):
            j = (i+self.master)%4
            ## while 1:
            ## demande Ã  player[j] de jouer une carte "played_card"
            ## -option belotte/rebelotte (self.belotte +=  0.5)
            ## if played_card in player[j].cardlist:
            ## self.pli.append(played_card)
            ## self.player.cardlist.remove(played_card)
            ## break
        ## affichage mis Ã  jour
    
    def strenght(self, card):
        if card.color == self.trump:
            return 12+POINTS_ATOUTS[card.value]
        else:
            return POINTS[card.value]
    
    #trump is "atout" in French
    def set_trump(self, trump):
        if trump not in range(4):
            raise ValueError("Trump must be 0, 1, 2 or 3.")
        self.trump = trump
    
    def master_card(self):
        master_card_index = 0
        initial_color = self.pli[master_card_index].color
        for i in range(1,4):
            if self.pli[i].color in [initial_color,self.trump]:
                if self.strenght(self.pli[i]) > self.strenght(self.pli[master_card_index]):
                    master_card_index = i
        return master_card_index
    
    def seek_master(self):
        old_master = self.master
        self.master = (self.master + self.master_card())%4
        self.masters.append(self.master)
    
    def card_point(self, card):
        if card.color == self.trump:
            return POINTS_ATOUTS[card.value]
        else:
            return POINTS[card.value]
    
    def round_won(self, points):
        if isinstance(self.contract, int):
            if self.belotte == 1:
                points += 20
            if points >= self.contract:
                return 1
            else:
                return 0
        elif self.contract == "capot":
            if points == 162:
                return 1
            else:
                return 0
        elif self.contract == "generale":
            if (points == 162) and (len(set(self.masters)) == 1):
                return 1
            else:
                return 0
    
