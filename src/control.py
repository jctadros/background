import mahotas
import warnings
import numpy as np
import skimage.morphology as morph
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
from scipy.ndimage.filters import generic_filter

warnings.filterwarnings("ignore")
thres, count, size_morph = 0, 0, 0
pass_accept = True

def better_histogram(zoom, plot_switch, best_thres, directory_1, nbins=255):
    #flatten zoom and remove 'NaN' 
    array = [pix for pix in zoom.reshape((-1,1)) if pix != 'nan']
    hist, bin_edges = np.histogram(array, nbins)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.
    
    #TODO: very slow when TRUE
    if plot_switch:
        plt.hist(array, bins=nbins)
        plt.axvline(x=best_thres, color='red')
        plt.savefig(directory_1+'/HIST.png')
        plt.close()
    
    return hist, bin_centers

def Otsu_method(hist, bin_centers, nbins=255):
    hist = hist.astype(float)
    weight1 = np.cumsum(hist)
    weight2 = np.cumsum(hist[::-1])[::-1]
    mean1 = np.cumsum(hist * bin_centers) / weight1
    mean2 = (np.cumsum((hist * bin_centers)[::-1]) / weight2[::-1])[::-1]
    variance12 = weight1[:-1] * weight2[1:] * (mean1[:-1] - mean2[1:]) ** 2
    idx = np.argmax(variance12)
    
    best_thres = bin_centers[:-1][idx]

    return best_thres

def build_contour(zoom, thres, size_morph, xsize, ysize):
    #------------------------------------ DISCLAIMER -------------------------------
    #no idea how this works. written by Sarkis Kassounian <sakokassounian@gmail.com>
    #-------------------------------------------------------------------------------
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

def interactive_Otsu(info, zoom, corner_coord, file_name, directory_1):
    global best_thres, xsize, ysize
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

        x_contour, y_contour, pix = build_contour(zoom, best_thres*(1-thres), size_morph, xsize, ysize)
        image_2.set_data(x_contour, y_contour)
        image_1.set_data(zoom)
        plt.draw()
    
    xsize, ysize, row_i, col_i = len(zoom), len(zoom.T), np.min(corner_coord[0]), np.min(corner_coord[1])
  
    hist, bin_centers = better_histogram(zoom, False, None, directory_1)
    best_thres = Otsu_method(hist, bin_centers)
    x_contour, y_contour, pix = build_contour(zoom, best_thres*(1-thres), size_morph, xsize, ysize)

    f = plt.figure()
    ax = f.add_subplot(111)
    ax.axis('off')
    image_1  = plt.imshow(zoom)
    image_2, = plt.plot(x_contour, y_contour, 'r', alpha=0.4, label='Region of Interest')
    plt.legend(loc='lower right')
    #cb = plt.colorbar()
    f.canvas.mpl_connect("key_press_event", on_key)
    plt.show()

    x_contour, y_contour, pix = build_contour(zoom, best_thres*(1-thres), size_morph, xsize, ysize)
    _, __ = better_histogram(zoom, False, best_thres*(1-thres), directory_1)
    del _, __

    pix_x = pix[0] + col_i
    exit()
    pix_y = pix[1] + row_i
    masked_image = info.copy()
    mask = np.zeros((info.shape[0], info.shape[1]))
    for elem in range(len(pix_x)):
        masked_image[pix_x[elem]][pix_y[elem]] = np.nan
        mask[pix_x[elem]][pix_y[elem]]  = 255

    return masked_image, mask, x_contour, y_contour

def interactive_ROI(info):  
  def on_key(event):
    global pass_accept
    if event.key == 'enter':
      pass_accept = False
      plt.close('all')
  
    elif event.key == 'backspace':
      pass_accept = True
      plt.close('all')

  def onselect(eclick, erelease):
    if eclick.ydata > erelease.ydata:
      eclick.ydata, erelease.ydata = erelease.ydata, eclick.ydata
    if eclick.xdata > erelease.xdata:
      eclick.xdata, erelease.xdata = erelease.xdata, eclick.xdata

    x[:] = eclick.xdata, erelease.xdata
    y[:] = erelease.ydata, erelease.ydata - erelease.xdata + eclick.xdata

    ax.set_xlim(min(x), max(x))
    ax.set_ylim(max(y), min(y))
    ax.axis('off')
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    fig.canvas.mpl_connect("key_press_event", on_key)

  while pass_accept:
    fig = plt.figure()
    ax  = fig.add_subplot(111)

    x, y = [], []
    rs = widgets.RectangleSelector(
                 ax, onselect, drawtype='box',
                 rectprops = dict(facecolor='red',
                 edgecolor='black', alpha=0.2, fill=True))

    ax.axis('off')
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    plt.imshow(info)
    plt.show()
      
  zoom = info[int(np.min(y)): int(np.max(y)), int(np.min(x)): int(np.max(x))]
  corner_coord = (int(np.min(x)), int(np.min(y)))
  
  return corner_coord, zoom
