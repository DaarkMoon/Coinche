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
        self.connection = conn           # réf. du socket de connection 

    def run(self): 
        while 1: 
            message_recu = self.connection.recv(1024) 
            print message_recu
            if message_recu == "END":
                break
        # Le thread <réception> se termine ici. 
        # On force la fermeture du thread <émission> : 
        th_E._Thread__stop() 
        print "Client END. Connexion shutdown." 
        self.connection.close() 

class ThreadEmission(threading.Thread): 
    """objet thread gérant l'émission des messages""" 
    def __init__(self, conn): 
        threading.Thread.__init__(self) 
        self.connection = conn           # réf. du socket de connection 

    def run(self): 
        while 1: 
            message_emis = raw_input() 
            self.connection.send(message_emis+"\r\n") 

# Programme principal - Établissement de la connection : 
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
try: 
    connection.connect((host, port)) 
except socket.error: 
    print "Connection failed. Exit ..." 
    sys.exit()
print "Connection established." 

# Dialogue avec le serveur : on lance deux threads pour gérer 
# indépendamment l'émission et la réception des messages : 
th_E = ThreadEmission(connection) 
th_R = ThreadReception(connection) 
th_E.start() 
th_R.start()