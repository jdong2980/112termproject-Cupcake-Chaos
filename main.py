from cmu_graphics import *
from PIL import Image
import os, pathlib
import Board
import random
import math
import time
import Order
import Player
import OnPlate
import Inventory
import Score
import Setup
import Oven
import Sink
import Score
import Tips
import Hint
import Day

"""This global variable is used to track information across all days"""
DAY = Day.Day(0)
"""Code from CMU ImageDemo.py"""
def openImage(fileName):
    return Image.open(os.path.join(pathlib.Path(__file__).parent, fileName))
"""Code from CMU SoundDemo.py"""
def loadSound(relativePath):
    absolutePath = os.path.abspath(relativePath)
    url = pathlib.Path(absolutePath).as_uri()
    return Sound(url)
"""Each day onAppStart is reset"""
def onAppStart(app):
    """GameScreen"""
    app.boardWidth = 800
    app.boardHeight = 800
    app.board = Board.Board(app, app.boardHeight, app.boardWidth)
    app.cols = app.board.getCol()
    app.rows = app.board.getRow()
    app.boardLeft = 0
    app.boardTop = 0
    app.oven = Oven.Oven(DAY)
    app.cellBorderWidth = 2
    app.setup = Setup.Setup(app.board)
    app.allOrders = app.setup.getAllItems()
    app.orderList = [Order.Order(app, app.board, DAY), Order.Order(app, app.board, DAY)]
    app.cellWidth, app.cellHeight = getCellSize(app)
    app.onPlate = OnPlate.OnPlate(app.board)
    app.sink = Sink.Sink(DAY)
    app.player = Player.Player(app, app.board, app.onPlate, app.setup, app.oven, app.sink, DAY)
    app.finalCupcake = None
    app.inventory = Inventory.Inventory(app, app.player)
    app.counter = 0
    app.ovenLocation = (0, 0)
    app.isGoop = False
    app.tip = 0
    app.hint = Hint.Hint(app.player, app.onPlate, app.orderList)
    app.score = 0
    app.day = Day.Day(DAY.getDayTimeIncrement())
    app.dayOver = False
    app.sound1 = loadSound("Music/videoplayback.mp3")
    app.sound1.play(restart=True, loop = True)
    """StartScreen"""
    app.titleText = openImage("images/HomeScreen/title.PNG")
    app.playButton = openImage("images/HomeScreen/play.png")
    app.imageWidth,app.imageHeight = app.playButton.width, app.playButton.height
    app.cupcakeStrip = openImage("images/HomeScreen/cupcakeStrip.png")
    app.tipsButton = openImage("images/HomeScreen/tips.png")
    app.instructionsButton = openImage("images/HomeScreen/instructions.png")
    app.sprinkleBackground = openImage("images/HomeScreen/sprinkleBackground.png")
    app.playText = openImage("images/HomeScreen/playText.png")
    app.tipsText = openImage("images/HomeScreen/tipsText.png")
    app.instructionsText = openImage("images/HomeScreen/instructionsText.png")
    app.cx = 20
    app.cy = 620
    app.dx = 50
    """InstructionScreen"""
    app.instructionsMessage = '''
    Try to complete as many cupcake orders as possible while managing multiple orders a once!
    \nBuild the cupcakes according to the “order” displayed in the top right of the screen.
    \nThis is line 2.'''
    app.instructionsSprinkleBackground = openImage('images/InstructionScreen/sprinkleBackground.png')
    app.instructionsManualImage = openImage('images/InstructionScreen/instructionsmanual.png')
    app.instructionsParagraph = openImage('images/InstructionScreen/instructionsParagraph.jpeg')
    app.instructionsPlay = openImage('images/InstructionScreen/play.png')
    app.instructionImagewidth, app.instructionImageHeight = app.instructionsPlay.width, app.instructionsPlay.height
    app.instructionsBack = openImage('images/InstructionScreen/back.png')
    """SubmitScreen"""
    app.submitMessage = 'Your Cupcake'
    app.submitSprinkleBackground = openImage('images/SubmitScreen/sprinklebackground.png')
    app.submitBack = openImage('images/SubmitScreen/back.png')
    app.submitImageWidth, app.submitImageHeight = app.submitBack.width, app.submitBack.height
    """EndScreen"""
    app.endScreenSprinkleBackground = openImage('images/EndScreen/sprinkleBackground.png')
    app.endScreenPlayAgain = openImage('images/EndScreen/playAgain.png')
    app.endScreenGameOver = openImage('images/EndScreen/gameOver.png')
    app.endScreenImageWidth, app.endScreenImageHeight = app.endScreenPlayAgain.width, app.endScreenPlayAgain.height
    app.endScreenMessage = 'Sorry, you are in debt :('
    """PauseScreen"""
    app.gamePaused = openImage('images/PauseScreen/gamePaused.png')
    app.pauseScreenHome = openImage('images/PauseScreen/home.png')
    app.pauseScreenSprinkleBackground = openImage("images/PauseScreen/sprinkleBackground.png")
    """DayOverScreen"""
    app.dayOverDayOver = openImage('images/DayOverScreen/dayOver.png')
    app.dayOverHome = openImage('images/DayOverScreen/home.png')
    app.dayOverSprinkleBackground = openImage("images/DayOverScreen/sprinkleBackground.png")
    app.dayOverNextDayButton = openImage('images/DayOverScreen/nextDay2.png')
    app.dayOverStoreButton = openImage('images/DayOverScreen/store.png')
    """StoreScreen"""
    app.storeLabel = openImage('images/storeScreen/storeLabel.png')
    app.storeSprinkleBackground = openImage("images/storeScreen/sprinkleBackground.png")
    app.storeFasterSprite = openImage('images/storeScreen/fasterSprite.png')
    app.storeBetterHint = openImage('images/storeScreen/betterHint.png')
    app.storeMoreTime = openImage('images/storeScreen/moreTime.png')
    app.storeOvenAndSink = openImage('images/storeScreen/ovenAndSink.png')
    app.storeExpensiveCupcakes = openImage('images/storeScreen/expensiveCupcakes.png')
    app.storeCustomerLongerWait = openImage('images/storeScreen/customerLongerWait.png')
    app.storeBack = openImage('images/InstructionScreen/back.png')
    """WinScreen"""
    app.winSprinkleBackground = openImage('images/winScreen/sprinklebackground.png')
    app.winPlayAgain = openImage('images/winScreen/playAgain.png')
    app.win = openImage('images/winScreen/win.png')
    app.winImageWidth, app.winImageHeight = app.winPlayAgain.width, app.winPlayAgain.height
    app.winMessage = 'Congrats! You made it to 5 days with a total of $'
    """TipsScreen"""
    app.tipSprinkleBackground = openImage('images/tipScreen/sprinklebackground.png')
    app.tipBack = openImage('images/tipScreen/back.png')
    app.yourTips = openImage('images/tipScreen/yourTips.png')
    app.tipsImageWidth,app.tipsImageHeight = app.tipBack.width,app.tipBack.height


"""
If Money < 0 -> endScreen
If Customer Leaves -> new order comes in
If day 5 is done -> winScreen
Oven and Sink conditional is set
"""
def gameScreen_onStep(app):
    if(DAY.getTOTALMONEY() < 0):
        onAppStart(app)
        setActiveScreen("endScreen")
    if(len(app.orderList) == 0):
        DAY.dayOver()
        if(DAY.getDay() == 6):
            setActiveScreen("winScreen")
        else:
            setActiveScreen("dayOverScreen")
    if(app.counter % 20 == 0):
        for order in range(len(app.orderList) - 1, -1, -1):
            app.orderList[order].decreaseTimerByOne()
            if(app.orderList[order].leave()):
                if(order == 1 and not app.dayOver):
                    customerLeave(app, order)
                elif(order == 0 and not app.dayOver):
                    customerLeave(app, order)
                else:
                    DAY.addMoney(-5)
                    app.orderList.pop(order)
                    if(len(app.orderList) > 0):
                        app.orderList[0].resetOrder()
        if(app.player.getOvenOn()):
            app.oven.decreaseTimerByOne()
        if(app.oven.getTime() == 0):
            app.player.setOvenDone(True)
        if(app.player.getSinkOn()):
            app.sink.decreaseTimerByOne()
        if (app.sink.getTime() == 0):
            app.player.setSinkOn(False)
            app.sink.reset()
            if(app.player.getItem() == "StrawberryTopping"):
                app.player.setStrawberryWash(True)
            elif (app.player.getItem() == "CherryTopping"):
                app.player.setCherryWash(True)
        if(not app.dayOver):
            app.day.decreaseTime()
        if(app.day.getTime() == 0):
            app.dayOver = True
    app.counter+=1
def customerLeave(app, order):
    app.orderList.pop(order)
    app.orderList[0].resetOrder()
    app.orderList.append(Order.Order(app, app.board,DAY))
    DAY.addMoney(-5)
    DAY.orderIteration(0,0)
    app.day.orderIteration(0,0)
def gameScreen_redrawAll(app):
    drawBoard(app)
    drawBoardBorder(app)
    drawOrderBoarder(app)
    drawOnPlateBorder(app)
    app.inventory.setItem(app.player.getItem())
    drawHint(app)
    drawOvenText(app)
    drawSinkText(app)
    drawSpirite(app)
def drawOvenText(app):
    if(app.player.getOvenOn()):
        drawLabel("OVEN:" + str(app.oven.getTime()), 475,775, size = 40)
def drawSinkText(app):
    if (app.player.getSinkOn()):
        drawLabel("SINK:" + str(app.sink.getTime()), 325, 775, size = 40)
def drawHint(app):
    if(DAY.getHintLevelIncrement() == 1):
        drawLabel(app.hint.giveEasyHint(), 400, 25, size=30)
    elif(DAY.getHintLevelIncrement() == 2):
        drawLabel(app.hint.giveComplexHint(), 400, 25, size = 30)
def drawSpirite(app):
    if(app.player.getDirection() == "down"):
        drawImage(app.player.getSprites()[0], app.player.getXPosition(), app.player.getYPosition())
    elif(app.player.getDirection() == "right"):
        drawImage(app.player.getSprites()[1], app.player.getXPosition(), app.player.getYPosition())
    elif (app.player.getDirection() == "up"):
        drawImage(app.player.getSprites()[2], app.player.getXPosition(), app.player.getYPosition())
    elif (app.player.getDirection() == "left"):
        drawImage(app.player.getSprites()[3], app.player.getXPosition(), app.player.getYPosition())

"""See Board Class for more information"""
def drawBoard(app):
    orderCount = 0
    itemCount = 0
    invCount = 0
    if(len(app.orderList) <= 1):
        orderNum = 0
    else:
        orderNum = 1
    orderListCopy = app.orderList.copy()
    first = True
    if(len(orderListCopy) > 0):
        for col in range(len(app.board.getBoard()[0])):
            for row in range(len(app.board.getBoard())):
                cellLeft, cellTop = getCellLeftTop(app, row, col)
                if(app.board.getBoard()[row][col] == 1):
                    drawStation(app, row, col, app.setup.getItemList()[itemCount])
                    itemCount +=1
                elif(app.board.getBoard()[row][col] == 0):
                    drawImage(CMUImage(openImage("images/GameScreen/floor.PNG")), cellLeft, cellTop)
                elif(app.board.getBoard()[row][col] == 2):
                    if(orderCount == 0):
                        drawImage(CMUImage(openImage("images/GameScreen/order.PNG")), cellLeft, cellTop)
                    elif(orderListCopy[orderNum].getWithTopping()):
                        drawOrder(app, orderListCopy[orderNum].getFinal()[-orderCount], row, col)
                    elif(orderCount != len(orderListCopy[orderNum].getFinal())):
                        drawOrder(app, orderListCopy[orderNum].getFinal()[-orderCount-1], row, col)
                    orderCount += 1
                elif(app.board.getBoard()[row][col] == 3):
                    drawImage(app.onPlate.getIngredientList()[invCount], cellLeft, cellTop)
                    invCount +=1
                elif(app.board.getBoard()[row][col] == 4):
                    drawImage(app.inventory.showInventory(), cellLeft, cellTop)
                elif(app.board.getBoard()[row][col] == 5):
                    drawImage(CMUImage(openImage("images/GameScreen/floor.PNG")), cellLeft, cellTop)
                    drawLabel(orderListCopy[orderNum].getTime(), col * app.cellWidth + 40, row * app.cellHeight + 40, size=40)
            if(orderCount > 0 and len(orderListCopy) == 2):
                orderNum -= 1
                orderCount = 0

def getSquareColor(row, col):
    if (row + col) % 2 == 0:
        return "black"
    else:
        return "white"

def drawOrder(app, image, row,col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    drawImage(image, cellLeft, cellTop)
"""From 15112 Tetris Code"""
def drawBoardBorder(app):
    # draw the board outline (with double-thickness):
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
             fill=None, border='black',
             borderWidth=2 * app.cellBorderWidth)
def drawCell(app, row, col, color="BLACK"):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight, fill=color, border='black', borderWidth=app.cellBorderWidth)


def getCellLeftTop(app, row, col):
    cellLeft = app.boardLeft + col * app.cellWidth
    cellTop = app.boardTop + row * app.cellHeight
    return (cellLeft, cellTop)
def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

def drawOnPlateBorder(app):
    app.onPlate.updateLowestRow()
    drawRect(0, (app.onPlate.getLowestRow())*app.cellHeight, app.cellWidth, (app.rows-app.onPlate.getLowestRow())*app.cellHeight,
             fill=None, border='black',
             borderWidth=2 * app.cellBorderWidth)
def drawOrderBoarder(app):
    if(len(app.orderList) == 1):
        if(app.orderList[0].getWithTopping()):
            drawRect(9 * app.cellWidth, 0,  app.cellWidth, 5* app.cellHeight,
             fill = None, border = "brown", borderWidth=5)
        else:
            drawRect(9 * app.cellWidth, 0, app.cellWidth, 4 * app.cellHeight,
                     fill=None, border="brown", borderWidth=5)
    if(len(app.orderList) == 2):
        if(app.orderList[0].getWithTopping()):
            drawRect(9 * app.cellWidth, 0,  app.cellWidth, 5* app.cellHeight,
             fill = None, border = "brown", borderWidth=5)
        else:
            drawRect(9 * app.cellWidth, 0, app.cellWidth, 4 * app.cellHeight,
                     fill=None, border="brown", borderWidth=5)
        if(app.orderList[1].getWithTopping()):
            drawRect(8 * app.cellWidth, 0,  app.cellWidth, 5* app.cellHeight,
             fill = None, border = "brown", borderWidth=5)
        else:
            drawRect(8 * app.cellWidth, 0, app.cellWidth, 4 * app.cellHeight,
                     fill=None, border="brown", borderWidth=5)
"""Randomly draw station based on a randomly generated list"""
def drawStation(app, row, col, itemCount):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    if(itemCount >= len(app.allOrders)):
        item = CMUImage(openImage("images/GameScreen/countertop.PNG"))
        drawImage(item, cellLeft, cellTop)
    else:
        app.board.setMapOfFood(row, col, app.setup.getAllItemsNameList()[itemCount])
        item = app.allOrders[itemCount]
        drawImage(item, cellLeft, cellTop)
        if(app.onPlate.getIsFinal()):
            if (app.setup.getAllItemsNameList()[itemCount] == "Plate"):
                drawImage(CMUImage(app.finalCupcake.resize((79,79))), cellLeft,cellTop)

"""GameScreen Movement"""
def gameScreen_onKeyHold(app, keys):
    step = 20 + (3 * DAY.getPlayerSpeedIncrement())
    if(not app.player.getSinkOn()):
        if(app.player.canMove(app.cellWidth, app.cellHeight) and app.player.checkBoundary(app.boardWidth, app.boardHeight)):
            if 'right' in keys:
                app.player.setXPosition(step)
                app.player.setDirection("right")
            elif 'left' in keys:
                app.player.setXPosition(-step)
                app.player.setDirection("left")
            elif 'up' in keys:
                app.player.setYPosition(-step)
                app.player.setDirection("up")
            elif 'down' in keys:
                app.player.setYPosition(step)
                app.player.setDirection("down")
"""
When submitting, most recent is on the right. 
If both are the same, the one with less time is submitted
If one is correct, that one is submitted
If none is correct, the one with less time is submitted
Customers not allowed to place order after DayOver but orders can be finished
"""
def gameScreen_onKeyPress(app, key):
    cupcakeCost = 5 + DAY.getCupcakePriceIncrement()
    if key == "p":
        setActiveScreen("pauseScreen")
    if key == "space":
        if(app.player.getHasItem()):
            app.player.itemDrop()
        else:
            app.player.itemPickUp()
    elif key == "enter":
        if(app.onPlate.getIsHoldingFinal() and not app.dayOver):
            if(len(app.orderList) > 1 and app.orderList[0].checkRESULT(app.onPlate.getCurrIngredientIndex()) and app.orderList[1].checkRESULT(app.onPlate.getCurrIngredientIndex())):
                if(app.orderList[0].getTime() <= app.orderList[1].getTime()):
                    finalCupcakeSubmission(app, 0)
                else:
                    finalCupcakeSubmission(app, 1)
            elif (app.orderList[0].checkRESULT(app.onPlate.getCurrIngredientIndex())):
                finalCupcakeSubmission(app, 0)
            elif(len(app.orderList) > 1 and app.orderList[1].checkRESULT(app.onPlate.getCurrIngredientIndex())):
                finalCupcakeSubmission(app, 1)
            else:
                if(app.orderList[0].getTime() <= app.orderList[1].getTime()):
                    finalCupcakeSubmission(app, 0)
                else:
                    finalCupcakeSubmission(app, 1)
        elif(app.onPlate.getIsHoldingFinal() and app.dayOver):
            if(len(app.orderList) > 1 and app.orderList[0].checkRESULT(app.onPlate.getCurrIngredientIndex())
                    and app.orderList[1].checkRESULT(app.onPlate.getCurrIngredientIndex())):
                if(app.orderList[0].getTime() <= app.orderList[1].getTime()):
                    app.score = Score.Score(app, app.orderList[0], app.onPlate.getCurrIngredientIndex(),app.isGoop).getScore()
                    app.tip = Tips.Tips(app.score, cupcakeCost).getTips()
                    DAY.orderIteration(app.score, app.tip)
                    app.day.orderIteration(app.score, app.tip)
                    setActiveScreen("submitScreen")
                    app.orderList.pop(0)
                    DAY.addMoney(app.tip + 5 + DAY.getCupcakePriceIncrement())
                    app.onPlate.resetCurrIngredientIndex()
                    app.player.reset()
                    app.orderList[0].resetOrder()
                elif(len(app.orderList) > 1 and app.orderList[0].getTime() > app.orderList[1].getTime()):
                    app.score = Score.Score(app, app.orderList[1], app.onPlate.getCurrIngredientIndex(), app.isGoop).getScore()
                    app.tip = Tips.Tips(app.score, cupcakeCost).getTips()
                    DAY.orderIteration(app.score, app.tip)
                    app.day.orderIteration(app.score, app.tip)
                    setActiveScreen("submitScreen")
                    app.orderList.pop(1)
                    DAY.addMoney(app.tip + 5 + DAY.getCupcakePriceIncrement())
                    app.onPlate.resetCurrIngredientIndex()
                    app.player.reset()
                    app.orderList[0].resetOrder()
            elif (app.orderList[0].checkRESULT(app.onPlate.getCurrIngredientIndex())):
                app.score = Score.Score(app, app.orderList[0], app.onPlate.getCurrIngredientIndex(),app.isGoop).getScore()
                app.tip = Tips.Tips(app.score, cupcakeCost).getTips()
                DAY.orderIteration(app.score, app.tip)
                app.day.orderIteration(app.score, app.tip)
                setActiveScreen("submitScreen")
                app.orderList.pop(0)
                DAY.addMoney(app.tip + 5 + DAY.getCupcakePriceIncrement())
                app.onPlate.resetCurrIngredientIndex()
                app.player.reset()
                if(len(app.orderList) > 0):
                    app.orderList[0].resetOrder()
            elif(len(app.orderList) > 1 and app.orderList[1].checkRESULT(app.onPlate.getCurrIngredientIndex())):
                app.score = Score.Score(app, app.orderList[1], app.onPlate.getCurrIngredientIndex(),app.isGoop).getScore()
                app.tip = Tips.Tips(app.score, cupcakeCost).getTips()
                DAY.orderIteration(app.score, app.tip)
                app.day.orderIteration(app.score, app.tip)
                setActiveScreen("submitScreen")
                app.orderList.pop(1)
                DAY.addMoney(app.tip + 5 + DAY.getCupcakePriceIncrement())
                app.onPlate.resetCurrIngredientIndex()
                app.player.reset()
                app.orderList[0].resetOrder()
            else:
                if(len(app.orderList)>1 and app.orderList[0].getTime() <= app.orderList[1].getTime()):
                    app.score = Score.Score(app, app.orderList[0], app.onPlate.getCurrIngredientIndex(),app.isGoop).getScore()
                    app.tip = Tips.Tips(app.score, cupcakeCost).getTips()
                    DAY.orderIteration(app.score, app.tip)
                    app.day.orderIteration(app.score, app.tip)
                    setActiveScreen("submitScreen")
                    app.orderList.pop(0)
                    DAY.addMoney(app.tip + 5 + DAY.getCupcakePriceIncrement())
                    app.onPlate.resetCurrIngredientIndex()
                    app.player.reset()
                    app.orderList[0].resetOrder()
                elif(len(app.orderList)>1 and app.orderList[0].getTime() > app.orderList[1].getTime()):
                    app.score = Score.Score(app, app.orderList[1], app.onPlate.getCurrIngredientIndex(),app.isGoop).getScore()
                    app.tip = Tips.Tips(app.score, cupcakeCost).getTips()
                    DAY.orderIteration(app.score, app.tip)
                    app.day.orderIteration(app.score, app.tip)
                    setActiveScreen("submitScreen")
                    app.orderList.pop(1)
                    DAY.addMoney(app.tip + 5 + DAY.getCupcakePriceIncrement())
                    app.onPlate.resetCurrIngredientIndex()
                    app.player.reset()
                    app.orderList[0].resetOrder()
                else:
                    app.score = Score.Score(app, app.orderList[0], app.onPlate.getCurrIngredientIndex(),app.isGoop).getScore()
                    app.tip = Tips.Tips(app.score, cupcakeCost).getTips()
                    DAY.orderIteration(app.score, app.tip)
                    app.day.orderIteration(app.score, app.tip)
                    setActiveScreen("submitScreen")
                    app.orderList.pop(0)
                    DAY.addMoney(app.tip + 5 + DAY.getCupcakePriceIncrement())
                    app.onPlate.resetCurrIngredientIndex()
                    app.player.reset()
        elif(not app.player.getHasItem() and app.onPlate.plateHasItem()):
            app.finalCupcake, app.isGoop = app.onPlate.showResult()
            app.onPlate.setIsFinal(True)
def finalCupcakeSubmission(app, num):
    cupcakeCost = 5 + DAY.getCupcakePriceIncrement()
    app.score = Score.Score(app, app.orderList[num], app.onPlate.getCurrIngredientIndex(), app.isGoop).getScore()
    app.tip = Tips.Tips(app.score, cupcakeCost).getTips()
    DAY.orderIteration(app.score, app.tip)
    app.day.orderIteration(app.score, app.tip)
    app.orderList.pop(num)
    if(len(app.orderList) > 0):
        app.orderList[0].resetOrder()
    app.orderList.append(Order.Order(app, app.board,DAY))
    DAY.addMoney(app.tip + 5 + DAY.getCupcakePriceIncrement())
    app.onPlate.resetCurrIngredientIndex()
    app.player.reset()
    setActiveScreen("submitScreen")

"""START SCREEN"""
def startScreen_onMousePress(app, mouseX, mouseY):
    playButtonX = 315
    playButtonY = 400
    playButtonWidth = app.imageWidth//3
    #accounts for button underneath
    playButtonHeight = app.imageHeight//3 + 30
    tipsButtonX = 575
    tipsButtonY = 400
    tipsButtonWidth = app.imageWidth // 3
    # accounts for button underneath
    tipsButtonHeight = app.imageHeight // 3  + 20
    instructionsButtonX = 50
    instructionsButtonY = 400
    instructionsButtonWidth = app.imageWidth // 3
    instructionsButtonHeight = app.imageHeight // 3 + 10
    if ((playButtonX <= mouseX <= playButtonX + playButtonWidth) and (playButtonY <= mouseY <= playButtonY + playButtonHeight )):
        DAY.resetTime(DAY.getDayTime())
        setActiveScreen('gameScreen')
    elif ((tipsButtonX <= mouseX <= tipsButtonX + tipsButtonWidth) and (tipsButtonY <= mouseY <= tipsButtonY + tipsButtonHeight)):
        setActiveScreen("tipsScreen")
    elif ((instructionsButtonX <= mouseX <= instructionsButtonX + instructionsButtonWidth) and (instructionsButtonY <= mouseY <= instructionsButtonY + instructionsButtonHeight )):
        setActiveScreen("instructionsScreen")
def startScreen_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill='purple')
    drawImage(CMUImage(app.titleText), 60, 5)
    newWidth, newHeight = (app.imageWidth // 3, app.imageHeight // 3)
    drawImage(CMUImage(app.playButton), 315, 400, width=newWidth, height=newHeight)
    drawImage(CMUImage(app.cupcakeStrip), app.cx, app.cy)
    drawImage(CMUImage(app.tipsButton), 575, 400, width=newWidth, height=newHeight)
    drawImage(CMUImage(app.instructionsButton), 50, 400, width=newWidth, height=newHeight)
    drawImage(CMUImage(app.sprinkleBackground), 130, 0)
    drawRect(100, 545, newWidth / 2.5, newHeight / 7, fill='white')
    drawImage(CMUImage(app.playText), 360, 560, width=newWidth / 2, height=newHeight / 5)
    drawImage(CMUImage(app.tipsText), 620, 550, width=newWidth / 2, height=newHeight / 5)
    drawImage(CMUImage(app.instructionsText), 90, 540, width=newWidth / 2, height=newHeight / 5)
def startScreen_onStep(app):
    app.cx += app.dx
    if app.cx + app.cupcakeStrip.width // 2 >= app.width:
        app.cx = -app.cupcakeStrip.width
"""INSTRUCTIONS SCREEN"""
def instructionsScreen_redrawAll(app):
    newWidth, newHeight = (app.instructionImagewidth // 1.5, app.instructionImageHeight // 1.5)
    drawRect(0, 0, app.width, app.height, fill='pink')
    drawRect(100, 196, 600, 500, fill='purple')
    drawImage(CMUImage(app.instructionsManualImage), 0, 0)
    drawImage(CMUImage(app.instructionsParagraph), 100, 196)
    drawImage(CMUImage(app.instructionsSprinkleBackground), 130, 0)
    drawImage(CMUImage(app.instructionsBack), 360, 730, width=newWidth / 2, height=newHeight / 2)
def instructionsScreen_onMousePress(app, mouseX, mouseY):
    instructionsBackButtonX = 360
    instructionsBackButtonY = 730
    instructionsBackButtonWidth = app.imageWidth // 3
    instructionsBackButtonHeight = app.imageWidth // 3
    if ((instructionsBackButtonX <= mouseX <= instructionsBackButtonX + instructionsBackButtonWidth) and (
            instructionsBackButtonY <= mouseY <= instructionsBackButtonY + instructionsBackButtonHeight)):
        onAppStart(app)
        setActiveScreen("startScreen")
"""SUBMIT SCREEN"""
def submitScreen_redrawAll(app):
    newWidth, newHeight = (app.submitImageWidth//1.5,app.submitImageHeight//1.5)
    drawRect(0, 0, app.width, app.height, fill = 'pink')
    drawLabel(app.submitMessage, 220, 150, font = 'Courier', size = 40, fill = 'purple', bold = True)
    drawLabel('Rating', 600, 150, font = 'Courier', size = 40, fill = 'purple', bold = True)
    drawLabel('Tips', 600, 550, font = 'Courier', size = 40, fill = 'purple', bold = True)
    drawImage(CMUImage(app.submitSprinkleBackground), 130, 0)
    drawLabel("PRESS SPACE TO CONTINUE", 400,775, size = 30)
    drawImage(CMUImage(app.finalCupcake.resize((400,400))), 50,200)
    drawLabel(str(app.score) + " STARS", 600, 250, size = 60)
    drawLabel("$" + str(app.tip), 600, 650, size=100)
def submitScreen_onKeyPress(app, key):
    if(key == "space"):
        setActiveScreen("gameScreen")
"""END SCREEN"""
def endScreen_redrawAll(app):
    newWidth, newHeight = (app.endScreenImageWidth//1.5,app.endScreenImageHeight//1.5)
    drawRect(0, 0, app.width, app.height, fill = 'pink')
    drawImage(CMUImage(app.endScreenSprinkleBackground), 130, 0)
    drawImage(CMUImage(app.endScreenPlayAgain), 360, 730, width=newWidth / 2, height=newHeight / 2)
    drawImage(CMUImage(app.endScreenGameOver), 35, 150)
    drawRect(220, 380, 350, 50, fill = 'purple')
    drawLabel(app.endScreenMessage, 400, 400, font = 'Courier', size = 20, bold = True)
    drawLabel('Yay! You played for ' + str(DAY.getDay()) + ' days', 400, 500, font='Courier', size=20, bold=True)
    drawLabel('You averaged a total of '+ str(pythonRound(DAY.getTotalTips() / DAY.getDay(), 2)) +' stars!', 400, 525, font='Courier', size=20, bold=True)
    drawLabel('You earned ' + str(DAY.getTotalTips()) + ' in tips!', 400, 550, font='Courier', size=20, bold=True)
def endScreen_onMousePress(app, mouseX, mouseY):
    global DAY
    endScreenPlayAgainButtonX = 360
    endScreenPlayAgainButtonY = 730
    endScreenPlayAgainButtonWidth = app.imageWidth // 3
    endScreenPlayAgainButtonHeight = app.imageWidth // 3
    if ((endScreenPlayAgainButtonX <= mouseX <= endScreenPlayAgainButtonX+ endScreenPlayAgainButtonWidth) and
            (endScreenPlayAgainButtonY <= mouseY <= endScreenPlayAgainButtonY + endScreenPlayAgainButtonHeight)):
        DAY = Day.Day(0)
        onAppStart(app)
        setActiveScreen("startScreen")
"""PAUSE SCREEN"""
def pauseScreen_redrawAll(app):
    newWidth, newHeight = app.pauseScreenHome.width//3, app.pauseScreenHome.height//3
    drawRect(0, 0, app.width, app.height, fill = 'purple')
    drawImage(CMUImage(app.gamePaused), 20, 0)
    drawLabel('Press [p] to unpause', 400, 500, font = 'Courier', size = 30, bold = True, fill = 'pink')
    drawLabel('Total Money: $' + str(DAY.getTOTALMONEY()), 400, 300, font = 'Courier', size = 30, bold = True, fill = 'pink')
    drawLabel('Time left for Day: ' + str(app.day.getTime()) + " seconds", 400, 200, font='Courier', size=30, bold=True, fill='pink')
    drawImage(CMUImage(app.pauseScreenHome), 360, 730, width = newWidth, height = newHeight)
    drawImage(CMUImage(app.pauseScreenSprinkleBackground), 130, 0)
def pauseScreen_onMousePress(app, mouseX, mouseY):
    pauseScreenHomeButtonX = 360
    pauseScreenHomeButtonY = 730
    pauseScreenHomeButtonWidth = app.imageWidth // 3
    pauseScreenHomeButtonHeight = app.imageWidth // 3
    if ((pauseScreenHomeButtonX <= mouseX <= pauseScreenHomeButtonX + pauseScreenHomeButtonWidth) and (
            pauseScreenHomeButtonY <= mouseY <= pauseScreenHomeButtonY + pauseScreenHomeButtonHeight)):
        onAppStart(app)
        setActiveScreen("startScreen")
def pauseScreen_onKeyPress(app, key):
    if key=='p':
        setActiveScreen('gameScreen')
"""DAY OVER SCREEN"""
def dayOverScreen_redrawAll(app):
    newWidth, newHeight = app.dayOverHome.width//3, app.dayOverHome.height//3
    drawRect(0, 0, app.width, app.height, fill = 'purple')
    drawImage(CMUImage(app.dayOverDayOver), -25, 0)
    if(app.day.getNumberOfOrders() == 0):
        average = 0
    else:
        average = pythonRound(app.day.getTotalStars() / app.day.getNumberOfOrders(),2)
    drawLabel('You completed ' + str(app.day.getNumberOfOrders()) +' orders', 400, 500, font = 'Courier', size = 30, bold = True, fill = 'pink')
    drawLabel('You averaged ' + str(average) +' stars today', 400, 400, font = 'Courier', size = 30, bold = True, fill = 'pink')
    drawLabel('You got $'  + str(app.day.getTotalTips()) +' in tips today', 400, 300, font = 'Courier', size = 30, bold = True, fill = 'pink')
    drawRect(710,740,50,15, fill = "white")
    drawImage(CMUImage(app.dayOverHome), 360, 730, width = newWidth, height = newHeight)
    drawImage(CMUImage(app.dayOverSprinkleBackground), 130, 0)
    drawImage(CMUImage(app.dayOverNextDayButton), 700, 730, width = newWidth, height = newHeight)
    drawImage(CMUImage(app.dayOverStoreButton), 50, 730, width = newWidth, height = newHeight)
def dayOverScreen_onMousePress(app, mouseX, mouseY):
    dayOverHomeButtonX = 360
    dayOverHomeButtonY = 730
    dayOverHomeButtonWidth = app.imageWidth // 3
    dayOverHomeButtonHeight = app.imageWidth // 3
    dayOverNextDayButtonX = 700
    dayOverNextDayButtonY = 730
    dayOverNextDayButtonWidth = app.imageWidth // 3
    dayOverNextDayButtonnHeight = app.imageWidth // 3
    dayOverNextStoreButtonX = 50
    dayOverNextStoreButtonY = 730
    dayOverNextStoreButtonWidth = app.imageWidth // 3
    dayOverNextStoreButtonHeight = app.imageWidth // 3
    if ((dayOverHomeButtonX <= mouseX <= dayOverHomeButtonX + dayOverHomeButtonWidth) and (
            dayOverHomeButtonY <= mouseY <= dayOverHomeButtonY + dayOverHomeButtonHeight)):
        onAppStart(app)
        setActiveScreen("startScreen")
    elif ((dayOverNextDayButtonX <= mouseX <= dayOverNextDayButtonX + dayOverNextDayButtonWidth) and (
            dayOverNextDayButtonY <= mouseY <= dayOverNextDayButtonY + dayOverNextDayButtonnHeight)):
        onAppStart(app)
        setActiveScreen("gameScreen")
    elif ((dayOverNextStoreButtonX <= mouseX <= dayOverNextStoreButtonX + dayOverNextStoreButtonWidth) and (
            dayOverNextStoreButtonY <= mouseY <= dayOverNextStoreButtonY + dayOverNextStoreButtonHeight)):
        setActiveScreen("storeScreen")
"""STORE SCREEN"""
def storeScreen_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill = 'purple')
    drawImage(CMUImage(app.storeLabel), 200, 0)
    drawImage(CMUImage(app.storeSprinkleBackground), 130, 0)
    newWidth, newHeight = (app.instructionImagewidth // 1.5, app.instructionImageHeight // 1.5)
    drawImage(CMUImage(app.storeBack), 360, 750, width=newWidth / 2, height=newHeight / 2)
    if(DAY.getPlayerSpeedIncrement()<3):
        drawImage(CMUImage(app.storeFasterSprite), 100, 200)
        drawLabel('Faster Sprite!', 200, 425, font='Courier', size=20, bold=True)
        drawLabel('Cost: $' + str(DAY.getPlayerSpeedPrice()), 200, 470, font='Courier', size=20, bold=True)
    if(DAY.getHintLevelIncrement() < 2):
        drawImage(CMUImage(app.storeBetterHint), 300, 200)
        drawLabel('Better Hints!', 400, 425, font='Courier', size=20, bold=True)
        drawLabel('Cost: $' + str(DAY.getHintLevelPrice()), 400, 470, font='Courier', size=20, bold=True)
    if(DAY.getDayTimeIncrement() < 3):
        drawImage(CMUImage(app.storeMoreTime), 500, 200)
        drawLabel('More Time For Cupcakes!', 625, 425, font='Courier', size=20, bold=True)
        drawLabel('Cost: $' + str(DAY.getDayTimePrice()), 600, 470, font='Courier', size=20, bold=True)
    if(DAY.getSinkAndOvenIncrement() < 3):
        drawImage(CMUImage(app.storeOvenAndSink), 100, 500)
        drawLabel('Less Baking/Washing', 150, 725, font='Courier', size=20, bold=True)
        drawLabel('Cost: $' + str(DAY.getSinkAndOvenPrice()), 200, 750, font='Courier', size=20, bold=True)
    if(DAY.getCupcakePriceIncrement() < 3):
        drawImage(CMUImage(app.storeExpensiveCupcakes), 300, 500)
        drawLabel('Higher Cupcake Price', 400, 725, font='Courier', size=20, bold=True)
        drawLabel('Cost: $' + str(DAY.getCupcakePricePrice()), 400, 750, font='Courier', size=20, bold=True)
    if(DAY.getWaitTimeIncrement() < 2):
        drawImage(CMUImage(app.storeCustomerLongerWait), 500, 500)
        drawLabel('Longer Wait Time', 625, 725, font = 'Courier', size = 20, bold = True)
        drawLabel('Cost: $' + str(DAY.getWaitTimePrice()), 600, 750, font = 'Courier', size = 20, bold = True)
    drawLabel('Click to Buy Advanced Features', 400, 175, font = 'Courier', size = 20, bold = True)
    drawLabel('You have $'+ str(DAY.getTOTALMONEY()) +' to spend', 150, 10, font = 'Courier', size = 20, bold = True)
def storeScreen_onMousePress(app, mouseX, mouseY):
    storeBackButtonX = 360
    storeBackButtonY = 730
    storeBackButtonWidth = app.imageWidth // 3
    storeBackButtonHeight = app.imageWidth // 3
    storeFasterSpriteButtonX = 100
    storeFasterSpriteButtonY = 200
    storeFasterSpriteButtonWidth = 200
    storeFasterSpriteButtonHeight = 200
    storeBetterHintButtonX = 300
    storeBetterHintButtonY = 200
    storeBetterHintButtonWidth = 200
    storeBetterHintButtonHeight = 200
    storeMoreTimeButtonX = 500
    storeMoreTimeButtonY = 200
    storeMoreTimeButtonWidth = 200
    storeMoreTimeButtonHeight = 200
    storeOvenAndSinkButtonX = 100
    storeOvenAndSinkButtonY= 500
    storeOvenAndSinkButtonWidth = 200
    storeOvenAndSinkButtonHeight = 200
    storeExpensiveCupcakesButtonX = 300
    storeExpensiveCupcakesButtonY= 500
    storeExpensiveCupcakesButtonWidth = 200
    storeExpensiveCupcakesButtonHeight = 200

    storeCustomerLongerWaitButtonX = 500
    storeCustomerLongerWaitButtonY= 500
    storeCustomerLongerWaitButtonWidth = 200
    storeCustomerLongerWaitButtonHeight = 200
    if (DAY.getPlayerSpeedIncrement()<3 and (storeFasterSpriteButtonX <= mouseX <= storeFasterSpriteButtonX + storeFasterSpriteButtonWidth) and (
            storeFasterSpriteButtonY <= mouseY <= storeFasterSpriteButtonY + storeFasterSpriteButtonHeight)):
        if(DAY.getTOTALMONEY() >= DAY.getPlayerSpeedPrice()):
            DAY.addMoney(-DAY.getPlayerSpeedPrice())
            DAY.playerSpeedIncrement()
    elif (DAY.getHintLevelIncrement() < 2 and (storeBetterHintButtonX <= mouseX <= storeBetterHintButtonX + storeBetterHintButtonWidth) and (
            storeBetterHintButtonY <= mouseY <= storeBetterHintButtonY + storeBetterHintButtonHeight)):
        if(DAY.getTOTALMONEY() >= DAY.getHintLevelPrice()):
            DAY.addMoney(-DAY.getHintLevelPrice())
            DAY.hintLevelIncrement()
    elif (DAY.getDayTimeIncrement() < 3 and (storeMoreTimeButtonX <= mouseX <= storeMoreTimeButtonX + storeMoreTimeButtonWidth) and (
            storeMoreTimeButtonY <= mouseY <= storeMoreTimeButtonY + storeMoreTimeButtonHeight)):
        if (DAY.getTOTALMONEY() >= DAY.getDayTimePrice()):
            DAY.addMoney(-DAY.getDayTimePrice())
            DAY.dayTimeIncrement()
    elif (DAY.getSinkAndOvenIncrement() < 3 and (storeOvenAndSinkButtonX <= mouseX <= storeOvenAndSinkButtonX + storeOvenAndSinkButtonWidth) and (
            storeOvenAndSinkButtonY <= mouseY <= storeOvenAndSinkButtonY + storeOvenAndSinkButtonHeight)):
        if (DAY.getTOTALMONEY() >= DAY.getSinkAndOvenPrice()):
            DAY.addMoney(-DAY.getSinkAndOvenPrice())
            DAY.sinkAndOvenIncrement()
    elif (DAY.getCupcakePriceIncrement() < 3 and (storeExpensiveCupcakesButtonX <= mouseX <= storeExpensiveCupcakesButtonX + storeExpensiveCupcakesButtonWidth) and (
            storeExpensiveCupcakesButtonY <= mouseY <= storeExpensiveCupcakesButtonY + storeExpensiveCupcakesButtonHeight)):
        if (DAY.getTOTALMONEY() >= DAY.getCupcakePricePrice()):
            DAY.addMoney(-DAY.getCupcakePricePrice())
            DAY.cupcakePriceIncrement()
    elif (DAY.getWaitTimeIncrement() < 2 and (storeCustomerLongerWaitButtonX <= mouseX <= storeCustomerLongerWaitButtonX + storeCustomerLongerWaitButtonWidth) and (
            storeCustomerLongerWaitButtonY <= mouseY <= storeCustomerLongerWaitButtonY + storeCustomerLongerWaitButtonHeight)):
        if (DAY.getTOTALMONEY() >= DAY.getWaitTimePrice()):
            DAY.addMoney(-DAY.getWaitTimePrice())
            DAY.waitTimeIncrement()
    elif ((storeBackButtonX <= mouseX <= storeBackButtonX + storeBackButtonWidth) and (
            storeBackButtonY <= mouseY <= storeBackButtonY + storeBackButtonHeight)):
        setActiveScreen("dayOverScreen")
def winScreen_redrawAll(app):
    newWidth, newHeight = (app.winImageWidth//1.5,app.winImageHeight//1.5)
    drawRect(0, 0, app.width, app.height, fill = 'pink')
    drawImage(CMUImage(app.winSprinkleBackground), 130, 0)
    drawImage(CMUImage(app.winPlayAgain), 360, 730, width=newWidth / 2, height=newHeight / 2)
    drawImage(CMUImage(app.win), 35, 150)
    if (DAY.getNumberOfOrders() == 0):
        average = 0
    else:
        average = pythonRound(DAY.getTotalStars() / DAY.getNumberOfOrders(),2)
    drawLabel(app.winMessage + str(DAY.getTOTALMONEY()), 400, 400, font = 'Courier', size = 20, bold = True)
    drawLabel('You completed '+ str(DAY.getNumberOfOrders())+' orders', 400, 550, font='Courier', size=30, bold=True)
    drawLabel('You averaged '+ str(average)+' stars in total', 400, 500, font='Courier', size=30, bold=True)
    drawLabel('You got $'+ str(DAY.getTotalTips()) +' in tips in total', 400, 450, font='Courier', size=30, bold=True)
def winScreen_onMousePress(app, mouseX, mouseY):
    global DAY
    winPlayAgainButtonX = 360
    winPlayAgainButtonY = 730
    winPlayAgainButtonWidth = app.imageWidth // 1.5
    winPlayAgainButtonHeight = app.imageHeight // 1.5
    if ((winPlayAgainButtonX <= mouseX <= winPlayAgainButtonX + winPlayAgainButtonWidth) and (
    winPlayAgainButtonY <= mouseY <= winPlayAgainButtonY + winPlayAgainButtonHeight)):
        DAY = Day.Day(0)
        onAppStart(app)
        setActiveScreen("startScreen")
"""TIPS SCREEN"""
def tipsScreen_redrawAll(app):
    newWidth, newHeight = (app.tipsImageWidth//1.5,app.tipsImageHeight//1.5)
    drawRect(0, 0, app.width, app.height, fill = 'pink')
    drawImage(CMUImage(app.tipSprinkleBackground), 130, 0)
    drawImage(CMUImage(app.tipBack), 360, 730, width=newWidth / 2, height=newHeight / 2)
    drawImage(CMUImage(app.yourTips), 35, 150)
    if (DAY.getNumberOfOrders() == 0):
        average = 0
    else:
        average = pythonRound(DAY.getTotalStars() / DAY.getNumberOfOrders(),2)
    drawLabel('You averaged ' + str(average) + ' stars', 400, 550, font = 'Courier', size = 30, bold = True)
    drawLabel('You got $'+str(DAY.getTotalTips()) +' in tips', 400, 500, font = 'Courier', size = 30, bold = True)
    drawLabel('You got $'+ str(DAY.TOTALMONEY) +' in Total Money', 400, 450, font='Courier', size=30, bold=True)
    drawLabel('DAY:' + str(DAY.getDay()), 400, 400, font='Courier', size=30, bold=True)


def tipsScreen_onMousePress(app, mouseX, mouseY):
    tipBackButtonX = 360
    tipBackButtonY = 730
    tipBackButtonWidth = app.imageWidth // 1.5
    tipBackButtonHeight = app.imageHeight // 1.5
    if ((tipBackButtonX <= mouseX <= tipBackButtonX + tipBackButtonWidth) and (
            tipBackButtonY <= mouseY <= tipBackButtonY + tipBackButtonHeight)):
        setActiveScreen("startScreen")
def main():
    runAppWithScreens(initialScreen='storeScreen', width = 800, height = 800)

main()

