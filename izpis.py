import os
import scipy.optimize as sp
import numpy as np
import math
import lmfit
import matplotlib.pyplot as plt
from matplotlib.patches import *
import natsort
from tkinter import filedialog


def beri(poti):
    lagtime = []
    corr = []
    with open(poti, encoding='windows-1250') as file:
        for i in range(33):
            next(file)
        for line in file:
            temp = line.strip().split('\t')
            if '' in temp:
                break
            lagtime.append(float(temp[0]))
            corr.append(float(temp[1]))

    return np.array(lagtime), np.array(corr)


def f(x, y0, jd, A, f1, f2, s1, s2):
    return y0 + (1 + jd * ((A * np.exp(-pow(f1 * x, s1))) + ((1 - A) * np.exp(-pow(f2 * x, s2))) - 1)) ** 2


def fl(x, f1, A, y0):
    return A*np.exp(-x*f1)+y0


def q2(fi):
    return ((4*math.pi*1.33*math.sin(fi*math.pi/360))/(532*10**(-9)))**2


def risanje():
    fig, ax = plt.subplots(1)
    plt.plot(xdata, ydata, 'bo', alpha=0.8)
    plt.plot(xdata, f(xdata, param[0], param[1], param[2], param[3], param[4], param[5], param[6]), 'r')
    # plt.plot(xdata, fl(xdata, latp[0], latp[1], latp[2]), 'r', linewidth=2.0)
    plt.xscale('log')
    plt.xlabel('$Time$ $[ms]$', fontsize=14)
    plt.ylabel('$g(2)-1$', fontsize=14)
    plt.ylim(0, 1.1)
    text = '$y_{0}=%.4f$\n$j_{d}=%.4f$\n$A=%.4f$\n$f_{1}=%.4f$\n$f_{2}=%.4f$\n$s_{1}=%.4f$\n$s_{2}=%.4f$' \
          % (param[0], param[1], param[2], param[3], param[4], param[5], param[6])
    # text = '$f_{3}={0}$\n$A={1}$\n$y_{4}={2}$'.format(round(latp[0], 4), round(latp[1], 4), round(latp[2], 4), "{1}", "{0}")
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.70, 0.95, text, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=props)
    # plt.show()
    plt.savefig(pot + '/' + str(a) + '.jpg')
    plt.close()


def premica(x, D):
    return D*x


def risanje2(seznamk, seznamf, seznamfer, ime):
    koti = np.array(seznamk)
    fji = np.array(seznamf)
    fjierr = np.array(seznamfer)
    para, error = sp.curve_fit(premica, koti, fji, sigma=fjierr)
    par = para[0] * 10 ** 3
    t = np.linspace(0, 9e14, 100)

    fig, ax = plt.subplots(1)
    plt.plot(koti, fji, 'bo', alpha=0.8)
    plt.plot(t, premica(t, para),  'r')
    plt.xlabel('$q^{2}$ $[m^{2}/s]$', fontsize=14)
    plt.ylabel('$f_{1}$ $kHz$', fontsize=14)
    plt.xlim(xmin=0)
    tex = '$D={:0=8.7f}$'.format(par/1e-10) + '$\\times 10^{-10}$' + ' $m^{2}/s$'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.60, 0.50, tex, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=props)

    plt.savefig(ime + '.jpg')
    plt.close()


def beri2(pot):
    f1 = []
    with open(pot) as file:
        for line in file:
            if 'f1' in line:
                f1.append(line.split(' ')[1:])
    return f1


pot = filedialog.askdirectory(initialdir='/media/vid/DLS Data/VidS/')
seznam = os.listdir(pot)
seznam = natsort.natsorted(seznam)
# print(seznam)

param = [-0.02, 0.8, 0.01, 52, 0.2, 1, 1]
paramstr = ['y0', 'jd', 'A', 'f1', 'f2', 's1', 's2']
latp = [3, 0.9, 0.01]
latpstr = ['f1', 'A', 'y0']

koti = []
fji = []
fjierr = []
serije = {}

file = open('parametri.txt', 'w')

for a in seznam:

    if a[-4:] == '.ASC':

        if '_' in a:

            try:

                b = a.split('_')
                print('razdelim')
                kot = float(b[0])
                key = float(b[1][0])
                xdata, ydata = beri(a)
                if kot > 100:
                    param = [-0.0919, 0.692, 0.2635, 124.95, 0.424, 0.9875, 0.8944]

                param, err = sp.curve_fit(f, xdata, ydata, param)
                print('fitam ' + a)

                vekt = q2(kot)
                file.write(a + '\n' + str(kot) + '\n' + str(vekt) + '\n')

                for i in range(len(param)):
                    file.write(str(paramstr[i]) + '  ' + str(param[i]) + ' ' + str(err[i][i]) + '\n')

                if key in serije:
                    if param[3] > param[4]:
                        serije[key].append([vekt, param[3], np.sqrt(err[3][3])])
                    else:
                        serije[key].append([vekt, param[4], np.sqrt(err[4][4])])
                else:
                    if param[3] > param[4]:
                        serije[key] = [[vekt, param[3], np.sqrt(err[3][3])]]
                    else:
                        serije[key] = [[vekt, param[4], np.sqrt(err[4][4])]]

                risanje()

                file.write('\n')

            except:
                print('Z datoteko ' + str(a) + ' so problemi (ne konvergira, ali ni prav poimenovana).')
                pass
        else:
                key = a
                xdata, ydata = beri(pot + '/' + a)
                param, err = sp.curve_fit(f, xdata, ydata, param)
                print('fitam ' + a)
                # print(err)
                file.write(a + '\n')
                try:
                    for i in range(len(param)):
                        file.write(str(paramstr[i]) + ' ' + str(param[i]) + ' ' + str(err[i][i]) + '\n')
                except TypeError:
                    print('Ne fita v redu! Neskončna napaka!')
                risanje()
                file.write('\n')



# for i in serije:
#     koti = []
#     fji = []
#     fjierr = []
#
#     for j in range(len(serije[i])):
#         koti.append(serije[i][j][0])
#         fji.append(serije[i][j][1])
#         fjierr.append(serije[i][j][2])
#     text = str(i)
#     risanje2(koti, fji, fjierr, text)

file.close()

j = beri2('parametri.txt')
file = open('fji.txt', 'w')
for i in range(len(j)):
    for k in range(len(j[i])):
        file.write(str(j[i][k]) + ' ')
file.close()

