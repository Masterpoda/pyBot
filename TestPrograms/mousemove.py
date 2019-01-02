from pyautogui import position, size, moveTo, moveRel
from time import sleep, perf_counter
from math import sin, cos, pi
import pyautogui

screenSize = size()
screenCenter = (int(screenSize[0]/2), int(screenSize[1]/2))

degToRad = pi/180.0

# Any duration less than this is rounded to 0.0 to instantly move the mouse.
pyautogui.MINIMUM_DURATION = 0  # Default: 0.1
# Minimal number of seconds to sleep between mouse moves.
pyautogui.MINIMUM_SLEEP = 0 # Default: 0.05
# The number of seconds to pause after EVERY public function call.
pyautogui.PAUSE = 0  # Default: 0.1

#traces a path in uniform time
def traceTargetList(targets, traceTime = 1):
    targetTime = traceTime/len(targets)
    for target in targets:
        moveTo(target[0], target[1] )

def traceCircle(center, radius, startDegrees = 0, resDegrees = 1):
    tList = list()
    for degree in range(0, 360, resDegrees):
        xTarget = radius*cos((degree + startDegrees)*degToRad) + center[0]
        yTarget = radius*sin((degree + startDegrees)*degToRad) + center[1]
        tList.append((xTarget, yTarget))
    traceTargetList(tList)

#move to center of screen
moveTo(screenCenter[0], screenCenter[1], 1)

#traceCircle(screenCenter, 300, 90, 3)

numMoves = 100
print(1/numMoves)
before = perf_counter()
for x in range(numMoves):
        #should complete in 1 second
        #moveTo(screenCenter[0] + 500*((x+1)/numMoves), screenCenter[1], 1/numMoves)
        pyautogui.platformModule._moveTo(int(screenCenter[0] + 500*((x+1)/numMoves)), int(screenCenter[1]))
        sleep(1.0/numMoves)
after = perf_counter()

print("Total Time: ", after - before, " seconds.")
moveTo(screenCenter[0], screenCenter[1], 0)

before = perf_counter()
moveTo(screenCenter[0] + 500, screenCenter[1], 1)
after = perf_counter()

print("Total Time: ", after - before, " seconds.")