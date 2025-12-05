# This file is about finite multiplicative groups with rijndael structure for the Cryptool project.

from cryptool.group import Group
from cryptool.utils import int2poly

class F2nMul(Group):
    """Group of multiplication over F_2^n."""
    def __init__(self, p: int):
        """Initialize the group with irreducible polynomial p.
        
        Args:
            p (int): An irreducible polynomial defining the field F_2^n.
        """
        self.p = p
        self.n = p.bit_length() - 1
        self.N = 2**self.n - 1
        self.e = 1 

    def loi(self, x: int, y: int) -> int:
        """Define the multiplication operation in F_2^n.
        
        Args:
            x (int): First element.
            y (int): Second element.
        Returns:
            int: The product of x and y in F_2^n.
        """
        z = 0
        while y != 0:
            if (y & 1) > 0:
                z ^= x
            x <<= 1
            if x.bit_length() > self.n:
                x ^= self.p
            y >>= 1
        return z
    
def rotateLeft(byte: int, n: int) -> int:
    """Rotate bits of a byte to the left by n positions.
    
    Args:
        byte (int): The byte to be rotated.
        n (int): Number of positions to rotate.
    Returns:
        int: The rotated byte.
    """
    n = n % 8
    return ((byte << n) & 0xFF) | (byte >> (8 - n))

def rotateRight(byte: int, n: int) -> int:
    """Rotate bits of a byte to the right by n positions.
    
    Args:
        byte (int): The byte to be rotated.
        n (int): Number of positions to rotate.
    Returns:
        int: The rotated byte.
    """
    n = n % 8
    return (byte >> n) | ((byte << (8 - n)) & 0xFF)

def sbox():
    """Generate the AES S-box using the F_2^8 multiplicative group.

    Returns:
        list[int]: The AES S-box as a list of 256 integers.
    """
    P = 0x11B  # Irreducible polynomial for AES (x^8 + x^4 + x^3 + x + 1)
    group = F2nMul(P)

    sbox = [0] * 256
    for i in range(256):
        if i == 0:
            inv = 0
        else:
            inv = group.exp(i, -1)
        
        transformed = inv
        transformed ^= rotateLeft(inv, 1)
        transformed ^= rotateLeft(inv, 2)
        transformed ^= rotateLeft(inv, 3)
        transformed ^= rotateLeft(inv, 4)
        transformed ^= 0x63  

        sbox[i] = transformed & 0xFF

    return sbox