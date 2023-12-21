from cmu_graphics import *
from PIL import Image
import os, pathlib

class Score:
    def __init__(self, app, order, userOrder, isGoop):
        self.order = order
        self.userOrder = userOrder
        self.isGoop = isGoop
        self.score = self.setScore()

    """
    Real Cupcake
    1. Time
        +1.5 - finished above half way between start and 0
        +1 - finished before 0
        +.5 - finished before half way between 0 and customer leaving
        +0 - finished after half way between 0 and customer leaving
    2. Topping
        +.5 if correctly adds or omits topping
        -.5 if incorrectly adds or omits topping
    3. Components
        +1 if adds correct component
        -1 if adds incorrect component
    GOOP
    - Automatic 0
    """
    def setScore(self):
        tempScore = 0
        if(self.isGoop):
            return tempScore
        timeStarted = self.order.getInitialTime()
        timeFinished = self.order.getTime()
        customerLeaveTime = self.order.getEndTime()
        halfTime = timeStarted / 2
        halfTimeToEnd = customerLeaveTime / 2
        if timeFinished >= halfTime:
            tempScore += 1.5
        elif timeFinished >= 0:
            tempScore += 1
        elif timeFinished >= halfTimeToEnd:
            tempScore += 0.5
        else:
            tempScore += 0
        for i in range(3):
            if(self.order.getRESULT()[i] == self.userOrder[i]):
                tempScore += 1
            else:
                tempScore -= 1
        if(self.order.getRESULT()[3] == 8):
            if(len(self.userOrder) == 3):
                tempScore += .5
            else:
                tempScore -= .5
        else:
            if(self.order.getRESULT()[3] == self.userOrder[3]):
                tempScore += .5
            else:
                tempScore -= .5
        if(tempScore<0):
            return 0
        return tempScore
    def getScore(self):
        return self.score
