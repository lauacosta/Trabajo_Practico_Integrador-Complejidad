#!/usr/bin/env python
from abc import ABC, abstractmethod
from math import gcd, sqrt

from helpers import Cache, format_n, mostrar_tiempos_ejecución, total_timer

# MATERIAL DE INTERES:
# https://wiki.python.org/moin/TimeComplexity
# https://www.python.org/doc/essays/list2str/
# https://wiki.python.org/moin/PythonSpeed/PerformanceTips#Loops

class AlgoritmoFactorizacion(ABC):
    @abstractmethod
    def factorizar(self, num: int) -> dict[int, int]:
        pass

class DivisionTentativa(AlgoritmoFactorizacion):
    @total_timer
    def factorizar(self, num: int) -> dict[int, int]:
        """
        El algoritmo más básico para factorizar un entero en números primos

        Referencias:
        https://cp-algorithms.com/algebra/factorization.html
        """
        lista_factores = {}
        if num == 0:
            return lista_factores

        for d in [2, 3, 5]:
            while num % d == 0:
                lista_factores[d] = lista_factores.get(d, 0) + 1
                num //= d

        incrementos = [4, 2, 4, 2, 4, 6, 2, 6]
        i = 0
        d = 7
        while d * d <= num:
            while num % d == 0:
                lista_factores[d] = lista_factores.get(d, 0) + 1
                num //= d

            d += incrementos[i]
            i += 1

            if i == 8:
                i = 0

        if num > 1:
            lista_factores[num] = lista_factores.get(num, 0) + 1

        return lista_factores


class DivisionTentativaPrimos(AlgoritmoFactorizacion):
    def __init__(self, lista_primos: list[int]):
        self.lista_primos = lista_primos

    @total_timer
    def factorizar(self, num: int) -> dict[int,int]:
        """
        El algoritmo más básico para factorizar un entero en números primos

        Referencias:
        https://cp-algorithms.com/algebra/factorization.html
        """
        techo = int(sqrt(num))
        lista_primos_efectiva = self.lista_primos[:techo]
        lista_factores = {}
        if num == 0 or num == 1:
            return lista_factores

        for p in lista_primos_efectiva:
            if p * p > num:
                break

            while num % p == 0:
                lista_factores[p] = lista_factores.get(p, 0) + 1
                num //= p
        
        if num > 1:
            lista_factores[num] = lista_factores.get(num, 0) + 1

        return lista_factores



class BrentPollardPrime(AlgoritmoFactorizacion):
    @total_timer
    def factorizar(self, num: int) -> dict[int, int]:
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


                else:
                    factor = division_tentativa(m) if m < 100 else brent_pollard(m)
                    lista_factores.append(m // factor)
                    lista_factores.append(factor)


            return lista_factores_primos

@total_timer
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

    ## Hasta que no encuentre una mejor solución así se queda.
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

    print(result)
    return result

@total_timer
def brent_pollard(n, x0=2, c=1):
    @total_timer
    def f(x, c, mod):
        return (mult(x, x, mod) + c) % mod


    @total_timer
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

class App:
    def __init__(self, limite: int, periodo: int, algoritmo: AlgoritmoFactorizacion):
        self.limite = limite
        self.periodo = periodo
        self.algoritmo_de_factorizacion = algoritmo
        self.cache_suma_factores = Cache()

        # Realmente está ad hoc para representar al único conjunto de numeros sociables de periodo 28.
        self.numeros_sociables_especiales = set()

    @total_timer
    def run(self):
        """
        Referencias:
        - https://djm.cc/sociable.txt
        """
        actual = 0
        nro_sucesion = 1
        try:
            for num in range(1, self.limite + 1):
                es_candidato, sucesion = self.sucesion_de_numeros_sociables(num, [])
                if es_candidato:
                    if len(sucesion) >= self.periodo:
                        print(f"{format_n(nro_sucesion):2}  {format_n(sucesion[0]):6}")
                        for n in sucesion[1:]:
                            print(f"    {format_n(n)}")

                        print("")
                        nro_sucesion += 1
                actual = num

            print("---------------------------------------")
            print(f"Los numeros sociales hasta {format_n(actual)}:")

        except KeyboardInterrupt:
            print("---------------------------------------")
            print(
                f"Ejecución interrumpida, los numeros sociales hasta {format_n(actual)}:"
            )

        finally:
            print(
                f"  Elementos en el self.cache_suma_factores: {format_n(len(self.cache_suma_factores))}"
            )
            print(f"  Cache refs: {format_n(self.cache_suma_factores.cache_refs)}")
            print(
                f"  Cache hits: {format_n(self.cache_suma_factores.cache_hits)} ({((self.cache_suma_factores.cache_hits / self.cache_suma_factores.cache_refs) * 100):1.3f}%)"
            )
            print("")
            print(
                f"  Elementos en el cache_numeros_sociables: {format_n(len(self.numeros_sociables_especiales))}"
            )

    @total_timer
    def sucesion_de_numeros_sociables(
        self, num: int, arr: list[int]
    ) -> tuple[bool, list[int]]:
        """
        Realiza un control de si el número es primo para así ahorrar operaciones.

        De no ser primo, buscará encontrar si el número tiene una sucesión alícuota.

        Referencias:
        - https://es.wikipedia.org/wiki/N%C3%BAmeros_sociables
        - https://es.wikipedia.org/wiki/Sucesi%C3%B3n_al%C3%ADcuota

        """
        # No significa que los numeros no sean sociables sino que ya fueron mostrados por pantalla.
        # El porcentaje de hits es terriblemente bajo y por sí solo apenas reduce el tiempo de ejecución, incluso lo sube.
        # La ventaja es que me permite determinar la maxima cantidad de iteraciones al construir la sucesion a 10 porque no evaluará
        # El resto de numeros dentro de la sucesión formada por 14316 y eso reduce muchísimo el tiempo de ejecución.
        # Estaría bueno encontrar otra manera de mantener el formato de salida y la cantidad de iteraciones a 10.
        if num in self.numeros_sociables_especiales:
            return False, arr

        # if miller_rabin_deterministico(num):
        #     return False, arr

        arr.append(num)
        es_candidato, sucesion = self.construir_sucesion(num, num, arr)
        if es_candidato and len(sucesion) >= self.periodo:
            for n in sucesion:
                self.numeros_sociables_especiales.add(n)

        return es_candidato, sucesion

    @total_timer
    def construir_sucesion(
        self, start: int, num: int, arr: list[int]
    ) -> tuple[bool, list[int]]:
        """
        Devuelve verdadero o falso dependiendo si la sucesión, en donde cada término es la suma
        de los divisores propios del término anterior, es infinita.

        Referencias:
        - https://djm.cc/sociable.txt
        """

        if num == 14316:
            max_iteraciones = 30
        else:
            max_iteraciones = 10
        while max_iteraciones != 0:
            sum = self.suma_de_factores_propios_factorizado(num)

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
    def suma_de_factores_propios_factorizado(self, num: int) -> int:
        """
        1) Obtener los factores a través de una tecnica de factorización.
        2) Encontrar todas las combinaciones de los factores con sus exponentes.
        3) Realizar la sumatoria de los resultados de cada combinación excepto la primera.

        Referencias:
        - https://planetmath.org/formulaforsumofdivisors
        """
        self.cache_suma_factores.cache_refs += 1
        if num in self.cache_suma_factores:
            return self.cache_suma_factores[num]

        factores = self.algoritmo_de_factorizacion.factorizar(num)
        result = 1
        for n, e in factores.items():
            result *= (pow(n, e + 1) - 1) / (n - 1)

        result = int(result - num)
        self.cache_suma_factores[num] = result
        return result


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

def sociables(app: App):
    app.run()

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
        help="Determina el tamaño de la entrada.",
    )
    parser.add_argument(
        "-p",
        "--periodo",
        type=int,
        default=1,
        help="Determina el periodo a buscar.",
    )
    parser.add_argument(
        "-a",
        "--algoritmo",
        type=str,
        help="Determina el algoritmo de factorización a usar.",
    )
    args = parser.parse_args()

    if args.algoritmo == "div":
        sociables(App(args.entrada, args.periodo, DivisionTentativa()))
    elif args.algoritmo == "div2":
        sociables(App(args.entrada, args.periodo, DivisionTentativaPrimos(criba_eratosthenes(args.entrada))))
    elif args.algoritmo == "brent":
        sociables(App(args.entrada, args.periodo, BrentPollardPrime()))
    else:
        print("algoritmo desconocido")

    mostrar_tiempos_ejecución()
