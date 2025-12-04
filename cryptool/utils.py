# This file contains utility functions for the Cryptool project.

def gcd(a: int, b: int) -> int:
    """Calculate the greatest common divisor of a and b using the Euclidean algorithm. 

    Args:
        a (int): First integer.
        b (int): Second integer.

    Returns:
        int: The greatest common divisor of a and b.
    """

    while b:
        a, b = b, a % b
    return a

def bezout(a: int, b: int) -> tuple[int, int, int]:
    """Extended Euclidean algorithm to find integers u and v such that au + bv = gcd(a, b).
    
    Args:
        a (int): First integer.
        b (int): Second integer.
        
    Returns:
        tuple[int, int, int]: A tuple containing gcd(a, b), u, and v.
    """

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

def inverse(x: int, n: int) -> int:
    """Calculate the modular inverse of x modulo n.

    Args:
        x (int): The integer to find the inverse of.
        n (int): The modulus.

    Returns:
        int: The modular inverse of x modulo n if it exists, otherwise raises an error.
    """

    thisGcd = gcd(x, n)

    if thisGcd != 1:
        print(f"Error: The number {x} do not have an inverse modulo {n}.")

    _, be1, _ = bezout(x, n)
    return be1 % n

def _primalityList(numList: list[int]) -> bool:
    """Check if all numbers in the list are pairwise coprime.
    
    Args:
        numList (list[int]): A list of integers to check for pairwise coprimality.

    Returns:
        bool: True if all numbers are pairwise coprime, False otherwise.
    """

    for i in range(len(numList)):
        for j in range(i+1,len(numList)):
            if gcd(numList[i], numList[j]) != 1:
                return False
            
    return True

def chineseRemainder(listRemainders: list[int], listModulos: list[int]) -> int:
    """Solve the system of congruences using the Chinese Remainder Theorem.
    
    Args:
        listRemainders (list[int]): A list of remainders.
        listModulos (list[int]): A list of moduli.
        
    Returns:
        int: The solution to the system of congruences.
    """

    if len(listRemainders) != len(listModulos):
        print("The 2 lists need to have the same size.")
        return
    
    if not _primalityList(listModulos):
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

def isQuadraticResidue(a: int, p: int) -> bool:
    """Check if a is a quadratic residue modulo p using Euler's criterion.
    
    Args:
        a (int): The integer to check.
        p (int): The prime modulus.

    Returns:
        bool: True if a is a quadratic residue modulo p, False otherwise.
    """

    return pow(a, (p - 1) // 2, p) == 1

def legendreSymbol(a: int, p: int) -> int:
    """Compute the Legendre symbol (a/p).
    
    Args:
        a (int): The integer to compute the Legendre symbol for.
        p (int): The prime modulus.

    Returns:
        int: 1 if a is a quadratic residue modulo p, -1 if not, and 0 if a is divisible by p.
    """

    ls = pow(a, (p - 1) // 2, p)
    if ls == p - 1:
        return -1
    return ls

def squareRootModP(a: int, p: int) -> int:
    """Compute a square root of a modulo p using the Tonelli-Shanks algorithm.
    
    Args:
        a (int): The integer to compute the square root for.
        p (int): The prime modulus.

    Returns:
        int: A square root of a modulo p if it exists, otherwise raises an error.
    """

    if not isQuadraticResidue(a, p):
        print(f"Error: {a} is not a quadratic residue modulo {p}.")
        return

    if p % 4 == 3:
        r = pow(a, (p + 1) // 4, p)
        return r
    
    if p % 4 == 1:
        return TonelliShanks(a, p)
    
def TonelliShanks(x: int, p: int) -> int:
    """Tonelli-Shanks algorithm to find a square root of x modulo p.
    
    Args:
        x (int): The integer to compute the square root for.
        p (int): The prime modulus.

    Returns:
        int: A square root of x modulo p.
    """

    # Step 1: Write p - 1 as 2^k * q with q odd
    k = 0
    phiP = p - 1
    while phiP % 2 == 0:
        phiP //= 2
        k += 1
    q = phiP

    # Step 2: Find a quadratic non-residue z
    z = 2
    while isQuadraticResidue(z, p):
        z += 1

    # Step 3: Initializations
    c = pow(z, q, p)
    t = pow(x, q, p)
    r = pow(x, (q + 1) // 2, p)

    # Step 4: Main loop
    while t != 0 and t != 1:
        i = 0
        for i in range(1, k):
            if pow(t, 2**i, p) == 1:
                break

        b = pow(c, 2**(k - i - 1), p)
        k = i
        c = (b * b) % p
        t = (t * c) % p
        r = (r * b) % p

    if t == 0:
        return 0
    return r

def quadraticEquationModP(A: int, B: int, C: int, p: int) -> tuple[int, int] | None:
    """Solve the quadratic equation Ax^2 + Bx + C ≡ 0 (mod p).
    
    Args:
        A (int): Coefficient of x^2.
        B (int): Coefficient of x.
        C (int): Constant term.
        p (int): The prime modulus.
    Returns:
        tuple[int, int] | None: A tuple containing the two solutions if they exist, otherwise None.
    """
    
    if A % p == 0:
        raise ValueError("A must be non-zero modulo p")

    x = (B * B - 4 * A * C) % p

    if not isQuadraticResidue(x, p):
        return None

    sqrt_x = squareRootModP(x, p)
    inv_2A = inverse(2 * A, p)

    root1 = (-B + sqrt_x) * inv_2A % p
    root2 = (-B - sqrt_x) * inv_2A % p

    return root1, root2

def integerCubeRoot(n: int) -> int:
    """Compute the integer cube root of n using binary search.
    
    Args:
        n (int): The integer to compute the cube root for.
        
    Returns:
        int: The integer cube root of n.
    """

    low = 0
    high = n

    while low < high:
        mid = (low + high) // 2
        mid_cubed = mid * mid * mid

        if mid_cubed < n:
            low = mid + 1
        else:
            high = mid

    return low if low * low * low == n else low - 1
        