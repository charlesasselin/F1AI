from solution import Solution


class Decision(Solution):
    def __init__(self, racingdata):
        super(Decision, self).__init__()
        self.racingData = racingdata
        self.pitDecision = {}
        self.gpTitle = racingdata.gpTitle
        self.compoundStrategy = {}

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
                           f"Here is the complete scenario: {dict(sorted(self.compoundStrategy.items()))}"

            return decision_str
