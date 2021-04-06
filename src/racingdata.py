from src.data import Data
import numpy as np
import matplotlib.pyplot as plt


class RacingData(Data):

    def __init__(self, lapdata):
        super(RacingData, self).__init__()
        self.lapData = lapdata['laptimes']
        self.gpTitle = lapdata['gptitle']
        self.pitTime = 17
        self.tyreUsageData = lapdata['tyreusage']

    def __str__(self):
        tmp_str = ''
        for a_list in self.lapData:
            tmp_str = tmp_str + ', '.join([str(i) for i in a_list])
            tmp_str = tmp_str + '\n'
        return str(tmp_str)

    @staticmethod
    def get_nb_laps():
        # return f1.PacketSessionData_V1._fields_[5] # ('Total Laps', int)
        imola = 50
        return imola

    @staticmethod
    def compound2021():
        return ["Soft", "Medium", "Hard"]

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
                    for tyre in self.compound2021()
                    for coeff in coefficients
                    for avg in average}
        return estimate

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

