import numpy as np
import os, sys, argparse, warnings
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
from matplotlib.colors import LogNorm
from matplotlib.ticker import MultipleLocator
from matplotlib import ticker, cm

from astropy import wcs
import astropy.io.fits as fits
from control import interactive_ROI, interactive_Otsu

warnings.filterwarnings("ignore")

image_path   = '/Users/jeantad/Desktop/new_crab/DATA_TEST/'
output_path  = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'

arg_parser   = argparse.ArgumentParser()
arg_parser.add_argument("-fn", "--file_name", required=True, help="  file name without extension")
arg_parser.add_argument("-mode", "--mode", required=True, help=" rectangular or Otsu mode")
args = vars(arg_parser.parse_args())
file_name = args['file_name']
mode = args['mode']

directory_1 = output_path + str(file_name) + '/Otsu'
directory_2 = output_path + str(file_name) + '/analysis/otsu/ROI_0'
directory_3 = output_path + str(file_name) + '/analysis/rect/ROI_0'

if mode == 'rect':
    try:
        masked_image = np.load(directory_2+'/masked_image.npy')
        mask = np.load(directory_2+'/mask.npy')
    except IOError:
        print('Error: file not found. -mode otsu first')
        exit(1)

    new_image, new_mask = np.copy(masked_image), np.copy(mask)

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

    try:
        if not os.path.exists(directory_3):
            os.makedirs(directory_3)
    except OSError:
            print ('Error: Creating directory. ' + directory_3)

    plt.imshow(new_mask)
    plt.axis('off')
    plt.savefig(directory_3+'/mask.png')
    plt.close('all')
    np.save(directory_3+'/mask.npy', new_mask)

    plt.imshow(new_image)
    plt.axis('off')
    plt.savefig(directory_3+'/masked_image.png')
    plt.close('all')
    np.save(directory_3+'/masked_image.npy', new_image)

    Q_11 = [minx-1, miny-1]
    Q_12 = [minx-1, maxy+1]
    Q_21 = [maxx+1, miny-1]
    Q_22 = [maxx+1, maxy+1]

    contour_coord = [[], []]
    for x in range(Q_11[0], Q_22[0]+1):
        contour_coord[0].append(x)
        contour_coord[1].append(Q_11[1])
        contour_coord[0].append(x)
        contour_coord[1].append(Q_22[1])

    for y in range(Q_11[1], Q_22[1]+1):
        contour_coord[1].append(y)
        contour_coord[0].append(Q_11[0])
        contour_coord[1].append(y)
        contour_coord[0].append(Q_22[0])

    np.save(directory_3+'/contour_coord.npy', contour_coord)
    np.save(directory_3+'/points.npy', [Q_11, Q_12, Q_21, Q_22])

elif mode == 'otsu':
    try:
        path   = image_path + file_name + '.fits'
        #TODO: Make sure the image is always in [1] and header is in [0]
        info   = fits.open(path)[1].data
        header = fits.open(path)[0].header

        for dir in [directory_1, directory_2]:
          #to not override the files each time, we only create them once
          if not os.path.exists(dir):
            os.makedirs(dir)

    except IOError:
        print ('Error: File not found in directory.')
        exit(1)
    
    corner_coord, zoom = interactive_ROI(info)
    np.save(output_path+str(file_name)+'/Otsu/roi.npy', zoom)
    
    image, mask, x_contour, y_contour = interactive_Otsu(info, zoom, corner_coord, file_name, directory_1)
    im_zoom = image[int(np.min(y)):int(np.max(y)), int(np.min(x)):int(np.max(x))]

    for idx, pic in enumerate([image, mask]):
        fig = plt.figure()
        ax  = fig.add_subplot(111)
        ax.axis('off')
        plt.imshow(pic)
        if idx==0:
            plt.savefig(directory_1+'/masked_image.png')
            plt.savefig(directory_2+'/masked_image.png')
            np.save(directory_1+'/masked_image.npy', image)
            np.save(directory_2+'/masked_image.npy', image)
        elif idx ==1:
            plt.savefig(directory_1+'/mask.png')
            plt.savefig(directory_2+'/mask.png')
            np.save(directory_1+'/mask.npy', pic)
            np.save(directory_2+'/mask.npy', pic)

    np.save(directory_1+'/contour_coord.npy', [x_contour, y_contour])
    np.save(directory_2+'/contour_coord.npy', [x_contour,y_contour])
    np.save(directory_1+'/zoom.npy', [x, y])

    fig = plt.figure()
    ax  = fig.add_subplot(111)
    ax.axis('off')
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    plt.imshow(zoom)
    plt.plot(x_contour, y_contour, 'r', alpha=0.5, label='Source Footprint')
    plt.legend(loc='lower right')
    plt.savefig('/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/Otsu/roi.png')
    plt.close('all')
