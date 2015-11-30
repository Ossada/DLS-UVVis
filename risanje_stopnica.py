__author__ = 'vid'
import matplotlib.pyplot as plt
from tkinter import filedialog
import os

pot = filedialog.askdirectory(initialdir='/media/vid/DLS Data/VidS/Uv vis/')

seznam = os.listdir(pot)
di = {}
temperatura = []
absor = []
print(seznam)

for a in seznam:
    if a[-4:] == '.CSV':
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

print (di)
# print(di)
seznam = list(di.keys())

try:
    fig, ax = plt.subplots(1)
    # plt.plot(di['SEG1'][0], di['SEG1'][1], 'r')
    # plt.plot(di['OHL'][0], di['OHL'][1], 'b', linewidth=3.0)
    plt.plot(di['SEG2'][0], di['SEG2'][1], color='#ff6400', linewidth=3.0)
    # tex = '$c=1mM$ $Seq4Amod3$ $+$' + '\n' '$10mM$ $NaPi$ $+$ $100mM$ $NaCl$' +\
    #     '\n' + '$\\lambda = 600 nm$'
    tex = 'Črnilo'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.80, 0.90, tex, transform=ax.transAxes, fontsize=18,
            verticalalignment='top', bbox=props)
    plt.xlabel('$Temperatura$ $[^{\\circ}C]$', fontsize=22)
    plt.ylabel('$Absorbanca$', fontsize=22)
    # plt.xlim(10,90)
    # plt.ylim(-0.01, 0.01)
    # plt.show()
except:
    pass


for ne in di:
    for i in range(len(di[ne][1])-1):
        vmes = abs(di[ne][1][i+1] - di[ne][1][i])

        if vmes > 0.008:
            try:
                ods = (di[ne][1][i+1] + di[ne][1][i+2])/2 -(di[ne][1][i] + di[ne][1][i-1])/2
                tocka = i
            except:
                pass
    try:

        for i in range(tocka+1, len(di[ne][1])):
            di[ne][1][i] -= ods
    except NameError:
        pass

    #     try:
    #         di[ne][1][i+1] -= ods
    #     except:
    #         pass
    # try:
    #     di[ne][1][tocka] += ods
    # except:
    #     pass
    tocka = 0
    ods = 0

plt.plot(di['SEG2'][0], di['SEG2'][1], 'b', linewidth=1.0)
plt.show()