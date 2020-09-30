import copy
from termcolor import colored
from colorama import init
from excepciones import InvalidPlayException

init(autoreset = True)                                              # para los colores en consola

class Tablero:
	def __init__(self):
		self.tablero = []
		self.tableroAnterior = []
		self.jugadas = []
		self.ultimaJugada = []

	# Permite imprimir el tablero de juego 
	def imprimirTablero(self, mostrarJugadasValidas = True):
        # si el tablero está vacío
		if len(self.tablero) == 0:
			print('  A')
			print('01', colored('■', 'white'))
			return

		jugadasValidas = self.jugadasValidas()            
		lineas = []                                       # Aquí se almacenan las líneas del tablero
		for y in range(len(self.tablero)):                # por cada fila del tablero
			line = ''
			for x in range(len(self.tablero[y])):         # por cada columna en esa fila
				if self.tablero[y][x] is not None:
					if (x, y) in self.ultimaJugada:
						line += colored(self.tablero[y][x].figura + ' ', self.tablero[y][x].color, 'on_white')    # si la pieza esta es la última jugada se resalta el color blanco
					else:
						line += colored(self.tablero[y][x].figura + ' ', self.tablero[y][x].color)                # sino es de la última jugada la muestra normal
				elif (x, y) in jugadasValidas and mostrarJugadasValidas:       
						line += colored('■', 'white') + ' '
				else:
					line += '  '

			lineas.append(line)

		# Agregamos la primer línea del tablero, con sus identificadores
		line = ''.join([chr(65 + i) + ' ' for i in range(len(self.tablero[0]))])
		lineas.insert(0, line)                                                                   # Como es la primera línea la agregamos al inicio del array
		lineas.append(line)

        # Imprimimos la línea
		for i in range(0, len(lineas)):
			mostrar = str(i).zfill(2) if 0 < i < len(lineas) - 1 else '  '
			print(mostrar, lineas[i], mostrar)

    # Determina cuales son las casillas en las que el jugador tiene la oportunidad de poner una ficha
    def jugadasValidas(self):
        jugadasValidas = []

        if not self.tablero:
            return [(1, 1)]                                         # la única casilla válida

        for y in range(len(self.tablero)):
            for x in range(len(self.tablero[y])):
                if self.jugadaValida(None, x, y):                   # Si cumple con las condiciones se agrega a la lista
                    jugadasValidas.append((x, y))
        return jugadasValidas

    # Verifica que una jugada sea válida
    # Retorna False si la jugada no es válida o True si la jugada es válida
    def jugadaValida(self, ficha, x, y):

        if x < 0 or x >= len(self.tablero[0]):                                  # verifica que el número de columna este dentro del tablero
            return False
        if y < 0 or y >= len(self.tablero):                                     # verifica que el número de línea este dentro del tablero
            return False
        if x == 0 and y == 0:                                                   # verifica que no sea la esquina superior izquierda
            return False
        if x == 0 and y == len(self.tablero) - 1:                               # verifica que no sea la esquina inferior izquierda
            return False
        if x == len(self.tablero[0]) - 1 and y == len(self.tablero) - 1:        # verifica que no sea la esquina inferior derecha
            return False
        if x == len(self.tablero[0]) - 1 and y == 0:                            # verifica que no sea la esquina superior izquierda
            return False

                       
        if self.tablero[y][x] is not None:                                      # verifica que no sea una posición donde ya hay una ficha
            return False


        # Verifica que haya al menos un espacio adyacente al elegido que contenga una ficha
        espaciosAdyacentes = []
        if y - 1 >= 0:
            espaciosAdyacentes.append((self.tablero[y - 1][x] is None))      
        if y + 1 < len(self.tablero):
            espaciosAdyacentes.append((self.tablero[y + 1][x] is None))
        if x - 1 >= 0:
            espaciosAdyacentes.append((self.tablero[y][x - 1] is None))
        if x + 1 < len(self.tablero[y]):
            espaciosAdyacentes.append((self.tablero[y][x + 1] is None))

        if all(espaciosAdyacentes):                                                    # all () verifica si todos los elementos de la lista son True
            return False                                                               # Si todos los espacios adyacentes están vacíos retorna False pues no es un lugar válido

        # Verifica que la jugada este conectada a otra jugada
        arregloJugadas = [(play[0], play[1]) for play in self.jugadas]
        if len(arregloJugadas) > 0:
            revisarHorizontal = True
            revisarVertical = True
            if len(arregloJugadas) > 1:
                if arregloJugadas[0][0] == arregloJugadas[1][0]:
                    revisarHorizontal = False
                if arregloJugadas[0][1] == arregloJugadas[1][1]:
                    revisarVertical = False

            inPlays = False

            if revisarHorizontal:
                fichaEnX = x
                while fichaEnX - 1 >= 0 and self.tablero[y][fichaEnX - 1] is not None:
                    fichaEnX -= 1
                    if (fichaEnX, y) in arregloJugadas:
                        inPlays = True

                fichaEnX = x
                while fichaEnX + 1 < len(self.tablero[y]) and self.tablero[y][fichaEnX + 1] is not None:
                    fichaEnX += 1
                    if (fichaEnX, y) in arregloJugadas:
                        inPlays = True

            if revisarVertical:
                fichaEnY = y
                while fichaEnY - 1 >= 0 and self.tablero[fichaEnY - 1][x] is not None:
                    fichaEnY -= 1
                    if (x, fichaEnY) in arregloJugadas:
                        inPlays = True

                fichaEnY = y
                while fichaEnY + 1 < len(self.tablero) and self.tablero[fichaEnY + 1][x] is not None:
                    fichaEnY += 1
                    if (x, fichaEnY) in arregloJugadas:
                        inPlays = True

            if not inPlays:
                return False

        # Si no se pone ninguna ficha no se hace ninguna prueba, se acepta la jugada y se toma como un skip
        if ficha is None:
            return True

        # Verifica todas las fichas horizontales
        fila = [ficha]
        fichaEnX = x + 1
        while fichaEnX < len(self.tablero[0]) and self.tablero[y][fichaEnX] is not None:
            fila.append(self.tablero[y][fichaEnX])
            fichaEnX += 1

        fichaEnX = x - 1
        while fichaEnX >= 0 and self.tablero[y][fichaEnX] is not None:
            fila.append(self.tablero[y][fichaEnX])
            fichaEnX -= 1

        if not self.verificarLineaValida(fila):                                     # Si la línea no es válida, la jugada tampoco lo es
            return False

        # Verifica todas las fichas verticales
        fila = [ficha]
        fichaEnY = y + 1
        while fichaEnY < len(self.tablero) and self.tablero[fichaEnY][x] is not None:
            fila.append(self.tablero[fichaEnY][x])
            fichaEnY += 1

        fichaEnY = y - 1
        while fichaEnY >= 0 and self.tablero[fichaEnY][x] is not None:
            fila.append(self.tablero[fichaEnY][x])
            fichaEnY -= 1

        if not self.verificarLineaValida(fila):
            return False

        return True                                                                 # Si no pasa ninguna de las situaciones anteriores la jugada es válida

    # Verifa si una línea dada es válida o no
    # Si toda la línea es del mismo color, verifica que cada figura aparezca una única vez
    # Si toda la línea es de la misma figura, verifica que cada color aparezca una única vez
    def verificarLineaValida(self, fila):

        if len(fila) == 1:
            return True

        if all(fila[i].color == fila[0].color for i in range(len(fila))):                       # si toda la fila es del mismo color
            figuras = []
            for i in range(len(fila)):
                if fila[i].figura in figuras:                                                     # si la ficha ya está el la fila
                    return False
                figuras.append(fila[i].figura)                                                    # si no está la agrega para seguir verificando

        elif all(fila[i].figura == fila[0].figura for i in range(len(fila))):                     # si toda la fila es de la misma ficha
            colores = []
            for i in range(len(fila)):
                if fila[i].color in colores:                                                     # verifica que no haya colores repetidos
                    return False
                colores.append(fila[i].color)

        else:                                                                                   # si no es ninguno de los casos anteriores la fila es inválida
            return False

        return True                                                                             # la fila es válida

# Inicia un turno
def iniciarTurno(self):
        self.jugadas = []
        self.tableroAnterior = copy.deepcopy(self.tablero)

# Da la puntuación de la jugada actual
def puntuacion(self):
    if len(self.jugadas) == 0:                      # si no puso ninguna ficha
        return 0

    puntuacion = 0
    puntuacionHorizontal = []
    puntuacionVertical = []

    for jugada in self.jugadas:
        x, y = jugada

        xMinimo = x
        while xMinimo - 1 >= 0 and self.tablero[y][xMinimo - 1] is not None:
            xMinimo -= 1

        xMaximo = x
        while xMaximo + 1 < len(self.tablero[y]) and self.tablero[y][xMaximo + 1] is not None:
            xMaximo += 1

        if xMinimo != xMaximo:                                                      # si son diferentes es porque se puso más de una ficha
            qwirkleContador = 0
            for posX in range(xMinimo, xMaximo + 1):
                if (posX, y) not in puntuacionHorizontal:                            # si la jugada no se ha sumado a la puntuación
                    puntuacion += 1
                    qwirkleContador += 1
                    puntuacionHorizontal.append((posX, y))

                    if (x, y) not in puntuacionHorizontal:
                        puntuacion += 1
                        qwirkleContador += 1
                        puntuacionHorizontal.append((x, y))
                posX += 1

            if qwirkleContador == 6:                                              # si hizo una jugada qwirkle
                puntuacion += 6

        yMinimo = y
        while yMinimo - 1 >= 0 and self.tablero[yMinimo - 1][x] is not None:
            yMinimo -= 1

        yMaximo = y
        while yMaximo + 1 < len(self.tablero) and self.tablero[yMaximo + 1][x] is not None:
            yMaximo += 1

        if yMinimo != yMaximo:
            qwirkleContador = 0
            for posY in range(yMinimo, yMaximo + 1):
                if (x, posY) not in puntuacionVertical:
                    puntuacion += 1
                    qwirkleContador += 1
                    puntuacionVertical.append((x, posY))

                    if (x, y) not in puntuacionVertical:
                        puntuacion += 1
                        qwirkleContador += 1
                        puntuacionVertical.append((x, y))
                posY += 1

            if qwirkleContador == 6:
                puntuacion += 6

    return puntuacion

# Termina el turno actual
def terminarTurno(self):
    self.ultimaJugada = self.jugadas[:]                                             # Guardamos la última jugada 
    self.jugadas = []                                                               # Vaciamos el arreglo de jugadas

def jugar(self, ficha, x = 1, y = 1):
    if len(self.tablero) == 0:                                              # Si el tablero está vacío crea un tablero de 3 * 3
        self.tablero = [[None] * 3 for i in range(3)]
        x = 1
        y = 1
    else:
        if not self.jugadaValida(ficha, x, y):
            raise InvalidPlayException()

    self.tablero[y][x] = ficha
    self.jugadas.append((x, y))
    self.generarEspacios()

# Genera espacio suficiente en el alrededor del tablero, de manera que siempre haya un espacio alrededor 
# Cada vez que genera un nuevo espacio actualiza las jugadas
def generarEspacios(self):

        # Inicio del tablero
        if any(self.tablero[0][i] is not None for i in range(len(self.tablero[0]))):
            self.tablero.insert(0, [None] * (len(self.tablero[0])))
            self.jugadas = [(jugada[0], jugada[1]+1) for jugada in self.jugadas]
            self.ultimaJugada = [(jugada[0], jugada[1]+1) for jugada in self.ultimaJugada]

        # Final del tablero
        fondo = len(self.tablero) - 1
        if any(self.tablero[fondo][i] is not None for i in range(len(self.tablero[0]))):
            self.tablero += [[None] * (len(self.tablero[0]))]

        # Parte izquierda del tablero
        if any(self.tablero[i][0] is not None for i in range(len(self.tablero))):
            for i in range(len(self.tablero)):
                self.tablero[i].insert(0, None)
            self.jugadas = [(jugada[0] + 1, jugada[1]) for jugada in self.jugadas]
            self.ultimaJugada = [(jugada[0] + 1, jugada[1]) for jugada in self.ultimaJugada]

        # Parte derecha del tablero
        right = len(self.tablero[0]) - 1
        if any(self.tablero[i][right] is not None for i in range(len(self.tablero))):
            for i in range(len(self.tablero)):
                self.tablero[i] += [None]

