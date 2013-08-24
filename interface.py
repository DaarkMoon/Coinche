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
            self.error_message("Connection to server failed.\nPress any key to exit ...") 
            sys.exit()
        print "Connection established." 
        self.UDPThread.start()
        
    def send(self,data):
        try:
            self.sock.send(data+'\r\n')
        except socket.error:
            print "Lost connection"
            sys.exit()
            
    def set_nick(self,nick):
        self.send("NICK %s"%nick)
        while True:
            for event in pygame.event.get():
                print event
                if event.type == USEREVENT:
                    if event.dict['msg'] == "OK":
                        return True
                    else:
                        return False
            self.FPSSyncro()
            
    def terminate(self):
        self.send("END")
        self.sock.close()
        pygame.quit()
        sys.exit()
    
    def error_message(self,msg):
        msg_surf, msg_rect = self.prepare_message(msg,24,BLACK,self.disp_rect.center)
        win_rect = msg_rect.inflate(8,8)
        pygame.draw.rect(self.disp_surf, DARKGREY, win_rect, 3)
        self.disp_surf.fill( LIGHTGREY, win_rect)
        self.disp_surf.blit(msg_surf, msg_rect)
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.terminate()
                elif event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        return False
                    elif event.key == K_RETURN:
                        return True
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
                elif event.type == USEREVENT:
                    msg = event.dict['msg']
                    if ' ' in msg:
                        command,arg = msg.split(' ',1)
                    else:
                        command = msg
                        arg = None
                    if command == "ERROR":
                        self.error_message(arg)
            self.FPSSyncro()
            
    def prepare_message(self,msg,size,color,pos,align="center",interline=0.25):
        """prépare un message"""
        # ajouter vérif font size
        if '\n' in msg:
            msg_rect = None
            tmp_surf = pygame.surface.Surface(self.disp_rect.size, pygame.SRCALPHA)
            for id,line in enumerate(msg.split('\n')):
                surf, rect = self.prepare_message(line,size,color,pos,align)
                rect.move_ip(0, size * (id + interline) )
                tmp_surf.blit(surf,rect)
                if msg_rect == None:
                    msg_rect = rect
                else:
                    msg_rect.union_ip(rect)
            msg_surf = pygame.surface.Surface(msg_rect.size, pygame.SRCALPHA)
            msg_surf.blit(tmp_surf, (0,0), msg_rect)
            setattr(msg_rect, align, pos)
            
        else:
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
            self.draw_message("Code Client\nby\nDaarkMoon (daarkmoon@mailoo.org)",24,RED, self.disp_rect.center)
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
            pygame.event.post(pygame.event.Event(USEREVENT,msg=message_recu))
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