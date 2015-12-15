__author__ = 'vid'

import natsort
from tkinter import filedialog
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
                print('dela')
                break
        for line in file:
            temp = line.strip().split('\t')



a = filedialog.askopenfilename(initialdir='/home/vid/IJS/Meritve/1611/')
beriInt(a)