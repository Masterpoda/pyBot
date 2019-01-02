#this code will be used to store and track the creation of paths 
#that represent all forms of sectional transfer (i.e. all possible
#moves from one section to another, e.g. up 2, left 3, etc.)

import pathLogger

#how many paths need to be recorded for each transfer.
pathsPerTransfer = 5

#list of all possible section moves
sectionTransferTable = list()

#number of recorded section move paths
recordedSectionTransfer = dict()

#initialize records of transfers
for x in range(-pathLogger.widthSections, pathLogger.widthSections + 1):
    for y in range(-pathLogger.heightSections, pathLogger.heightSections + 1):
        sectionTransferTable.append((x,y))

for move in sectionTransferTable:
    recordedSectionMoves[move] = 0

print("we will create ", pathsPerTransfer, " paths for ", pathLogger.heightSections*pathLogger.widthSections*4, "transfers")