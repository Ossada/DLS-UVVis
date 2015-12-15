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


def risi(xdata, ydat1, ydat2, ind):
    plt.plot(xdata, ydat1)
    plt.plot(xdata, ydat2)
    plt.xlabel('$Time$ $[s]$', fontsize=22)
    plt.ylabel('$Count$ $rate$ $[kHz]$', fontsize=22)
    plt.title('Seq4Amod5, T={0:4.2f}'.format(tempe[ind]))
    plt.savefig('/home/vid/IJS/Meritve/1611/nov seq4amod5/' + str(a)[:-4] + '.jpg')  #Test path
    print('Graf ' + str(a)[:-4] + ' shranjen!')
    plt.close()


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
indeks = 0
risanje = True  #Če True, se za vsako temp izriše graf

povprecja = open(pot + '/povprecja.txt', 'w')

for a in seznam:
    if a[-4:] == '.ASC':
        xdata, ydata1, ydata2 = beriInt(pot + '/' + a)

        if risanje:
            risi(xdata, ydata1, ydata2, indeks)

        c = povp(ydata1, ydata2)
        povprecja.write(str(tempe[indeks]) + ',' + str(c) + '\n')
        indeks += 1

povprecja.close()

