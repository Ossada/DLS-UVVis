import matplotlib.pyplot as plt
from matplotlib.patches import *
from lomnikol import *
import statistics as st
import tkinter.filedialog as tk

temp = []
pot = tk.askopenfilename(initialdir='/media/vid/DLS Data/VidS/seq4Amod3/mod3 kot 110/ohl')  # odpre temperaturo
with open(pot, 'r') as file:
    try:
        for line in file:
            temp.append(float(line.split(' ')[0]))
            for i in range(4):
                next(file)
    except StopIteration:
        pass

# with open('vsaka5a.txt', 'w') as f:
#     for i in temp:
#         f.write(i)

parametri = {'A': [], 'y0': [], 'jd': [], 'f1': [], 'f2': [], 's1': [], 's2': []}
error = {'A': [], 'y0': [], 'jd': [], 'f1': [], 'f2': [], 's1': [], 's2': []}

pot = tk.askopenfilename(initialdir='/media/vid/DLS Data/VidS/seq4Amod3/mod3 kot 110/ohl')
f1 = open(pot, 'r')
for i, lin in enumerate(f1):
    # print(lin)
    if (i+1)%8 == 2:
        parametri['A'].append(float(lin.split('   ')[0]))
        error['A'].append(float(lin.split('   ')[1]))
    if (i+1)%8 == 3:
        parametri['y0'].append(float(lin.split('   ')[0]))
        error['y0'].append(float(lin.split('   ')[1]))
    if (i+1)%8 == 4:
        parametri['jd'].append(float(lin.split('   ')[0]))
        error['jd'].append(float(lin.split('   ')[1]))
    if (i+1)%8 == 5:
        parametri['f1'].append(float(lin.split('   ')[0]))
        error['f1'].append(float(lin.split('   ')[1]))
    if (i+1)%8 == 6:
        parametri['f2'].append(float(lin.split('   ')[0]))
        error['f2'].append(float(lin.split('   ')[1]))
    if (i+1)%8 == 7:
        parametri['s1'].append(float(lin.split('   ')[0]))
        error['s1'].append(float(lin.split('   ')[1]))
    if (i+1)%8 == 0:
        parametri['s2'].append(float(lin.split('   ')[0]))
        error['s2'].append(float(lin.split('   ')[1]))
print(len(parametri['A']))
# print(len(error['f1']))
# print(len(temp))
# print(error['f1'])
f1.close()

Dnorm = []
D = []
q = q2(110)
visk26 = visk(26)
err = []

for j in range(len(parametri['f1'])):
    D.append(parametri['f1'][j]/q)

for k in range(len(parametri['f1'])):
    err.append(error['f1'][k]/parametri['f1'][k])

print(len(D))
print(len(temp))
dolg = len(D)

for i in range(len(temp)):
    temp0 = D[i]*(299/(temp[i]+273))*(visk(temp[i])/visk26)*1000
    Dnorm.append(temp0)
file = open('dnorm_ohl.txt', 'w')
for i in Dnorm:
    file.write(str(i) + '\n')

file.close()

try:
    for i in range(len(Dnorm)):
        err[i] = Dnorm[i]*err[i]
except IndexError:
    print('Neki je predolgo/prekratko')
    pass
# print(err)
# plt.plot(temperatura, Dnorm)
Dpovp = st.mean(Dnorm[1:61])
# print(Dpovp)
Ddev = st.stdev(Dnorm[1:61])
x = []
# try:
#     for m in err:
#         if m > Ddev:
#             print('nutr')
#             print(m)
#             x.append(err.index(m))
#
#     for i in x:
#         err.remove(err[i])
#         Dnorm.remove(Dnorm[i])
# except IndexError:
#     pass
print(len(temp))
print(len(Dnorm))
dolg = len(Dnorm)
# fig, axs = plt.subplots(nrows=1, ncols=1, sharex=True)
# ax = axs[0]
# # ax.errorbar(temp[1:29], Dnorm[1:29], xerr=None, yerr=err[1:29])
# ax.plot(temp, Dnorm,  color='b')
# ax.set_ylim(0, 9e-10)
# ax.set_xlim(35, 92)
# tex = '$\\overline{}={:.4e}$'.format('{D}', Dpovp) + '\n' + '$\sigma = {:.4e}$'.format(Ddev)
# props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
# ax.text(0.55, 0.90, tex, transform=ax.transAxes, fontsize=14,
#         verticalalignment='top', bbox=props)
# ax.set_title('D normaliziran')
#
# ax = axs[0]
# ax.errorbar(temp, Dnorm, xerr=None, yerr=err,  color='b')
# ax.set_title('D normaliziran povečan')
# ax.set_xlim(35, 92)
# ax.set_ylim(1e-10, 2e-10)
# plt.show()

fig, ax = plt.subplots(1)
plt.errorbar(temp[1:61], Dnorm[1:61], xerr=None, yerr=err[1:61], color='r', linewidth=2, elinewidth=1)
plt.title('$Normalizirana$ $difuzijska$ $konstanta$', fontsize=22)
plt.xlabel('$Temperatura [^{\\circ}C]$', fontsize=22)
plt.ylabel('$D [\\times 10^{-10} m^{2}/s]$', fontsize=22)
text = '$\\overline{}={:.4e}$'.format('{D}', Dpovp) + '\n' + '$\sigma = {:.4e}$'.format(Ddev)
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax.text(0.45, 0.95, text, transform=ax.transAxes, fontsize=18,
        verticalalignment='top', bbox=props)
plt.show()


a = len(temp)


fig, axs = plt.subplots(nrows=2, ncols=1, sharex=True)

ax = axs[0]
ax.errorbar(temp, parametri['f1'], yerr=error['f1'], color='b')
ax.set_title('$f_{1}(T)$', fontsize=22)


ax = axs[1]
ax.errorbar(temp, parametri['f2'], yerr=error['f2'],  color='b')
ax.set_title('$f_{2}(T)$', fontsize=22)
ax.set_xlabel('$Temperatura [^{\\circ}C]$', fontsize=22)


plt.show()
fig, axs = plt.subplots(nrows=2, ncols=1, sharex=True)

ax = axs[0]
ax.errorbar(temp, parametri['s1'], yerr=error['s1'], color='b')
ax.set_title('$s_{1}(T)$', fontsize=22)
ax.set_ylim(0, 1.1)
ax = axs[1]
ax.errorbar(temp[:a], parametri['s2'], yerr=error['s2'],  color='b')
ax.set_title('$s_{2}(T)$', fontsize=22)
ax.set_xlabel('$Temperatura [^{\\circ}C]$', fontsize=22)
plt.show()

plt.errorbar(temp[:60], parametri['A'][:60], yerr=error['A'][:60])
plt.ylabel('$Amplituda$ $A$', fontsize=20)
plt.xlabel('$Temperatura [^{\\circ}C]$', fontsize=20)
plt.show()