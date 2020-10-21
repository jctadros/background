import matplotlib.pyplot as plt
import numpy as np

try:
    import cPickle as pickle
except ImportError:  # Python 3.x
    import pickle

with open('data.p', 'rb') as fp:
    data = pickle.load(fp)

for fn in data.keys():
    sizes  = ['0','1','2','3']

    lin_v  = data[fn]['lin'][0]
    inp_v  = data[fn]['inp'][0]
    bil_v  = data[fn]['bil'][0]

    lin_e  = [elem**0.5 for elem in data[fn]['lin'][1]]
    inp_e  = [elem**0.5 for elem in data[fn]['inp'][1]]
    bil_e  = [elem**0.5 for elem in data[fn]['bil'][1]]

    if fn == '500': ln = '--'
    if fn == '350': ln = '-.'
    if fn == '250': ln = ':'

    plt.errorbar(sizes, lin_v, linestyle=ln, marker='s', yerr=lin_e, color='red')
    plt.errorbar(sizes, inp_v, linestyle=ln, marker='s', yerr=inp_e, color='green')
    plt.errorbar(sizes, bil_v, linestyle=ln, marker='s', yerr=bil_e, color='orange')

plt.show()
