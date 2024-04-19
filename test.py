import unittest
from math import sqrt
from helpers import timer


# TODO: Bug, devuelve también números que no son primos!
@timer
def criba_erathosthenes(num: int) -> list[int]:
    if num == 0 or num == 1:
        return []

    es_primo = [True for _ in range(num + 1)]
    es_primo[0] = es_primo[1] = False
    for i in range(2, num + 1):
        if i & 1 == 0:
            continue

        if es_primo[i] and i * i <= num:
            for j in range(i * i, num + 1, i):
                if j <= num:
                    es_primo[j] = False

    result = []
    count = 0
    for i in es_primo:
        if i:
            result.append(count)
        count += 1

    return result


def division_tentativa3(num: int) -> list[int]:
    """
    El algoritmo más básico para factorizar un entero en números primos

    Referencias:
    https://cp-algorithms.com/algebra/factorization.html
    """
    factores = []
    for d in criba_erathosthenes(int(sqrt(num))):
        if d * d > num:
            break
        while num % d == 0:
            factores.append(d)
            num //= d

    if num > 1:
        factores.append(num)

    return factores


def division_tentativa(num: int) -> list[int]:
    """
    El algoritmo más básico para factorizar un entero en números primos

    Referencias:
    https://cp-algorithms.com/algebra/factorization.html
    """

    factores = []
    for n in range(2, num):
        if not n * n <= num:
            break

        while num % n == 0:
            factores.append(n)
            num //= n

    if num > 1:
        factores.append(num)

    return factores


def division_tentativa2(num: int) -> list[int]:
    """
    El algoritmo más básico para factorizar un entero en números primos

    Referencias:
    https://cp-algorithms.com/algebra/factorization.html
    """

    factores = []
    if num == 0:
        return factores

    while num % 2 == 0:
        factores.append(2)
        num //= 2

    for n in range(3, num, 2):
        if not n * n <= num:
            break
        while num % n == 0:
            factores.append(n)
            num //= n

    if num > 1:
        factores.append(num)

    return factores


def lista_de_factores_propios(num):
    result = []
    for i in range(1, num - 1):
        if num % i == 0:
            result.append(i)

    return result


def suma_de_factores_propios_fuerza_bruta(num: int) -> int:
    """
    Esta es la solución más facil pero también la más lenta.
    """
    result = 0
    for i in range(1, num):
        if num % i == 0:
            result += i

    return result


# @timer
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


# @timer
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


# @timer
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


# def suma_de_factores_propios_factorizado(num: int) -> int:
#     """
#         1) Obtener los factores a través de una tecnica de factorización.
#         2) Encontrar todas las combinaciones de los factores con sus exponentes.
#         3) Realizar la sumatoria de los resultados de cada combinación excepto la primera.

#         Referencias:
#         - https://planetmath.org/formulaforsumofdivisors
#     """

#     factores = division_tentativa(num)
#     numeros = {}
#     for n in factores:
#         numeros[n] = numeros.get(n, 0) + 1

#     exponentes = list(numeros.values())
#     numeros_unicos = list(numeros.keys())

#     result = 1
#     for n, e in zip(numeros_unicos, exponentes):
#         result *= (pow(n, e+1) - 1) / (n-1)

#     return int(result - num)


def suma_de_factores_propios_factorizado(num: int) -> int:
    """
    1) Obtener los factores a través de una tecnica de factorización.
    2) Encontrar todas las combinaciones de los factores con sus exponentes.
    3) Realizar la sumatoria de los resultados de cada combinación excepto la primera.

    Referencias:
    - https://planetmath.org/formulaforsumofdivisors
    """

    factores = division_tentativa(num)
    numeros = {}
    for n in factores:
        numeros[n] = numeros.get(n, 0) + 1

    # exponentes = list(numeros.values())
    # numeros_unicos = list(numeros.keys())

    result = 1
    for n, e in numeros.items():
        result *= (pow(n, e + 1) - 1) / (n - 1)

    # for n, e in zip(numeros_unicos, exponentes):
    #     result *= (pow(n, e+1) - 1) / (n-1)

    return int(result - num)


def construir_sucesion(start: int, num: int, arr: list[int]) -> tuple[bool, list[int]]:
    """
    Devuelve verdadero o falso dependiendo si la sucesión, en donde cada término es la suma
    de los divisores propios del término anterior, es infinita.
    """
    # sum = suma_de_factores_propios_fuerza_bruta(num)
    sum = suma_de_factores_propios_factorizado(num)

    # Si es así, significa que se cumplió el periodo, entonces devuelvo la lista.
    if sum == start:
        return True, arr

    # Definir si es correcto
    if sum in arr:
        return False, arr

    arr.append(sum)
    return construir_sucesion(start, sum, arr)


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
    return construir_sucesion(num, num, arr)


class TestearFunciones(unittest.TestCase):
    def test_lista_de_factores_primos_1264460(self):
        factos = lista_de_factores_propios(1264460)
        self.assertEqual(
            factos,
            [
                1,
                2,
                4,
                5,
                10,
                17,
                20,
                34,
                68,
                85,
                170,
                340,
                3719,
                7438,
                14876,
                18595,
                37190,
                63223,
                74380,
                126446,
                252892,
                316115,
                632230,
            ],
        )

    def test_suma_de_factores_primos_1264460_fuerza_bruta(self):
        factos = suma_de_factores_propios_fuerza_bruta(1264460)
        self.assertEqual(factos, 1547860)

    def test_suma_de_factores_primos_1264460_factorizado(self):
        factos = suma_de_factores_propios_factorizado(1264460)
        self.assertEqual(factos, 1547860)

    def test_suma_de_factores_primos_1264460_factorizado2(self):
        factos = suma_de_factores_propios_factorizado(45946)
        self.assertEqual(factos, 22976)

        factos = suma_de_factores_propios_factorizado(486178)
        self.assertEqual(factos, 469028)

        factos = suma_de_factores_propios_factorizado(469028)
        self.assertEqual(factos, 486178)

        factos = suma_de_factores_propios_factorizado(503056)
        self.assertEqual(factos, 514736)

        factos = suma_de_factores_propios_factorizado(514736)
        self.assertEqual(factos, 503056)

    def test_serie_de_numeros_sociables_1264460_factorizado(self):
        _, arr = serie_de_numeros_sociables(1264460, [])
        self.assertEqual(arr, [1264460, 1547860, 1727636, 1305184])

    def test_division_tentativa_1264460_1(self):
        self.assertEqual(division_tentativa(1264460), [2, 2, 5, 17, 3719])

    def test_division_tentativa_1264460_2(self):
        self.assertEqual(division_tentativa2(1264460), [2, 2, 5, 17, 3719])

    def test_division_tentativa_1264460_3(self):
        self.assertEqual(division_tentativa3(1264460), [2, 2, 5, 17, 3719])


if __name__ == "__main__":
    unittest.main()
