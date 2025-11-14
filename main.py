#-------------------------------------------#
#  This file is for demonstration purposes. #
#-------------------------------------------#

from cryptool.utils import gcd, bezout, inverse
from cryptool.prime import genPrime

if __name__ == "__main__":
    print(gcd(10,2))
    print(bezout(14, -21))
    print(inverse(3, 1<<1024))

    """Generate a random prime number with n bits."""
    p = genPrime(60)
    print(f"Generated prime p: {p}")