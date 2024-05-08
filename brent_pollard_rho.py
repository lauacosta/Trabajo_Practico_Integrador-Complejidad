
class BrentPollardPrime(AlgoritmoFactorizacion):
    #@total_timer
    @override
    def factorizar(self, num: int) -> dict[int, int]:
        def division_tentativa(n: int) -> int:
            for i in range(2, n + 1):
                if i * i > num:
                    break

                if n % i == 0:
                    return i
            return n

        lista_factores: list[int] = []
        lista_factores_primos: dict[int,int] = {}

        if miller_rabin_deterministico(num):
            return lista_factores_primos

        factor = brent_pollard_factor(num)
        lista_factores.append(num // factor)
        lista_factores.append(factor)

        while lista_factores:
            m = lista_factores[-1]
            _ = lista_factores.pop()

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
                factor = division_tentativa(m) if m < 100 else brent_pollard_factor(m)
                lista_factores.append(m // factor)
                lista_factores.append(factor)


        return lista_factores_primos


#@total_timer
def mult(a:int, b:int, mod:int) -> int:
    result = 0
    while b:
        if b & 1:
            result = (result + a) % mod

        a = (a + a) % mod
        b >>= 1

    return result

#@total_timer
def brent_pollard_factor(n: int):
    import random
    m = 1000
    a = x = y = ys = r= q = g = 0

    while True:
        a = int(random.randint(1, max_uint64))
        a %= n
        if not(a == 0 or a == n - 2):
            break
    y = int(random.randint(1, max_uint64)) % n
    r = 1
    q = 1

    while True:
        x = y
        for i in range(r):
            y = mult(y,y,n)
            y += a
            if y < a:
                y += (max_uint64 -n) + 1

            y %= n

        k = 0
        while True:
            i = 0
            while i < m and i < r - k:
                ys = y
                y = mult(y,y,n)
                y += a
                if y < a:
                    y += max_uint64 - n + 1
                y %= n

                q = mult(q, x-y, n) if x > y else mult(q, y-x, n)
                i += 1
            g = gcd(q,n)
            k += m
            if not (k < r and g == 1):
                break

        r <<= 1
        if g != 1:
            break

    if g == n:
        while True:
            ys = mult(ys,ys,n)
            ys += a
            if ys < a:
                ys += max_uint64 - n + 1

            ys %= n
            g = gcd(x-ys,n) if x > ys else gcd(ys-x, n)
            if g != 1:
                break
    return g
