__author__ = 'vid'
import matplotlib.pyplot as plt
from matplotlib.patches import *
import tkinter.filedialog as tk
import os


def beri(poti):
    tempe = []
    time = []
    with open(poti, encoding='windows-1250') as file:
        for line in file:
            temp = line.strip().split(' ')
            if '' in temp:
                break
            tempe.append(float(temp[0]))
            time.append(float(temp[1]))

    return np.array(time), np.array(tempe)


def risanje():
    fig, ax = plt.subplots(1)
    plt.plot(time1, temp1, 'r', alpha=0.8)
    plt.xlabel('$Čas$ $[s]$', fontsize=22)
    plt.ylabel('$Temperatura [^{\\circ}C]$', fontsize=22)
    # plt.show()
    plt.savefig(str(i) + '.jpeg')
    plt.close()


pot = tk.askdirectory()
seznam = os.listdir(pot)

for i in seznam:
    if 'Temperatura' in i:
        try:
            print('res je!')
            time1, temp1 = beri(i)
            risanje()
        except IndexError:
            print(i)
        except UnicodeDecodeError:
            print(i)