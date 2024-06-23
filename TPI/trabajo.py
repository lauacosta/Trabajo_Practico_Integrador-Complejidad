import sys
from tabulate import tabulate
# Un viajante tiene que llegar de la ciudad A a la ciudad B, con un tanque de nafta de tamaño C,
# que es la maxima capacidad en litros del tanque de combustible. Entre la ciudad A y la ciudad B hay N estaciones de servicio,
# cada una con un precio de nafta asociado, y en cada estacion de servicio el viajante puede llenar el tanque.
# Sabemos la distancia que hay entre la ciudad A y la primera estacion de servicio, entre la ciudad B y la estacion de servicio N,
# y entre cada una de las estaciones de servicio. El viajante quiere parar lo menos posible a cargar nafta y parar
# en las estaciones más baratas, por lo tanto, queremos minimizar la cantidad de paradas y el gasto al minimo posible para llegar de la ciudad A a la ciudad B.

CAPACIDAD_TANQUE = 100


# Heuristica: Desde la posición actual busco cual es la estación más lejana que puedo alcanzar
# con la capacidad de mi tanque. Entre las estaciónes dentro de ese alcance, selecciono la que tiene el costo minimo
def greedy_impl(opciones: list[tuple[int, int]], seleccion: list[tuple[int, int]]):
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
            # capacidad_en_mejor_caso = capacidad_tanque

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


def main():
    # estaciones = [
    #     (0, 0),
    #     (50, 100),
    #     (100, 60),
    #     (180, 50),
    #     (200, 100),
    #     (250, 50),
    #     (300, 0),
    # ]

    # estaciones = [
    #     (0, 0),
    #     (50, 25),
    #     (80, 30),
    #     (100, 50),
    #     (120, 29),
    #     (200, 0),
    # ]

    estaciones = [
        (0, 0),
        (50, 20),
        (80, 70),
        (100, 75),
        (180, 60),
        (200, 0),
    ]

    total_cost, seleccion = greedy_impl(estaciones, [])
    tabla = [
        ["Numero de paradas", len(seleccion)],
        ["Costo total", total_cost],
        ["Paradas tomadas", seleccion],
    ]
    print(f"GREEDY:\n{tabulate(tabla,tablefmt="simple_grid")}")

    mejor_gasto, mejor_seleccion = backtracking_impl(
        0,
        estaciones,
        0,
        [],
        CAPACIDAD_TANQUE,
        [],
        sys.maxsize,
    )

    tabla = [
        ["Numero de paradas", len(mejor_seleccion)],
        ["Costo total", mejor_gasto],
        ["Paradas tomadas", mejor_seleccion],
    ]
    print(f"BACKTRACKING:\n{tabulate(tabla,tablefmt="simple_grid")}")


if __name__ == "__main__":
    main()
