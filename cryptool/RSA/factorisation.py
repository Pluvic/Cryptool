# This file contains functions related to RSA encryption for the Cryptool project.

from math import sqrt, ceil
from cryptool.utils import gcd
from decimal import Decimal, getcontext


# Set precision for Decimal calculations
getcontext().prec = 1024

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

def pollardRho(N : int) -> tuple[int, int] | None:
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

def factorizNwithPhi(N: int, phi: int) -> tuple[int, int]:
    """Factor N given its totient phi(N).

    Args:
        N (int): The integer to be factorized.
        phi (int): The totient of N.

    Returns:
        tuple[int, int]: A tuple containing the two factors of N.
    """

    b = phi - N - 1
    delta = b * b - 4 * N

    sqrtDelta = Decimal(delta).sqrt()

    p = ( -b + sqrtDelta ) / 2
    q = ( -b - sqrtDelta ) / 2

    return int(p), int(q)

def factorizeNwithD(N: int, d: int, e: int) -> tuple[int, int] | None:
    """Factor N given the private exponent d and public exponent e.

    Args:
        N (int): The integer to be factorized.
        d (int): The private exponent.
        e (int): The public exponent.

    Returns:
        tuple[int, int] | None: A tuple containing the two factors of N if found, otherwise None.
    """

    k = d * e - 1

    if k % 2 == 1:
        return None

    r = 0
    s = k

    while s % 2 == 0:
        s //= 2
        r += 1

    for a in range(2, 100):
        x = pow(a, s, N)

        if x == 1 or x == N - 1:
            continue

        for _ in range(r):
            x_prev = x
            x = pow(x, 2, N)

            if x == 1:
                p = gcd(x_prev - 1, N)
                q = N // p
                return p, q

            if x == N - 1:
                break

    return None

def reducesRationals(A: int, B: int) -> tuple[list[int], list[int]]:
    """Compute the continued fraction expansion of A/B.

    Args:
        A (int): The numerator.
        B (int): The denominator.

    Returns:
        tuple[list[int], list[int]]: Two lists containing the numerators and denominators of the convergents.
    """

    ui = [1]
    vi = [0, 1]
    ai = [1]
    a1 = A // B
    ai.append(a1)
    ui.append(a1)
    A, B = B, A % B

    while B != 0:
        q = A // B
        ai.append(q)
        r = A % B
        A, B = B, r
        ui.append(ui[-1]*ai[-1] + ui[-2])
        vi.append(vi[-1]*ai[-1] + vi[-2])

    ui.pop(0)
    vi.pop(0)
    return ui, vi

def wienerAttack(N: int, e: int) -> tuple[int, int] | None:
    """Perform Wiener's attack to factor N given a small private exponent d.

    Args:
        N (int): The RSA modulus.
        e (int): The public exponent.

    Returns:
        tuple[int, int] | None: A tuple containing the two factors of N if found, otherwise None.
    """

    ki, di = reducesRationals(N, e)

    for i in range(len(ki)):
        if di[i] == 0:
            continue

        phiN = (e * ki[i] - 1) // di[i]
        
        if phiN > N:
            continue
        p, q = factorizNwithPhi(N, phiN)
        
        if p * q == N:
            return p, q

    return None