# -*- coding: UTF-8 -*-
###############################################################################
##  @author : Mazikim                                                        ##
##  @file : Sockets.py                                                       ##
###############################################################################
 
import select
import socket
 
class Server:
 
	# Contructeur de la class Server.
	#
	# @param port Port de connexion
	# @param listen Nombre de connexion en attente max
	def __init__(self, port = 35890, listen = 5):
		# Initialisation of attr
		self.nbClients = 0	# Nombre de client connecté
		self.sockets = []	# Liste des sockets client
 
		# Création du socket serveur
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		# On passe le socket serveur en non-bloquant
		self.socket.setblocking(0)
		# On attache le socket au port d'écoute. 
		self.socket.bind(('', port))
		# On lance l'écoute du serveur. "listen" est le nombre max de 
		# connexion quand la file d'attente
		self.socket.listen(listen)
 
 
 
	# Surcouche de la fonction socket.recv
	# On utilise le système d'exeption de recv pour savoir si il reste
	# des donnees a lire
	#
	# @param socket Socket sur lequelle il faut recuperer les données
	# @return Données envoyées par le client
	def receive(self, socket):
		buf = "" # Variable dans laquelle on stocke les données
		_hasData = True # Nous permet de savoir si il y de données à lire
		while _hasData:
			# On passe le socket en non-bloquant
			socket.setblocking(0)
			try:
				_data = socket.recv(256)
				if(_data):
					buf += _data
				else:
					# Déconnexion du client
					_hasData = False
			except:
				_hasData = False
		return buf
 
 
 
	# Fonction qui lance les sockets et s'occupe des clients
	def run(self):
		# On ajoute le socket serveur à la liste des sockets
		self.sockets.append(self.socket)
		# Go
		while True:
			try:
				# La fonction select prends trois paramètres qui sont la liste des sockets
				# Elle renvoie 3 valeurs
				# 	1- La liste des sockets qui ont reçus des données
				# 	2- La liste des sockets qui sont prêt à envoyer des données
				#	3- Ne nous interesse pas dans notre cas
				readReady ,writeReady, nothing = select.select(self.sockets, self.sockets, [])
			except select.error, e:
				break
			except socket.error, e:
				break
 
			# On parcours les sockets qui ont reçus des données
			for sock in readReady:
				if sock == self.socket:
					# C'est le socket serveur qui a reçus des données
					# Cela signifie qu'un client vient de se connecter
					# On accept donc ce client et on récupère qques infos
					client, address = self.socket.accept()
					# On incrémente le nombre de connecté
					self.nbClients += 1
					# On ajoute le socket client dans la liste des sockets
					self.sockets.append(client)
				else:
					# Le client a envoyé des données, on essaye de les lire
					try:
						# On fait appelle à la surchage que l'on a écrite plus haut
						data = self.receive(sock)
						if data:
							# On renvoi au client ce qu'il a envoyé
							sock.send(data)
						else:
							# Si data est vide c'est que le client s'est déconnecté
							# On diminu le nombre de client
							self.nbClients -= 1
							# On supprime le socket de la liste des sockets
							self.sockets.remove(sock)
					except socket.error, e:
						self.sockets.remove(sock)
 
server = Server(35890, 5)
server.run()