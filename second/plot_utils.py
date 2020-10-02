def on_key(event):
    global pass_accept
    if event.key == 'enter':
        pass_accept = False
        np.save(output_path+str(file_name)+'/Otsu/roi.npy', info[int(min(y)):int(max(y)), int(min(x)):int(max(x))])
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
