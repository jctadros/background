import numpy as np
import matplotlib.pyplot as plt
import os, sys, argparse, math
import astropy.io.fits as fits

arg_parser  = argparse.ArgumentParser()
arg_parser.add_argument('-fn', '--file_name', required=True, help=' file name without extension')
arg_parser.add_argument('-v', '--version', required=True, help=' file name without extension')
arg_parser.add_argument('-mode', '--mode', required=True, help=' rect or Otsu mode')

args = vars(arg_parser.parse_args())
file_name = args['file_name']
version = args['version']
mode = args['mode']


if mode == 'otsu':
    mask = np.load('/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/ROI_'+str(version)+'/mask.npy')
    inp  = np.load('/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/ROI_'+str(version)+'/inpainting/inpainted_image.npy')
    lin  = np.load('/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/ROI_'+str(version)+'/linear/linear_interpol_image.npy')
if mode == 'rect':
    mask = np.load('/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/rect/ROI_'+str(version)+'/mask.npy')
    inp  = np.load('/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/rect/ROI_'+str(version)+'/inpainting/inpainted_image.npy')
    lin  = np.load('/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/rect/ROI_'+str(version)+'/linear/linear_interpol_image.npy')
    bil  = np.load('/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/rect/ROI_'+str(version)+'/bilinear/reconstruction.npy')

image_path  = '/Users/jeantad/Desktop/new_crab/DATA_TEST/'
path = image_path + file_name + '.fits'
org = fits.open(path)[1].data

x_l = []
y_l = []
for x in range(org.shape[0]):
    for y in range(org.shape[1]):
        if mask[x][y] == 255:
            x_l.append(x)
            y_l.append(y)

        else:
            lin[x][y] = np.nan
            inp[x][y] = np.nan
            org[x][y] = np.nan
            if mode == 'rect':
                bil[x][y] = np.nan

for im in [org, inp]:
    plt.imshow(im[np.min(x_l):np.max(x_l), np.min(y_l):np.max(y_l)])
    plt.show()

#amin maalouf samarkamb
#jihan omar khayam
