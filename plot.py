#!/usr/bin/env python
from abc import ABC, abstractmethod
from math import gcd


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


class BrentPollardPrime(AlgoritmoFactorizacion):
    def factorizar(self, num: int) -> tuple[dict[int, int], int]:
        pasos = 0

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
            factor = brent_pollard(num)
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

                        pasos += 1

                else:
                    factor = division_tentativa(m) if m < 100 else brent_pollard(m)
                    lista_factores.append(m // factor)
                    lista_factores.append(factor)

                pasos += 1

            return lista_factores_primos, pasos


def brent_pollard(n, x0=2, c=1):
    def f(x, c, mod):
        return (mult(x, x, mod) + c) % mod

    def mult(a, b, mod):
        result = 0
        while b:
            if b & 1:
                result = (result + a) % mod

            a = (a + a) % mod
            b >>= 1

        return result

    x = x0
    g = 1
    q = 1
    xs = y = 0

    m = 128
    l = 1

    while g == 1:
        y = x
        i = 1
        while i < l:
            x = f(x, c, n)
            i += 1
        k = 0
        while k < l and g == 1:
            xs = x
            i = 0
            while i < m and i < l - k:
                x = f(x, c, n)
                q = mult(q, abs(y - x), n)
                i += 1
            g = gcd(q, n)
            k += m
        l *= 2
    if g == n:
        xs = f(xs, c, n)
        g = gcd(abs(xs - y), n)
        while g == 1:
            xs = f(xs, c, n)
            g = gcd(abs(xs - y), n)

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
    for l in largos:
        numero = generate_random_number_of_length(l)
        while miller_rabin_deterministico(numero):
            numero = generate_random_number_of_length(l)

        lista.append(generate_random_number_of_length(l))

    return lista


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
    for n in generar_lista([15,16,17,18]):
        for _ in range(10):
            tiempo, pasos = bench(DivisionTentativa().factorizar, n)
            print(f"DivisionTentativa {n} {tiempo} {pasos}")

            tiempo, pasos = bench(BrentPollardPrime().factorizar, n)
            print(f"BrentPollardPrime {n} {tiempo} {pasos}")

