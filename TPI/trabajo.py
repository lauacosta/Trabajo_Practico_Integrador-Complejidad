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
def min_paradas_min_costo(opciones: list[tuple[int, int]], seleccion: list[tuple[int,int]]):
    pos_actual = 0
    cant_paradas = 0
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
            cant_paradas += 1
            opcion = opciones[sig_pos]
            seleccion.append(opcion)
            costo_total += (
                costo_min
                * (opciones[sig_pos][0] - opciones[pos_actual][0])
                / CAPACIDAD_TANQUE
            )

        pos_actual = sig_pos

    return cant_paradas, costo_total, seleccion


PARE = False
def backtracking(
    idx: int,
    opciones: list[tuple[int, int]],
    gasto: float,
    cantidad_paradas: int,
    paradas_realizadas: list[tuple[int, int]],
    capacidad_tanque: int,
    mejor_seleccion: list[tuple[int, int]],
    mejor_gasto: float,
    mejor_cantidad: int,
    capacidad_en_mejor_caso: int,
):
    if idx == len(opciones) - 1:
        if mejor_gasto >= gasto and mejor_cantidad >= cantidad_paradas:
            mejor_gasto = gasto  
            mejor_cantidad = cantidad_paradas
            mejor_seleccion = paradas_realizadas[:]
            capacidad_en_mejor_caso = capacidad_tanque

        return mejor_gasto, mejor_cantidad, mejor_seleccion, capacidad_en_mejor_caso

    distancia = opciones[idx + 1][0] - opciones[idx][0]
    # print(f"La distancia entre {opciones[idx + 1][0]} y {opciones[idx][0]} es: {distancia} y mi capacidad es: {capacidad_tanque}")
    # TODO: Revisar el bug, en donde cuando retrocede despues de verificar que no se puede tomar esa ruta
    # añade a la lista de paradas seleccionadas, la parada en donde decide que va a cargar en la siguiente parada y no a dicha siguiente parada.
    # Si probas con una capacidad de 100, va a devolverte [(50, 100), (180, 50)] cuando debería devolverte [(100, 60), (200, 100)]

    if distancia > capacidad_tanque:
        return mejor_gasto, mejor_cantidad, mejor_seleccion, capacidad_en_mejor_caso

    mejor_gasto, mejor_cantidad, mejor_seleccion, capacidad_en_mejor_caso = (
        backtracking(
            idx + 1,
            opciones,
            gasto,
            cantidad_paradas,
            paradas_realizadas,
            capacidad_tanque - distancia,
            mejor_seleccion,
            mejor_gasto,
            mejor_cantidad,
            capacidad_en_mejor_caso,
        )
    )

    modelo_actual = opciones[idx]
    if modelo_actual == (180,50) or modelo_actual == (50,100):
        print("Aca!")
    paradas_realizadas.append(modelo_actual)
     

    mejor_gasto, mejor_cantidad, mejor_seleccion, capacidad_en_mejor_caso = (
        backtracking(
            idx + 1,
            opciones,
            gasto + modelo_actual[1],
            cantidad_paradas + 1,
            paradas_realizadas,
            CAPACIDAD_TANQUE,
            mejor_seleccion,
            mejor_gasto,
            mejor_cantidad,
            capacidad_en_mejor_caso,
        )
    )
    # if not PARE:
    paradas_realizadas.pop()

    return mejor_gasto, mejor_cantidad, mejor_seleccion, capacidad_en_mejor_caso


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

    paradas, total_cost, seleccion = min_paradas_min_costo(estaciones, [])
    tabla = [["Numero de paradas",paradas], ["Costo total", total_cost], ["Paradas tomadas", seleccion]]
    print(f"GREEDY:\n{tabulate(tabla,tablefmt="simple_grid")}")

    mejor_gasto, mejor_cantidad, mejor_seleccion, capacidad_tanque = backtracking(
        0,
        estaciones,
        0,
        0,
        [],
        CAPACIDAD_TANQUE,
        [],
        sys.maxsize,
        sys.maxsize,
        0,
    )
    tabla = [["Numero de paradas",mejor_cantidad], ["Costo total", mejor_gasto],["Capacidad final del tanque", capacidad_tanque], ["Paradas tomadas", mejor_seleccion]]
    print(f"BACKTRACKING:\n{tabulate(tabla,tablefmt="simple_grid")}")


if __name__ == "__main__":
    main()
