import os, time, argparse
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.filters import convolve
from astropy.convolution import Moffat2DKernel as moffat
from UTILS import makeGaussian, bilinearInterpol, createMask, saveroutine
from ALGO import inpainter

arg_parser  = argparse.ArgumentParser()
arg_parser.add_argument('-hpw', '--halfPatchWidth', required=True, help=' file name without extension')
arg_parser.add_argument('-s', '--save', required=True, help=' file name without extension')
args = vars(arg_parser.parse_args())
halfPatchWidth = int(args['halfPatchWidth'])
save = int(args['save'])

if save:
    output_path = '/Users/jeantad/Desktop/new_crab/OUT_TEST/sim'
    directory_1 = output_path + '/inpainting'
    directory_2 = output_path + '/linear'
    directory = [directory_1, directory_2]
    for dir in directory:
        try:
            os.makedirs(dir)
        except OSError:
            pass

n = 100
fwhm = 0.1*n
r = np.arange(0.1, 2.1, 0.1)
run = 10
NRMSE_int = np.zeros((run, len(r)))
NRMSE_inp = np.zeros((run, len(r)))

for it in range(run):
    if save:
        try:
            os.makedirs(directory_2+'/'+str(it))
        except OSError:
            pass

    sky = np.array(np.random.randn(1, n*n)).reshape((n,n))
    psf = makeGaussian(n, fwhm)
    signal = convolve(sky, psf)
    for id, step in enumerate([elem*fwhm for elem in r]):
        if save:
            try:
                os.makedirs(directory_1+'/'+str(it)+'/'+str(id))
                os.makedirs(directory_2+'/'+str(it)+'/'+str(id))
            except OSError:
                pass

        Q_11 = [int(n/2-step), int(n/2-step)]
        Q_21 = [int(n/2+step), int(n/2-step)]
        Q_12 = [int(n/2-step), int(n/2+step)]
        Q_22 = [int(n/2+step), int(n/2+step)]
        pts  = np.vstack((Q_11,Q_21,Q_12,Q_22))
        recon_im_int, residual_im_int, RMSE_int = bilinearInterpol(Q_11, Q_12, Q_21, Q_22, signal)
        NRMSE_int[it, id] = RMSE_int/((2*step)*(2*step))

        mask, masked_im, gray_originalImage = createMask(Q_11, Q_12, Q_21, Q_22, signal)
        i = inpainter(gray_originalImage, mask, halfPatchWidth)
        recon_im_bit = i.inpaint()
        recon_im_inp = (recon_im_bit*(np.nanmax(signal)-np.nanmin(signal)))/(2**8 - 1)+np.nanmin(signal)

        residual_im_inp = []
        for x in range(Q_11[0], Q_22[0]+1):
            for y in range(Q_11[0], Q_22[0]+1):
                residual_im_inp.append(np.sqrt((signal[x][y]-recon_im_inp[x][y])**2))

        RMSE_inp = np.sum(residual_im_inp)
        NRMSE_inp[it, id] = RMSE_inp/((2*step)*(2*step))
        if save:
            saveroutine(directory_2+'/'+str(it)+'/'+str(id), directory_1+'/'+str(it)+'/'+str(id),
                        recon_im_int, pts, signal, id, recon_im_inp)

plt.plot(r, np.median(NRMSE_int, axis=0), label='Interpolation')
plt.plot(r, np.median(NRMSE_inp, axis=0), label='Inpainting')
plt.xlabel('Multiple of fwhm')
plt.ylabel('Normalized RMSE')
plt.legend()
plt.savefig(output_path+'/result.png')
