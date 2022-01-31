import numpy as np
import math
import sympy as sp

class Triangle:
    def __init__(self, A, B, C):
        self.A, self.B, self.C = A, B, C
        self.AB = self.side_length(A, B)
        self.AC = self.side_length(A, C)
        self.BC = self.side_length(B, C)
        self.area = self.area()
        self.ha = self.height(self.BC)
        self.hb = self.height(self.AC)
        self.hc = self.height(self.AB)
        self.alpha = self.angle(self.BC, self.AC, self.AB)
        self.beta = self.angle(self.AC, self.BC, self.AB)
        self.gamma = self.angle(self.AB, self.BC, self.AC)
    
    def side_length(self, p1, p2):
        return sp.simplify(sp.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 + (p2[2] - p1[2])**2))
    
    def area(self):
        p = (self.AB + self.AC + self.BC)/2
        return sp.simplify(sp.sqrt(p*(p-self.AB)*(p-self.AC)*(p-self.BC)))
    
    def height(self, a):
        return (2*self.area)/a
    
    def angle(self, a, b, c):
        return np.degrees(math.acos((b**2 + c**2 - a**2)/(2*b*c)))


class Tetrahedron:
    def __init__(self, A, B, C, D):
        self.A, self.B, self.C, self.D = A, B, C, D
        self.fABC = Triangle(A, B, C)
        self.fABD = Triangle(A, B, D)
        self.fACD = Triangle(A, C, D)
        self.fBCD = Triangle(B, C, D)
        self.surface_area = self.surface_area()
        self.volume = self.volume()
        self.ha = self.height(self.volume, self.fBCD)
        self.hb = self.height(self.volume, self.fACD)
        self.hc = self.height(self.volume, self.fABD)
        self.hd = self.height(self.volume, self.fABC)
    
    def surface_area(self):
        return self.fABC.area + self.fABD.area + self.fACD.area + self.fBCD.area
    
    def volume(self):
        vAB = sp.Matrix(self.B - self.A)
        vAC = sp.Matrix(self.C - self.A)
        vAD = sp.Matrix(self.D - self.A)
        
        return sp.simplify(abs(((vAB.cross(vAC)).dot(vAD)) * 1/6))
    
    def height(self, V, face):
        return (3*V)/face.area
    

def is_colinear(A, B, C):
    AB = B - A
    AC = C - A
    
    if np.array_equal(np.cross(AB, AC), np.array([0, 0, 0])):
        return True
    else:
        return False

def is_coplanar(A, B, C, D):
    AB = B - A
    AC = C - A
    AD = D - A
    
    if np.dot(AD, np.cross(AB, AC)) == 0:
        return True
    else:
        return False