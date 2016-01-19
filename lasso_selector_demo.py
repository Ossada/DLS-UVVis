from __future__ import print_function

import numpy as np

from matplotlib.widgets import LassoSelector
from matplotlib.path import Path

try:
    raw_input
except NameError:
    # Python 3
    raw_input = input


class SelectFromCollection(object):
    """Select indices from a matplotlib collection using `LassoSelector`.

    Selected indices are saved in the `ind` attribute. This tool highlights
    selected points by fading them out (i.e., reducing their alpha values).
    If your collection has alpha < 1, this tool will permanently alter them.

    Note that this tool selects collection objects based on their *origins*
    (i.e., `offsets`).

    Parameters
    ----------
    ax : :class:`~matplotlib.axes.Axes`
        Axes to interact with.

    collection : :class:`matplotlib.collections.Collection` subclass
        Collection you want to select from.

    alpha_other : 0 <= float <= 1
        To highlight a selection, this tool sets all selected points to an
        alpha value of 1 and non-selected points to `alpha_other`.
    """

    def __init__(self, ax, collection, alpha_other=0.3):
        self.canvas = ax.figure.canvas
        self.collection = collection
        self.alpha_other = alpha_other

        self.xys = collection.get_offsets()
        self.Npts = len(self.xys)

        # Ensure that we have separate colors for each object
        self.fc = collection.get_facecolors()
        if len(self.fc) == 0:
            raise ValueError('Collection must have a facecolor')
        elif len(self.fc) == 1:
            self.fc = np.tile(self.fc, self.Npts).reshape(self.Npts, -1)

        self.lasso = LassoSelector(ax, onselect=self.onselect)
        self.ind = []

    def onselect(self, verts):
        path = Path(verts)
        self.ind = np.nonzero([path.contains_point(xy) for xy in self.xys])[0]
        self.fc[:, -1] = self.alpha_other
        self.fc[self.ind, -1] = 1
        self.collection.set_facecolors(self.fc)
        self.canvas.draw_idle()

    def disconnect(self):
        self.lasso.disconnect_events()
        self.fc[:, -1] = 1
        self.collection.set_facecolors(self.fc)
        self.canvas.draw_idle()


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import os
    from tkinter import filedialog

    plt.ion()

    root = filedialog.Tk()
    root.withdraw()
    pot = filedialog.askdirectory(initialdir='/media/vid/DLS DATA/')

    seznam = os.listdir(pot)
    di = {}
    temperatura = []
    absor = []
    # print(seznam)

    for a in seznam:
        if a[-4:] == '.txt':
            key = a.split('.')[0]
            # print('nutr')
            # try:
            with open(pot + '//' + a, encoding='windows-1250') as file:
                next(file)
                for line in file:
                    temp = line.split(',')
                    temperatura.append(float(temp[0]))
                    absor.append(float(temp[1]))
                di[key] = ([temperatura, absor])
            # except:
            #     print(a)
            temperatura = []
            absor = []

    subplot_kw = dict(xlim=(10, 90), ylim=(0.95, 1.3), autoscale_on=False)
    fig, ax = plt.subplots(subplot_kw=subplot_kw)

    pts = ax.scatter(di['SEG1'][0], di['SEG1'][1])
    selector = SelectFromCollection(ax, pts)

    plt.draw()
    plt.pause(0.01)

    raw_input('Press any key to accept selected points')
    print("Selected points:")
    print(selector.xys[selector.ind])
    print(type(selector.xys[selector.ind]))
    selector.disconnect()

    # Block end of script so you can check that the lasso is disconnected.
    raw_input('Press any key to quit')
