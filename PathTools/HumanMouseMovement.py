import sys

from time import sleep
from pyautogui import position, size, moveTo
from pathLogger import getSection, manhattanDist, verticalSectionLength, horizontalSectionLength, playBackPath
from sectionTransfer import getTransferFromSections
from sectionTransfer import getRandomPathFromTransfer as getPath 

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
    xScale = (xG - x)/(y-y0)
    yScale = (yG - y - xScale*(y-y0))/(x-x0)
    return applyShearTransformToPath(xScale, yScale, path.startPoint, path)

def getPathToPoint(goalPoint):
    currPoint = position()
    
    #prevent small movements that cross section boundaries from being causing highly distorted.
    if pythagoranDist(goalPoint, currPoint) < 0.5 * minSecLength:
        transfer = (0,0)
    else:
        transfer = getTransferFromSections(getSection(currPoint), getSection(goalPoint))

    pathToPoint = getPath(transfer)
    startDiff = (0,0)#pointDiff(currPoint, pathToPoint.startPoint)

    #ensure start points match
    pathToPoint = applyOffsetToPath(pathToPoint, startDiff)

    if(pathToPoint.startPoint != position()[0]):
        print("paths don't match")
    else:
        print("paths match")

    #Start point of path is the "Fixed point"
    return shearPathToPoint(pathToPoint, goalPoint)



"""
testpath = getPath((0,-1))
print("Playing back random path...")
playBackPath(testpath)
sleep(1)
moveTo(testpath.startPoint)


print("Playing back sheared path...")
sleep(1)
testpath = shearPathToPoint(testpath, (100, 100))
playBackPath(testpath)


"""
def getDiamondpoints():
    width = size()[0]
    height = size()[1]
    return(
        (width*0.5, height*0.75),
        (width*0.25, height*0.5),
        (width*0.5, height*0.25),
        (width*0.75, height*0.5),
        (width*0.5, height*0.75)
    )
print(size())
print(getDiamondpoints())

for dPoint in getDiamondpoints():
    moveTo(dPoint)
    #playBackPath(getPathToPoint(dPoint))
    sleep(1)
