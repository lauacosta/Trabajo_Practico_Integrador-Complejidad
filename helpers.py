def time_interval(start, end):
    interval = end - start
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

        print(f"{func_name(func)} tomó: {time_interval(start_time, end_time)}")
        return result

    return wrapper
