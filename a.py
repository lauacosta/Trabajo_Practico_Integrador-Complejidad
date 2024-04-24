import random


def generate_random_number_of_length(length):
    min_value = 10 ** (length - 1)
    max_value = (10**length) - 1
    return random.randint(min_value, max_value)


# Example usage:
lengths = [2, 3, 4]  # Specify the lengths you want
for length in lengths:
    random_number = generate_random_number_of_length(length)
    print(f"Random number of length {length}: {random_number}")
