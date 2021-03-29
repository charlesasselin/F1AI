class Decision:
    def __init__(self, racingData):
        super(Decision, self).__init__()
        self.racingData = racingData
        self.pitDecision = {}
        self.gpTitle = racingData.gpTitle

    def __str__(self):
        decision_str = f"Lance, the pit strategy for this {self.gpTitle} is the following: {self.pitDecision}"
        return decision_str
