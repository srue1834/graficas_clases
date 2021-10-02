# se hacer una clase para crear metodos capaces de leer archivos .obj

class Obj(object):
    def __init__(self, filename):
        # con with se limpia todo lo que haga la funcion al finalizar
        with open(filename) as f:
            # splitlines agarra el string grande y lo separa linea por linea 
            self.lines = f.read().splitlines()

        # el objetivo final es que cualquier archivo OBJ tenga una lista de vertices y una lista de caras
        self.vertices = []
        self.faces = []
        # para no llamar a mano, se llama al constructor 
        self.read()


    def read(self):
        # esto se hara para ir linea por linea en el archivo
        for line in self.lines:
            # esto no funciona con todos los obj, ESTO TRUENA CUANDO EL ARCHIVO TENGA LINEAS EN BLANCO
            if line:
                # si la linea es de vertice empieza con una V, y es una cara cuando empieza con F
                prefix, value  = line.split(' ', 1)

                if prefix == 'v':
                    # se hace un append por cada vez que se encuetra una V se tiene que ir acomulando 
                    self.vertices.append(
                        # se utiliza map para aplicarle una funcion a todos los parametros de un array, no es tan eficiente porque recorre el array dos veces
                        list(map(float, value.split(' ')))
                    )
                elif prefix == 'f':
                    self.faces.append(
                        [list(map(int, face.split('/'))) for face in value.split(' ')]
                    )



