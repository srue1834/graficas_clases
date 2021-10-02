import struct
from collections import namedtuple # es para nombrar cada elemento de un array 
from obj import Obj, Texture

# esto lo hace mas legible
V2 = namedtuple('Point2D', ['x', 'y'])
V3 = namedtuple('Point3D', ['x', 'y', 'z'])


def char(c):
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    # short
    return struct.pack('=h', w)

def dword(w):
    # long
    return struct.pack('=l', w)



def color(r, g, b):
    return bytes([b, g, r])


BLACK =  color(0, 0, 0)
WHITE =  color(255, 255, 255)


# este bounding box va a recibir los 3 parametros A,B,C
def bbox(A, B, C):
    xs = [A.x, B.x, C.x]
    xs.sort()
    ys = [A.y, B.y, C.y]
    ys.sort()
    # se utiliza -1 para regresar al ulitmo valor del array
    return xs[0], xs[-1], ys[0], ys[-1]

def cross(v0, v1):
    # el producto cruz entre 3 vectores se calcula
    cx = v0.y * v1.z - v0.z * v1.y
    cy = v0.z * v1.x - v0.x * v1.z
    cz = v0.x * v1.y - v0.y * v1.x
    return V3(cx, cy, cz)

def barycentric(A, B, C, P):
    # calcular producto cruz entre dos vectores para calcular las 3 variables.
    cx, cy, cz = cross(
        V3(B.x - A.x, C.x - A.x, A.x - P.x),
        V3(B.y - A.y, C.y - A.y, A.y - P.y)
    )
    if cz == 0:
        return -1, -1, -1  # con esto se evita la division entre 0

    # para forzar a que uno sea 1 hay que dividirlos a todos entre cz
    u = cx/cz      # siempre que aparezca una división, hay una posibilidad que cz de 0. Esto significa que el triangulo es solo una linea
    v = cy/cz
    w = 1 - (cx + cy) / cz

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

class Renderer(object):
    def glinit():
        r =  Renderer(1024, 768)

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.light =  norm(V3(0,0,1))

        # Esta variable le da color al punto
        self.current_color = WHITE

        self.clear()

    def clear(self):
        self.framebuffer = [
            [BLACK for x in range(self.width)]
            for y in range(self.height)
        ]

        # hay que hacer un calculo en todos los pixeles, para ver cual corresponde en su coordenada en z


        self.zbuffer = [
            [-99999 for x in range(self.width)]
            for y in range(self.height)
        ]
        
    def write(self, filename):
        f = open(filename, 'bw')

        # File header (14)
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + 3*(self.width*self.height)))
        f.write(dword(0))
        f.write(dword(14 + 40))

        # Info header (40)
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(3*(self.width*self.height)))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        # Bitmap (se recorre el framebuffer completo, para meter los bytes en un array de 4)
        for y in range(self.height):
            for x in range(self.width):
                try:
                    f.write(self.framebuffer[y][x])
                except:
                    pass
        f.close()

 # --------------- LINE ---------------

    #  ALGORITMO DE DIXTRA, VER BRESENHAM ALGORITHM 
    
    def line(self, A, B, color=None):
        x0 = A.x
        x1 = B.x
        y0 = A.y
        y1 = B.y


        dy = abs(y1 - y0)
        dx = abs(x1 - x0)
        # en el caso que no funcione la linea, steep hace que se cambien los valores de y a x. Le da la vuelta
        steep = dy > dx
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

            # esto es para voltearlo
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        # ahora se reemplatea la pendiente.
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)
    
        offset = 0 # offset = 0 * 2 * dx
        
        threshold = dx # threshold = 0.5 * 2 * dx
        

        y = y0
        points = []
        for x in range(int(x0), int(x1) + 1):
            #se agrega esto para que este en la direccion correcta
            if steep:
                points.append((y, x, color))
            else:
                points.append((x, y, color))


            offset += 2 * dy # offset += (dy/dx) * 2 * dx
            
            if offset >= threshold:
                y += 1 if y0 < y1 else -1
                threshold += 2 * dx # threshold += 1 * 2 * dx

        for point in points:
            r.point(*point)

    # --------------- LINE ---------------
 

    def render(self):
        self.write('a.bmp')

        # Se agregara un punto 
    def point(self, x, y, color = None):
        try:

            self.framebuffer[y][x] = color or self.current_color
        except:
            pass

        # esta es una funcion que reciba un vertice como parametro que se transforma en X y Y
    def transform(self, v, translate=(0, 0, 0), scale=(1, 1, 1)):
       
        return V3(
            round((v[0] + translate[0]) * scale[0]),
            round((v[1] + translate[1]) * scale[1]),
            round((v[2] + translate[2]) * scale[2])
        )

    

    # Esta funcion es para cargar y renderizar obj
    def load(self, filename, translate=(0, 0, 0), scale=(1, 1, 1)): # ahora a load se le pasa que tanto se quiere que se mueva para los lados y abajo
        model = Obj(filename)
        # se tienen que recorrer las caras, agarrar cada uno de los indices y pintar cada vertice
        
        for face in model.faces:
            # para saber si hace triangulos o cuadrados
            vcount =  len(face)

            if vcount == 3:
                # se agarra el array 0 en la posicion 0
                f1 = face[0][0] -1
                f2 = face[1][0] -1
                f3 = face[2][0] -1  

                A = self.transform(model.vertex[f1], translate, scale)
                B = self.transform(model.vertex[f2], translate, scale)
                C = self.transform(model.vertex[f3], translate, scale)

                # normalizar un vector u=v/|v|
                normal = norm(cross(
                    sub(B, A),
                    sub(C, A)
                ))

                intensity = dot(normal, self.light)
                # en este caso tendra un 1 si esta en frente
                # tendra 0 si esta de lado 

                grey = round(250 * intensity)

                if grey < 0:
                    continue   # si la intensidad es menor a 0, el loop termina y procede a la siguiente
                # esto es para que tenga colorcito
                # self.triangle(A, B, C, color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

                self.triangle(A, B, C, color(grey, grey, grey))


            elif vcount == 4:
                # se agarra el array 0 en la posicion 0
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1
                f4 = face[3][0] - 1

                A = self.transform(model.vertex[f1], translate, scale)
                B = self.transform(model.vertex[f2], translate, scale)
                C = self.transform(model.vertex[f3], translate, scale)
                D = self.transform(model.vertex[f4], translate, scale)
                normal = norm(cross(
                    sub(B, A),
                    sub(C, A)
                ))

                intensity = dot(normal, self.light)
                
                grey = round(250 * intensity)
                if grey < 0:
                    continue
                self.triangle(A, B, C, color(grey, grey, grey))
                self.triangle(A, C, D, color(grey, grey, grey))
           

    # este es un triangle wirefram
    def triangle_wireframe(self, A, B, C):
        self.line(A, B)
        self.line(B, C)
        self.line(C, A)

    # funcion que recibe 3 vertices y dibuja un triangulo
    def triangle(self, A, B, C, color= None):
        xmin, xmax, ymin, ymax = bbox(A, B, C)

        # encontrar el rectangulo mas pequeño
        # se va marcando un punto
        for x in range(xmin, xmax + 1):
            for y in range(ymin, ymax + 1):
                # se toman las 3 coordenadas de triangulo y el punto P que es (x, y)
                P = V2(x,y)
                w, v, u = barycentric(A, B, C, P)
                # si alguna de las 3 es negativa quiere decir que esta afuera del triangulo
                if w  < 0 or v < 0 or u < 0:
                    continue # todo lo que este despues de continue no se va a ejecutar
                z = A.z * w + B.z * v + C.z * u

                try:
                    if z > self.zbuffer[x][y]:
                        self.point(x, y, color)
                        self.zbuffer[x][y] = z
                except:
                        pass

           
# r.load('./models/cube2.obj', (4, 3, 3), (100, 100, 100))
# r.load('./models/model.obj', (1, 1, 1), (300, 300, 300))
# r.render()


r = Renderer(1024, 1024)
t = Texture('./textures/model.bmp')
r.framebuffer = t.pixels

model = Obj('./models/model.obj')

# se hace una pequeña escala
def transform(tvertx):
    return V3(
        round(tvertx[0] * 1024), # este es un valor que va a 0 a 4096 para renderizar 
        round(tvertx[1] * 1024), 
        0
    )

# ahora se van a recorrer las caras del modelo
for face in model.faces:
    vcount = len(face)
    # si es un triangulo 
    if vcount == 3:
        # se cambia a 1 porque se quiere sacar el segundo valor de F
        f1 = face[0][1] - 1
        f2 = face[1][1] - 1
        f3 = face[2][1] - 1
        # asi se sacan los vertices de textura
        
        vtA = transform(model.tvertex[f1])
        vtB = transform(model.tvertex[f2])
        vtC = transform(model.tvertex[f3])  # se convierten todos los vertices conforme se vayan leyendo  

        # se dibuja el triangulo 
        # r.triangle(vtA, vtB, vtC, color(255, 255, 255))
        r.line(vtA, vtB)
        r.line(vtB, vtC)
        r.line(vtC, vtA)

        
   
    # si es un triangulo 
    elif vcount == 4:
        # se agrega la cuarta cara
        f1 = face[0][1] - 1
        f2 = face[1][1] - 1
        f3 = face[2][1] - 1
        f4 = face[3][1] - 1

        vtA = transform(model.tvertex[f1])
        vtB = transform(model.tvertex[f2])
        vtC = transform(model.tvertex[f3])
        vtD = transform(model.tvertex[f4])

        r.line(vtA, vtB)
        r.line(vtB, vtC)
        r.line(vtC, vtA) 
        
        r.line(vtA, vtC)
        r.line(vtC, vtD)  
        r.line(vtD, vtA) 


# r = Renderer(4096, 2048)
# model = Obj('./models/earth.obj')
# print(model.tvertex[0])



# print(model.tvertex[0], model.tvertex[1], model.tvertex[2]) # hay que armar un triangulo entre los valores X y Y de tvertex[0][1][2] 
# hay que recordar que hay algunos obj que no incluyen el Z, es decir, dan 0.0 entonces hay que modificar el codigo para que pueda sorportar los 3 valores
# r = Renderer(800, 600)
# r.load('./models/earth.obj', (800, 600, 0), (0.5, 0.5, 1))
r.write('a.bmp')


