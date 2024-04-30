import math

class Ponto:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Ponto(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Ponto(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        return Ponto(self.x * scalar, self.y * scalar, self.z * scalar)

    def distancia_ate(self, outro):
        return math.sqrt((self.x - outro.x) ** 2 + (self.y - outro.y) ** 2 + (self.z - outro.z) ** 2)

    def imprime(self, msg=""):
        print(msg, f"({self.x}, {self.y}, {self.z})")

    def rotacionaZ(self, angulo, centro=None):
        if centro is None:
            centro = Ponto()
        anguloRad = math.radians(angulo)
        x_temp = self.x - centro.x
        y_temp = self.y - centro.y
        xr = x_temp * math.cos(anguloRad) - y_temp * math.sin(anguloRad)
        yr = x_temp * math.sin(anguloRad) + y_temp * math.cos(anguloRad)
        self.x = xr + centro.x
        self.y = yr + centro.y

    def rotacionaY(self, angulo):
        anguloRad = math.radians(angulo)
        xr = self.x * math.cos(anguloRad) + self.z * math.sin(anguloRad)
        zr = -self.x * math.sin(anguloRad) + self.z * math.cos(anguloRad)
        self.x = xr
        self.z = zr

    def rotacionaX(self, angulo):
        anguloRad = math.radians(angulo)
        yr = self.y * math.cos(anguloRad) - self.z * math.sin(anguloRad)
        zr = self.y * math.sin(anguloRad) + self.z * math.cos(anguloRad)
        self.y = yr
        self.z = zr

def intersec2d(k, l, m, n):
    det = (n.x - m.x) * (l.y - k.y) - (n.y - m.y) * (l.x - k.x)
    if abs(det) < 1e-10:
        return 0, None, None  # Linhas paralelas ou coincidentes
    s = ((n.x - m.x) * (m.y - k.y) - (n.y - m.y) * (m.x - k.x)) / det
    t = ((l.x - k.x) * (m.y - k.y) - (l.y - k.y) * (m.x - k.x)) / det
    return 1, s, t

def HaInterseccao(k, l, m, n):
    ret, s, t = intersec2d(k, l, m, n)
    if not ret:
        return False
    return 0 <= s <= 1 and 0 <= t <= 1
