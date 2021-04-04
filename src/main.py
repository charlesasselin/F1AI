"""
Listen to telemetry packets and print them to standard output
"""
import socket
from racingdata import RacingData
from ampl_solver import AmplSolver
from decision import Decision

data = [[72.056, 69.165, 69.712, 70.309, 70.148, 69.352, 70.695, 70.408, 70.485, 70.107, 69.881, 70.344, 69.786, 70.267, 70.335, 70.373, 70.071, 70.698, 70.109, 71.897],
        [73.559, 70.127, 70.419, 70.045, 69.766, 69.699, 69.728, 70.651, 69.774, 70.070, 70.410, 70.840, 69.795, 70.940, 70.152, 70.002, 69.644, 70.472, 70.603, 69.988, 69.526, 69.667, 69.355, 69.206, 69.094, 69.248, 73.176],
        [71.634, 67.964, 67.921, 67.426, 68.536, 68.548, 68.428, 69.302, 68.015, 68.522, 68.568, 68.729, 68.234, 68.158, 68.113, 68.331, 68.334, 69.023, 68.638, 67.576, 69.038, 68.152, 68.271, 67.884]]

# data = [[117, 116, 117, 118, 119],
#         [118, 117, 118, 119, 120],
#         [123, 122, 123, 122, 121]]

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
print(racing_sol)
print(Decision)