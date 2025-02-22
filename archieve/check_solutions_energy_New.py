# make the text beautiful
# Ansi color in python
# pip install ansi

ANSI_Enabled = True

try:
    from ansi.colour.rgb import rgb256
    from ansi.colour.fx import reset
except ImportError:
    ANSI_Enabled = False

print("Library status: ")
print("[ ANSI_library ] : " + str(ANSI_Enabled))
print()

# Python program to read
# json file

import json
from os import walk
import sys
import math
import numpy as np

file_name = sys.argv[1]
# file_name = "result_Gamma0.2_Strength1.0_Lattice9_9_64.json"

# Opening JSON file
f = open(file_name)

# returns JSON object as
# a dictionary
file = json.load(f)

# see if the file is being read
# print(file)


def print_progress_info():
    progress_info = file["qubo_solution"]["progress"]
    progress_energy = progress_info[0]["energy"]
    progress_time = progress_info[0]["time"]
    print("===== Progress information =====")
    print(" Lowest Energy = " + str(progress_energy))
    print(" Total run time = " + str(progress_time) + " (s) ")
    print("==============================")
    print()


solutions = file["qubo_solution"]["solutions"]
# print(solutions)

result_args = file_name.split("_")

# for i in result_args:
#  print(i)

Gamma = float(result_args[1].lstrip("Gamma"))
# K
Strength = float(result_args[2].lstrip("Strength"))

# tao
deltaT = 1.0

# K'
Layer_Strength = 0.0
if Gamma != 0.0:
    Layer_Strength = (-0.5) * math.log(math.tanh(deltaT * Gamma))
    Layer_Strength = round(Layer_Strength * 100000.0 * 100000.0) / (100000.0 * 100000.0)

L = int(result_args[3].lstrip("Lattice"))
H = int(result_args[5].rstrip(".json"))

# Lattice_args = result_args[3].split("*")
# L = int(Lattice_args[2].lstrip("Lattice"))
# H = int(Lattice_args[2].rstrip(".json"))

print("===== Model information =====")
print(" Length = " + str(L))
print(" Height = " + str(H))
print(" Gamma = " + str(Gamma))
print(" tao = " + str(deltaT))
print(" Strength = " + str(Strength))
print(" K'_Strength = " + str(Layer_Strength))


print_progress_info()

print()

#print("------ index color ------")

for s in range(0, len(solutions)):
    val = [False] * (L * L * H)
    sol = solutions[s]["configuration"]
    fujitsu_energy = solutions[s]["energy"]

    test_energy = 0

    for key in sol:
        if sol[key] == True:
            val[int(key)] = 1.0
        else:
            val[int(key)] = -1.0
    # print(val)

    In_Layer_count = 0
    each_In_layer_energy = []

    # Blue, Black, Red declaration [pos_num, neg_num]
    color_parameter = [[0, 0], [0, 0], [0, 0]]

    for h in range(0, H):
        h0_layer = h * L * L
        # h1_layer = ((h+1)%H)*L*L
        temp = test_energy

        for i in range(0, L):
            i = L-1-i
            i0_layer = i * L
            i1_layer = ((i + 1) % L) * L
            for j in range(0, L):
                cur = h0_layer + i0_layer + j
                cur_right = h0_layer + i0_layer + ((j + 1) % L)
                cur_buttom = h0_layer + i1_layer + j
                cur_btm_right = h0_layer + i1_layer + ((j + 1) % L)
                # cur_layer_up = h1_layer + i0_layer + j

                # Blue = 1
                # Black = 2
                # Red = 0
                color =  (2*i+j)%3

            #    print("index =\t" + str(cur) + ",\tcolor =\t" + str(color) )

                # only do one layer !!!
                #if h == 0:
                if val[cur] == 1.0:
                    color_parameter[color][0] += 1
                elif val[cur] == -1.0:
                   color_parameter[color][1] += 1

                test_energy += val[cur] * val[cur_right] * Strength
                In_Layer_count += 1
                test_energy += val[cur] * val[cur_buttom] * Strength
                In_Layer_count += 1
                test_energy += val[cur] * val[cur_btm_right] * Strength
                In_Layer_count += 1

        each_In_layer_energy.append(test_energy - temp)

    In_Layer_energy = test_energy

    each_Between_Layer_energy = []

    Between_Layer_count = 0
    if H > 1:
        # count Layer up energy
        for h in range(0, H):
            h0_layer = h * L * L
            h1_layer = ((h + 1) % H) * L * L
            temp = test_energy
            for i in range(0, L):
                i0_layer = i * L
                for j in range(0, L):
                    cur = h0_layer + i0_layer + j
                    cur_layer_up = h1_layer + i0_layer + j

                    test_energy -= val[cur] * val[cur_layer_up] * Layer_Strength
                    Between_Layer_count += 1
            each_Between_Layer_energy.append(test_energy - temp)

    print("====== Solutions[ " + str(s) + " ] =====")

    print(" fujitsu =\t" + str(fujitsu_energy))
    print(" In_Layer_energy =\t" + str(In_Layer_energy))
    print(" Between_Layer_energy =\t" + str(test_energy - In_Layer_energy))
    print(" cal_energy =\t" + str(test_energy))

    if round(fujitsu_energy, 5) == round(test_energy, 5):
        print(" [ Matched!! ]")
    else:
        print(" [ Error!! ]")

    print()

    """
    print("In_Layer_count = " + str(In_Layer_count))

    print("Energy = ")
    for i in range(0, len(each_In_layer_energy)):
        print("In_Layer[ " + str(i) + " ] = " + str(each_In_layer_energy[i]))
  
    print("Between_Layer_count = " + str(Between_Layer_count))
    print("Energy = ")
  
    for i in range(0, len(each_Between_Layer_energy)):
        print("Between_Layer[ " + str(i) + " ] = " + str(each_Between_Layer_energy[i]))
    """

    print(" -- order parameter --")

    blue_str = "Blue"
    red_str = "Red"
    black_str = "Black"

    if ANSI_Enabled:
        blue_str = "".join(map(str, ("\033[0;94m", "Blue", reset, "\033[0m")))
        black_str = "".join(map(str, ("\033[1m", "Black", reset, "\033[0m")))
        red_str = "".join(map(str, ("\033[0;91m", "Red", reset, "\033[0m")))
    
    m_red = (color_parameter[0][0] * 1.0 + color_parameter[0][1] * -1.0) / (
        color_parameter[0][0] + color_parameter[0][1]
    )
    m_blue = (color_parameter[1][0] * 1.0 + color_parameter[1][1] * -1.0) / (
        color_parameter[1][0] + color_parameter[1][1]
    )
    m_black = (color_parameter[2][0] * 1.0 + color_parameter[2][1] * -1.0) / (
        color_parameter[2][0] + color_parameter[2][1]
    )
   

    # testing when m_blue, m_black and m_red = 1.0
    # m_blue  = 1.0
    # m_black = 0.0
    # m_red   = -1.0
    
    print( red_str + ":\tpos/neg = "   + str(color_parameter[0][0]) + " / " + str(color_parameter[0][1]) )
    print( blue_str + ":\tpos/neg = "  + str(color_parameter[1][0]) + " / " + str(color_parameter[1][1]) )
    print( black_str + ":\tpos/neg = " + str(color_parameter[2][0]) + " / " + str(color_parameter[2][1]) )
   
    
    print(red_str + ":\tavg = " + str(m_red))
    print(blue_str + ":\tavg = " + str(m_blue))
    print(black_str + ":\tavg = " + str(m_black))
    

    imag_pi = complex(0, 4 / 3 * math.pi)

    order_parameter = (
        m_blue + m_red * (math.e ** (imag_pi)) + m_black * (math.e ** (-1.0 * imag_pi))
    ) / math.sqrt(3)

    NP_order_parameter = (
            m_red * (np.cos(np.pi * 4 / 3) + np.sin(np.pi * 4 / 3) * complex(0, 1))
        +   m_blue
        +   m_black * (np.cos(np.pi * 4 / 3) - np.sin(np.pi * 4 / 3) * complex(0, 1))
    ) / np.sqrt(3)

    print("Ordered_parameter = " + str(order_parameter))
    print(
        "Length of Order_P = "
        + str(np.real(order_parameter) ** 2 + np.imag(order_parameter) ** 2)
    )

    print("(NP) Ordered_parameter = " + str(NP_order_parameter))
    print(
        "(NP) Length of Order_P = "
        + str(np.real(NP_order_parameter) ** 2 + np.imag(NP_order_parameter) ** 2)
    )

    print()

    def print_layer():
        print(" -- check first two layers -- ")
        print("Layer 1 = ")
        for i in range(0, L):
            s = ""
            for j in range(0, L):
                s += str(val[i * L + j]) + ",\t"
            print(s)

        print("Layer 2 = ")

        for i in range(0, L):
            s = ""
            for j in range(0, L):
                s += str(val[i * L + j + L * L]) + ",\t"
            print(s)
        print()

    # print_layer()

    # print("========== End ==========")
