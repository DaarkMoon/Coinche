# -*- coding: utf8 -*-

import random

VALUE_LIST = ("7","8","9","10","Valet","Dame","Roi","As") 
COLOR_LIST = ("carreau", "pique", "trefle", "coeur")
POINTS = (0,0,0,10,2,3,4,11)
POINTS_ATOUTS = (0,0,14,10,20,3,4,11)
VALID_DISTRIBUTION_SCHEMA = ( (3,3,2), (3,2,3), (2,3,3) )
							  
class CoincheError(Exception):
    def __init__(self,raison):
        self.raison = raison
     
    def __str__(self):
        return self.raison
		
class Card():
	"""
	Classe Carte qui représente une Carte par 
	- Sa valeur ("7","8","9","10","Valet","Dame","Roi","As") 
	- Sa couleur ("carreau", "pique", "trefle", "coeur")

	Attributs
		Valeur		Valeur de la carte représenté par un int dans l'intervale [0,7] mappé sur VALUE_LIST
		Couleur 	Couleur de la carte représenté par un int dans l'intervale [0,3] mappé sur COLOR_LIST
	"""
	def __init__(self,value,color):
		if value not in range(8):
			raise CoincheError("Value out of range [0,7] : %s"%(value))
		if color not in range(4):
			raise CoincheError("Color out of range [0,3] : %s"%(color))
		self.value = value
		self.color = color
		
	def __repr__(self):
		return "%s de %s"%(VALUE_LIST[self.value],COLOR_LIST[self.color])

class Deck():
	"""
	Classe représentant un jeu de 32 cartes avec les fonctions pour

	Attributs
		cardlist	tableau des 32 cartes à distribuer
	"""
	def __init__(self):
		self.cardlist = [Card(i,j) for j in range(4) for i in range(8)]

	def __repr__(self):
		s = ""
		for card in self.cardlist:
			s += str(carte) + "\n"
		return s

	def shuffle(self):
		"""Mélange le jeu"""
		random.shuffle(self.cardlist)

	def cut(self,mode="Auto",coupe=16,err=3):
		"""
		Coupe le jeux suivant 3 méthodes
		- Auto : le bot choisit
		- Flou : le joueur choisit et le bot ajoute un marge d'erreurs
		- Fin  : le joueur choisit précisement
		"""
		if mode == "Auto":
			coupe = random.randint(0,31)
		elif mode == "Flou":
			coupe += random.randint(-err,+err)
		elif mode != "Fin":
			raise coincheError("Invalid cut mode : %s"%(mode))

		self.cardlist = self.cardlist[coupe:]+self.cardlist[:coupe]

	def distribute(self,schema=(3,2,3)):
		if schema not in VALID_DISTRIBUTION_SCHEMA:
			raise coincheError("Invalid disribution schema : %s"%(schema))
		hands = [Hand() for i in range(4)]
		for turn in range(3):
			for player in range(4):
				for card in range(schema[turn]):
					hands[player].cardlist.append(self.cardlist.pop())
		return hands

class Hand():
	def __init__(self):
		self.cardlist = []

	def __repr__(self):
		s = ""
		for card in self.list:
			s += str(carte) + "\n"
		return s
    
class Player():
	def __init__(self,name="Joueur"):
		self.name = name
		self.hand = None
	
class Turn():
	def __init__(self,cartes,atout):
		self.cartes = cartes
		self.points = self.calculPoints(atout)

	def calculPoints(self):
		total = 0
		for carte in cartes:
			if carte.couleur == atout:
				total += POINTS_ATOUTS[carte.valeur]
			else:
				total += POINTS[carte.valeur]
		return total
    
class Team():
	"""
		une Equipe est composé de deux joueurs et un score
	"""
	def __init__(self,playerA,playerB):
		if not (isinstance(playerA,Player) and isinstance(playerB, Player) ):
			raise CoincheError("Invalid player in team : %s vs %s"%(playerA,playerB))
		self.playerA = playerA
		self.playerB = playerB
		self.score = 0
		
	def addPoints(self, points):
		"""Ajoute les points à l'équipe"""
		self.score += points

class Round():
	"""
		Un round est une manche en 8 tour.
	"""
	def __init__(self,atout,startPlayer):
		self.startPlayer = startPlayer
		self.atout = atout

class Party():
	"""
		Une Partie est une succession de manche jusqu'à dépassement du score maximum
	"""
	def __init_(self, teamNS, teamEO, atout, scoreMax=1000):
		if not (isinstance(teamNS,Team) and isinstance(teamEO, Team) ):
			raise CoincheError("Invalid team : %s or %s"%(teamNS,teamEO))
		if not isinstance(scoreMax, int) or scoreMax<0:
			raise CoincheError("Invalid Maximum Score : %s"%(scoreMax))
		self.teamNS = teamNS
		self.teamEO	= teamEO
		self.scoreMax = scoreMax

	def isEnded(self):
		"""
			Retourne l'équipe gagnante s'il y en a une
			Retourne False sinon
		"""
		if self.teamNS.score > self.scoreMax:
			return self.teamNS
		elif self.teamEO.score > self.scoreMax:
			return self.teamEO
		else:
			return False

	