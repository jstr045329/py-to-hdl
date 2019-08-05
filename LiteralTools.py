"""Contains tools to generate literals in VHDL"""


def insert_underscore(some_str, idx):
    _, remainder = divmod(len(some_str) - idx, 4)
    return remainder == 0 and idx > 0


def underscorify(y, prefix):
    z = ''
    for i in range(len(y)):
        if insert_underscore(y, i):
            z += "_"
        z += y[i]
    return prefix + z + '"'


def bin_literal(num_digits, n=1, use_underscores=True):
    """Like hex_literal(), but with single quotes."""
    y = bin(n)
    y = y[2:]
    if len(y) < num_digits:
        num_zeros = num_digits - len(y)
        zero_str = "0" * num_zeros
        y = zero_str + y
    if use_underscores:
        return underscorify(y, 'B"')
    return 'B"' + y + '"'


def hex_literal(num_digits, n=1, use_underscores=True):
    """Like bin_literal(), but with double quotes."""
    y = hex(n)
    y = y[2:]
    if len(y) < num_digits:
        num_zeros = num_digits - len(y)
        zero_str = "0" * num_zeros
        y = zero_str + y
    if use_underscores:
        return underscorify(y, 'X"')
    return 'X"' + y + '"'


def all_ones_binary(num_digits, use_underscores=True):
    if use_underscores:
        return underscorify("1"*num_digits, 'B"')
    return 'B"' + ("1" * num_digits) + '"'


def all_ones_hex(num_digits, use_underscores=True):
    if use_underscores:
        return underscorify("1" * num_digits, 'X"')
    return 'X"' + ("F" * num_digits) + '"'


if __name__ == "__main__":
    print(bin_literal(64, 2934872938))
    print(bin_literal(7, 1, use_underscores=False))
    print(bin_literal(7, 1, use_underscores=True))
    print(bin_literal(11, 72, use_underscores=False))
    print(bin_literal(11, 72, use_underscores=True))
    print(hex_literal(32, 93920394820394802934802934802394))
    print(hex_literal(33, 93920394820394802934802934802394))
    print(hex_literal(34, 93920394820394802934802934802394))
    print(hex_literal(35, 93920394820394802934802934802394))
