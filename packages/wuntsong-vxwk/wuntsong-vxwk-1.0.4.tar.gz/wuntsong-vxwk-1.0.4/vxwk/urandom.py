import random


def generate_unique_number(length):
    numbers = "0123456789"
    result = [random.choice(numbers) for _ in range(length)]
    return ''.join(result)
