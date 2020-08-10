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

err_inp = []
err_lin = []
err_bil = []
err_im_inp = np.zeros((mask.shape[0], mask.shape[1]))
err_im_lin = np.zeros((mask.shape[0], mask.shape[1]))

if mode == 'rect':
    err_im_bil = np.zeros((mask.shape[0], mask.shape[1]))

for x in range(mask.shape[0]):
    for y in range(mask.shape[1]):
        if mask[x][y] == 255:
            err_inp.append((inp[x][y] - org[x][y])**2)
            err_lin.append((lin[x][y] - org[x][y])**2)
            if mode == 'rect':
                err_bil.append((bil[x][y] - org[x][y])**2)

            err_im_inp[x][y] = err_inp[-1]
            err_im_lin[x][y] = err_lin[-1]
            if mode == 'rect':
                err_im_bil[x][y] = err_bil[-1]
        else:
            lin[x][y] = np.nan
            inp[x][y] = np.nan
            if mode == 'rect':
                bil[x][y] = np.nan

            org[x][y] = np.nan
            err_im_inp[x][y] = np.nan
            err_im_lin[x][y] = np.nan
            if mode == 'rect':
                err_im_bil[x][y] = np.nan

mean_err_inp, mean_err_lin  = np.nanmean(err_im_inp), np.nanmean(err_im_lin)
if mode == 'rect':
    mean_err_bil = np.nanmean(err_im_bil)

rmse_inp, rmse_lin = np.sqrt(mean_err_inp), np.sqrt(mean_err_lin)
if mode == 'rect':
    rmse_bil = np.sqrt(mean_err_bil)

print 'rmse_inp = ', mean_err_inp
print 'rmse_lin = ', mean_err_lin

if mode == 'rect':
    print 'rmse_bil = ', mean_err_bil
