import unittest


# def lista_de_factores_propios(num: int) -> list[int]:
def lista_de_factores_propios(num):
    result = []
    for i in range(1, num - 1):
        if num % i == 0:
            result.append(i)

    return result


def suma_de_factores_propios_fuerza_bruta(num):
    result = 0
    for i in range(1, num - 1):
        if num % i == 0:
            result += i

    return result


arr = []


def numeros_sociables(start, num):
    sum = suma_de_factores_propios_fuerza_bruta(num)
    if sum == start:
        return

    arr.append(sum)
    numeros_sociables(start, sum)


def serie_de_numeros_sociables(start, num):
    """
    Referencias:
    - https://es.wikipedia.org/wiki/N%C3%BAmeros_sociables
    - https://es.wikipedia.org/wiki/Sucesi%C3%B3n_al%C3%ADcuota
    """
    arr.append(start)
    numeros_sociables(start, num)


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

    def test_serie_de_numeros_sociables_1264460(self):
        serie_de_numeros_sociables(1264460, 1264460)
        self.assertEqual(arr, [1264460, 1547860, 1727636, 1305184])


if __name__ == "__main__":
    unittest.main()
