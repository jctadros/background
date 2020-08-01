import os, sys, argparse, math
import numpy as np
import matplotlib.pyplot as plt
from linear import Interpol
from matplotlib import ticker, cm

arg_parser  = argparse.ArgumentParser()
arg_parser.add_argument('-fn', '--file_name', required=True, help=' file name without extension')
arg_parser.add_argument('-v', '--version', required=True, help=' file name without extension')
arg_parser.add_argument('-mode', '--mode', required=True, help=' rect or Otsu mode')
arg_parser.add_argument('-m', '--m', required=False, help=' rect or Otsu mode')

args = vars(arg_parser.parse_args())
file_name = args['file_name']
version = int(args['version'])
mode = args['mode']
m = args['m']

if mode == 'rect':
    if m == 'sim':
        image_path  = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/rect/sim/ROI_'+str(version)+'/masked_image.npy'
        mask_path   = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/rect/sim/ROI_'+str(version)+'/mask.npy'
        output_path = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/rect/sim/ROI_'+str(version)+'/linear'
        coord_path  = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/rect/sim/ROI_'+str(version)+'/contour_coord.npy'
        directory_1 = output_path + '/iterations'
        directory_2 = output_path + '/updatedMask'
    else:
        image_path  = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/rect/ROI_'+str(version)+'/masked_image.npy'
        mask_path   = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/rect/ROI_'+str(version)+'/mask.npy'
        output_path = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/rect/ROI_'+str(version)+'/linear'
        coord_path  = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/rect/ROI_'+str(version)+'/contour_coord.npy'
        directory_1 = output_path + '/iterations'
        directory_2 = output_path + '/updatedMask'

if mode == 'otsu':
    image_path  = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/ROI_'+str(version)+'/masked_image.npy'
    mask_path   = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/ROI_'+str(version)+'/mask.npy'
    output_path = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/ROI_'+str(version)+'/linear'
    coord_path  = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/ROI_'+str(version)+'/contour_coord.npy'
    directory_1 = output_path + '/iterations'
    directory_2 = output_path + '/updatedMask'

directory = [directory_1, directory_2]
for dir in directory:
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
    except OSError:
        print 'Error: Creating directory ' + dir

originalImage = np.load(image_path)
mask = np.load(mask_path)

[xcoord, ycoord] = np.load(coord_path)
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
        mu, std = np.nanmedian(zoom_float), np.nanstd(zoom_float)
        for x in range(zoom_float.shape[0]):
            for y in range(zoom_float.shape[1]):
                if np.absolute(zoom_float[x][y]-mu) >= 5*std:
                    zoom_float[x][y] = np.nan
    else:
        zoom_float = float_result[cy-sh:cy+sh, cx-sh:cx+sh]
        mu, std = np.nanmedian(zoom_float), np.nanstd(zoom_float)
        for x in range(zoom_float.shape[0]):
            for y in range(zoom_float.shape[1]):
                if np.absolute(zoom_float[x][y]-mu) >= 5*std:
                    zoom_float[x][y] = np.nan

plt.imshow(zoom_float, cmap=cm.seismic)
plt.tight_layout()
plt.savefig(output_path+'/linear_interpol_image.png')
plt.close(f)
np.save(output_path+'/linear_interpol_image.npy', float_result)

if mode == 'rect':
    if m == 'sim':
        points_path = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/rect/sim/ROI_'+str(version)+'/points.npy'
        points = np.load(points_path)
        Q_11, Q_12, Q_21, Q_22 = points[0], points[1], points[2], points[3]
        residual_im = np.zeros((originalImage.shape[0], originalImage.shape[1]))
        org_im_path = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/Otsu/masked_image.npy'
        org_im = np.load(org_im_path)
        l_r = []
        for x in range(Q_11[0], Q_22[0]+1):
            for y in range(Q_11[1], Q_22[1]+1):
                l_r.append( (org_im[x][y] - float_result[x][y])**2)

        RMSE = np.sqrt(np.nanmean(l_r))
        dir = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/rect/sim/ROI_'+str(version)+'/linear'
        np.save(dir+'/RMSE.npy', [RMSE, (Q_11[0]-Q_22[0]-1) * (Q_11[1]-Q_22[1]-1)])
