from solution import Solution


class Decision(Solution):
    def __init__(self, racingData):
        super(Decision, self).__init__()
        self.racingData = racingData
        self.pitDecision = {}
        self.gpTitle = racingData.gpTitle
        self.compoundStrategy = {}

    def __str__(self):
        pitLaps = list(self.pitDecision.keys())
        decision_str = f"\nLance, the pit strategy for this {self.gpTitle}" \
                       f"is the following: first pit is at lap {pitLaps[0]} " \
                       f"on a {self.compoundStrategy.get(pitLaps[0]+1)[0]} compound\n"\
                       f"We will start on a fresh set of {self.compoundStrategy.get(1)[0]} \n\n"\
                       f"Here is the complete scenario: {dict(sorted(self.compoundStrategy.items()))}"
        return decision_str