# This file contains functions related to prime numbers for the Cryptool project.

import random

def temoinMillerRabin(a: int, p: int) -> bool:
    """Perform the Miller-Rabin primality test.
    
    Args:
        a (int): The base for the test.
        p (int): The odd integer to be tested for primality.
        
    Returns:
        bool: True if p is probably prime, False if p is composite.
    """
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

def millerRabin(p: int, n: int) -> bool:
    """Perform the Miller-Rabin primality test n times to determine if p is probably prime.
    
    Args:
        p (int): The integer to be tested for primality.
        n (int): The number of iterations to perform.
        
    Returns:
        bool: True if p is probably prime, False if p is composite.
    """

    if p <= 1 or p == 4:
        return False
    if p <= 3:
        return True

    for _ in range(n):
        a = random.randint(2, p - 2)
        if not temoinMillerRabin(a, p):
            return False
    return True

def gatherPrimes(filePath: str) -> list[int]:
    """Read prime numbers from a file and return them as a list of integers.
    
    Args:
        filePath (str): The path to the file containing prime numbers.
        
    Returns:
        list[int]: A list of prime numbers read from the file.
    """
    primes = []
    with open(filePath, 'r') as file:
        for line in file:
            primes.append(int(line.strip()))
    return primes

def isPrime(p: int) -> bool:
    """Test if p is prime using trial division up to the square root of p.
    
    Args:
        p (int): The integer to be tested for primality.

    Returns:
        bool: True if p is probably prime, False if p is composite.
    """

    primeList = gatherPrimes("primes_100000.txt")
    for prime in primeList:
        if prime == p:
            return True
        if p % prime == 0:
            return False
        
    return millerRabin(p, 40)

def genPrime(n: int) -> int:
    """ Generate a random prime number with n bits.
    
    Args:
        n (int): The number of bits for the prime number.
        
    Returns:
        int: A random prime number with n bits.
    """
    x = random.randint(1<<(n-1), (1<<(n)))
    if x % 2 == 0:
        x += 1

    while (not isPrime(x)):
        x += 2
    return x
