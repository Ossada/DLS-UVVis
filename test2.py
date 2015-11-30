__author__ = 'root'
for i in range(10):
    print(i)
from sys import argv

a=open(argv[1],'r')

print (argv[0],"to je file")

for i in a:
    print (i)