__author__ = 'vid'
import os
import math
import natsort


def q2(fi):
    return ((4*math.pi*1.33*math.sin(fi*math.pi/360))/(532*10**(-9)))**2



pot = os.getcwd()
seznam = os.listdir(pot)
slovar = {}

seznam = natsort.natsorted(seznam)
print(seznam)
for a in seznam:
    if a[-4:] == '.ASC':

        b = a.split('_')
        kot = float(b[0])
        key = b[1][0]

        vekt = q2(kot)

        if key in slovar:
            slovar[key].append([vekt, b[1]])
        else:
            slovar[key] = [[vekt, b[1]]]

