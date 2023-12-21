import random as rand
from PIL import Image as img
import os, pathlib
from cmu_graphics import *
import Timer

class Sink:
    def __init__(self, DAY):
        self.location = None
        self.DAY = DAY
        self.timer = Timer.Timer(4-self.DAY.getSinkAndOvenIncrement())

    def reset(self):
        self.timer = Timer.Timer(4 - self.DAY.getSinkAndOvenIncrement())
    def decreaseTimerByOne(self):
        return self.timer.decreaseTime(1)
    def getTime(self):
        return self.timer.getTime()