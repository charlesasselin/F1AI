from solution import Solution
import record
import sys


class Decision(Solution):
    def __init__(self, racingdata):
        super(Decision, self).__init__()
        self.racingData = racingdata
        self.pitDecision = {}
        self.gpTitle = racingdata.gpTitle
        self.compoundStrategy = {}
        self.totalTime: int = 0
        self.lapTimes = [[], [], []]
        self.fuel = 0
        self.countedlaps = 0

    def __str__(self):
        pitlaps = sorted(list(self.pitDecision.keys()))
        decision_str = f"\nLance, the pit strategy for this {self.gpTitle} " \
                       f"is the following:\nFirst pit is at lap {pitlaps[0]} " \
                       f"for a {self.compoundStrategy.get(pitlaps[0] + 1)[0]} compound.\n"

        if len(pitlaps) == 2:
            add = f"Second pit is at lap {pitlaps[1]} " \
                  f"for a {self.compoundStrategy.get(pitlaps[1] + 1)[0]} compound.\n"
            decision_str += add

        add = f"We will start on a fresh set of {self.compoundStrategy.get(1)[0]} \n\n" \
              f"It should take {record.LapTime(self.totalTime)} minutes.\n\n"
        decision_str += add

        if self.fuel != 0:
            add = f"We should fill {self.fuel}L of fuel in the tank so that we end with a surplus of 0.5L"
            decision_str += add
        return decision_str

    def validate(self):
    # Vérifier que la stratégie est calculée en fonction du nombre de tours dans le grand prix
        for lap in self.compoundStrategy.keys():
            usage = self.compoundStrategy[lap][1]
            for k, v in self.racingData.compounds.items():
                if self.lapTimes[k][usage - 1] <= 0:
                    return False
        if len(self.compoundStrategy) != self.racingData.totalLaps:
            return False
        for tyre in self.racingData.lapData:
            self.countedlaps += len(tyre)
        if self.countedlaps <= self.racingData.totalLaps:
            return False
        return True


    def evaluate(self):
    # Calculer la fonction objectif si la solution est validée
        if self.validate() is True:
            for lap in self.compoundStrategy.keys():
                tyre = self.compoundStrategy[lap][0]
                usage = self.compoundStrategy[lap][1]
                for k, v in self.racingData.compounds.items():
                    if v == tyre:
                        laptime = self.lapTimes[k][usage-1]
                        self.totalTime += laptime
            self.totalTime += len(sorted(list(self.pitDecision.keys()))) * self.racingData.pitTime
        else:
            self.totalTime = sys.float_info.max
        return self.totalTime
