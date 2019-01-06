import sys

from time import sleep
from pyautogui import position, size, moveTo
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

def getPathToPoint(goalPoint):
    currPoint = position()
    
    #prevent small movements that cross section boundaries from being highly distorted by shear.
    if pythagoranDist(goalPoint, currPoint) < 0.5 * minSecLength:
        transfer = (0,0)
    else:
        transfer = getTransferFromPoints(currPoint, goalPoint)

    pathToPoint = getPathFromTransfer(transfer)
    pathToPoint = MovePathToStartPoint(pathToPoint, currPoint)

    #Start point of path is the "Fixed point"
    return shearPathToPoint(pathToPoint, goalPoint)


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
    return(
        (int(width*0.75), int(height*0.75)),
        (int(width*0.25), int(height*0.75)),
        (int(width*0.25), int(height*0.25)),
        (int(width*0.75), int(height*0.25)),
        (int(width*0.75), int(height*0.75))
    )

for x in range(5):
    for dPoint in getDiamondPoints():
        print("Transfer: ", getTransferFromPoints(position(), dPoint))
        playBackPath(getPathToPoint(dPoint))
        print("Goal was: ", dPoint, " Landed at ", position())
        sleep(1)

for x in range(5):
    for dPoint in getSquarePoints():
        print("Transfer: ", getTransferFromPoints(position(), dPoint))
        playBackPath(getPathToPoint(dPoint))
        print("Goal was: ", dPoint, " Landed at ", position())
        sleep(1)


