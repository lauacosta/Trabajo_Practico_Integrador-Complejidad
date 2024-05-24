#!/usr/bin/env python
import pprint
import unittest

FILAS = 8
COLUMNAS = FILAS

#El conjunto de candidatos son todas las posiciones del tablero 
TABLERO = [[0 for _ in range(FILAS)] for _ in range(COLUMNAS)]
CONJUNTO_SOLUCION = []

def control_limites(x: int, y: int):
    """
    Controla que los índices puedan ubicarse dentro del tablero.
    """
    return FILAS > x >= 0 and COLUMNAS > y >= 0

#Función de selección
def ev_movimientos(coordenada: tuple[int, int]) -> list[tuple[int, int]]:
    """
    Encuentra y devuelve todas los posibles movimientos validos desde una posición.
    """
    posibles_movimientos = [
        (coordenada[0] + x, coordenada[1] + y)
        for x, y in [
            (2, 1),
            (2, -1),
            (-2, 1),
            (-2, -1),
            (1, 2),
            (1, -2),
            (-1, 2),
            (-1, -2),
        ]
    ]
    
    movimientos_efectivos = [
        (x, y)
        for x, y in posibles_movimientos
        if control_limites(x, y)
        if TABLERO[x][y] == 0
    ]

    return movimientos_efectivos

#Función objetivo
def mover_pieza(coordenada: tuple[int, int], paso: int):
    """
    Implementación en base al Algoritmo de Warnsdorff.
        1. Comienza en la posición inicial.
        2. Desde la posición actual, calcula todos los movimientos posibles del caballo.
           Para cada movimiento posible, cuenta el número de movimientos futuros posibles desde esa nueva posición.
        3  Elige el movimiento que deja al caballo con la menor cantidad de
           movimientos futuros posibles. Si hay un empate, elige cualquiera de los movimientos empatados.
        4. Mueve el caballo a la nueva posición.
        5. Repite los pasos 2 a 4 hasta que todas las casillas hayan sido visitadas.
    """

    movimientos = ev_movimientos(coordenada)
    min_mov = 8
    min_idx = (0, 0)

    # Función de factibilidad. Busco el movimiento del caballo que deja al caballo con la menor cantidad de movimientos futuros posibles.
    for mov in movimientos:
        cant_mov = len(ev_movimientos(mov))
        if cant_mov < min_mov:
            min_mov = cant_mov
            min_idx = mov

    # Agrego al conjunto solución el movimiento que deja la menor cantidad de movimientos futuros 
    CONJUNTO_SOLUCION.append(min_idx)
    # Escribo el numero de paso en esa posición en el tablero
    TABLERO[min_idx[0]][min_idx[1]] = paso

    return min_idx

def main(x: int, y: int):
    print("Comienzo:")
    pprint.pp(TABLERO)

    pos = (x, y)
    CONJUNTO_SOLUCION.append(pos)

    TABLERO[x][y] = 1

    for i in range(2, FILAS * COLUMNAS + 1):
        pos = mover_pieza(pos, i)
        if pos is None:
            print("La quedamos aca jefe")
            break

    print("\nFinal:")
    pprint.pp(TABLERO)


def generar_csv():
    import csv

    with open("movimientos.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for i in range(len(CONJUNTO_SOLUCION) - 1):
            x1, y1 = CONJUNTO_SOLUCION[i]
            x2, y2 = CONJUNTO_SOLUCION[i + 1]
            writer.writerow([x1, y1, x2, y2])


class TestMain(unittest.TestCase):
    def test_main(self):
        for i in range(FILAS):
            for j in range(COLUMNAS):
                global TABLERO
                TABLERO = [[0 for _ in range(FILAS)] for _ in range(COLUMNAS)]
                global CONJUNTO_SOLUCION
                CONJUNTO_SOLUCION = []

                main(i, j)

                self.assertEqual(len(CONJUNTO_SOLUCION), 64, f"con {i,j}")
                self.assertIn(
                    64, [item for sublist in TABLERO for item in sublist], f"con {i,j}"
                )


def parse_args():
    import argparse

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-c",
        "--check",
        action="store_true",
        help="Activa el modo de prueba.",
    )
    parser.add_argument(
        "-x",
        "--fila",
        type=int,
        default=0,
        help="Determina el valor de la fila en donde empezar.",
    )
    parser.add_argument(
        "-y",
        "--columna",
        type=int,
        default=0,
        help="Determina el valor de la columna en donde empezar.",
    )
    parser.add_argument(
        "-i",
        "--imagen",
        action="store_true",
        help="Genera una imagen del tablero.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.check:
        unittest.main()
    elif args.imagen:
        from ploteo import generar_imagen

        main(args.fila, args.columna)
        print(f"\nEl conjunto solución es: \n {CONJUNTO_SOLUCION}")
        generar_csv()
        generar_imagen()
    else:
        main(args.fila, args.columna)
        print(f"\nEl conjunto solución es: \n {CONJUNTO_SOLUCION}")
