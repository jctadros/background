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

arg_parser   = argparse.ArgumentParser()
arg_parser.add_argument("-fn", "--file_name", required=True, help="  file name without extension")
args = vars(arg_parser.parse_args())
file_name = args['file_name']

image_path   = '/Users/jeantad/Desktop/new_crab/DATA_TEST/'
output_path  = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'
directory_1 = output_path + str(file_name)
directory_2 = directory_1 + '/ROI_0'

try:
  path   = image_path + file_name + '.fits'
  #TODO: Make sure the image is always in [1] and header is in [0]
  info   = fits.open(path)[1].data
  header = fits.open(path)[0].header
  #to not override the files each time, we only create them once
  if not os.path.exists(directory_2):
    os.makedirs(directory_2)
  
except IOError:
    print ('Error: File not found in directory.')
    exit(1)

corner_coord, zoom = interactive_ROI(info)
masked_image, mask, x_contour, y_contour = interactive_Otsu(info, zoom, corner_coord, file_name, directory_1)

fig = plt.figure()
ax  = fig.add_subplot(111)
ax.axis('off')
plt.imshow(masked_image)
plt.savefig(directory_1+'/masked_image.png')
plt.savefig(directory_2+'/masked_image.png')
plt.close('all')

fig = plt.figure()
ax  = fig.add_subplot(111)
ax.axis('off')
plt.imshow(mask)
plt.savefig(directory_1+'/mask_image.png')
plt.savefig(directory_2+'/mask_image.png')
plt.close('all')

np.save(directory_1+'/masked_data.npy', masked_image)
np.save(directory_2+'/masked_data.npy', masked_image)
np.save(directory_1+'/mask_data.npy', mask)
np.save(directory_2+'/mask_data.npy', mask)
np.save(directory_1+'/contour_coord.npy', [x_contour, y_contour])
np.save(directory_2+'/contour_coord.npy', [x_contour,y_contour])
np.save(directory_1+'/zoom_coord.npy', [corner_coord[0], corner_coord[1]])
np.save(directory_1+'/zoom_data.npy', zoom)
