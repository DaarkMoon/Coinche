#!/var/bin python

global Colorlist 
Colorlist = ["carreau", "pique", "trefle", "coeur"]

class Card():
    def __init__(self, value, color):
        assert isinstance(value, int), "value must be type of int."
        assert isinstance(color, str), "color must be type of str."
        if value > 8 or value <0:
            raise ValueError("value value must be between 0 and 7.")
        self.value = value
        if not color in Colorlist:
            raise ValueError("color value must be carreau, pique, trefle or coeur.") 
        self.color = color

    def __str__(self):
        return "value %s, color %s"%(self.value, self.color)

