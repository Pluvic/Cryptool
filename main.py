#-------------------------------------------#
#  This file is for demonstration purposes. #
#-------------------------------------------#

from cryptool.utils import gcd, bezout, inverse
from cryptool.prime import genPrime, isPrime
from cryptool.RSA.factorisation import factorizNwithPhi, factorizeNwithD
from cryptool.RSA.attack import commonModulus, commonExponent
from cryptool.group import ZpMult
from Cryptodome.Util.number import long_to_bytes, bytes_to_long


if __name__ == "__main__":
    print(gcd(10,2))
    print(bezout(14, -21))
    print(inverse(3, 1<<1024))

    """Generate a random prime number with n bits."""
    p = genPrime(100)
    q = genPrime(100)
    print(f"Generated prime p: {p}")
    print(f"Generated prime q: {q}")

    print(f"Is p prime? {isPrime(p)}")
    print(f"Is q prime? {isPrime(q)}")

    N = p * q
    phi = (p - 1) * (q - 1)
    e1 = 31
    e2 = 17

    message = b"Hello, Cryptool!"
    m = bytes_to_long(message)
    c1 = pow(m, e1, N)
    c2 = pow(m, e2, N)

    decrypted_m1 = commonModulus(N, e1, e2, c1, c2)
    decrypted_message1 = long_to_bytes(decrypted_m1)
    print(f"Decrypted message using common modulus attack: {decrypted_message1}") 

    # Test group operations
    group = ZpMult(809)

    g = 3
    h = 525

    print(f"Calculating discrete logarithm of {h} base {g} in ZpMult(809):")
    x = group.calculDL(g, h)
    print(f"Discrete logarithm result: x = {x}")
