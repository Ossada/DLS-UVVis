__author__ = 'vid'

import natsort
import tkinter.filedialog as tk
import os
import matplotlib.pyplot as plt


def beriInt(poti):
    intensity1 = []
    intensity2 = []
    time = []
    with open(poti, encoding='windows-1250') as file:
        for line in file:
            temp = line.strip().split('\t')
            next(file)
            # print('berem' + str(temp))
            if '"Count Rate"' in temp:
                # print('dela')
                break
        for line in file:
            temp = line.strip().split('\t')
            time.append(float(temp[0]))
            intensity1.append(float(temp[1]))
            intensity2.append(float(temp[2]))

    return time, intensity1, intensity2


def beriTemp(poti):
    temperatura = []
    with open(poti, 'r') as file:
        try:
            for line in file:
                temperatura.append(float(line.split(' ')[0]))
                for i in range(4):
                    next(file)
        except StopIteration:
            pass
    return temperatura


def risi(xdata, ydata1, ydata2):
    plt.plot(xdata, ydata1)
    plt.plot(xdata, ydata2)
    plt.savefig('/home/vid/IJS/Meritve')  #Test path


root = tk.Tk()
root.withdraw()

a = tk.askopenfilename(initialdir='/home/vid/IJS/Meritve/1611/')
test = beriInt(a)
risi(test[0], test[1], test[2])
