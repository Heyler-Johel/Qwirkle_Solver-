# Qwirkle_Solver
Qwirkle es un juego de mesa, en cual el objetivo es obtener puntos creando filas o columnas con fichas que contienen símbolos
de colores. Existen 6 símbolos y 6 colores diferentes. Cada símbolo existen en cada uno de los 6 colores y cada una de estas combinacio-
nes
se repite 3 veces, para un total de 108 fichas. Las reglas son sencillas, cada fila o columna de fichas adyacentes debe estar formada por:
	1) Fichas del mismo color, pero con símbolos diferentes
	2) Fichas con el mismo símbolo pero de colores diferentes.
El objetivo de este proyecto es crear 2 algoritmos que puedan jugar qwirkle, uno básico que busque la mejor solución basado en los puntos obteni-
dos en el turno y uno ”inteligente”, que es una versión optimizada con más reglas de poda para buscar también soluciones que sean 
buenas a futuro. La base de ambos algoritmos es la estrategia debacktracking.
