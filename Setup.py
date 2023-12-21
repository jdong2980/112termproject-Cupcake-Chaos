import math
from cmu_graphics import *
from PIL import Image
import os, pathlib
import random as rand

class Setup:
    """Sets everything into lists to compare"""
    def __init__(self, board):
        self.allItemsNameList = [
            "CherryTopping", "StrawberryTopping", "PinkFrosting", "YellowFrosting",
            "BlueCup", "OrangeCup", "BrownBatter", "WhiteBatter", "Plate", "Trash",
            "Oven", "Sink", "WhiteCake", "BrownCake"
        ]
        self.allFoodItemsNameList = [
            "CherryTopping", "StrawberryTopping", "PinkFrosting", "YellowFrosting",
            "BlueCup", "OrangeCup", "BrownBatter", "WhiteBatter", "WhiteCake", "BrownCake"
        ]
        self.allItems = [
            CMUImage(self.openImage("images/Topping/CherryTopping.PNG")),
            CMUImage(self.openImage("images/Topping/StrawberryTopping.PNG")),
            CMUImage(self.openImage("images/Frosting/PinkFrosting.PNG")),
            CMUImage(self.openImage("images/Frosting/YellowFrosting.PNG")),
            CMUImage(self.openImage("images/Cup/BlueCup.PNG")),
            CMUImage(self.openImage("images/Cup/OrangeCup.PNG")),
            CMUImage(self.openImage("images/Batter/BrownBatter.PNG")),
            CMUImage(self.openImage("images/Batter/WhiteBatter.PNG")),
            CMUImage(self.openImage("images/GameScreen/plate.png")),
            CMUImage(self.openImage("images/GameScreen/trash.PNG")),
            CMUImage(self.openImage("images/GameScreen/oven.PNG")),
            CMUImage(self.openImage("images/GameScreen/sink.jpeg").resize((80, 80))),
            # Assuming WhiteCake and BrownCake are not images but placeholders for some other logic
        ]
        self.itemList = list(range(0, board.getNumCounterTops()))
        rand.shuffle(self.itemList)

    def openImage(self, fileName):
        return Image.open(os.path.join(pathlib.Path(__file__).parent, fileName))
    def getAllItemsNameList(self):
        return self.allItemsNameList
    def getAllFoodItemsNameList(self):
        return self.allFoodItemsNameList
    def getAllItems(self):
        return self.allItems
    def getItemList(self):
        return self.itemList
