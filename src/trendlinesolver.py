from solver import Solver
import amplpy
import os
from decision import Decision


class AmplTrendlineSolver(Solver):
    def __init__(self):
        super(AmplTrendlineSolver, self).__init__()

    @staticmethod
    def solve(racingdata):
        ampl_env = amplpy.Environment()
        ampl = amplpy.AMPL(ampl_env)

        ampl.setOption('solver', 'gurobi')

        model_dir = os.path.normpath('./ampl_models/Trend3D')
        ampl.read(os.path.join(model_dir, 'f1aiTyre.mod'))

        listlaps = list(range(1, racingdata.totalLaps + 1))
        listwear = list(range(1, (min(len(racingdata.lapData[0]),
                                      len(racingdata.lapData[1]),
                                      len(racingdata.lapData[2]))+1
                                  )))
        listtyres = racingdata.compounds.values()

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
        totallaps.set(racingdata.totalLaps)

        tyrelifespan = ampl.getParameter('tyreLifeSpan')
        tyrelifespan.set(len(listwear))

        pittime = ampl.getParameter('pitTime')
        pittime.set(racingdata.pitTime)

        df = amplpy.DataFrame(('tyres', 'wear'), 'usage')

        df.setValues({
            (tyre, wear): racingdata.futureTyreUsageData[i][j]
            for i, tyre in enumerate(listtyres)
            for j, wear in enumerate(listwear)})
        ampl.setData(df)
        df = amplpy.DataFrame('tyres', ['avg', 'coeff'])
        df.setValues(racingdata.trendlinedata())
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

        time = ampl.getVariable('time')
        dftime = time.getValues()
        for row in dftime:
            for k, v in racingdata.compounds.items():
                if v == row[0]:
                    solution.lapTimes[k].append(row[2])
        return solution
