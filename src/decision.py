from solution import Solution


class Decision(Solution):
    def __init__(self, racingdata):
        super(Decision, self).__init__()
        self.racingData = racingdata
        self.pitDecision = {}
        self.gpTitle = racingdata.gpTitle
        self.compoundStrategy = {}
        self.totalTime: int = 0
        self.lapTimes = [[], [], []]

    def __str__(self):
        pitlaps = sorted(list(self.pitDecision.keys()))
        if len(pitlaps) == 1:
            decision_str = f"\nLance, the pit strategy for this {self.gpTitle} " \
                           f"is the following:\nFirst pit is at lap {pitlaps[0]} " \
                           f"for a {self.compoundStrategy.get(pitlaps[0]+1)[0]} compound.\n"\
                           f"We will start on a fresh set of {self.compoundStrategy.get(1)[0]} \n\n"\
                           f"Here is the complete scenario: {dict(sorted(self.compoundStrategy.items()))}"
            return decision_str
        elif len(pitlaps) == 2:
            decision_str = f"\nLance, the pit strategy for this {self.gpTitle} " \
                           f"is the following:\nFirst pit is at lap {pitlaps[0]} " \
                           f"for a {self.compoundStrategy.get(pitlaps[0] + 1)[0]} compound.\n" \
                           f"Second pit is at lap {pitlaps[1]} " \
                           f"for a {self.compoundStrategy.get(pitlaps[1] + 1)[0]} compound.\n" \
                           f"We will start on a fresh set of {self.compoundStrategy.get(1)[0]}. \n\n" \
                           f"Here is the complete scenario: {dict(sorted(self.compoundStrategy.items()))}\n\n" \
                           f"It should take {self.totalTime} seconds."

            return decision_str

    def validate(self):
        pass

    def evaluate(self):
        compounds = self.racingData.compounds
        for lap in self.compoundStrategy.keys():
            tyre = self.compoundStrategy[lap][0]
            usage = self.compoundStrategy[lap][1]
            for k, v in compounds.items():
                if v == tyre:
                    laptime = self.lapTimes[k][usage-1]
                    self.totalTime += laptime
        self.totalTime += len(sorted(list(self.pitDecision.keys()))) * self.racingData.pitTime
