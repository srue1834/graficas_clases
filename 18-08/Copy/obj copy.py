import struct


def color(r, g, b):
    return bytes([b, g, r])

# se hacer una clase para crear metodos capaces de leer archivos .obj
class Obj(object):
    def __init__(self, filename):
        # con with se limpia todo lo que haga la funcion al finalizar
        with open(filename) as f:
            # splitlines agarra el string grande y lo separa linea por linea 
            self.lines = f.read().splitlines()

        # el objetivo final es que cualquier archivo OBJ tenga una lista de vertices y una lista de caras
        self.vertex = []
        self.tvertex = []
        self.faces = []
        # para no llamar a mano, se llama al constructor 
        self.read()


    def read(self):
        # esto se hara para ir linea por linea en el archivo
        for line in self.lines:
            # esto no funciona con todos los obj, ESTO TRUENA CUANDO EL ARCHIVO TENGA LINEAS EN BLANCO
            if line:
                #NUEVOOOOOOO
                try:
                    # si la linea es de vertice empieza con una V, y es una cara cuando empieza con F
                    prefix, value  = line.split(' ', 1)
                except:
                    prefix = ''

                if prefix == 'v':
                    # se hace un append por cada vez que se encuetra una V se tiene que ir acomulando 
                    self.vertex.append(
                        # se utiliza map para aplicarle una funcion a todos los parametros de un array, no es tan eficiente porque recorre el array dos veces
                        list(map(float, value.split(' ')))
                    )
                elif prefix == 'vt':
                    self.tvertex.append(
                        list(map(float, value.split(' ')))
                    )
                elif prefix == 'f':
                    self.faces.append(
                        [list(map(int, face.split('/'))) for face in value.split(' ')]
                    )


# NUEVO
# se tiene que hacer el procedimiento inverso a un BM para poder leer un archivo externo de textura
# constructor que recibe el archivo
class Texture(object):
    def __init__(self, path):
        self.path = path
        # siempre que se declara una textura, se quiere cargar de una vez
        self.read()

    def read(self):
        image = open(self.path, "rb")
        # leer el archivo
        image.seek(10) # 2 + 4 + 4 seek es un punturo que hace que se mueva de lado a lado
        # aqui se tiene que leer exactamente 4 bits
        # se convierte en un entero, entonces se hace el proceso inverso a dword
        header_size = struct.unpack("=l", image.read(4))[0] # el primer parametro es el formato
        image.seek(18)

        # para poder llegar a los otros datos de image header 
        self.width = struct.unpack("=l", image.read(4))[0]
        self.height = struct.unpack("=l", image.read(4))[0]
        self.pixels = []
        image.seek(header_size) # ahora se salta el encabezado completo
    
        for y in range(self.height):
            # cada fila que lea el archivo se le metera una array vacio, para aplicar un array de dos dimensiones
            self.pixels.append([]) # al array vacio se le agregara los 3 colores
            for x in range(self.width):
                b = ord(image.read(1)) # ord lo convierte en ordinal y se puede utilizar por ser unicamente un byte
                g = ord(image.read(1))
                r = ord(image.read(1))
                

                self.pixels[y].append(color(r,g,b))
                
        image.close()


        # self.pixels = []
        # image = open(self.path, 'rb')

        # # leer el archivo
        # image.seek(10) # 2 + 4 + 4 seek es un punturo que hace que se mueva de lado a lado

        # # aqui se tiene que leer exactamente 4 bits
        # val = image.read(4)
        # # se convierte en un entero, entonces se hace el proceso inverso a dword
        # header_size = struct.unpack('=l', image.read(4))[0] # el primer parametro es el formato

        # # para poder llegar a los otros datos de image header 
        # # image.seek(18) #2 +4 +4 +4 +4 = 18
        # self.width = struct.unpack('=l', image.read(4))[0]
        # self.height = struct.unpack('=l', image.read(4))[0]

        # image.seek(header_size) # ahora se salta el encabezado completo

        # for y in range(self.height):
        #     # cada fila que lea el archivo se le metera una array vacio, para aplicar un array de dos dimensiones
        #     self.pixels.append([]) # al array vacio se le agregara los 3 colores
        #     for x in range(self.width):
        #         b = ord(image.read(1)) # ord lo convierte en ordinal y se puede utilizar por ser unicamente un byte
        #         r = ord(image.read(1))
        #         g = ord(image.read(1))

        #         self.pixels[y].append(color(r,g,b))

# t = Texture('./textures/earth.bmp')
# print(t.width)
# print(t.height)