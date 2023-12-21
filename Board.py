import random


class Board:
    # Station height
    # Station width
    """VERY RARE CHANCE WHERE IMPORTANT COUNTER IS TRAPPED"""
    def __init__(self, app, height, width):
        self.height = height
        self.width = width
        self.worstCaseBoard = [[4,0,0,6,6,6,6,0,2,2],
                              [3,0,0,0,0,0,0,0,2,2],
                              [3,0,0,0,0,0,0,0,2,2],
                              [3,0,0,0,0,0,0,0,2,2],
                              [3,0,0,0,0,0,0,0,2,2],
                              [3,0,0,0,0,0,0,0,5,5],
                              [3,0,0,0,0,0,0,0,0,0],
                              [3,0,0,0,0,0,0,0,0,0],
                              [3,0,0,0,0,0,0,0,0,0],
                              [3,0,0,6,6,6,6,0,0,0]]
        self.numOfCounterTops = 0
        self.board = self.randomizeBoard()
        self.cols = 10
        self.rows = 10
        self.cellWidth = self.width//self.cols
        self.cellHeight = self.height // self.rows
        self.counterCoordinates = []

        self.mapOfFood = {}
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if(self.board[row][col] == 1):
                    self.counterCoordinates.append([row,col])
    """Randomly Generate a 10 x 10 board with the outer layer of each row and each column
    set to a specific number. Random number of counters places randomly in allowed space. 
    0 = floor
    1 = counter
    2 = order
    3 = item on plate
    4 = inventory
    5 = timer
    6 = Text
    """
    def randomizeBoard(self):
        numOnes = random.randint(14, 20)
        self.numOfCounterTops = numOnes
        tempBoard = []
        for row in range(10):
            temp = []
            for col in range(10):
                temp.append(0)
            tempBoard.append(temp)
        tempBoard[0][0] = 4
        tempBoard[9][0] = 3
        onesPlaced = 0
        while onesPlaced < numOnes:
            row = random.randint(0, 9)
            col = random.randint(0, 9)
            if self.worstCaseBoard[row][col] == 0:
                self.worstCaseBoard[row][col] = 1
                tempBoard[row][col] = 1
                onesPlaced += 1
        return tempBoard
    def getNumCounterTops(self):
        return self.numOfCounterTops
    def getBoard(self):
        return self.board
    def setBoard(self, row, col, newItem):
        self.board[row][col] = newItem
    def getCounterCoordinates(self):
        return self.counterCoordinates
    def getRowAndCol(self, xPixel, yPixel):
        return (xPixel//self.cellWidth, yPixel//self.cellHeight)
    def setMapOfFood(self, row, col, name):
        self.mapOfFood[(row,col)] = name
    def isCounter(self, row, col):
        if([row, col] in self.counterCoordinates):
            return True
        return False
    def getMapOfFoodItem(self, row, col):
        if((row,col) in self.mapOfFood):
            return self.mapOfFood[row,col]
        return None
    def getRow(self):
        return self.rows
    def getCol(self):
        return self.cols
    """Sets order to closest empty col from left"""
    def setOrder(self, numberOfItems):
        for i in range(9, 1, -1):
            if(self.board[0][i] == 0):
                j = 0
                while(j<numberOfItems+1):
                    self.board[j][i] = 2
                    j+=1
                self.board[j][i] = 5
                return i


