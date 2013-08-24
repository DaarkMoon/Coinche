# -*- coding: utf8 -*-

import socket
import sys
import threading
import random
import os
import logging
import logging.config
import time

SERVER_RECV_BUFFER = 512
class ThreadClient(threading.Thread): 
    '''dérivation d'un objet thread pour gérer la connection avec un client''' 
    def __init__(self, in_socket,server): 
        threading.Thread.__init__(self) 
        self.connection, self.adresse = in_socket 
        self.server = server
        self.logger = self.server.logger
        self.logger.info("New Client (%s:%s) connect"%(self.adresse[0], self.adresse[1]))
        self.nick = None
        self.room = None
    
    def __repr__(self):
        return "Thread %s [%s:%s] <%s>"%(self.ident,self.adresse[0], self.adresse[1],self.nick)
        
    def __str__(self):
        return "[%s:%s] <%s>"%(self.adresse[0], self.adresse[1],self.nick)

    def run(self):
        self.logger.debug("ThreadClient %s started.",self.ident)
        while True:
            self.send(self.process(self.recv()))
        
    def send(self,data):
        try:
            self.connection.send(data+'\r\n')
            self.logger.debug("Command send to %s : %s"%(self,data))
        except socket.error:
            self.disconect_on_error()

    def disconect_on_error(self):
        self.logger.error("Lost connection %s",self)
        del self.server.threads[self.ident]
        sys.exit()
        
    def recv(self):
        buff = ""
        while True:
            try:
                buff += self.connection.recv(SERVER_RECV_BUFFER)
                if buff.endswith('\r\n'):   #message always end with '\r\n'
                    break
                self.logger.debug("buffer oversize !")
            except socket.error:
                self.disconect_on_error()
        msg = buff[:-2]
        self.logger.debug("Command receive from %s : %s"%(self,msg))
        return msg    #retunr msg Without '\r\n'
        
    def process(self,msg):
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
        # elif self.nick == None:
            # return "ERROR NO_NICK No Nick, No Command"
        elif command == "CHAT":
            for th in self.server.threads.values():
                if th != self:
                    th.send("<%s> %s"%(self.nick,arg))
            return ""
        elif command == "END":
            self.send("END")
            self.connection.close()      # couper la connection côté serveur
            del self.server.threads[self.ident]        # supprimer son entrée dans le dictionnaire 
            self.logger.info("Client (%s:%s) disconect"%(self.adresse[0], self.adresse[1]))
            sys.exit()
        elif command == "SHUTDOWN":
            if arg != self.server.master_code:
                return "ERROR BAD_MASTER_CODE"
            return "ERROR NOT_IMPLEMENTED"%(command)
        elif command == "DEBUG":
            if arg != self.server.master_code:
                return "ERROR BAD_MASTER_CODE"
            s = "DEBUG :\n"
            for th in self.server.threads.values():
                s += "  "+ repr(th) + "\n"
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
    '''dérivation d'un objet thread pour gérer la connection avec un client''' 
    def __init__(self, id, master): 
        threading.Thread.__init__(self) 
        self.server = master.server
        self.id = id
        self.master = master
        self.players = [master]
        self.logger = self.server.logger
        self.logger.info("%s Create a new room with id %s"%(self.master.nick, self.id))
    
    def __repr__(self):
        return "Room %s <%s>,%s"%(self.id,self.master, self.players[1:])
        
    def run(self):
        self.logger.debug("ThreadRoom %s started.",self.ident)
        while True:
            for player in self.players:
                player.send("GIVE ME YOUR NAME !")
            time.sleep(5)


class Server:
    """
        Server TCP Multi threadé pour la coinche
    """
    def __init__(self,server_adress,max_listen=5,master_code='{0:x}'.format(random.getrandbits(64)),log_conf='log.cfg'):
        self.logger = self.init_logger(log_conf)

        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        try: 
            self.mySocket.bind(server_adress)
        except socket.error: 
            self.logger.error("Socket Connection Failed on %s",server_adress)
            sys.exit()
        self.logger.info("Server ready, waiting request ...")
        self.mySocket.listen(max_listen)

        self.master_code = master_code
        self.logger.critical("Master Code : %s",self.master_code)

        self.threads = {}                # dictionnaire des connections clients
        self.rooms = {}

    def init_logger(self,log_conf):
        if os.access(log_conf,os.F_OK):
            logging.config.fileConfig(log_conf) 
            logger = logging.getLogger()
            logger.debug("Loading log configuration")
        else:
            try:
                cfg = open(log_conf,'w')
            except IOError:
                logger = logging.getLogger()
                logger.setLevel(logging.DEBUG) 														# <- ajout config.txt
                formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
                fileHandler = logging.FileHandler('Coinche_server.log')								# <- ajout config.txt
                fileHandler.setLevel(logging.INFO)
                fileHandler.setFormatter(formatter)
                logger.addHandler(fileHandler)
                consoleHandler = logging.StreamHandler()
                consoleHandler.setLevel(logging.INFO)												# <- ajout config.txt
                logger.addHandler(consoleHandler)
                logger.warning("Can't create configuration file for log. Loading Hard-coded version")
                return logger		
			
            # Crétion du fichier de config (coder très salement :/ )
            cfg.write("[loggers]\nkeys=root\n\n[handlers]\nkeys=consoleHandler,fileHandler\n\n[formatters]\nkeys=simpleFormatter\n\n[logger_root]\nlevel=DEBUG\nhandlers=consoleHandler,fileHandler\n\n[handler_consoleHandler]\nclass=StreamHandler\nlevel=INFO\nargs=(sys.stdout,)\n\n[handler_fileHandler]\nclass=FileHandler\nlevel=INFO\nformatter=simpleFormatter\nargs=('Coinche_server.log', 'a')\n\n[formatter_simpleFormatter]\nformat=%(asctime)s %(levelname)-8s %(message)s\n")
            cfg.close()
            logging.config.fileConfig(log_conf) 
            logger = logging.getLogger()
            logger.warning("Log configuration file don't exist. Creating a new one")
        return logger        
        
    def run(self):
        while True:
            th = ThreadClient(self.mySocket.accept(),self) 
            th.start()
            self.threads[th.ident] = th
            
def main():
    HOST = 'localhost'
    PORT = 6804
    MASTER_CODE = "666"
    S = Server((HOST,PORT),master_code = MASTER_CODE) 
    S.run()

if __name__ == "__main__":
    main()