import unittest
from decision import Decision
from racingdata import RacingData


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)

    try:
        len(Decision.compoundStrategy) == RacingData.totalLaps

    except: 'Not enough laps'


if __name__ == '__main__':
    unittest.main()
