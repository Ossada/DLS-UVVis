import os
import tkinter.filedialog as tk
import natsort


pot = '/media/vid/DLS DATA/seq4Amod35/2112'
seznam = os.listdir(pot)
seznam = natsort.natsorted(seznam)
key = 'OHL'
temp = []

for i in seznam:
    if key in i:
        print(i)
        if '.txt' in i:
            continue
        with open(pot + '/' + i, encoding='windows-1250') as file:
            next(file)
            for line in file:
                temp.append(line)

print(len(temp))
# print(temp)
f = open(pot + '//' + key[:4] + '.txt', 'w')
for j in range(len(temp)):
    f.write(temp[j])
    # print(temp[j])

f.close()
