import sys

from time import sleep
from random import random, randint
from pyautogui import position, size, moveTo, click, mouseDown, mouseUp
from pathLogger import getSection, verticalSectionLength, horizontalSectionLength, playBackPath
from sectionTransfer import getTransferFromSections, getTransferFromPoints
from sectionTransfer import getRandomPathFromTransfer as getPathFromTransfer

minSecLength = min(verticalSectionLength, horizontalSectionLength)

def pythagoranDist(point1, point2):
    squaredXDiff = (point1[0] - point2[0])**2
    squaredYDiff = (point1[1] - point2[1])**2
    return (squaredXDiff + squaredYDiff)**0.5

def pointDiff(point1, point2):
    return (
        point1[0] - point2[0],
        point1[1] - point2[1]
    )

def pointSum(point1, point2):
    return (
        point1[0] + point2[0],
        point1[1] + point2[1]
    )

def applyOffsetToPath(path, offset):
    path.startPoint = pointSum(path.startPoint, offset)
    for index in range(len(path.pointList)):
        path.pointList[index] = pointSum(path.pointList[index], offset)
    path.endPoint = pointSum(path.endPoint, offset)
    path.startSection = getSection(path.startPoint)
    path.endSection = getSection(path.endPoint)
    return path

def applyShearTransformToPoint(xScale, yScale, fixedPoint, tPoint):
    return (
        int(tPoint[0] + xScale * (tPoint[1] - fixedPoint[1])),
        int(yScale*(tPoint[0]-fixedPoint[0]) + xScale*(tPoint[1] - fixedPoint[1]) + tPoint[1])
    )

def applyShearTransformToPath(xScale, yScale, fixedPoint, path):
    for index in range(len(path.pointList)):
        path.pointList[index] = applyShearTransformToPoint(xScale, yScale, fixedPoint, path.pointList[index])
    path.endPoint = applyShearTransformToPoint(xScale, yScale, fixedPoint, path.endPoint)
    return path


def shearPathToPoint(path, goalPoint):
    x = path.endPoint[0]
    xG = goalPoint[0]
    y = path.endPoint[1]
    yG = goalPoint[1]
    x0 = path.startPoint[0]
    y0 = path.startPoint[1]
    xScale = 0
    yScale = 0

    if (y-y0) != 0:
        xScale = (xG - x)/(y-y0)
    if (x - x0) != 0:
        yScale = (yG - y - xScale*(y-y0))/(x-x0)
    
    return applyShearTransformToPath(xScale, yScale, path.startPoint, path)

def MovePathToStartPoint(path, newStartPoint):
    startDiff = pointDiff(newStartPoint, path.startPoint)
    path = applyOffsetToPath(path, startDiff)
    return path

def combinePaths(path1, path2):
    newpath = path1
    mixPath = path2
    ratio = random()/4
    if len(path1.pointList) > len(path2.pointList):
        newpath = path2
        mixPath = path1

    mixIndex = randint(0, len(mixPath.pointList) - len(newpath.pointList))

    if mixIndex != 0:
        mixpath = applyOffsetToPath(mixPath, pointDiff(newpath.startPoint, mixPath.pointList[mixIndex - 1]))
    
         

    if mixIndex == 0:
        newpath.startPoint = averagePoints(newpath.startPoint, mixPath.startPoint, ratio)
    else:
        newpath.startPoint = averagePoints(newpath.startPoint, mixPath.pointList[mixIndex - 1], ratio)

    for index in range(len(newpath.pointList)):
        newpath.pointList[index] = averagePoints(newpath.pointList[index], mixPath.pointList[index + mixIndex], ratio)
    newpath.endPoint = averagePoints(newpath.endPoint, mixPath.pointList[len(newpath.pointList) - 1 + mixIndex], ratio)

    newpath.startSection = getSection(newpath.startPoint)
    newpath.endSection = getSection(newpath.endPoint)

    return newpath


def averagePoints(point1, point2, ratio = 0.5):
    return(
        point1[0]*ratio + point2[0]*(1.0 - ratio),
        point1[1]*ratio + point2[1]*(1.0 - ratio),
    )

def getPathToPoint(goalPoint):
    currPoint = position()
    transfer = getTransferFromPoints(currPoint, goalPoint)
    pathToPoint = getPathFromTransfer(transfer)

    for x in range(randint(0, 3)):
        mixPath = getPathFromTransfer(transfer)
        mixPath = MovePathToStartPoint(mixPath, currPoint)
        pathToPoint = MovePathToStartPoint(pathToPoint, currPoint)
        pathToPoint = combinePaths(pathToPoint, mixPath)
    
    pathToPoint = MovePathToStartPoint(pathToPoint, currPoint)
    #Start point of path is the "Fixed point"
    return shearPathToPoint(pathToPoint, goalPoint)

def moveMouseToPoint(goalPoint):
    currPoint = position()
    dist = pythagoranDist(goalPoint, currPoint)

    if dist < 1:
        return

    if dist < 0.125 * minSecLength:
        rate = 1920/(random()*2.5 + 0.5)
        moveTo(goalPoint[0], goalPoint[1], dist/rate, circlePath) #start and end slow
        return

    path = getPathToPoint(goalPoint)
    playBackPath(path)
    return

def circlePath(pos):
    if pos < 0.25:
        return -(0.0625 - pos**2)**0.5 + 0.25
    else:
        return (0.5625 - (pos-1)**2)**0.5 + 0.25
        
"""

def getDiamondPoints():
    width = size()[0]
    height = size()[1]
    return(
        (int(width*0.5), int(height*0.75)),
        (int(width*0.25), int(height*0.5)),
        (int(width*0.5), int(height*0.25)),
        (int(width*0.75), int(height*0.5)),
        (int(width*0.5), int(height*0.75))
    )

def getSquarePoints():
    width = size()[0]
    height = size()[1]
    return(
        (int(width*0.75), int(height*0.75)),
        (int(width*0.25), int(height*0.75)),
        (int(width*0.25), int(height*0.25)),
        (int(width*0.75), int(height*0.25)),
        (int(width*0.75), int(height*0.75))
    )

for x in range(15):
    for dPoint in getDiamondPoints():
        moveMouseToPoint(dPoint)
        mouseDown()
        sleep(1)



for x in range(15):
    for dPoint in getSquarePoints():
        print("Transfer: ", getTransferFromPoints(position(), dPoint))
        moveMouseToPoint(dPoint)
        print("Goal was: ", dPoint, " Landed at ", position())
        sleep(1)

mouseUp()
""" 