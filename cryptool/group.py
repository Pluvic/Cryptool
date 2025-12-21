# This file contains functions related to group theory for the Cryptool project.

from abc import ABC, abstractmethod
from math import log, ceil, sqrt
from sympy.ntheory import factorint
from cryptool.utils import chineseRemainder

class Group(ABC):
    """Abstract base class for mathematical groups.
    
     Args:
        p (int): A parameter defining the group.
    """
    def __init__(self, p: int):
        """Initialize the group with parameter p."""
        self.p = p
    
    @abstractmethod
    def loi(self, g1: int, g2: int) -> int:
        """Abstract method for the group operation."""
        pass

    def exp(self, g: int, k: int) -> int:
        """Perform fast exponentiation in the group."""
        if k == -1:
            return self.exp(g, (self.N)-1)

        if k == 0:
            return self.e
        
        h = self.e
        t = int(log(k, 2)) + 1
        for i in range(t, -1, -1):
            h = self.loi(h, h)
            if ((k >> i) & 1) == 1:
                h = self.loi(h, g)
        return h
    
    def DLnaive(self, g: int, h: int) -> int:
        """Naive discrete logarithm function."""
        x, k = self.e, 0
        while(x != h):
            x = self.loi(x, g) % self.p
            k += 1
        return k
    
    def babyStepGiantStep(self, g: int, h: int) -> int:
        """Baby-step giant-step algorithm for discrete logarithm."""
        w = ceil(sqrt(self.N))
        tabI = []
        for i in range(w+1):
            tabI.append(self.exp(g, i*w))
        
        j = 0
        while (self.loi(h, self.exp(g, self.N - j)) not in tabI):
            j += 1
        
        x = self.loi(h, self.exp(g, self.N - j))
        i = tabI.index(x)

        return w*i + j
    
    def calculDL(self, g: int, h: int, t: int = 1000) -> int:
        """Calculate the discrete logarithm using an appropriate method."""
        if self.N < t:
            return self.DLnaive(g, h)
        else: 
            return self.babyStepGiantStep(g, h)

class ZpAdd(Group):
    """Group of integers modulo p under addition."""
    def __init__(self, p: int):
        Group.__init__(self, p)
        self.e = 0
        self.N = p

    def loi(self, g1: int, g2: int) -> int:
        return (g1 + g2) % self.p
    
    def inv(self, g: int) -> int:
        return (-g) % self.p

class ZpMult(Group):
    """Group of integers modulo p under multiplication."""
    def __init__(self, p: int):
        Group.__init__(self, p)
        self.e = 1
        self.N = p - 1

    def loi(self, g1: int, g2: int) -> int:
        return (g1 * g2) % self.p
    
    def inv(self, g: int) -> int:
        return pow(g, -1, self.p)
    
class ZpMulWithOrder(ZpMult):
    """Group of integers modulo p under multiplication with specified order."""
    def __init__(self, p: int, N: int):
        super().__init__(p)
        self.N = N

    def ShanksAlgorithm(self, g: int, h: int) -> int:
        """Shanks' algorithm for discrete logarithm."""
        m = ceil(sqrt(self.N))
        table = {}

        for j in range(m):
            value = self.exp(g, j)
            table[value] = j

        g_inv_m = self.exp(g, self.N - m)

        current = h
        for i in range(m):
            if current in table:
                return i * m + table[current]
            current = self.loi(current, g_inv_m)
        
        return None
    
    def DLinGroupofPrimePowerOrder(self, g: int, h: int, q: int, n: int) -> int:
        """Discrete logarithm in a group of prime power order."""
        i = 0
        y = pow(g, pow(q, n-1, self.N), self.p)
        
        for j in range(n):
            e_j = pow(q, n - j - 1, self.N)
            h_j = pow(h * self.inv(pow(g, i, self.p)), e_j, self.p)
            
            subgroup = ZpMulWithOrder(self.p, q)
            d_j = subgroup.ShanksAlgorithm(y, h_j)

            i += d_j * pow(q, j, self.N)
        return i
    
    def pohligHellman(self, g: int, h: int) -> int:
        """Pohlig-Hellman algorithm for discrete logarithm."""
        factors = factorint(self.N)
        ijs = []

        for p, e in factors.items():
            print(f"Processing prime factor {p}^{e}")
            g_j = pow(g, (self.N // pow(p, e)), self.p)
            h_j = pow(h, (self.N // pow(p, e)), self.p)

            group = ZpMulWithOrder(self.p, pow(p, e))
            i_j = group.DLinGroupofPrimePowerOrder(g_j, h_j, p, e)
            ijs.append(i_j)

        modulos = [pow(p, e) for p, e in factors.items()]
        x = chineseRemainder(ijs, modulos)
        return x % self.N
        