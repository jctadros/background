import os, sys, argparse, math
import numpy as np
import matplotlib.pyplot as plt
from linearizer import Interpol
from matplotlib import ticker, cm

arg_parser  = argparse.ArgumentParser()
arg_parser.add_argument('-fn', '--file_name', required=True, help=' file name without extension')
arg_parser.add_argument('-v', '--version', required=True, help=' file name without extension')
arg_parser.add_argument('-mode', '--mode', required=True, help=' rect or Otsu mode')

args = vars(arg_parser.parse_args())
file_name = args['file_name']
version = int(args['version'])
mode = args['mode']

output_path = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'
directory_1 = output_path + str(file_name) + '/Otsu'
directory_2 = output_path + str(file_name) + '/analysis/ROI_' + str(version)
directory_3 = output_path + str(file_name) + '/analysis/rect/ROI_' + str(version)

if mode == 'rect':
    image_path  = directory_3 + '/masked_image.npy'
    mask_path   = directory_3 + '/mask.npy'
    output_path = directory_3 + '/linear'
    coord_path  = directory_3 + '/contour_coord.npy'
    directory_4 = output_path + '/iterations'
    directory_5 = output_path + '/updatedMask'

if mode == 'otsu':
    image_path  = directory_2 + '/masked_image.npy'
    mask_path   = directory_2 +'/mask.npy'
    output_path = directory_2 +'/linear'
    coord_path  = directory_2 +'/contour_coord.npy'
    directory_4 = output_path + '/iterations'
    directory_5 = output_path + '/updatedMask'

for dir in [directory_4, directory_5]:
    if not os.path.exists(dir):
        os.makedirs(dir)

try:
    originalImage = np.load(image_path)
    mask = np.load(mask_path)
    [xcoord, ycoord] = np.load(coord_path)
except:
    print('Error: file not available')
    exit(1)

cx = int(np.mean(xcoord))
cy = int(np.mean(ycoord))
i = Interpol(originalImage, mask, None)
i.Linear(file_name, output_path)
result = i.result

float_result = (result*(np.nanmax(originalImage)-np.nanmin(originalImage)))/(2**8 - 1)+np.nanmin(originalImage)
mean, std = np.nanmean(float_result), np.nanstd(float_result)
for x in range(originalImage.shape[0]):
    for y in range(originalImage.shape[1]):
        if math.isnan(originalImage[x, y]):
            if mask[x, y] == 0:
                float_result[x, y] = 'nan'

f = plt.figure()
ax = f.add_subplot(111)
ax.axis('off')
sh = 100
if mode == 'rect':
    if version == 0:
        zoom_float = float_result[cx-sh:cx+sh, cy-sh:cy+sh]
    else:
        zoom_float = float_result[cy-sh:cy+sh, cx-sh:cx+sh]

if mode == 'otsu':
    if version == 0:
        co = np.load(coord_path)
        xc , yc = co[0], co[1]
        [x, y] = [[0,float_result.shape[0]], [float_result.shape[1], 0]]
        xm, ym = np.mean(xc), np.mean(yc)
        center_x = int(np.mean(xc-xm+float(x[0]+x[1])/2))
        center_y = int(np.mean(yc-ym+float(y[0]+y[1])/2))

        zoom_float = float_result[center_x-sh:center_x+sh+1, center_y-sh:center_y+sh+1]

    else:
        zoom_float = float_result[cy-sh:cy+sh, cx-sh:cx+sh]

    mu, std = np.nanmedian(zoom_float), np.nanstd(zoom_float)
    for x in range(zoom_float.shape[0]):
        for y in range(zoom_float.shape[1]):
            if np.absolute(zoom_float[x][y]-mu) >= 3*std:
                zoom_float[x][y] = np.nan

plt.imshow(zoom_float, cmap=cm.seismic)
plt.tight_layout()
plt.savefig(output_path+'/linear_interpol_image.png')
plt.close(f)
np.save(output_path+'/linear_interpol_image.npy', float_result)
