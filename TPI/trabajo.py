"""
GRUPO 2 - FutbolSabadoALas21
 Acosta Quintana, Lautaro
 Aguirre, Amilcar
 Niveyro, Iván
 Stegmayer, Tobías
 Vallejos, Enzo

Problema:
    un viajante tiene que llegar de la ciudad “A” la ciudad “B”, con un tanque de combustible de tamaño “C” (máxima capacidad, en litros, del tanque de combustible). Entre ambas ciudades hay N estaciones de servicio,
    cada una con un precio de combustible asociado, en donde el viajante puede parar para cargar por completo el tanque. Tenemos como información de cada estación de servicio la distancia relativa a la ciudad “A”.

    La solución requiere determinar la cantidad de paradas en estaciones de servicio que el viajante deberá realizar si quiere minimizar la cantidad de paradas y el gasto total para llegar a la ciudad “B”.
    Hay que tener en cuenta que el costo total cargado varia dependiendo cuanto combustible queda en el tanque cuando paramos a cargar, entonces se carga lo necesario para llenar el tanque.
"""

import sys
from tabulate import tabulate


def greedy_impl(opciones: list[tuple[int, int]], seleccion: list[tuple[int, int]]):
    """
    Heuristica: Desde la posición actual busco cual es la estación más lejana que puedo alcanzar con la capacidad de mi tanque.
    Entre las estaciónes dentro de ese alcance, selecciono la que tiene el costo minimo.
    """
    pos_actual = 0
    costo_total = 0
    n = len(opciones)

    while pos_actual < n - 1:
        costo_min = float("inf")
        sig_pos = 0

        for i in range(pos_actual + 1, n):
            if opciones[i][0] - opciones[pos_actual][0] <= CAPACIDAD_TANQUE:
                if opciones[i][1] <= costo_min:
                    costo_min = opciones[i][1]
                    sig_pos = i
            else:
                # En este punto todo el resto de distancias ya estarían fuera de mi alcance.
                break

        # Si no es el final, entonces paré en una estación
        if sig_pos < n - 1:
            opcion = opciones[sig_pos]
            seleccion.append(opcion)
            costo_total += costo_min * (opciones[sig_pos][0] - opciones[pos_actual][0])

        pos_actual = sig_pos

    return costo_total, seleccion


def backtracking_impl(
    idx: int,
    opciones: list[tuple[int, int]],
    gasto: float,
    paradas_realizadas: list[tuple[int, int]],
    capacidad_tanque: int,
    mejor_seleccion: list[tuple[int, int]],
    aux_minimo_gasto: float,
):
    if idx == len(opciones) - 1:
        if aux_minimo_gasto > gasto:
            aux_minimo_gasto = gasto
            mejor_seleccion = paradas_realizadas[:]

        return aux_minimo_gasto, mejor_seleccion

    distancia = opciones[idx + 1][0] - opciones[idx][0]
    if distancia > capacidad_tanque:
        return aux_minimo_gasto, mejor_seleccion

    aux_minimo_gasto, mejor_seleccion = backtracking_impl(
        idx + 1,
        opciones,
        gasto,
        paradas_realizadas,
        capacidad_tanque - distancia,
        mejor_seleccion,
        aux_minimo_gasto,
    )

    paradas_realizadas.append(opciones[idx + 1])

    litros_por_cargar = CAPACIDAD_TANQUE - capacidad_tanque + distancia
    gasto_recarga = gasto + opciones[idx + 1][1] * (litros_por_cargar)

    aux_minimo_gasto, mejor_seleccion = backtracking_impl(
        idx + 1,
        opciones,
        gasto_recarga,
        paradas_realizadas,
        CAPACIDAD_TANQUE,
        mejor_seleccion,
        aux_minimo_gasto,
    )

    paradas_realizadas.pop()

    return aux_minimo_gasto, mejor_seleccion


def dinamica_impl(
    idx: int,
    opciones: list[tuple[int, int]],
    gasto: float,
    paradas_realizadas: list[tuple[int, int]],
    capacidad_tanque: int,
    mejor_seleccion: list[tuple[int, int]],
    aux_minimo_gasto: float,
    memo,
):
    aux = (idx, capacidad_tanque, len(paradas_realizadas))

    if aux in memo:
        return memo[aux]

    if idx == len(opciones) - 1:
        if aux_minimo_gasto > gasto:
            aux_minimo_gasto = gasto
            mejor_seleccion = paradas_realizadas[:]

        return aux_minimo_gasto, mejor_seleccion

    distancia = opciones[idx + 1][0] - opciones[idx][0]
    if distancia > capacidad_tanque:
        return aux_minimo_gasto, mejor_seleccion

    aux_minimo_gasto, mejor_seleccion = dinamica_impl(
        idx + 1,
        opciones,
        gasto,
        paradas_realizadas,
        capacidad_tanque - distancia,
        mejor_seleccion,
        aux_minimo_gasto,
        memo,
    )

    paradas_realizadas.append(opciones[idx + 1])

    litros_por_cargar = CAPACIDAD_TANQUE - capacidad_tanque + distancia
    gasto_recarga = gasto + opciones[idx + 1][1] * (litros_por_cargar)

    aux_minimo_gasto, mejor_seleccion = dinamica_impl(
        idx + 1,
        opciones,
        gasto_recarga,
        paradas_realizadas,
        CAPACIDAD_TANQUE,
        mejor_seleccion,
        aux_minimo_gasto,
        memo,
    )

    paradas_realizadas.pop()

    memo[aux] = (aux_minimo_gasto, mejor_seleccion)
    return aux_minimo_gasto, mejor_seleccion


CAPACIDAD_TANQUE = 100


def main():
    estaciones = [
        (0, 0),
        (50, 100),
        (100, 60),
        (180, 50),
        (200, 100),
        (250, 50),
        (300, 0),
    ]

    # estaciones = [
    #     (0, 0),
    #     (50, 25),
    #     (80, 30),
    #     (100, 50),
    #     (120, 29),
    #     (200, 0),
    # ]

    # estaciones = [
    #     (0, 0),
    #     (50, 20),
    #     (80, 70),
    #     (100, 75),
    #     (180, 60),
    #     (200, 0),
    # ]

    total_cost, seleccion = greedy_impl(estaciones, [])
    tabla = [
        ["Numero de paradas", len(seleccion)],
        ["Costo total", total_cost],
        ["Paradas tomadas", seleccion],
    ]
    print(f"GREEDY:\n{tabulate(tabla,tablefmt="simple_grid")}")

    mejor_gasto, mejor_seleccion = backtracking_impl(
        idx=0,
        opciones=estaciones,
        gasto=0,
        paradas_realizadas=[],
        capacidad_tanque=CAPACIDAD_TANQUE,
        mejor_seleccion=[],
        aux_minimo_gasto=sys.maxsize,
    )

    tabla = [
        ["Numero de paradas", len(mejor_seleccion)],
        ["Costo total", mejor_gasto],
        ["Paradas tomadas", mejor_seleccion],
    ]
    print(f"BACKTRACKING:\n{tabulate(tabla,tablefmt="simple_grid")}")

    mejor_gasto, mejor_seleccion = dinamica_impl(
        idx=0,
        opciones=estaciones,
        gasto=0,
        paradas_realizadas=[],
        capacidad_tanque=CAPACIDAD_TANQUE,
        mejor_seleccion=[],
        aux_minimo_gasto=sys.maxsize,
        memo={},
    )
    tabla = [
        ["Numero de paradas", len(mejor_seleccion)],
        ["Costo total", mejor_gasto],
        ["Paradas tomadas", mejor_seleccion],
    ]
    print(f"Dinamica:\n{tabulate(tabla,tablefmt="simple_grid")}")


if __name__ == "__main__":
    main()
