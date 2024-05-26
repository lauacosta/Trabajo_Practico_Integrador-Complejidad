'''
Un triómino es una forma que consiste de tres cuadrados unidos, hay dos formas básicas:
** y ***
*
Si todas las posibles orientaciones son tenidas en cuenta, existen 6 posibles:
* | *** | ** | ** | *  |  * |
* |     | *  |  * | ** | ** | 
* |     |    |    |    |    | 
Cualquier tablero n x m que es divisible por 3 puede ser completado con trióminos.
Si consideramos todas las posibles combinaciones que se pueden dar con estas 6 piezas hay 41 posibilidades para completar un tablero de 2x9

Entonces, cuantas combinaciones existen para completar un tablero de 9x12.                 
'''

formas = [
  [(0,0),(1,0),(0,1)],
  [(0,0),(1,0),(1,1)],
  [(0,0),(0,1),(1,1)],
  [(0,0),(0,1),(-1,1)],
  [(0,0),(1,0),(2,0)],
  [(0,0),(0,1),(0,2)]
  ]