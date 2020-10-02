import mahotas
import warnings
import numpy as np
import skimage.morphology as morph
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
from scipy.ndimage.filters import generic_filter
from UTILS import better_histogram, otsu_method, plateau

warnings.filterwarnings("ignore")
thres, count, size_morph = 0, 0, 0

def better_histogram(array, p, Thresh, directory_1, nbins=255):
    val = []
    for i in array:
        if np.isnan(i): continue
        else: val.append(i)
    val = np.array(val)
    hist, bin_edges = np.histogram(val, nbins)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.
    if p:
        plt.hist(val, bins=nbins)
        plt.axvline(x=Thresh, color='red')
        plt.savefig(directory_1+'/HIST.png')
        plt.close()

    return hist, bin_centers

def otsu_method(hist, bin_centers, nbins=255):
    hist = hist.astype(float)
    weight1 = np.cumsum(hist)
    weight2 = np.cumsum(hist[::-1])[::-1]
    mean1 = np.cumsum(hist * bin_centers) / weight1
    mean2 = (np.cumsum((hist * bin_centers)[::-1]) / weight2[::-1])[::-1]
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

def build_contour(zoom, thres, size_morph, xsize, ysize):
    global count
    count += 1
    cond = thres
    mask = np.zeros((xsize, ysize), dtype=np.int8)
    for i in range(xsize):
        for j in range(ysize):
            if zoom[i][j] > cond:
                mask[i][j] = 1

    strel = morph.disk(size_morph)
    mask  = morph.opening(mask, strel)
    Y = np.arange(0, xsize, 1)
    X = np.arange(0, ysize, 1)
    X, Y = np.meshgrid(X, Y)

    g = plt.figure()
    CS = plt.contour(X, Y, mask, [0,1,2], cmap='gray')
    plt.close(g)

    segs = CS.allsegs
    index = []
    for i in range(len(segs[0])):
        temp = len(segs[0][i])
        index.append(temp)

    best = np.argmax(index)
    segs = segs[0][best]
    poly_verts = []
    for i in range(len(segs[:,0])):
        val = (segs[:,0][i], segs[:,1][i])
        poly_verts.append(val)

    n_grid = np.zeros((xsize, ysize), dtype=np.int8)
    poly = []
    for i in range(len(segs[:,0])):
        temp = int(segs[:,1][i]), int(segs[:,0][i])
        poly.append(temp)

    mahotas.polygon.fill_polygon(poly, n_grid)
    pix = np.where(n_grid == 1)

    return segs[:,0], segs[:,1], pix

def interactive_otsu_thresholding(info, zoom, row_i, col_i, file_name, directory_1):
    global Thresh, xsize, ysize, data
    def on_key(event):
        global thres, size_morph, p
        if event.key == 'up': thres += 0.5
        elif event.key == 'down':  thres -= 0.5
        elif event.key == 'left':  thres -= 0.1
        elif event.key == 'right': thres += 0.1
        elif event.key == 'super+right': thres += 0.01
        elif event.key == 'super+left':  thres -= 0.01
        elif event.key == 'shift+super+right': thres += 0.005
        elif event.key == 'shift+super+left':  thres -= 0.005
        elif event.key == 'a':  size_morph += 1
        elif event.key == 'b':  size_morph -= 1
        elif event.key == 'enter':
            plt.savefig(directory_1+'/roi.png')
            plt.close()

        x_contour, y_contour, pix = build_contour(zoom, Thresh*(1-thres), size_morph, xsize, ysize)
        image_2.set_data(x_contour, y_contour)
        image_1.set_data(zoom)
        plt.draw()

    xsize, ysize, data = len(zoom), len(np.transpose(zoom)), {}
    for i in range(xsize):
        for j in range(ysize):
            data[(i,j)] = zoom[i,j]

    hist, bin_centers = better_histogram(data.values(), False, None, directory_1)
    Thresh = otsu_method(hist, bin_centers)
    x_contour, y_contour, pix = build_contour(zoom, Thresh*(1-thres), size_morph, xsize, ysize)

    f = plt.figure()
    ax  = f.add_subplot(111)
    ax.axis('off')
    image_1  = plt.imshow(zoom)
    image_2, = plt.plot(x_contour, y_contour, 'r', alpha=0.4, label='Region of Interest')
    plt.legend(loc='lower right')
    cb = plt.colorbar()
    cb.set_label(r"$S_{\nu}$[Jy]")
    f.canvas.mpl_connect("key_press_event", on_key)
    plt.show()

    x_contour, y_contour, pix = build_contour(zoom, Thresh*(1-thres), size_morph, xsize, ysize)
    _, __ = better_histogram(data.values(), True, Thresh*(1-thres), directory_1)
    del _, __

    pix_x = pix[0] + col_i
    pix_y = pix[1] + row_i
    image = info.copy()
    mask  = np.zeros((info.shape[0], info.shape[1]))
    pix_vals = {}
    for l in range(len(pix_x)):
        pix_vals[(pix_x[l], pix_y[l])] = image[pix_x[l]][pix_y[l]]
        image[pix_x[l]][pix_y[l]] = np.nan
        mask[pix_x[l]][pix_y[l]]  = 255

    return image, mask, x_contour, y_contour
