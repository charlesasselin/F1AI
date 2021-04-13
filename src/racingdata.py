from src.data import Data
import numpy as np
import matplotlib.pyplot as plt
import copy
from mpl_toolkits.mplot3d import Axes3D
import scipy.linalg


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
        self.fuelInTank = lapdata['fuelintank']
        self.futureFuelInTankData = copy.deepcopy(self.fuelInTank)

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

    def fueldiff(self):
        fueldiffdata = {}
        for i in self.compounds.keys():
            if len(self.fuelInTank[i]) == 0:
                raise ValueError('no items in list')
            a = np.array(self.fuelInTank[i])
            fueldiff = sum(np.diff(a)) / len(self.fuelInTank[i])
            fueldiffdata[i] = fueldiff
        total = 0
        for i in fueldiffdata.values():
            total += i
        avg = total/len(self.compounds)
        return avg

    def trendlinedata(self):
        g1 = (self.tyreUsageData[0], self.lapData[0])
        g2 = (self.tyreUsageData[1], self.lapData[1])
        g3 = (self.tyreUsageData[2], self.lapData[2])
        data = (g1, g2, g3)
        equation = []
        for data in data:
            x, y = data
            z = np.polyfit(x, y, 1)
            eq = [z[1], z[0]]
            equation.append(eq)
        estimate = {tyre: eq for tyre, eq in zip(self.compounds.values(), equation)}
        return estimate

    def appendlists(self):
        it = iter(self.tyreUsageData)
        the_len = len(next(it))
        maxlen = max(len(l) for l in self.tyreUsageData)
        if not all(len(l) == the_len for l in it):
            for i, l in enumerate(self.tyreUsageData):
                missinglaps = maxlen - len(l)
                tyre = self.compounds[i]
                coeff = self.trendlinedata()[tyre][1]
                avg = self.trendlinedata()[tyre][0]
                while missinglaps != 0:
                    self.futureTyreUsageData[i].append(self.futureTyreUsageData[i][-1] + self.tyreusediff()[i])
                    self.futureLapData[i].append(self.futureTyreUsageData[i][-1] * coeff + avg)
                    missinglaps -= 1

    def plotdata(self):
        g1 = (self.futureTyreUsageData[0], self.futureLapData[0])
        g2 = (self.futureTyreUsageData[1], self.futureLapData[1])
        g3 = (self.futureTyreUsageData[2], self.futureLapData[2])
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
        plt.title(f'Tyre wear evolution and its effect \n on lap times in {self.gpTitle} for Soft, Medium and Hard compounds')
        plt.legend(loc="best", labelspacing=0.5, borderpad=0.2, handletextpad=0.05)
        plt.xlabel("Tyre Usage")
        plt.ylabel("Lap Times")
        plt.savefig('figure1.png')

    def fullplotdata(self):
        g1 = (self.tyreUsageData[0], self.fuelInTank[0], self.lapData[0])
        g2 = (self.tyreUsageData[1], self.fuelInTank[1], self.lapData[1])
        g3 = (self.tyreUsageData[2], self.fuelInTank[2], self.lapData[2])
        data = (g1, g2, g3)
        colors = ("red", "blue", "black")
        groups = ("Soft", "Medium", "Hard")
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        equation = []
        for data, color, group in zip(data, colors, groups):
            x, y, z = data
            data = np.c_[x,y,z]
            mn = np.min(data, axis=0)
            mx = np.max(data, axis=0)
            X, Y = np.meshgrid(np.linspace(mn[0], mx[0], 20), np.linspace(mn[1], mx[1], 20))
            A = np.c_[data[:, 0], data[:, 1], np.ones(data.shape[0])]
            C, _, _, _ = scipy.linalg.lstsq(A, data[:, 2])
            ax.scatter(data[:, 0], data[:, 1], data[:, 2], alpha=0.8, c=color, edgecolors='none', s=30, label=group)
            Z = C[0] * X + C[1] * Y + C[2]
            eq = [C[0], C[1], C[2]]
            equation.append(eq)
            p = np.poly1d(z)
            surf = ax.plot_surface(X, Y, Z, color=color, rstride=1, cstride=1, alpha=0.2, label="z=%.6fx+%.6fy+(%.6f)" % (C[0], C[1], C[2]))
            surf._facecolors2d = surf._facecolor3d
            surf._edgecolors2d = surf._edgecolor3d
        plt.title(f'Tyre wear and Fuel evolution and their effects \n on lap times in {self.gpTitle} for Soft, Medium and Hard compounds')
        plt.legend(loc="best", labelspacing=0.5, borderpad=0.2, handletextpad=0.05)
        ax.set_xlabel('Tyre Usage')
        ax.set_ylabel('Fuel in tank')
        ax.set_zlabel('Lap times')
        plt.savefig('figure2.png')
        return {tyre: eq for tyre, eq in zip(self.compounds.values(), equation)}

if __name__ == '__main__':
    data = {"laptimes": [[69.165, 69.712, 70.309, 70.148, 69.352, 70.695, 70.408, 70.485, 70.107, 69.881, 70.344, 69.786, 70.267, 70.335, 70.373, 70.071, 70.698, 70.109, 71.897, 72],
                         [67.964, 67.921, 67.426, 68.536, 68.548, 68.428, 69.302, 68.015, 68.522, 68.568, 68.729, 68.234, 68.158, 68.113, 68.331, 68.334, 69.023, 68.638, 67.576],
                         [70.127, 70.419, 70.045, 69.766, 69.699, 69.728, 70.651, 69.774, 70.070, 70.410, 70.840, 69.795, 70.940, 70.152, 70.002, 69.644, 70.472, 70.603]],
            "tyreusage": [[0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95],
                          [0, 0.04, 0.08, 0.12, 0.16, 0.20, 0.24, 0.28, 0.32, 0.36, 0.40, 0.44, 0.48, 0.52, 0.56, 0.60, 0.64, 0.68, 0.72],
                          [0, 0.03, 0.06, 0.09, 0.12, 0.15, 0.18, 0.21, 0.24, 0.27, 0.30, 0.33, 0.36, 0.39, 0.42, 0.45, 0.48, 0.51]],
            'fuelintank': [[70, 68.75, 67.5, 66.25, 65, 63.75, 62.5, 61.25, 60, 58.75, 57.5, 56.25, 55, 53.75, 52.5, 51.25, 50, 48.75, 47.5, 46.25],
                           [45, 43.75, 42.5, 41.25, 40, 38.75, 37.5, 36.25, 35, 33.75, 32.5, 31.25, 30, 28.75, 27.5, 26.25, 25, 23.75, 22.5],
                           [21.25, 20, 18.75, 17.5, 16.25, 15, 13.75, 12.5, 11.25, 10, 8.75, 7.5, 6.25, 5, 3.75, 2.5, 1.25, 0]],
            "totallaps": 50,
            "gptitle": "Imola Grand Prix",
            "compounds": {0: "Soft", 1: "Medium", 2: "Hard"}}
    RacingData(data).fullplotdata()
    RacingData(data).fueldiff()
