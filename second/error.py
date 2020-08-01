import os, sys, argparse, math
import numpy as np
import os
import matplotlib.pyplot as plt

arg_parser  = argparse.ArgumentParser()
arg_parser.add_argument('-fn', '--file_name', required=True, help=' file name without extension')
args = vars(arg_parser.parse_args())
file_name = args['file_name']

l_bit_RMSE, l_int_RMSE, l_area, l_inp_RMSE = [], [], [], []

i = 2
while True:
    inp_rmse_path = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/rect/sim/ROI_'+str(i)+'/inpainting/RMSE.npy'
    bit_rmse_path = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/rect/sim/ROI_'+str(i)+'/bilinear/RMSE.npy'
    int_rmse_path = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/rect/sim/ROI_'+str(i)+'/linear/RMSE.npy'

    try:
        inp_rmse, area = np.load(inp_rmse_path)
        bit_rmse, area = np.load(bit_rmse_path)
        int_rmse, _ = np.load(int_rmse_path)

    except IOError:
        break

    l_inp_RMSE.append(inp_rmse)
    l_bit_RMSE.append(bit_rmse)
    l_int_RMSE.append(int_rmse)
    l_area.append(area)
    i += 1

plt.plot(l_area, l_bit_RMSE, label='bi-linear')
plt.plot(l_area, l_int_RMSE, label='linear')
plt.plot(l_area, l_inp_RMSE, label='inpainting')
plt.legend(loc='best')
plt.show()
