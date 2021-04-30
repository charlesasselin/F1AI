import unittest
import yaml
from racingdata import RacingData
from ampl_solver import AmplSolver
import sys

class MyTestCase(unittest.TestCase):
    def setUp(self):
        with open('BahrainRecordData.yaml', 'r') as handle:
            self.data = yaml.load(handle, Loader=yaml.FullLoader)
        self.racing_inst = RacingData(self.data)
        RacingData.appendlists(self.racing_inst)
        self.racingsol = AmplSolver().solve(self.racing_inst)

        with open('FalseBahrainRecordData.yaml', 'r') as handle:
            self.falseData = yaml.load(handle, Loader=yaml.FullLoader)
        self.false_racing_inst = RacingData(self.falseData)
        RacingData.appendlists(self.false_racing_inst)
        self.falseracingsol = AmplSolver().solve(self.false_racing_inst)

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
        self.racingsol.evaluate()
        self.assertGreaterEqual(len(sorted(list(self.racingsol.pitDecision.keys()))), 1)        # make sure that we pit at least once
        self.assertGreater(self.racingsol.totalTime, 0)
        self.assertEqual(len(self.racingsol.compoundStrategy), self.racing_inst.totalLaps)

    def test_validate(self):
        self.assertTrue(self.racingsol.validate())
        self.assertFalse(self.falseracingsol.validate())

    def test_evaluate(self):
        self.assertTrue(self.racingsol.evaluate() >= 0)
        self.assertTrue(self.falseracingsol.evaluate() == sys.float_info.max)
        self.assertIsInstance(self.racingsol.evaluate(), float)
        self.assertIsInstance(self.falseracingsol.evaluate(), float)

if __name__ == '__main__':
    unittest.main()
