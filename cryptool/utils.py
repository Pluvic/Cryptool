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

def primalityList(numList: list[int]) -> bool:
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