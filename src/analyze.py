"""
Listen to telemetry packets and print them to standard output
"""
from racingdata import RacingData
from ampl_solver import AmplSolver

data = [[72.056, 69.165, 69.712, 70.309, 70.148, 69.352, 70.695, 70.408, 70.485, 70.107, 69.881, 70.344, 69.786, 70.267, 70.335, 70.373, 70.071, 70.698, 70.109, 71.897],
         [71.634, 67.964, 67.921, 67.426, 68.536, 68.548, 68.428, 69.302, 68.015, 68.522, 68.568, 68.729, 68.234, 68.158, 68.113, 68.331, 68.334, 69.023, 68.638, 67.576, 69.038, 68.152, 68.271, 67.884],
         [73.559, 70.127, 70.419, 70.045, 69.766, 69.699, 69.728, 70.651, 69.774, 70.070, 70.410, 70.840, 69.795, 70.940, 70.152, 70.002, 69.644, 70.472, 70.603, 69.988, 69.526, 69.667, 69.355, 69.206, 69.094, 69.248, 73.176],]
with open('lapData', 'r') as lapData:
    line = lapData.readline()
    while line != '':
        print(line[0:-1])
        line = lapData.readline()


if __name__ == "__main__":
    racing_inst = RacingData(data)
    racing_sol = AmplSolver().solve(racing_inst)
    print(racing_sol)
