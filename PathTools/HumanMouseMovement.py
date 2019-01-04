import sys

from pyautogui import position, size
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
    for point in path.pointList:
        point = pointSum(point, offset)
    path.startPoint = pointSum(path.startPoint, offset)
    path.endPoint = pointSum(path.endPoint, offset)
    path.startSection = getSection(path.startPoint)
    path.endSection = getSection(path.endPoint)
    return path

def applyTransformToPoint(xScale, yScale, fixedPoint, pointToTransform):
    return (
        int(pointToTransform[0]*xScale + (1 - xScale)*fixedPoint[0]),
        int(pointToTransform[1]*yScale + (1 - yScale)*fixedPoint[1])
    )

def applyTransformToPath(xScale, yScale, fixedPoint, path):
    for index in range(len(path.pointList)):
        path.pointList[index] = applyTransformToPoint(xScale, yScale, fixedPoint, path.pointList[index])
    path.endPoint = applyTransformToPoint(xScale, yScale, fixedPoint, path.endPoint)
    return path


def getPathToPoint(goalPoint):
    currPoint = position()
    
    #prevent small movements that cross section boundaries from being causing highly distorted.
    if pythagoranDist(goalPoint, currPoint) < 0.5 * minSecLength:
        transfer = (0,0)
    else:
        transfer = getTransferFromSections(getSection(currPoint), getSection(goalPoint))
    
    pathToPoint = getPath(transfer)
    startDiff = pointDiff(pathToPoint.startPoint, currPoint)
    applyOffsetToPath(pathToPoint, startDiff)

    pathDiff = pointDiff(pathToPoint.endPoint, pathToPoint.startPoint)
    endPointDiff = pointDiff(goalPoint, pathToPoint.startPoint)
    xScaleFactor = pathDiff[0]/endPointDiff[0]
    yScaleFactor = pathDiff[1]/endPointDiff[1]

    #Start point of path is the "Fixed point"
    return applyTransformToPath(xScaleFactor, yScaleFactor, pathToPoint.startPoint, pathToPoint)

"""
def getDiamondpoints():
    width = size()[0]/2
    height = size()[1]
    return(
        (width*0.5, height*0.75),
        (width*0.25, height*0.5),
        (width*0.5, height*0.25),
        (width*0.75, height*0.5),
        (width*0.5, height*0.75)
    )

for dPoint in getDiamondpoints():
    playBackPath(getPathToPoint(dPoint))
"""