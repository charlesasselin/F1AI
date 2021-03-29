"""
Listen to telemetry packets and print them to standard output
"""
import socket

from f1_2020_telemetry.packets import unpack_udp_packet

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(("0.0.0.0", 20777))

while True:
    udp_packet = udp_socket.recv(2048)
    packet = unpack_udp_packet(udp_packet)
    data =  packet._fields_
    # for name, info in data:
    #     if name == 'totalLaps':
    # print("Received:", packet._fields_[1])