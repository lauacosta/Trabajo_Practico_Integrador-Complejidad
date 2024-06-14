# Un viajante tiene que llegar de la ciudad A a la ciudad B, con un tanque de nafta de tamaño C,
# que es la maxima capacidad en litros del tanque de combustible. Entre la ciudad A y la ciudad B hay N estaciones de servicio,
# cada una con un precio de nafta asociado, y en cada estacion de servicio el viajante puede llenar el tanque.
# Sabemos la distancia que hay entre la ciudad A y la primera estacion de servicio, entre la ciudad B y la estacion de servicio N,
# y entre cada una de las estaciones de servicio. El viajante quiere parar lo menos posible a cargar nafta y parar
# en las estaciones más baratas, por lo tanto, queremos minimizar la cantidad de paradas y el gasto al minimo posible para llegar de la ciudad A a la ciudad B.


# Heuristica: Desde la posición actual busco cual es la estación más lejana que puedo alcanzar
# con la capacidad de mi tanque. Entre las estaciónes dentro de ese alcance, selecciono la que tiene el costo minimo
def min_paradas_min_costo(
    distancias: list[int], costos: list[int], capacidad: int
) -> tuple[int, float]:
    pos_actual = 0
    cant_paradas = 0
    costo_total = 0
    n = len(distancias)

    while pos_actual < n - 1:
        costo_min = float("inf")
        sig_pos = 0

        for i in range(pos_actual + 1, n):
            if distancias[i] - distancias[pos_actual] <= capacidad:
                if costos[i] <= costo_min:
                    costo_min = costos[i]
                    sig_pos = i
            else:
                # En este punto todo el resto de distancias ya estarían fuera de mi alcance.
                break

        # Si no es el final, entonces paré en una estación
        if sig_pos < n - 1:
            cant_paradas += 1
            print(f"parada: {distancias[sig_pos]}, costo: {costo_min}")
            costo_total += (
                costo_min * (distancias[sig_pos] - distancias[pos_actual]) / capacidad
            )

        pos_actual = sig_pos

    return cant_paradas, costo_total


def main():
    distancias = [
        0,
        50,
        100,
        180,
        200,
        250,
        300,
    ]  # Distancias de cada estación, relativas a la posicion incial. El ultimo elemento es el destino.
    costos = [
        0,
        100,
        60,
        50,
        100,
        50,
        0,
    ]  # Costo de la nafta por litro en cada estación.
    capacidad = 200  # Capacidad máxima de combustible
    paradas, total_cost = min_paradas_min_costo(distancias, costos, capacidad)
    print(f"Numero de paradas: {paradas}, Costo total: {total_cost}")


if __name__ == "__main__":
    main()
