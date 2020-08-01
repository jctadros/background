import numpy as np
import os, sys, argparse
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
from matplotlib import ticker, cm

image_path   = '/Users/jeantad/Desktop/new_crab/DATA_TEST/'
output_path  = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'
arg_parser   = argparse.ArgumentParser()
arg_parser.add_argument("-fn", "--file_name", required=True, help="  file name without extension")
args = vars(arg_parser.parse_args())
file_name = args['file_name']

masked_image = np.load(output_path+file_name+'/analysis/ROI_0/masked_image.npy')
mask = np.load(output_path+file_name+'/analysis/ROI_0/mask.npy')
new_image = np.copy(masked_image)
new_mask  = np.copy(mask)

xlist, ylist = [], []
for x in range(mask.shape[0]):
    for y in range(mask.shape[1]):
        if mask[x][y] == 255:
            xlist.append(x)
            ylist.append(y)

minx, maxx = min(xlist), max(xlist)
miny, maxy = min(ylist), max(ylist)

new_image[minx:maxx+1, miny:maxy+1] = np.nan
new_mask[minx:maxx+1, miny:maxy+1]  = 255

directory_1 = output_path + str(file_name) + '/analysis/rect'
directory = [directory_1]

for dir in directory:
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
    except OSError:
            print ('Error: Creating directory. ' + dir)

plt.imshow(new_mask)
plt.axis('off')
plt.savefig(directory_1+'/mask.png')
plt.close('all')
np.save(directory_1+'/mask.npy', new_mask)

plt.imshow(new_image)
plt.axis('off')
plt.savefig(directory_1+'/masked_image.png')
plt.close('all')
np.save(directory_1+'/masked_image.npy', new_image)

Q_11 = [minx-1, miny-1]
Q_12 = [minx-1, maxy+1]
Q_21 = [maxx+1, miny-1]
Q_22 = [maxx+1, maxy+1]

np.save(directory_1+'/points.npy', [Q_11, Q_12, Q_21, Q_22])
