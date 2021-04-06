from solver import Solver
import amplpy
import os
from decision import Decision


class AmplTyreSolver(Solver):
    def __init__(self):
        super(AmplTyreSolver, self).__init__()

    @staticmethod
    def solve(racingdata):
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
        ampl.read(os.path.join(model_dir, 'f1aiTyre.mod'))

        nb_laps = racingdata.get_nb_laps()

        listlaps = list(range(1, nb_laps + 1))
        listwear = list(range(1, (min(len(racingdata.lapData[0]),
                                      len(racingdata.lapData[1]),
                                      len(racingdata.lapData[2]))
                                  )))
        listtyres = racingdata.compound2021()

        dftyres = amplpy.DataFrame('tyres')
        dftyres.setColumn('tyres', listtyres)
        ampl.setData(dftyres, 'tyres')

        dfwear = amplpy.DataFrame('stints')
        dfwear.setColumn('stints', listwear)
        ampl.setData(dfwear, 'stints')

        dflaps = amplpy.DataFrame('laps')
        dflaps.setColumn('laps', listlaps)
        ampl.setData(dflaps, 'laps')

        totallaps = ampl.getParameter('totalLaps')
        totallaps.set(nb_laps)

        tyrelifespan = ampl.getParameter('tyreLifeSpan')
        tyrelifespan.set(len(listwear))

        pittime = ampl.getParameter('pitTime')
        pittime.set(racingdata.pitTime)

        df = amplpy.DataFrame(('tyres', 'wear'), 'usage')

        df.setValues({
            (tyre, wear): racingdata.tyreUsageData[i][j]
            for i, tyre in enumerate(listtyres)
            for j, wear in enumerate(listwear)})
        ampl.setData(df)

        df = amplpy.DataFrame('tyres', ['coeff', 'avg'])
        df.setValues(racingdata.estimatedata())
        ampl.setData(df)
        ampl.solve()

        solution = Decision(racingdata)

        pit = ampl.getVariable('pit')
        dfpit = pit.getValues()
        chosen = {int(row[1]): row[0] for row in dfpit if row[2] == 1}

        solution.pitDecision = chosen

        compound = ampl.getVariable('compound')
        dfcompound = compound.getValues()
        chosen = {int(row[2]): [row[0], int(row[1])] for row in dfcompound if row[3] == 1}
        solution.compoundStrategy = chosen

        return solution