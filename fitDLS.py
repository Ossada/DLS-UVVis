__author__ = 'vid'
import os
import numpy as np
import lmfit as lm
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


def slowfastmode(params, xdata, ydata):
    A = params['A'].value
    y0 = params['y0'].value
    jd = params['jd'].value
    f1 = params['f1'].value
    f2 = params['f2'].value
    s1 = params['s1'].value
    s2 = params['s2'].value

    model = y0 + (1 + jd * ((A * np.exp(-pow(f1 * xdata, s1))) +
                            ((1 - A) * np.exp(-pow(f2 * xdata, s2))) - 1)) ** 2
    return model - ydata


def q2(fi):
    return ((4*math.pi*1.33*math.sin(fi*math.pi/360))/(532*10**(-9)))**2


def parametri(slovar):
    temp = []
    for i in slovar:
        temp.append(((str(params[i]).split(',')[1]).split('=')[1]).split('+/-'))
    return temp


def zapis(sez):
    for i in sez:
        val, err = i
        file.write(val + ' ' + err + '\n')


def risanje(i):
    fig, ax = plt.subplots(1)
    plt.plot(xdata, ydata, 'bo', alpha=0.8)
    plt.plot(xdata[:175], final, 'r', linewidth=2)
    plt.xscale('log')
    plt.xlabel('$\\tau$ $[ms]$', fontsize=22)
    plt.ylabel('$g^{(2)}(\\tau)-1$', fontsize=22)
    plt.ylim(0, 1.1)
    plt.title('$0.5mM$' + ' ' + '$Seq4Amod3,$' + '$T={0:4.2f}$'.format(temp[i]))
    text = '$y_{0}=%.4f$\n$j_{d}=%.4f$\n$A=%.4f$\n$f_{1}=%.4f$\n$f_{2}=%.4f$\n$s_{1}=%.4f$\n$s_{2}=%.4f$' \
          % (float(tem[1][0]), float(tem[2][0]), float(tem[0][0]), float(tem[3][0]),
             float(tem[4][0]), float(tem[5][0]), float(tem[6][0]))
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.70, 0.95, text, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=props)
    plt.savefig(pot + '/' + str(a) + '.jpg')
    plt.close()

def risanje2(st):
    barve = ['k', 'b', 'g', 'm', 'r', 'y']

    if st%10 == 0:
        k += 1
        fig, ax = plt.subplots(1)
        plt.xscale('log')
        plt.xlabel('$\\tau$ $[ms]$', fontsize=22)
        plt.ylabel('$g^{(2)}(\\tau)-1$', fontsize=22)
        plt.ylim(0, 1.1)
        plt.plot(xdata, ydata, barve[k])


root = tk.Tk()
root.withdraw()
pot = filedialog.askdirectory(initialdir='/media/vid/DLS Data/VidS/seq4Amod3')
seznam = os.listdir(pot)
seznam = natsort.natsorted(seznam)

fji = []
fjierr = []
serije = {}
temp = []
indeks = -1

params = lm.Parameters()
params.add('A', value=0.01)
params.add('y0', value=0)
params.add('jd', value=0.7, min=0, max=1)
params.add('f1', value=430, min=0)
params.add('f2', value=1.5)
params.add('s1', value=1, min=0, max=1)
params.add('s2', value=1, min=0, max=1)

pot1 = filedialog.askopenfilename(initialdir=pot)
print(pot1)
k=-1  #test

with open(pot1, 'r') as file:
    try:
        for line in file:
            temp.append(float(line.split(' ')[0]))  # Odpre datoteko s temperaturami, uporabljeno za izpis grafov
            for i in range(4):
                next(file)
    except StopIteration:
        pass

file = open(pot + '/parametri.txt', 'w')

for a in seznam:
    if a[-4:] == '.ASC':
        xdata, ydata = beri(pot + '/' + a)
        try:
            indeks += 1
            result = lm.minimize(slowfastmode, params, args=(xdata[:175], ydata[:175]))
            print('Datoteki ' + a + ' se prilega krivulja!')
            final = ydata[:175] + result.residual
            tem = parametri(params)
            lm.report_fit(params, show_correl=False)
            file.write(a + '\n')
            zapis(tem)
            risanje(indeks)
            # risanje2(indeks)
        except:
            print('Z ' + a + ' je neki narobe!')
            plt.plot(xdata, ydata, 'ro')
            plt.xscale('log')
            plt.savefig(pot + '/' + str(a) + '.jpg')
            plt.close()
            pass
    if a == 'AutoSaveFileName0057.ASC':
        break
plt.show()
file.close()
# print(temp)
#
# fig, ax = plt.subplots(1)
# plt.xscale('log')
# plt.xlabel('$\\tau$ $[ms]$', fontsize=22)
# plt.ylabel('$g^{(2)}(\\tau)-1$', fontsize=22)
# plt.ylim(0, 1.1)
# barve =  ['k', 'b', 'g', 'm', 'r', 'y', 'c']
# for a in seznam:
#     if a[-4:] =='.ASC':
#         xdata, ydata = beri(pot + '/' + a)
#         indeks +=1
#         if indeks%11==0:
#             plt.plot(xdata, ydata, barve[indeks//10], label='{0:4.2f} °C'.format(temp[indeks]), linewidth=2)
# plt.legend()
# plt.show()