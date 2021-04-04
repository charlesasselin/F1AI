from solution import Solution


class Decision(Solution):
    def __init__(self, racingData):
        super(Decision, self).__init__()
        self.racingData = racingData
        self.pitDecision = {}
        self.gpTitle = racingData.gpTitle
        self.compoundStrategy = {}

    def __str__(self):
        decision_str = f"Lance, the pit strategy for this {self.gpTitle} is the following: {self.pitDecision} \n"\
                       f"We will start on a fresh set of {self.compoundStrategy.get(1)} \n"\
                       f"Here is the matrix: {dict(sorted(self.compoundStrategy.items()))}"
        return decision_str