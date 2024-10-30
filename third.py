import random

def generate_random_key():
    # genereate kunci
    return ''.join(random.choice('01') for _ in range(64))