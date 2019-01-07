import HumanMouseMovement as HMM
import PointPick

from pyautogui import mouseDown, mouseUp
from random import random, randint
from time import sleep

compassCenter = (1735, 79)
compassRadius = 14

playerBaseAtCameraReset = (963, 578)
spotInFrontOfPlayer = (963, 625)

def clickCompass():
    compassPoint = PointPick.pickPointInCircle(compassCenter, compassRadius)
    clickTarget(compassPoint)

def clickTarget(tPoint):
    sleep(getWaitBetweenMovesInterval())
    HMM.moveMouseToPoint(compassPoint)
    sleep(getWaitToClickInterval())
    humanClick()


def getWaitToClickInterval():
    return 0.4 + 0.4*random()

def getWaitBetweenMovesInterval():
    return 0.05 + 0.1 *random() 

def humanClick():
    mouseDown()
    sleep(random()/10)
    mouseUp()


clickCompass()
HMM.moveMouseToPoint(playerBaseAtCameraReset)