#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import threading 
import time
import sys
import pygame
from pygame.locals import *
from skin import *
from locals import *

class InterfaceError(Exception):
    def __init__(self,reason,detail=""):
        self.reason = reason
        self.detail = detail

    def __repr__(self):
        return self.reason + self.detail

        
class GUI:
    """
        Graphic User Interface
    """
    def __init__(self, resolution,FPS):
        pygame.init()
        self.resolution = resolution
        self.res_width = resolution[0]
        self.res_height = resolution[1]
        self.disp_surf = pygame.display.set_mode(resolution)
        self.disp_rect = self.disp_surf.get_rect()
        
        pygame.display.set_caption('PyCoinche')
        skin = SkinPack('std')
        self.FPSClock = pygame.time.Clock()
        self.FPS = FPS
        self.init_font('freesansbold.ttf',(16,24,32,48))

    def init_font(self,font_name,sizes):
        '''
            Construit un dict de Font, size doit être un iterrable contenant que des int
            (patch pour passer juste un int prévu)
        '''
        self.BASICFONT = {}
        for height in sizes:
            self.BASICFONT[height]=pygame.font.Font(font_name, height)
            
    def FPSSyncro(self):
        self.FPSClock.tick(self.FPS)
    
    def connect(self,server):
        self.server = server
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        try: 
            self.sock.connect(self.server)
            self.UDPThread = ThreadReception( self.sock )
        except socket.error: 
            print "Connection failed. Exit ..." 
            sys.exit()
        print "Connection established." 
        self.UDPThread.start()
        
    def send(self,data):
        try:
            self.sock.send(data+'\r\n')
        except socket.error:
            print "Lost connection"
            sys.exit()
            
    def terminate(self):
        self.send("END")
        self.sock.close()
        pygame.quit()
        sys.exit()
    
    def error_message(self,msg):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.terminate()
                elif event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        return False
                    elif event.key == K_RETURN:
                        return True
            msg_surf, msg_rect = self.prepare_message(msg,24,WHITE,self.display.get_rect().center)
            win_rect = msg_rect.inflate(5,5)
            pygame.draw.rect(self.display, BLACK, win_rect, 3)
            self.display.fill( RED, win_rect)
            self.display.blit(msg_surf, msg_rect)
            pygame.display.update()
            self.FPSSyncro()
    
    def main_menu(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.terminate()
                elif event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        return False
                    elif event.key == K_RETURN:
                        return True
    
    def prepare_message(self,msg,size,color,pos,align="center"):
        """prépare un message"""
        # ajouter vérif font size
        msg_surf = self.BASICFONT[size].render(msg, True, color)
        msg_rect = msg_surf.get_rect()
        setattr(msg_rect, align, pos)
        return msg_surf, msg_rect
    
    def draw_message(self,msg,size,color,pos,align="center"):
        """ prépare un message puis le blit imédiatement sur l'écran """
        msg_surf, msg_rect = self.prepare_message(msg,size,color,pos,align)
        self.disp_surf.blit(msg_surf, msg_rect)
        
    def quit(self):
        #ajouter écran de Fin
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or event.type == KEYUP:
                    self.terminate()
            self.disp_surf.fill(BLACK)
            x,y = self.disp_rect.center
            self.draw_message("Code Client",32,RED, (x,y-36))
            self.draw_message("by",16,RED, (x,y) )
            self.draw_message("DaarkMoon (daarkmoon@mailoo.org)",24,RED, (x,y+36))
            pygame.display.update()
            self.FPSSyncro()

            
class ThreadReception(threading.Thread): 
    """objet thread gérant la réception des messages""" 
    def __init__(self, conn): 
        threading.Thread.__init__(self) 
        self.connection = conn           # réf. du socket de connection 

    def run(self): 
        while 1: 
            message_recu = self.recv() 
            print message_recu
            if message_recu == "END":
                break
        print "Client END. Connexion shutdown." 
        self.connection.close() 

    def recv(self):
        buff = ""
        while True:
            try:
                buff += self.connection.recv(RECV_BUFF_SIZE)
                if buff.endswith('\r\n'):   #message always end with '\r\n'
                    break
                print "buffer oversize !"
            except socket.error:
                print "Lost connection"
                sys.exit()               
        return buff[:-2]    #retunr msg Without '\r\n'