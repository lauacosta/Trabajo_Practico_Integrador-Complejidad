# Acá moví código que me ocupa lugar y no estoy usando por ahora.

# TODO: Revisar qué tan mal implementé esto porque anda lentísimo jsj.
def criba_eratosthenes_segmentada(num: int) -> int:
    """
    Referencias:
    - https://cp-algorithms.com/algebra/sieve-of-eratosthenes.html
    """
    S = 10000
    primes = []
    nsqrt = int(sqrt(num))
    is_prime = [True for _ in range(nsqrt + 2)]

    for i in range(2, nsqrt + 1):
        if is_prime[i]:
            primes.append(i)
            for j in range(i * i, nsqrt + 1, i):
                is_prime[j] = False
    result = 0
    block = [None] * S
    for k in range(num + 1):
        if not k * S <= num:
            break

        block = [True for _ in range(len(block))]
        start = k * S
        for p in primes:
            start_idx = (start + p - 1) // p
            j = max(start_idx, p) * p - start
            for _ in range(j, S, p):
                block[j] = False
        if k == 0:
            block[0] = block[1] = False

        for i in range(S):
            if start + i <= num:
                if block[i]:
                    result += 1
    return result


def criba_eratosthenes_rango(L: int, R: int) -> list[int]:
    lim = int(sqrt(R))
    primes = []
    mark = [False for _ in range(lim + 1)]
    for i in range(2, lim + 1):
        if not mark[i]:
            primes.append(i)
            for j in range(i * i, lim + 1, i):
                mark[j] = True

    es_primo = [True for _ in range(R - L + 1)]
    for i in primes:
        start = max(i * i, (L + i - 1) // i * i)
        for j in range(start, R + 1, i):
            es_primo[j - L] = False
            if j == i and j not in primes:
                primes.append(j)

    if L == 1:
        es_primo[0] = False

    return primes


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

        if es_primo[i] == True:
            result.append(i)
            for j in range(i * i, num + 1, i * 2):
                es_primo[j] = False

    return result


def division_tentativa_serial(start, end) -> tuple[list[int], int]:
    ciclos = 0
    lista_factores = []
    while end % 2 == 0:
        print("RE LOCO")
        lista_factores.append(2)
        end = end // 2
        ciclos += 1

    for n in range(start, end, 2):
        if not n * n <= end:
            break

        while end % n == 0:
            lista_factores.append(n)
            end //= n
            ciclos += 1

        ciclos += 1

    if end > 1:
        lista_factores.append(end)

    return lista_factores, ciclos


def division_tentativa_primos(num: int, lista_primos: list[int]) -> list[int]:
    """
    El algoritmo más básico para factorizar un entero en números primos

    Referencias:
    https://cp-algorithms.com/algebra/factorization.html
    """
    ciclos = 0
    if num == 0 or num == 1:
        return []

    lista_factores = []
    for p in lista_primos:
        if p * p > num:
            break

        while num % p == 0:
            lista_factores.append(p)
            num //= p
            ciclos += 1

        ciclos += 1

    primo_mas_grande = max(lista_primos)
    if num > primo_mas_grande:
        factores, c = division_tentativa_serial(primo_mas_grande, num)
        lista_factores += factores
        print(f"Tomé {ciclos + c} ciclos")
        return lista_factores
    elif num != 1:
        lista_factores.append(num)

    return lista_factores
