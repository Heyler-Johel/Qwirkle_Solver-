from random import Random
from termcolor import colored
from tablero.exceptions import InvalidPlayException


class Jugador:
    # Constructor de objetos
    def __init__(self, nombre ='Unknown Player'):
        self.fichas = []
        self.puntuacion = 0
        self.nombre = nombre

    # Le asigna seis fichas iniciales de la bolsa de fichas al jugador
    def asignarFichas (self, bolsaFichas):
        rnd = Random()
        while len(self.fichas) < 6 and len(bolsaFichas) > 0:
            posRandom = rnd.randint(0, len(bolsaFichas) - 1)                # elige aleatoriamente una posición del arreglo de fichas 
            self.fichas.append(bolsaFichas.pop(posRandom))                  # y la agrega a la mano del jugador

    # Permite que el jugador humano juegue su turno en el juego
    def jugarTurno(self, tablero):
        fichasJugador = self.fichas.copy()
        while True:
            print(self.mostrarFichasMano(fichasJugador))
            print ('  Comandos:')
            print ('    (r)  reinicia la jugada')
            print ('    (#Ficha) (ColumnaFila)  por ejemplo: 1 A5')
            print ('    (t)  termina el turno')

            opcion = input ('  -> ')
            print('\n\n\n')

            if len(opcion) == 0:                                # si no selecciono nada se muestra la misma pantalla de nuevo
                continue   

            if opcion == 'r':                                   # se deshace cualquier jugada hecha y se muestran las fichas y tablero iniciales
                tablero.reiniciarTurno()
                fichasJugador = self.fichas.copy()
                tablero.imprimirTablero()
                continue

            if opcion == 't':                                   # se termina el turno del jugador actual
                break
                                                        
            try:                                                # si el primer dato no es el identificador de una ficha se muestra el error
                intFicha = int (opcion[0])
            except ValueError:
                print (colored('El valor de la ficha elegida debe ser un valor númerico', 'red', attrs=['bold']), '\n')
                continue

            if indiceFicha >= len(fichasJugador):                                       # la ficha elegida es mayor a la cantidad de fichas en la mano
                continue

            x, y = tablero.convertirCoordenada(opcion[2:].upper())                      # convertimos el valor dado en un par ordenado
            try:
                tablero.jugar(fichasJugador[indiceFicha], x, y)                         # use esta ficha es esta coordenada
                fichasJugador.pop(indiceFicha)
            except InvalidPlayException:                                                # si la jugada no es válida mostramos el error
                print (colored('La jugada elegida no es válida', 'red', attrs=['bold']), '\n')

            tablero.imprimirTablero()

        self.fichas = fichasJugador.copy()

    # Muestra las fichas que tiene un jugador en su mano
    @staticmethod
    def mostrarFichasMano(fichasMano):
        fichasEnMano = ''
        mensaje = ''
        for ficha in fichasMano:
            fichasEnMano += colored(ficha.figura, ficha.color) + ' '
        mensaje += '\n  Fichas del jugador: %s' % fichasEnMano
        mensaje += '\n                      1 2 3 4 5 6\n'

        return mensaje

    def sumarPuntos(self, pPuntos):
        self.puntuacion += pPuntos

    def sinFichas(self):
        return len(self.fichas) == 0

    def vaciarFichas(self):
        self.fichas = []

    def getFichas(self):
        return self.fichas

    def getPuntuacion(self):
        return self.puntuacion

    def getNombre(self):
        return self.nombre

