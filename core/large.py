import numpy as np
import matplotlib.pyplot as plt
import os

mask_path = '/Users/jeantad/Desktop/new_crab/OUT_TEST/500/analysis/rect/sim/ROI_1/mask.npy'
masked_image_path = '/Users/jeantad/Desktop/new_crab/OUT_TEST/500/analysis/rect/sim/ROI_1/masked_image.npy'
contour_path = '/Users/jeantad/Desktop/new_crab/OUT_TEST/500/analysis/rect/sim/ROI_1/contour_coord.npy'
output_path  = '/Users/jeantad/Desktop/new_crab/OUT_TEST/500/analysis/rect/sim'

l_step = []
for iter in range(2,5):
    step = int(iter*2)
    if step in l_step:
        continue
    l_step.append(step)

    dir = output_path+'/ROI_'+str(iter)
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
    except OSError:
            print ('Error: Creating directory. ' + dir)

    mask = np.load(mask_path)
    masked_image = np.load(masked_image_path)
    copy_mask = np.copy(mask)
    copy_image = np.copy(masked_image)

    xlist, ylist = [], []
    for x in range(mask.shape[0]):
        for y in range(mask.shape[1]):
            if mask[x][y] == 255:
                xlist.append(x)
                ylist.append(y)

    minx, maxx = min(xlist), max(xlist)
    miny, maxy = min(ylist), max(ylist)

    copy_mask = np.copy(mask)
    copy_image[minx-step:maxx+1+step, miny-step:maxy+1+step] = np.nan
    copy_mask[minx-step:maxx+1+step, miny-step:maxy+1+step]  = 255

    Q_11 = [minx-1-step, miny-1-step]
    Q_12 = [minx-1-step, maxy+1+step]
    Q_21 = [maxx+1+step, miny-1-step]
    Q_22 = [maxx+1+step, maxy+1+step]

    plt.imshow(copy_mask)
    plt.axis('off')
    plt.savefig(dir+'/mask.png')
    plt.close('all')
    np.save(dir+'/mask.npy', copy_mask)

    plt.imshow(copy_image)
    plt.axis('off')
    plt.savefig(dir+'/masked_image.png')
    plt.close('all')
    np.save(dir+'/masked_image.npy', copy_image)

    contour_coord = [[], []]
    for x in range(Q_11[0], Q_22[0]+1):
        contour_coord[0].append(x)
        contour_coord[1].append(Q_11[1])
        contour_coord[0].append(x)
        contour_coord[1].append(Q_22[1])

    for y in range(Q_11[1], Q_22[1]+1):
        contour_coord[1].append(y)
        contour_coord[0].append(Q_11[0])
        contour_coord[1].append(y)
        contour_coord[0].append(Q_22[0])

    np.save(dir+'/contour_coord.npy', contour_coord)
    np.save(dir+'/points.npy', [Q_11, Q_12, Q_21, Q_22])
