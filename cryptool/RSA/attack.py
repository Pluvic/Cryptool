# This file contains functions related to RSA encryption for the Cryptool project.

from cryptool.utils import inverse, integerCubeRoot


def commonModulus(N: int, e1: int, e2: int, c1: int, c2: int) -> int:
    """Perform common modulus attack on RSA encrypted messages.
    
    Args:
        N (int): The RSA modulus.
        e1 (int): The first public exponent.
        e2 (int): The second public exponent.
        c1 (int): The first ciphertext.
        c2 (int): The second ciphertext.
        
    Returns:
        int: The decrypted message.
    """

    u = inverse(e1, e2)
    v = (1 - u * e1) // e2

    c1u = pow(c1, u, N)
    c2v = pow(c2, v, N)

    m = (c1u * c2v) % N
    return m

def commonExponent(N1: int, N2: int, N3: int, c1: int, c2: int, c3: int) -> int:
    """Perform common exponent attack on RSA encrypted messages.
    
    Args:
        N1 (int): The first RSA modulus.
        N2 (int): The second RSA modulus.
        N3 (int): The third RSA modulus.
        c1 (int): The first ciphertext.
        c2 (int): The second ciphertext.
        c3 (int): The third ciphertext.
        
    Returns:
        int: The decrypted message.
    """

    m1 = N2 * N3
    m2 = N1 * N3
    m3 = N1 * N2

    u1, u2, u3 = inverse(m1, N1), inverse(m2, N2), inverse(m3, N3)

    M = c1 * m1 * u1 + c2 * m2 * u2 + c3 * m3 * u3
    M = M % (N1 * N2 * N3)

    m = integerCubeRoot(M)
    return m