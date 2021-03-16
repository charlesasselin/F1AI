from src.data import Data
import f1_2020_telemetry.packets as f1



class RacingData(Data):

    def __init__(self):
        super(RacingData, self).__init__()

    def nb_laps(self):
        return f1.PacketSessionData_V1._fields_[5] # ('Total Laps', int)
