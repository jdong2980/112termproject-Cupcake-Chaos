import random as rand
from PIL import Image as img
import os, pathlib
from cmu_graphics import *
import Timer
class Order:
    def __init__(self, app, board, DAY):
        self.DAY = DAY
        self.cupIndex = rand.randint(0,1)
        self.cupImage = CMUImage(self.getRandomImageFromFolder("images/Cup",["BlueCup.PNG", "OrangeCup.Png"], self.cupIndex, 0))
        self.cakeIndex = rand.randint(2, 3)
        self.cakeImage = CMUImage(self.getRandomImageFromFolder("images/Cake",["BrownCake.PNG", "WhiteCake.Png"], self.cakeIndex, 2))
        self.frostingIndex = rand.randint(4, 5)
        self.frostingImage = CMUImage(self.getRandomImageFromFolder("images/Frosting",["YellowFrosting.PNG", "PinkFrosting.Png"], self.frostingIndex,4))
        self.toppingIndex = rand.randint(6, 8)
        if(self.toppingIndex != 8):
            self.toppingImage = CMUImage(self.getRandomImageFromFolder("images/Topping", ["StrawberryTopping.PNG", "CherryTopping.Png"], self.toppingIndex,6))
            self.withTopping = True
            self.col = board.setOrder(4)
        else:
            self.toppingImage = None
            self.withTopping = False
            self.col = board.setOrder(3)
        self.board = board
        self.final = [self.cupImage, self.cakeImage, self.frostingImage,self.toppingImage]
        self.RESULT = [self.cupIndex, self.cakeIndex, self.frostingIndex, self.toppingIndex]
        self.initialTime = rand.randint(40 - (5 * DAY.getDay()) + (6 * DAY.getWaitTimeIncrement()),70-(5 * DAY.getDay()) + (6 * DAY.getWaitTimeIncrement()))
        # self.initialTime = rand.randint(10,15)
        self.timer = Timer.Timer(self.initialTime)
        self.endTime = -self.initialTime // 2
    """Determines if Order and user output"""
    def checkRESULT(self, attempt):
        if(len(attempt) == 3):
            return self.RESULT == attempt + [8]
        return self.RESULT == attempt
    def openImage(self, fileName):
        return img.open(os.path.join(pathlib.Path(__file__).parent, fileName))

    def getRandomImageFromFolder(self, pathFolder, imageList, index, subtracter):
        folder = pathFolder
        images = imageList
        selectedRandomImage = images[index-subtracter]
        return self.openImage(folder + "/" + selectedRandomImage)
    def leave(self):
        return self.endTime == self.timer.getTime()
    def getEndTime(self):
        return self.endTime
    def getRESULT(self):
        return self.RESULT
    def getInitialTime(self):
        return self.initialTime
    def getImageFolder(self):
        return None
    def getCupImage(self):
        return self.cupImage
    def getCakeImage(self):
        return self.cakeImage
    def getFrostingImage(self):
        return self.frostingImage
    def getToppingImage(self):
        if(self.withTopping):
            return self.toppingImage
    def getWithTopping(self):
        return self.withTopping
    def getFinal(self):
        return self.final
    def decreaseTimerByOne(self):
        return self.timer.decreaseTime(1)
    def getTime(self):
        return self.timer.getTime()
    """
    Moves current order to the very right
    Only accounts for 2 orders
    """
    def resetOrder(self):
        for i in range(8,10):
            for j in range(0,6):
                app.board.setBoard(j, i, 0)
        if(self.withTopping):
            self.col = self.board.setOrder(4)
        else:
            self.col = self.board.setOrder(3)
