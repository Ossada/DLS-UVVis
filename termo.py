__author__ = 'vid'
import sys
import serial
from datetime import datetime
import time
import numpy as np


def pretvorba(x):
# Funkcija pretvori upornost v temperaturo
    r0 = 100.00
    # Parametri so za pt100 sondo v območju od 0 do 661°C
    a = 3.90830 * 10 ** (-3)
    b = -5.77500 * 10 ** (-7)
    # R(T) = R0*(1 + a*T + b*T*T)  spreminjanje upornosti s temperaturo
    t1 = (-r0 * a + np.sqrt(a * a * r0 * r0 - 4 * r0 * b * (r0 - x))) / (2 * r0 * b)
    # Obrnjena formula
    return round(t1, 3)


ser = serial.Serial()
ser.baudrate = 9600
ser.bytesize = serial.SEVENBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_TWO
ser.xonxoff = 0
ser.rtscts = 0
ser.dsrdtr = 0
ser.timeout = 0.1
ser.port = "/dev/ttyUSB0"
# Ime vrat na katere je priklopljen multimeter (na windows sistemu ponavadi COM(številka))

a = 'D'
# Poziv multimetru, vsaka črka je v redu.
a = bytes(a, 'utf-8')
# Pretvorba v bajte, python 3 in višji tega ne delajo samodejno
i = 0
t = time.time()
# Začetni čas
ime = 'Temperatura_n' + str(datetime.now().date())
print(ime)
file = open(ime + '.txt', 'w')

ser.open()
# Odpre vrata
ser.setRTS(False)
ser.setDTR(True)
ser.flushOutput()

try:
    while i == 0:

        ser.write(a)
        minute = round(time.time() - t, 4)

        temp = str(ser.readline()).strip().split('k')
        # Razbije izpis na več delov
        # (b'~OH 1.0958kOhm\r   1.0958    \r   1.0958    \r
        # 1.0958    \r') je originalen izpis, zanima nas prva meritev
        temp = temp[0].split(' ')
        # prejšnji prvi del razbijem na dva dela, številko in znake
        temp = float(temp[1])
        # nazadnje spremenim številko v tip float (tako lahko z njo operiram)
        print(pretvorba(temp * 100))
        # pomnoženo s 100 ker je podatek v kOhm (za 10x prevelik kot bi moral biti)
        file.write(str(pretvorba(temp * 100)) + ' ' + str(minute) + '\n')

        if time.time() - t > 1200*60:
        # Zajemanje podatkov se ustavi na dva načina, ctrl+C v komandni vrstici ali pa po
        # določenem času, ki ga podamo v zgornji vrstici (v sekundah)
            ser.close()
            file.close()
            break

        time.sleep(10)

except KeyboardInterrupt:
    ser.close()
    file.close()
