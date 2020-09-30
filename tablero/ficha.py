# Clase Color
# Contiene los posibles colores que puede tener una ficha del tablero
class Color:
    red = 'red'
    yellow = 'yellow'
    green = 'green'
    cyan = 'cyan'
    magenta = 'magenta'
    blue = 'blue'

# Clase Figura
# Contiene las posibles figuras que puede tener una ficha del tablero
class Figura:
    triangulo = '▲'
    cuadrado = '■'
    circulo = '●'
    estrella = '✶'
    trebol = '♣'
    diamante = '♦'

# Clase Ficha 
# Permite crear fichas para el tablero, de un color y una figura especifica 
class Ficha:
    # Constructor de objetos Ficha
    def __init__(self, color = None, figura = None):
        self.color = color
        self.figura = figura

    # Retorna los datos de una ficha  en string.
    def toString(self):
        texto = self.color + ' ' + self.figura
        return texto
        