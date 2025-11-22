#-------------------------------------------#
#  This file is for demonstration purposes. #
#-------------------------------------------#

from cryptool.utils import gcd, bezout, inverse
from cryptool.prime import genPrime
from cryptool.RSA.factorisation import pollardRho

if __name__ == "__main__":
    print(gcd(10,2))
    print(bezout(14, -21))
    print(inverse(3, 1<<1024))

    """Generate a random prime number with n bits."""
    p = genPrime(60)
    q = genPrime(60)
    print(f"Generated prime p: {p}")
    print(f"Generated prime q: {q}")

    N = p * q

    factors = pollardRho(N)
    if factors:
        print(f"Factors of N: {factors[0]} and {factors[1]}")
    else:
        print("Failed to factor N.")
