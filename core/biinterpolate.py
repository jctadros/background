import os, time, argparse
import numpy as np
import matplotlib.pyplot as plt
from UTILS import bilinearInterpol
from matplotlib import ticker, cm

arg_parser   = argparse.ArgumentParser()
arg_parser.add_argument("-fn", "--file_name", required=True, help="  file name without extension")
arg_parser.add_argument("-v", "--version", required=True, help="  file name without extension")
arg_parser.add_argument("-mode", "--mode", required=True, help=" rect or sim")

args = vars(arg_parser.parse_args())
file_name = args['file_name']
version = args['version']
mode = args['mode']

output_path  = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'
directory_1 = output_path + str(file_name) + '/Otsu'
directory_2 = output_path + str(file_name) + '/analysis/ROI_' + str(version)
directory_3 = output_path + str(file_name) + '/analysis/rect/ROI_' + str(version)

if mode == 'rect':
    image_path  = directory_3 + '/masked_image.npy'
    points_path = directory_3 + '/points.npy'
    output_path = directory_3 + '/bilinear'
    coord_path  = directory_3 + '/contour_coord.npy'

if not os.path.exists(dir):
    os.makedirs(dir)

try:
    originalImage = np.load(image_path)
    points = np.load(points_path)
    [xcoord, ycoord] = np.load(coord_path)
except:
    print('Error: file not available')
    exit(1)

Q_11, Q_12, Q_21, Q_22 = points[0], points[1], points[2], points[3]
cx = int(np.mean(xcoord))
cy = int(np.mean(ycoord))

#TESTING
if True:
    originalImage[Q_11[0], Q_11[1]] = np.nan
    originalImage[Q_22[0], Q_22[1]] = np.nan

    plt.imshow(originalImage)
    plt.show()
    exit()

recon_im, residual_im, RMSE = bilinearInterpol(Q_11, Q_12, Q_21, Q_22, originalImage, file_name)
np.save(dir+'/RMSE.npy', [RMSE, (Q_11[0]-Q_22[0]-1) * (Q_11[1]-Q_22[1]-1)])

for x in range(Q_11[0], Q_22[0]+1):
    for y in range(Q_11[1], Q_22[1]+1):
        originalImage[x][y] = recon_im[x][y]


sh = 100
if mode == 'rect':
    if version == 0:
        cropimage = originalImage[cx-sh:cx+sh+1, cy-sh:cy+sh+1]
    else:
        cropimage = originalImage[cy-sh:cy+sh+1, cx-sh:cx+sh+1]
else:
    cropimage = originalImage[cx-sh:cx+sh+1, cy-sh:cy+sh+1]

plt.imshow(cropimage, cmap=cm.seismic)
plt.axis('off')
plt.savefig(output_path+'/crop_reconstruction.png')
plt.close('all')

mu, std = np.nanmedian(originalImage), np.nanstd(originalImage)
for x in range(originalImage.shape[0]):
    for y in range(originalImage.shape[1]):
        if np.absolute(originalImage[x][y]-mu) >= 4*std:
            originalImage[x][y] = np.nan

plt.imshow(originalImage, cmap=cm.seismic)
plt.axis('off')
plt.savefig(output_path+'/reconstruction.png')
plt.close('all')

np.save(output_path+'/bilinear.npy', recon_im)
np.save(output_path+'/reconstruction.npy', originalImage)
