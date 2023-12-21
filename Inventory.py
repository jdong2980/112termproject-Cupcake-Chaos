import math
from cmu_graphics import *
from PIL import Image
import os, pathlib

class Inventory:
    def __init__(self, app, player):
        self.item = player.getItem()
    def openImage(self, fileName):
        return Image.open(os.path.join(pathlib.Path(__file__).parent, fileName))
    def getImageFromName(self, item):
        start = "images/"
        if("CUPCAKE" in item):
            start+="Final/"
            item = item[:4]
        elif("Batter" in item):
            start+= "Batter/"
        elif("Cake" in item):
            start += "Cake/"
        elif("Topping" in item):
            start += "Topping/"
        elif ("Cup" in item):
            start += "Cup/"
        elif ("Frosting" in item):
            start += "Frosting/"
        return CMUImage(self.openImage(start + item + ".PNG").resize((80,80)))
    def setItem(self, item):
        self.item = item
    def showInventory(self):
        if(self.item == None):
            return CMUImage(self.openImage("images/GameScreen/None.PNG").resize((80, 80)))
        return self.getImageFromName(self.item)