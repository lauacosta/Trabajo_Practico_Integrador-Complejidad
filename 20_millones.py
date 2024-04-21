#!/usr/bin/env python
from abc import ABC, abstractmethod
from helpers import format_n, timer, total_timer, mostrar_tiempos_ejecución, Cache
from math import sqrt
# https://wiki.python.org/moin/TimeComplexity

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

class DivisionTentativa2(AlgoritmoFactorizacion):
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

# TODO: TODAVIA NO FUNCIONA
class DivisionTentativaPrimos(AlgoritmoFactorizacion):
    def factorizar(self, num:int) -> dict[int, int]:
        """
        El algoritmo más básico para factorizar un entero en números primos

        Referencias:
        https://cp-algorithms.com/algebra/factorization.html
        """
        lista_factores = {}
        lista_primos = criba_eratosthenes(int(sqrt(num)))
        if num == 0 or num == 1:
            return lista_factores

        for p in lista_primos:
            if p * p > num:
                break

            while num % p == 0:
                lista_factores[p] = lista_factores.get(p, 0) + 1
                num //= p


        primo_mas_grande = max(lista_primos)
        if num > primo_mas_grande:
            factores = division_tentativa_serial(primo_mas_grande, num)
            for f in factores:
                lista_factores[f] = lista_factores.get(f, 0) + 1

            return lista_factores
        elif num != 1:
            lista_factores[num] = lista_factores.get(num, 0) + 1

        return lista_factores

# TODO: TODAVIA NO FUNCIONA
memo_lista_primos = []
@timer
def criba_eratosthenes_rango(limite: int) -> list[int]:
    """
    Referencias:
    - https://cp-algorithms.com/algebra/sieve-of-eratosthenes.html
    """

    global memo_lista_primos

    if not memo_lista_primos:
        return criba_eratosthenes(limite)
    elif memo_lista_primos[-1] < limite:
        lim = sqrt(int(limite))
        marcas = [False for _ in range(limite + 1)]
        primos = []

        i = 2
        while i <= lim:
            if not marcas[i]:
                primos.append(i)
                j = i * i
                while j <= lim:
                    marcas[j] = True
                    j += i
            i += 1


        nuevos_primos = []

        start = memo_lista_primos[-1]
        es_primo = [True for _ in range(limite - start + 1)]
        for p in primos:
            j = max(p * p, start)
            while j <= limite:
                es_primo[j - start] = False
                j += p

        if start == 1:
            es_primo[0] = False

        for p in range(len(es_primo)):
            if es_primo[p]:
                nuevos_primos.append(p)
        
        print(f"Lista de nuevos primos desde {start} a {limite} : {nuevos_primos}")
        memo_lista_primos += nuevos_primos
        print(f"Nueva lista actualizada: {memo_lista_primos}")
        return memo_lista_primos

    else:
        print(f"No hizo falta actualizar: {memo_lista_primos}")
        return memo_lista_primos
    


# TODO: TODAVIA NO FUNCIONA
def criba_eratosthenes(num: int) -> list[int]:
    """
    Referencias:
    - https://cp-algorithms.com/algebra/sieve-of-eratosthenes.html
    """
    global memo_lista_primos
    if num == 0 or num == 1:
        return []

    result = []
    es_primo = [True for _ in range(num + 1)]
    es_primo[0] = False
    es_primo[1] = False

    i = 2
    while i * i <= num:
        if es_primo[i] == True:
            j = i * i
            while j <= num:
                es_primo[j] = False
                j += i
        i+=1

    for i in range(len(es_primo)):
        if es_primo[i]:
            result.append(i)

    print(f"lista de primos la primera vez: {result}")
    memo_lista_primos = result
    return memo_lista_primos

def division_tentativa_serial(start, end) -> list[int]:
    lista_factores = []
    while end % 2 == 0:
        print("RE LOCO")
        lista_factores.append(2)
        end = end // 2

    for n in range(start, end, 2):
        if not n * n <= end:
            break

        while end % n == 0:
            lista_factores.append(n)
            end //= n

    if end > 1:
        lista_factores.append(end)

    return lista_factores


class App():
    def __init__(self, limite: int, periodo:int, algoritmo: AlgoritmoFactorizacion):
        self.limite = limite
        self.periodo = periodo
        self.algoritmo_de_factorizacion = algoritmo
        self.cache_numeros_sociables = Cache()
        self.cache_suma_factores = Cache()

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
            print(f"Ejecución interrumpida, los numeros sociales hasta {format_n(actual)}:")

        finally:
            print(f"  Elementos en el self.cache_suma_factores: {format_n(len(self.cache_suma_factores))}")
            print(f"  Cache refs: {format_n(self.cache_suma_factores.cache_refs)}")
            print(
                f"  Cache hits: {format_n(self.cache_suma_factores.cache_hits)} ({((self.cache_suma_factores.cache_hits / self.cache_suma_factores.cache_refs) * 100):1.3f}%)"
            )
            print("")
            print(
                f"  Elementos en el cache_numeros_sociables: {format_n(len(self.cache_numeros_sociables))}"
            )
            print(f"  Cache refs: {format_n(self.cache_numeros_sociables.cache_refs)}")
            print(
                f"  Cache hits: {format_n(self.cache_numeros_sociables.cache_hits)} ({((self.cache_numeros_sociables.cache_hits / self.cache_numeros_sociables.cache_refs) * 100):1.3f}%)"
            )

    @total_timer
    def sucesion_de_numeros_sociables(self, num: int, arr: list[int]) -> tuple[bool, list[int]]:
        """
            Realiza un control de si el número es primo para así ahorrar operaciones.

            De no ser primo, buscará encontrar si el número tiene una sucesión alícuota.

            Referencias:
            - https://es.wikipedia.org/wiki/N%C3%BAmeros_sociables
            - https://es.wikipedia.org/wiki/Sucesi%C3%B3n_al%C3%ADcuota

        """
        # No significa que los numeros no sean sociables sino que ya fueron mostrados por pantalla.
        # El porcentaje de hits es terriblemente bajo y por sí solo apenas reduce el tiempo de ejecución, incluso lo sube.
        # La ventaja es que me permite determinar la maxima cantidad de iteraciones a 10 porque no evaluará
        # El resto de numeros de la sucesión de 14316 y eso reduce muchísimo el tiempo de ejecución.
        # Estaría bueno encontrar otra manera de mantener el formato de salida y la cantidad de iteraciones a 10.

        self.cache_numeros_sociables.cache_refs += 1
        if num in self.cache_numeros_sociables:
            self.cache_numeros_sociables.cache_hits += 1
            return False, arr
        if miller_rabin_deterministico(num):
            return False, arr

        arr.append(num)
        es_candidato, sucesion = self.construir_sucesion(num, num, arr)
        if es_candidato and len(sucesion) >= self.periodo:
            for n in sucesion:
                self.cache_numeros_sociables[n] = 0

        return es_candidato, sucesion

    @total_timer
    def construir_sucesion(self, start: int, num: int, arr: list[int]) -> tuple[bool, list[int]]:
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

    if args.algoritmo == "division":
        App(args.entrada, args.periodo, DivisionTentativa()).run()
    elif args.algoritmo == "division2":
        App(args.entrada, args.periodo, DivisionTentativa2()).run()
    else:
        print("algoritmo desconocido")
    
    mostrar_tiempos_ejecución()
    criba_eratosthenes_rango(12451)
    criba_eratosthenes_rango(18445)
