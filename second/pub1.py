import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from matplotlib import ticker, cm

n, unit = 51, 1
image = np.array(np.random.randint(255, size=n*n)).reshape(n,n)
kernel = np.ones((5,5))
image = np.uint32(ndimage.convolve(image, kernel))

offset = n/2
image[0][offset-unit:offset+unit]  = 255
image[-1][offset-unit:offset+unit] = 255
image[offset][0] = 255
image[offset][-1] = 255

for x in range(n-offset-unit):
    image[x+offset+unit][x]  = 255
    image[-x+offset-unit][x] = 255
for x in range(offset+unit, n):
    image[x-offset-unit][x] = 255
    image[-x+offset][x]  = 255
for x in range(image.shape[0]):
    for y in range(image.shape[1]):
        if y-x-offset-unit>0 or y-x+offset+unit<0 or y+x-offset+unit<0 or y+x>3*offset+unit:
            image[x,y] = 255

def on_key(event):
    if event.key == 'backspace':
        image[undo[0]][undo[1]] = undo[2]

def onclick(event):
    global undo, image
    undo = [int(np.floor(event.ydata)), int(np.floor(event.xdata)), image[int(np.floor(event.ydata))][int(np.floor(event.xdata))]]
    image[int(np.floor(event.ydata))][int(np.floor(event.xdata))] = 255
    i.set_data(image)
    fig.canvas.mpl_connect('key_press_event', on_key)
    plt.draw()


fig = plt.figure()
ax  = plt.subplot(111)
ax.set_xticks(np.arange(-.5, n, 1))
ax.set_yticks(np.arange(-.5, n, 1))
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.xaxis.set_ticks_position('none')
ax.yaxis.set_ticks_position('none')
plt.grid(color='r', linestyle='-', linewidth=0.2, which='major', axis='both')
i = plt.imshow(image)
fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()
