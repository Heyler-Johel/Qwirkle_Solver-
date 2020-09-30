from tablero import Tablero, Ficha, Figura, Color
from jugador import Jugador
from bots import BotHumano, BotInteligente

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

        Figura = [
            Figura.circulo,
            Figura.diamante,
            Figura.trebol,
            Figura.cuadrado,
            Figura.estrella,
            Figura.triangulo
        ]

        Color = [
            Color.blue,
            Color.cyan,
            Color.green,
            Color.magenta,
            Color.red,
            Color.yellow
        ]

        for i in range(3):
            for j in range(len(colors)):
                for k in range(len(shapes)):
                    self.bolsaFichas.append(Ficha(color = Color[j], figura = Figura[s]))

    def main(self, jugadores):           

        self.tablero = Tablero() 
        self.generarFichas()   

        for jugador in jugadores:
            if jugador == 'humano':
                self.jugadores.append(BotHumano('Humano'))
            elif jugador == 'bot_basico':
                self.jugadores.append(BotBasico('Basico'))
            elif jugador == 'bot_inteligente':
                self.jugadores.append(BotInteligente('Inteligente'))
            else:
                raise ValueError('%s no es un tipo de jugador válido' % jugador)

        msgPuntuacion = (-1, 0)
        jugadorActual = 0
        while True:
            print('\n' * 50)                            # espacios entre cada tablero
            input ('Presione una tecla para continuar...')     # para que se aprecie cada jugada
            print('Jugando Qwirkle\n')

            print('  Puntuación:')
            for i in range(len(self.jugadores)):
                message = '    %s - %i' % (self.jugadores[i].nombre(), self.jugadores[i].puntuacion())
                if msgPuntuacion[0] == i:
                    message += ' +%i' % msgPuntuacion[1]                #msgPuntuacion[1] es la cantidad de puntos nuevos obtenidos
                print(message)
            print('\n  Es el turno de: %s \n' % self.jugadores[jugadorActual].nombre())

            self.tablero.imprimirTablero(mostrarJugadasValidas = True)
            self.jugadores[jugadorActual].asignarFichas(self.bolsaFichas)               # Se le asigna al jugador sus seis fichas
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
