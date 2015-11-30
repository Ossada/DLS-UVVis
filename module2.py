from lomnikol import *
import matplotlib.pyplot as plt
import statistics as st
#
# dif = []
# diferr = []

# with open('Sheet1.dat') as file:
#     for line in file:
#         temp = line.strip().split('\t')
#         dif.append(float(temp[0]))
#         diferr.append(float(temp[1]))
#
# temperatura = [24.7, 24.7, 24.7, 24.8, 24.8, 24.8, 24.9, 24.9, 24.9, 23.2, 23.3, 23.7, 24.1, 24.3, 23.3, 23.1, 23.1, 24.5, 24.5]
# # temperatura.append(float(input('VpiĂ„â€šĂ˘â‚¬ĹľÄ‚â€žĂ˘â‚¬Â¦Ă„â€šĂ˘â‚¬Ä…Ä‚ËĂ˘â€šÂ¬Ă‹â€ˇi zadnjo temperaturo merjenja (uporabi decimalno piko!): ')))
#
#
#
# skupno = []
# for i in range(len(temperatura)):
#     skupno.append([dif[i], diferr[i], temperatura[i]])
#
# #print(skupno)
#
#
# f = open('normalizirano.txt', 'w')
# for i in range(len(temperatura)):
#     a = skupno[i][0]*((skupno[i][2]+273)/298)*(visk(skupno[i][2])/visk(25))
#     aer = skupno[i][1]*((skupno[i][2]+273)/298)*(visk(skupno[i][2])/visk(25))
#
#     f.write(str(a) + '\t' + str(aer) + '\n')
#
# f.close()

temperatura = []
with open('Book1.txt', 'r') as file:
    for line in file:
        temperatura.append(float(line.split('\t')[0]))

# print(temperatura

D = []
q = q2(70)
visk26 = visk(26)
err = []
with open('fji.txt', 'r') as file:
    for line in file:
        try:
            # print(line)
            D.append(float(line.split()[0])/q)
            err.append(float(line.split()[1])/float(line.split()[0]))
        except IndexError:
            print('Vrstic je več kot meritev!')
            pass

Dnorm = []

for i in range(len(temperatura)):
    temp = D[i]*(299/(temperatura[i]+273))*(visk(temperatura[i])/visk26)*1000
    Dnorm.append(temp)

print(Dnorm)
try:
    for i in range(len(Dnorm)):
        err[i]=Dnorm[i]*err[i]
except IndexError:
    print('Neki je predolgo/prekratko')
    pass

# plt.plot(temperatura, Dnorm)
Dpovp = st.mean(Dnorm)
Ddev = st.stdev(Dnorm)

fig, axs = plt.subplots(nrows=2, ncols=1, sharex=True)
ax = axs[0]
ax.errorbar(temperatura, Dnorm, xerr=None, yerr=err[:59])
ax.set_ylim(0,9e-12)
tex = '$\\overline{}={:.4e}$'.format('{D}', Dpovp) + '\n' + '$\sigma = {:.4e}$'.format(Ddev) + '\n' + \
    '$\\overline{}={:.4f}$'.format('{D}', Dpovp*10e11) + '$(1\\pm{:.4f})e-12$'.format( Ddev/Dpovp)

props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax.text(0.58, 0.40, tex, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=props)
ax.set_title('D normaliziran')

ax = axs[1]
ax.errorbar(temperatura, Dnorm, xerr=None, yerr=err[:59])
ax.set_title('D normaliziran povečan')
plt.show()