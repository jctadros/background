import numpy as np
import os, sys, argparse
#from astropy import wcs
import astropy.io.fits as fits
import matplotlib.pyplot as plt
from matplotlib import ticker, cm
import matplotlib.widgets as widgets
import matplotlib.patches as patches
import matplotlib

image_path   = '/Users/jeantad/Desktop/new_crab/DATA_TEST/'
output_path  = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'
arg_parser   = argparse.ArgumentParser()
arg_parser.add_argument("-fn", "--file_name", required=True, help="  file name without extension")
arg_parser.add_argument("-v", "--version", required=True, help="  version")
args = vars(arg_parser.parse_args())
file_name = args['file_name']
version = args['version']
pass_accept  = True

path   = image_path + file_name + '.fits'
mask = np.load('/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/ROI_'+str(version)+'/mask.npy')
xc, yc, c = 0, 0, 0
for x in range(mask.shape[0]):
    for y in range(mask.shape[1]):
        if mask[x,y] == 255:
            c  += 1
            xc += x
            yc += y

xc, yc = xc/c, yc/c
original_im = fits.open(path)[1].data
masked_im   = np.load('/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/ROI_'+str(version)+'/masked_image.npy')
inpaint_im  = np.load('/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/ROI_'+str(version)+'/inpainting/inpainted_image.npy')
linear_im   = np.load('/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/ROI_'+str(version)+'/linear/linear_interpol_image.npy')
contour     = np.load('/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/Otsu/contours.npy')

out, ph = [], 110

coord = []
total = []

for idx, image in enumerate([masked_im, inpaint_im, linear_im, original_im]):

    if idx==0:
        for x in range(image.shape[0]):
            for y in range(image.shape[1]):
                if mask[x][y] == 255:
                    coord.append((x,y))
    else:
        pix = []
        for elem in range(len(coord)):
            pix.append(image[coord[elem][0]][coord[elem][1]])
        total.append(np.sum(pix))

print total

exit()

for idx, image in enumerate([original_im, masked_im, inpaint_im, linear_im]):
    if idx == 1:
        mean, std = np.nanmean(image), np.nanstd(image)
        for x in range(image.shape[0]):
            for y in range(image.shape[1]):
                if np.absolute(image[x,y]-mean)>10000*std:
                    image[x,y] = np.nan
                    out.append((x,y))

    elif idx!=0:
        for elem in out:
            image[elem[0], elem[1]] = np.nan

    to_show = image[xc-ph:xc+ph, yc-ph:yc+ph]
    '''
    xsize, ysize = to_show.shape[0], to_show.shape[1]

    X = np.arange(0, ysize, 1)
    Y = np.arange(0, xsize, 1)
    X, Y = np.meshgrid(X, Y)

    if idx==0 or idx==1:
        min, max = np.nanmin(to_show), np.nanmax(to_show)

    fig = plt.figure()
    ax  = fig.add_subplot(111, aspect='equal')
    ax.invert_yaxis()
    ax.axis('off')
    plt.contour(Y, X, to_show.T, 10, cmap=cm.seismic, vmin=min, vmax=max, origin='upper')
    plt.plot(contour[0]+xc-2*ph-7, contour[1]+yc-2*ph-1, 'black', label='Source footprint')
    plt.legend(loc='lower right')
    plt.tight_layout()
    plt.show()
    '''

    if idx==0 or idx==1:
        min, max = np.nanmin(to_show), np.nanmax(to_show)

    fig = plt.figure()
    ax  = fig.add_subplot(111, aspect='equal')
    ax.axis('off')
    plt.imshow(to_show, cmap=cm.seismic, vmin=min, vmax=max, origin='upper')
    plt.plot(contour[0]+xc-2*ph-7, contour[1]+yc-2*ph-1, 'black', label='Source footprint')
    plt.legend(loc='lower right')
    plt.tight_layout()
    plt.show()
    plt.close('all')
