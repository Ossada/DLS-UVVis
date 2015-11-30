__author__ = 'vid'
import os
import csv
import natsort
from tkinter import filedialog
import copy

pot = filedialog.askdirectory(initialdir='/media/vid/DLS Data/VidS/Uv vis/seq4Amod3 0.5mM/0.2 inkrement')
seznam = os.listdir(pot)
seznam = natsort.natsorted(seznam)
ime1 = 'OHL'
print(ime1)

# print(seznam)
j = 0
temp = []
tex = []
prejsni = ""

for i in seznam:
    if i[-4:] == '.CSV' and '_' in i:
        print(i)

        ime = i.split('_')[0]
        print(ime)
        # try:
        #     ime1 = enumerate(seznam)[j-1][1].split('_')[0]
        #     print(ime1,'uizui')
        # except:
        #     pass


        with open(pot + '/' + i, 'r', encoding='windows-1250') as file:

            next(file)
            for line in file:
                a , b = line.split(',')
                b = b[:-2]
                tex.append([a, b])
                #print(line.split(','))


        print(len(tex))

        # with open(pot+'/'+i[1], 'r', encoding='windows-1250') as file:
        #     test = csv.reader(file)
        #     next(csv.reader(file))
        #     sez = list(test)
        #     print(sez)
        print(ime == ime1)
        if ime == copy.copy(ime1):
            temp += tex
            # print(temp)
        # if ime != ime1 and j == 0:
        #     temp += sez

        else:
            with open(pot + '/' + ime + '.CSV', 'w') as f:
                writer = csv.writer(f)
                writer.writerows(temp)
                print('napisu sm')
            tex = []
            temp = []

        ime1 = ime
        sez = []
        j += 1
        tex = []

with open(pot + '/' + ime + '.CSV', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(temp)
        print('napisu sm')