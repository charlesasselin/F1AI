from src.data import Data
import f1_2020_telemetry.packets as f1


class RacingData(Data):

    def __init__(self, lapdata):
        super(RacingData, self).__init__()
        self.lapData = lapdata
        self.gpTitle = "Austria Spielberg Grand Prix"
        self.pitTime = 17
        self.tyreUsageData = [[0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90],
                              [0, 0.04, 0.08, 0.12, 0.16, 0.20, 0.24, 0.28, 0.32, 0.36, 0.40, 0.44, 0.48, 0.52, 0.56, 0.60, 0.64, 0.68, 0.72],
                              [0, 0.03, 0.06, 0.09, 0.12, 0.15, 0.18, 0.21, 0.24, 0.27, 0.30, 0.33, 0.36, 0.39, 0.42, 0.45, 0.48, 0.51, 0.54]]

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

    def estimatedata(self):
        coefficients = [1.1265, 1.797, 0.9527]
        average = [69.711, 67.863, 70.023]
        estimate = {tyre : [coeff, avg]
                    for tyre in self.compound2021()
                    for coeff in coefficients
                    for avg in average}
        return estimate
