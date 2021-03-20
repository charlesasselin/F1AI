from solver import Solver
import amplpy
import os


class AmplSolver(Solver):
    def __init__(self):
        super(AmplSolver, self).__init__()

    def solve(self, racingdata):
        ampl_env = amplpy.Environment()
        ampl = amplpy.AMPL(ampl_env)

        ampl.setOption('solver', 'gurobi')
        ampl.setOption('gurobi_options',
                       "mipfocus 1"
                       "relax 0"
                       "timelim 7200 "
                       "tunetimelimit 60 "
                       )

        model_dir = os.path.normpath('./ampl_models')
        ampl.read(os.path.join(model_dir, 'f1ai.mod'))

        nb_locations = racingdata.count_locations()
        laps = list(range(1, nb_locations+1))

        tyres = amplpy.DataFrame('tyres')
        tyres.setColumn('tyres', tyres)
        ampl.setData(tyres, 'tyres')

        laps = amplpy.DataFrame('laps')
        laps.setColumn('laps', laps)
        ampl.setData(laps, 'laps')

        df = amplpy.DataFrame(('tyres', 'laps'), 'time')

        df.setValues({
            (start, end): racingdata.projected_times[i][j]
            for i, start in enumerate(laps)
            for j, end in enumerate(laps)})
        # print(df)

        ampl.setData(df)
        ampl.solve()

        compound = ampl.getVariable('compound')
        dfy = compound.getValues()
        print(compound)
        chosen = {int(row[0]): int(row[1]) for row in dfy if row[3] == 1}

        x = ampl.getParameter('X')
        dfx = x.getValues()
        pitScenario = []
        for row in dfx:
            for i in chosen:
                to_append = [row[2]]
                if i == (row[0], row[1]):
                    dist_list.append(to_append)

        print()