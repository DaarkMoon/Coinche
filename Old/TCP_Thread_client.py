# -*- coding: utf8 -*-

# Définition d'un client réseau gérant en parallèle l'émission 
# et la réception des messages (utilisation de 2 THREADS). 

host = 'localhost' 
port = 6804 

import socket, sys, threading 

class ThreadReception(threading.Thread): 
    """objet thread gérant la réception des messages""" 
    def __init__(self, conn): 
        threading.Thread.__init__(self) 
        self.connexion = conn           # réf. du socket de connexion 

    def run(self): 
        while 1: 
            message_recu = self.connexion.recv(1024) 
            print message_recu
            if message_recu == "END":
                break
        # Le thread <réception> se termine ici. 
        # On force la fermeture du thread <émission> : 
        th_E._Thread__stop() 
        print "Client END. Connexion shutdown." 
        self.connexion.close() 

class ThreadEmission(threading.Thread): 
    """objet thread gérant l'émission des messages""" 
    def __init__(self, conn): 
        threading.Thread.__init__(self) 
        self.connexion = conn           # réf. du socket de connexion 

    def run(self): 
        while 1: 
            message_emis = raw_input() 
            self.connexion.send(message_emis) 

# Programme principal - Établissement de la connexion : 
connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
try: 
    connexion.connect((host, port)) 
except socket.error: 
    print "Connection failed. Exit ..." 
    sys.exit()
print "Connection established." 

# Dialogue avec le serveur : on lance deux threads pour gérer 
# indépendamment l'émission et la réception des messages : 
th_E = ThreadEmission(connexion) 
th_R = ThreadReception(connexion) 
th_E.start() 
th_R.start()