from cmu_graphics import *
from PIL import Image
import os, pathlib

class OnPlate:
    def __init__(self, board):
        self.currRow = 8
        self.board = board
        self.ingredientList = [CMUImage(self.openImage("images/GameScreen/inventory.PNG"))]
        self.ingredientNameList = []
        self.currIngredientIndex = []
        self.isFinal = False
        self.isHoldingFinal = False
        self.lowestRow = 9
    def getLowestRow(self):
        return self.lowestRow
    def openImage(self, fileName):
        return Image.open(os.path.join(pathlib.Path(__file__).parent, fileName))
    """Adding to OnPlate"""
    def addIngredientList(self, item):
        if(self.currRow == 0):
            self.currRow = 1
            # self.ingredientList.remove()
        self.board.setBoard(self.currRow, 0, 3)
        self.currRow -= 1
        cmuImage = self.getImageFromName(item)
        self.ingredientList.insert(0, cmuImage)
        self.ingredientNameList.insert(0, item)
        self.currIngredientIndex.append(self.getIndexFromItem(item))
    """Used for Border of OnPlate"""
    def updateLowestRow(self):
        for row in range(len(self.board.getBoard())):
            for col in range(len(self.board.getBoard()[0])):
                if(self.board.getBoard()[row][col] == 3):
                    self.lowestRow = row
                    return
    """Removing from Plate"""
    def pop(self):
        if(len(self.ingredientNameList) > 0):
            if(not self.isFinal):
                self.currIngredientIndex.pop()
            self.ingredientList.pop(0)
            self.currRow += 1
            self.board.setBoard(self.currRow, 0, 0)
            return self.ingredientNameList.pop(0)

    def resetCurrIngredientIndex(self):
        self.currIngredientIndex = []
    def getIngredientList(self):
        return self.ingredientList
    def getIngredientNameList(self):
        return self.ingredientNameList
    def getCurrIngredientIndex(self):
        return self.currIngredientIndex
    def getImageFromName(self, item):
        start = "images/"
        if("CUPCAKE" in item):
            start+="Final/"
            item = item[:4]
        elif("Cake" in item):
            start += "Cake/"
        elif("Topping" in item):
            start += "Topping/"
        elif ("Cup" in item):
            start += "Cup/"
        elif ("Frosting" in item):
            start += "Frosting/"
        return CMUImage(self.openImage(start + item + ".PNG").resize((80,80)))
    """Each item has a unique number associated"""
    def getIndexFromItem(self, item):
        if(item == "BlueCup"):
            return 0
        elif(item == "OrangeCup"):
            return 1
        elif(item == "BrownCake"):
            return 2
        elif(item == "WhiteCake"):
            return 3
        elif(item == "YellowFrosting"):
            return 4
        elif (item == "PinkFrosting"):
            return 5
        elif (item == "StrawberryTopping"):
            return 6
        elif (item == "CherryTopping"):
            return 7
    def plateHasItem(self):
        return len(self.ingredientNameList) > 0
    def getIsFinal(self):
        return self.isFinal
    def setIsFinal(self, boolean):
        self.isFinal = boolean
    def setIsHoldingFinal(self, boolean):
        self.isHoldingFinal = boolean
    def getIsHoldingFinal(self):
        return self.isHoldingFinal
    """Shows result from the items on Plate(Real Cupcake if it's valid, GOOP otherwise)"""
    def showResult(self):
        self.isFinal = True
        self.currRow = 7
        for i in range(1,self.board.getRow()-2):
            app.board.setBoard(i, 0, 0)
        if(len(self.currIngredientIndex) == 3):
            stg = "".join([str(i) for i in self.currIngredientIndex])
            stg += "8"
        else:
            stg = "".join([str(i) for i in self.currIngredientIndex])
        try:
            res = (self.openImage("images/Final/"+stg+".png"), False)
            self.ingredientList = [CMUImage(res[0]), CMUImage(self.openImage("images/GameScreen/inventory.PNG"))]
            self.ingredientNameList = [stg+"CUPCAKE"]
        except Exception as e:
            res = (self.openImage("images/GOOP.PNG").resize((79, 79)), True)
            self.ingredientList = [CMUImage(res[0]), CMUImage(self.openImage("images/GameScreen/inventory.PNG"))]
            self.ingredientNameList = ["GOOP"]
        return res
    """If final is thrown away, OnPlate is reset"""
    def trashFinal(self):
        self.isFinal = False
        self.currRow = 8
        self.isHoldingFinal = False
        self.ingredientList = [CMUImage(self.openImage("images/GameScreen/inventory.PNG"))]
        self.ingredientNameList = []
        self.currIngredientIndex = []