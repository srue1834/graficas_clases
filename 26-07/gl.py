import struct
from obj import Obj


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
    def line(self, x0, y0, x1, y1):
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)
        # en el caso que no funcione la linea, steep hace que se cambien los valores de y a x. Le da la vuelta
        steep = dy > dx
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        # ahora se reemplatea la pendiente.
            dy = abs(y1 - y0)
            dx = abs(x1 - x0)
    
        offset = 0 # offset = 0 * 2 * dx
        
        threshold = dx # threshold = 0.5 * 2 * dx
        y = y0

        points = []
        for x in range(x0, x1):
            #se agrega esto para que este en la direccion correcta
            if steep:
                points.append((y, x))
            else:
                points.append((x, y))
            
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
    
    # Esta funcion es para cargar y renderizar obj
    def load(self, filename, translate, scale): # ahora a load se le pasa que tanto se quiere que se mueva para los lados y abajo
        model = Obj(filename)
        # se tienen que recorrer las caras, agarrar cada uno de los indices y pintar cada vertice
        
        for face in model.faces:
            # para saber si hace triangulos o cuadrados
            vcount =  len(face)
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
            

r =  Renderer(800, 600)
r.load('./models/face.obj', [25, -5], [15, 15])
r.render()

