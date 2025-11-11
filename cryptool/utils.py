# This file contains utility functions for the Cryptool project.

def gcd(a, b):
    """Calculate the greatest common divisor of a and b using the Euclidean algorithm."""
    while b:
        a, b = b, a % b
    return a

def bezout(a, b):
    """Calculate the bezout coeficient"""

    u0, u1 = 1, 0
    v0, v1 = 0, 1

    while b != 0:
        q = a // b
        r = a % b
        a, b = b, r
        u0, u1 = u1, u0 - q*u1
        v0, v1 = v1, v0 - q*v1

    if a < 0:
        a, u0, v0 = -a, -u0, -v0
    
    return a, u0, v0

def inverse(x, n):
    """Calculate the inverse of x modulo n"""

    thisGcd = gcd(x, n)

    if thisGcd != 1:
        print(f"Error: The number {x} do not have an inverse modulo {n}.")

    _, be1, _ = bezout(x, n)
    return be1 % n

def primalityList(numList):
    for i in range(len(numList)):
        for j in range(i+1,len(numList)):
            if gcd(numList[i], numList[j]) != 1:
                return False
            
    return True

def chineseRemainder(listRemainders, listModulos):
    if len(listRemainders) != len(listModulos):
        print("The 2 lists need to have the same size.")
        return
    
    if not primalityList(listModulos):
        print("The modulos need to be pairwise coprime.")
        return
    
    N = 1
    x = 0
    for modulo in listModulos:
        N *= modulo

    for i, j in zip(listRemainders, listModulos):
        ni = N // j
        bi = inverse(ni, j)
        x += i * ni * bi
    
    return x % N