import numpy as np
import skimage.morphology as morph
import matplotlib.pyplot as plt
import mahotas
from UTILS import better_histogram, otsu_method, plateau
import warnings
warnings.filterwarnings("ignore")

thres = 0
count = 0
p = False
size_morph = 0

def build_contour(zoom, thres, size_morph, p, file_name, xsize, ysize, data):
    global count
    count += 1
    cond = thres
    mask = np.zeros((xsize, ysize), dtype=np.int8)
    for i in range(xsize):
        for j in range(ysize):
            if zoom[i][j] >= (cond):
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
    flux = 0
    for m in range(len(pix[0])):
        if np.isnan(data[(pix[0][m], pix[1][m])]): continue
        else: flux = flux + data[(pix[0][m], pix[1][m])]

    return segs[:,0], segs[:,1], pix, flux

def interactive_otsu_thresholding(info, zoom, row_i, col_i, file_name, output_path, directory_2):
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
            plt.savefig(output_path+str(file_name)+'/Otsu/roi.png')
            plt.close()

        x_contour, y_contour, pix, ___ = build_contour(zoom, Thresh*(1-thres), size_morph, p, file_name, xsize, ysize, data)
        image_2.set_data(x_contour, y_contour)
        image_1.set_data(zoom)
        plt.draw()

    xsize, ysize = len(zoom), len(np.transpose(zoom))
    data  = {}
    for i in range(xsize):
        for j in range(ysize):
            data[(i,j)] = zoom[i,j]

    hist, bin_centers = better_histogram(data.values(), False, False, None, file_name)
    Thresh = otsu_method(hist, bin_centers)

    x_contour, y_contour, pix, ___ = build_contour(zoom, Thresh*(1-thres), size_morph, False, file_name, xsize, ysize, data)
    f = plt.figure()
    ax  = f.add_subplot(111)
    ax.axis('off')
    image_1  = plt.imshow(zoom)
    image_2, = plt.plot(x_contour, y_contour, 'r', alpha=0.4, label='Region of Interest')
    plt.legend(loc='lower right')
    cb = plt.colorbar()
    cb.set_label(r"$S_{\nu}$[Jy]")
    h = 0
    f.canvas.mpl_connect("key_press_event", on_key)
    plt.show()

    x_contour, y_contour, pix, ___ = build_contour(zoom, Thresh*(1-thres), size_morph, True, file_name, xsize, ysize, data)
    _, __ = better_histogram(data.values(), True, False, Thresh*(1-thres), file_name)
    del _, __, ___

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

def otsu_thresholding(info, zoom, row_i, col_i, file_name, output_path):
    thresh, fluxes, contours, grids = [], [], [], []
    file_name = int(file_name)
    if file_name==70:  ites=list(np.arange(0,1,0.1)); size_morph  = 12
    if file_name==100: ites=list(np.arange(0,0.6,0.1)); size_morph = 5
    if file_name==160: ites=list(np.arange(0,0.6,0.1)); size_morph = 8
    if file_name==250: ites=list(np.arange(0,0.3,0.1)); size_morph = 0
    if file_name==350: ites=list(np.arange(0,0.4,0.1)); size_morph = 0
    if file_name==500: ites=list(np.arange(0,0.6,0.1)); size_morph = 0

    xsize = len(zoom)
    ysize = len(np.transpose(zoom))
    data  = {}
    for i in range(xsize):
        for j in range(ysize):
            data[(i,j)] = zoom[i,j]

    hist, bin_centers = better_histogram(data.values(), False, False, None, file_name) #takes into account np.nan values
    Thresh = otsu_method(hist, bin_centers)

    for k in range(len(ites)):
        x_contour, y_contour, pix, flux = build_contour(zoom, Thresh*(1-ites[k]), size_morph, p, file_name, xsize, ysize, data)
        contours.append([x_contour, y_contour])
        thresh.append(Thresh*(1-ites[k]))
        fluxes.append(flux)
        grids.append(pix)

    dfluxes = np.gradient(fluxes)
    best = plateau(range(len(thresh)), dfluxes)

    try:
        conts = contours[best]
        pix   = grids[best]

    except IndexError:
        safe_factor = 30
        temp  = len(thresh)
        best  = plateau(range(temp-safe_factor), dfluxes[0: temp-safe_factor])
        conts = contours[best]
        pix = grids[best]

    f = plt.figure()
    ax  = f.add_subplot(111)
    ax.axis('off')
    image_1  = plt.imshow(zoom)
    image_2, = plt.plot(conts[0], conts[1], 'r', alpha=0.4, label='Region of Interest')
    plt.legend(loc='lower right')
    cb = plt.colorbar()
    cb.set_label(r"$S_{\nu}$[Jy]")
    plt.savefig(output_path+str(file_name)+'/Otsu/ot_roi.png')
    plt.close(f)

    _, __ = better_histogram(data.values(), True, True, thresh[best], file_name)
    del _, __
    pix_x = pix[0] + col_i
    pix_y = pix[1] + row_i
    image  = info.copy()
    ots_mask = np.zeros((info.shape[0], info.shape[1]))
    pix_vals = {}
    for l in range(len(pix_x)):
        pix_vals[(pix_x[l], pix_y[l])] = image[pix_x[l]][pix_y[l]]
        image[pix_x[l]][pix_y[l]] = np.nan
        ots_mask[pix_x[l]][pix_y[l]] = 255

    return image, ots_mask, conts[0], conts[1]
