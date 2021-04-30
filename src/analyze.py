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

### COMMENT FOR ASTON MARTIN RACING ###
## PLEASE PRIORTIZE USAGE OF PICKLE DURING RACE WEEKENDS SO THAT THE DATA CAN'T BE READ BY HUMANS ##
# -------------------------------------------------
# with open('recordData', 'rb') as handle:
#     data = pickle.load(handle)

class Analyzer:
    def __init__(self, handle, solver='Trendline Solver'):
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
