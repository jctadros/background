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
args = vars(arg_parser.parse_args())
file_name = args['file_name']

directory_1 = output_path + str(file_name) + '/Otsu'
directory_2 = output_path + str(file_name) + '/recon/ROI_0'

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
masked_image, mask, x_contour, y_contour = interactive_Otsu(info, zoom, corner_coord, file_name, directory_1)

for idx, pic in enumerate([masked_image, mask]):
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
np.save(directory_1+'/zoom-im.npy', zoom)

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
