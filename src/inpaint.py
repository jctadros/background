import os, sys, argparse, math
import numpy as np
import matplotlib.pyplot as plt
from inpainter import Inpainter
import matplotlib.widgets as widgets
from matplotlib import ticker, cm
import time

arg_parser  = argparse.ArgumentParser()
arg_parser.add_argument('-fn', '--file_name', required=True, help=' file name without extension')
arg_parser.add_argument('-v', '--version', required=True, type=int, help=' file name without extension')
arg_parser.add_argument('-hpw','--half_patch_width', required=False, type=int, default=4,  help= 'half patch width')
arg_parser.add_argument('-select', '--select', required=False, type=bool, default=True,  help='select source region')

args = vars(arg_parser.parse_args())
file_name = args['file_name']
version = args['version']
select = args['select']
halfPatchWidth = args['half_patch_width']

output_path = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'
directory_1 = output_path + file_name + '/ROI_' + str(version)
directory_2 = directory_1 + '/inpainting'
directory_3 = directory_2 + '/iterations'
directory_4 = directory_2 + '/updatedMask'
directory_5 = directory_2 + '/positionTrack'

image_path  = directory_1 + '/masked_image.npy'
mask_path   = directory_1 + '/mask.npy'
coord_path  = directory_1 + '/contour_coord.npy'
zoom = output_path + file_name + '/zoom.npy'

for dir in [directory_3, directory_4, directory_5]:
    if not os.path.exists(dir):
        os.makedirs(dir)

try:
    originalImage = np.load(image_path)
    inpaintMask = np.load(mask_path)
except IOError:
    print 'Error: File not found'
    exit(1)

if select:
    def on_key(event):
        global pass_accept
        if event.key == 'enter':
            pass_accept = False
            plt.close('all')
        elif event.key == 'backspace':
            pass_accept = True
            plt.close('all')

    def onselect(eclick, erelease):
        global yr, yl, xl, xr
        if eclick.ydata > erelease.ydata:
            eclick.ydata, erelease.ydata = erelease.ydata, eclick.ydata
        if eclick.xdata > erelease.xdata:
            eclick.xdata, erelease.xdata = erelease.xdata, eclick.xdata
        x[:] = eclick.xdata, erelease.xdata
        y[:] = eclick.ydata, erelease.ydata
        xr, xl = ax.set_xlim(int(min(x)), int(max(x)))
        yr, yl = ax.set_ylim(int(max(y)), int(min(y)))
        fig.canvas.mpl_connect("key_press_event", on_key)

    pass_accept = True
    while pass_accept:
        fig = plt.figure()
        ax  = fig.add_subplot(111)
        x, y = [], []
        rs = widgets.RectangleSelector(
                     ax, onselect, drawtype='box',
                     rectprops = dict(facecolor='red',
                     edgecolor='black', alpha=0.2, fill=True))

        vmin, vmax = np.nanmin(originalImage), np.nanmax(originalImage)
        ax.axis('off')
        plt.imshow(originalImage)
        plt.show()

    crop_originalImage = originalImage[yl:yr, xr:xl]
    fig = plt.figure()
    ax  = fig.add_subplot(111)
    ax.axis('off')
    plt.imshow(crop_originalImage, vmin=vmin, vmax=vmax)
    fig.canvas.mpl_connect("key_press_event", on_key)

    crop_inpaintMask = inpaintMask[yl:yr, xr:xl]
    fig = plt.figure()
    ax  = fig.add_subplot(111)
    ax.axis('off')
    plt.imshow(crop_inpaintMask, vmin=vmin, vmax=vmax)
    plt.close('all')
    time.sleep(1)
    crop_gray_originalImage = np.uint16(np.round(((2**16 - 1)*(crop_originalImage-np.nanmin(originalImage)))/(np.nanmax(originalImage)-np.nanmin(originalImage))))

else:
    crop_gray_originalImage = None
    crop_inpaintMask = None
    yl, xr = 0, 0

gray_originalImage = np.uint16(np.round(((2**16 - 1)*(originalImage-np.nanmin(originalImage)))/(np.nanmax(originalImage)-np.nanmin(originalImage))))
model = Inpainter(gray_originalImage, inpaintMask, crop_gray_originalImage, crop_inpaintMask, halfPatchWidth, select)
model.inpaint(file_name, directory_2 , yl, xr)

result = model.result
float_result = (result*(np.nanmax(originalImage)-np.nanmin(originalImage)))/(2**16 - 1)+np.nanmin(originalImage)
for x in range(originalImage.shape[0]):
    for y in range(originalImage.shape[1]):
        if math.isnan(originalImage[x, y]):
            if inpaintMask[x, y] == 0:
                float_result[x, y] = 'nan'

[xcoord, ycoord] = np.load(coord_path)
cx = int(np.nanmean(xcoord))
cy = int(np.nanmean(ycoord))

f = plt.figure()
ax  = f.add_subplot(111)
ax.axis('off')
sh = 100

if version==0:
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
plt.savefig(directory_2 + '/inpainted_image.png')
plt.tight_layout()
plt.close(f)
np.save(directory_2 + '/inpainted_image.npy', float_result)
