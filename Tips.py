from cmu_graphics import *
from PIL import Image
import os, pathlib
import random

class Tips:
    def __init__(self, stars, cupcakeCost):
        self.cupcakeCost = cupcakeCost
        self.stars = stars
        self.tips = self.setTip()

    def getTips(self):
        return self.tips
    """
    Above 4 stars
    - 20% for 20% Tip
    - 50% for 15% Tip
    - 29% for 10% Tip
    - 1% for a tip between 50% - 100% Tip
    Above 2.5 stars but less than 4 stars
    - 50% for 15% Tip
    - 50% for 10% Tip
    Above 1 stars but less than 2.5 stars
    - 10% for 10% Tip
    - 90% for 0% Tip
    Below 1 star
    - 0% Tip
    """
    def setTip(self):
        rand_chance = random.randint(1, 100)
        if self.stars >= 4:
            if rand_chance <= 20:
                return pythonRound(self.cupcakeCost * 0.20,2)
            elif rand_chance <= 50:
                return pythonRound(self.cupcakeCost * 0.15,2)
            elif rand_chance == 67:
                randomTip = pythonRound(random.uniform(0.5, 1), 2)
                return pythonRound(self.cupcakeCost * randomTip,2)
            else:
                return pythonRound(self.cupcakeCost * 0.10,2)
        elif self.stars >= 2.5:
            if(rand_chance<= 50):
                return pythonRound(self.cupcakeCost * 0.15,2)
            else:
                return pythonRound(self.cupcakeCost * 0.1,2)
        elif self.stars >= 1:
            if(rand_chance <= 15):
                return pythonRound(self.cupcakeCost * 0.1,2)
        return 0

