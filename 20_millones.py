from helpers import timer

cache = {}
cache_hits = 0




def binpower(base: int, e: int, mod: int) -> int:
    """
    https://cp-algorithms.com/algebra/primality_tests.html
    """
    result = 1
    base %= mod
    while e:
        if e & 1:
            result = result * base % mod
        base = base * base % mod
        e >>= 1

    return result


def check_composite(num: int, a: int, d: int, s: int) -> bool:
    """
    https://cp-algorithms.com/algebra/primality_tests.html
    """
    x = binpower(a, d, num)
    if x == 1 or x == (num - 1):
        return False
    for _ in range(1, s):
        x = x * x % num
        if x == (num - 1):
            return False

    return True


def miller_rabin_deterministico(num: int) -> bool:
    """
    https://cp-algorithms.com/algebra/primality_tests.html
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
        if check_composite(num, i, d, r):
            return False

    return True

@timer
def division_tentativa(num: int) -> list[int]:
    """
    https://cp-algorithms.com/algebra/factorization.html
    """

    factores = []
    for n in range(2, num):
        if not n * n <= num:
            break

        while num % n == 0:
            factores.append(n)
            num = int(num / n)

    if num > 1:
        factores.append(num)

    return factores

def suma_de_factores_propios_factorizado(num: int) -> int:
    """
    1) Obtener los factores a través de una tecnica de factorización.
    1.1) Si el número a factorizar es primo, conviene no utilizar un algoritmo de factorización
         ya que por definición sus factores son 1 y él mismo.
    1.2) Controlamos si el número, antes de ingresarlo al algoritmo, sea compuesto.
    2) Encontrar todas las combinaciones de los factores con sus exponentes.
    3) Realizar la sumatoria de los resultados de cada combinación excepto la primera.
    """

    result = 0

    factores = division_tentativa(num)
    # TODO: implementar cómo encontrar todas las combinaciones de factores.
    return result

@timer
def suma_de_factores_propios_fuerza_bruta(num: int) -> int:
    """
    Esta es la solución más facil pero también la más lenta.
    """
    # TODO: Revisar si introducir un caché sirve de algo para este tipo de problemas.
    if num in cache:
        global cache_hits
        cache_hits += 1
        return cache[num]

    result = 0
    for i in range(1, num - 1):
        if num % i == 0:
            result += i

    cache[num] = result
    return result

@timer
def numeros_sociables(start: int, num: int, arr: list[int]) -> tuple[bool, list[int]]:
    # if miller_rabin_deterministico(num):
    #     arr.append(num)
    #     return False, arr
    
    sum = suma_de_factores_propios_fuerza_bruta(num)
    # sum = suma_de_factores_propios_factorizado(num)

    # Si es así, significa que se cumplió el periodo, entonces devuelvo la lista.
    if sum == start:
        return True, arr

    # Observé que en una serie infinita la suma de los factores propios no es menor que el valor que estamos ingresando, entonces ya la descarto.
    # TODO: Ver si la observación es correcta y pensar si hay una mejor manera de hacer el control
    if sum < num:
        arr.append(0)
        return False, arr

    arr.append(sum)
    return numeros_sociables(start, sum, arr)

def serie_de_numeros_sociables(num: int, arr: list[int]) -> tuple[bool, list[int]]:
    """
    Referencias:
    - https://es.wikipedia.org/wiki/N%C3%BAmeros_sociables
    - https://es.wikipedia.org/wiki/Sucesi%C3%B3n_al%C3%ADcuota
    """
    arr.append(num)
    return numeros_sociables(num, num, arr)


if __name__ == "__main__":
    # Según wikipedia, el número sociable más pequeño es el 12_497
    # TODO: Ver cómo llega a verificar esto, así si lo podemos implementar podemos no gastarnos en verificar números a la fuerza.
    print(suma_de_factores_propios_fuerza_bruta(31))
    for num in range(1, 12497):
        print(f">>{num}")
        candidato, arr = serie_de_numeros_sociables(num, [])
        if candidato:
            if len(arr) == 2:
                print(f"El número {num} es un número amigo. {arr}")
            elif len(arr) >= 3:
                print(f"El número {num} es un número sociable. {arr}")
