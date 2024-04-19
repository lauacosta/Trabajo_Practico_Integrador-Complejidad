#!/usr/bin/env python
from helpers import total_timer, mostrar_tiempos_ejecución
from array import array
# https://wiki.python.org/moin/TimeComplexity


@total_timer
def potencia_por_cuadrados(base: int, exp: int, mod: int) -> int:
    """
    Calcula base^n en O(log n) multiplicaciones.

    Referencias:
    https://cp-algorithms.com/algebra/binary-exp.html
    https://es.wikipedia.org/wiki/Exponenciaci%C3%B3n_binaria
    """
    result = 1
    base %= mod
    while exp:
        if exp & 1:
            result = result * base % mod
        base = base * base % mod
        exp >>= 1

    return result


@total_timer
def es_compuesto(num: int, a: int, d: int, s: int) -> bool:
    """
    Referencias:
    https://cp-algorithms.com/algebra/primality_tests.html
    """
    x = potencia_por_cuadrados(a, d, num)
    if x == 1 or x == (num - 1):
        return False
    for _ in range(1, s):
        x = x * x % num
        if x == (num - 1):
            return False

    return True


@total_timer
def miller_rabin_deterministico(num: int) -> bool:
    """
    Versión determinística del algoritmo del test de primalidad de Miller-Rabin

    Referencias:
    https://cp-algorithms.com/algebra/primality_tests.html
    https://es.wikipedia.org/wiki/Test_de_primalidad
    """
    if num < 2:
        return False

    r = 0
    d = num - 1

    while (d & 1) == 0:
        d >>= 1
        r += 1

    base = [2, 3, 5, 7]
    for i in base:
        if num == i:
            return True
        if es_compuesto(num, i, d, r):
            return False

    return True


# @timer
def division_tentativa2(num: int) -> tuple[list[int], int]:
    """
    El algoritmo más básico para factorizar un entero en números primos

    Referencias:
    https://cp-algorithms.com/algebra/factorization.html
    """
    ciclos = 0
    lista_factores = []
    # if num == 0:
    #     return lista_factores, ciclos

    for d in [2, 3, 5]:
        while num % d == 0:
            lista_factores.append(d)
            num //= d
            ciclos += 1

        ciclos += 1

    incrementos = array("i", [4, 2, 4, 2, 4, 6, 2, 6])
    i = 0
    for d in range(7, num + 1, incrementos[i]):
        if not d * d <= num:
            break

        while num % d == 0:
            lista_factores.append(d)
            num //= d
            ciclos += 1

        i += 1
        if i == 8:
            i = 0

        ciclos += 1

    if num > 1:
        lista_factores.append(num)

    return lista_factores, ciclos


@total_timer
def division_tentativa(num: int) -> dict[int, int]:
    """
    El algoritmo más básico para factorizar un entero en números primos

    Referencias:
    https://cp-algorithms.com/algebra/factorization.html
    """
    lista_factores = {}
    if num == 0:
        return lista_factores

    while num % 2 == 0:
        lista_factores[2] = lista_factores.get(2, 0) + 1
        num = num // 2

    for n in range(3, num, 2):
        if not n * n <= num:
            break
        while num % n == 0:
            lista_factores[n] = lista_factores.get(n, 0) + 1
            num //= n

    if num > 1:
        lista_factores[num] = lista_factores.get(num, 0) + 1

    return lista_factores


# TODO: Lo que se puede hacer para mejorar el cache es limitar número elementos a los x más recientemente usados.
# Porque la complejidad temporal de la búsqueda en un diccionario es O(n), entonces no conviene tener elementos que no estén siendo útiles.
cache = {}
cache_hits = 0


# @timer
@total_timer
def suma_de_factores_propios_factorizado(num: int) -> int:
    """
    1) Obtener los factores a través de una tecnica de factorización.
    2) Encontrar todas las combinaciones de los factores con sus exponentes.
    3) Realizar la sumatoria de los resultados de cada combinación excepto la primera.

    Referencias:
    - https://planetmath.org/formulaforsumofdivisors
    """
    if num in cache:
        global cache_hits
        cache_hits += 1
        return cache[num]

    factores = division_tentativa(num)
    result = 1
    for n, e in factores.items():
        result *= (pow(n, e + 1) - 1) / (n - 1)

    result = int(result - num)
    cache[num] = result
    return result


# Podríamos guardar un registros de las sumas de las secuencias que efectivamente son de numeros sociables.
# Así cuando entra un número buscamos si ya fue generado dentro de una secuencia sociable.
# Habría que implementar y ver cual alternativa es más rápida.
@total_timer
def construir_sucesion(start: int, num: int, arr: list[int]) -> tuple[bool, list[int]]:
    """
    Devuelve verdadero o falso dependiendo si la sucesión, en donde cada término es la suma
    de los divisores propios del término anterior, es infinita.

    Referencias:
    - https://djm.cc/sociable.txt
    """
    max_iteraciones = 30
    while max_iteraciones != 0:
        sum = suma_de_factores_propios_factorizado(num)

        # Si es así, significa que se cumplió el periodo, entonces devuelvo la lista.
        if sum == start:
            return True, arr

        # Para detectar si una secuencia se vuelve cíclica pero no respecto al primer número.
        if sum in arr:
            return False, arr

        arr.append(sum)
        num = sum
        max_iteraciones -= 1

    return False, arr


@total_timer
def serie_de_numeros_sociables(num: int, arr: list[int]) -> tuple[bool, list[int]]:
    """
    Realiza un control de si el número es primo para así ahorrar operaciones.

    De no ser primo, buscará encontrar si el número tiene una sucesión alícuota.

    Referencias:
    - https://es.wikipedia.org/wiki/N%C3%BAmeros_sociables
    - https://es.wikipedia.org/wiki/Sucesi%C3%B3n_al%C3%ADcuota

    """
    if miller_rabin_deterministico(num):
        return False, arr

    arr.append(num)
    a, b = construir_sucesion(num, num, arr)
    return a, b
    # return construir_sucesion(num, num, arr)


@total_timer
def main():
    limite = 20000000
    for num in range(12496, limite + 1):
        es_candidato, arr = serie_de_numeros_sociables(num, [])
        if es_candidato:
            # if len(arr) == 2:
            # print(f"El número {num} es un número amigo. {arr}")
            # elif len(arr) >= 3:
            if len(arr) >= 3:
                print(f"El número {num} es un número sociable.")

    print("---------------------------------------")
    print(f"Los numeros sociales hasta {limite}:")
    print(f"  Total cache hits: {cache_hits}")
    print(f"  Total cache length: {len(cache)}")


if __name__ == "__main__":
    main()
    mostrar_tiempos_ejecución()
