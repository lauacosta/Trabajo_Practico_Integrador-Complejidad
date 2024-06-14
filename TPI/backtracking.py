import sys

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
    file,
):
    if idx == len(opciones) - 1:
        if mejor_gasto >= gasto and mejor_cantidad >= cantidad_paradas:
            mejor_gasto = gasto
            mejor_cantidad = cantidad_paradas
            mejor_seleccion = paradas_realizadas[:]
            capacidad_en_mejor_caso = capacidad_tanque

        return mejor_gasto, mejor_cantidad, mejor_seleccion, capacidad_en_mejor_caso

    distancia = opciones[idx + 1][0] - opciones[idx][0]

    if distancia > capacidad_tanque:
        return mejor_gasto, mejor_cantidad, mejor_seleccion, capacidad_en_mejor_caso

    print(
        f"Tramo: {opciones[idx][0]} -> {opciones[idx+1][0]}, Distancia: {distancia}, Capacidad luego: {capacidad_tanque-distancia}"
    )

    file.write(
        f'"({capacidad_tanque},{cantidad_paradas},{gasto})" -> "({capacidad_tanque-distancia},{cantidad_paradas},{gasto})"\n'
    )
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
            file,
        )
    )

    modelo_actual = opciones[idx]
    paradas_realizadas.append(modelo_actual)

    file.write(
        f'"({capacidad_tanque},{cantidad_paradas},{gasto})" -> "(200,{cantidad_paradas+1},{gasto + modelo_actual[1]})"\n'
    )
    mejor_gasto, mejor_cantidad, mejor_seleccion, capacidad_en_mejor_caso = (
        backtracking(
            idx + 1,
            opciones,
            gasto + modelo_actual[1],
            cantidad_paradas + 1,
            paradas_realizadas,
            200,
            mejor_seleccion,
            mejor_gasto,
            mejor_cantidad,
            capacidad_en_mejor_caso,
            file,
        )
    )
    paradas_realizadas.pop()
    return mejor_gasto, mejor_cantidad, mejor_seleccion, capacidad_en_mejor_caso


def main():
    try:
        with open("viaje.dot", "w") as file:
            file.write("digraph nose{\n")
            file.write("  node [shape=box];\n")
            distancia_con_costo = [
                (0, 0),
                (50, 100),
                (100, 60),
                (180, 50),
                (200, 100),
                (250, 50),
                (300, 0),
            ]
            capacidad = 200
            mejor_gasto, mejor_cantidad, mejor_seleccion, capacidad_tanque = (
                backtracking(
                    0,
                    distancia_con_costo,
                    0,
                    0,
                    [],
                    capacidad,
                    [],
                    sys.maxsize,
                    sys.maxsize,
                    0,
                    file,
                )
            )
            print(f"Mejor gasto: {mejor_gasto}")
            print(f"Mejor_cantidad: {mejor_cantidad}")
            print(
                f"Capacidad final del tanque: {capacidad_tanque}"
            )  # FIXME: Revisar porque tendría que ser 130 no 100.
            print(f"Mejor_seleccion: {mejor_seleccion}")

            file.write("}\n")
    except Exception as e:
        print(f"Error creando archivo: {e}")
        exit(1)

if __name__ == "__main__":
    main()
