cache = {}
cache_hits = 0
def suma_de_factores_propios(num):
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

arr = []
def numeros_sociables(start, num):
    sum = suma_de_factores_propios(num)
    
    # Si es así, significa que se cumplió el periodo, entonces devuelvo la lista armada hasta entonces.
    if sum == start:
        return 

    # Observé que en una serie infinita la suma de los factores propios no es menor que el valor que estamos ingresando, entonces ya la descarto.
    # TODO: Ver si la observación es correcta y pensar si hay una mejor manera de hacer el control
    if sum < num:
        arr.append(0)
        return

    arr.append(sum)
    numeros_sociables(start, sum)
    

def serie_de_numeros_sociables(num):
    """
    Referencias:
    - https://es.wikipedia.org/wiki/N%C3%BAmeros_sociables
    - https://es.wikipedia.org/wiki/Sucesi%C3%B3n_al%C3%ADcuota
    """
    arr.append(num)
    numeros_sociables(num, num) 

if __name__ == "__main__":
    # Según wikipedia, el número sociable más pequeño es el 12_497
    # TODO: Ver cómo llega a verificar esto, así si lo podemos implementar podemos no gastarnos en verificar números a la fuerza.
    for num in range (1,12497):
        serie_de_numeros_sociables(num)
        print(f"El número {num} tiene una serie finita: {arr}")
        print(f"Hasta ahora, la cantidad de hits en el cache son: {cache_hits}")
        if arr[-1] != 0:
            if len(arr) == 1:
                print(f"El número {num} es un número perfecto")
            elif len(arr) == 2:
                print(f"El número {num} es un número amigo")
            else:
                print(f"El número {num} es un número sociable")
            print(arr)

        arr = []
