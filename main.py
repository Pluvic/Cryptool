#-------------------------------------------#
#  This file is for demonstration purposes. #
#-------------------------------------------#

from cryptool.utils import gcd, bezout, inverse
from cryptool.prime import genPrime
from cryptool.RSA.factorisation import pollardRho
from cryptool.group import ZpMult

if __name__ == "__main__":
    print(gcd(10,2))
    print(bezout(14, -21))
    print(inverse(3, 1<<1024))

    """Generate a random prime number with n bits."""
    p = genPrime(60)
    q = genPrime(60)
    print(f"Generated prime p: {p}")
    print(f"Generated prime q: {q}")

    # Test group operations
    group = ZpMult(809)

    g = 3
    h = 525

    print(f"Calculating discrete logarithm of {h} base {g} in ZpMult(809):")
    x = group.calculDL(g, h)
    print(f"Discrete logarithm result: x = {x}")
