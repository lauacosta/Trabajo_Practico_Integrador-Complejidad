#!/usr/bin/env python
from abc import ABC, abstractmethod
from math import gcd, sqrt

maxim = pow(2, 64) - 1


class AlgoritmoFactorizacion(ABC):
    @abstractmethod
    def factorizar(self, num: int) -> tuple[dict[int, int], int]:
        pass


class DivisionTentativa(AlgoritmoFactorizacion):
    def factorizar(self, num: int) -> tuple[dict[int, int], int]:
        """
        El algoritmo más básico para factorizar un entero en números primos

        Referencias:
        https://cp-algorithms.com/algebra/factorization.html
        """
        pasos = 0
        lista_factores = {}
        if num == 0:
            return lista_factores, pasos

        for d in [2, 3, 5]:
            while num % d == 0:
                lista_factores[d] = lista_factores.get(d, 0) + 1
                num //= d
                pasos += 1
            pasos += 1

        incrementos = [4, 2, 4, 2, 4, 6, 2, 6]
        i = 0
        d = 7
        while d * d <= num:
            while num % d == 0:
                lista_factores[d] = lista_factores.get(d, 0) + 1
                num //= d
                pasos += 1

            pasos += 1
            d += incrementos[i]
            i += 1

            if i == 8:
                i = 0

        if num > 1:
            lista_factores[num] = lista_factores.get(num, 0) + 1
            pasos += 1

        return lista_factores, pasos


class DivisionTentativaPrimos(AlgoritmoFactorizacion):
    def __init__(self, lista_primos: list[int]):
        self.lista_primos = lista_primos

    def factorizar(self, num: int) -> tuple[dict[int, int], int]:
        """
        El algoritmo más básico para factorizar un entero en números primos

        Referencias:
        https://cp-algorithms.com/algebra/factorization.html
        """
        pasos = 0
        techo = int(sqrt(num))
        lista_primos_efectiva = self.lista_primos[:techo]
        lista_factores = {}
        if num == 0 or num == 1:
            return lista_factores, pasos

        for p in lista_primos_efectiva:
            if p * p > num:
                break

            while num % p == 0:
                lista_factores[p] = lista_factores.get(p, 0) + 1
                num //= p
                pasos += 1

            pasos += 1

        if num > 1:
            lista_factores[num] = lista_factores.get(num, 0) + 1
            pasos += 1

        return lista_factores, pasos


class BrentPollardPrime(AlgoritmoFactorizacion):
    def factorizar(self, num: int) -> tuple[dict[int, int], int]:
        def division_tentativa(n):
            for i in range(2, int(n**0.5) + 1):
                if n % i == 0:
                    return i
            return n

        if num <= 1:
            return DivisionTentativa().factorizar(num)
        else:
            lista_factores = []
            lista_factores_primos = {}
            factor = brent_pollard_factor(num)
            # factor = brent_pollard(num)
            lista_factores.append(num // factor)
            lista_factores.append(factor)

            while lista_factores:
                m = lista_factores[-1]

                lista_factores.pop()

                if m == 1:
                    continue

                if miller_rabin_deterministico(m):
                    lista_factores_primos[m] = lista_factores_primos.get(m, 0) + 1
                    for i in range(len(lista_factores)):
                        k = lista_factores[i]

                        if k % m == 0:
                            while True:
                                k //= m
                                lista_factores_primos[m] = (
                                    lista_factores_primos.get(m, 0) + 1
                                )
                                if k % m != 0:
                                    break

                            lista_factores[i] = k

                else:
                    factor = (
                        division_tentativa(m) if m < 100 else brent_pollard_factor(m)
                    )
                    # factor = division_tentativa(m) if m < 100 else brent_pollard(m)
                    lista_factores.append(m // factor)
                    lista_factores.append(factor)

            return lista_factores_primos, 0


def mult(a: int, b: int, mod: int) -> int:
    result = 0
    while b:
        if b & 1:
            result = (result + a) % mod

        a = (a + a) % mod
        b >>= 1

    return result


def brent_pollard_factor(n: int):
    import random

    m = 1000
    a = x = y = ys = r = q = g = 0

    while True:
        a = int(random.randint(1, maxim))
        a %= n
        if not (a == 0 or a == n - 2):
            break
    y = int(random.randint(1, maxim)) % n
    r = 1
    q = 1

    while True:
        x = y
        for i in range(r):
            y = mult(y, y, n)
            y += a
            if y < a:
                y += (maxim - n) + 1

            y %= n

        k = 0
        while True:
            i = 0
            while i < m and i < r - k:
                ys = y
                y = mult(y, y, n)
                y += a
                if y < a:
                    y += maxim - n + 1
                y %= n

                q = mult(q, x - y, n) if x > y else mult(q, y - x, n)
                i += 1
            g = gcd(q, n)
            k += m
            if not (k < r and g == 1):
                break

        r <<= 1
        if g != 1:
            break

    if g == n:
        while True:
            ys = mult(ys, ys, n)
            ys += a
            if ys < a:
                ys += maxim - n + 1

            ys %= n
            g = gcd(x - ys, n) if x > ys else gcd(ys - x, n)
            if g != 1:
                break
    return g


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


def bench(func, number: int) -> tuple[float, int]:
    import time

    if miller_rabin_deterministico(number):
        return 0, 0
    start_time = time.time()
    _, pasos = func(number)
    end_time = time.time()

    return end_time - start_time, pasos


def generate_random_number_of_length(length):
    import random

    return int("".join(str(random.randint(0, 9)) for _ in range(length)))


def generar_lista(largos: list[int]) -> list[int]:
    lista = []
    for longitud in largos:
        numero = generate_random_number_of_length(longitud)
        while miller_rabin_deterministico(numero):
            numero = generate_random_number_of_length(longitud)

        lista.append(generate_random_number_of_length(longitud))

    return lista


def pollard(num: int, primes: list[int]):
    import random

    B = 10
    g = 1
    while B <= 1000000 and g < num:
        a = int(2 + random.random() % (num - 3))
        g = gcd(a, num)
        if g > 1:
            return g

        # compute a^M
        for p in primes:
            if p >= B:
                continue
            p_power = 1
            while p_power * p <= B:
                p_power *= p
            a = pow(a, p_power, num)

            g = gcd(a - 1, num)
            if g > 1 and g < num:
                return g
        B *= 2
    return 1


def criba_eratosthenes(num: int) -> list[int]:
    """
    Referencias:
    - https://cp-algorithms.com/algebra/sieve-of-eratosthenes.html
    """
    if num == 0 or num == 1:
        return []

    result = []
    es_primo = [True for _ in range(num + 1)]
    es_primo[0] = False
    es_primo[1] = False
    result.append(2)

    # Hasta que no encuentre una mejor solución así se queda.
    if num == 3:
        result.append(3)
        return result

    for i in range(3, num + 1, 2):
        if not i * i <= num:
            break

        if es_primo[i]:
            result.append(i)
            for j in range(i * i, num + 1, i * 2):
                es_primo[j] = False

    return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-n",
        "--entrada",
        type=int,
        default=1000000,
        help="Determina el tamaño de la entrada, debe ser >= 12496",
    )

    args = parser.parse_args()

    print("nombre tamaño tiempo pasos")
    # for n in range(1, 1000000000, 1000):
    for n in [
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        30,
    ]:
        for _ in range(10):
            a = generar_lista([n])[0]
            tiempo, pasos = bench(DivisionTentativa().factorizar, a)
            print(f"DivisionTentativa {a} {tiempo} {pasos}")

            tiempo, pasos = bench(BrentPollardPrime().factorizar, a)
            print(f"BrentPollardPrime {a} {tiempo} {pasos}")

            # NO ESTA BIEN HECHO
            # tiempo, pasos = bench(DivisionTentativaPrimos(criba_eratosthenes(a)).factorizar, a)
            # print(f"DivisionTentativaPrimos {a} {tiempo} {pasos}")
