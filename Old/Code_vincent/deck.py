#!/var/bin python
from card import Card, Colorlist

class Deck():

    def __init__(self):
        self.cardlist = []
        #create all card
        #loop in value with 0,1,...,7
        for value in range(0, 8):
            for color in Colorlist:
                self.cardlist.append(Card(value, color))
                
    #trump is "atout" in french             
    def set_trump(self, trump):
        if trump not in Colorlist:
            raise ValueError("Trump must be in colorlist.")
        else :
            self.trump = trump
            
        
    
