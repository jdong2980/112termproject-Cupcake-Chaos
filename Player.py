import math
from cmu_graphics import *
from PIL import Image
import os, pathlib


class Player:
    """Source for Character Picture: https://github.com/summerthesun/undercooked/tree/main"""
    def __init__(self, app, board, onPlate, setup, oven, sink, money):
        self.xPosition = 0
        self.yPosition = 80
        self.spritestrip = [self.openImage('images/Player/down.png'), self.openImage('images/Player/right.png'), self.openImage(
            'images/Player/up.png'), self.openImage('images/Player/left.png')]
        self.sprites = []
        #Directions
        self.sprites.append(CMUImage(self.spritestrip[0].crop((0, 0, 115, 145)).resize((50,50))))
        self.sprites.append(CMUImage(self.spritestrip[1].crop((0, 0, 115, 145)).resize((50, 50))))
        self.sprites.append(CMUImage(self.spritestrip[2].crop((0, 0, 115, 145)).resize((50, 50))))
        self.sprites.append(CMUImage(self.spritestrip[3].crop((0, 0, 115, 145)).resize((50, 50))))

        self.spriteWidth = self.sprites[0].surface.get_width()
        self.spriteHeight = self.sprites[0].surface.get_height()
        self.spriteCounter = 0
        self.stepsPerSecond = 10
        self.board = board
        self.counterCoordinates = board.getCounterCoordinates()
        self.cols = self.board.getCol()
        self.rows = self.board.getRow()
        self.direction = "down"
        self.item = None
        self.hasItem = False
        self.onPlate = onPlate
        self.setup = setup
        self.ovenDone = True
        self.ovenOn = False
        self.ovenBatter = None
        self.sinkOn = False
        self.cherryWash = False
        self.strawberryWash = False
        self.oven = oven
        self.sink = sink
        self.money = money
    def getSinkOn(self):
        return self.sinkOn
    def setSinkOn(self, boolean):
        self.sinkOn = boolean
    def setOvenDone(self, boolean):
        self.ovenDone = boolean
    def getOvenDone(self):
        return self.ovenDone
    def getOvenOn(self):
        return self.ovenOn
    def getOvenBatter(self):
        return self.ovenBatter
    def getItem(self):
        return self.item
    def getHasItem(self):
        return self.hasItem
    def openImage(self, fileName):
        return Image.open(os.path.join(pathlib.Path(__file__).parent, fileName))
    def getSprites(self):
        return self.sprites
    def getXPosition(self):
        return self.xPosition
    def getYPosition(self):
        return self.yPosition
    def setXPosition(self, num):
        self.xPosition += num
    def setYPosition(self, num):
        self.yPosition += num
    def getDirection(self):
        return self.direction
    def setDirection(self, direction):
        self.direction = direction
    def setCherryWash(self, boolean):
        self.cherryWash = boolean
    def setStrawberryWash(self, boolean):
        self.strawberryWash = boolean
    def getStrawberryWash(self):
        return self.strawberryWash
    def getCherryWash(self):
        return self.cherryWash
    """Checks if Player is in a counter"""
    def canMove(self, cellWidth, cellHeight):
        count = 0
        for counterY, counterX in self.counterCoordinates:
            counterLeft = counterX * cellWidth
            counterRight = counterLeft + cellWidth
            counterTop = counterY * cellHeight
            counterBottom = counterTop + cellHeight
            spriteRight = self.xPosition + self.spriteWidth
            spriteBottom = self.yPosition + self.spriteHeight
            if (self.xPosition < counterRight and
                    spriteRight > counterLeft and
                    self.yPosition < counterBottom and
                    spriteBottom > counterTop):
                self.reAdjust()
                return False
            count+=1
        return True
    """Allows player to walk after running into counter"""
    def reAdjust(self):
        steps = 10
        if(self.direction == "left"):
            self.xPosition += steps
        elif(self.direction == "right"):
            self.xPosition -= steps
        elif(self.direction == "up"):
            self.yPosition += steps
        elif (self.direction == "down"):
            self.yPosition -= steps
    """Check for walls"""
    def checkBoundary(self, mapWidth, mapHeight):
        if (self.xPosition < 0):
            self.xPosition = 0
        elif (self.xPosition + self.spriteWidth > mapWidth):
            self.xPosition = mapWidth - self.spriteWidth
        if(self.yPosition < 0):
            self.yPosition = 0
        elif (self.yPosition + self.spriteHeight > mapHeight):
            self.yPosition = mapHeight - self.spriteHeight
        return True

    """A lot of conditionals upon picking up item from plate, sink, and oven"""
    def itemPickUp(self):
        spriteCenterX = self.xPosition + self.spriteWidth//2
        spriteCenterY = self.yPosition + self.spriteHeight//2
        cellX, cellY = self.board.getRowAndCol(spriteCenterX, spriteCenterY)
        if(not self.hasItem):
            if(self.direction == "up" and self.board.isCounter(cellY - 1, cellX) and
                    self.board.getMapOfFoodItem(cellY-1, cellX) in self.setup.getAllFoodItemsNameList()):
                self.item = self.board.getMapOfFoodItem(cellY-1, cellX)
                self.money.addMoney(-.5 - ((self.money.getDay()-1) * .10))
                self.hasItem = True
                if(self.item == "StrawberryTopping"):
                    self.strawberryWash = False
                elif(self.item == "CherryTopping"):
                    self.cherryWash = False
            elif(self.direction == "down" and self.board.isCounter(cellY + 1, cellX) and
                 self.board.getMapOfFoodItem(cellY+1, cellX) in self.setup.getAllFoodItemsNameList()):
                self.item = self.board.getMapOfFoodItem(cellY+1, cellX)
                self.money.addMoney(-.5 - ((self.money.getDay()-1) * .10))
                self.hasItem = True
                if (self.item == "StrawberryTopping"):
                    self.strawberryWash = False
                elif (self.item == "CherryTopping"):
                    self.cherryWash = False
            elif(self.direction == "left" and self.board.isCounter(cellY, cellX-1) and
                 self.board.getMapOfFoodItem(cellY,cellX-1) in self.setup.getAllFoodItemsNameList()):
                self.item = self.board.getMapOfFoodItem(cellY, cellX-1)
                self.money.addMoney(-.5 - ((self.money.getDay()-1) * .10))
                self.hasItem = True
                if (self.item == "StrawberryTopping"):
                    self.strawberryWash = False
                elif (self.item == "CherryTopping"):
                    self.cherryWash = False
            elif(self.direction == "right" and self.board.isCounter(cellY, cellX+1) and
                 self.board.getMapOfFoodItem(cellY, cellX+1) in self.setup.getAllFoodItemsNameList()):
                self.item = self.board.getMapOfFoodItem(cellY, cellX+1)
                self.money.addMoney(-.5 - ((self.money.getDay()-1) * .10))
                self.hasItem = True
                if (self.item == "StrawberryTopping"):
                    self.strawberryWash = False
                elif (self.item == "CherryTopping"):
                    self.cherryWash = False
            elif(self.direction == "up" and self.board.isCounter(cellY - 1, cellX) and
                    self.board.getMapOfFoodItem(cellY-1, cellX) == "Plate"):
                self.platePickUp()
            elif(self.direction == "down" and self.board.isCounter(cellY + 1, cellX) and
                 self.board.getMapOfFoodItem(cellY+1, cellX) == "Plate"):
                self.platePickUp()
            elif(self.direction == "left" and self.board.isCounter(cellY, cellX-1) and
                 self.board.getMapOfFoodItem(cellY,cellX-1) == "Plate"):
                self.platePickUp()
            elif(self.direction == "right" and self.board.isCounter(cellY, cellX+1) and
                 self.board.getMapOfFoodItem(cellY, cellX+1) == "Plate"):
                self.platePickUp()
            elif (self.direction == "up" and self.board.isCounter(cellY - 1, cellX) and
                      self.board.getMapOfFoodItem(cellY - 1, cellX) == "Oven" and self.ovenOn and self.ovenDone):
                self.ovenOn = False
                self.item = self.ovenBatter+"Cake"
                self.hasItem = True
                self.oven.reset()
            elif (self.direction == "down" and self.board.isCounter(cellY + 1, cellX) and
                  self.board.getMapOfFoodItem(cellY + 1, cellX) == "Oven" and self.ovenOn and self.ovenDone):
                self.ovenOn = False
                self.item = self.ovenBatter + "Cake"
                self.hasItem = True
                self.oven.reset()
            elif (self.direction == "left" and self.board.isCounter(cellY, cellX - 1) and
                  self.board.getMapOfFoodItem(cellY, cellX - 1) == "Oven" and self.ovenOn and self.ovenDone):
                self.ovenOn = False
                self.item = self.ovenBatter + "Cake"
                self.hasItem = True
                self.oven.reset()
            elif (self.direction == "right" and self.board.isCounter(cellY, cellX + 1) and
                  self.board.getMapOfFoodItem(cellY, cellX + 1) == "Oven" and self.ovenOn and self.ovenDone):
                self.ovenOn = False
                self.item = self.ovenBatter + "Cake"
                self.hasItem = True
                self.oven.reset()
    """Picking up from plate"""
    def platePickUp(self):
        if (len(self.onPlate.getIngredientNameList()) > 0):
            self.item = self.onPlate.pop()
            self.hasItem = True
            if (self.onPlate.getIsFinal()):
                self.onPlate.setIsHoldingFinal(True)
            self.onPlate.setIsFinal(False)
            if (self.item == "StrawberryTopping"):
                self.strawberryWash = True
            elif (self.item == "CherryTopping"):
                self.cherryWash = True
    """Conditional on what to do when player drops item on plate, trash, oven, and sink"""
    def itemDrop(self):
        spriteCenterX = self.xPosition + self.spriteWidth//2
        spriteCenterY = self.yPosition + self.spriteHeight//2
        cellX, cellY = self.board.getRowAndCol(spriteCenterX, spriteCenterY)
        if(self.hasItem):
            if (self.direction == "up" and self.board.isCounter(cellY - 1, cellX) and
                    self.board.getMapOfFoodItem(cellY - 1, cellX) == "Trash"):
                self.trashDrop()
            elif (self.direction == "down" and self.board.isCounter(cellY + 1, cellX) and
                  self.board.getMapOfFoodItem(cellY + 1, cellX) == "Trash"):
                self.trashDrop()
            elif (self.direction == "left" and self.board.isCounter(cellY, cellX - 1) and
                  self.board.getMapOfFoodItem(cellY, cellX - 1) == "Trash"):
                self.trashDrop()
            elif (self.direction == "right" and self.board.isCounter(cellY, cellX + 1) and
                  self.board.getMapOfFoodItem(cellY, cellX + 1) == "Trash"):
                self.trashDrop()
            elif ((self.item == "BrownBatter" or self.item == "WhiteBatter") and not self.ovenOn):
                if (self.direction == "up" and self.board.isCounter(cellY - 1, cellX) and
                        self.board.getMapOfFoodItem(cellY - 1, cellX) == "Oven"):
                    if(self.item == "BrownBatter"):
                        self.ovenBatter = "Brown"
                    else:
                        self.ovenBatter = "White"
                    self.ovenOn = True
                    self.hasItem = False
                    self.item = None
                    self.ovenDone = False
                elif (self.direction == "down" and self.board.isCounter(cellY + 1, cellX) and
                      self.board.getMapOfFoodItem(cellY + 1, cellX) == "Oven"):
                    if (self.item == "BrownBatter"):
                        self.ovenBatter = "Brown"
                    else:
                        self.ovenBatter = "White"
                    self.ovenOn = True
                    self.hasItem = False
                    self.item = None
                    self.ovenDone = False
                elif (self.direction == "left" and self.board.isCounter(cellY, cellX - 1) and
                      self.board.getMapOfFoodItem(cellY, cellX - 1) == "Oven"):
                    if (self.item == "BrownBatter"):
                        self.ovenBatter = "Brown"
                    else:
                        self.ovenBatter = "White"
                    self.ovenOn = True
                    self.hasItem = False
                    self.item = None
                    self.ovenDone = False
                elif (self.direction == "right" and self.board.isCounter(cellY, cellX + 1) and
                      self.board.getMapOfFoodItem(cellY, cellX + 1) == "Oven"):
                    if (self.item == "BrownBatter"):
                        self.ovenBatter = "Brown"
                    else:
                        self.ovenBatter = "White"
                    self.ovenOn = True
                    self.hasItem = False
                    self.item = None
                    self.ovenDone = False
            elif (self.item == "StrawberryTopping"):
                if (self.direction == "up" and self.board.isCounter(cellY - 1, cellX) and
                        self.board.getMapOfFoodItem(cellY - 1, cellX) == "Sink" and not self.strawberryWash):
                    self.sink.reset()
                    self.sinkOn = True
                elif (self.direction == "down" and self.board.isCounter(cellY + 1, cellX) and
                      self.board.getMapOfFoodItem(cellY + 1, cellX) == "Sink" and not self.strawberryWash):
                    self.sink.reset()
                    self.sinkOn = True
                elif (self.direction == "left" and self.board.isCounter(cellY, cellX - 1) and
                      self.board.getMapOfFoodItem(cellY, cellX - 1) == "Sink" and not self.strawberryWash):
                    self.sink.reset()
                    self.sinkOn = True
                elif (self.direction == "right" and self.board.isCounter(cellY, cellX + 1) and
                      self.board.getMapOfFoodItem(cellY, cellX + 1) == "Sink" and not self.strawberryWash):
                    self.sink.reset()
                    self.sinkOn = True
                elif (self.direction == "up" and self.board.isCounter(cellY - 1, cellX) and
                        self.board.getMapOfFoodItem(cellY - 1, cellX) == "Plate" and self.strawberryWash):
                    self.plateDrop()
                elif (self.direction == "down" and self.board.isCounter(cellY + 1, cellX) and
                      self.board.getMapOfFoodItem(cellY + 1, cellX) == "Plate" and self.strawberryWash):
                    self.plateDrop()
                elif (self.direction == "left" and self.board.isCounter(cellY, cellX - 1) and
                      self.board.getMapOfFoodItem(cellY, cellX - 1) == "Plate" and self.strawberryWash):
                    self.plateDrop()
                elif (self.direction == "right" and self.board.isCounter(cellY, cellX + 1) and
                      self.board.getMapOfFoodItem(cellY, cellX + 1) == "Plate" and self.strawberryWash):
                    self.plateDrop()
            elif(self.item == "CherryTopping"):
                if (self.direction == "up" and self.board.isCounter(cellY - 1, cellX) and
                        self.board.getMapOfFoodItem(cellY - 1, cellX) == "Sink" and not self.cherryWash):
                    self.sink.reset()
                    self.sinkOn = True
                elif (self.direction == "down" and self.board.isCounter(cellY + 1, cellX) and
                      self.board.getMapOfFoodItem(cellY + 1, cellX) == "Sink" and not self.cherryWash):
                    self.sink.reset()
                    self.sinkOn = True
                elif (self.direction == "left" and self.board.isCounter(cellY, cellX - 1) and
                      self.board.getMapOfFoodItem(cellY, cellX - 1) == "Sink" and not self.cherryWash):
                    self.sink.reset()
                    self.sinkOn = True
                elif (self.direction == "right" and self.board.isCounter(cellY, cellX + 1) and
                      self.board.getMapOfFoodItem(cellY, cellX + 1) == "Sink" and not self.cherryWash):
                    self.sink.reset()
                    self.sinkOn = True
                elif (self.direction == "up" and self.board.isCounter(cellY - 1, cellX) and
                        self.board.getMapOfFoodItem(cellY - 1, cellX) == "Plate" and self.cherryWash):
                    self.plateDrop()
                elif (self.direction == "down" and self.board.isCounter(cellY + 1, cellX) and
                      self.board.getMapOfFoodItem(cellY + 1, cellX) == "Plate" and self.cherryWash):
                    self.plateDrop()
                elif (self.direction == "left" and self.board.isCounter(cellY, cellX - 1) and
                      self.board.getMapOfFoodItem(cellY, cellX - 1) == "Plate" and self.cherryWash):
                    self.plateDrop()
                elif (self.direction == "right" and self.board.isCounter(cellY, cellX + 1) and
                      self.board.getMapOfFoodItem(cellY, cellX + 1) == "Plate" and self.cherryWash):
                    self.plateDrop()
            elif(not (self.item == "BrownBatter" or self.item == "WhiteBatter") and
                 not (self.item == "StrawberryTopping" or self.item == "CherryTopping")):
                if (self.direction == "up" and self.board.isCounter(cellY - 1, cellX) and
                        self.board.getMapOfFoodItem(cellY - 1, cellX) == "Plate"):
                    self.plateDrop()
                elif (self.direction == "down" and self.board.isCounter(cellY + 1, cellX) and
                      self.board.getMapOfFoodItem(cellY + 1, cellX) == "Plate"):
                    self.plateDrop()
                elif (self.direction == "left" and self.board.isCounter(cellY, cellX - 1) and
                      self.board.getMapOfFoodItem(cellY, cellX - 1) == "Plate"):
                    self.plateDrop()
                elif (self.direction == "right" and self.board.isCounter(cellY, cellX + 1) and
                      self.board.getMapOfFoodItem(cellY, cellX + 1) == "Plate"):
                    self.plateDrop()
    """Dropping onto plate"""
    def plateDrop(self):
        item = self.item
        self.onPlate.addIngredientList(item)
        if (self.onPlate.getIsHoldingFinal()):
            self.onPlate.setIsHoldingFinal(False)
            self.onPlate.setIsFinal(True)
        self.hasItem = False
        self.item = None
    """Dropping into trash"""
    def trashDrop(self):
        item = self.item
        if (self.onPlate.getIsHoldingFinal()):
            self.onPlate.trashFinal()
        self.onPlate.setIsHoldingFinal(False)
        self.hasItem = False
        self.item = None

    def reset(self):
        self.onPlate.setIsHoldingFinal(False)
        self.hasItem = False
        self.item = None
    def distance(self, x, y):
        return math.sqrt((self.xPosition - x) ** 2 + (self.yPosition - y) ** 2)



