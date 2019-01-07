from pyautogui import platformModule, size
from math import sin, pi
import pyautogui
from time import sleep
from random import random

center = (int(size()[0]/2), int(size()[1]/2))
goal = (center[0] - 500, center[1] - 500)

def goToCenter():
    platformModule._moveTo(center[0],center[1])

def goToGoal():
    platformModule._moveTo(goal[0],goal[1])

def circlePath(pos):
    if pos < 0.25:
        return -(0.0625 - pos**2)**0.5 + 0.25
    else:
        return (0.5625 - (pos-1)**2)**0.5 + 0.25

goToCenter()
sleep(1)

for x in range(5):
    dist = ((center[0] - goal[0])**2 + (center[1] - goal[1])**2)**0.5
    print(dist)
    rate = 1920/(random()*3 + 1)
    print(dist/rate)
    goToCenter()
    pyautogui.moveTo(goal[0], goal[1], dist/rate, circlePath) #start and end slow

