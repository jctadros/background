import numpy as np
import mahotas
import os, sys, argparse
import matplotlib.pyplot as plt
from matplotlib import ticker, cm
from os import listdir
from os.path import isfile, join

arg_parser   = argparse.ArgumentParser()
arg_parser.add_argument("-fn", "--file_name", required=True, help="  file name without extension")
arg_parser.add_argument("-mode", "--mode", required=True, help=" rect or Otsu mode")
arg_parser.add_argument("-size", "--size", required=False, help=" size of rect")

args = vars(arg_parser.parse_args())
file_name = args['file_name']
mode = args['mode']
if mode == 'rect':
    size = args['size']

output_path  = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'
directory_1 = output_path + str(file_name) + '/Otsu'
directory_2 = output_path + str(file_name) + '/analysis/ROI_0'
directory_4 = output_path + str(file_name) + '/analysis/rect/ROI_0'

if mode == 'rect':
    directory_3 = output_path + str(file_name) + '/analysis/rect/'+str(size)+'/ROI_0'
    masked_path  = directory_4+'/masked_image.npy'
    contour_path = directory_4+'/contour_coord.npy'
    points_path  = directory_4+'/points.npy'
    points = np.load(points_path)
    Q_11, Q_12, Q_21, Q_22 = points[0], points[1], points[2], points[3]
    [y_contour, x_contour] = np.load(contour_path)
    masked_image = np.load(masked_path)
    directory = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis/rect/'+str(size)

elif mode == 'otsu':
    masked_path  = directory_1+'/masked_image.npy'
    contour_path = directory_1+'/contour_coord.npy'
    masked_image = np.load(masked_path)
    [x_contour, y_contour] = np.load(contour_path)
    directory = '/Users/jeantad/Desktop/new_crab/OUT_TEST/'+str(file_name)+'/analysis'

f, idx = [], [0]
for (dirpath, dirnames, filenames) in os.walk(directory):
    f.extend(filenames)
    for folder in dirnames:
        if folder[:4]=='ROI_':
            idx.append(int(folder[-1]))
    break
idx = np.max(idx)+1
if mode == 'otsu': output_path  = directory+'/ROI_'+str(idx)+'/'
elif mode == 'rect': output_path = directory+'/ROI_'+str(idx)+'/'
if not os.path.exists(output_path):
    os.makedirs(output_path)

ok_pass, count = True, 0
def on_key(event):
    global ok_pass, image, count
    if event.key == 'enter':
        ok_pass = False
        if count == 0:
            plt.savefig(output_path+'/mask_contour.png')
        plt.close('all')
        count+=1
    elif event.key == 'backspace':
        im.set_data(np.copy(image))
        plt.draw()
        ok_pass = True

def on_press(event):
    global x_contour, y_contour, xc, yc, xdata, ydata
    xdata, ydata = event.xdata, event.ydata
    x_contour, y_contour = x_contour+xdata-xc, y_contour+ydata-yc
    image_1.set_data(x_contour, y_contour)
    xc, yc = np.mean(x_contour), np.mean(y_contour)
    plt.draw()
    fig.canvas.mpl_connect("key_press_event", on_key)

while ok_pass:
    xc, yc = np.mean(x_contour), np.mean(y_contour)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.axis('off')
    image_0 = plt.imshow(masked_image)
    image_1, = plt.plot(x_contour, y_contour)
    fig.canvas.mpl_connect('button_press_event', on_press)
    plt.show()

poly = []
n_grid = np.zeros((len(masked_image), len(np.transpose(masked_image))))
image  = np.copy(masked_image)
mask   = np.zeros((image.shape[0], image.shape[1]))

for i in range(len(x_contour)):
    temp = int(x_contour[i]), int(y_contour[i])
    poly.append(temp)

mahotas.polygon.fill_polygon(poly, n_grid)
pix = np.where(n_grid == 1)
coord = [[],[]]
for l in range(len(pix[0])):
    image[pix[1][l]][pix[0][l]] = np.nan
    mask[pix[1][l]][pix[0][l]] = 255
    coord[0].append(pix[0][l])
    coord[1].append(pix[1][l])

if mode == 'rect':
    xlist, ylist = [], []
    for x in range(mask.shape[0]):
        for y in range(mask.shape[1]):
            if mask[x][y] == 255:
                xlist.append(x)
                ylist.append(y)

    minx, maxx = min(xlist), max(xlist)
    miny, maxy = min(ylist), max(ylist)

    Q_11 = [minx-1, miny-1]
    Q_12 = [minx-1, maxy+1]
    Q_21 = [maxx+1, miny-1]
    Q_22 = [maxx+1, maxy+1]

    np.save(output_path+'points.npy', [Q_11, Q_12, Q_21, Q_22])


np.save(output_path+'contour_coord.npy', [x_contour, y_contour])

fig = plt.figure()
ax = fig.add_subplot(111)
ax.axis('off')
im = plt.imshow(image)
fig.canvas.mpl_connect('key_press_event', on_key)
plt.savefig(output_path+'masked_image.png')
np.save(output_path+'masked_image.npy', image)
plt.show()

fig = plt.figure()
ax = fig.add_subplot(111)
ax.axis('off')
plt.imshow(mask)
fig.canvas.mpl_connect('key_press_event', on_key)
plt.savefig(output_path+'mask.png')
np.save(output_path+'mask.npy', mask)
plt.show()
