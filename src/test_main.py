import unittest
from decision import Decision as decision

class MyTestCase(unittest.TestCase):
    def __init__(self, racing_inst):
        super(MyTestCase, self).__init__()
        self.racing_inst = racing_inst

    def test_data(self):
        self.assertIsInstance(self.racing_inst.lapData, list)
        self.assertIsInstance(self.racing_inst.tyreUsageData, list)
        count_laps = 0
        for i in range(len(self.racing_inst.lapData)):
            count_laps += len(self.racing_inst.lapData[i])
        self.assertGreater(count_laps, self.racing_inst.totalLaps)

    def test_appendlists(self):
        it = iter(self.racing_inst.futureLapData)
        the_len = len(next(it))
        maxlen = max(len(l) for l in self.racing_inst.lapData)
        for l in it:
            self.assertEqual(the_len, maxlen)
        for i in range(len(self.racing_inst.futureLapData)):
            self.assertEqual(len(self.racing_inst.futureTyreUsageData), len(self.racing_inst.futureLapData))
            self.assertEqual(len(self.racing_inst.futureTyreUsageData[i]), len(self.racing_inst.futureLapData[i]))

    def test_trendlinedata(self):
        for i in range(len(self.racing_inst.lapData)):
            self.assertEqual(len(self.racing_inst.tyreUsageData[i]), len(self.racing_inst.lapData[i]))
        self.assertIsInstance(self.racing_inst.trendlinedata(), dict)

    def test_decision(self):
        self.assertGreaterEqual(len(sorted(list(decision(self.racing_inst).pitDecision.keys()))), 1)        # make sure that we pit at least once
        self.assertGreater(decision(self.racing_inst).totalTime, 0)
        self.assertEqual(len(decision(self.racing_inst).compoundStrategy), self.racing_inst.totalLaps)

if __name__ == '__main__':
    unittest.main()
