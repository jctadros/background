import numpy as np
import os, argparse, warnings
import matplotlib.pyplot as plt

from control import interactive_ROI, interactive_Otsu

warnings.filterwarnings("ignore")

arg_parser   = argparse.ArgumentParser()
arg_parser.add_argument("-fn", "--file_name", required=True, help=" include fits file name without the extension")
args = vars(arg_parser.parse_args())
file_name = args['file_name']

os.chdir("..")
image_path = os.path.abspath(os.curdir) + '/images/'
output_path = image_path
directory_1 = output_path + file_name
directory_2 = directory_1 + '/ROI_0'

if not os.path.exists(directory_2):
  os.makedirs(directory_2)
 
try:
  path = image_path + file_name + '.npy'
  info   = np.load(path)
except IOError:
    print ('Error: File not found in directory.')
    exit(1)

zoom, corner_coord = interactive_ROI(info, directory_1)
interactive_Otsu(info, zoom, corner_coord, file_name, directory_1, directory_2)
