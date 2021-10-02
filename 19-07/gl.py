from random import randint
import struct
from typing import KeysView

''' 
Se crea una clase que deje escribir en byte. La clase struct permite que se pueda pasar cosas y que se interprete en data binaria.
La información se puede guardar en un formato especifico. 
En la funcion word va un "h" ya que se necesita dos bits.
'''

def char(c):
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    # short
    return struct.pack('=h', w)

def dword(w):
    # long
    return struct.pack('=l', w)

'''
Aqui se crea una función de color (r,g,b) que regresa bytes que se tienen que escribir en memoria.
La manera mas simple para convertir en bytes algo es casting. En py hay una funcion que hace eso llamada bytes().
'''

def color(r, g, b):
    return bytes([b, g, r])

BLACK =  color(0, 0, 0)
WHITE =  color(255, 255, 255)

'''

Se creara algo bien básico, que se pueda escribir en una pantalla. 
En el constructor se tienen que recibir dos parametros; el ancho de la pantalla (sirve para inicializar la raiz), y el alto.
Object es la clase padre de la que se hereda de forma generica. El constructor se crea primero con self 

'''

class Renderer(object):
    def glinit():
        r =  Renderer(1024, 768)

    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Esta variable le da color al punto
        self.current_color = WHITE

        self.clear()

    '''
    Aqui se inicializa el framebuffer, que es una red de arrays que tienen los canales verde, rojo y azul.
    Ahora se dice que retorna BLACK para cada valor en un rango, y el rango va ser el ancho completo de la pantalla.
    Se quiere que haga eso en un rango que es el alto completo de la pantalla.
    Clear es una función que regresa todo a negro.
    '''

    def clear(self):
        self.framebuffer = [
            [BLACK for x in range(self.width)]
            for y in range(self.height)
        ]

    '''
    Eset es un metodo que sirve para escribir un archivo y que reciba el nombre del archivo que escribira.
    '''

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
        

    def render(self):
        self.write('a.bmp')

    # Se agregara un punto 
    def point(self, x, y, color = None):
        self.framebuffer[y][x] = color or self.current_color

'''

El objetivo es que se crea un nuevo render que contenga el tamño de la pantalla.
Despues se llama algo para que lo rendirice, y que el render este en un a.bmp

'''
r =  Renderer(80, 80)
r.current_color = color(255, 255, 255)

''' 
PUNTITO

r.point(10, 10)
r.point(11, 10)
r.point(10, 11)
r.point(11, 11)

CUADRADO

for x in range(10, 100):
    for y in range(10, 100):
        r.point(x, y)

lINEA DIAGONAL

for x in range(10, 100):
    for y in range(10, 100):
        if x == y:
            r.point(x, y)


VARIOS PUNTOS

import random

for x in range(1024):
    for y in range(768):
        if random.random() > 0.5:
            r.point(x, y)

COLOR AL AZAR

for x in range(1024):
    for y in range(768):
        if random.random() > 0.5:
            r.point(x, y, color(
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            ))
'''

# ALGORITMO DE DIXTRA, VER BRESENHAM ALGORITHM
def line(x0, y0, x1, y1):
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

    # la division se elimina 
    # ahora todo se multiplica por dx, ya que son parte de la exuacion   
   
    offset = 0 # offset = 0 * 2 * dx
    # se le suma 1 al threshold cada vez que Y aumente. Se suma Y cuando el offset pase del threshold actual.
    # el 0.5 se elimina multiplicandolo todo por 2
    threshold = dx # threshold = 0.5 * 2 * dx
    y = y0
    '''
    y = mx + b
    x es un valor que empieza en x0 y termina en x1. Se va subiendole 1 hasta que llegue al final.
    Ahora se meten los puntos a un array.

    '''
    points = []
    for x in range(x0, x1):
        #se agrega esto para que este en la direccion correcta
        if steep:
            points.append((y, x))
        else:
            points.append((x, y))
        
        offset += 2 * dy # offset += (dy/dx) * 2 * dx
        # se le suma a la pendiente el offset, y se revisa si el offset ya paso el threshold
        if offset >= threshold:
        # en vez de sumarle el offset a Y solo se le suma 1
            y += 1 if y0 < y1 else -1
            threshold += 2 * dx # threshold += 1 * 2 * dx

        #se recorre el array de puntos
    for point in points:
        #esto es un destructuración del punto
        r.point(*point)
        

    '''
    # aqui se hace un while para que hayan puntos en medio, se forma una linea diagonal 
    i = 0
    while i <= 1:
        x = x0 + (x1 - x0) * i
        y = y0 + (y1 - y0) * i
        r.point(round(x), round(y))
        i += 0.01
    '''
    
'''
    i = 0
    j = 0
    while (x0 + i) < x1 and (y0 + j) < y1:
        r.point(x0 + i, y0 + j)
        i += 1
        j += 1
    r.point(x0, y0)
    r.point(x1, y1)
'''
    
'''
line(13, 20, 60, 40)
line(20, 10, 40, 60)
line(40, 60, 10, 20)

'''
# line(10, 60, 70, 10)
# line(40, 10, 20, 60)
line(13, 20, 60, 40)
line(20, 10, 40, 60)
line(40, 60, 10, 20)
r.render()

