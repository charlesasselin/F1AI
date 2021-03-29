"""
Listen to telemetry packets and print them to standard output
"""
import socket
from racingdata import RacingData
from ampl_solver import AmplSolver

data = [[115, 116, 117, 118, 119],
        [116, 117, 118, 119, 120],
        [117, 118, 119, 120, 121]]

from f1_2020_telemetry.packets import unpack_udp_packet

# udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# udp_socket.bind(("0.0.0.0", 20777))

# while True:
#     udp_packet = udp_socket.recv(2048)
#     packet = unpack_udp_packet(udp_packet)
#     data =  packet._fields_
    # for name, info in data:
    #     if name == 'totalLaps':
    # print("Received:", packet._fields_[1])

racing_inst = RacingData(data)
print(racing_inst)
racing_sol = AmplSolver().solve(racing_inst)
