from pyautogui import position, size, moveTo
import pyautogui
from time import perf_counter, sleep
from ast import literal_eval as make_tuple

import copy

screenSize = size()

#screen is divided into 8x4 'Sections'
#5-10 mouse movements representing each permutation of one section to another are recorded
heightSections = 3
widthSections = 3

verticalSectionLength = screenSize[1]/heightSections
horizontalSectionLength = screenSize[0]/widthSections

logFileName = r'MousePaths.txt' 

pyautogui.FAILSAFE = False



class mousePath:
    startPoint = (0,0)
    endPoint = (0,0)
    startSection = (0,0)
    endSection = (0,0)

    pointList = list()
    timeList = list()
    
    def __init__(self):
        self.pointList = list()
        self.timeList = list()

    def setStartPoint(self):
        self.startPoint = position()
        self.startSection = getSection(self.startPoint)

    def setEndPoint(self):
        self.endPoint = position()
        self.endSection = getSection(self.endPoint)



def getNewMousePath():
    newpath = mousePath()
    newpath.setStartPoint()
    #path recording starts when mouse moves, ends when mouse is motionless for 2 seconds.

    print("Waiting for motion...")
    waitForMotion()
    print("Recording...")
    newpath.pointList, newpath.timeList = buildPathList()
    newpath.setEndPoint()
    print("Recording complete.")

    return newpath

def waitForMotion():
    prevTime = perf_counter()
    prevPos = position()
    vel = 0
    while vel == 0:
        sleep(0.05)
        currPos = position()
        currTime = perf_counter()
        deltaTime = currTime - prevTime
        deltaPos = manhattanDist(prevPos, currPos)
        prevPos = currPos
        if deltaTime != 0:
            vel = deltaPos/deltaTime
    
def buildPathList():
    motionlessTime = 0
    moving = True
    initTime = perf_counter()
    stopTime = initTime
    prevTime = perf_counter()
    prevPos = position()
    velocity = 0
    prevVel = 0
    acc = 0

    pointList = list()
    timeList = list()
    while motionlessTime < 2:
        currPos = position()
        currTime = perf_counter()
        deltaTime = currTime - prevTime
        deltaPos = manhattanDist(prevPos, currPos)
        prevPos = currPos
        prevRecTime = currTime

        if deltaTime != 0:
            velocity = deltaPos/deltaTime
        
        acc = ( velocity - prevVel ) / deltaTime
        prevVel = velocity


        justStopped = moving and velocity == 0 and acc == 0

        
        if velocity !=0 or acc != 0:
            if not moving:
                moving=True
                pointList.append(position())
                timeList.append(motionlessTime)
            pointList.append(position())
            timeList.append(currTime - prevRecTime)
            prevRecTime = currTime

        if not moving:
            motionlessTime = perf_counter() - stopTime

        if justStopped:
            moving = False
            stopTime = perf_counter()

    return pointList, timeList


def getSection(position):
    width = int(position[0]/horizontalSectionLength)
    height = int(position[1]/verticalSectionLength)
    return(width, height)

def targetDiff(start, end):
    return (end[0]-start[0], end[1]-start[1])

def dist(start, end):
    diff = targetDiff(start, end)
    square = (diff[0]**2, diff[1]**2)
    distSum = sum(square)
    return(distSum**0.5)

def manhattanDist(start, end):
    return abs(end[0] - start[0]) + abs(end[1] - start[1])

def playBackPath(mousePath):
    moveTo(mousePath.startPoint)
    for index in range(len(mousePath.pointList) - 1):
        point = mousePath.pointList[index]
        time = mousePath.timeList[index]
        pyautogui.platformModule._moveTo(point[0], point[1])
        sleep(time)

def logPathToFile(file, path):
    file.write(str(path.startSection) + "#")
    file.write(str(path.endSection) + "#")
    file.write(str(path.startPoint) + "#")
    for index in range(len(path.pointList) - 1):
        file.write(str(path.pointList[index]) + "#")
        file.write("{0:.4f}".format(path.timeList[index]) + "#")
    file.write(str(path.endPoint) + "\n")

def getPathFromFile(numPath, pathFile):
    pathString = getNthLineFromFile(numPath, pathFile)
    if pathString == None:
        return mousePath()
    return getMousePathfromString(pathString)

def getPathDataFromFile(numPath, pathFile):
    pathString = getNthLineFromFile(numPath, pathFile)
    if pathString == None:
        return mousePath()
    return getMousePathfromString(pathString)

def getMousePathSectionDataFromString(pathString):
    pathList = pathString.split('#')
    pathObj = mousePath()
    pathObj.startSection = make_tuple(pathList[0])
    pathObj.endSection = make_tuple(pathList[1])
    pathObj.startPoint = make_tuple(pathList[2])
    pathObj.endPoint = make_tuple(pathList[-1])
    return pathObj

def getMousePathfromString(pathString):
    pathList = pathString.split('#')
    pathObj = mousePath()
    pathObj.startSection = make_tuple(pathList[0])
    pathObj.endSection = make_tuple(pathList[1])
    pathObj.startPoint = make_tuple(pathList[2])
    pathObj.endPoint = make_tuple(pathList[-1])
    pathList = pathList[3:-1]

    for element in pathList:
        if tryToConvert(element , float):
            pathObj.timeList.append(float(element))
        else:
            pathObj.pointList.append(make_tuple(element))
    return pathObj

def tryToConvert(item, convertType):
    try:
        isinstance(convertType(item), convertType)
    except:
        return False
    return True

def getNthLineFromFile(n, lineFile):
    lineFile.seek(0)
    for i, line in enumerate(lineFile):
        if i == n:
            return line
    return None

#Basic testing

logPaths = 3

"""
with open(logFileName, 'w+') as logFile:
    for x in range(logPaths):
        print("Logging ", x+1, " of ", logPaths)
        newPath = getNewMousePath()
        print("Writing ", len(newPath.pointList), " points to file.")
        logPathToFile(logFile, newPath)

print("Playing back recorded paths now.")
sleep(1)
with open(logFileName, 'r') as logFile:
    for x in range(logPaths):
        retrievedPath = getPathFromFile(x, logFile)
        print("Playing back path ", x+1, " starting at ", retrievedPath.startPoint, " and ending at ", retrievedPath.endPoint, " in ", len(retrievedPath.pointList), " moves." )
        sleep(1)
        playBackPath(retrievedPath)

"""
