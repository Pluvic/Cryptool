# This file contains functions related to prime numbers for the Cryptool project.

import random

def temoinMillerRabin(a, p):
    """Perform the Miller-Rabin primality test for a given base a and odd integer p > 2."""
    q = p - 1
    k = 0

    while q % 2 == 0:
        q //= 2
        k += 1
    
    b = pow(a, q, p)

    if b == 1 or b == p - 1:
        return True
    
    while k > 0:
        b = (b * b) % p
        if b == p - 1:
            return True
        k -= 1
    return False

def millerRabin(p, n):
    """Perform the Miller-Rabin primality test n times to determine if p is probably prime."""

    if p <= 1 or p == 4:
        return False
    if p <= 3:
        return True

    for _ in range(n):
        a = random.randint(2, p - 2)
        if not temoinMillerRabin(a, p):
            return False
    return True

def gatherPrimes(fileName):
    """Read prime numbers from a file and return them as a list of integers."""
    primes = []
    with open(fileName, 'r') as file:
        for line in file:
            primes.append(int(line.strip()))
    return primes

def testPrime(p):
    """Test if p is prime using trial division up to the square root of p."""

    primeList = gatherPrimes("primes_100000.txt")
    for prime in primeList:
        if prime == p:
            return True
        if p % prime == 0:
            return False
        
    return millerRabin(p, 40)

def genPrime(n):
    # Générer un nombre aléatoire
    x = random.randint(1<<(n-1), (1<<(n)))
    if x % 2 == 0:
        x += 1

    while (not testPrime(x)):
        x += 2
    return x
