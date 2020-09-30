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

    def jugarTurno(self, board):
        # aquí se debe implementar el algoritmo de juego del humano
        return False

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

