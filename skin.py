#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from locals import *

class SkinError(Exception):
    def __init__(self,raison):
        self.raison = raison
     
    def __str__(self):
        return self.raison
        
class SkinPack():
    def __init__(self,name):
        path = "./Skin/"+name+"/"
        #ajouter check du fichier ! + check ratio ?
        img = pygame.image.load(path+"background.png")
        self.background = pygame.transform.smoothscale( img , (RES_WIDTH, RES_HEIGHT)).convert()
        
        #ajouter check du fichier !  + check ratio ?
        img = pygame.image.load(path+"back.png")
        self.back = pygame.transform.smoothscale( img , (RES_HEIGHT/12, RES_HEIGHT/8)).convert_alpha()


        #ajouter check du fichier !  + check ratio ?
        img  = pygame.image.load(path+"front.png")
        width  = img.get_width()
        height = img.get_height()
        if width%8 != 0:
            raise SkinError('Bad width resolution : %s pixel is not divisible by 8'%(width) )
    
        if height%4 != 0:
            raise SkinError('Bad height resolution : %s pixel is not divisible by 4'%(width) )
        
        card_width = width/8
        card_height = height/4
        card_size = (card_width , card_height)
        
        self.front = [[None]*8 for i in range(4)]
        for value in range(8):
            for color in range(4):
                rect = pygame.Rect((card_width*value , card_height*color), card_size)
                surf = pygame.Surface(card_size)
                surf.blit(img, (0,0) ,rect)
                self.front[color][value] = pygame.transform.smoothscale( surf , (RES_HEIGHT/12, RES_HEIGHT/8)).convert_alpha()
            
    def get_card(self,card_id):
        return self.front[card_id[1]][card_id[0]]
    
           