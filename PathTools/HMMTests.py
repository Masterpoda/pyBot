import HumanMouseMovement as HMM
from pathLogger import mousePath
from pyautogui import position, size
import unittest
import copy

class PointMathTests(unittest.TestCase):

    def test_PointDiff(self):
        point1 = (10, 5)
        point2 = (2, -1)
        expected = (8, 6)

        actual = HMM.pointDiff(point1, point2)

        self.assertEqual(actual, expected)

    def test_PythagoreanDistance(self):
        point1 = (-1, -1)
        point2 = (2, 3)
        expected = 5.0

        actual = HMM.pythagoranDist(point1, point2)

        self.assertEqual(actual, expected)

    def test_PointSum(self):
        point1 = (10, 5)
        point2 = (2, -1)
        expected = (12, 4)

        actual = HMM.pointSum(point1, point2)

        self.assertEqual(actual, expected)

    def test_ApplyOffsetToPath(self):
        offset = (-1, 2)
        path = HMM.getPathFromTransfer((0,0))
        pathcopy = copy.deepcopy(path)

        HMM.applyOffsetToPath(path, offset)

        self.assertEqual(path.startPoint, HMM.pointSum(pathcopy.startPoint, offset))
        for index in range(len(path.pointList)):
            self.assertEqual(path.pointList[index], (pathcopy.pointList[index][0] + offset[0], pathcopy.pointList[index][1] + offset[1]))
        self.assertEqual(path.endPoint, HMM.pointSum(pathcopy.endPoint, offset))

    
    def test_ApplyShearTransformOrigin(self):
        testPath = mousePath()
        testPath.startPoint = (0,0)
        testPath.endPoint = (12,27)
        goalPoint = (30, 42)
        expected = goalPoint

        actual = HMM.shearPathToPoint(testPath, goalPoint).endPoint

        self.assertEqual(actual, expected)

    def test_MovePathToStartPoint(self):
        testPath = HMM.getPathFromTransfer((1,1))
        screenSize = size()
        newStartPoint = (int(screenSize[0]/2), int(screenSize[1]/2))
        expected = newStartPoint

        actual = HMM.MovePathToStartPoint(testPath, newStartPoint).startPoint

        self.assertEqual(actual, expected)

    def test_GetPathToPoint(self):
        goalPoint = (100, 100)
        expectedEndPoint = goalPoint
        
        
        goalPath = HMM.getPathToPoint(goalPoint)
        expectedStartPoint = position()
        actualStartPoint = goalPath.startPoint
        actualEndPoint = goalPath.endPoint

        self.assertEqual(actualStartPoint, expectedStartPoint)
        self.assertEqual(actualEndPoint, expectedEndPoint)




unittest.main()