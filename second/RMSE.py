import os, sys, argparse, math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker, cm

def better_histogram(array, nbins=255):
    val = []
    for i in array:
        if np.isnan(i): continue
        else: val.append(i)
    val = np.array(val)
    hist, bin_edges = np.histogram(val, nbins)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.
    plt.hist(val, bins=nbins)

    return hist, bin_centers

arg_parser  = argparse.ArgumentParser()
arg_parser.add_argument('-fn', '--file_name', required=True, help=' file name without extension')
arg_parser.add_argument('-v', '--version', required=True, help=' file name without extension')
args = vars(arg_parser.parse_args())
file_name = args['file_name']
version = args['version']

if int(version) == 0:
    org_im_path = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/Otsu/masked_image.npy'
    inp_im_path = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/ROI_'+str(version)+'/inpainting/inpainted_image.npy'
    coord_path  = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/ROI_'+str(version)+'/contour_coord.npy'
    
    org_im = np.load(org_im_path)
    imp_im = np.load(inp_im_path)
    [xcoord, ycoord] = np.load(coord_path)

    cx = int(np.mean(xcoord))
    cy = int(np.mean(ycoord))

    sh = 50
    #org_im = org_im[cy-sh:cy+sh, cx-sh:cx+sh]
    #imp_im = imp_im[cy-sh:cy+sh, cx-sh:cx+sh]
    for idx, im in enumerate([org_im, imp_im]):
        fig = plt.figure()
        ax  = fig.add_subplot(111)
        ax.axis('off')
        c = [cm.coolwarm, cm.seismic, cm.Paired, cm.binary]
        c = c[1]
        if True:
            mu, std = np.nanmedian(im), np.nanstd(im)
            for x in range(im.shape[0]):
                for y in range(im.shape[1]):
                    if np.absolute(im[x][y]-mu) >= 5*std:
                        im[x][y] = np.nan
        if idx==0:
            vminn = np.nanmin(im)
            vmaxx = np.nanmax(im)

        print cx, cy
        plt.imshow(im[cx-sh:cx+sh, cy-sh:cy+sh], vmin=vminn, vmax=vmaxx, cmap=c, interpolation='none')
        cb = plt.colorbar(cmap=c)
        cb.set_label(r"$S_{\nu}$[Jy]")
        plt.show()

    exit()

org_im_path = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/Otsu/masked_image.npy'
inp_im_path = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/ROI_'+str(version)+'/inpainting/inpainted_image.npy'
lin_im_path = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/ROI_'+str(version)+'/linear/linear_interpol_image.npy'
coord_path  = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/ROI_'+str(version)+'/contour_coord.npy'

org_im = np.load(org_im_path)
imp_im = np.load(inp_im_path)
lin_im = np.load(lin_im_path)

[xcoord, ycoord] = np.load(coord_path)
cx = int(np.mean(xcoord))
cy = int(np.mean(ycoord))

org_im = org_im[cy-40:cy+40, cx-40:cx+40]
imp_im = imp_im[cy-40:cy+40, cx-40:cx+40]
lin_im = lin_im[cy-40:cy+40, cx-40:cx+40]

imp_dif = (org_im - imp_im)**2
lin_dif = (org_im - lin_im)**2
plt.imshow(imp_dif)
plt.show()
plt.imshow(lin_dif)
plt.show()
print 'RMSE_INP = '+str(np.sqrt(np.nanmean(imp_dif)))
print 'RMSE_LIN = '+str(np.sqrt(np.nanmean(lin_dif)))

exit()

for idx, im in enumerate([org_im, imp_im]):
    fig = plt.figure()
    ax  = fig.add_subplot(111)
    ax.axis('off')
    c = [cm.coolwarm, cm.seismic, cm.Paired, cm.binary]
    c = c[1]
    if True:
        mu, std = np.nanmedian(im), np.nanstd(im)
        for x in range(im.shape[0]):
            for y in range(im.shape[1]):
                if np.absolute(im[x][y]-mu) >= 10*std:
                    im[x][y] = np.nan
    if idx==0:
        vminn = np.nanmin(im)
        vmaxx = np.nanmax(im)

    plt.imshow(im, vmin=vminn, vmax=vmaxx, cmap=c, interpolation='none')
    cb = plt.colorbar(cmap=c)
    cb.set_label(r"$S_{\nu}$[Jy]")
    plt.show()
