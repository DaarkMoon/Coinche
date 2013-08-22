#!/usr/bin/env python
# -*- coding: utf8 -*-

from global_values import *

class Round_coinche():
    """
    Un round est une manche en 8 tour.
    Un round possède tous les attributs et fonctions valables pendant un round.
    
    Attributs
        trump       entier faisant référence à la couleur atout pour le round
        contract    valeur du contrat, compris dans CONTRACT_VALUES
        master      joueur maître et prochain joueur à joueur à jouer le pli
        belotte     indicateur de belotte: 0 si pas de belotte, 0.5 si belotte ou rebelotte, 1 si belotte et rebelotte
        pli         pli en cours
    
    """
    def __init__(self, trump, contract, players, teams):
        
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
            ## demande à player[j] de jouer une carte "played_card"
            ## -option belotte/rebelotte (self.belotte +=  0.5)
            ## if played_card in player[j].cardlist:
            ## self.pli.append(played_card)
            ## self.player.cardlist.remove(played_card)
            ## break
        ## affichage mis à jour
    
    def strenght(self, card):
        if card.color == self.trump:
            return 12+POINTS_ATOUTS[card.value]
        else:
            return POINTS[card.value]
    
    #trump is "atout" in French
    def set_trump(self, trump):
        if trump not in COLOR_LIST:
            raise ValueError("Trump must be in COLOR_LIST.")
        else:
            self.trump = COLOR_LIST.index(trump)
    
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
    
