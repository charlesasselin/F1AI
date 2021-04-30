from f1_2020_telemetry.packets import unpack_udp_packet
from f1_2020_telemetry import packets as f1packets
import socket
from dataclasses import dataclass
import pickle
import yaml

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
                self.data['gptitle'] = str(self.appendix[packet.trackId])

            elif isinstance(packet, f1packets.PacketCarStatusData_V1):
                if lastLapNum != 0:
                    if lastLapNum not in self.lapCompound.keys():
                        carStatusData = packet.carStatusData[player_car]
                        self.lapCompound[lastLapNum] = Tyre(compound=carStatusData.actualTyreCompound)
                        print(self.lapCompound[lastLapNum])
                        for index, compound in self.data['compounds'].items():
                            if self.lapCompound[lastLapNum] == compound:
                                self.data['laptimes'][index].append(float(format(round(self.lapTimes[lastLapNum].getseconds(), 3))))
                                self.data['fuelintank'][index].append(float(format(round(carStatusData.fuelInTank, 1))))
                                totalTyresWear = 0
                                for i in range(4):
                                    totalTyresWear += carStatusData.tyresWear[i] / 100
                                avgTyresWear = format(round(totalTyresWear / 4, 2))
                                self.data['tyreusage'][index].append(avgTyresWear)
                        print(self.data)
                        with open('MonzaRecordData.yaml', 'w') as handle:
                            yaml.dump(self.data, handle, default_flow_style=False)

            else:
                pass





if __name__ == "__main__":
    Recorder().record()
