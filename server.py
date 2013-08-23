# -*- coding: utf8 -*-

import socket
import sys
import threading
import random

class ThreadClient(threading.Thread): 
    '''dérivation d'un objet thread pour gérer la connection avec un client''' 
    def __init__(self, in_socket,server): 
        threading.Thread.__init__(self) 
        self.connection, self.adresse = in_socket 
        self.server=server
        self.nick = None
        self.room = None
        print "Client (%s:%s) connect, thread %s started." %(self.adresse[0], self.adresse[1],self.getName())
    
    def __repr__(self):
        return "Thread %s [%s:%s] <%s>"%(self.ident,self.adresse[0], self.adresse[1],self.nick)
        
    def run(self):
        while True:
            self.send(self.process(self.recv()))

    def send(self,data):
        try:
            self.connection.send(data+'\r\n')
        except socket.error:
            print "Lost connection"
            sys.exit()

    def recv(self):
        buff = ""
        while True:
            try:
                buff += self.connection.recv(32)
                if buff.endswith('\r\n'):   #message always end with '\r\n'
                    break
                print "buffer oversize !"
            except socket.error:
                print "Lost connection"
                sys.exit()               
        return buff[:-2]    #retunr msg Withou '\r\n'
        
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
            return "NO HELP WRITEN"
        elif self.nick == None:
            return "ERROR NO_NICK No Nick, No Command"
        elif command == "END":
            self.connection.close()      # couper la connection côté serveur
            del self.server.threads[self.ident]        # supprimer son entrée dans le dictionnaire 
            print "Client (%s:%s) disconnect, thread %s terminated."%(self.adresse[0], self.adresse[1],self.getName())# à passé sur un logger
            sys.exit()
        elif command == "SHUTDOWN" and arg == self.server.master_code:
            print threading.enumerate()
            pass  #AJOUT DES KILL DES THREAD  UN PAR UN
        elif command == "DEBUG" and arg == self.server.master_code:
            s = ""
            for th in self.server.threads.values():
                s += str(th) + "\n"
            return "DEBUG " + s
        else:
            return "ERROR UKW_CMD %s"%(command)


class Server:
    """
        Server TCP Multi threadé pour la coinche
    """
    def __init__(self,server_adress,max_listen=5,master_code='{0:x}'.format(random.getrandbits(64))):
        self.master_code = master_code
        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        try: 
            self.mySocket.bind(server_adress)
        except socket.error: 
            print "Socket Connection Failed"  # à passé sur un logger
            sys.exit()
        print "Server ready, waiting request ..."  # à passé sur un logger
        self.mySocket.listen(max_listen)
        self.threads = {}                # dictionnaire des connections clients
        self.rooms = {}
        
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