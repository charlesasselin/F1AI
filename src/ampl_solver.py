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

        nb_laps = racingdata.get_nb_laps()

        listLaps = list(range(1, nb_laps+1))
        listWear = list(range(1, 6))
        listTyres = list(range(1, 4))

        dfTyres = amplpy.DataFrame('tyres')
        dfTyres.setColumn('tyres', listTyres)
        ampl.setData(dfTyres, 'tyres')

        dfWear = amplpy.DataFrame('stints')
        dfWear.setColumn('stints', listWear)
        ampl.setData(dfWear, 'stints')

        dfLaps = amplpy.DataFrame('laps')
        dfLaps.setColumn('laps', listLaps)
        ampl.setData(dfLaps, 'laps')

        df = amplpy.DataFrame(('tyres', 'wear'), 'time')

        print(listTyres)
        print(listWear)

        df.setValues({
            (tyre, wear): racingdata.lapData[i][j]
            for i, tyre in enumerate(listTyres)
            for j, wear in enumerate(listWear)})
        print(df)

        ampl.setData(df)
        ampl.solve()

        compound = ampl.getVariable('compound')
        dfy = compound.getValues()
        print(dfy)
        chosen = {int(row[0]): int(row[1]) for row in dfy if row[3] == 1}
        print(chosen)

        pitScenario = []
        # for row in dfx:
        #     for i in chosen:
        #         to_append = [row[2]]
        #         if i == (row[0], row[1]):
        #             dist_list.append(to_append)