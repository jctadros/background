import numpy as np
import matplotlib.pyplot as plt

def makeGaussian(size, fwhm):
    x = np.arange(start=0, stop=size, step=1, dtype=float)
    y = x[:, np.newaxis]
    x0 = y0 = size//2
    return np.exp(-4*np.log(2)*((x-x0)**2 + (y-y0)**2)/fwhm**2)

def bilinearInterpol(Q_11, Q_12, Q_21, Q_22, originalImage, file_name):
    f_11 = originalImage[Q_11[0], Q_11[1]]
    f_21 = originalImage[Q_21[0], Q_21[1]]
    f_12 = originalImage[Q_12[0], Q_12[1]]
    f_22 = originalImage[Q_22[0], Q_22[1]]
    #print f_11, f_12, f_21, f_22
    v1 = np.ones((4,))
    v2 = [Q_11[0], Q_11[0], Q_21[0], Q_21[0]]
    v3 = [Q_11[1], Q_12[1], Q_11[1], Q_12[1]]
    v4 = [Q_11[0]*Q_11[1], Q_11[0]*Q_12[1], Q_21[0]*Q_21[1], Q_21[0]*Q_12[1]]
    array = np.vstack((v1, v2, v3, v4))
    array = array.T

    recon_im = np.zeros((originalImage.shape[0], originalImage.shape[1]))
    residual_im = np.zeros((originalImage.shape[0], originalImage.shape[1]))
    org_im_path = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/Otsu/masked_image.npy'
    org_im = np.load(org_im_path)

    l_r = []
    for x in range(Q_11[0], Q_22[0]+1):
        for y in range(Q_11[1], Q_22[1]+1):
            b = np.array(np.dot(np.linalg.inv(array).T, [1, x, y, x*y]))
            recon_im[x][y]    = np.dot(b, [f_11, f_12, f_21, f_22])
            l_r.append( (org_im[x][y] - recon_im[x][y])**2)

    RMSE = np.sqrt(np.nanmean(l_r))

    return recon_im, residual_im, RMSE

def createMask(Q_11, Q_12, Q_21, Q_22, originalImage):
    mask = np.zeros((originalImage.shape[0], originalImage.shape[1]))
    masked_image = np.copy(originalImage)
    for x in range(Q_11[0], Q_22[0]+1):
        for y in range(Q_11[0], Q_22[0]+1):
            mask[x,y] = 255
            masked_image[x,y] = 0

    gray_originalImage = np.uint8(np.round(((2**8 - 1)*(originalImage-np.nanmin(originalImage)))/(np.nanmax(originalImage)-np.nanmin(originalImage))))

    return mask, masked_image, gray_originalImage

def saveroutine(directory_int, directory_inp, recon_im_int, pts, originalImage, id, recon_im_inp):
    np.save(directory_int+'/recon_im_'+str(id)+'.npy', recon_im_int)
    plt.imshow(recon_im_int)
    plt.plot(pts[:,0], pts[:,1], '*')
    plt.axis('off')
    plt.savefig(directory_int+'/recon_im_'+str(id)+'.png')
    plt.close('all')

    plt.imshow(originalImage)
    plt.plot(pts[:,0], pts[:,1], '*')
    plt.axis('off')
    plt.savefig(directory_int+'/originalImage_'+str(id)+'.png')
    plt.close('all')

    plt.imshow(originalImage)
    plt.plot(pts[:,0], pts[:,1], '*')
    plt.axis('off')
    plt.savefig(directory_inp+'/originalImage_'+str(id)+'.png')
    plt.close('all')

    plt.imshow(recon_im_inp)
    plt.plot(pts[:,0], pts[:,1], '*')
    plt.axis('off')
    plt.savefig(directory_inp+'/recon_im_'+str(id)+'.png')
    plt.close('all')
