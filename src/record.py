from f1_2020_telemetry.packets import unpack_udp_packet
from f1_2020_telemetry import packets as f1packets
import socket
from dataclasses import dataclass
import pickle

@dataclass
class LapStatus:
    pass

@dataclass
class LapTime(LapStatus):
    seconds: float

    def __repr__(self):
        return self.minutes

    def getseconds(self):
        return self.seconds

    @property
    def minutes(self):
        return f"{int(self.seconds // 60)}:{self.seconds % 60:.3f}"


@dataclass
class Tyre(LapStatus):
    compound: int

    def __repr__(self):
        return self.tyretype

    def __eq__(self, other):
        return other == self.tyretype

    @property
    def tyretype(self):
        if self.compound == 16:
            return 'Soft'
        elif self.compound == 17:
            return 'Soft'
        elif self.compound == 18:
            return 'Medium'
        elif self.compound == 19:
            return 'Hard'
        elif self.compound == 20:
            return 'Hard'


class Recorder:
    def __init__(self):
        self.lapTimes = {}
        self.listLapTimes = []
        self.lapCompound = {}
        self.appendix = {0: 'Melbourne', 1: 'Paul Ricard', 2: 'Shanghai', 3: 'Sakhir (Bahrain)',
                         4: 'Catalunya', 5: 'Monaco', 6: 'Montreal', 7: 'Silverstone',
                         8: 'Hockenheim', 9: 'Hungaroring', 10: 'Spa', 11: 'Monza',
                         12: 'Singapore', 13: 'Suzuka', 14: 'Abu Dhabi', 15: 'Texas',
                         16: 'Brazil', 17: 'Austria', 18: 'Sochi', 19: 'Mexico',
                         20: 'Baku (Azerbaijan)', 21: 'Sakhir Short', 22: 'Silverstone Short', 23: 'Texas Short',
                         24: 'Suzuka Short', 25: 'Hanoi', 26: 'Zandvoort'}
        self.data = {'laptimes': [[], [], []],
                     'tyreusage': [[], [], []],
                     'fuelintank': [[], [], []],
                     'compounds': {0: 'Soft', 1: 'Medium', 2: 'Hard'}}
    def record(self):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind(("0.0.0.0", 20777))

        currentLapNum = 1
        lastLapNum = 0

        testDict = {'laptimes': [[69.165, 69.712, 70.309, 70.148, 69.352, 70.695, 70.408, 70.485, 70.107, 69.881, 70.344, 69.786, 70.267, 70.335, 70.373, 70.071, 70.698, 70.109, 71.897, 72],
                     [67.964, 67.921, 67.426, 68.536, 68.548, 68.428, 69.302, 68.015, 68.522, 68.568, 68.729, 68.234, 68.158, 68.113, 68.331, 68.334, 69.023, 68.638, 67.576],
                     [70.127, 70.419, 70.045, 69.766, 69.699, 69.728, 70.651, 69.774, 70.070, 70.410, 70.840, 69.795, 70.940, 70.152, 70.002, 69.644, 70.472, 70.603, 69.988]],
        'tyreusage': [[0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95],
                      [0, 0.04, 0.08, 0.12, 0.16, 0.20, 0.24, 0.28, 0.32, 0.36, 0.40, 0.44, 0.48, 0.52, 0.56, 0.60, 0.64, 0.68, 0.72],
                      [0, 0.03, 0.06, 0.09, 0.12, 0.15, 0.18, 0.21, 0.24, 0.27, 0.30, 0.33, 0.36, 0.39, 0.42, 0.45, 0.48, 0.51, 0.54]],
        'totallaps': 50,
        'gptitle': 'Imola Grand Prix',
        'compounds': {0: 'Soft', 1: 'Medium', 2: 'Hard'}}


        with open('testData', 'wb') as handle:
            pickle.dump(testDict, handle, protocol=pickle.HIGHEST_PROTOCOL)

        while True:
            udp_packet = udp_socket.recv(2048)
            packet = unpack_udp_packet(udp_packet)
            attribute = packet.header
            player_car = attribute.playerCarIndex

            if isinstance(packet, f1packets.PacketLapData_V1):
                self.lapData = packet.lapData[player_car]
                currentLapNum = self.lapData.currentLapNum
                lastLapNum = currentLapNum - 1
                if lastLapNum not in self.lapTimes.keys():
                    self.lapTimes[lastLapNum] = LapTime(seconds=self.lapData.lastLapTime)
                    self.listLapTimes.append(format(self.lapTimes[lastLapNum].getseconds(), '.3f'))
                    print(self.listLapTimes)
                else:
                    pass

            elif isinstance(packet, f1packets.PacketSessionData_V1):
                self.data['totallaps'] = packet.totalLaps
                self.data['gptitle'] = self.appendix[packet.trackId]

            elif isinstance(packet, f1packets.PacketCarStatusData_V1):
                if lastLapNum != 0:
                    if lastLapNum not in self.lapCompound.keys():
                        carStatusData = packet.carStatusData[player_car]
                        self.lapCompound[lastLapNum] = Tyre(compound=carStatusData.actualTyreCompound)
                        print(self.lapCompound[lastLapNum])
                        for index, compound in self.data['compounds'].items():
                            if self.lapCompound[lastLapNum] == compound:
                                self.data['laptimes'][index].append(format(self.lapTimes[lastLapNum].getseconds(), '.3f'))
                                self.data['fuelintank'][index].append(format(carStatusData.fuelInTank, '.1f'))
                                totalTyresWear = 0
                                for i in range(4):
                                    totalTyresWear += carStatusData.tyresWear[i] / 100
                                avgTyresWear = format(totalTyresWear / 4, '.2f')
                                self.data['tyreusage'][index].append(avgTyresWear)
                        print(self.data)
                        with open('recordData', 'wb') as handle:
                            pickle.dump(self.data, handle, protocol=pickle.HIGHEST_PROTOCOL)

            else:
                pass





if __name__ == "__main__":
    Recorder().record()

#
#     udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     udp_socket.bind(("0.0.0.0", 20777))
#
#     lapTimes = {}
#     listLapTimes = []
#     lapCompound = {}
#     appendix = {0: 'Melbourne', 1: 'Paul Ricard', 2: 'Shanghai', 3: 'Sakhir (Bahrain)',
#                 4: 'Catalunya', 5: 'Monaco', 6: 'Montreal', 7: 'Silverstone',
#                 8: 'Hockenheim', 9: 'Hungaroring', 10: 'Spa', 11: 'Monza',
#                 12: 'Singapore', 13: 'Suzuka', 14: 'Abu Dhabi', 15: 'Texas',
#                 16: 'Brazil', 17: 'Austria', 18: 'Sochi', 19: 'Mexico',
#                 20: 'Baku (Azerbaijan)', 21: 'Sakhir Short', 22: 'Silverstone Short', 23: 'Texas Short',
#                 24: 'Suzuka Short', 25: 'Hanoi', 26: 'Zandvoort'}
#     data = {'laptimes': [[], [], []],
#             'tyreusage': [[], [], []],
#             'fuelintank': [[], [], []],
#             'compounds': {0: 'Soft', 1: 'Medium', 2: 'Hard'}}
#     currentLapNum = 1
#     lastLapNum = 0
#     while True:
#         udp_packet = udp_socket.recv(2048)
#         packet = unpack_udp_packet(udp_packet)
#         attribute = packet.header
#         player_car = attribute.playerCarIndex
#
#         if isinstance(packet, f1packets.PacketLapData_V1):
#             lapData = packet.lapData[player_car]
#             currentLapNum = lapData.currentLapNum
#             lastLapNum = currentLapNum - 1
#             if lastLapNum not in lapTimes.keys():
#                 lapTimes[lastLapNum] = LapTime(seconds=lapData.lastLapTime)
#                 listLapTimes.append(format(lapTimes[lastLapNum].getseconds(), '.3f'))
#                 print(listLapTimes)
#             else:
#                 pass
#
#         elif isinstance(packet, f1packets.PacketSessionData_V1):
#             data['totallaps'] = packet.totalLaps
#             data['gptitle'] = appendix[packet.trackId]
#
#         elif isinstance(packet, f1packets.PacketCarStatusData_V1):
#             if lastLapNum != 0:
#                 if lastLapNum not in lapCompound.keys():
#                     carStatusData = packet.carStatusData[player_car]
#                     lapCompound[lastLapNum] = Tyre(compound=carStatusData.actualTyreCompound)
#                     print(lapCompound[lastLapNum])
#                     for index, compound in data['compounds'].items():
#                         if lapCompound[lastLapNum] == compound:
#                             data['laptimes'][index].append(format(lapTimes[lastLapNum].getseconds(), '.3f'))
#                             data['fuelintank'][index].append(format(carStatusData.fuelInTank, '.1f'))
#                             totalTyresWear = 0
#                             for i in range(4):
#                                 totalTyresWear += carStatusData.tyresWear[i]/100
#                             avgTyresWear = format(totalTyresWear/4, '.2f')
#                             data['tyreusage'][index].append(avgTyresWear)
#                     print(data)
#                     with open('recordData', 'wb') as handle:
#                         pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
#
#         else:
#             pass
#
