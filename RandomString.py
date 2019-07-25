"""Generates a random string"""
import string
import random


def random_string(num_char=16):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(num_char))
