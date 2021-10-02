import struct

# clase vertice que se pueda sumar con el operador + 
class V3(object):
    def __init__(self, x, y, z = None):
        self.x = x
        self.y = y
        self.z = z

    def __getitem__(self, i):
        if i == 0:
            return self.x
        elif i == 1:
            return self.y
        elif i == 2:
            return self.z
    # metodo para imprimir algo 
    def __repr__(self):
        return "V3(%s, %s, %s)" %(self.x, self.y, self.z)
def clamp_color(v):
    return max(0, min(255, int(v)))

class color(object):
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
    # metodo para imprimir algo 
    def __repr__(self):
        b = clamp_color(self.b) # cual es el valor minimo entre 255 y self.b
        g = clamp_color(self.g)
        r = clamp_color(self.r)
        return "color(%s, %s, %s)" % (r, g, b)

    def toBytes(self):
        b = clamp_color(self.b) # cual es el valor minimo entre 255 y self.b
        g = clamp_color(self.g)
        r = clamp_color(self.r)

        return bytes([b, g, r])

    # suma de colores
    def __add__(self, other):
        r = clamp_color(self.r + other.r)
        g = clamp_color(self.g + other.g)
        b = clamp_color(self.b + other.b)
        return color(r, g, b)

    # multiplica de colores
    def __mul__(self, k):
        r = clamp_color(self.r * k)
        g = clamp_color(self.g * k)
        b = clamp_color(self.b * k)
        return color(r, g, b)


def char(c):
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    # short
    return struct.pack('=h', w)

def dword(w):
    # long
    return struct.pack('=l', w)


BLACK =  color(0, 0, 0)
WHITE =  color(255, 255, 255)


# este bounding box va a recibir los 3 parametros A,B,C
def bbox(A, B, C):
    xs = [A.x, B.x, C.x]
    xs.sort()
    ys = [A.y, B.y, C.y]
    ys.sort()
    # zs = [A.z, B.z, C.z]
    # zs.sort()
    # se utiliza -1 para regresar al ulitmo valor del array
    return V3(xs[0], ys[0]), V3(xs[-1], ys[-1])


def cross(v0, v1):
    # el producto cruz entre 3 vectores se calcula
    cx = v0.y * v1.z - v0.z * v1.y
    cy = v0.z * v1.x - v0.x * v1.z
    cz = v0.x * v1.y - v0.y * v1.x
    return V3(cx, cy, cz)

def barycentric(A, B, C, P):
    # calcular producto cruz entre dos vectores para calcular las 3 variables.
    bary = cross(
    V3(C.x - A.x, B.x - A.x, A.x - P.x), 
    V3(C.y - A.y, B.y - A.y, A.y - P.y)
  )

    if abs(bary[2]) < 1:
        return -1, -1, -1    # con esto se evita la division entre 0

    # para forzar a que uno sea 1 hay que dividirlos a todos entre cz
    w = 1 - (bary[0] + bary[1]) / bary[2]
    v = bary[1] / bary[2]
    u = bary[0] / bary[2]  # siempre que aparezca una división, hay una posibilidad que cz de 0. Esto significa que el triangulo es solo una linea

    # si ya tenemos herramienta, modulo que se va a priorizar sobretoido el valor de cleinte ubicar que clase o metodos hay que trabajar primero. se tiene que considerar refactorizarlo 
    # que framework de pruebas se van a utilizar.

    return w, v, u


def sub(v0, v1):
    return V3(
        v0.x - v1.x,
        v0.y - v1.y,
        v0.z - v1.z,
    )
def length(v0):
    return(v0.x**2 + v0.y**2 +v0.z**2) ** 0.5

def norm(v0):
    l = length(v0)
    if l ==0:
        return V3(0,0,0)

    return V3(
        v0.x / l,
        v0.y / l,
        v0.z / l
    )

def dot(v0, v1):
    return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z