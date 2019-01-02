from pyautogui import position, size, moveTo
from time import perf_counter, sleep
from math import sin, cos, pi

def targetDiff(start, end):
    return (end[0]-start[0], end[1]-start[1])


def dist(start, end):
    diff = targetDiff(start, end)
    square = (diff[0]**2, diff[1]**2)
    distSum = sum(square)
    return(distSum**0.5)

def logMetrics():
    prevTime = perf_counter()
    prevPos = position()
    vel = 0
    prevVel = 0
    acc = 0
    prevAcc = 0
    jerk = 0
    startTime = perf_counter()
    print("Beginning to log.")
    with open("mousedata.csv", "w+") as datafile:
        curTime = perf_counter()
        while curTime - startTime < 10:
            curTime = perf_counter()
            curPos = position()
            deltaTime = curTime - prevTime
            deltaPos = dist(prevPos, curPos)
            
            if deltaTime > 0.0:
                vel = deltaPos/deltaTime
                acc = (vel-prevVel)/deltaTime
                jerk = (acc-prevAcc)/deltaTime

            prevPos = curPos
            prevVel = vel
            prevAcc = acc
            if(vel != 0.0 and acc != 0.0 and jerk != 0.0):
                prevTime = curTime
                datafile.write(str(vel) + ", " + str(acc) + ", " + str(jerk) + '\n')


def printMetrics():
    prevTime = perf_counter()
    prevPos = position()
    vel = 0
    prevVel = 0
    acc = 0
    prevAcc = 0
    jerk = 0
    startTime = perf_counter()
    curTime = perf_counter()
    while True:
        curTime = perf_counter()
        curPos = position()
        deltaTime = curTime - prevTime
        deltaPos = dist(prevPos, curPos)
        
        if deltaTime > 0.0:
            vel = deltaPos/deltaTime
            acc = (vel-prevVel)/deltaTime
            jerk = (acc-prevAcc)/deltaTime

        prevPos = curPos
        prevVel = vel
        prevAcc = acc
        if(vel != 0.0 and acc != 0.0):
            prevTime = curTime
            print(str(vel) + ", " + str(acc) + ", " + str(jerk) + '\n')
        sleep(0.01) #10 ms to prevent wild derivatives due to time resolution being much higher than position resolution.

"""          
print("ready to begin logging. Will begin logging in 5 seconds")
sleep(5)
logMetrics()
print("logging complete.")
"""

printMetrics()