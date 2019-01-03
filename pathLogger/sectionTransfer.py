#this code will be used to store and track the creation of paths 
#that represent all forms of sectional transfer (i.e. all possible
#moves from one section to another, e.g. up 2, left 3, etc.)

import pathLogger
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
    return (
        path.endSection[0] - path.startSection[0],
        path.endSection[1] - path.startSection[1]
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

def addNewPaths():
    print("we will create ", pathsPerTransfer, " paths for ", len(sectionTransferList), "transfers")
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

print("Populating...")
with open(pathLogger.logFileName, 'r') as pathfile:
            populateUsingFile(pathfile)

print("Playing 0,0 transfer")
with open(pathLogger.logFileName, 'r') as pathfile:
    playbackTransferRandom((0,0), pathfile)

sleep(1)

print("Playing 1,0 transfer")
with open(pathLogger.logFileName, 'r') as pathfile:
    playbackTransferRandom((1,0), pathfile)

sleep(1)
