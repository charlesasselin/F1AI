from f1_2020_telemetry.packets import unpack_udp_packet
from f1_2020_telemetry import packets as f1packets
import socket
from dataclasses import dataclass


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

    @property
    def tyretype(self):
        if self.compound == 16:
            return 'C5'
        elif self.compound == 17:
            return 'C4'
        elif self.compound == 18:
            return 'C3'
        elif self.compound == 19:
            return 'C2'
        elif self.compound == 20:
            return 'C1'


if __name__ == "__main__":

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("0.0.0.0", 20777))

    lapTimes = {}
    listLapTimes = []
    lapCompound = {}
    file1 = open("lapData", "a")
    current_lap = 0

    while True:

        udp_packet = udp_socket.recv(2048)
        packet = unpack_udp_packet(udp_packet)
        attribute = packet.header

        # frame = attribute.frameIdentifier
        player_car = attribute.playerCarIndex
        # current_frame_data[PacketID(attribute.packetId)] = packet

        if isinstance(packet, f1packets.PacketLapData_V1):
            lapData = packet.lapData[player_car]
            lastLapNum = lapData.currentLapNum - 1
            if lastLapNum not in lapTimes.keys():
                current_lap = lastLapNum + 1
                lapTimes[lastLapNum] = LapTime(seconds=lapData.lastLapTime)
                listLapTimes.append(LapTime(seconds=lapData.lastLapTime).getseconds())
                totalLaps = f1packets.PacketSessionData_V1.totalLaps
                file1.write(f'{listLapTimes}\n')
                print(lapTimes)
        elif isinstance(packet, f1packets.PacketSessionData_V1):
            pass
        elif isinstance(packet, f1packets.PacketCarStatusData_V1):
            if current_lap - 1 not in lapCompound.keys():
                carStatusData = packet.carStatusData[player_car]
                lapCompound[current_lap-1] = Tyre(compound=carStatusData.actualTyreCompound)
                file1.write(f'{lapCompound}\n')
                print(lapCompound)

        else:
            pass

            # distance = current_frame_data[PacketID.LAP_DATA].lapData[player_car].totalDistance # THIS WORKS
            # lap = current_frame_data[PacketID.SESSION]  # THIS DOES NOT WORK HOW DO I ACCESS totalLaps?
            # print("Received:", frame, player_car, distance, lap)
