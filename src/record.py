from f1_2020_telemetry.packets import unpack_udp_packet
from f1_2020_telemetry import packets as f1packets
import socket
from dataclasses import dataclass
import pickle


@dataclass
class LapTime:
    seconds: float

    def __repr__(self):
        return self.minutes

    def getseconds(self):
        return self.seconds

    @property
    def minutes(self):
        return f"{int(self.seconds // 60)}:{self.seconds % 60:.3f}"


@dataclass
class Tyre:
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


if __name__ == "__main__":

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("0.0.0.0", 20777))

    lapTimes = {}
    listLapTimes = []
    lapCompound = {}
    appendix = {0: 'Melbourne', 1: 'Paul Ricard', 2: 'Shanghai', 3: 'Sakhir (Bahrain)',
                4: 'Catalunya', 5: 'Monaco', 6: 'Montreal', 7: 'Silverstone',
                8: 'Hockenheim', 9: 'Hungaroring', 10: 'Spa', 11: 'Monza',
                12: 'Singapore', 13: 'Suzuka', 14: 'Abu Dhabi', 15: 'Texas',
                16: 'Brazil', 17: 'Austria', 18: 'Sochi', 19: 'Mexico',
                20: 'Baku (Azerbaijan)', 21: 'Sakhir Short', 22: 'Silverstone Short', 23: 'Texas Short',
                24: 'Suzuka Short', 25: 'Hanoi', 26: 'Zandvoort'}
    data = {'laptimes': [[], [], []],
            'tyreusage': [[], [], []],
            'compounds': {'Soft': 0, 'Medium': 1, 'Hard': 2}}
    currentLapNum = 1
    lastLapNum = 0
    while True:
        udp_packet = udp_socket.recv(2048)
        packet = unpack_udp_packet(udp_packet)
        attribute = packet.header
        player_car = attribute.playerCarIndex

        if isinstance(packet, f1packets.PacketLapData_V1):
            lapData = packet.lapData[player_car]
            currentLapNum = lapData.currentLapNum
            lastLapNum = currentLapNum - 1
            if lastLapNum not in lapTimes.keys():
                lapTimes[lastLapNum] = LapTime(seconds=lapData.lastLapTime)
                listLapTimes.append(format(lapTimes[lastLapNum].getseconds(), '.3f'))
                print(listLapTimes)
            else:
                pass

        elif isinstance(packet, f1packets.PacketSessionData_V1):
            data['totallaps'] = packet.totalLaps
            data['gptitle'] = appendix[packet.trackId]

        elif isinstance(packet, f1packets.PacketCarStatusData_V1):
            if lastLapNum not in lapCompound.keys():
                carStatusData = packet.carStatusData[player_car]
                lapCompound[lastLapNum] = Tyre(compound=carStatusData.actualTyreCompound)
                print(lapCompound[lastLapNum])
                for compound in data['compounds']:
                    if lapCompound[lastLapNum] == compound:
                        data['laptimes'][data['compounds'][compound]].append(format(lapTimes[lastLapNum].getseconds(), '.3f'))
                        totalTyresWear = 0
                        for i in range(4):
                            totalTyresWear += carStatusData.tyresWear[i]/100
                        avgTyresWear = format(totalTyresWear/4, '.3f')
                        data['tyreusage'][data['compounds'][compound]].append(avgTyresWear)
                print(data)
                with open('recordData', 'wb') as handle:
                    pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            pass

