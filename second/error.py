import numpy as np
import matplotlib.pyplot as plt
import os, sys, argparse, math
import astropy.io.fits as fits

arg_parser  = argparse.ArgumentParser()
arg_parser.add_argument('-fn', '--file_name', required=True, help=' file name without extension')
arg_parser.add_argument('-v', '--version', required=True, help=' file name without extension')
arg_parser.add_argument('-mode', '--mode', required=True, help=' rect or Otsu mode')
arg_parser.add_argument("-size", "--size", required=False, help=" size of rect")

args = vars(arg_parser.parse_args())
file_name = args['file_name']
version = args['version']
mode = args['mode']
if mode == 'rect': size = args['size']

if mode == 'otsu':
    mask = np.load('/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/otsu/ROI_'+str(version)+'/mask.npy')
    inp  = np.load('/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/otsu/ROI_'+str(version)+'/inpainting/inpainted_image.npy')
    lin  = np.load('/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/otsu/ROI_'+str(version)+'/linear/linear_interpol_image.npy')

if mode == 'rect':
    mask = np.load('/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/rect/'+str(size)+'/ROI_'+str(version)+'/mask.npy')
    inp  = np.load('/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/rect/'+str(size)+'/ROI_'+str(version)+'/inpainting/inpainted_image.npy')
    lin  = np.load('/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/rect/'+str(size)+'/ROI_'+str(version)+'/linear/linear_interpol_image.npy')
    bil  = np.load('/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/rect/'+str(size)+'/ROI_'+str(version)+'/bilinear/reconstruction.npy')

image_path  = '/Users/jeantad/Desktop/new_crab/DATA_TEST/'
path = image_path + file_name + '.fits'
org = fits.open(path)[1].data

err_inp = []
err_lin = []
err_bil = []
org_l = []
inp_l = []
lin_l = []

err_im_inp = np.zeros((mask.shape[0], mask.shape[1]))
err_im_lin = np.zeros((mask.shape[0], mask.shape[1]))
if mode == 'rect':
    err_im_bil = np.zeros((mask.shape[0], mask.shape[1]))

for x in range(mask.shape[0]):
    for y in range(mask.shape[1]):
        if mask[x][y] == 255:
            err_inp.append((inp[x][y] - org[x][y])**2)
            err_lin.append((lin[x][y] - org[x][y])**2)
            err_im_inp[x][y] = inp[x][y] - org[x][y]
            err_im_lin[x][y] = lin[x][y] - org[x][y]

            org_l.append(org[x][y])
            inp_l.append(inp[x][y])
            lin_l.append(lin[x][y])
            if mode == 'rect':
                err_bil.append((bil[x][y] - org[x][y])**2)

        else:
            lin[x][y] = np.nan
            inp[x][y] = np.nan
            org[x][y] = np.nan
            err_im_inp[x][y] = np.nan
            err_im_lin[x][y] = np.nan
            if mode == 'rect':
                bil[x][y] = np.nan

def better_histogram(array):
    val = []
    for x in range(array.shape[0]):
        for y in range(array.shape[1]):
            if np.isnan(array[x][y]): continue
            else: val.append(array[x][y])
    val = np.array(val)
    return plt.hist(val, 255)

org_h, lin_h, inp_h = better_histogram(org), better_histogram(lin), better_histogram(inp)

def _distance(x, y):
    distance = 0
    for i in range(len(x)):
        if x[i] == 0 and y[i] == 0:
            distance += 0
        else:
            distance += ((x[i]-y[i])**2)/(x[i]+y[i])
    return 0.5*distance

print ''
print 'linear  = ', _distance(org_h[0], lin_h[0])
print 'inpaint = ', _distance(org_h[0], inp_h[0])

if mode == 'rect':
    bil_h = better_histogram(bil)
    print 'biinter = ', _distance(org_h[0], bil_h[0])

plt.show()
