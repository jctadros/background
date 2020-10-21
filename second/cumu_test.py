import numpy as np
import matplotlib.pyplot as plt
import os
import astropy.io.fits as fits
from scipy.spatial.distance import euclidean as euclid

def better_histogram(array):
    val = []
    for x in range(array.shape[0]):
        for y in range(array.shape[1]):
            if np.isnan(array[x][y]): continue
            else: val.append(array[x][y])
    val = np.array(val)

    return plt.hist(val, 100)

def _distance(x, y):
    return euclid(x, y)

result = {}
save_result = {}

for fn in ['500']:
    result[fn] = {}
    save_result[fn] = {}

    image_path  = '/Users/jeantad/Desktop/new_crab/DATA_TEST/'
    path = image_path + fn + '.fits'

    for s in range(0, 4):
        result[fn][s] = {}
        lin_d, inp_d, bil_d = [], [], []

        for v in range(1, 11):
            dir = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(fn)+'/analysis/rect/'+str(s)+'/ROI_'+str(v)
            org  = fits.open(path)[1].data
            mask = np.load(dir + '/mask.npy')
            inp  = np.load(dir + '/inpainting/inpainted_image.npy')
            lin  = np.load(dir + '/linear/linear_interpol_image.npy')
            bil  = np.load(dir + '/bilinear/reconstruction.npy')

            for x in range(mask.shape[0]):
                for y in range(mask.shape[1]):
                    if mask[x][y] == 255:
                        continue
                    else:
                        lin[x][y] = np.nan
                        inp[x][y] = np.nan
                        org[x][y] = np.nan
                        bil[x][y] = np.nan

            org_h, lin_h, inp_h, bil_h = better_histogram(org), better_histogram(lin), better_histogram(inp), better_histogram(bil)
            lin_d.append(_distance(org_h[0]/np.sum(org_h[0]), lin_h[0]/np.sum(lin_h[0])))
            inp_d.append(_distance(org_h[0]/np.sum(org_h[0]), inp_h[0]/np.sum(inp_h[0])))
            bil_d.append(_distance(org_h[0]/np.sum(org_h[0]), bil_h[0]/np.sum(bil_h[0])))

            plt.close('all')

        result[fn][s]['lin'] = [np.mean(lin_d), np.var(lin_d)]
        result[fn][s]['inp'] = [np.mean(inp_d), np.var(inp_d)]
        result[fn][s]['bil'] = [np.mean(bil_d), np.var(bil_d)]

    lin_v = [result[fn][elem]['lin'][0] for elem in range(0,4)]
    inp_v = [result[fn][elem]['inp'][0] for elem in range(0,4)]
    bil_v = [result[fn][elem]['bil'][0] for elem in range(0,4)]

    lin_e = [result[fn][elem]['lin'][1] for elem in range(0,4)]
    inp_e = [result[fn][elem]['inp'][1] for elem in range(0,4)]
    bil_e = [result[fn][elem]['bil'][1] for elem in range(0,4)]

    del result
    save_result[fn]['lin'] = [lin_v, lin_e]
    save_result[fn]['inp'] = [inp_v, inp_e]
    save_result[fn]['bil'] = [bil_v, bil_e]

try:
    import cPickle as pickle
except ImportError:  # Python 3.x
    import pickle

with open('data.p', 'wb') as fp:
    pickle.dump(save_result, fp, protocol=pickle.HIGHEST_PROTOCOL)
