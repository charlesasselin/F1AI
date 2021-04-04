from f1_2020_telemetry.packets import PacketID, unpack_udp_packet
from f1_2020_telemetry import packets as f1packets
import socket
import math
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class LapTime:
    seconds: float

    def __repr__(self):
        return self.minutes

    @property
    def minutes(self):
        return f"{int(self.seconds // 60)}:{self.seconds % 60:.3f}"


@dataclass
class Tyre:
    compound: Optional[int]

    def __repr__(self):
        return self.tyreType

    @property
    def tyreType(self):
        return self.compound


info = [LapTime, Tyre]

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(("0.0.0.0", 20777))

lapTimes = {}
file1 = open("lapData", "a")

while True:
    current_frame = None
    current_frame_data = {}

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
            lapTimes[lastLapNum] = [LapTime(seconds=lapData.lastLapTime), Tyre(compound=0)]
            totalLaps = f1packets.PacketSessionData_V1.totalLaps
            if lastLapNum+1 == totalLaps:
                file1.write(str(lapTimes))
                file1.close()
            print(lapTimes)
    elif isinstance(packet, f1packets.PacketSessionData_V1):
        pass
    if isinstance(packet, f1packets.PacketCarStatusData_V1):
        carStatusData = packet.carStatusData[player_car]
        Tyre.compound = carStatusData.actualTyreCompound

    else:
        pass

        # distance = current_frame_data[PacketID.LAP_DATA].lapData[player_car].totalDistance # THIS WORKS
        # lap = current_frame_data[PacketID.SESSION]  # THIS DOES NOT WORK HOW DO I ACCESS totalLaps?
        # print("Received:", frame, player_car, distance, lap)


