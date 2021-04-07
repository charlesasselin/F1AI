from src.data import Data
import numpy as np
import matplotlib.pyplot as plt
import copy


class RacingData(Data):

    def __init__(self, lapdata):
        super(RacingData, self).__init__()
        self.lapData = lapdata['laptimes']
        self.futureLapData = copy.deepcopy(self.lapData)
        self.gpTitle = lapdata['gptitle']
        self.pitTime = 17
        self.tyreUsageData = lapdata['tyreusage']
        self.futureTyreUsageData = copy.deepcopy(self.tyreUsageData)
        self.totalLaps = lapdata['totallaps']
        self.compounds = lapdata['compounds']

    def __str__(self):
        tmp_str = ''
        for a_list in self.lapData:
            tmp_str = tmp_str + ', '.join([str(i) for i in a_list])
            tmp_str = tmp_str + '\n'
        return str(tmp_str)

    def tyreusediff(self):
        usediff = {}
        for i in self.compounds.keys():
            if len(self.tyreUsageData[i]) == 0:
                raise ValueError('no items in list')
            a = np.array(self.tyreUsageData[i])
            tyrediff = sum(np.diff(a))/len(self.tyreUsageData[i])
            usediff[i] = tyrediff
        return usediff

    def trendlinedata(self):
        g1 = (self.tyreUsageData[0], self.lapData[0])
        g2 = (self.tyreUsageData[1], self.lapData[1])
        g3 = (self.tyreUsageData[2], self.lapData[2])
        data = (g1, g2, g3)
        trendlinedata = {'coefficients': [], 'average': []}
        for data in data:
            x, y = data
            z = np.polyfit(x, y, 1)
            trendlinedata['coefficients'].append(z[1])
            trendlinedata['average'].append(z[0])
        coefficients = trendlinedata['coefficients']
        average = trendlinedata['average']
        estimate = {tyre: [coeff, avg]
                    for tyre in self.compounds.values()
                    for coeff in coefficients
                    for avg in average}
        return estimate

    def appendlists(self):
        it = iter(self.tyreUsageData)
        the_len = len(next(it))
        maxlen = max(len(l) for l in self.tyreUsageData)
        print(maxlen)
        if not all(len(l) == the_len for l in it):
            for i, l in enumerate(self.tyreUsageData):
                missinglaps = maxlen - len(l)
                while missinglaps != 0:
                    self.futureTyreUsageData[i].append(self.futureTyreUsageData[i][-1] + self.tyreusediff()[i])
                    self.futureLapData[i].append(self.futureTyreUsageData[i][-1]
                                                 * self.trendlinedata()[self.compounds[i]][0]
                                                 + self.trendlinedata()[self.compounds[i]][1])
                    missinglaps -= 1

    def plotdata(self):
        g1 = (self.tyreUsageData[0], self.lapData[0])
        g2 = (self.tyreUsageData[1], self.lapData[1])
        g3 = (self.tyreUsageData[2], self.lapData[2])
        data = (g1, g2, g3)
        colors = ("red", "blue", "black")
        groups = ("Soft", "Medium", "Hard")
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        for data, color, group in zip(data, colors, groups):
            x, y = data
            ax.scatter(x, y, alpha=0.8, c=color, edgecolors='none', s=30, label=group)
            z = np.polyfit(x, y, 1)
            p = np.poly1d(z)
            ax.plot(x, p(x), c=color, label="y=%.6fx+(%.6f)" % (z[0], z[1]))
        plt.title('Tyre wear evolution in Austria for Soft, Medium and Hard compounds')
        plt.legend(loc="best", labelspacing=0.5, borderpad=0.2, handletextpad=0.05)
        plt.xlabel("Tyre Usage")
        plt.ylabel("Lap Times")
        return plt.show()
