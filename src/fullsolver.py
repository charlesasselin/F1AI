from solver import Solver
import amplpy
import os
from decision import Decision


class AmplFullSolver(Solver):
    def __init__(self):
        super(AmplFullSolver, self).__init__()

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

        model_dir = os.path.normpath('./ampl_models/All3D')
        ampl.read(os.path.join(model_dir, 'f1aiFull.mod'))

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

        df = amplpy.DataFrame('tyres', ['coeffx', 'coeffy', 'avg'])
        df.setValues(racingdata.fullplotdata())
        ampl.setData(df)
        startingfuel = 0.05
        flattenfuel = [startingfuel]
        fueldiff = -1 * racingdata.fueldiff()
        for lap in listlaps:
            startingfuel += fueldiff
            flattenfuel.append(float("{:.2f}".format(startingfuel)))
        df = amplpy.DataFrame('laps', 'fuel')
        flattenfuel.reverse()
        df.setValues({lap: flattenfuel[i] for i, lap in enumerate(listlaps)})
        ampl.setData(df)
        ampl.solve()

        solution = Decision(racingdata)

        pit = ampl.getVariable('pit')
        dfpit = pit.getValues()
        chosen = {int(row[1]): row[0] for row in dfpit if row[2] == 1}

        solution.pitDecision = chosen

        solution.fuel = flattenfuel[0]

        compound = ampl.getVariable('compound')
        dfcompound = compound.getValues()
        chosen = {int(row[2]): [row[0], int(row[1])] for row in dfcompound if row[3] == 1}
        solution.compoundStrategy = chosen

        time = ampl.getVariable('time')
        dftime = time.getValues()
        for row in dftime:
            for k, v in racingdata.compounds.items():
                if v == row[0]:
                    solution.lapTimes[k].append(row[3])
        return solution
