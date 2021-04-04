class Decision:
    def __init__(self, racingData):
        super(Decision, self).__init__()
        self.racingData = racingData
        self.pitDecision = {}
        self.gpTitle = racingData.gpTitle
        self.compoundStrategy = {}

    def __str__(self):
        decision_str = f"Lance, the pit strategy for this {self.gpTitle} is the following: {self.pitDecision} \n"\
                       f"We will start on a fresh set of {self.compoundStrategy.get(1)}"
        return decision_str
