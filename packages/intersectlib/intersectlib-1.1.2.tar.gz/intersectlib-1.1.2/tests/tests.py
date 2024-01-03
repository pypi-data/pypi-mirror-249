import unittest
import sys

sys.path.insert(1, 'C://Users//ducke//PycharmProjects//intersectlib//intersectlib')

from intersectlib import find_remainders
from intersectlib import find_intersection
from intersectlib import find_intersection_and_remainders
from intersectlib import transform_intersection
from intersectlib import InvalidTupleError
from intersectlib import InvalidRangeError
from intersectlib import InvalidArgumentError


class TestFile(unittest.TestCase):
    def testErrors(self):
        self.assertRaises(InvalidTupleError, find_intersection, (3, 1), (5, 6))
        self.assertRaises(InvalidTupleError, find_intersection, (1, 2, 3), (8, 9))
        self.assertRaises(InvalidTupleError, find_intersection, (1, 'p'), (2, 8))

        self.assertRaises(InvalidRangeError, find_intersection, range(10, 9), range(3, 4))

        self.assertRaises(InvalidArgumentError, find_intersection, 'p', (9, 10))
        self.assertRaises(InvalidArgumentError, find_intersection, [], (9, 10))
        self.assertRaises(InvalidArgumentError, find_intersection, range, (9, 10))

    def testIntersection(self):
        # 1.1
        result = find_intersection((2, 10), (2, 5))
        self.assertEqual(result, (2, 5))

        result = find_intersection((1, 1000), (1, 200))
        self.assertEqual(result, (1, 200))

        result = find_intersection((8000, 78909), (8000, 10000))
        self.assertEqual(result, (8000, 10000))

        result = find_intersection((-20, -10), (-20, -18))
        self.assertEqual(result, (-20, -18))

        # 1.2

        result = find_intersection((2, 20), (8, 12))
        self.assertEqual(result, (8, 12))

        result = find_intersection((400, 1000), (800, 900))
        self.assertEqual(result, (800, 900))

        result = find_intersection((1, 9999), (3, 6796))
        self.assertEqual(result, (3, 6796))

        # 1.3
        result = find_intersection((1, 20), (10, 20))
        self.assertEqual(result, (10, 20))

        result = find_intersection((200, 1000), (500, 1000))
        self.assertEqual(result, (500, 1000))

        result = find_intersection((809, 5678), (1000, 5678))
        self.assertEqual(result, (1000, 5678))

        # 2
        result = find_intersection((5, 10), (1, 15))
        self.assertEqual(result, (5, 10))

        result = find_intersection((100, 200), (-200, 500))
        self.assertEqual(result, (100, 200))

        result = find_intersection((-1000, -500), (-1500, 0))
        self.assertEqual(result, (-1000, -500))

        # 3
        result = find_intersection((2, 10), (2, 20))
        self.assertEqual(result, (2, 10))

        result = find_intersection((-100, -50), (-100, 0))
        self.assertEqual(result, (-100, -50))

        result = find_intersection((-100, 100), (-100, 300))
        self.assertEqual(result, (-100, 100))

        # 4
        result = find_intersection((8, 10), (0, 10))
        self.assertEqual(result, (8, 10))

        result = find_intersection((300, 500), (100, 500))
        self.assertEqual(result, (300, 500))

        result = find_intersection((-400, -300), (-500, -300))
        self.assertEqual(result, (-400, -300))

        # 5
        result = find_intersection((2, 10), (5, 20))
        self.assertEqual(result, (5, 10))

        result = find_intersection((100, 500), (300, 1000))
        self.assertEqual(result, (300, 500))

        result = find_intersection((-300, 0), (-200, 500))
        self.assertEqual(result, (-200, 0))

        # 6
        result = find_intersection((8, 10), (2, 9))
        self.assertEqual(result, (8, 9))

        result = find_intersection((100, 500), (50, 300))
        self.assertEqual(result, (100, 300))

        result = find_intersection((-50, 0), (-100, -20))
        self.assertEqual(result, (-50, -20))

        # 7
        result = find_intersection((2, 10), (2, 10))
        self.assertEqual(result, (2, 10))

        result = find_intersection((-100, 250), (-100, 250))
        self.assertEqual(result, (-100, 250))

        result = find_intersection((-100, -50), (-100, -50))
        self.assertEqual(result, (-100, -50))

        # 8
        result = find_intersection((-500, -100), (100, 500))
        self.assertEqual(result, None)

        result = find_intersection((-1000, -400), (-350, -10))
        self.assertEqual(result, None)

        result = find_intersection((500, 1000), (1500, 2000))
        self.assertEqual(result, None)

    def testRemainders(self):
        # 1.1
        result = find_remainders((2, 10), (2, 5))
        self.assertEqual(result, [(5, 10)])

        result = find_remainders((1, 1000), (1, 200))
        self.assertEqual(result, [(200, 1000)])

        result = find_remainders((8000, 78909), (8000, 10000))
        self.assertEqual(result, [(10000, 78909)])

        result = find_remainders((-20, -10), (-20, -18))
        self.assertEqual(result, [(-18, -10)])

        # 1.2

        result = find_remainders((2, 20), (8, 12))
        self.assertEqual(result, [(2, 8), (12, 20)])

        result = find_remainders((400, 1000), (800, 900))
        self.assertEqual(result, [(400, 800), (900, 1000)])

        result = find_remainders((1, 9999), (3, 6796))
        self.assertEqual(result, [(1, 3), (6796, 9999)])

        # 1.3
        result = find_remainders((1, 20), (10, 20))
        self.assertEqual(result, [(1, 10)])

        result = find_remainders((200, 1000), (500, 1000))
        self.assertEqual(result, [(200, 500)])

        result = find_remainders((809, 5678), (1000, 5678))
        self.assertEqual(result, [(809, 1000)])

        # 2
        result = find_remainders((5, 10), (1, 15))
        self.assertEqual(result, [])

        result = find_remainders((100, 200), (-200, 500))
        self.assertEqual(result, [])

        result = find_remainders((-1000, -500), (-1500, 0))
        self.assertEqual(result, [])

        # 3
        result = find_remainders((2, 10), (2, 20))
        self.assertEqual(result, [])

        result = find_remainders((-100, -50), (-100, 0))
        self.assertEqual(result, [])

        result = find_remainders((-100, 100), (-100, 300))
        self.assertEqual(result, [])

        # 4
        result = find_remainders((8, 10), (0, 10))
        self.assertEqual(result, [])

        result = find_remainders((300, 500), (100, 500))
        self.assertEqual(result, [])

        result = find_remainders((-400, -300), (-500, -300))
        self.assertEqual(result, [])

        # 5
        result = find_remainders((2, 10), (5, 20))
        self.assertEqual(result, [(2, 5)])

        result = find_remainders((100, 500), (300, 1000))
        self.assertEqual(result, [(100, 300)])

        result = find_remainders((-300, 0), (-200, 500))
        self.assertEqual(result, [(-300, -200)])

        # 6
        result = find_remainders((8, 10), (2, 9))
        self.assertEqual(result, [(9, 10)])

        result = find_remainders((100, 500), (50, 300))
        self.assertEqual(result, [(300, 500)])

        result = find_remainders((-50, 0), (-100, -20))
        self.assertEqual(result, [(-20, 0)])

        # 7
        result = find_remainders((2, 10), (2, 10))
        self.assertEqual(result, [])

        result = find_remainders((-100, 250), (-100, 250))
        self.assertEqual(result, [])

        result = find_remainders((-100, -50), (-100, -50))
        self.assertEqual(result, [])

        # 8
        result = find_remainders((-500, -100), (100, 500))
        self.assertEqual(result, [(-500, -100)])

        result = find_remainders((-1000, -400), (-350, -10))
        self.assertEqual(result, [(-1000, -400)])

        result = find_remainders((500, 1000), (1500, 2000))
        self.assertEqual(result, [(500, 1000)])
