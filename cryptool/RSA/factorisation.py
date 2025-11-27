# This file contains functions related to RSA encryption for the Cryptool project.

from math import sqrt, ceil
from cryptool.utils import gcd

def naiveFactor(N: int) -> tuple[int, int] | None:
    """Perform naive factorization of n by trial division.
    
    Args:
        N (int): The integer to be factorized.
        
    Returns:
        tuple[int, int] | None: A tuple containing the two factors of N if found, otherwise None.
    """

    limit = ceil(sqrt(N))

    for i in range(limit, 1, -1):
        if N % i == 0:
            return i, N // i
        
    return None

def _isSquare(n: int) -> bool:
    """Check if n is a perfect square.
    
    Args:
        n (int): The integer to check.
        
    Returns:
        bool: True if n is a perfect square, False otherwise.
    """

    root = int(sqrt(n))
    return root * root == n

def fermatFactor(N: int) -> tuple[int, int]:
    """Perform Fermat's factorization method on n.

    Args:
        N (int): The integer to be factorized.

    Returns:
        tuple[int, int]: A tuple containing the two factors of N.
    """

    a = ceil(sqrt(N))
    b2 = a * a - N

    while not _isSquare(b2):
        a += 1
        b2 = a * a - N

    b = int(sqrt(b2))
    return a - b, a + b

def pollardRho(N):
    """Perform Pollard's Rho factorization method on n.

    Args:
        N (int): The integer to be factorized.
    Returns:
        tuple[int, int] | None: A tuple containing the two factors of N if found, otherwise None.
    """
    
    x = 2
    y = 2
    d = 1
    f = lambda x: (x * x + 1) % N

    while d == 1:
        x = f(x)
        y = f(f(y))
        d = gcd(abs(x - y), N)

    if d == N:
        return None
    return d, N // d