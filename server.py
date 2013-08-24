# -*- coding: utf8 -*-

import socket
import sys
import threading
import random
import os
import logging
import logging.config
import time

class ThreadClient(threading.Thread): 
    '''
        On créer un thread client en dérivation d'un objet thread
        
        attributs
            server      : retro-lien sur le server pour ajouter/suprimer la room
            logger      : retro-lien sur le logger du server
            nick        : pseudo du joueur
            room        : room dans lequel le joueur se trouve, None pour aucune room
            adresse     : adresse IP du joueur sous forme d'un tuple (IPv4,port)
            connection  : socket de connection
    '''
    def __init__(self, in_socket,server): 
        """
            Initialisation du thread client
            
            Parametre
                in_socket   : socket entrant
                server      : retro-lien sur le serveur
        """
        threading.Thread.__init__(self)  # on charge la classe Thread pour l'étendre au lieu de l'écraser
        self.connection, self.adresse = in_socket 
        self.server = server
        self.logger = self.server.logger
        self.logger.info("New Client (%s:%s) connect"%(self.adresse[0], self.adresse[1]))
        self.nick = None
        self.room = None
    
    def __repr__(self):
        """
            Detailled representation of ThreadClient
            must be improve to respect philosophy of __repr__
        """
        return "Thread %s [%s:%s] <%s>"%(self.ident,self.adresse[0], self.adresse[1],self.nick)
        
    def __str__(self):
        """ Ligth representation of ThreadClient """
        return "[%s:%s] <%s>"%(self.adresse[0], self.adresse[1],self.nick)

    def run(self):
        """
            Boucle du thread Client
            
            On attend de recevoir quelquechose
            quand on le reçois on le traite avec process
            puis on revoie le retrour de process avec send
        """
        self.logger.debug("ThreadClient %s started.",self.ident)
        while True:
            self.send(self.process(self.recv()))
        
    def send(self,data):
        """ Version sure pour l'envoie de données avec deconxion sur erreur du socket """
        try:
            self.connection.send(data+'\r\n')       # on ajoute "\r\n" pour signifier la fin des données
            self.logger.debug("Command send to %s : %s"%(self,data))
        except socket.error, err:
            self.disconect_on_error()   # En cas d'erreur on deconecte le client

    def disconect_on_error(self,err):
        """ Deconection propre d'un client sur une erreur """
        self.logger.error("Lost connection from %s, reason %s"%(self,err))  # On log l'erreur
        del self.server.threads[self.ident]                                 # On suprime le thread client de la liste des thread client du server
        sys.exit()                                                          # On termine le thread                    
        
    def recv(self):
        """ Reception des données bufferisé, ce qui assure que toute les donées sont reçus """
        buff = ""
        while True:
            try:
                buff += self.connection.recv(1) # On lit octet par octet pour éviter d'avoir 2 commande à la suite (surement pas optimal)
                if buff.endswith('\r\n'):       # le message finnit toujours avec '\r\n'
                    break
            except socket.error:
                self.disconect_on_error()
        msg = buff[:-2] # msg sans le '\r\n' signifant la fin
        self.logger.debug("Command receive from %s : %s"%(self,msg))
        return msg
        
    def process(self,msg):
        """
            On traduit le message en commande on le traite.
            Les diverses commandes sont :
            NICK    : changer de pseudo
            HELP    : aide
            CHAT    : envoyer un message texte
            END     : se deconecter
            SHUTDOWN: extinction du serveur
            DEBUG   : info de debugage
            JOIN    : rejoindre une room
            QUIT    : quitter la room
        """
        
        # on split le msg pour avoir la command et les arguments
        if ' ' in msg:
            command,arg = msg.split(' ',1)
        else:
            command = msg
            arg = None       
        
        if command == "NICK":
            if arg == None:
                return "ERROR NICK_EMPTY Asked nick is empty"
            if self.nick == arg:
                return "ERROR NICK_YOUR %s is already your nick"%(self.nick)
            for client in self.server.threads.values():
                if client.nick == arg:
                    return "ERROR NICK_TAKEN Nick %s Already Taken"%(arg)
            self.nick = arg
            return "OK"
        elif command == "HELP":
            # faire un help file
            return "NO HELP WRITEN"
        elif self.nick == None:
            return "ERROR No Nick, No Command\nType \"NICK your_nick\" to set your nick"
        elif command == "END":
            self.send("END")
            self.connection.close()      # couper la connection côté serveur
            del self.server.threads[self.ident]        # supprimer son entrée dans le dictionnaire 
            self.logger.info("Client (%s:%s) disconect"%(self.adresse[0], self.adresse[1]))
            sys.exit()
        elif command == "CHAT":
            for th in self.server.threads.values():
                if th != self:
                    th.send("<%s> %s"%(self.nick,arg))
            return ""
        elif command == "SHUTDOWN":
            if arg != self.server.master_code:
                return "ERROR BAD_MASTER_CODE"
            return "ERROR SHUTDOWN NOT IMPLEMENTED"
        elif command == "DEBUG":
            if arg != self.server.master_code:
                return "ERROR BAD_MASTER_CODE"
            s = "DEBUG :\n  CLIENT :\n"
            for th in self.server.threads.values():
                s += " "*4+ repr(th) + "\n"
            s += "  ROOM :\n"    
            for th in self.server.threads.values():
                s += " "*4+ repr(th) + "\n"
            return s
        elif command == "JOIN":
            if arg not in self.server.rooms:
                self.room = ThreadRoom(arg,self)
                self.server.rooms[arg] = self.room
                self.room.start()
            else:
                self.server.rooms[arg].players.append(self)
            return "OK"
        elif command == "QUIT":
            if self.room == None:
                return "ERROR You are not in any room"
            else:
                self.room.players.remove(self)
                self.room = None
                return "OK"
        else:
            return "ERROR UKW_CMD %s"%(command)
        return "ERROR SERVER RETURN NOTHING"

        
class ThreadRoom(threading.Thread): 
    '''
        On créer un thread rooom en dérivation d'un objet thread
        
        attributs
            server  : retro-lien sur le server pour ajouter/suprimer la room
            id      : numéro d'identification de la room
            master  : thread client du maître de le room
            players : liste des threads client (maître inclut)
            logger  : retro-lien sur le logger du server
    ''' 
    def __init__(self, id, master): 
        """
            initialisation de la room

            Parametre
                id      : id de la chambre (type int)
                master  : maîtrede la chambre (thread client)
        """
        threading.Thread.__init__(self) # on charge la classe Thread pour l'étendre au lieu de l'écraser
        self.server = master.server
        self.id = id
        self.master = master
        self.players = [master]
        self.logger = self.server.logger
        self.logger.info("%s Create a new room with id %s"%(self.master.nick, self.id))
    
    def __repr__(self):
        """
            Représentation de la room par son id, et la liste des joueurs
            le maitre de la room est indiqué par <>
        """
        return "Room %s <%s> %s"%(self.id,self.master, self.players[1:])
        
    def run(self):
        """
            Boucle principale de la room.
            Le code actuel n'est là qu'à des fins de test
        """
        self.logger.debug("ThreadRoom %s started.",self.ident)
        while True:
            for player in self.players:
                player.send("GIVE ME YOUR NAME !")
            time.sleep(5)


class Server:
    """
        Server TCP créant un thread client à chaque connection.
        C'est le thread client qui réagit au commandes
        
        attributs
            logger      : objet de type logger pour permettre le logage
            mySocket    : socket d'écoute
            master_code : code maître pour accéder à certaine fonction de maintenace ou d'administration
            threads     : dictionnaire des threads client
            rooms       : dictionnaire des threads room
     """
    def __init__(self,server_address,max_listen=5,master_code='{0:x}'.format(random.getrandbits(64)),log_conf='log.cfg'):
        """
            Initialise le serveur
            
            Parametre
                server_adress   : adresse d'ecoute sous forme d'un tuple (host,port)
                max_listen      : nombre max de connection en attentes
                master_code     : code maître pour accéder à certaine fonction de maintenace ou d'administration
                                  si ce dernier n'est pas précisser c'est une valeur hexa de 64 bits
                log.cfg         : fichier de configuration du logger
        """
        
        self.logger = self.init_logger(log_conf)    # on commence par initialiser le logger pour pouvor tout logger

        #Mise en place du socket d'écoute
        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        try: 
            self.mySocket.bind(server_address)
        except socket.error, err:
            # En cas d'erreur on log l'erreur et on quittes
            self.logger.error("Socket Connection Failed on %s, error : %s"%(server_address,err))
            sys.exit()
        self.logger.info("Server ready, waiting request ...")
        self.mySocket.listen(max_listen) # Configuration du nombre max de connection en attentes

        self.master_code = master_code
        self.logger.critical("Master Code : %s",self.master_code) # Affichage du master code dans le log pour les cas ou ce denier n'est précisé

        self.threads = {}   # initialisation du dictionnaire des threads client
        self.rooms = {}     # initialisation du dictionnaire des threads room

    def init_logger(self,log_conf):
        """
            Initialisation du logger, d'après le fichier de configuration log_conf
            Si le fichier ne peut être lu on en charge la configuration  par defaut
            On essaye en même temps de créer ce fichier de configuration
        """
        if os.access(log_conf,os.R_OK):                 # on essaye de lire le fichier                      
            logging.config.fileConfig(log_conf)         # Si ça marche on charge
            logger = logging.getLogger()
            logger.debug("Log configuration loaded")
        else: 
            try:                                        # sinon on essaye créer le fichier
                cfg = open(log_conf,'w')
            except IOError:                             # on gère le cas ou l'on as pas les droits en écriture en utilisant la version hard-coded
                logger = logging.getLogger()
                logger.setLevel(logging.DEBUG)
                formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
                fileHandler = logging.FileHandler('Coinche_server.log')
                fileHandler.setLevel(logging.INFO)
                fileHandler.setFormatter(formatter)
                logger.addHandler(fileHandler)
                consoleHandler = logging.StreamHandler()
                consoleHandler.setLevel(logging.INFO)
                logger.addHandler(consoleHandler)
                
                # on warn pour l'impossibilté d'écrire le fichier de conf
                logger.warning("Can't create configuration file for log. Loading Hard-coded version")
                
                return logger		
			
            # Ecriture du fichier de config (coder très très salement :/ ) quand on peut
            cfg.write("[loggers]\nkeys=root\n\n[handlers]\nkeys=consoleHandler,fileHandler\n\n[formatters]\nkeys=simpleFormatter\n\n[logger_root]\nlevel=DEBUG\nhandlers=consoleHandler,fileHandler\n\n[handler_consoleHandler]\nclass=StreamHandler\nlevel=INFO\nargs=(sys.stdout,)\n\n[handler_fileHandler]\nclass=FileHandler\nlevel=INFO\nformatter=simpleFormatter\nargs=('Coinche_server.log', 'a')\n\n[formatter_simpleFormatter]\nformat=%(asctime)s %(levelname)-8s %(message)s\n")
            cfg.close()
            
            # On charge le fichier que l'on vient de créer
            logging.config.fileConfig(log_conf)
            logger = logging.getLogger()
            
            # on warn sur le fichier de conf inexistant
            logger.warning("Log configuration file don't exist. Creating a new one") 
        return logger        
        
    def run(self):
        """
            Lance le serveur dans une boucle infinies
            Un thread Client est créer à chaque nouvelle connection
        """
        while True:
            th = ThreadClient(self.mySocket.accept(),self)  # initialisation du thread à chaque connection reçu
            th.start()                                      # on lance le thread et on continue
            self.threads[th.ident] = th                     # on repére chaque thread par son numéro (unique)

            
def main():
    """ Lance le serveur en local sur le port par défaut (6804) avec le code maître 666 """
    HOST = 'localhost'
    PORT = 6804
    MASTER_CODE = "666"
    S = Server((HOST,PORT),master_code = MASTER_CODE) 
    S.run()

    
if __name__ == "__main__":
    main()