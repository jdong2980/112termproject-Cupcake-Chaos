from cmu_graphics import *
from PIL import Image
import os, pathlib
import Timer
class Day:
    def __init__(self,increment):
        self.day = 1
        self.totalStars = 0
        self.numberOfOrders = 0
        self.totalTips = 0
        self.dayTime = 60
        self.TOTALMONEY = 10
        """FOR STORE"""
        self.playerSpeedIncrementValue = 0
        self.playerSpeedPrice = 5
        self.dayTimeIncrementValue = 0
        self.dayTimePrice = 5
        self.hintLevelIncrementValue = 2
        self.hintLevelPrice = 5
        self.cupcakePriceIncrementValue = 0
        self.cupcakePricePrice = 5
        self.waitTimeIncrementValue = 0
        self.waitTimePrice = 5
        self.sinkAndOvenIncrementValue = 0
        self.sinkAndOvenPrice = 5
        self.timer = Timer.Timer(self.dayTime + (60*increment))
    def getPlayerSpeedIncrement(self):
        return self.playerSpeedIncrementValue
    def getDayTimeIncrement(self):
        return self.dayTimeIncrementValue
    def getHintLevelIncrement(self):
        return self.hintLevelIncrementValue
    def getCupcakePriceIncrement(self):
        return self.cupcakePriceIncrementValue
    def getWaitTimeIncrement(self):
        return self.waitTimeIncrementValue
    def getSinkAndOvenIncrement(self):
        return self.sinkAndOvenIncrementValue
    def getPlayerSpeedPrice(self):
        return self.playerSpeedPrice
    def getDayTimePrice(self):
        return self.dayTimePrice
    def getHintLevelPrice(self):
        return self.hintLevelPrice
    def getCupcakePricePrice(self):
        return self.cupcakePricePrice
    def getWaitTimePrice(self):
        return self.waitTimePrice
    def getSinkAndOvenPrice(self):
        return self.sinkAndOvenPrice

    def playerSpeedIncrement(self):
        self.playerSpeedIncrementValue += 1
        self.playerSpeedPrice *= 1.5
    def dayTimeIncrement(self):
        self.dayTimeIncrementValue += 1
        self.dayTimePrice *= 1.5
    def hintLevelIncrement(self):
        self.hintLevelIncrementValue += 1
        self.hintLevelPrice *= 1.5
    def cupcakePriceIncrement(self):
        self.cupcakePriceIncrementValue += 1
        self.cupcakePricePrice *= 1.5
    def waitTimeIncrement(self):
        self.waitTimeIncrementValue += 1
        self.waitTimePrice *= 1.5
    def sinkAndOvenIncrement(self):
        self.sinkAndOvenIncrementValue += 1
        self.sinkAndOvenPrice *= 1.5
    def getDay(self):
        return self.day
    def getTOTALMONEY(self):
        return pythonRound(self.TOTALMONEY,2)
    def getTotalStars(self):
        return self.totalStars
    def getNumberOfOrders(self):
        return self.numberOfOrders
    def getTotalTips(self):
        return self.totalTips
    def addMoney(self, money):
        self.TOTALMONEY += money
    """Called after every order leaves orderlist"""
    def orderIteration(self, stars, tips):
        self.totalStars += stars
        self.numberOfOrders += 1
        self.totalTips += tips
    def decreaseTime(self):
        self.timer.decreaseTime(1)
    def resetTime(self, seconds):
        self.timer = Timer.Timer(seconds)
    def getTime(self):
        return self.timer.getTime()
    def dayOver(self):
        self.day += 1
    def getDayTime(self):
        return self.dayTime
