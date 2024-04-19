class Cache(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.contador_accesos = {}
        self.cache_hits = 0
        self.cache_refs = 0

    def __getitem__(self, key):
        self.cache_hits += 1
        self.contador_accesos[key] = self.contador_accesos.get(key,0) + 1
        return super().__getitem__(key)

class LFUCache(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.capacity = 1000000
        self.cache= {}
        self.contador_accesos = {}
        self.cache_hits = 0
        self.minimo_de_accesos = 10

    def __getitem__(self, key):
        self.cache_hits += 1
        self.contador_accesos[key] += 1
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        if key in self.cache:
            self.cache[key] = value
            self.contador_accesos[key] += 1
        else:
            if len(self.cache) >= self.capacity:
                print("LIMPIEZA")
                keys_con_menor_acceso = [k for k,v in self.contador_accesos.items() if v <= self.minimo_de_accesos]
                for k in keys_con_menor_acceso:
                    del self.cache[k]
                    del self.contador_accesos[k]

            self.cache[key] = value
            self.contador_accesos[key] = 1

def time_interval(interval):
    if interval < 0.001:
        return "{:10.3f} µs".format(interval * 1e6)
    elif interval < 1.0:
        return "{:10.3f} ms".format(interval * 1e3)
    else:
        return "{:10.3f} s".format(interval)


def func_name(func):
    return str(func).split(" ")[1]


def timer(func):
    import time

    # time.time() -> Segundos
    def wrapper(*wrapped_func_args):
        start_time = time.time()
        result = func(*wrapped_func_args)
        end_time = time.time()

        print(f"{func_name(func)} tomó: {time_interval(end_time-start_time)}")
        return result

    return wrapper


registro_tiempo = {}


def total_timer(func):
    import time

    def wrapper(*wrapped_func_args):
        start_time = time.time()
        result = func(*wrapped_func_args)
        end_time = time.time()

        registro_tiempo[func_name(func)] = registro_tiempo.get(func_name(func), 0) + (
            end_time - start_time
        )
        return result

    return wrapper


def mostrar_tiempos_ejecución():
    print("    Tiempos de ejecución de cada función:")
    for func_name, tiempo in registro_tiempo.items():
        print(f"      - {func_name}:")
        print(f"     {time_interval(tiempo)}")
