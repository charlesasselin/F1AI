"""
Listen to telemetry packets and print them to standard output
"""
from racingdata import RacingData
from ampl_solver import AmplSolver
from trendlinesolver import AmplTrendlineSolver
import json
import yaml
from test_main import MyTestCase as test
from fullsolver import AmplFullSolver

data = {"laptimes": [[69.165, 69.712, 70.309, 70.148, 69.352, 70.695, 70.408, 70.485, 70.107, 69.881, 70.344, 69.786, 70.267, 70.335, 70.373, 70.071, 70.698, 70.109, 71.897],
                     [67.964, 67.921, 67.426, 68.536, 68.548, 68.428, 69.302, 68.015, 68.522, 68.568, 68.729, 68.234, 68.158, 68.113, 68.331, 68.334, 69.023, 68.638, 67.576],
                     [70.127, 70.419, 70.045, 69.766, 69.699, 69.728, 70.651, 69.774, 70.070, 70.410, 70.840, 69.795, 70.940, 70.152, 70.002, 69.644, 70.472, 70.603, 71.272]],
        "tyreusage": [[0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90],
                      [0, 0.04, 0.08, 0.12, 0.16, 0.20, 0.24, 0.28, 0.32, 0.36, 0.40, 0.44, 0.48, 0.52, 0.56, 0.60, 0.64, 0.68, 0.72],
                      [0, 0.03, 0.06, 0.09, 0.12, 0.15, 0.18, 0.21, 0.24, 0.27, 0.30, 0.33, 0.36, 0.39, 0.42, 0.45, 0.48, 0.51, 0.54]],
        "totallaps": 50,
        "gptitle": "Imola Grand Prix",
        "compounds": {int(0): "Soft", int(1): "Medium", int(2): "Hard"}}

# with open('recordData', 'rb') as handle:
#     data = pickle.load(handle)

class Analyzer:
    def __init__(self, handle, solver='trendline'):
        self.handle = handle
        self.data = {}
        self.solver = solver
        self.racingsol = None

    def __str__(self):
        return str(self.racingsol)

    def analyze(self):
        with open(self.handle, 'r') as handle:
            self.data = yaml.load(handle, Loader=yaml.FullLoader)
        racing_inst = RacingData(self.data)
        RacingData.appendlists(racing_inst)
        test(racing_inst)
        if self.solver == 'Trendline Solver':
            self.racingsol = AmplTrendlineSolver().solve(racing_inst)
            self.racingsol.evaluate()
        elif self.solver == 'Basic Solver':
            self.racingsol = AmplSolver().solve(racing_inst)
            self.racingsol.evaluate()
        elif self.solver == 'Complete 3D Solver':
            self.racingsol = AmplFullSolver().solve(racing_inst)
            self.racingsol.evaluate()
    def plotter(self):
        if self.solver == 'Trendline Solver':
            RacingData(self.data).plotdata()




if __name__ == "__main__":
    Analyzer('AustriaTestData.yaml').analyze()





    # racing_inst = RacingData(data)
    # RacingData.appendlists(racing_inst)
    # #racing_sol = AmplTrendlineSolver().solve(racing_inst)
    # racing_sol = AmplSolver().solve(racing_inst)
    # racing_sol.evaluate()
    # print(racing_sol)
    # RacingData.plotdata(racing_inst)