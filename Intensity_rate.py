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


def povp(data1, data2):
    a = 0
    if len(data1) == len(data2):
        for i in range(len(data1)):
            a += (data1[i] + data2[i])
        povpre = a/(2*len(data1))

    if len(data1) > len(data2):
        for i in range(len(data2)):
            a += (data1[i] + data2[i])
        povpre = a/(2*len(data2))

    return povpre



root = tk.Tk()
root.withdraw()
pot = tk.askdirectory(initialdir='/home/vid/IJS/Meritve/1611/')
seznam = os.listdir(pot)
seznam  = natsort.natsorted(seznam)
pot1 = tk.askopenfilename(initialdir=pot)
tempe = beriTemp(pot1)

for a in seznam:
    if a[-4:] == '.ASC':
        xdata, ydata = beriInt(pot + '/' + a)
