#!/usr/bin/env python
from math import prod

from helpers import Cache, format_n, total_timer, mostrar_tiempos_ejecución

# MATERIAL DE INTERES:
# https://wiki.python.org/moin/TimeComplexity
# https://www.python.org/doc/essays/list2str/
# https://wiki.python.org/moin/PythonSpeed/PerformanceTips#Loops

class App:
    def __init__(self, limite: int, periodo: list[int], lista_primos: list[int]):
        self.limite = limite
        self.periodo = periodo
        self.lista_primos = lista_primos
        self.cache_suma_factores = Cache()

        # Realmente está ad hoc para representar al conjunto de numeros sociables de que ya aparecieron.
        self.numeros_sociables_vistos: set[int] = set()

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
                    if len(sucesion) in self.periodo:
                        print(f"{format_n(nro_sucesion):2}  {format_n(sucesion[0]):6}")
                        for n in sucesion[1:]:
                            print(f"    {format_n(n)}")

                        print("")
                        nro_sucesion += 1
                actual = num

            self.mostrar_informacion(f"Los numeros sociales hasta {format_n(actual)}:")
        except KeyboardInterrupt:
            self.mostrar_informacion(
                f"Ejecución interrumpida, los numeros sociales hasta {format_n(actual)}:"
            )

    #@total_timer
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
        if num in self.numeros_sociables_vistos:
            return False, arr

        arr.append(num)
        es_candidato, sucesion = self.construir_sucesion(num, num, arr)
        if es_candidato and len(sucesion) in self.periodo:
            for n in sucesion:
                self.numeros_sociables_vistos.add(n)
            # add = self.numeros_sociables_vistos.add
            # map(add, sucesion)

        return es_candidato, sucesion

    #@total_timer
    def construir_sucesion(
        self, start: int, num: int, arr: list[int]
    ) -> tuple[bool, list[int]]:
        """
        Devuelve verdadero o falso dependiendo si la sucesión, en donde cada término es la suma
        de los divisores propios del término anterior, es infinita.

        Referencias:
        - https://djm.cc/sociable.txt
        """

        max_iteraciones = self.periodo[-1]
        while max_iteraciones != 0:
            sum = self.suma_de_factores_propios_factorizado(num)

            # Significa que se cumplió el periodo, entonces devuelvo la lista.
            if sum == start:
                return True, arr

            # Detecta si una secuencia se vuelve cíclica pero no respecto al primer número.
            if sum in arr:
                return False, arr

            arr.append(sum)
            num = sum
            max_iteraciones -= 1

        return False, arr

    #@total_timer
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

        factores = DivisionTentativa(num, self.lista_primos)
        serie = [(pow(n, e + 1) - 1) // (n - 1) for n, e in factores.items()]
        result = prod(serie) - num
        self.cache_suma_factores[num] = result
        return result

    def mostrar_informacion(self, titulo: str):
        informacion: list[str] = [
            titulo,
            f"  Elementos en el self.cache_suma_factores: {format_n(len(self.cache_suma_factores))}",
            f"  Cache refs: {format_n(self.cache_suma_factores.cache_refs)}",
            f"  Cache hits: {format_n(self.cache_suma_factores.cache_hits)} ({((self.cache_suma_factores.cache_hits / self.cache_suma_factores.cache_refs) * 100):1.3f}%)",
            f"  Elementos en el cache_numeros_sociables: {format_n(len(self.numeros_sociables_vistos))}"
        ]

        for info in informacion:
            print(info)


# @total_timer
def DivisionTentativa(num: int, lista_primos: list[int]) -> dict[int,int]:
    """
    El algoritmo más básico para factorizar un entero en números primos

    Referencias:
    https://cp-algorithms.com/algebra/factorization.html
    """
    lista_factores: dict[int,int] = {}
    if num == 0 or num == 1:
        return lista_factores

    for p in lista_primos:
        if p * p > num:
            break

        while num % p == 0:
            lista_factores[p] = lista_factores.get(p, 0) + 1
            num //= p
    
    if num > 1:
        lista_factores[num] = lista_factores.get(num, 0) + 1

    return lista_factores

# @total_timer
def criba_eratosthenes(num: int) -> list[int]:
    """
    Encuentra todos los números primos menores a un número natural dado.
    Referencias:
    - https://cp-algorithms.com/algebra/sieve-of-eratosthenes.html
    """
    if num == 0 or num == 1:
        return []

    resultado: list[int] = []
    es_primo = [True for _ in range(num + 1)]
    es_primo[0] = False
    es_primo[1] = False
    resultado.append(2)

    ## Hasta que no encuentre una mejor solución así se queda.
    if num == 3:
        resultado.append(3)
        return resultado

    for i in range(3, num + 1, 2):
        if not i * i <= num:
            break

        if es_primo[i]:
            resultado.append(i)
            for j in range(i * i, num + 1, i * 2):
                es_primo[j] = False

    return resultado

def sociables(app: App):
    app.run()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    _ = parser.add_argument(
        "-n",
        "--entrada",
        type=int,
        default=1000000,
        help="Determina el tamaño de la entrada.",
    )
    _ = parser.add_argument(
        "-p",
        "--periodo",
        nargs='+',
        type=int,
        default=[1,2,4,5],
        help="Determina el periodo a buscar.",
    )
    args = parser.parse_args()

    sociables(App(args.entrada, args.periodo, criba_eratosthenes(args.entrada)))
    mostrar_tiempos_ejecución()
