from bots.botBasico import BotBasico
from bots.botInteligente import BotInteligente
from jugador import Jugador
from tablero.tablero import Tablero
from tablero.ficha import Ficha, Color, Figura

class QwirkleGame:
    #Constructor de objetos
    def __init__(self):
        self.bolsaFichas = []
        self.jugadores = []
        self.tablero = []


    # Genera la bolsa de fichas inicial con 108 fichas.
    # Seis fichas de cada color y figura.
    def generarFichas(self):
        self.bolsaFichas = []

        figuras = [
            Figura.circulo,
            Figura.diamante,
            Figura.trebol,
            Figura.cuadrado,
            Figura.estrella,
            Figura.triangulo
        ]

        colores = [
            Color.blue,
            Color.cyan,
            Color.green,
            Color.magenta,
            Color.red,
            Color.yellow
        ]

        for i in range(3):
            for j in range(len(colores)):
                for k in range(len(figuras)):
                    self.bolsaFichas.append(Ficha(color = colores[j], figura = figuras[k]))

    # Permite mostrar la bolsa de fichas del juego
    def mostrarBolsaFichas(self):
        for i in range (len(self.bolsaFichas)):
            print (self.bolsaFichas[i])

    def main(self, jugadores):           

        self.tablero = Tablero() 
        self.generarFichas()   
#        self.mostrarBolsaFichas()

        for jugador in jugadores:
            if jugador == 'humano':
                self.jugadores.append(Jugador('Humano'))
            elif jugador == 'botBasico':
                self.jugadores.append(BotBasico('Basico'))
            elif jugador == 'botInteligente':
                self.jugadores.append(BotInteligente('Inteligente'))
            else:
                raise ValueError('%s no es un tipo de jugador válido' % jugador)

        msgPuntuacion = (-1, 0)
        jugadorActual = 0
        while True:
            input ('\n\nPresione una tecla para continuar...')     # para que se aprecie cada jugada
            print('\n' * 50)                            # espacios entre cada tablero
            print('Jugando Qwirkle\n')

            print('  Puntuación:')
            for i in range(len(self.jugadores)):
                message = '    %s - %i' % (self.jugadores[i].getNombre(), self.jugadores[i].getPuntuacion())
                if msgPuntuacion[0] == i:
                    message += ' + %i' % msgPuntuacion[1]                #msgPuntuacion[1] es la cantidad de puntos nuevos obtenidos
                print(message)
            print('\n  Es el turno de: %s \n' % self.jugadores[jugadorActual].getNombre())

            self.jugadores[jugadorActual].asignarFichas(self.bolsaFichas)                                                       # Se le asigna al jugador sus seis fichas
            print (self.jugadores[jugadorActual].mostrarFichasMano(self.jugadores[jugadorActual].getFichas()))             
            self.tablero.imprimirTablero(mostrarJugadasValidas = True)
            self.tablero.iniciarTurno()
            self.jugadores[jugadorActual].jugarTurno(self.tablero)

            puntuacion = self.tablero.puntuacion()                                           
            self.jugadores[jugadorActual].sumarPuntos(puntuacion)                               # Le agregamos los puntos al marcador global del jugador

            msgPuntuacion = (jugadorActual, puntuacion)
            self.tablero.terminarTurno()                                                        # Terminamos el turno del jugador actual
            self.jugadores[jugadorActual].asignarFichas(self.bolsaFichas)                       # Reemplazamos las fichas que fueron usadas

            if self.jugadores[jugadorActual].sinFichas():                                       # Si el jugador se quedo sin fichas termina el juego
                break

            jugadorActual += 1                                                                  # Cambiamos de jugador
            if jugadorActual >= len(self.jugadores):
                jugadorActual = 0

        jugadorGanador = max(self.jugadores, key = lambda p: p.puntuacion())                    # Se elige al jugador con mayor puntuación

        print('\n  Puntuación final:')                                                          # Imprimimos las puntuaciones finales
        for i in range(len(self.jugadores)):
            message = '    %s - %i' % (self.jugadores[i].nombre(), self.jugadores[i].puntuacion())
            print(message)

        print('\n  %s es el ganador!\n' % jugadorGanador.nombre())
