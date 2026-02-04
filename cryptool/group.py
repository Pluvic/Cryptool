# This file contains functions related to group theory for the Cryptool project.

from abc import ABC, abstractmethod
from random import randint
from math import log, ceil, sqrt
from sympy.ntheory import factorint
from cryptool.utils import chineseRemainder

class Group(ABC):
    """Abstract base class for mathematical groups.
    
     Args:
        p (int): A parameter defining the group.
        N (int, optional): The order of the group. Defaults to None.
        e (any, optional): The identity element of the group. Defaults to None.
    """
    def __init__(self, p: int, N:int = None, e = None):
        """Initialize the group with parameter p."""
        self.p = p
        self.N = N
        self.e = e
    
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

class ECConZp(Group):
    """Elliptic Curve over Zp.
        Args:
            A (int): Coefficient A of the elliptic curve.
            B (int): Coefficient B of the elliptic curve.
            p (int): A prime number defining the field Zp.
            N (int): Order of the elliptic curve.
            e (list): Identity element of the elliptic curve.
            G (list): Base point G on the elliptic curve.
    """
    def __init__(self, A: int, B: int, G: list, p: int, N: int, e: list):
        super().__init__(p, N, e)
        self.A = A
        self.B = B
        self.G = G

    def exp(self, P: list, k: int) -> list:
        """Perform fast exponentiation on the elliptic curve."""
        if k == -1:
            return self.exp(P, (self.N)-1)

        if k == 0:
            return self.e
        
        R = self.e
        t = int(log(k, 2)) + 1
        for i in range(t, -1, -1):
            R = self.loi(R, R)
            if ((k >> i) & 1) == 1:
                R = self.loi(R, P)
        return R

    def loi(self, P: list, Q: list) -> list:
        """Define the group operation (point addition) on the elliptic curve."""
        if P == self.e:
            return Q
        elif Q == self.e:
            return P
        
        if P[0] == Q[0]:

            if P[1] == (-Q[1] % self.p):
                return self.e
            else: # 2 * P
                x, y = P[0], P[1]
                Lambda = ((3 * x**2 + self.A) * pow(2*y, -1, self.p)) % self.p
                x3 = (Lambda**2 - 2*x) % self.p
                y3 = (Lambda*(x - x3) - y) % self.p
        
        else:
            x1, y1, x2, y2 = P[0], P[1], Q[0], Q[1]
            Lambda = ((y2 - y1) * pow((x2 - x1), -1, self.p)) % self.p
            x3 = (Lambda**2 - x1 - x2) % self.p
            y3 = (Lambda*(x1 - x3) - y1) % self.p
        
        return [x3, y3]

    def verify(self, P: list):
        """Verify if a point P lies on the elliptic curve."""
        if P == self.e:
            return True
        
        leftSideEquation = pow(P[1], 2, self.p)
        rightSideEquation = (pow(P[0], 3, self.p) + self.A * P[0] + self.B) % self.p

        if leftSideEquation == rightSideEquation:
            return True
        
        return False
    
    def ECDSA_sign(self, m:int, d:int):
        """ECDSA signing method
        Args:
            m: hashed message to be signed (int)
            d: private key (int)
        """
        k = randint(1, self.N - 1)
        K = self.exp(self.G, k)
        t = K[0] % self.N

        s = ((m + d*t) * pow(k, -1, self.N)) % self.N

        return (t, s)
        

    def ECDSA_verif(self, Q:int, m:int, sign: tuple):
        """ECDSA verification method
        Args:
            Q: public key (list[2])
            m: message (int)
            sign: signature (tuple)
        """
        t, s = sign[0], sign[1]
        if ( not(t > 0 and t <= (self.N -1)) or not(s > 0 and s <= (self.N -1))):
            print("Var t or s not in the scope.")
            return False
        
        R1 = self.exp(self.G, m * pow(s, -1, self.N))
        R2 = self.exp(Q, t * pow(s, -1, self.N))

        R = self.loi(R1, R2)

        if R[0] % self.N == t:
            return True
        
        return False