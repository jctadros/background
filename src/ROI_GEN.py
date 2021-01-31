import numpy as np
import os, argparse, warnings
import matplotlib.pyplot as plt
import astropy.io.fits as fits
from control import interactive_ROI, interactive_Otsu

warnings.filterwarnings("ignore")

arg_parser   = argparse.ArgumentParser()
arg_parser.add_argument("-fn", "--file_name", required=True, help=" include fits file name without the extension")
args = vars(arg_parser.parse_args())
file_name = args['file_name']

image_path   = '/Users/jeantad/Desktop/new_crab/DATA_TEST/'
output_path  = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'
directory_1 = output_path + file_name
directory_2 = directory_1 + '/ROI_0'

try:
  #TODO: Include image in arguments
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

zoom, corner_coord = interactive_ROI(info, directory_1)
interactive_Otsu(info, zoom, corner_coord, file_name, directory_1, directory_2)
