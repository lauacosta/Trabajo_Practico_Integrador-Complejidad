def sociables(entrada: int, periodo: list[int]) -> list[list[int]]:
    app = App(entrada, periodo, criba_eratosthenes(entrada))
    resultado = app.run()
    return resultado


class App:
    def __init__(self, limite: int, periodo: list[int], lista_primos: list[int]):
        self.limite = limite
        self.periodo = periodo
        self.lista_primos = lista_primos
        self.cache_suma_factores = Cache()
        self.max_iteraciones = (
            5 if any(x > 5 for x in self.periodo) else max(self.periodo)
        )

        # Realmente está ad hoc para representar al conjunto de numeros sociables de que ya aparecieron.
        self.numeros_sociables_vistos: set[int] = set()

    def run(self) -> list[list[int]]:
        """
        Referencias:
        - https://djm.cc/sociable.txt
        """
        resultado: list[list[int]] = []
        comienzo = 6
        paso = 1
        fin = self.limite
        append = resultado.append

        # Algunos casos especiales:
        if self.periodo == [1]:
            paso = 2
            if self.limite < 35_000_000:
                fin = 8_128

        elif min(self.periodo) == 4 and 5 not in self.periodo:
            comienzo = 1_264_459

        elif self.periodo == [3]:
            return []

        sucesion_de_numeros_sociables = self.sucesion_de_numeros_sociables
        for num in range(comienzo, fin + 1, paso):
            es_candidato, sucesion = sucesion_de_numeros_sociables(num, [])
            if es_candidato and len(sucesion) in self.periodo:
                append(sucesion)

        # self.mostrar_informacion(f"Los numeros sociales hasta {(self.limite)}:")
        return resultado

    def sucesion_de_numeros_sociables(
        self, num: int, arr: list[int]
    ) -> tuple[bool, list[int]]:
        """
        Buscará encontrar si el número tiene una sucesión alícuota.

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

        return es_candidato, sucesion

    def construir_sucesion(
        self, start: int, num: int, arr: list[int]
    ) -> tuple[bool, list[int]]:
        """
        Devuelve verdadero o falso dependiendo si la sucesión, en donde cada término es la suma
        de los divisores propios del término anterior, es infinita.

        Referencias:
        - https://djm.cc/sociable.txt
        """

        if num == 14316 and 28 in self.periodo:
            max_iteraciones = 28
        else:
            max_iteraciones = self.max_iteraciones

        append = arr.append
        while max_iteraciones != 0:
            sum = self.suma_de_factores_propios_factorizado(num)

            # Significa que se cumplió el periodo, entonces devuelvo la lista.
            if sum == start:
                return True, arr

            # Detecta si una secuencia se vuelve cíclica pero no respecto al primer número.
            if sum in arr:
                return False, arr

            append(sum)
            num = sum
            max_iteraciones -= 1

        return False, arr

    def suma_de_factores_propios_factorizado(self, num: int) -> int:
        """
        1) Obtener los factores a través de una tecnica de factorización.
        2) Encontrar todas las combinaciones de los factores con sus exponentes.
        3) Realizar la sumatoria de los resultados de cada combinación excepto la primera.

        Referencias:
        - https://planetmath.org/formulaforsumofdivisors
        """
        from math import prod

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
            "-----------------------------------------------------------\n",
            f"{titulo}\n",
            f"  Elementos en el self.cache_suma_factores: {len(self.cache_suma_factores)}\n",
            f"  Cache refs: {(self.cache_suma_factores.cache_refs)}\n",
            f"  Cache hits: {(self.cache_suma_factores.cache_hits)} ({((self.cache_suma_factores.cache_hits / self.cache_suma_factores.cache_refs) * 100):1.3f}%)\n",
            f"  Elementos en el cache_numeros_sociables: {(len(self.numeros_sociables_vistos))}\n",
        ]

        print("".join(informacion))


def DivisionTentativa(num: int, lista_primos: list[int]) -> dict[int, int]:
    """
    El algoritmo más básico para factorizar un entero en números primos.

    Referencias:
    https://cp-algorithms.com/algebra/factorization.html
    """
    lista_factores: dict[int, int] = {}
    get = lista_factores.get
    if num == 0 or num == 1:
        return lista_factores

    for p in lista_primos:
        if p * p > num:
            break

        while num % p == 0:
            lista_factores[p] = get(p, 0) + 1
            num //= p

    if num > 1:
        lista_factores[num] = get(num, 0) + 1

    return lista_factores


def criba_eratosthenes(num: int) -> list[int]:
    """
    Encuentra todos los números primos menores a un número natural dado.

    Referencias:
    - https://cp-algorithms.com/algebra/sieve-of-eratosthenes.html
    """
    if num == 0 or num == 1:
        return []

    resultado: list[int] = []
    append = resultado.append
    es_primo = [True for _ in range(num + 1)]
    es_primo[0] = False
    es_primo[1] = False
    append(2)

    ## Hasta que no encuentre una mejor solución así se queda.
    if num == 3:
        append(3)
        return resultado

    for i in range(3, num + 1, 2):
        if not i * i <= num:
            break

        if es_primo[i]:
            append(i)
            for j in range(i * i, num + 1, i * 2):
                es_primo[j] = False

    return resultado


class Cache(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache_hits = 0
        self.cache_refs = 0

    def __getitem__(self, key):
        self.cache_hits += 1
        return super().__getitem__(key)


if __name__ == "__main__":
    print(sociables(2000000, [1, 2, 4, 5, 28]))
