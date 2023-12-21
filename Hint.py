class Hint:
    def __init__(self, player, onPlate, orderList):
        self.player = player
        self.onPlate = onPlate
        self.orderList = orderList
        self.hint = ""
        self.mapOfFood = {
            0: "BlueCup",
            1: "OrangeCup",
            2: "BrownCake",
            3: "WhiteCake",
            4: "YellowFrosting",
            5: "PinkFrosting",
            6: "StrawberryTopping",
            7: "CherryTopping",
        }
        self.mapOfFoodEnglish = {
            0: "Blue Cup",
            1: "Orange Cup",
            2: "Brown Cake",
            3: "White Cake",
            4: "Yellow Frosting",
            5: "Pink Frosting",
            6: "Strawberry",
            7: "Cherry",
        }
    def getHint(self):
        return self.hint
    """Simple hints"""
    def giveEasyHint(self):
        if(self.onPlate.getIsFinal()):
            return "Submit Cupcake"
        if(self.player.getItem() == None):
            return ""
        if(self.player.getItem() == "StrawberryTopping"):
            if(self.player.getStrawberryWash()):
                return "Put Strawberry On Plate"
            else:
                return "Wash Strawberry"
        if (self.player.getItem() == "CherryTopping"):
            if (self.player.getCherryWash()):
                return "Put Cherry On Plate"
            else:
                return "Wash Cherry"
        if("Batter" in self.player.getItem()):
            return "Bake Batter"
        if("Cake" in self.player.getItem()):
            return "Put Cake On Plate"
        if("Cup" in self.player.getItem()):
            return "Put Cup on Plate"
        if("Frosting" in self.player.getItem()):
            return "Put Frosting on Plate"

        return ""
    """
    Big decision Tree for what to do in every circumstance
    Values what is on the Plate
    Then values the Time
    """
    def giveComplexHint(self):
        if(self.onPlate.getIsFinal() or self.onPlate.getIsHoldingFinal()):
            if(self.orderList[1].checkRESULT(self.onPlate.getCurrIngredientIndex()) or self.orderList[0].checkRESULT(self.onPlate.getCurrIngredientIndex())):
                return "Submit Cupcake"
            else:
                return "Throw Cupcake away/GOOP away"
        #ONE ITEM
        if(len(self.orderList) == 1):
            if(len(self.onPlate.getCurrIngredientIndex()) > 0):
                for index in range(len(self.onPlate.getCurrIngredientIndex())):
                    if(index) > 3:
                        return ("Throw " + self.mapOfFoodEnglish[self.onPlate.getCurrIngredientIndex()[index]] +
                                    " on plate away")
                    if(self.onPlate.getCurrIngredientIndex()[index] != self.orderList[0].getRESULT()[index]):
                        if(self.player.getHasItem()):
                            return "Throw away current item"
                        else:
                            return ("Throw " + self.mapOfFoodEnglish[self.onPlate.getCurrIngredientIndex()[index]] +
                                    " on plate away")
                if(len(self.onPlate.getCurrIngredientIndex())  == 4):
                    if(self.player.getHasItem()):
                        return "Throw away current item"
                    return "Create Cupcake"
                elif(len(self.onPlate.getCurrIngredientIndex()) == 3 and self.orderList[0].getRESULT()[3] == 8):
                    if(self.player.getHasItem()):
                        return "Throw away current item"
                    return "Create Cupcake"
                if(self.player.getHasItem()):
                    num = self.orderList[0].getRESULT()[len(self.onPlate.getCurrIngredientIndex())]
                    if(num == self.getIndexFromItem(self.player.getItem()) or (self.player.getItem() == "WhiteBatter" and num == 3) or (self.player.getItem() == "BrownBatter" and num == 2)):
                        if(self.player.getItem() == "WhiteBatter" or self.player.getItem() == "BrownBatter"):
                            return "Place batter in oven"
                        elif(self.player.getItem() == "WhiteCake" or self.player.getItem() == "BrownCake"):
                            return "Place cake on plate"
                        elif (self.player.getItem() == "StrawberryTopping"):
                            if(self.player.getStrawberryWash()):
                                return "Place Strawberry on plate"
                            return "Wash Strawberry"
                        elif(self.player.getItem() == "CherryTopping"):
                            if (self.player.getStrawberryWash()):
                                return "Place Cherry on plate"
                            return "Wash Cherry"
                        elif(self.player.getItem() == "YellowFrosting" or self.player.getItem() == "PinkFrosting"):
                            return "Put frosting on plate"
                    else:
                        return "Throw away current item"
                else:
                    num = self.orderList[0].getRESULT()[len(self.onPlate.getCurrIngredientIndex())]
                    if((num == 2 or num == 3) and self.player.getOvenDone() and self.player.getOvenOn()):
                        return "Get batter from Oven"
                    elif((num == 2 or num == 3) and self.player.getOvenOn()):
                        return "WAIT"
                    else:
                        if(num == 2):
                            return "Pick up Brown Batter"
                        if(num == 3):
                            return "Pick up White Batter"
                        return "Pick up " + self.mapOfFoodEnglish[num]
            elif(self.player.getItem() != None):
                if(self.player.getItem() == self.mapOfFood[0] and self.orderList[0].getRESULT()[0] == self.getIndexFromItem(self.player.getItem())):
                    return "Place " + self.mapOfFoodEnglish[0] + " on Plate"
                elif(self.player.getItem() == self.mapOfFood[1] and self.orderList[0].getRESULT()[0] == self.getIndexFromItem(self.player.getItem())):
                    return "Place " + self.mapOfFoodEnglish[1] + " on Plate"
                else:
                    return "Throw away current item"
            else:
                item = self.orderList[0].getRESULT()[0]
                return "Pick Up " + self.mapOfFoodEnglish[item]
        #TWO ORDERS
        elif(len(self.orderList) == 2):
            if (len(self.onPlate.getCurrIngredientIndex()) > 0):
                #ONE ITEM ON PLATE
                if(len(self.onPlate.getCurrIngredientIndex()) == 1):
                    #HAS ITEM
                    if(self.player.getHasItem()):
                        if(self.orderList[0].getRESULT()[0] == self.onPlate.getCurrIngredientIndex()[0] and self.orderList[1].getRESULT()[0] == self.onPlate.getCurrIngredientIndex()[0]):
                            if(self.orderList[0].getTime() < self.orderList[1].getTime()):
                                num = self.orderList[0].getRESULT()[len(self.onPlate.getCurrIngredientIndex())]
                                if (num == 3 and self.player.getItem() == "WhiteBatter"):
                                    return "Bake Batter"
                                elif (num == 2 and self.player.getItem() == "BrownBatter"):
                                    return "Bake Batter"
                                elif (num == 3 and self.player.getItem() == "WhiteCake"):
                                    return "Place White Cake on Plate"
                                elif (num == 2 and self.player.getItem() == "BrownCake"):
                                    return "Place Brown Cake on Plate"
                                else:
                                    return "Throw away current item"
                            else:
                                num = self.orderList[1].getRESULT()[len(self.onPlate.getCurrIngredientIndex())]
                                if (num == 3 and self.player.getItem() == "WhiteBatter"):
                                    return "Bake Batter"
                                elif (num == 2 and self.player.getItem() == "BrownBatter"):
                                    return "Bake Batter"
                                elif (num == 3 and self.player.getItem() == "WhiteCake"):
                                    return "Place White Cake on Plate"
                                elif (num == 2 and self.player.getItem() == "BrownCake"):
                                    return "Place Brown Cake on Plate"
                                else:
                                    return "Throw away current item"
                        elif(self.orderList[0].getRESULT()[0] == self.onPlate.getCurrIngredientIndex()[0]):
                            num = self.orderList[0].getRESULT()[len(self.onPlate.getCurrIngredientIndex())]
                            if(num == 3 and self.player.getItem() == "WhiteBatter"):
                                return "Bake Batter"
                            elif(num == 2 and self.player.getItem() == "BrownBatter"):
                                return "Bake Batter"
                            elif(num == 3 and self.player.getItem() == "WhiteCake"):
                                return "Place White Cake on Plate"
                            elif(num == 2 and self.player.getItem() == "BrownCake"):
                                return "Place Brown Cake on Plate"
                            else:
                                return "Throw away current item"
                        elif (self.orderList[1].getRESULT()[0] == self.onPlate.getCurrIngredientIndex()[0]):
                            num = self.orderList[1].getRESULT()[len(self.onPlate.getCurrIngredientIndex())]
                            if (num == 3 and self.player.getItem() == "WhiteBatter"):
                                return "Bake Batter"
                            elif (num == 2 and self.player.getItem() == "BrownBatter"):
                                return "Bake Batter"
                            elif(num == 3 and self.player.getItem() == "WhiteCake"):
                                return "Place White Cake on Plate"
                            elif(num == 2 and self.player.getItem() == "BrownCake"):
                                return "Place Brown Cake on Plate"
                            else:
                                return "Throw away current item"
                        else:
                            return "Throw away current Item"
                    #Player does not have item
                    else:
                        num = self.orderList[0].getRESULT()[len(self.onPlate.getCurrIngredientIndex())]
                        if ((num == 2 or num == 3) and self.player.getOvenDone() and self.player.getOvenOn()):
                            return "Get batter from Oven"
                        elif ((num == 2 or num == 3) and self.player.getOvenOn()):
                            return "WAIT"
                        if(self.orderList[0].getRESULT()[0] == self.onPlate.getCurrIngredientIndex()[0] and self.orderList[1].getRESULT()[0] == self.onPlate.getCurrIngredientIndex()[0]):
                            if(self.orderList[0].getTime() <= self.orderList[1].getTime()):
                                if(self.mapOfFood[self.orderList[0].getRESULT()[1]] == "WhiteCake"):
                                    return "Pick up " + "White Batter"
                                else:
                                    return "Pick up " + "Brown Batter"
                            else:
                                if (self.mapOfFood[self.orderList[1].getRESULT()[1]] == "WhiteCake"):
                                    return "Pick up " + "White Batter"
                                else:
                                    return "Pick up " + "Brown Batter"
                        elif(self.orderList[0].getRESULT()[0] == self.onPlate.getCurrIngredientIndex()[0]):
                            if (self.mapOfFood[self.orderList[0].getRESULT()[1]] == "WhiteCake"):
                                return "Pick up " + "White Batter"
                            else:
                                return "Pick up " + "Brown Batter"
                        elif(self.orderList[1].getRESULT()[0] == self.onPlate.getCurrIngredientIndex()[0]):
                            if (self.mapOfFood[self.orderList[1].getRESULT()[1]] == "WhiteCake"):
                                return "Pick up " + "White Batter"
                            else:
                                return "Pick up " + "Brown Batter"
                        else:
                            return ("Throw " + self.mapOfFoodEnglish[self.onPlate.getCurrIngredientIndex()[0]] +
                             " on plate away")
                #TWO ITEMS ON PLATE
                elif (len(self.onPlate.getCurrIngredientIndex()) == 2):
                    if(self.player.getHasItem()):
                        if (self.orderList[0].getRESULT()[0] == self.onPlate.getCurrIngredientIndex()[0] and
                                self.orderList[1].getRESULT()[0] == self.onPlate.getCurrIngredientIndex()[0] and
                                self.orderList[0].getRESULT()[1] == self.onPlate.getCurrIngredientIndex()[1] and
                                self.orderList[1].getRESULT()[1] == self.onPlate.getCurrIngredientIndex()[1]):
                            if (self.orderList[0].getTime() <= self.orderList[1].getTime()):
                                num = self.orderList[0].getRESULT()[len(self.onPlate.getCurrIngredientIndex())]
                                if(num == 4 and self.player.getItem() == "YellowFrosting"):
                                    return "Place Yellow Frosting on Plate"
                                elif(num == 5 and self.player.getItem() == "PinkFrosting"):
                                    return "Place Pink Frosting on Plate"
                                else:
                                    return "Throw current item away"
                            else:
                                num = self.orderList[1].getRESULT()[len(self.onPlate.getCurrIngredientIndex())]
                                if (num == 4 and self.player.getItem() == "YellowFrosting"):
                                    return "Place Yellow Frosting on Plate"
                                elif (num == 5 and self.player.getItem() == "PinkFrosting"):
                                    return "Place Pink Frosting on Plate"
                                else:
                                    return "Throw current item away"
                        elif (self.orderList[0].getRESULT()[0] == self.onPlate.getCurrIngredientIndex()[0]
                        and self.orderList[0].getRESULT()[1] == self.onPlate.getCurrIngredientIndex()[1] ):
                            num = self.orderList[0].getRESULT()[len(self.onPlate.getCurrIngredientIndex())]
                            if (num == 4 and self.player.getItem() == "YellowFrosting"):
                                return "Place Yellow Frosting on Plate"
                            elif (num == 5 and self.player.getItem() == "PinkFrosting"):
                                return "Place Pink Frosting on Plate"
                            else:
                                return "Throw current item away"
                        elif (self.orderList[1].getRESULT()[0] == self.onPlate.getCurrIngredientIndex()[0]
                        and self.orderList[1].getRESULT()[1] == self.onPlate.getCurrIngredientIndex()[1]):
                            num = self.orderList[1].getRESULT()[len(self.onPlate.getCurrIngredientIndex())]
                            if (num == 4 and self.player.getItem() == "YellowFrosting"):
                                return "Place Yellow Frosting on Plate"
                            elif (num == 5 and self.player.getItem() == "PinkFrosting"):
                                return "Place Pink Frosting on Plate"
                            else:
                                return "Throw current item away"
                        else:
                            return ("Throw " + self.mapOfFoodEnglish[self.onPlate.getCurrIngredientIndex()[1]] +
                                    " on plate away")
                    else:
                        if (self.orderList[0].getRESULT()[0] == self.onPlate.getCurrIngredientIndex()[0] and
                                self.orderList[1].getRESULT()[0] == self.onPlate.getCurrIngredientIndex()[0] and
                                self.orderList[0].getRESULT()[1] == self.onPlate.getCurrIngredientIndex()[1] and
                                self.orderList[1].getRESULT()[1] == self.onPlate.getCurrIngredientIndex()[1]):
                            if (self.orderList[0].getTime() <= self.orderList[1].getTime()):
                                return "Pick up " +  self.mapOfFoodEnglish[self.orderList[0].getRESULT()[2]]
                            else:
                                return "Pick up " +  self.mapOfFoodEnglish[self.orderList[1].getRESULT()[2]]
                        elif (self.orderList[0].getRESULT()[0] == self.onPlate.getCurrIngredientIndex()[0]
                        and self.orderList[0].getRESULT()[1] == self.onPlate.getCurrIngredientIndex()[1] ):
                            return "Pick up " +  self.mapOfFoodEnglish[self.orderList[0].getRESULT()[2]]
                        elif (self.orderList[1].getRESULT()[0] == self.onPlate.getCurrIngredientIndex()[0]
                        and self.orderList[1].getRESULT()[1] == self.onPlate.getCurrIngredientIndex()[1]):
                            return "Pick up " +  self.mapOfFoodEnglish[self.orderList[1].getRESULT()[2]]
                        else:
                            return ("Throw " + self.mapOfFoodEnglish[self.onPlate.getCurrIngredientIndex()[1]] +
                                    " on plate away")
                #THREE ITEMS ON PLATE
                elif (len(self.onPlate.getCurrIngredientIndex()) == 3):
                    if (self.player.getHasItem()):
                        if (self.orderList[0].getRESULT()[0] == self.onPlate.getCurrIngredientIndex()[0] and
                                self.orderList[1].getRESULT()[0] == self.onPlate.getCurrIngredientIndex()[0] and
                                self.orderList[0].getRESULT()[1] == self.onPlate.getCurrIngredientIndex()[1] and
                                self.orderList[1].getRESULT()[1] == self.onPlate.getCurrIngredientIndex()[1] and
                                self.orderList[0].getRESULT()[2] == self.onPlate.getCurrIngredientIndex()[2] and
                                self.orderList[1].getRESULT()[2] == self.onPlate.getCurrIngredientIndex()[2]):
                            if (self.orderList[0].getTime() <= self.orderList[1].getTime()):
                                num = self.orderList[0].getRESULT()[len(self.onPlate.getCurrIngredientIndex())]
                                if(self.orderList[0].getRESULT()[3] == 8):
                                    return "Throw current item away"
                                else:
                                    if (num == 6 and self.player.getItem() == "StrawberryTopping"):
                                        if (self.player.getStrawberryWash()):
                                            return "Place Strawberry on Plate"
                                        else:
                                            return "Wash Strawberry"
                                    elif (num == 7 and self.player.getItem() == "CherryTopping"):
                                        if(self.player.getCherryWash()):
                                            return "Place Cherry on Plate"
                                        else:
                                            return "Wash Cherry"
                                    else:
                                        return "Throw current item away"
                            else:
                                if (self.orderList[1].getRESULT()[3] == 8):
                                    return "Throw current item away"
                                else:
                                    num = self.orderList[1].getRESULT()[len(self.onPlate.getCurrIngredientIndex())]
                                    if (num == 6 and self.player.getItem() == "StrawberryTopping"):
                                        if (self.player.getStrawberryWash()):
                                            return "Place Strawberry on Plate"
                                        else:
                                            return "Wash Strawberry"
                                    elif (num == 7 and self.player.getItem() == "CherryTopping"):
                                        if (self.player.getCherryWash()):
                                            return "Place Cherry on Plate"
                                        else:
                                            return "Wash Cherry"
                                    else:
                                        "Throw current item away"
                        elif (self.orderList[0].getRESULT()[0] == self.onPlate.getCurrIngredientIndex()[0]
                              and self.orderList[0].getRESULT()[1] == self.onPlate.getCurrIngredientIndex()[1]
                              and self.orderList[0].getRESULT()[2] == self.onPlate.getCurrIngredientIndex()[2]):
                            num = self.orderList[0].getRESULT()[len(self.onPlate.getCurrIngredientIndex())]
                            if (self.orderList[0].getRESULT()[3] == 8):
                                return "Throw current item away"
                            else:
                                if (num == 6 and self.player.getItem() == "StrawberryTopping"):
                                    if (self.player.getStrawberryWash()):
                                        return "Place Strawberry on Plate"
                                    else:
                                        return "Wash Strawberry"
                                elif (num == 7 and self.player.getItem() == "CherryTopping"):
                                    if (self.player.getCherryWash()):
                                        return "Place Cherry on Plate"
                                    else:
                                        return "Wash Cherry"
                                else:
                                    return "Throw current item away"
                        elif (self.orderList[1].getRESULT()[0] == self.onPlate.getCurrIngredientIndex()[0]
                              and self.orderList[1].getRESULT()[1] == self.onPlate.getCurrIngredientIndex()[1]
                              and self.orderList[1].getRESULT()[2] == self.onPlate.getCurrIngredientIndex()[2]):
                            if (self.orderList[1].getRESULT()[3] == 8):
                                return "Throw current item away"
                            else:
                                num = self.orderList[1].getRESULT()[len(self.onPlate.getCurrIngredientIndex())]
                                if (num == 6 and self.player.getItem() == "StrawberryTopping"):
                                    if (self.player.getStrawberryWash()):
                                        return "Place Strawberry on Plate"
                                    else:
                                        return "Wash Strawberry"
                                elif (num == 7 and self.player.getItem() == "CherryTopping"):
                                    if (self.player.getCherryWash()):
                                        return "Place Cherry on Plate"
                                    else:
                                        return "Wash Cherry"
                                else:
                                    return "Throw current item away"
                        else:
                            return ("Throw " + self.mapOfFoodEnglish[self.onPlate.getCurrIngredientIndex()[2]] + " on plate away")
                    else:
                        if (self.orderList[0].getRESULT()[0] == self.onPlate.getCurrIngredientIndex()[0] and
                                self.orderList[1].getRESULT()[0] == self.onPlate.getCurrIngredientIndex()[0] and
                                self.orderList[0].getRESULT()[1] == self.onPlate.getCurrIngredientIndex()[1] and
                                self.orderList[1].getRESULT()[1] == self.onPlate.getCurrIngredientIndex()[1] and
                                self.orderList[0].getRESULT()[2] == self.onPlate.getCurrIngredientIndex()[2] and
                                self.orderList[1].getRESULT()[2] == self.onPlate.getCurrIngredientIndex()[2]):
                            if (self.orderList[0].getTime() <= self.orderList[1].getTime()):
                                if (self.orderList[0].getRESULT()[3] == 8):
                                    return "Submit order"
                                else:
                                    return "Pick up " + self.mapOfFoodEnglish[self.orderList[0].getRESULT()[3]]
                            else:
                                if (self.orderList[1].getRESULT()[3] == 8):
                                    return "Submit order"
                                else:
                                    return "Pick up " + self.mapOfFoodEnglish[self.orderList[1].getRESULT()[3]]
                        elif (self.orderList[0].getRESULT()[0] == self.onPlate.getCurrIngredientIndex()[0]
                              and self.orderList[0].getRESULT()[1] == self.onPlate.getCurrIngredientIndex()[1]
                              and self.orderList[0].getRESULT()[2] == self.onPlate.getCurrIngredientIndex()[2]):
                            if (self.orderList[0].getRESULT()[3] == 8):
                                return "Submit order"
                            else:
                                return "Pick up " + self.mapOfFoodEnglish[self.orderList[0].getRESULT()[3]]
                        elif (self.orderList[1].getRESULT()[0] == self.onPlate.getCurrIngredientIndex()[0]
                              and self.orderList[1].getRESULT()[1] == self.onPlate.getCurrIngredientIndex()[1]
                              and self.orderList[1].getRESULT()[2] == self.onPlate.getCurrIngredientIndex()[2]):
                            if (self.orderList[1].getRESULT()[3] == 8):
                                return "Submit order"
                            else:
                                return "Pick up " + self.mapOfFoodEnglish[self.orderList[1].getRESULT()[3]]
                        else:
                            return ("Throw " + self.mapOfFoodEnglish[self.onPlate.getCurrIngredientIndex()[2]] +
                                    " on plate away")
                elif (len(self.onPlate.getCurrIngredientIndex()) == 4):
                    if (self.player.getHasItem()):
                        return "Throw away current item"
                    elif (self.orderList[0].getRESULT()[0] == self.onPlate.getCurrIngredientIndex()[0]
                            and self.orderList[0].getRESULT()[1] == self.onPlate.getCurrIngredientIndex()[1]
                            and self.orderList[0].getRESULT()[2] == self.onPlate.getCurrIngredientIndex()[2]
                            and self.orderList[0].getRESULT()[3] == self.onPlate.getCurrIngredientIndex()[3]):
                        return "Create Cupcake"
                    elif (self.orderList[1].getRESULT()[0] == self.onPlate.getCurrIngredientIndex()[0]
                            and self.orderList[1].getRESULT()[1] == self.onPlate.getCurrIngredientIndex()[1]
                            and self.orderList[1].getRESULT()[2] == self.onPlate.getCurrIngredientIndex()[2]
                            and self.orderList[1].getRESULT()[3] == self.onPlate.getCurrIngredientIndex()[3]):
                        return "Create Cupcake"
                    else:
                        return ("Throw " + self.mapOfFoodEnglish[self.onPlate.getCurrIngredientIndex()[2]] +" on plate away")
                #MORE THAN 4 ITEMS ON PLATE
                else:
                    return ("Throw " + self.mapOfFoodEnglish[self.onPlate.getCurrIngredientIndex()[len(self.onPlate.getCurrIngredientIndex())-1]] +
                            " on plate away")
            elif(self.orderList[0].getTime() <= self.orderList[1].getTime()):
                if (self.player.getHasItem()):
                    if (self.player.getItem() == self.mapOfFood[0] and self.orderList[0].getRESULT()[0] == self.getIndexFromItem(self.player.getItem())):
                        return "Place " + self.mapOfFoodEnglish[0] + " on Plate"
                    elif (self.player.getItem() == self.mapOfFood[1] and self.orderList[0].getRESULT()[0] == self.getIndexFromItem(self.player.getItem())):
                        return "Place " + self.mapOfFoodEnglish[1] + " on Plate"
                    else:
                        return "Throw away current item"
                else:
                    item = self.orderList[0].getRESULT()[0]
                    return "Pick Up " + self.mapOfFoodEnglish[item]
            else:
                if (self.player.getHasItem()):
                    if (self.player.getItem() == self.mapOfFood[0] and self.orderList[1].getRESULT()[0] == self.getIndexFromItem(self.player.getItem())):
                        return "Place " + self.mapOfFoodEnglish[0] + " on Plate"
                    elif (self.player.getItem() == self.mapOfFood[1] and self.orderList[1].getRESULT()[0] == self.getIndexFromItem(self.player.getItem())):
                        return "Place " + self.mapOfFoodEnglish[1] + " on Plate"
                    else:
                        return "Throw away current item"
                else:
                    item = self.orderList[1].getRESULT()[0]
                    return "Pick Up " + self.mapOfFoodEnglish[item]
        return ""

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