import sys

CAPACIDAD_TANQUE = 100

def backtracking(
    idx: int,
    opciones: list[tuple[int, int]],
    gasto: int,
    cantidad_paradas: int,
    paradas_realizadas: list[tuple[int, int]],
    capacidad_tanque: int,
    mejor_seleccion: list[tuple[int, int]],
    mejor_gasto: int,
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
    print(f"La distancia entre {opciones[idx + 1][0]} y {opciones[idx][0]} es: {distancia} y mi capacidad es: {capacidad_tanque}")
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
    print(f"Mejor gasto: {mejor_gasto}")
    print(f"Mejor_cantidad: {mejor_cantidad}")
    print(
        f"Capacidad final del tanque: {capacidad_tanque}"
    )  # FIXME: Revisar porque tendría que ser 130 no 100.
    print(f"Mejor_seleccion: {mejor_seleccion}")


if __name__ == "__main__":
    main()
