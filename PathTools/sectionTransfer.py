#this code will be used to store and track the creation of paths 
#that represent all forms of sectional transfer (i.e. all possible
#moves from one section to another, e.g. up 2, left 3, etc.)

import pathLogger
import os.path
from random import choice as randomChoice
from time import sleep

#how many paths need to be recorded for each transfer.
pathsPerTransfer = 5

#List of all possible section transfers
sectionTransferList = list()

#lists containing lines where a desired transfer can be found
recordedSectionTransfer = dict()

#used to denote no transfer
nullTransfer = (-10000, -10000)

#initialize records of transfers
for x in range(-(pathLogger.widthSections - 1), pathLogger.widthSections):
    for y in range(-(pathLogger.heightSections - 1), pathLogger.heightSections):
        sectionTransferList.append((x,y))
        recordedSectionTransfer[(x,y)] = list()

def populateUsingFile(fileObj):
    pathNum = 0
    currPath = pathLogger.getPathDataFromFile(pathNum, fileObj)
    while len(currPath.pointList) != 0:
        if pathNum not in recordedSectionTransfer[getTransferFromPath(currPath)]:
            recordedSectionTransfer[getTransferFromPath(currPath)].append(pathNum)
        pathNum +=1
        currPath = pathLogger.getPathFromFile(pathNum, fileObj)

def getTransferFromPath(path):
    return getTransferFromSections(
        path.startSection,
        path.endSection
    )

def getTransferFromSections(start, end):
    return (
        end[0] - start[0],
        end[1] - start[1]
    )

def getTransferFromPoints(startPoint, endPoint):
    return getTransferFromSections(
        pathLogger.getSection(startPoint), 
        pathLogger.getSection(endPoint)
        )

def getNumDiscoveredPaths():
    pathCount = 0
    for transfer, fileIndexList in recordedSectionTransfer.items():
        pathCount += len(fileIndexList)
    return pathCount

def getNextNeededTransfer():
    for transfer, fileIndexList in recordedSectionTransfer.items():
        if len(fileIndexList) < pathsPerTransfer:
            return transfer
    return nullTransfer

def playbackTransferRandom(transfer, pathFile):
    transferList = recordedSectionTransfer[transfer]
    pathToPlayback = pathLogger.getPathFromFile(randomChoice(transferList), pathFile)
    pathLogger.playBackPath(pathToPlayback)

def getRandomPathFromTransfer(transfer):
    transferList = recordedSectionTransfer[transfer]
    with open(pathLogger.logFileName, 'r') as pathFile:
        return pathLogger.getPathFromFile(randomChoice(transferList), pathFile)


def addNewPaths():
    print("we must create ", pathsPerTransfer, " paths for ", len(sectionTransferList), " transfers")
    #populate transfer records from the mousPaths file
    with open(pathLogger.logFileName, 'r') as pathfile:
        populateUsingFile(pathfile)

    print("Discovered ", getNumDiscoveredPaths(), " paths.")

    nexTran = getNextNeededTransfer()
    while nexTran != nullTransfer:
        print("Next required transfer is: ", getNextNeededTransfer())
        with open(pathLogger.logFileName, 'a') as pathfile:
            newPath = pathLogger.getNewMousePath()
            print("Path recorded transfer: ", getTransferFromPath(newPath))
            pathLogger.logPathToFile(pathfile, newPath)
            nexTran = getNextNeededTransfer()
        
        with open(pathLogger.logFileName, 'r') as pathfile:
            populateUsingFile(pathfile)
        
        nexTran = getNextNeededTransfer()

if os.path.isfile(pathLogger.logFileName):
    with open(pathLogger.logFileName, 'r') as pathfile:
            populateUsingFile(pathfile)
else:
    with open(pathLogger.logFileName, "w+") as pathfile:
            populateUsingFile(pathfile)

if getNextNeededTransfer() != nullTransfer:
    addNewPaths()
