from random import random
from math import pi, sin, cos
from time import sleep
from pyautogui import moveTo, click
import pyautogui

def pickPointInCircle(center, radius):
    polarRadius = radius*random()
    angle = 2*pi*random()
    pointX = polarRadius*cos(angle)
    pointY = polarRadius*sin(angle)
    return (
        int(pointX + center[0]),
        int(pointY + center[1])
    )

def pickPointinRectangle(corner, height, width):
    return (
        int(random()*height + corner[0]),
        int(random()*width  + corner[1])
    )

def pickPointinSquare(center, length):
    return (
        int(random()*length + center[0] - 0.5*length),
        int(random()*length + center[1] - 0.5*length)
    )

