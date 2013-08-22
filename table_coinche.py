#!/usr/bin/env python
# -*- coding: utf8 -*-

from global_values import *
from card import Card
from deck import Deck
from player import Player
from team import Team
from round_coinche import Round_coinche


class Table_coinche():
    """
    Une table_coinche est le support pour une partie de coinche entre 2 Ã©quipes de 2 joueurs
    
    Attributs
        teams       une liste des Ã©quipes qui jouent
        deck        le jeu de cartes utilisÃ©s pour la partie
        players     une liste des joueurs dans l'ordre oÃ¹ ils jouent, 2 joueurs consÃ©cutifs de la liste sont dans des Ã©quipes diffÃ©rentes
    """
    def __init__(self, teamA, teamB):
        if not (isinstance(teamA,Team) and isinstance(teamB, Team)):
            raise ValueError("Invalid team")
        self.deck = Deck()
        self.deck.shuffle_deck()
        self.teams = [teamA, teamB]
        self.players = [self.teams[team_index].players[player_index] for player_index in range(2) for team_index in range(2)]
    
    def play_round(self, trump, contract, team_playing):
        if (trump not in range(4)) or (contract not in CONTRACT_VALUES):
            raise ValueError("invalid announce for the round")
        elif isinstance(contract, int):
            round_points = contract*(2^(self.coinche))
        elif contract == "capot":
            round_points = 250
        elif contract = "generale"
            round_points = 500
        contracted_team = self.teams.index(team_playing)
        table_round = Round(trump, contract, self.players)
        other_pli = []
        count = 0
        for number_pli in range(8):
            table_round.play_pli()
            table_round.seek_master()
            if self.players[table_round.master] in self.contracted_team:
                self.deck.add_cards(table_round.take_pli())
            else:
                other_pli.extend(table_round.pli())
        
        for card_index in self.deck.cardlist:
            count += table_round.card_point(card_index)
        self.deck.add_cards(other_pli)
        
        if table_round.round_won(count):
            self.teams[contracted_teams].score += round_points
        else:
            self.teams[1-contracted_teams].score += round_points
    
    def launch_party(self, first_player=0):
        if first_player in range(4):
            self.players = self.players[self.first_player:] + self.players[:self.first_player]
        else:
            raise ValueError("first_player must be type 0, 1, 2 or 3")
        
        #### joue la partie jusque dÃ©passement du score ou par interruption manuelle de la partie
        while 1:
            coinche = 0
            
            #### coupage de deck ####
            ## ask self.players[-2] to cut with "cut_value"
            ## obtain "cut_value" of cut between 2 and 29
            ## if cut_value not in range(2,30):
            ##  mode = "Auto"
            ## else:
            ##  mode = "Flou" # on considÃ¨re que les gens sont forcÃ©ment bourrÃ©s pour jouer XD
            ## ask self.players[-1] to distribute with "two_cards"
            self.deck.cut_deck(mode, cut_value)
            
            #### distribution du deck ####
            [self.players[0].cardlist, self.players[1].cardlist, self.players[2].cardlist, self.players[3].cardlist] = self.deck.distribute_deck(two_cards)
            
            #### annonces des joueurs ####
            ## team_index = 0 ou 1 suivant si team[0] ou team[1] qui commence Ã  annoncer
            ## team_index = (team_index + 1)%2 Ã  chaque annonce mÃªme None ou coinche !!! 1 pass ou 1 coinche change l'Ã©quipe, 1 surcoinche = 2 coinches donc pas de changement d'Ã©quipe
            ## annonce du type (contract=None, color=None, self.team[team_index]) <- Ã©quipe qui annonce mis Ã  jour automatiquement, donc l'Ã©quipe qui annonce est connu par la table grace au team_index
            ## if (contract in CONTRACT_VALUES) and (color in COLOR_LIST)
            ##  TO CONTINUES
            #### gestion des coinchages ####
            ## player_coinche est un boolÃ©en qui indique si coinchage est vrai
            ## idem pour player_coinche_2 mais je sais pas si il y a moyen de faire avec juste une variable....
            ## if player_coinche and (player_who_coinche not in teams[team_index]):
            ##  coinche += 1
            ##   if player_coinche_2 and (player_who_coinche_2 in team[team_index]):
            ##    coinche += 1
            
            #### joue la partie avec l'annonce la plus forte ####
            self.play_round(trump, contract, team_playing)
            
            #### test si la partie est finie par dÃ©passement du score ou si la partie est stoppÃ© manuellement
            if (self.teams[0].score >= 1000) or (self.teams[1].score >= 1000) or (stop_party):
                break
            
            #### change le joueur Ã  annoncer et Ã  jouer en 1er ####
            self.players = self.players[1:] + self.players[:1]
            
        #### affiche les rÃ©sultats ####
        self.print_results()
    
    def print_results(self):
        pass
    
    


    


