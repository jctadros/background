import os, time, argparse
import numpy as np
import matplotlib.pyplot as plt
from UTILS2 import bilinearInterpol
from matplotlib import ticker, cm

arg_parser   = argparse.ArgumentParser()
arg_parser.add_argument("-fn", "--file_name", required=True, help="  file name without extension")
arg_parser.add_argument("-v", "--version", required=True, help="  file name without extension")
arg_parser.add_argument("-mode", "--mode", required=True, help=" rect or sim")

args = vars(arg_parser.parse_args())
file_name = args['file_name']
version = args['version']
mode = args['mode']

if mode == 'rect':
    image_path  = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/rect/ROI_'+str(version)+'/masked_image.npy'
    points_path = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/rect/ROI_'+str(version)+'/points.npy'
    output_path = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/rect/ROI_'+str(version)+'/bilinear'
    coord_path  = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/rect/ROI_'+str(version)+'/contour_coord.npy'
elif mode == 'sim':
    image_path  = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/rect/sim/ROI_'+str(version)+'/masked_image.npy'
    points_path = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/rect/sim/ROI_'+str(version)+'/points.npy'
    output_path = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/rect/sim/ROI_'+str(version)+'/bilinear'
    coord_path  = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/rect/sim/ROI_'+str(version)+'/contour_coord.npy'

directory = [output_path]
for dir in directory:
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
    except OSError:
        print 'Error: Creating directory ' + dir

originalImage = np.load(image_path)
points = np.load(points_path)
Q_11, Q_12, Q_21, Q_22 = points[0], points[1], points[2], points[3]
'''
originalImage[Q_11[0], Q_11[1]] = np.nan
originalImage[Q_22[0], Q_22[1]] = np.nan

plt.imshow(originalImage)
plt.show()
exit()
'''

recon_im, residual_im, RMSE = bilinearInterpol(Q_11, Q_12, Q_21, Q_22, originalImage, file_name)
np.save(dir+'/RMSE.npy', [RMSE, (Q_11[0]-Q_22[0]-1) * (Q_11[1]-Q_22[1]-1)])

for x in range(Q_11[0], Q_22[0]+1):
    for y in range(Q_11[1], Q_22[1]+1):
        originalImage[x][y] = recon_im[x][y]

[xcoord, ycoord] = np.load(coord_path)
cx = int(np.mean(xcoord))
cy = int(np.mean(ycoord))
sh = 100

if mode == 'rect':
    cropimage = originalImage[cy-sh:cy+sh+1, cx-sh:cx+sh+1]
else:
    cropimage = originalImage[cx-sh:cx+sh+1, cy-sh:cy+sh+1]

'''
mean, std = np.nanmean(cropimage), np.nanstd(cropimage)
for x in range(cropimage.shape[0]):
    for y in range(cropimage.shape[1]):
        if np.absolute(cropimage[x,y]-mean) > 2*std:
            cropimage[x,y] = 'nan'
'''

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
