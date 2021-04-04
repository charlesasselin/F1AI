from src.data import Data
import f1_2020_telemetry.packets as f1



class RacingData(Data):

    def __init__(self, lapData):
        super(RacingData, self).__init__()
        self.lapData = lapData
        self.gpTitle = "Imola Grand Prix"

    def __str__(self):
        tmp_str = ''
        for a_list in self.lapData:
            tmp_str = tmp_str + ', '.join([str(i) for i in a_list])
            tmp_str = tmp_str + '\n'
        return str(tmp_str)

    def get_nb_laps(self):
        #return f1.PacketSessionData_V1._fields_[5] # ('Total Laps', int)
        imola = 31
        return imola

    def compound2021(self):
        return ["Soft", "Medium", "Hard"]
