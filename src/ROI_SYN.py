import numpy as np
import matplotlib.pyplot as plt 
import os, argparse
import mahotas

arg_parser   = argparse.ArgumentParser()
arg_parser.add_argument("-fn", "--file_name", required=True, help="  file name without extension")
args = vars(arg_parser.parse_args())
file_name = args['file_name']

os.chdir("..")
output_path = os.path.abspath(os.curdir) + '/images/'

directory_1  = output_path + file_name 
directory_2  = output_path + file_name + '/ROI_0'

masked_path  = directory_1 + '/masked_image.npy'
contour_path = directory_1+'/contour_coord.npy'
masked_image = np.load(masked_path) 
[x_contour, y_contour] = np.load(contour_path)

f, idx = [], [0]
for (dirpath, dirnames, filenames) in os.walk(directory_1):
    f.extend(filenames)
    for folder in dirnames:
        if folder[:4]=='ROI_':
            idx.append(int(folder[-1]))
    break

idx = np.max(idx)+1
output_path  = directory_1 + '/ROI_' + str(idx) + '/'
if not os.path.exists(output_path):
    os.makedirs(output_path)

def on_key(event):
    global ok_pass, image
    if event.key == 'enter':
        ok_pass = False
        plt.savefig(output_path+'/mask_contour.png')
        plt.close('all')

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

ok_pass = True
while ok_pass:
    #get center of ROI from contour coord
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

np.save(output_path+'contour_coord.npy', [x_contour, y_contour])
