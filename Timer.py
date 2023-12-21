import math
from cmu_graphics import *
from PIL import Image
import os, pathlib

class Timer:
    def __init__(self, time):
        self.time = time
    def getTime(self):
        return self.time
    def decreaseTime(self, decrement):
        self.time -= decrement