import struct
from collections import namedtuple # es para nombrar cada elemento de un array 
from obj import Obj
import random

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
    return cx, cy, cz

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
    w = 1 - (u + v)

    # si ya tenemos herramienta, modulo que se va a priorizar sobretoido el valor de cleinte ubicar que clase o metodos hay que trabajar primero. se tiene que considerar refactorizarlo 
    # que framework de pruebas se van a utilizar.

    return w, v, u

class Renderer(object):
    def glinit():
        r =  Renderer(1024, 768)

    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Esta variable le da color al punto
        self.current_color = WHITE

        self.clear()

    def clear(self):
        self.framebuffer = [
            [BLACK for x in range(self.width)]
            for y in range(self.height)
        ]









        # hay que hacer un calculo en todos los pixeles, para ver cual corresponde en su coordenada en z

        # self.zbuffer = [
        #     [-9999 for x in range(self.width)]    # aqui se inicializo un array que ocupa toda la pantalla con numero negativos 
        #     for y in range(self.height)
        # ]









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
                f.write(self.framebuffer[y][x])

        f.close()
        
    # --------------- LINE ---------------

    # ALGORITMO DE DIXTRA, VER BRESENHAM ALGORITHM 
    def line(self, A, B, color= None):
        x0, y0 = A.x, A.y
        x1, y1 = B.x, B.y


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
        for x in range(x0, x1 + 1):
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
        self.framebuffer[y][x] = color or self.current_color

        # esta es una funcion que reciba un vertice como parametro que se transforma en X y Y
    def transform(self, v, translate=(0, 0, 0), scale=(1, 1, 1)):
        # se tiene que retornar V2 (uno de los objetos de antes)
        # return V2(
        #     round((v[0] + translate[0]) * scale[0]),
        #     round((v[1] + translate[1]) * scale[1])
        # )

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

                A = self.transform(model.vertices[f1], translate, scale)
                B = self.transform(model.vertices[f2], translate, scale)
                C = self.transform(model.vertices[f3], translate, scale)

                self.triangle(A, B, C)

            elif vcount == 4:
                # se agarra el array 0 en la posicion 0
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1
                f4 = face[3][0] - 1

                A = self.transform(model.vertices[f1], translate, scale)
                B = self.transform(model.vertices[f2], translate, scale)
                C = self.transform(model.vertices[f3], translate, scale)
                D = self.transform(model.vertices[f4], translate, scale)
                self.triangle(A, B, C)
                self.triangle(A, C, D)
            '''
            for j in range(vcount):
                f1 = face[j][0]
                # modulo 4 (% 4) hace que se loopee
                f2 = face[(j + 1) % vcount][0]

                # esto se hace para trabajar desde el vertice 0
                v1 = model.vertices[f1 - 1]
                v2 = model.vertices[f2 - 1]

                # esto se hace para no tener que trabajar con decimales 
                # se suma y multiplica para mover y agrandar el cuadrado 
                
                x1 = round((v1[0] + translate[0]) * scale[0])
                y1 = round((v1[1] - translate[1]) * scale[1])
                x2 = round((v2[0] + translate[0]) * scale[0])
                y2 = round((v2[1] - translate[1]) * scale[1])
                
                self.line(x1, y1, x2, y2)
            '''
            

    # # este es un triangle wirefram
    # def triangle_wireframe(self, A, B, C):
    #     self.line(A, B)
    #     self.line(B, C)
    #     self.line(C, A)

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
                
                # self.point(x, y, color)
                # # las coordenadas baricentricas permiten que se oueda interpolar 
                # z = A.z * w + B.z * v + C.z * u
                # try:
                #     # hay que revisar cual valor de z esta almacenado en el zbuffer
                #     if z > self.zbuffer[x][y]:
                #         self.point(x, y) #ahora se necesita una funcion que diga si hay un punto dentro de triangulo
                #         #cada vez que se agregue un punto, se quiere saber cual es su coordenada en z para guardarla en el zbuffer
                #         self.zbuffer[x][y] = z
                # except:
                #     pass

           

r =  Renderer(800, 600)

# # r.current_color = color(255, 0, 0)
# r.triangle(V2(10,70), V2(50, 160), V2(70, 80), color(random.randint(0, 225), random.randint(0, 225), random.randint(0, 225)))
# # r.current_color = color(255, 255, 255)
# r.triangle(V2(180, 50), V2(150, 1), V2(70, 180), color(random.randint(0, 225), random.randint(0, 225), random.randint(0, 225)))
# # r.current_color = color(0, 255, 0)
# r.triangle(V2(180, 150), V2(120, 160), V2(130, 180), color(random.randint(0, 225), random.randint(0, 225), random.randint(0, 225)))

# r.load('./models/cube2.obj', (4, 3, 3), (100, 100, 100))
r.load('./models/model.obj', (1, 1, 1), (300, 300, 300))
r.render()




