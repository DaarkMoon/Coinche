# -*- coding: UTF-8 -*-

import socket
import time

PORT = 6804
HOST = "localhost"
TIMEOUT = 1

class WebPlayer():
    def __init__(self):
       self.name = ""
       self.room = -1  # -1 means wait room
       self.last_seen = time.time()

class CoincheServer():
    def __init__(self, host, port,timeout):
        self.players = {}
        self.nick_list =[]
        self.rooms = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, port))
        self.sock.settimeout(timeout)
        
    def run(self):
        while True:
            try:
                self.process(self.sock.recvfrom(1024))
            except socket.timeout:
                pass
            except socket.error, err:
                print "Disconected !"
            
    def process(self,recv):
        data,address = recv
        print "receive : %s from %s on port %s"%(data, address[0],address[1])
        
        data = data.split(' ',1)
        command = data[0]
        if len(data) == 2:
            arg = data[1]
        if command == "CONNECT":
            self.sock.sendto("CONNECTED", address)
            self.players[address] = WebPlayer()
        elif command == "NICK" and arg !="": #Check plus sérieux des pseudo à faire
            self.update_nick_list()
            if arg not in nick_list:
                self.players[adress].name = arg
                self.update_nick_list()
                self.sock.sendto("OK", address)
            else:
                self.sock.sendto("ERROR Nick alaways taken", address)
            
        else:
            self.sock.sendto("BAD REQUEST", address)        

    def update_nick_list(self):
        nicklist = []
        for player in self.players.values():
            self.nick_list.append(player.name)

def main():
    server = CoincheServer(HOST, PORT,TIMEOUT)
    server.run()
    
if __name__ == "__main__":
    main()