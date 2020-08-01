import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.filters import generic_filter
import matplotlib.widgets as widgets

def better_histogram(array, p, q, Thresh, file_name, nbins=255):
    val = []
    for i in array:
        if np.isnan(i): continue
        else: val.append(i)
    val = np.array(val)
    hist, bin_edges = np.histogram(val, nbins)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.
    if p: #For ploting p=True
        plt.hist(val, bins=nbins)
        plt.axvline(x=Thresh, color='red')
        if q:   #For Otsu Thresholding if q=True
            plt.savefig('/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/Otsu/ots_HIST_'+str(file_name)+'.png')
        else:   #For Otsu Interactive Thresholding if q=False
            plt.savefig('/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/Otsu/HIST_'+str(file_name)+'.png')
        plt.close()
    return hist, bin_centers

def otsu_method(hist, bin_centers, nbins=255):
    hist = hist.astype(float)
    # class probabilities for all possible thresholds
    weight1 = np.cumsum(hist)
    weight2 = np.cumsum(hist[::-1])[::-1]
    # class means for all possible thresholds
    mean1 = np.cumsum(hist * bin_centers) / weight1
    mean2 = (np.cumsum((hist * bin_centers)[::-1]) / weight2[::-1])[::-1]

    '''
    Clip ends to align class 1 and class 2 variables:
    The last value of `weight1`/`mean1` should pair with zero values in
    `weight2`/`mean2`, which do not exist.
    '''
    variance12 = weight1[:-1] * weight2[1:] * (mean1[:-1] - mean2[1:]) ** 2
    idx = np.argmax(variance12)
    threshold = bin_centers[:-1][idx]
    return threshold

def plateau(x, y):
    I_filt = generic_filter(y, np.std, size=5)
    max = 0
    for i in range(len(I_filt)):
        if I_filt[i] > max:
            max = x[i]
    return max + 5/2
