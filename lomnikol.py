import math


def n(T, lamb, ro):
    Tref = 273.15

    lambdaref = 589  # v nanometrih
    roref = 1000
    a0 = 0.244257733
    a1 = 9.74634476*10**(-3)
    a2 = -3.73234996*10**(-3)
    a3 = 2.68678472*10**(-4)
    a4 = 1.58920570*10**(-3)
    a5 = 2.45934259*10**(-3)
    a6 = 0.900704920
    a7 = -1.66626219*10**(-2)
    lambUV = 0.2292020
    lambIR = 5.432937

    B = a0 + a1*(ro/roref) + a2*(T/Tref) + a3*(T/Tref)*(lamb/lambdaref)**2 + \
        a4/(lamb/lambdaref)**2 + a5/((lamb/lambdaref)**2 - lambUV**2) + \
        a6/((lamb/lambdaref)**2 - lambIR**2) + a7*(ro/roref)**2

    return pow(((2*B + 1)/(1 - B)), 0.5)


# print(n(298, 700, 1000))

def visk(T):  # V stopinjah celzija
    vis20 = 1006.2  # v Pa s x10^-6
    b = ((20-T)/(T+96))*(1.2378 - 1.37*(20-T)*10**(-3) + \
        5.7*((20-T)**2)*10**(-6))
    return vis20 * 10**(b)

# print(visk(25.7))


def q2(fi):
    return ((4*math.pi*1.33*math.sin(fi*math.pi/360))/(532*10**(-9)))**2
